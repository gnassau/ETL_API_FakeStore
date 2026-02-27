
import json
from pathlib import Path
import requests


def extract_products(min_id=None, max_id=None):
    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "data" / "bronze" / "products"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "products.json"

    # Se arquivo existir, carregar dados
    if output_file.exists():
        with open(output_file, "r") as f:
            products = json.load(f)
    else:
        products = []

    # Descobrir maior ID já salvo
    if products:
        max_id = max(product["id"] for product in products)
    else:
        max_id = 0

    next_id = max_id + 1

    # Buscar próximo produto
    response = requests.get(f"https://fakestoreapi.com/products/{next_id}")

    if response.status_code == 200:
        new_product = response.json()
        products.append(new_product)

        with open(output_file, "w") as f:
            json.dump(products, f, indent=4)

        print(f"✅ Produto {next_id} adicionado com sucesso!")
        print("SALVANDO EM:", output_file.resolve())
    else:
        print(f"❌ Erro ao buscar produto {next_id}: Status {response.status_code}")
        return


if __name__ == "__main__":
    extract_products()


