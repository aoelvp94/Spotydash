import itertools
import logging
import pickle
from datetime import timedelta

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from spotydash.constants import DATA_DIR
from spotydash.dags.common_args import default_args
from spotydash.extract import get_playlist_audio_features
from spotydash.helpers import get_user_playlist
from spotydash.load import load
from spotydash.transform import transform_songs_data


@dag(
    "song_ETL_taskflow",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=["ETL"],
)
def taskflow_api_etl():
    @task
    def extract_task(avoid_api=True):
        if avoid_api:
            logging.info("avoid_api = True, reading data from local storage..")
            with open(DATA_DIR / "audio_features.pickle", "rb") as handle:
                composed_audio_features = pickle.load(handle)
            with open(DATA_DIR / "ids.pickle", "rb") as handle:
                composed_ids = pickle.load(handle)
        else:
            playlists = get_user_playlist()
            list_of_audio = []
            list_of_ids = []
            for p in playlists:
                audio, ids = get_playlist_audio_features(p)
                list_of_audio.append(audio)
                list_of_ids.append(ids)

            composed_audio_features = list(itertools.chain.from_iterable(list_of_audio))
            composed_ids = list(itertools.chain.from_iterable(list_of_ids))

        return composed_audio_features, composed_ids

    @task
    def transform_task(result, avoid_api=True):
        logging.info(result)
        if avoid_api:
            return (
                pd.read_csv(DATA_DIR / "transformed_songs_data.csv")
                .drop_duplicates(subset=["id"])
                .to_json()
            )
        else:
            return (
                transform_songs_data(result[0], result[1])
                .drop_duplicates(subset=["id"])
                .to_json()
            )

    @task
    def load_task(json_df):
        load(pd.read_json(json_df), "Song")

    df = extract_task()
    clean_df = transform_task(df)
    load_task(clean_df)


taskflow_api_etl_dag = taskflow_api_etl()
