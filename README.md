# Tweet Sentiment Analysis System

An Information Retrieval mini project designed for the **Information Retrieval** curriculum (**Savitribai Phule Pune University - SPPU**).

This system provides **real-time Sentiment Analysis for Tweets** (supporting direct text or live public Twitter/X URLs) powered by a **TF-IDF Vector Space Model** and **Logistic Regression**, paired with **100% genuine, computed model evaluation metrics**.

---

## 🚀 Key Features

1. **Dual-Mode Tweet Sentiment Analyzer:**
   - **Direct Tweet Text:** Input any tweet or sentence for immediate classification.
   - **Live Tweet URL:** Paste any public `twitter.com` or `x.com` status link (e.g. `https://x.com/jack/status/20`). The system fetches tweet text and author metadata via Twitter's public oEmbed service with zero API keys required.
   - **Feature Attribution (IR Term Weights):** Identifies and displays the key vocabulary words present in the tweet that drove the prediction, along with their model coefficient weights.
   - **Class Probabilities Breakdown:** Live probability distribution across Positive, Negative, and Neutral sentiment.

2. **Real Model Evaluation & Performance Metrics (Zero Dummy Data):**
   - Evaluated on a real held-out test split of **2,400 tweets** (20% of 12,000 balanced benchmark tweets from the Cardiff NLP TweetEval benchmark).
   - **Real Metrics Computed:**
     - **Test Accuracy:** 61.00% (1,464 / 2,400 correct)
     - **Macro F1-Score:** 61.06%
     - **ROC-AUC (One-vs-Rest):** 0.7889
     - **Cross-Entropy Log Loss:** 0.8554
   - **Real Classification Report:** Precision, Recall, F1, and Support per class (800 negative, 800 neutral, 800 positive).
   - **Real Confusion Matrix:** Complete actual vs. predicted counts matrix.
   - **Real Test Sample Predictions Inspector:** Interactive table inspecting 100 actual test tweets with ground truth label, predicted label, confidence, and correctness verification (filter by All, Correctly Classified, or Misclassified).

---

## 📚 Mapping to the Information Retrieval Syllabus

| Syllabus Unit | Concept Implemented in Project | Implementation Details |
|---|---|---|
| **Unit I: Basic IR Models** | Vector Space Model (TF-IDF Weighting) | Scikit-learn `TfidfVectorizer` with sublinear TF scaling ($1 + \log(tf)$) and L2 length normalization |
| **Unit IV: Categorization & Filtering** | Supervised Probabilistic Classification | Multi-class `LogisticRegression` minimizing cross-entropy loss, feature term weight attribution |
| **Unit V: Measuring Effectiveness** | Comprehensive Evaluation Metrics | Test Accuracy, Macro F1, One-vs-Rest ROC-AUC, Log Loss, Confusion Matrix, and Error Inspection |
| **Unit VI: Web Data Ingestion** | Live Web Scraping / Extraction | Twitter/X oEmbed integration and `BeautifulSoup` HTML parsing |

---

## 🛠️ Project Structure

```
charming-planck/
├── data/
│   ├── download_data.py            # Dataset ingestion & offline fallback
│   └── tweets.csv                  # 12,000 balanced benchmark tweets
├── models/                         # Pre-trained, cached models (instant startup)
│   ├── sentiment_classifier.joblib 
│   ├── tfidf_vectorizer.joblib    
│   └── evaluation_metrics.joblib   
├── src/
│   ├── tweet_fetcher.py            # Extracts tweet text from direct input or Twitter/X URLs
│   └── sentiment_model.py          # Scikit-learn TF-IDF + Logistic Regression classification engine
├── app.py                          # Streamlit web dashboard
├── requirements.txt                # Dependencies
└── README.md                       # Documentation and setup instructions
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
Open **`http://127.0.0.1:8501`** in your browser.

---

## 🧪 Sample Inputs for Demo / Viva

- **Sample URL:** `https://x.com/jack/status/20`
- **Sample Positive:** `"Love the incredible battery life and crisp display quality on this device!"`
- **Sample Negative:** `"Worst customer support ever, flight delayed by 6 hours without any food or refund."`
- **Sample Neutral:** `"The annual developer conference will take place this Thursday at 10 AM."`
