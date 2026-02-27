import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Diretório bronze base (agora particionado)
BRONZE_PATH = BASE_DIR / "data" / "bronze" / "products"

# ==========================================
# Lê TODOS os arquivos parquet do bronze
# ==========================================
def create_dataframe():

    parquet_files = list(BRONZE_PATH.glob("**/*.parquet"))

    if not parquet_files:
        raise FileNotFoundError("❌ Nenhum arquivo Parquet encontrado no bronze.")

    df_list = [pd.read_parquet(file) for file in parquet_files]

    df = pd.concat(df_list, ignore_index=True)

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