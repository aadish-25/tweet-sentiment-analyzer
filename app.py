import os
import time
import pandas as pd
import streamlit as st
import altair as alt

from src.tweet_fetcher import extract_tweet_input
from src.sentiment_model import SentimentEngine
from src.search_engine import IRSearchEngine

# Page configuration
st.set_page_config(
    page_title="Tweet Sentiment & IR System",
    page_icon="🔎",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tweets.csv")


@st.cache_resource(show_spinner="Loading models and search index...")
def load_resources():
    sentiment_engine = SentimentEngine()
    metrics = sentiment_engine.train(DATA_PATH)
    search_engine = IRSearchEngine(DATA_PATH)
    return sentiment_engine, search_engine, metrics


# Load engines
sentiment_engine, search_engine, metrics = load_resources()

# Sidebar: System Summary and Sample Inputs
with st.sidebar:
    st.title("⚙️ System Overview")
    st.markdown("**Information Retrieval Mini Project**")
    st.markdown(
        """
        - **Model:** TF-IDF Vector Space + Logistic Regression
        - **Vocabulary:** 12,000 features (unigrams + bigrams)
        - **Index Corpus:** 12,000 balanced tweets
        - **Input Modes:** Direct text or live Tweet/X URL
        """
    )
    st.divider()

    st.subheader("💡 Quick Test Presets")
    st.caption("Click any preset to copy into the analyzer:")
    st.code("https://x.com/jack/status/20", language="text")
    st.code("Worst customer service, delayed flight and lost luggage!", language="text")
    st.code("Love this incredible camera quality and battery life!", language="text")

    st.divider()
    stats = search_engine.get_stats()
    st.metric("Indexed Documents", f"{stats['total_documents']:,}")
    st.metric("Test Accuracy", f"{metrics['accuracy'] * 100:.2f}%")

# Main Title
st.title("🔎 Tweet Sentiment Analysis & IR Search Engine")
st.caption(
    "A dual-purpose Information Retrieval system: Fetch & analyze live tweets by URL or text, and perform ranked retrieval with sentiment filtering."
)

tab1, tab2, tab3 = st.tabs([
    "🧪 Tweet Sentiment Analyzer (Text or URL)",
    "🔍 IR Tweet Search & Filter",
    "📊 Model Evaluation & Metrics",
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

    if st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True):
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
                    st.altair_chart(chart, use_container_width=True)

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
# TAB 2: IR Tweet Search & Filtering
# -------------------------------------------------------------------------------------------------
with tab2:
    st.subheader("Ranked Tweet Retrieval with Sentiment Filtering")
    st.write(
        "Search indexed tweets using the **Vector Space Model (Cosine Similarity)** and optionally filter by sentiment class."
    )

    col_q, col_filt, col_top = st.columns([3, 1, 1])
    with col_q:
        search_query = st.text_input(
            "Search Query:",
            value="delayed flight",
            placeholder="e.g. battery drain, excellent movie, flight cancel",
        )
    with col_filt:
        sentiment_choice = st.selectbox(
            "Filter Sentiment:",
            ["all", "positive", "negative", "neutral"],
            format_func=lambda x: x.capitalize(),
        )
    with col_top:
        top_k = st.slider("Results count:", min_value=5, max_value=30, value=10)

    if st.button("🔎 Search Tweets", type="primary"):
        if not search_query.strip():
            st.warning("Please enter a search query.")
        else:
            t_start = time.time()
            results = search_engine.search(
                search_query, sentiment_filter=sentiment_choice, top_k=top_k
            )
            elapsed = (time.time() - t_start) * 1000

            st.write(f"⏱️ Found **{len(results)}** ranked documents in **{elapsed:.2f} ms**")

            if not results:
                st.info("No matching tweets found for the query and filter combination.")
            else:
                for idx, r in enumerate(results, start=1):
                    sent = r["sentiment"]
                    badge_color = (
                        "🟢" if sent == "positive" else ("🔴" if sent == "negative" else "⚪")
                    )

                    with st.container():
                        st.markdown(
                            f"**#{idx}** {badge_color} **{sent.upper()}** "
                            f"| **IR Relevance Score:** `{r['relevance_score']:.4f}` "
                            f"| **Matched Terms:** `{', '.join(r['matched_terms']) if r['matched_terms'] else 'N/A'}`"
                        )
                        st.markdown(f"> *{r['text']}*")
                        st.divider()

# -------------------------------------------------------------------------------------------------
# TAB 3: Model Evaluation & Metrics
# -------------------------------------------------------------------------------------------------
with tab3:
    st.subheader("Model Effectiveness & Performance Metrics")
    st.write(
        "Standard classification and information retrieval evaluation metrics on the held-out test split (2,400 tweets)."
    )

    # Top metrics row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Test Accuracy", f"{metrics['accuracy'] * 100:.2f}%")
    with m_col2:
        macro_f1 = metrics["report"]["macro avg"]["f1-score"] * 100
        st.metric("Macro F1-Score", f"{macro_f1:.2f}%")
    with m_col3:
        st.metric("Vocabulary Size", f"{metrics['vocab_size']:,}")
    with m_col4:
        st.metric("Test Samples", f"{metrics['test_samples']:,}")

    st.divider()

    col_rep, col_cm = st.columns([3, 2])
    with col_rep:
        st.markdown("#### 📋 Detailed Classification Report")
        rep = metrics["report"]
        report_data = []
        for cls_name in ["negative", "neutral", "positive"]:
            row = rep[cls_name]
            report_data.append({
                "Class": cls_name.capitalize(),
                "Precision": f"{row['precision']:.3f}",
                "Recall": f"{row['recall']:.3f}",
                "F1-Score": f"{row['f1-score']:.3f}",
                "Support": int(row["support"]),
            })
        st.dataframe(pd.DataFrame(report_data), hide_index=True, use_container_width=True)

    with col_cm:
        st.markdown("#### 🔲 Confusion Matrix")
        cm = metrics["confusion_matrix"]
        cm_df = pd.DataFrame(
            cm,
            index=["Actual Neg", "Actual Neu", "Actual Pos"],
            columns=["Pred Neg", "Pred Neu", "Pred Pos"],
        )
        st.dataframe(cm_df, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📘 Architecture Summary")
    st.markdown(
        """
        - **Representation:** Scikit-learn `TfidfVectorizer` using sublinear term-frequency scaling and L2 normalization (Unit I: Vector Space Model).
        - **Classification:** Scikit-learn `LogisticRegression` with multi-class cross-entropy and calibrated posterior probabilities (Unit IV: Categorization & Filtering).
        - **Retrieval Engine:** Cosine similarity over the document-term matrix with query term projection and faceted sentiment filtering (Unit II: Ranked Retrieval).
        - **Live Extraction:** Twitter/X oEmbed integration and HTML parsing via `BeautifulSoup` (Unit VI: Data ingestion & web crawling).
        """
    )
