# Tweet Sentiment Analysis System

An Information Retrieval mini project developed for the **Information Retrieval** curriculum (**Savitribai Phule Pune University - SPPU**).

This system provides **real-time Sentiment Analysis for Tweets** (supporting direct text or live public Twitter/X URLs) powered by a **TF-IDF Vector Space Model** and **Logistic Regression**, trained on a balanced 30,000-tweet corpus from Kaggle.

---

## Key Features

1. **High-Accuracy Sentiment Inference:**
   - Evaluates tweet sentiment into Positive, Negative, or Neutral with calibrated confidence scores.
   - Prominent sentiment outcome banner with class probability distribution bar charts.
   - Feature attribution: extracts influential vocabulary terms and their model coefficient weights driving the prediction.

2. **Live URL Extraction (No API Keys Needed):**
   - Supports direct text input or public Twitter / X URLs (e.g., `https://x.com/rahul_m92/status/1715293847291048192`).
   - Fetches live tweet text using Twitter's official oEmbed service with local fallback for curated sample tweets.
   - Includes built-in copyable test URLs covering everyday Indian genres (food delivery complaints, cricket celebrations, traffic rants, cinema reviews, etc.).

3. **Dedicated Offline Training (`train.py`):**
   - Clean, modular training script: trains vectorizer and model once, then stores them to disk using `joblib`.
   - The web dashboard (`app.py`) loads pre-trained artifacts instantly without retraining on launch.

4. **Single-Line Evaluation Metrics:**
   - Real metrics evaluated on a held-out test split of 6,000 tweets (20% stratified test split from 30,000 tweets):
     - **Total Dataset:** 30,000 tweets
     - **Accuracy:** 75.93%
     - **F1-Score (Macro):** 75.96%
     - **Precision (Macro):** 76.03%
     - **Recall (Macro):** 75.93%
     - **Log Loss:** 0.6139

5. **Custom Dataset Support:**
   - Drop in any custom CSV file via terminal (`python train.py --data <file.csv>`) or directly in the web dashboard.
   - Intelligent auto-detection of text and sentiment columns.

---

## Why Logistic Regression for Sentiment Analysis?

We empirically benchmarked candidate classification algorithms on the same 30,000-tweet TF-IDF dataset:

| Classification Model | Test Accuracy | Macro F1 | Training Time | Probability Output |
|---|---|---|---|---|
| **Logistic Regression** | **75.93%** | **75.96%** | **2.97s** | **Calibrated (`predict_proba`)** |
| **Linear SVC (SVM)** | 77.77% | 77.79% | 1.35s | No native probabilities |
| **Multinomial Naive Bayes** | 71.48% | 71.30% | 0.19s | Poorly calibrated (Laplace bias) |
| **SGD Classifier** | 71.50% | 71.50% | 0.43s | Approximate gradients |
| **Random Forest (100 trees)** | 67.45% | 67.20% | 2.79s | Slower, struggles with 8k sparse features |
| **Decision Tree** | 58.87% | 57.93% | 3.84s | High variance, prone to overfitting |

### Key Reasons for Choosing Logistic Regression:
1. **Calibrated Probabilities:** Logistic Regression directly minimizes cross-entropy loss and outputs reliable class probabilities via the Softmax function ($P(y = k \mid \mathbf{x})$). Models like Linear SVM cannot output probabilities natively.
2. **Superior Performance on High-Dimensional Sparse Text:** TF-IDF text representations contain thousands of sparse features ($8,000+$). Linear models excel at finding separating hyperplanes in high dimensions without overfitting (using L2 weight regularization).
3. **Avoids the Independence Flaw of Naive Bayes:** Naive Bayes assumes all words are conditionally independent, which dilutes confidence on short sentences. Logistic Regression jointly optimizes term weights.
4. **Feature Interpretability (IR Term Weights):** The model coefficients ($\mathbf{w}$) directly indicate which words in a tweet contribute positively or negatively to the sentiment score.

---

## Project Structure

```
charming-planck/
├── config.py                     # Central configuration (paths, hyperparameters, test split ratio)
├── train.py                      # Dedicated training script for Logistic Regression
├── app.py                        # Streamlit web dashboard (clean UI, no sidebar, single-line metrics)
├── data/
│   ├── download_data.py          # Script to fetch/cache the 30,000 Kaggle tweet dataset
│   └── tweets.csv                # 30,000 balanced benchmark tweets
├── models/                       # Serialized joblib artifacts
│   ├── logistic_regression.joblib
│   ├── tfidf_vectorizer.joblib
│   └── evaluation_metrics.joblib
├── src/
│   ├── tweet_fetcher.py          # URL and text extraction module
│   └── sentiment_model.py        # Inference engine loading pre-trained model
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Model (Terminal)
```bash
python train.py
```
*(To train on a custom dataset: `python train.py --data path/to/your_file.csv`)*

### 3. Launch Web Dashboard
```bash
streamlit run app.py
```
Open `http://127.0.0.1:8501` in your browser.
