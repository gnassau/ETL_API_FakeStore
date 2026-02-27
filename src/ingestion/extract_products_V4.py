import json
from pathlib import Path
import requests

# Todos os modos de extração em uma função só


def extract_products(mode="incremental", min_id=None, max_id=None):
    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "data" / "bronze" / "products"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "products.json"

    if output_file.exists():
        with open(output_file, "r") as f:
            products = json.load(f)
    else:
        products = []

    existing_ids = {p["id"] for p in products}

    # 🎯 MODO FULL
    if mode == "full":
        print("🔄 FULL REFRESH")
        products = []
        id_range = range(1, 21)  # limite da FakeStore

    # 🎯 MODO RANGE
    elif mode == "range" and min_id and max_id:
        print(f"🔄 RANGE {min_id} - {max_id}")
        id_range = range(min_id, max_id + 1)

    # 🎯 MODO INCREMENTAL
    else:
        print("📈 INCREMENTAL")
        next_id = max(existing_ids) + 1 if existing_ids else 1
        id_range = [next_id]

    # 🔄 Buscar dados
    for product_id in id_range:
        response = requests.get(f"https://fakestoreapi.com/products/{product_id}")

        if response.status_code == 200:
            new_product = response.json()

            # remove se já existir
            products = [p for p in products if p["id"] != product_id]
            products.append(new_product)

            print(f"✅ Produto {product_id} processado")

    with open(output_file, "w") as f:
        json.dump(products, f, indent=4)

    print("SALVANDO EM:", output_file.resolve())