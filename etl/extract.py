import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def extract_inventory():

    path =os.path.join(DATA_DIR,"inventory.csv")
    return pd.read_csv(path)


def extract_reviews():
    path =os.path.join(DATA_DIR,"reviews.csv")
    return  pd.read_csv(path)