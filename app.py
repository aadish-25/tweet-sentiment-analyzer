import os
import pandas as pd
import streamlit as st
import altair as alt

from src.tweet_fetcher import extract_tweet_input
from src.sentiment_model import SentimentEngine

# Page configuration
st.set_page_config(
    page_title="Tweet Sentiment Analysis System",
    page_icon="🐦",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tweets.csv")


@st.cache_resource(show_spinner="Loading sentiment model...")
def load_resources():
    sentiment_engine = SentimentEngine()
    metrics = sentiment_engine.train(DATA_PATH)
    return sentiment_engine, metrics


# Load engine and verified evaluation metrics
sentiment_engine, metrics = load_resources()

# Sidebar: System Overview
with st.sidebar:
    st.title("⚙️ System Overview")
    st.markdown("**Information Retrieval Mini Project**")
    st.markdown(
        """
        - **Topic:** Tweet Sentiment Analysis System
        - **Pipeline:** TF-IDF Representation + Logistic Regression
        - **Dataset:** 12,000 Balanced Benchmark Tweets
        - **Vocabulary:** 8,000 n-gram features
        """
    )
    st.divider()

    st.subheader("💡 Sample Inputs")
    st.caption("Click to copy and test in the analyzer:")
    st.code("https://x.com/jack/status/20", language="text")
    st.code("Worst customer service, delayed flight and lost luggage!", language="text")
    st.code("Love this incredible camera quality and battery life!", language="text")

    st.divider()
    st.metric("Test Accuracy", f"{metrics['accuracy'] * 100:.2f}%")
    st.metric("ROC-AUC Score", f"{metrics['roc_auc']:.4f}")

    st.divider()
    with st.expander("📁 Train with Custom CSV"):
        st.caption("Upload a custom CSV to retrain and re-evaluate the model:")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("⚡ Retrain on Custom CSV", type="primary", width="stretch"):
                with st.spinner("Training on custom dataset..."):
                    custom_df = pd.read_csv(uploaded_file)
                    try:
                        metrics = sentiment_engine.train(custom_df, force_retrain=True)
                        st.success(f"Trained on {metrics['total_samples']:,} samples!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Training failed: {e}")

# Main Header
st.title("🐦 Tweet Sentiment Analysis System")
st.caption(
    "Information Retrieval Project: Analyze sentiment from custom text or public Twitter/X URLs with real model evaluation."
)

tab1, tab2 = st.tabs([
    "🧪 Tweet Sentiment Analyzer (Text or URL)",
    "📊 Real Model Evaluation & Metrics",
])

# -------------------------------------------------------------------------------------------------
# TAB 1: Single Tweet Analyzer (Text or URL)
# -------------------------------------------------------------------------------------------------
with tab1:
    st.subheader("Analyze Sentiment from Text or Tweet URL")
    st.write(
        "Enter raw text or paste any public **Twitter/X status URL** (e.g. `https://x.com/username/status/...`)."
    )

    col_mode, _ = st.columns([2, 1])
    with col_mode:
        input_type = st.radio(
            "Select Input Type:",
            ["Direct Tweet Text", "Tweet URL (twitter.com / x.com)"],
            horizontal=True,
        )

    if input_type == "Direct Tweet Text":
        user_text = st.text_area(
            "Enter Tweet Text:",
            value="Absolutely love the new software update! Battery life is incredible and super responsive.",
            height=110,
        )
        input_value = user_text
    else:
        user_url = st.text_input(
            "Paste Twitter / X URL:",
            value="https://x.com/jack/status/20",
            placeholder="https://x.com/username/status/123456789",
        )
        input_value = user_url

    if st.button("🚀 Analyze Sentiment", type="primary", width="stretch"):
        if not input_value.strip():
            st.warning("Please enter some text or a valid tweet URL.")
        else:
            with st.spinner("Processing input..."):
                resolved = extract_tweet_input(input_value)

            if resolved["status"] == "error":
                st.error(f"⚠️ {resolved['message']}")
            else:
                tweet_text = resolved["text"]
                author = resolved.get("author", "Direct Input")
                tweet_url = resolved.get("url")

                # Show fetched tweet details if fetched via URL
                if resolved.get("source_type") == "url":
                    st.success("✅ Successfully fetched tweet from URL!")
                    with st.expander("📄 Fetched Tweet Metadata", expanded=True):
                        st.markdown(f"**Author:** {author}")
                        if tweet_url:
                            st.markdown(f"**URL:** [{tweet_url}]({tweet_url})")
                        st.markdown(f"**Tweet Content:** *\"{tweet_text}\"*")

                # Run sentiment analysis
                prediction_result = sentiment_engine.predict(tweet_text)
                sentiment = prediction_result["prediction"]
                confidence = prediction_result["confidence"]
                probabilities = prediction_result["probabilities"]
                top_terms = prediction_result["top_terms"]

                st.divider()

                # Sentiment Banner
                col_banner1, col_banner2 = st.columns([1, 2])
                with col_banner1:
                    if sentiment == "positive":
                        st.success(f"### 🟢 POSITIVE\n**Confidence:** {confidence * 100:.1f}%")
                    elif sentiment == "negative":
                        st.error(f"### 🔴 NEGATIVE\n**Confidence:** {confidence * 100:.1f}%")
                    else:
                        st.info(f"### ⚪ NEUTRAL\n**Confidence:** {confidence * 100:.1f}%")

                with col_banner2:
                    st.markdown("**Class Probabilities Breakdown:**")
                    prob_df = pd.DataFrame({
                        "Sentiment": [k.capitalize() for k in probabilities.keys()],
                        "Probability": [v * 100 for v in probabilities.values()],
                    })

                    chart = (
                        alt.Chart(prob_df)
                        .mark_bar()
                        .encode(
                            x=alt.X("Probability:Q", scale=alt.Scale(domain=[0, 100])),
                            y=alt.Y("Sentiment:N", sort=["Negative", "Neutral", "Positive"]),
                            color=alt.Color(
                                "Sentiment:N",
                                scale=alt.Scale(
                                    domain=["Negative", "Neutral", "Positive"],
                                    range=["#e63946", "#8d99ae", "#2a9d8f"],
                                ),
                                legend=None,
                            ),
                            tooltip=["Sentiment", alt.Tooltip("Probability:Q", format=".2f")],
                        )
                        .properties(height=140)
                    )
                    st.altair_chart(chart, width="stretch")

                # Feature attribution (IR Term Weights)
                st.markdown("#### 🔍 Influential Terms")
                st.caption("Key words in the tweet contributing toward the sentiment classification:")
                if top_terms:
                    term_cols = st.columns(min(len(top_terms), 5))
                    for i, (term, weight) in enumerate(top_terms[:5]):
                        with term_cols[i]:
                            st.metric(
                                label=f"Term {i+1}",
                                value=term,
                                delta=f"{weight:+.2f}",
                            )
                else:
                    st.write("No distinct vocabulary weights detected (common or neutral terms).")

# -------------------------------------------------------------------------------------------------
# TAB 2: Real Model Evaluation & Performance Metrics
# -------------------------------------------------------------------------------------------------
with tab2:
    st.subheader("Model Effectiveness & Performance Metrics")
    st.write(
        "All values below are **real calculations** computed by scikit-learn on the stratified test split (**2,400 tweets**, 20% of 12,000 benchmark dataset)."
    )

    # Top metrics row (100% computed from test set)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Test Accuracy", f"{metrics['accuracy'] * 100:.2f}%", help="Exact: 1,464 / 2,400 correct")
    with m2:
        macro_f1 = metrics["report"]["macro avg"]["f1-score"] * 100
        st.metric("Macro F1-Score", f"{macro_f1:.2f}%")
    with m3:
        st.metric("ROC-AUC (OVR)", f"{metrics['roc_auc']:.4f}")
    with m4:
        st.metric("Log Loss", f"{metrics['log_loss']:.4f}")

    st.divider()

    col_rep, col_cm = st.columns([3, 2])
    with col_rep:
        st.markdown("#### 📋 Classification Report (Test Set)")
        rep = metrics["report"]
        report_data = []
        for cls_name in ["negative", "neutral", "positive"]:
            row = rep[cls_name]
            report_data.append({
                "Class": cls_name.capitalize(),
                "Precision": f"{row['precision']:.3f}",
                "Recall": f"{row['recall']:.3f}",
                "F1-Score": f"{row['f1-score']:.3f}",
                "Support (Samples)": int(row["support"]),
            })
        st.dataframe(pd.DataFrame(report_data), hide_index=True, width="stretch")

    with col_cm:
        st.markdown("#### 🔲 Confusion Matrix (Counts)")
        cm = metrics["confusion_matrix"]
        cm_df = pd.DataFrame(
            cm,
            index=["Actual Negative", "Actual Neutral", "Actual Positive"],
            columns=["Predicted Negative", "Predicted Neutral", "Predicted Positive"],
        )
        st.dataframe(cm_df, width="stretch")

    st.markdown("---")
    st.markdown("#### 🔬 Real Test Sample Predictions Inspector")
    st.caption("Inspect actual test tweets from the held-out split to verify real predictions vs ground truth labels:")

    filter_choice = st.radio(
        "Filter Test Samples:",
        ["All (100 samples)", "Only Correctly Classified", "Only Misclassified"],
        horizontal=True,
    )

    samples = metrics.get("sample_test_predictions", [])
    if samples:
        sample_df = pd.DataFrame(samples)
        if filter_choice == "Only Correctly Classified":
            sample_df = sample_df[sample_df["is_correct"] == True]
        elif filter_choice == "Only Misclassified":
            sample_df = sample_df[sample_df["is_correct"] == False]

        display_df = sample_df.rename(columns={
            "text": "Tweet Text",
            "actual": "Actual Label",
            "predicted": "Predicted Label",
            "confidence": "Confidence",
            "is_correct": "Correct?",
        })
        st.dataframe(display_df, hide_index=True, width="stretch")

    st.markdown("---")
    st.markdown("#### 📘 Architecture & Syllabus Mapping")
    st.markdown(
        """
        - **Unit I (Basic IR Models):** Scikit-learn `TfidfVectorizer` applying sublinear TF scaling (1 + log(tf)) and L2 document length normalization.
        - **Unit IV (Categorization & Filtering):** `LogisticRegression` multi-class probabilistic model with cross-entropy loss minimization.
        - **Unit V (Measuring Effectiveness):** True test evaluation via Accuracy, Precision, Recall, F1, ROC-AUC, Log Loss, and Confusion Matrix.
        - **Unit VI (Web Data Ingestion):** Twitter/X oEmbed integration and `BeautifulSoup` parsing to fetch live public tweets from URLs.
        """
    )
