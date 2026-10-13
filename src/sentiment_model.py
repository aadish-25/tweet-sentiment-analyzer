import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
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

        # 80/20 train-test split for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            df["text"], df["sentiment"], test_size=0.2, random_state=42, stratify=df["sentiment"]
        )

        # Standard TF-IDF Vector Space representation with stop-words and unigrams+bigrams
        self.vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # Logistic Regression with probabilistic calibration
        self.model = LogisticRegression(max_iter=600, C=1.5, random_state=42)
        self.model.fit(X_train_vec, y_train)
        self.classes_ = list(self.model.classes_)

        # Evaluation metrics
        y_pred = self.model.predict(X_test_vec)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred, labels=self.classes_)

        self.metrics = {
            "accuracy": acc,
            "report": report,
            "confusion_matrix": conf_matrix.tolist(),
            "classes": self.classes_,
            "total_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "vocab_size": len(self.vectorizer.vocabulary_),
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
    import os
    data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tweets.csv")
    engine = SentimentEngine()
    metrics = engine.train(data_file)
    print("Training Complete. Accuracy:", f"{metrics['accuracy']:.4f}")
    sample = "Terrible delay and horrible flight experience!"
    print("Sample Prediction:", engine.predict(sample))
