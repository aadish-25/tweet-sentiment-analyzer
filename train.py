import argparse
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from sklearn.model_selection import train_test_split

import config


def detect_columns(df: pd.DataFrame, text_col: str = None, label_col: str = None) -> tuple[str, str]:
    """Auto-detect text and sentiment columns if not explicitly specified."""
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
            str_cols = df.select_dtypes(include=["object", "string"]).columns
            if len(str_cols) > 0:
                final_text = str_cols[0]
            else:
                raise ValueError("Could not find a text column in the dataset.")

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
                raise ValueError("Could not find a sentiment label column in the dataset.")

    return final_text, final_label


def normalize_sentiment_labels(series: pd.Series) -> pd.Series:
    """Normalize sentiment values to lowercase standard strings: negative, neutral, positive."""
    if pd.api.types.is_numeric_dtype(series):
        unique_vals = set(series.dropna().unique())
        if unique_vals.issubset({0, 1, 2}):
            return series.map({0: "negative", 1: "neutral", 2: "positive"})
        elif unique_vals.issubset({-1, 0, 1}):
            return series.map({-1: "negative", 0: "neutral", 1: "positive"})
        elif unique_vals.issubset({0, 2, 4}):
            return series.map({0: "negative", 2: "neutral", 4: "positive"})

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


def prepare_dataset(data_source, text_col: str = None, label_col: str = None) -> pd.DataFrame:
    """Load and prepare dataframe from path or existing DataFrame."""
    if isinstance(data_source, pd.DataFrame):
        df = data_source.copy()
    else:
        df = pd.read_csv(data_source)

    actual_text, actual_label = detect_columns(df, text_col=text_col, label_col=label_col)
    clean_df = df[[actual_text, actual_label]].dropna().copy()
    clean_df.columns = ["text", "sentiment"]
    clean_df["sentiment"] = normalize_sentiment_labels(clean_df["sentiment"])
    clean_df = clean_df.dropna(subset=["sentiment"])

    # Require minimum samples per class
    counts = clean_df["sentiment"].value_counts()
    valid_classes = counts[counts >= 10].index
    clean_df = clean_df[clean_df["sentiment"].isin(valid_classes)]

    if len(clean_df["sentiment"].unique()) < 2:
        raise ValueError("Dataset must have at least 2 distinct sentiment classes.")

    return clean_df


def train_models(data_source=None, text_col: str = None, label_col: str = None) -> dict:
    """
    Train TF-IDF vectorizer, Logistic Regression, and Naive Bayes models.
    Evaluates both on the same test split and saves serialized artifacts.
    """
    if data_source is None:
        data_source = config.DATA_PATH

    os.makedirs(config.MODEL_DIR, exist_ok=True)
    df = prepare_dataset(data_source, text_col=text_col, label_col=label_col)

    # Stratified train-test split (80/20) with fixed random seed
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["sentiment"],
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=df["sentiment"],
    )

    # TF-IDF Feature Extraction
    vectorizer = TfidfVectorizer(
        max_features=config.MAX_FEATURES,
        ngram_range=config.NGRAM_RANGE,
        stop_words="english",
        sublinear_tf=True,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Model 1: Logistic Regression
    lr_model = LogisticRegression(max_iter=600, C=1.5, random_state=config.RANDOM_STATE)
    lr_model.fit(X_train_vec, y_train)

    # Model 2: Multinomial Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_vec, y_train)

    # Evaluation on the exact same test split
    lr_preds = lr_model.predict(X_test_vec)
    lr_probs = lr_model.predict_proba(X_test_vec)

    nb_preds = nb_model.predict(X_test_vec)
    nb_probs = nb_model.predict_proba(X_test_vec)

    classes = sorted(list(lr_model.classes_))

    metrics = {
        "dataset_info": {
            "total_samples": int(len(df)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "vocabulary_size": int(len(vectorizer.vocabulary_)),
            "classes": classes,
        },
        "logistic_regression": {
            "accuracy": float(accuracy_score(y_test, lr_preds)),
            "precision": float(precision_score(y_test, lr_preds, average="macro", zero_division=0)),
            "recall": float(recall_score(y_test, lr_preds, average="macro", zero_division=0)),
            "f1_score": float(f1_score(y_test, lr_preds, average="macro", zero_division=0)),
            "log_loss": float(log_loss(y_test, lr_probs)),
        },
        "naive_bayes": {
            "accuracy": float(accuracy_score(y_test, nb_preds)),
            "precision": float(precision_score(y_test, nb_preds, average="macro", zero_division=0)),
            "recall": float(recall_score(y_test, nb_preds, average="macro", zero_division=0)),
            "f1_score": float(f1_score(y_test, nb_preds, average="macro", zero_division=0)),
            "log_loss": float(log_loss(y_test, nb_probs)),
        },
    }

    # Save artifacts to disk using joblib
    joblib.dump(lr_model, config.LR_MODEL_FILE)
    joblib.dump(nb_model, config.NB_MODEL_FILE)
    joblib.dump(vectorizer, config.VEC_FILE)
    joblib.dump(metrics, config.METRICS_FILE)

    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Sentiment Analysis Models (Logistic Regression & Naive Bayes)")
    parser.add_argument("--data", type=str, default=None, help="Path to custom CSV dataset")
    parser.add_argument("--text-col", type=str, default=None, help="Text column name")
    parser.add_argument("--label-col", type=str, default=None, help="Sentiment label column name")
    args = parser.parse_args()

    data_file = args.data if args.data else config.DATA_PATH
    print(f"Loading and training on: {data_file}")
    results = train_models(data_source=data_file, text_col=args.text_col, label_col=args.label_col)

    d_info = results["dataset_info"]
    lr_m = results["logistic_regression"]
    nb_m = results["naive_bayes"]

    print("\n" + "=" * 65)
    print("TRAINING COMPLETE - EVALUATION METRICS COMPARISON (TEST SPLIT)")
    print("=" * 65)
    print(f"Total Samples: {d_info['total_samples']:,} | Train: {d_info['train_samples']:,} | Test: {d_info['test_samples']:,}")
    print(f"Vocabulary Features: {d_info['vocabulary_size']:,}")
    print("-" * 65)
    print(f"{'Metric':<18} | {'Logistic Regression':<20} | {'Naive Bayes':<15}")
    print("-" * 65)
    print(f"{'Accuracy':<18} | {lr_m['accuracy'] * 100:>18.2f}% | {nb_m['accuracy'] * 100:>13.2f}%")
    print(f"{'Precision (Macro)':<18} | {lr_m['precision'] * 100:>18.2f}% | {nb_m['precision'] * 100:>13.2f}%")
    print(f"{'Recall (Macro)':<18} | {lr_m['recall'] * 100:>18.2f}% | {nb_m['recall'] * 100:>13.2f}%")
    print(f"{'F1-Score (Macro)':<18} | {lr_m['f1_score'] * 100:>18.2f}% | {nb_m['f1_score'] * 100:>13.2f}%")
    print(f"{'Log Loss':<18} | {lr_m['log_loss']:>19.4f} | {nb_m['log_loss']:>14.4f}")
    print("=" * 65)
    print(f"Models saved in: {config.MODEL_DIR}/")
