from db.db_config import get_connection
import pandas as pd

def load_inventory(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO inventory
        (product_id, product_name, category, stock_quantity, price)
        VALUES (%s, %s, %s, %s, %s)
    """

    data = [
        (
            int(row["product_id"]),
            row["product_name"],
            row["category"],
            int(row["stock_quantity"]),
            float(row["price"])
        )
        for row in df.to_dict("records")
    ]

    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()


def load_reviews(df: pd.DataFrame):
    """
    Load reviews with sentiment into MySQL
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO reviews_sentiment
        (product_id, review_text, rating, sentiment_score, sentiment_label, demand_score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            int(row["product_id"]),
            row["review_text"],
            int(row["rating"]),
            float(row["sentiment_score"]),
            row["sentiment_label"],
            float(row["demand_score"])
        )
        for row in df.to_dict("records")
    ]

    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()


def load_category_summary(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE category_summary")

    query = """
        INSERT INTO category_summary
        (category, avg_rating, avg_demand_score, total_reviews, positive_share)
        VALUES (%s, %s, %s, %s, %s)
    """

    data = [
        (
            row["category"],
            float(row["avg_rating"]),
            float(row["avg_demand_score"]),
            int(row["total_reviews"]),
            float(row["positive_share"])
        )
        for row in df.to_dict("records")
    ]

    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()

