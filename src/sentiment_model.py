import os
import sys
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SentimentEngine:
    """Inference engine loading pre-trained Logistic Regression and Naive Bayes models."""

    def __init__(self):
        self.lr_model = None
        self.nb_model = None
        self.vectorizer = None
        self.metrics = None
        self.classes_ = ["negative", "neutral", "positive"]
        self.load_models()

    def load_models(self):
        """Load trained model artifacts from disk."""
        if not (os.path.exists(config.LR_MODEL_FILE) and os.path.exists(config.NB_MODEL_FILE) and os.path.exists(config.VEC_FILE)):
            from train import train_models
            self.metrics = train_models()

        self.lr_model = joblib.load(config.LR_MODEL_FILE)
        self.nb_model = joblib.load(config.NB_MODEL_FILE)
        self.vectorizer = joblib.load(config.VEC_FILE)
        if os.path.exists(config.METRICS_FILE):
            self.metrics = joblib.load(config.METRICS_FILE)

        self.classes_ = sorted(list(self.lr_model.classes_))

    def predict(self, text: str) -> dict:
        """Run inference using both Logistic Regression and Naive Bayes."""
        text_vec = self.vectorizer.transform([text])

        # Logistic Regression
        lr_pred = str(self.lr_model.predict(text_vec)[0])
        lr_probs = self.lr_model.predict_proba(text_vec)[0]
        lr_dict = {cls: float(prob) for cls, prob in zip(self.classes_, lr_probs)}

        # Naive Bayes
        nb_pred = str(self.nb_model.predict(text_vec)[0])
        nb_probs = self.nb_model.predict_proba(text_vec)[0]
        nb_dict = {cls: float(prob) for cls, prob in zip(self.classes_, nb_probs)}

        return {
            "logistic_regression": {
                "prediction": lr_pred,
                "confidence": lr_dict[lr_pred],
                "probabilities": lr_dict,
            },
            "naive_bayes": {
                "prediction": nb_pred,
                "confidence": nb_dict[nb_pred],
                "probabilities": nb_dict,
            },
        }


if __name__ == "__main__":
    engine = SentimentEngine()
    test_phrase = "Loving the incredible camera quality and smooth software update!"
    res = engine.predict(test_phrase)
    print("Testing phrase:", test_phrase)
    print("Logistic Regression:", res["logistic_regression"])
    print("Naive Bayes:", res["naive_bayes"])
