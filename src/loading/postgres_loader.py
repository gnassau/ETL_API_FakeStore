from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv('/home/gustavo/data-engineering-fakestore/.env')

# LOCAL
# def get_engine():
#     return create_engine(
#         f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
#         f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
#     )

# docker
def get_engine():
    return create_engine(
        f"postgresql://{os.getenv('POSTGRES_DB_USER')}:{os.getenv('POSTGRES_DB_PASSWORD')}"
        f"@{os.getenv('POSTGRES_DB_HOST')}:{os.getenv('POSTGRES_DB_PORT')}/"
        f"{os.getenv('POSTGRES_DB_NAME')}"
    )


def create_table_if_not_exists():
    engine = get_engine()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS public.products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price NUMERIC NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        image TEXT NOT NULL,
        rating_rate FLOAT NOT NULL,
        rating_count INTEGER NOT NULL,
        price_category VARCHAR NOT NULL
    );
    """

    with engine.begin() as connection:
        connection.execute(text(create_table_query))

def load_products(df):
    engine = get_engine()

    # garante que tabela existe
    create_table_if_not_exists()

    insert_query = text("""
        INSERT INTO public.products (
            id,
            title,
            price,
            description,
            category,
            image,
            rating_rate,
            rating_count,
            price_category
        )
        VALUES (
            :id,
            :title,
            :price,
            :description,
            :category,
            :image,
            :rating_rate,
            :rating_count,
            :price_category
        )
        ON CONFLICT (id)
        DO UPDATE SET
            title = EXCLUDED.title,
            price = EXCLUDED.price,
            description = EXCLUDED.description,
            category = EXCLUDED.category,
            image = EXCLUDED.image,
            rating_rate = EXCLUDED.rating_rate,
            rating_count = EXCLUDED.rating_count,
            price_category = EXCLUDED.price_category;
    """)

    # transforma dataframe em lista de dicionários
    records = df.to_dict(orient="records")

    # executa em batch (mais performático)
    with engine.begin() as connection:
        connection.execute(insert_query, records)
