from etl.extract import extract_reviews
from etl.transform import transform_reviews, aggregate_category_summary
from etl.load_mysql import load_category_summary

def run_analytics_etl():
    print("Starting Analytics ETL...")

    df = extract_reviews()
    df = transform_reviews(df)

    summary_df = aggregate_category_summary(df)
    load_category_summary(summary_df)

    print("Analytics ETL completed successfully")

if __name__ == "__main__":
    run_analytics_etl()
