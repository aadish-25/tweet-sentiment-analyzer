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
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
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
    "Information Retrieval Project: Dual-Model Sentiment Classification using Logistic Regression and Multinomial Naive Bayes."
)

tab1, tab2 = st.tabs(["Sentiment Analysis", "Evaluation Metrics"])

# -------------------------------------------------------------------------------------------------
# TAB 1: Sentiment Analysis (Dual Model Comparison with Visual Probability Bars)
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

                def create_probability_chart(prob_dict):
                    df_prob = pd.DataFrame({
                        "Sentiment": [k.capitalize() for k in prob_dict.keys()],
                        "Probability": [v * 100 for v in prob_dict.values()],
                    })
                    return (
                        alt.Chart(df_prob)
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

                # Column 1: Logistic Regression
                with col_lr:
                    st.markdown("#### Logistic Regression")
                    st.markdown(
                        f"**Prediction:** `{lr_res['prediction'].upper()}` | **Confidence:** `{lr_res['confidence'] * 100:.2f}%`"
                    )
                    st.altair_chart(create_probability_chart(lr_res["probabilities"]), width="stretch")
                    st.caption(
                        f"Negative: {lr_res['probabilities']['negative']*100:.1f}% | "
                        f"Neutral: {lr_res['probabilities']['neutral']*100:.1f}% | "
                        f"Positive: {lr_res['probabilities']['positive']*100:.1f}%"
                    )

                # Column 2: Multinomial Naive Bayes
                with col_nb:
                    st.markdown("#### Multinomial Naive Bayes")
                    st.markdown(
                        f"**Prediction:** `{nb_res['prediction'].upper()}` | **Confidence:** `{nb_res['confidence'] * 100:.2f}%`"
                    )
                    st.altair_chart(create_probability_chart(nb_res["probabilities"]), width="stretch")
                    st.caption(
                        f"Negative: {nb_res['probabilities']['negative']*100:.1f}% | "
                        f"Neutral: {nb_res['probabilities']['neutral']*100:.1f}% | "
                        f"Positive: {nb_res['probabilities']['positive']*100:.1f}%"
                    )

# -------------------------------------------------------------------------------------------------
# TAB 2: Evaluation Metrics (Grand Comparative Dashboard)
# -------------------------------------------------------------------------------------------------
with tab2:
    st.subheader("Model Evaluation and Comparative Metrics")

    if metrics is not None:
        d_info = metrics.get("dataset_info", {})
        lr_m = metrics.get("logistic_regression", {})
        nb_m = metrics.get("naive_bayes", {})

        # Top summary cards row
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Total Dataset Corpus", f"{d_info.get('total_samples', 0):,} tweets")
        with col_s2:
            st.metric("Training Split (80%)", f"{d_info.get('train_samples', 0):,} tweets")
        with col_s3:
            st.metric("Test Split (20%)", f"{d_info.get('test_samples', 0):,} tweets")
        with col_s4:
            st.metric("Vocabulary Features", f"{d_info.get('vocabulary_size', 0):,} terms")

        st.markdown("---")

        # Grand Visual Comparison Bar Chart
        st.markdown("#### Comparative Benchmark: Logistic Regression vs Naive Bayes")
        st.caption("Visual comparison of classification performance evaluated on the exact same 20% test split.")

        chart_data = pd.DataFrame([
            {"Metric": "Accuracy", "Model": "Logistic Regression", "Score": lr_m.get("accuracy", 0) * 100},
            {"Metric": "Accuracy", "Model": "Naive Bayes", "Score": nb_m.get("accuracy", 0) * 100},
            {"Metric": "Precision", "Model": "Logistic Regression", "Score": lr_m.get("precision", 0) * 100},
            {"Metric": "Precision", "Model": "Naive Bayes", "Score": nb_m.get("precision", 0) * 100},
            {"Metric": "Recall", "Model": "Logistic Regression", "Score": lr_m.get("recall", 0) * 100},
            {"Metric": "Recall", "Model": "Naive Bayes", "Score": nb_m.get("recall", 0) * 100},
            {"Metric": "F1-Score", "Model": "Logistic Regression", "Score": lr_m.get("f1_score", 0) * 100},
            {"Metric": "F1-Score", "Model": "Naive Bayes", "Score": nb_m.get("f1_score", 0) * 100},
        ])

        comparison_chart = (
            alt.Chart(chart_data)
            .mark_bar(cornerRadius=4)
            .encode(
                x=alt.X("Model:N", title=None, axis=alt.Axis(labels=True)),
                y=alt.Y("Score:Q", title="Percentage (%)", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color(
                    "Model:N",
                    scale=alt.Scale(
                        domain=["Logistic Regression", "Naive Bayes"],
                        range=["#1d3557", "#457b9d"],
                    ),
                    legend=alt.Legend(title="Algorithm", orient="top"),
                ),
                column=alt.Column("Metric:N", title=None, header=alt.Header(labelFontSize=13, labelFontWeight="bold")),
                tooltip=["Metric", "Model", alt.Tooltip("Score:Q", format=".2f")],
            )
            .properties(width=160, height=280)
        )
        st.altair_chart(comparison_chart)

        st.markdown("---")

        # Metric Details Table
        st.markdown("#### Performance Metrics Summary Table")
        comparison_table = [
            {
                "Evaluation Metric": "Accuracy",
                "Logistic Regression": f"{lr_m.get('accuracy', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('accuracy', 0) * 100:.2f}%",
                "Leading Model": "Logistic Regression" if lr_m.get("accuracy", 0) >= nb_m.get("accuracy", 0) else "Naive Bayes",
            },
            {
                "Evaluation Metric": "Precision (Macro)",
                "Logistic Regression": f"{lr_m.get('precision', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('precision', 0) * 100:.2f}%",
                "Leading Model": "Logistic Regression" if lr_m.get("precision", 0) >= nb_m.get("precision", 0) else "Naive Bayes",
            },
            {
                "Evaluation Metric": "Recall (Macro)",
                "Logistic Regression": f"{lr_m.get('recall', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('recall', 0) * 100:.2f}%",
                "Leading Model": "Logistic Regression" if lr_m.get("recall", 0) >= nb_m.get("recall", 0) else "Naive Bayes",
            },
            {
                "Evaluation Metric": "F1-Score (Macro)",
                "Logistic Regression": f"{lr_m.get('f1_score', 0) * 100:.2f}%",
                "Multinomial Naive Bayes": f"{nb_m.get('f1_score', 0) * 100:.2f}%",
                "Leading Model": "Logistic Regression" if lr_m.get("f1_score", 0) >= nb_m.get("f1_score", 0) else "Naive Bayes",
            },
            {
                "Evaluation Metric": "Log Loss (Cross-Entropy)",
                "Logistic Regression": f"{lr_m.get('log_loss', 0):.4f}",
                "Multinomial Naive Bayes": f"{nb_m.get('log_loss', 0):.4f}",
                "Leading Model": "Logistic Regression (Lower is better)",
            },
        ]
        st.dataframe(pd.DataFrame(comparison_table), hide_index=True, width="stretch")

    else:
        st.info("No trained models found. Train models below or run python train.py.")

    st.markdown("---")
    st.markdown("#### Retrain with Custom Dataset")
    st.caption("Upload any custom CSV dataset to retrain and benchmark both models on your data.")

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
