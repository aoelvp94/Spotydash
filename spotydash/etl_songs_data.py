""" ETL for songs data.
"""
import itertools
import logging
import pickle
from datetime import datetime, timedelta

import pandas as pd

from spotydash.constants import DATA_DIR
from spotydash.extract import get_playlist_audio_features
from spotydash.helpers import get_user_playlist
from spotydash.load import load
from spotydash.transform import transform_songs_data


def run_etl_songs_data(execution_date: datetime, avoid_api=True):
    """Run Extract-Load-Transform process.

    Parameters
    ----------
    execution_date : Datetime Object
        Execution date / Date to query.
    avoid_api : bool
        Flag to avoid call to Spotify API.

    """
    # Extract
    playlists = get_user_playlist()
    list_of_dfs = []
    for p in playlists:
        logging.info(f"Getting info about {p}")
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

        logging.info(f"Extracted {len(composed_audio_features)} registers")
        if avoid_api:
            clean_df = pd.read_csv(DATA_DIR / "transformed_songs_data.csv")
        else:
            clean_df = transform_songs_data(composed_audio_features, composed_ids)
        logging.info(f"{clean_df.shape[0]} registers after transform")
        list_of_dfs.append(clean_df)

    results = pd.concat(list_of_dfs)
    results = results.drop_duplicates(subset=["id"])
    # results = fit_clustering(compose_df)

    # Load
    load(results, "Song")
    logging.info("Done")


if __name__ == "__main__":
    date = datetime.today() - timedelta(days=1)
    run_etl_songs_data(date)
