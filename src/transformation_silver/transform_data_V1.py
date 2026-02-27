import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

path_name = BASE_DIR / 'data' / 'bronze' /'products' / 'products.json'

def create_dataframe():
    with open(path_name) as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    return df

def capitalize_category(df):
    df['category'] = df['category'].apply(lambda s: ' '.join(w.capitalize() for w in s.split()))
    return df

def remove_duplicates(df):
    df = df.drop_duplicates(subset='id')
    return df

def remove_negative_prices(df):
    df = df[df['price'] >= 0]
    return df

def remove_missing_values(df):
    df = df.dropna()
    return df

def add_price_bucket(df):
    df["price_category"] = df["price"].apply(
        lambda price: "Low" if price < 50
        else "Medium" if price < 150
        else "High"
    )
    return df

def extract_rating_fields(df):
    df["rating_rate"] = df["rating"].apply(lambda x: x["rate"])
    df["rating_count"] = df["rating"].apply(lambda x: x["count"])
    df = df.drop(columns=["rating"])
    return df

def transform_data():
    df = create_dataframe()
    df = capitalize_category(df)
    df = remove_duplicates(df)
    df = remove_negative_prices(df)
    df = remove_missing_values(df)
    df = add_price_bucket(df)
    df = extract_rating_fields(df)
    print("✅ Transformação de dados concluída com sucesso!")

    return df