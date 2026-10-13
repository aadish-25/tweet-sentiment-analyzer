import argparse
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score,
    log_loss,
)
from sklearn.model_selection import train_test_split

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_FILE = os.path.join(MODEL_DIR, "sentiment_classifier.joblib")
VEC_FILE = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")
METRICS_FILE = os.path.join(MODEL_DIR, "evaluation_metrics.joblib")


def detect_columns(df: pd.DataFrame, text_col: str = None, label_col: str = None) -> tuple[str, str]:
    """Auto-detect text and sentiment columns if not explicitly provided."""
    cols = {col.lower(): col for col in df.columns}

    # Detect text column
    if text_col and text_col in df.columns:
        final_text = text_col
    else:
        text_candidates = ["text", "tweet", "tweettext", "tweet_text", "content", "sentence", "clean_text", "tweets"]
        final_text = None
        for candidate in text_candidates:
            if candidate in cols:
                final_text = cols[candidate]
                break
        if not final_text:
            # Fallback to first object/string column
            str_cols = df.select_dtypes(include=["object", "string"]).columns
            if len(str_cols) > 0:
                final_text = str_cols[0]
            else:
                raise ValueError("Could not find a text column in the dataset. Please specify column name.")

    # Detect label column
    if label_col and label_col in df.columns:
        final_label = label_col
    else:
        label_candidates = ["sentiment", "label", "target", "class", "category", "polarity"]
        final_label = None
        for candidate in label_candidates:
            if candidate in cols:
                final_label = cols[candidate]
                break
        if not final_label:
            remaining = [c for c in df.columns if c != final_text]
            if len(remaining) > 0:
                final_label = remaining[0]
            else:
                raise ValueError("Could not find a sentiment/label column in the dataset. Please specify column name.")

    return final_text, final_label


def normalize_sentiment_labels(series: pd.Series) -> pd.Series:
    """Normalize sentiment values into standard lowercase strings: positive, negative, neutral."""
    # Handle numeric encodings
    if pd.api.types.is_numeric_dtype(series):
        unique_vals = set(series.dropna().unique())
        # Cardiff / SemEval 0: neg, 1: neu, 2: pos
        if unique_vals.issubset({0, 1, 2}):
            mapping = {0: "negative", 1: "neutral", 2: "positive"}
            return series.map(mapping)
        # -1, 0, 1
        elif unique_vals.issubset({-1, 0, 1}):
            mapping = {-1: "negative", 0: "neutral", 1: "positive"}
            return series.map(mapping)
        # Sentiment140: 0 = neg, 4 = pos
        elif unique_vals.issubset({0, 2, 4}):
            mapping = {0: "negative", 2: "neutral", 4: "positive"}
            return series.map(mapping)

    # String mapping
    s = series.astype(str).str.strip().str.lower()
    mapping = {
        "pos": "positive",
        "positive": "positive",
        "1": "positive",
        "2": "positive",
        "4": "positive",
        "neg": "negative",
        "negative": "negative",
        "-1": "negative",
        "0": "negative",
        "neu": "neutral",
        "neutral": "neutral",
    }
    return s.map(lambda x: mapping.get(x, x))


class SentimentEngine:
    """Modular sentiment classification engine using scikit-learn TF-IDF and Logistic Regression."""

    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.metrics = None
        self.classes_ = ["negative", "neutral", "positive"]

    def prepare_data(self, data_path_or_df, text_col: str = None, label_col: str = None) -> pd.DataFrame:
        """Load and clean dataset with flexible column support."""
        if isinstance(data_path_or_df, pd.DataFrame):
            df = data_path_or_df.copy()
        else:
            df = pd.read_csv(data_path_or_df)

        actual_text, actual_label = detect_columns(df, text_col=text_col, label_col=label_col)
        clean_df = df[[actual_text, actual_label]].dropna().copy()
        clean_df.columns = ["text", "sentiment"]
        clean_df["sentiment"] = normalize_sentiment_labels(clean_df["sentiment"])
        clean_df = clean_df.dropna(subset=["sentiment"])

        # Filter out classes with too few examples (< 10)
        class_counts = clean_df["sentiment"].value_counts()
        valid_classes = class_counts[class_counts >= 10].index
        clean_df = clean_df[clean_df["sentiment"].isin(valid_classes)]

        if len(clean_df["sentiment"].unique()) < 2:
            raise ValueError(f"Dataset must have at least 2 distinct sentiment classes, found: {list(clean_df['sentiment'].unique())}")

        return clean_df

    def train(self, data_path_or_df, text_col: str = None, label_col: str = None, force_retrain: bool = False):
        """Train TF-IDF vectorizer and Logistic Regression classifier with real evaluation metrics."""
        os.makedirs(MODEL_DIR, exist_ok=True)

        if not force_retrain and isinstance(data_path_or_df, str) and os.path.exists(MODEL_FILE) and os.path.exists(VEC_FILE) and os.path.exists(METRICS_FILE):
            self.model = joblib.load(MODEL_FILE)
            self.vectorizer = joblib.load(VEC_FILE)
            self.metrics = joblib.load(METRICS_FILE)
            self.classes_ = list(self.model.classes_)
            return self.metrics

        df = self.prepare_data(data_path_or_df, text_col=text_col, label_col=label_col)

        # 80/20 stratified train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            df["text"], df["sentiment"], test_size=0.2, random_state=42, stratify=df["sentiment"]
        )

        # TF-IDF Vector Space representation (sublinear scaling + n-grams)
        self.vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # Multi-class Logistic Regression with calibrated probability outputs
        self.model = LogisticRegression(max_iter=600, C=1.5, random_state=42)
        self.model.fit(X_train_vec, y_train)
        self.classes_ = sorted(list(self.model.classes_))

        # Real test set evaluation
        y_pred = self.model.predict(X_test_vec)
        y_prob = self.model.predict_proba(X_test_vec)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred, labels=self.classes_)

        # ROC-AUC (OVR)
        try:
            roc_auc = float(roc_auc_score(y_test, y_prob, multi_class="ovr"))
        except Exception:
            roc_auc = 0.0

        # Log Loss (Cross Entropy)
        try:
            loss = float(log_loss(y_test, y_prob))
        except Exception:
            loss = 0.0

        # Sample 100 test predictions for transparency
        sample_size = min(100, len(y_test))
        sample_indices = np.random.RandomState(42).choice(len(y_test), size=sample_size, replace=False)
        test_samples = []
        x_test_list = list(X_test)
        y_test_list = list(y_test)
        for idx in sample_indices:
            pred_class = y_pred[idx]
            actual_class = y_test_list[idx]
            max_prob = float(np.max(y_prob[idx]))
            test_samples.append({
                "text": x_test_list[idx],
                "actual": actual_class,
                "predicted": pred_class,
                "confidence": round(max_prob, 3),
                "is_correct": bool(pred_class == actual_class),
            })

        self.metrics = {
            "accuracy": float(acc),
            "roc_auc": float(roc_auc),
            "log_loss": float(loss),
            "report": report,
            "confusion_matrix": conf_matrix.tolist(),
            "classes": self.classes_,
            "total_samples": int(len(df)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "vocab_size": int(len(self.vectorizer.vocabulary_)),
            "sample_test_predictions": test_samples,
        }

        # Cache trained artifacts
        joblib.dump(self.model, MODEL_FILE)
        joblib.dump(self.vectorizer, VEC_FILE)
        joblib.dump(self.metrics, METRICS_FILE)

        return self.metrics

    def predict(self, text: str) -> dict:
        """Predict sentiment, probability breakdown, and top contributing terms."""
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Model is not loaded. Train or load existing model first.")

        text_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vec)[0]
        probabilities = self.model.predict_proba(text_vec)[0]

        prob_dict = {cls: float(prob) for cls, prob in zip(self.model.classes_, probabilities)}

        # Extract top influential tokens present in the input text
        feature_names = self.vectorizer.get_feature_names_out()
        nonzero_indices = text_vec.nonzero()[1]

        token_weights = []
        pred_idx = list(self.model.classes_).index(prediction)
        for idx in nonzero_indices:
            term = feature_names[idx]
            weight = self.model.coef_[pred_idx][idx]
            token_weights.append((term, float(weight)))

        token_weights.sort(key=lambda x: x[1], reverse=True)

        return {
            "prediction": prediction,
            "confidence": prob_dict[prediction],
            "probabilities": prob_dict,
            "top_terms": token_weights[:5],
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Tweet Sentiment Analysis Model on any dataset.")
    parser.add_argument("--data", type=str, default=None, help="Path to CSV dataset file")
    parser.add_argument("--text-col", type=str, default=None, help="Name of text/tweet column (optional, auto-detected)")
    parser.add_argument("--label-col", type=str, default=None, help="Name of sentiment/label column (optional, auto-detected)")
    parser.add_argument("--force", action="store_true", help="Force retrain even if cached models exist")
    args = parser.parse_args()

    default_data = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tweets.csv")
    csv_file = args.data if args.data else default_data

    print(f"Training on dataset: {csv_file}")
    engine = SentimentEngine()
    metrics = engine.train(csv_file, text_col=args.text_col, label_col=args.label_col, force_retrain=True)

    print("\n" + "=" * 50)
    print("TRAINING & EVALUATION SUMMARY (100% REAL TEST SET)")
    print("=" * 50)
    print(f"Total Dataset Samples: {metrics['total_samples']:,}")
    print(f"Train / Test Split:    {metrics['train_samples']:,} / {metrics['test_samples']:,}")
    print(f"Vocabulary Size:       {metrics['vocab_size']:,}")
    print(f"Test Accuracy:         {metrics['accuracy'] * 100:.2f}%")
    print(f"ROC-AUC (OVR):         {metrics['roc_auc']:.4f}")
    print(f"Log Loss:              {metrics['log_loss']:.4f}")
    print("=" * 50)
