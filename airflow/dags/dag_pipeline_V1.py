from airflow.decorators import dag, task
from datetime import datetime
import sys

# Permite importar seu projeto montado no container
sys.path.append("/opt/project")

from src.ingestion.extract_products_V1 import extract_products
from src.transformation_silver.transform_data_V1 import transform_data
from src.loading.postgres_loader import load_products


@dag(
    dag_id="products_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="* * * * *",
    catchup=False,
    tags=["bronze", "silver", "gold"],
)
def products_pipeline():

    @task
    def extract():
        extract_products()
        return "extract_done"


    @task
    def transform(_):
        df = transform_data()

        # TaskFlow já usa XCom automaticamente
        # então podemos retornar objeto simples
        return df.to_json()


    @task
    def load_silver(df_json: str):
        import pandas as pd

        df = pd.read_json(df_json)
        load_products(df)


    # Fluxo
    extract_output = extract()
    transformed = transform(extract_output)
    load_silver(transformed)


# Instancia a DAG
dag = products_pipeline()