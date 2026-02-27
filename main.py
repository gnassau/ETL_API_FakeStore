from src.ingestion.extract_products_V1 import extract_products
from src.transformation_silver.transform_data_V1 import transform_data
from src.loading.postgres_loader import load_products

from pathlib import Path
import argparse

BASE_DIR = Path(__file__).resolve().parents[2]

def run_pipeline(min_id=None, max_id=None):
    df = extract_products(min_id=min_id, max_id=max_id)
    df = transform_data()
    load_products(df)

    print("✅ Pipeline concluído com sucesso!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_id", type=int, default=None)
    parser.add_argument("--max_id", type=int, default=None)

    args = parser.parse_args()

    run_pipeline(min_id=args.min_id, max_id=args.max_id)