# Tweet Sentiment Analysis System

An Information Retrieval mini project developed for the **Information Retrieval** curriculum (**Savitribai Phule Pune University - SPPU**).

This system provides **dual-model Sentiment Analysis for Tweets** (supporting direct text or live public Twitter/X URLs) using both **Logistic Regression** and **Multinomial Naive Bayes** over a **TF-IDF Vector Space Model**, along with real, computed evaluation metrics.

---

## Key Features

1. **Dual-Model Sentiment Inference:**
   - Evaluates any tweet using both **Logistic Regression** and **Multinomial Naive Bayes** simultaneously.
   - Provides predicted sentiment labels and class probability distributions for direct comparison.

2. **Live URL Extraction (No API Keys Needed):**
   - Supports direct text input or public Twitter / X URLs (e.g., `https://x.com/jack/status/20`).
   - Fetches live tweet text using Twitter's official oEmbed service and parses HTML via BeautifulSoup.

3. **Dedicated Offline Training (`train.py`):**
   - Clean, modular training script: trains vectorizer and both models once, then stores them to disk using `joblib`.
   - The web dashboard (`app.py`) loads pre-trained artifacts instantly without retraining on launch.

4. **Real Evaluation Metrics Comparison:**
   - Evaluated on a held-out test split of 2,400 tweets (20% stratified test split).
   - Direct comparison of **Accuracy**, **Precision (Macro)**, **Recall (Macro)**, **F1-Score (Macro)**, and **Log Loss**.

5. **Custom Dataset Support:**
   - Drop in any custom CSV file via terminal (`python train.py --data <file.csv>`) or directly in the web dashboard.
   - Intelligent auto-detection of text and sentiment columns.

---

## Project Structure

```
charming-planck/
├── config.py                     # Central configuration (paths, hyperparameters, test split ratio)
├── train.py                      # Dedicated training script for Logistic Regression & Naive Bayes
├── app.py                        # Streamlit web dashboard (clean UI, no sidebar, dual model comparison)
├── data/
│   ├── download_data.py          # Script to fetch/cache the 12,000 benchmark tweet dataset
│   └── tweets.csv                # 12,000 balanced benchmark tweets (Cardiff NLP TweetEval)
├── models/                       # Serialized joblib artifacts
│   ├── logistic_regression.joblib
│   ├── naive_bayes.joblib
│   ├── tfidf_vectorizer.joblib
│   └── evaluation_metrics.joblib
├── src/
│   ├── tweet_fetcher.py          # URL and text extraction module
│   └── sentiment_model.py        # Inference engine loading pre-trained models
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

---

## How Model Storage Works

Trained models are serialized to disk using **`joblib`**:
- `joblib.dump(lr_model, "models/logistic_regression.joblib")`
- `joblib.dump(nb_model, "models/naive_bayes.joblib")`
- `joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")`
- `joblib.dump(metrics, "models/evaluation_metrics.joblib")`

When `app.py` runs, it simply loads these binary `.joblib` files into memory in 0.05 seconds. It does not re-train every time you launch the app.

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Models (Terminal)
```bash
python train.py
```
*(To train on a custom dataset, run `python train.py --data path/to/your_file.csv`)*

### 3. Launch Web Dashboard
```bash
streamlit run app.py
```
Open `http://127.0.0.1:8501` in your browser.
