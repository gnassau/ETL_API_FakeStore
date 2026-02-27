from airflow.decorators import dag, task
from datetime import datetime
import sys
from airflow.models.param import Param
from airflow.operators.python import get_current_context


# Permite importar seu projeto montado no container
sys.path.append("/opt/project")

from src.ingestion.extract_products_V4 import extract_products
from src.transformation_silver.transform_data_V1 import transform_data
from src.loading.postgres_loader import load_products


@dag(
    dag_id="products_pipeline_v2",
    start_date=datetime(2024, 1, 1),
    schedule="0 * * * *",
    catchup=False,
    tags=["bronze", "silver", "gold"],
    params={
        "extract_mode": Param("incremental", type="string"),
        "extract_mode": Param("full", type="string"),
        "extract_mode": Param("range", type="string"),
        # "transform_mode": Param("incremental", type="string"),
        "min_id": Param(None, type=["null", "integer"]),
        "max_id": Param(None, type=["null", "integer"]),
    }
)
def products_pipeline():

    @task
    def extract():
        context = get_current_context()
        params = context["params"]

        extract_mode = params["extract_mode"]
        min_id = params["min_id"]
        max_id = params["max_id"]

        extract_products(
            mode=extract_mode,
            min_id=min_id,
            max_id=max_id
        )


    @task
    def transform(_):
        df = transform_data()
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