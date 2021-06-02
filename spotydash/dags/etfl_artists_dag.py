"""ETFL for artists data"""

import logging
from datetime import timedelta

import mlflow
import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.utils.dates import days_ago

from spotydash.cfg import MLFLOW_TRACKING_URI
from spotydash.clustering import fit_clustering
from spotydash.dags.common_args import default_args
from spotydash.extract import extract_current_songs
from spotydash.load import load
from spotydash.transform import transform_artist_data


@dag(
    "artists_ETFL",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=["ETFL"],
)
def taskflow_api_etl():
    @task
    def extract_task():
        context = get_current_context()
        return extract_current_songs(context["execution_date"])

    @task
    def transform_task(json_df):
        logging.info(json_df)
        return transform_artist_data(json_df).to_json()

    @task
    def fit_task(json_df):
        context = get_current_context()
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment("kmeans_clustering")
        with mlflow.start_run(run_name=f"kmeans_{context['execution_date']}"):
            return fit_clustering(pd.read_json(json_df)).to_json()

    @task
    def load_task(json_df):
        logging.info(json_df)
        load(pd.read_json(json_df), "Artist")

    result = extract_task()
    clean_df = transform_task(result)
    results = fit_task(clean_df)
    load_task(results)


taskflow_api_etl_dag = taskflow_api_etl()
