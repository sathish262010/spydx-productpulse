from etl.extract import extract_reviews
from etl.transform import transform_reviews
from etl.load_mysql import load_reviews

def run_reviews_etl():
    print("Starting Reviews ETL...")

    df = extract_reviews()
    df = transform_reviews(df)
    load_reviews(df)

    print("Reviews ETL completed successfully")

if __name__ == "__main__":
    run_reviews_etl()
