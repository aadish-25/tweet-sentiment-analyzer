import os
import pandas as pd
import streamlit as st

import config
from src.tweet_fetcher import extract_tweet_input
from src.sentiment_model import SentimentEngine
from train import train_models

# Page configuration
st.set_page_config(
    page_title="Tweet Sentiment Analysis System",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS to hide sidebar toggle and keep interface clean
st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading models...")
def get_engine():
    return SentimentEngine()


engine = get_engine()
metrics = engine.metrics

# Header
st.title("Tweet Sentiment Analysis System")
st.caption(
    "Information Retrieval Project: Sentiment Classification using Logistic Regression and Multinomial Naive Bayes."
)

tab1, tab2 = st.tabs(["Sentiment Analysis", "Evaluation Metrics"])

# -------------------------------------------------------------------------------------------------
# TAB 1: Sentiment Analysis (Dual Model Comparison)
# -------------------------------------------------------------------------------------------------
with tab1:
    st.subheader("Analyze Tweet Sentiment")
    st.write("Input tweet text directly or paste a public Twitter / X status URL.")

    input_mode = st.radio(
        "Select Input Mode:",
        ["Direct Tweet Text", "Tweet URL (twitter.com / x.com)"],
        horizontal=True,
    )

    if input_mode == "Direct Tweet Text":
        user_input = st.text_area(
            "Enter Tweet Text:",
            value="Loving the incredible camera quality and smooth software update!",
            height=110,
        )
    else:
        user_input = st.text_input(
            "Paste Twitter / X URL:",
            value="https://x.com/jack/status/20",
            placeholder="https://x.com/username/status/123456789",
        )

    if st.button("Analyze Sentiment", type="primary", width="stretch"):
        clean_input = user_input.strip()
        if not clean_input:
            st.warning("Please provide input text or a valid URL.")
        else:
            with st.spinner("Processing input..."):
                resolved = extract_tweet_input(clean_input)

            if resolved["status"] == "error":
                st.error(resolved["message"])
            else:
                tweet_text = resolved["text"]

                # If URL, display fetched tweet content
                if resolved.get("source_type") == "url":
                    st.info(
                        f"Fetched Tweet from {resolved.get('author', 'User')}: \"{tweet_text}\""
                    )

                results = engine.predict(tweet_text)
                lr_res = results["logistic_regression"]
                nb_res = results["naive_bayes"]

                st.markdown("### Model Predictions Comparison")
                col_lr, col_nb = st.columns(2)

                # Column 1: Logistic Regression
                with col_lr:
                    st.markdown("#### Logistic Regression")
                    st.markdown(
                        f"**Prediction:** `{lr_res['prediction'].upper()}` | **Confidence:** `{lr_res['confidence'] * 100:.2f}%`"
                    )
                    lr_prob_df = pd.DataFrame({
                        "Sentiment": [k.capitalize() for k in lr_res["probabilities"].keys()],
                        "Probability (%)": [round(v * 100, 2) for v in lr_res["probabilities"].values()],
                    })
                    st.dataframe(lr_prob_df, hide_index=True, width="stretch")

                # Column 2: Multinomial Naive Bayes
                with col_nb:
                    st.markdown("#### Multinomial Naive Bayes")
                    st.markdown(
                        f"**Prediction:** `{nb_res['prediction'].upper()}` | **Confidence:** `{nb_res['confidence'] * 100:.2f}%`"
                    )
                    nb_prob_df = pd.DataFrame({
                        "Sentiment": [k.capitalize() for k in nb_res["probabilities"].keys()],
                        "Probability (%)": [round(v * 100, 2) for v in nb_res["probabilities"].values()],
                    })
                    st.dataframe(nb_prob_df, hide_index=True, width="stretch")

# -------------------------------------------------------------------------------------------------
# TAB 2: Evaluation Metrics
# -------------------------------------------------------------------------------------------------
with tab2:
    st.subheader("Model Evaluation and Metrics")

    if metrics is not None:
        d_info = metrics.get("dataset_info", {})
        lr_m = metrics.get("logistic_regression", {})
        nb_m = metrics.get("naive_bayes", {})

        # Dataset split summary
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Total Dataset Samples", f"{d_info.get('total_samples', 0):,}")
        with col_s2:
            st.metric("Training Samples (80%)", f"{d_info.get('train_samples', 0):,}")
        with col_s3:
            st.metric("Test Samples (20%)", f"{d_info.get('test_samples', 0):,}")
        with col_s4:
            st.metric("Vocabulary Features", f"{d_info.get('vocabulary_size', 0):,}")

        st.markdown("---")
        st.markdown("#### Performance Comparison on Held-Out Test Data")
        st.caption(
            "Both models were trained and tested on the exact same 80/20 stratified split using Scikit-learn."
        )

        comparison_data = [
            {
                "Metric": "Accuracy",
                "Logistic Regression": f"{lr_m.get('accuracy', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('accuracy', 0) * 100:.2f}%",
            },
            {
                "Metric": "Precision (Macro)",
                "Logistic Regression": f"{lr_m.get('precision', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('precision', 0) * 100:.2f}%",
            },
            {
                "Metric": "Recall (Macro)",
                "Logistic Regression": f"{lr_m.get('recall', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('recall', 0) * 100:.2f}%",
            },
            {
                "Metric": "F1-Score (Macro)",
                "Logistic Regression": f"{lr_m.get('f1_score', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('f1_score', 0) * 100:.2f}%",
            },
            {
                "Metric": "Log Loss (Cross-Entropy)",
                "Logistic Regression": f"{lr_m.get('log_loss', 0):.4f}",
                "Multinomial Naive Bayes": f"{nb_m.get('log_loss', 0):.4f}",
            },
        ]
        st.dataframe(pd.DataFrame(comparison_data), hide_index=True, width="stretch")

    else:
        st.info("No trained models found. Train models below or run python train.py.")

    st.markdown("---")
    st.markdown("#### Retrain with Custom Dataset")
    st.caption("Upload a custom CSV file to retrain and re-evaluate both models.")

    uploaded_file = st.file_uploader("Upload CSV File:", type=["csv"])
    if uploaded_file is not None:
        if st.button("Train Models on Uploaded CSV", type="primary", width="stretch"):
            with st.spinner("Training Logistic Regression and Naive Bayes on uploaded CSV..."):
                try:
                    updated_metrics = train_models(data_source=uploaded_file)
                    st.success("Training complete! Model artifacts and metrics updated.")
                    st.cache_resource.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Training failed: {e}")
