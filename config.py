import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Default dataset path
DATA_PATH = os.path.join(DATA_DIR, "tweets.csv")

# Model artifact paths
LR_MODEL_FILE = os.path.join(MODEL_DIR, "logistic_regression.joblib")
NB_MODEL_FILE = os.path.join(MODEL_DIR, "naive_bayes.joblib")
VEC_FILE = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")
METRICS_FILE = os.path.join(MODEL_DIR, "evaluation_metrics.joblib")

# Hyperparameters and split configuration
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_FEATURES = 8000
NGRAM_RANGE = (1, 2)
