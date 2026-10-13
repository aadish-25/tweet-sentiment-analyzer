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


class SentimentEngine:
    """Sentiment classification engine using scikit-learn TF-IDF and Logistic Regression."""

    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.metrics = None
        self.classes_ = ["negative", "neutral", "positive"]

    def train(self, data_path: str, force_retrain: bool = False):
        os.makedirs(MODEL_DIR, exist_ok=True)

        if not force_retrain and os.path.exists(MODEL_FILE) and os.path.exists(VEC_FILE) and os.path.exists(METRICS_FILE):
            self.model = joblib.load(MODEL_FILE)
            self.vectorizer = joblib.load(VEC_FILE)
            self.metrics = joblib.load(METRICS_FILE)
            self.classes_ = list(self.model.classes_)
            return self.metrics

        df = pd.read_csv(data_path)
        df = df.dropna(subset=["text", "sentiment"])

        # 80/20 stratified train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            df["text"], df["sentiment"], test_size=0.2, random_state=42, stratify=df["sentiment"]
        )

        # Standard TF-IDF representation
        self.vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # Logistic Regression
        self.model = LogisticRegression(max_iter=600, C=1.5, random_state=42)
        self.model.fit(X_train_vec, y_train)
        self.classes_ = list(self.model.classes_)

        # Real test set evaluation
        y_pred = self.model.predict(X_test_vec)
        y_prob = self.model.predict_proba(X_test_vec)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred, labels=self.classes_)
        roc_auc = roc_auc_score(y_test, y_prob, multi_class="ovr")
        loss = log_loss(y_test, y_prob)

        # Build real test prediction sample table for transparency
        sample_indices = np.random.RandomState(42).choice(len(y_test), size=min(100, len(y_test)), replace=False)
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
            raise RuntimeError("Model is not loaded. Run train() or load existing model first.")

        text_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vec)[0]
        probabilities = self.model.predict_proba(text_vec)[0]

        prob_dict = {cls: float(prob) for cls, prob in zip(self.classes_, probabilities)}

        # Extract top influential tokens present in the input text
        feature_names = self.vectorizer.get_feature_names_out()
        nonzero_indices = text_vec.nonzero()[1]

        token_weights = []
        pred_idx = self.classes_.index(prediction)
        for idx in nonzero_indices:
            term = feature_names[idx]
            weight = self.model.coef_[pred_idx][idx]
            token_weights.append((term, float(weight)))

        # Sort tokens by positive contribution to the predicted class
        token_weights.sort(key=lambda x: x[1], reverse=True)

        return {
            "prediction": prediction,
            "confidence": prob_dict[prediction],
            "probabilities": prob_dict,
            "top_terms": token_weights[:5],
        }


if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tweets.csv")
    engine = SentimentEngine()
    metrics = engine.train(data_file, force_retrain=True)
    print("Training Complete. Accuracy:", f"{metrics['accuracy']:.4f}")
    print("ROC-AUC:", f"{metrics['roc_auc']:.4f}")
    print("Log Loss:", f"{metrics['log_loss']:.4f}")
