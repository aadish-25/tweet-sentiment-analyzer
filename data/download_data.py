import os
import urllib.request
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(DATA_DIR, "tweets.csv")

# Kaggle Twitter Entity Sentiment Analysis mirror (74,682 tweets)
KAGGLE_TWITTER_URL = "https://raw.githubusercontent.com/Amolak001/Social-Media-Sentiment-Analysis/main/twitter_training.csv"
FALLBACK_TWEETEVAL_URL = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/train_text.txt"
FALLBACK_LABELS_URL = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/train_labels.txt"


def download_and_prepare_dataset(sample_per_class: int = 10000) -> pd.DataFrame:
    """
    Download and prepare a large, balanced tweet sentiment dataset.
    Prioritizes the Kaggle Twitter Sentiment corpus (74k+ tweets).
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Downloading Kaggle Twitter Sentiment dataset from mirror...")

    try:
        req = urllib.request.Request(KAGGLE_TWITTER_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw_df = pd.read_csv(resp, header=None, names=["id", "entity", "sentiment", "text"])

        raw_df = raw_df.dropna(subset=["text", "sentiment"])
        raw_df = raw_df[raw_df["sentiment"].isin(["Positive", "Negative", "Neutral"])].copy()
        raw_df["sentiment"] = raw_df["sentiment"].str.lower()

        # Create balanced dataset across Positive, Negative, and Neutral
        balanced_dfs = []
        for s in ["positive", "negative", "neutral"]:
            sub = raw_df[raw_df["sentiment"] == s]
            take_count = min(sample_per_class, len(sub))
            balanced_dfs.append(sub.sample(take_count, random_state=42))

        df = pd.concat(balanced_dfs, ignore_index=True)
        df["id"] = range(1, len(df) + 1)
        df = df[["id", "text", "sentiment"]].sample(frac=1.0, random_state=42).reset_index(drop=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Saved {len(df):,} balanced Kaggle tweets to {OUTPUT_FILE}")
        return df

    except Exception as e:
        print(f"Kaggle download failed ({e}). Falling back to TweetEval benchmark...")
        req_text = urllib.request.Request(FALLBACK_TWEETEVAL_URL, headers={"User-Agent": "Mozilla/5.0"})
        req_labels = urllib.request.Request(FALLBACK_LABELS_URL, headers={"User-Agent": "Mozilla/5.0"})

        with urllib.request.urlopen(req_text, timeout=15) as r:
            texts = r.read().decode("utf-8").splitlines()
        with urllib.request.urlopen(req_labels, timeout=15) as r:
            labels = r.read().decode("utf-8").splitlines()

        raw_df = pd.DataFrame({"text": texts, "label": labels})
        label_map = {"0": "negative", "1": "neutral", "2": "positive"}
        raw_df["sentiment"] = raw_df["label"].map(label_map)

        balanced_dfs = []
        for s in ["positive", "negative", "neutral"]:
            sub = raw_df[raw_df["sentiment"] == s]
            balanced_dfs.append(sub.sample(min(4000, len(sub)), random_state=42))

        df = pd.concat(balanced_dfs, ignore_index=True)
        df["id"] = range(1, len(df) + 1)
        df = df[["id", "text", "sentiment"]].sample(frac=1.0, random_state=42).reset_index(drop=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Saved {len(df):,} fallback tweets to {OUTPUT_FILE}")
        return df


if __name__ == "__main__":
    download_and_prepare_dataset()
