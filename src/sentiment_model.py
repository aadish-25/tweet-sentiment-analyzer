import os
import sys
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SentimentEngine:
    """Inference engine loading pre-trained Logistic Regression model."""

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metrics = None
        self.classes_ = ["negative", "neutral", "positive"]
        self.load_models()

    def load_models(self):
        """Load trained Logistic Regression artifacts from disk."""
        if not (os.path.exists(config.MODEL_FILE) and os.path.exists(config.VEC_FILE)):
            from train import train_models
            self.metrics = train_models()

        self.model = joblib.load(config.MODEL_FILE)
        self.vectorizer = joblib.load(config.VEC_FILE)
        if os.path.exists(config.METRICS_FILE):
            self.metrics = joblib.load(config.METRICS_FILE)

        self.classes_ = sorted(list(self.model.classes_))

    def predict(self, text: str) -> dict:
        """Run sentiment classification and term attribution on input text."""
        text_vec = self.vectorizer.transform([text])

        pred_class = str(self.model.predict(text_vec)[0])
        probabilities = self.model.predict_proba(text_vec)[0]
        prob_dict = {cls: float(prob) for cls, prob in zip(self.classes_, probabilities)}

        # Extract top influential vocabulary tokens
        feature_names = self.vectorizer.get_feature_names_out()
        nonzero_indices = text_vec.nonzero()[1]

        token_weights = []
        pred_idx = self.classes_.index(pred_class)
        for idx in nonzero_indices:
            term = feature_names[idx]
            weight = self.model.coef_[pred_idx][idx]
            token_weights.append((term, float(weight)))

        token_weights.sort(key=lambda x: x[1], reverse=True)

        return {
            "prediction": pred_class,
            "confidence": prob_dict[pred_class],
            "probabilities": prob_dict,
            "top_terms": token_weights[:5],
        }


if __name__ == "__main__":
    engine = SentimentEngine()
    test_phrase = "This is the best hotel in India."
    print("Testing phrase:", test_phrase)
    print("Prediction:", engine.predict(test_phrase))
