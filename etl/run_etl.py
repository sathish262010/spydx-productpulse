from etl.extract import extract_inventory
from etl.transform import transform_inventory
from etl.load_mysql import load_inventory


def run_inventory_etl():
    print("Starting inventory ETL ...")

    df=extract_inventory()
    df = transform_inventory(df)
    load_inventory(df)

    print("Inventory ETL completed Successfully")


if __name__ == "__main__":
    run_inventory_etl()