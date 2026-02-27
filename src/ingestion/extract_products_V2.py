import json
from pathlib import Path
import requests
import pandas as pd


def extract_products(min_id=None, max_id=None):
    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "data" / "bronze" / "products"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "products.json"

    # ==============================
    # Carrega bronze existente
    # ==============================
    if output_file.exists():
        with open(output_file, "r") as f:
            products_list = json.load(f)
    else:
        products_list = []

    # 🔥 Converte para dict indexado por ID (evita duplicação)
    products = {product["id"]: product for product in products_list}

    # ==============================
    # MODO RANGE (manual)
    # ==============================
    if min_id is not None and max_id is not None:

        for product_id in range(min_id, max_id + 1):

            response = requests.get(
                f"https://fakestoreapi.com/products/{product_id}"
            )

            if response.status_code == 200:
                product = response.json()

                # 🔥 Sobrescreve se já existir (deduplicado)
                products[product["id"]] = product

            else:
                print(f"❌ Erro ao buscar produto {product_id}")

        print(f"✅ Bronze atualizado. Total único: {len(products)} produtos")

    # ==============================
    # MODO INCREMENTAL AUTOMÁTICO
    # ==============================
    else:

        if products:
            current_max_id = max(products.keys())
        else:
            current_max_id = 0

        next_id = current_max_id + 1

        response = requests.get(
            f"https://fakestoreapi.com/products/{next_id}"
        )

        if response.status_code == 200:
            product = response.json()

            products[product["id"]] = product

            print(f"✅ Produto {next_id} adicionado com sucesso!")

        else:
            print(f"❌ Nenhum novo produto encontrado.")
            return pd.DataFrame(list(products.values()))

    # ==============================
    # Salva bronze deduplicado
    # ==============================
    with open(output_file, "w") as f:
        json.dump(list(products.values()), f, indent=4)

    # Retorna DataFrame
    return pd.DataFrame(list(products.values()))


if __name__ == "__main__":
    extract_products()