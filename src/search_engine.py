import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class IRSearchEngine:
    """Information Retrieval engine supporting ranked retrieval and sentiment filtering."""

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            sublinear_tf=True,
            norm="l2",
            max_features=12000,
        )
        # Build Document-Term Matrix (Inverted Index representation)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["text"])
        self.feature_names = set(self.vectorizer.get_feature_names_out())

    def search(self, query: str, sentiment_filter: str = "all", top_k: int = 10) -> list:
        """
        Rank documents using Cosine Similarity under the Vector Space Model.
        Optionally filter by sentiment class ('all', 'positive', 'negative', 'neutral').
        """
        query_str = query.strip()
        if not query_str:
            return []

        # Vectorize query
        query_vec = self.vectorizer.transform([query_str])
        if query_vec.nnz == 0:
            return []

        # Compute cosine similarity against all indexed tweets
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Extract non-zero matches
        matching_indices = scores.nonzero()[0]
        if len(matching_indices) == 0:
            return []

        # Query terms for keyword highlighting
        query_terms = set(self.vectorizer.build_analyzer()(query_str))

        results = []
        for idx in matching_indices:
            score = scores[idx]
            tweet_sent = self.df.iloc[idx]["sentiment"]

            # Apply sentiment filter if specified
            if sentiment_filter != "all" and tweet_sent != sentiment_filter:
                continue

            tweet_text = self.df.iloc[idx]["text"]
            tweet_id = int(self.df.iloc[idx]["id"])

            # Find matching terms present in this tweet
            tweet_tokens = set(self.vectorizer.build_analyzer()(tweet_text))
            matched_terms = list(query_terms.intersection(tweet_tokens))

            results.append({
                "id": tweet_id,
                "text": tweet_text,
                "sentiment": tweet_sent,
                "relevance_score": float(score),
                "matched_terms": matched_terms,
            })

        # Rank documents in descending order of relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]

    def get_stats(self) -> dict:
        """Return index statistics."""
        return {
            "total_documents": len(self.df),
            "vocabulary_size": len(self.feature_names),
            "sentiment_counts": self.df["sentiment"].value_counts().to_dict(),
        }


if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tweets.csv")
    engine = IRSearchEngine(data_file)
    print("Search Index Stats:", engine.get_stats())
    sample_results = engine.search("game update delayed", sentiment_filter="negative", top_k=3)
    print("Sample Ranked Results:")
    for r in sample_results:
        print(f"[{r['sentiment'].upper()}] (Score: {r['relevance_score']:.3f}) {r['text'][:90]}...")
