# Tweet Sentiment Analysis & Information Retrieval System

A comprehensive Information Retrieval (IR) mini project designed for the **Information Retrieval** curriculum (**Savitribai Phule Pune University - SPPU**).

This system combines **Ranked Document Retrieval (Vector Space Model)** with **Machine Learning Sentiment Categorization** and **Live Tweet Ingestion from URLs**.

---

## 🚀 Key Features

1. **Dual Input Sentiment Analyzer:**
   - **Direct Text:** Enter any custom tweet or text sentence.
   - **Live Tweet URL:** Paste any public `twitter.com` or `x.com` status link (e.g., `https://x.com/jack/status/20`). The system fetches the tweet text and author metadata via Twitter's public oEmbed service without requiring developer API keys.
   - **Feature Attribution:** Displays the influential keywords and their mathematical weights that drove the classification.
   - **Probability Breakdown:** Calibrated confidence metrics across Positive, Negative, and Neutral sentiment.

2. **Ranked Tweet Search Engine with Sentiment Filtering:**
   - Vector Space Model retrieval over 12,000 indexed tweets using TF-IDF representation and cosine similarity.
   - Faceted sentiment filtering: retrieve only *Positive*, *Negative*, or *Neutral* tweets matching a keyword query (e.g., find all negative tweets about *"delayed flight"* or positive tweets about *"camera quality"*).
   - Highlights overlapping matched terms and shows IR relevance scores.

3. **Evaluation & Performance Dashboard:**
   - Precision, Recall, F1-Score, and Overall Accuracy on held-out test data.
   - Confusion Matrix for multi-class classification.
   - Real-time search latency measurement in milliseconds.

---

## 📚 Mapping to the Information Retrieval Syllabus

| Syllabus Unit | Concept Implemented in Project | Implementation Details |
|---|---|---|
| **Unit I: Basic IR Models** | Vector Space Model (TF-IDF Weighting) | Scikit-learn `TfidfVectorizer` with sublinear TF scaling, n-grams, and L2 normalization |
| **Unit II: Ranked Retrieval** | Query Processing & Cosine Similarity | Document-term matrix similarity calculation, top-$K$ ranking |
| **Unit IV: Categorization & Filtering** | Supervised Classification & Faceted Filtering | Multi-class `LogisticRegression` for sentiment classification; faceted sentiment filtering over IR search results |
| **Unit V: Measuring Effectiveness** | Evaluation Metrics | Accuracy, Macro F1, Confusion Matrix, per-class Precision/Recall |
| **Unit VI: Web Data Ingestion** | Live Data Extraction | Twitter/X oEmbed endpoint and `BeautifulSoup` HTML parsing |

---

## 🛠️ Project Structure

```
charming-planck/
├── data/
│   ├── download_data.py          # Script to fetch/prepare the balanced benchmark dataset
│   └── tweets.csv                # 12,000 balanced benchmark tweets (positive, negative, neutral)
├── models/
│   ├── sentiment_classifier.joblib # Trained classifier
│   ├── tfidf_vectorizer.joblib    # Fitted TF-IDF vectorizer
│   └── evaluation_metrics.joblib  # Cached evaluation metrics
├── src/
│   ├── tweet_fetcher.py          # Fetches tweet text from Twitter/X URLs or direct text
│   ├── sentiment_model.py        # TF-IDF + Logistic Regression classification engine
│   └── search_engine.py          # Ranked IR search engine with sentiment filtering
├── app.py                        # Streamlit web application dashboard
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation and setup instructions
```

---

## 💻 Installation & Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py
```
*The app will automatically start at `http://localhost:8501`.*

---

## 🧪 Sample Inputs for Demo / Viva

### Sample Tweet URLs to Test:
- `https://x.com/jack/status/20` (Jack Dorsey's first tweet: *"just setting up my twttr"*)
- `https://twitter.com/Twitter/status/20`

### Sample Text Inputs:
- **Positive:** `"The new camera sensor and battery optimization are absolutely phenomenal!"`
- **Negative:** `"Worst customer support ever, delayed flight for 6 hours with no refund."`
- **Neutral:** `"The annual developer conference will take place this Thursday at 10 AM."`

### Sample IR Search Queries:
- `game delayed` *(Filter: Negative)*
- `amazing battery` *(Filter: Positive)*
- `scheduled meeting` *(Filter: Neutral)*
