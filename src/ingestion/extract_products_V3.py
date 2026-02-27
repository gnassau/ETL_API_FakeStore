import requests
import pandas as pd
from pathlib import Path
from datetime import datetime



def extract_products(min_id=None, max_id=None):

    BASE_DIR = Path(__file__).resolve().parents[2]
    bronze_base_dir = BASE_DIR / "data" / "bronze" / "products"

    # 📅 Partição por data
    ingestion_date = datetime.now().strftime("%Y-%m-%d")
    partition_dir = bronze_base_dir / f"ingestion_date={ingestion_date}"
    partition_dir.mkdir(parents=True, exist_ok=True)

    # 🕒 Timestamp no nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = partition_dir / f"products_{timestamp}.parquet"

    products = []

    if min_id is not None and max_id is not None:

        for product_id in range(min_id, max_id + 1):
            response = requests.get(
                f"https://fakestoreapi.com/products/{product_id}"
            )

            if response.status_code == 200:
                products.append(response.json())
            else:
                print(f"Erro ao buscar produto {product_id}")

    else:
        response = requests.get("https://fakestoreapi.com/products")

        if response.status_code == 200:
            products = response.json()
        else:
            print("Erro ao buscar produtos")
            return None

    df = pd.DataFrame(products)

    # 🔥 Salva como Parquet
    df.to_parquet(output_file, index=False)

    print(f"✅ Arquivo salvo em: {output_file}")
    print(f"📦 {len(df)} registros extraídos")

    return df