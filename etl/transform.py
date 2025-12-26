import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sia=SentimentIntensityAnalyzer()

def label_sentiment(score : float) -> str:
    if score >0.05:
        return "positive"
    elif score < -0.05:
        return "negative"
    return "neutral"

def transform_reviews(df : pd.DataFrame) -> pd.DataFrame:

    df.columns=(
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ","_")
    )

    df = df.dropna(subset=["review_text"])

    df["rating"] = df["rating"].fillna(0)


    df["sentiment_score"] = df["review_text"].astype(str).apply(
        lambda x: sia.polarity_scores(x)["compound"])


    df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

    df["demand_score"]=(
        df["rating"]*20
        + df["sentiment_score"]*100
    )

    return df

def transform_inventory(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df = df.dropna(subset=["product_id"])


    df["product_name"] = df["product_name"].fillna("unknown")
    df["category"] = df["category"].fillna("Uncategorized")

    df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)
    df["price"] = df["price"].fillna(0).astype(int)

    return df


def aggregate_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create category-level analytics summary
    """

    summary = (
        df.groupby("category")
        .agg(
            avg_rating=("rating", "mean"),
            avg_demand_score=("demand_score", "mean"),
            total_reviews=("review_text", "count"),
            positive_share=("sentiment_label", lambda x: (x == "positive").mean())
        )
        .reset_index()
    )

    return summary


