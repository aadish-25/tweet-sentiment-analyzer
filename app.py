import os
import pandas as pd
import streamlit as st
import altair as alt

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


@st.cache_resource(show_spinner="Loading model...")
def get_engine():
    return SentimentEngine()


engine = get_engine()
metrics = engine.metrics

# Header
st.title("Tweet Sentiment Analysis System")
st.caption(
    "Information Retrieval Project: Sentiment Classification using Logistic Regression."
)

tab1, tab2 = st.tabs(["Sentiment Analysis", "Evaluation Metrics"])

# -------------------------------------------------------------------------------------------------
# TAB 1: Sentiment Analysis
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
        analyze_clicked = st.button("Analyze Sentiment", key="btn_text", type="primary", width="stretch")
    else:
        col_input, col_samples = st.columns([1, 1], gap="large")

        with col_input:
            user_input = st.text_input(
                "Paste Twitter / X URL:",
                value="https://x.com/realDonaldTrump/status/794155725152980992",
                placeholder="https://x.com/username/status/123456789",
            )
            analyze_clicked = st.button("Analyze Sentiment", key="btn_url", type="primary", width="stretch")

        with col_samples:
            st.markdown("**Sample URLs for Testing:**")
            st.caption("Click the copy icon on any URL to copy and paste it into the analyzer.")

            st.markdown("- **Negative Sentiment:**")
            st.code("https://x.com/realDonaldTrump/status/794155725152980992", language="text")
            st.code("https://x.com/realDonaldTrump/status/802671162383802368", language="text")

            st.markdown("- **Positive Sentiment:**")
            st.code("https://x.com/TheEllenShow/status/440322224407314432", language="text")
            st.code("https://x.com/realDonaldTrump/status/814919370711461890", language="text")

            st.markdown("- **Neutral Sentiment:**")
            st.code("https://x.com/realDonaldTrump/status/815270850916208644", language="text")
            st.code("https://x.com/realDonaldTrump/status/814958820980039681", language="text")

    if analyze_clicked:
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

                result = engine.predict(tweet_text)
                pred_label = result["prediction"]
                confidence = result["confidence"]
                probabilities = result["probabilities"]
                top_terms = result["top_terms"]

                st.divider()

                # Big Colored Sentiment Box + Horizontal Probability Bar Chart
                col_box, col_chart = st.columns([1, 2])

                with col_box:
                    if pred_label == "positive":
                        st.success(
                            f"### POSITIVE\n**Confidence:** {confidence * 100:.1f}%"
                        )
                    elif pred_label == "negative":
                        st.error(
                            f"### NEGATIVE\n**Confidence:** {confidence * 100:.1f}%"
                        )
                    else:
                        st.info(
                            f"### NEUTRAL\n**Confidence:** {confidence * 100:.1f}%"
                        )

                with col_chart:
                    st.markdown("**Class Probabilities Breakdown:**")
                    prob_df = pd.DataFrame({
                        "Sentiment": [k.capitalize() for k in probabilities.keys()],
                        "Probability": [v * 100 for v in probabilities.values()],
                    })

                    chart = (
                        alt.Chart(prob_df)
                        .mark_bar(cornerRadius=4)
                        .encode(
                            x=alt.X("Probability:Q", scale=alt.Scale(domain=[0, 100]), title="Probability (%)"),
                            y=alt.Y("Sentiment:N", sort=["Negative", "Neutral", "Positive"], title=None),
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

                # Influential Vocabulary Terms
                st.markdown("#### Influential Terms")
                st.caption("Vocabulary terms in the tweet driving the classification:")
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
                    st.write("No distinct vocabulary weights detected.")

# -------------------------------------------------------------------------------------------------
# TAB 2: Evaluation Metrics (Single Line Metrics Row)
# -------------------------------------------------------------------------------------------------
with tab2:
    st.subheader("Model Evaluation and Metrics")

    if metrics is not None:
        # Single-line metrics row
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1:
            st.metric("Total Dataset", f"{metrics.get('total_samples', 0):,}")
        with m2:
            st.metric("Accuracy", f"{metrics.get('accuracy', 0) * 100:.2f}%")
        with m3:
            st.metric("F1-Score", f"{metrics.get('f1_score', 0) * 100:.2f}%")
        with m4:
            st.metric("Precision", f"{metrics.get('precision', 0) * 100:.2f}%")
        with m5:
            st.metric("Recall", f"{metrics.get('recall', 0) * 100:.2f}%")
        with m6:
            st.metric("Log Loss", f"{metrics.get('log_loss', 0):.4f}")

    else:
        st.info("No trained model found. Train model below or run python train.py.")

    st.markdown("---")
    st.markdown("#### Retrain with Custom Dataset")
    st.caption("Upload a custom CSV file to retrain and re-evaluate the model.")

    uploaded_file = st.file_uploader("Upload CSV File:", type=["csv"])
    if uploaded_file is not None:
        if st.button("Train Model on Uploaded CSV", type="primary", width="stretch"):
            with st.spinner("Training Logistic Regression on uploaded CSV..."):
                try:
                    updated_metrics = train_models(data_source=uploaded_file)
                    st.success("Training complete! Model artifacts and metrics updated.")
                    st.cache_resource.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Training failed: {e}")
