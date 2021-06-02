""" Transform module.

It contains transform functions by getting raw data from Spotify API.
"""
import logging
from typing import Dict, List

import pandas as pd
from pandera import check_output

from spotydash.cfg import sp
from spotydash.constants import DATA_DIR
from spotydash.schemas import SONG_COLUMNS
from spotydash.validate_schemas import null_schema_artists_data

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)


def clean_songs_without_genre(_df):
    """Clean songs data without genre

    Parameters
    ----------
    _df : pd.DataFrame
        Dataframe to be cleaned.

    Returns
    -------
    df_without_genre : pd.DataFrame
        Dataframe that contains not empty genre data.

    """
    df_with_genre = _df[_df.astype(str)["genre"] != "[]"]
    logging.info(f"We had {len(_df)} rows, now we have {len(df_with_genre)} rows")
    return df_with_genre


def transform_songs_data(audio_features: List, ids: List, avoid_api=True):
    """Transform songs data.

    Parameters
    ----------
    audio_features : list(JSON)
        List that contains info about songs.
    ids : list(str)
        List that containts songs ids.

    Returns
    -------
    df : pd.DataFrame
        Transformed DF.

    """

    features_list = []
    counter = 0
    for features in [x for x in audio_features if x is not None]:
        song_data = sp.track(ids[counter])
        song_id = song_data["id"]
        name = song_data["name"]
        if len(song_data["artists"]) > 0:
            artists = song_data["artists"][0]["name"]
        else:
            artists = song_data["artists"]["name"]
        features_list.append(
            [
                song_id,
                name,
                artists,
                features["energy"],
                features["liveness"],
                features["tempo"],
                features["speechiness"],
                features["acousticness"],
                features["instrumentalness"],
                features["time_signature"],
                features["danceability"],
                features["key"],
                features["duration_ms"],
                features["loudness"],
                features["valence"],
                features["mode"],
                features["uri"],
            ]
        )
        counter += 1

    df = pd.DataFrame(
        features_list,
        columns=SONG_COLUMNS,
    )
    df = clean_songs_without_genre(df)
    return df


@check_output(null_schema_artists_data)
def transform_artist_data(raw_data: Dict, avoid_api=True):
    """Transform artists data.

    Parameters
    ----------
    raw_data : dict
        Extracted data from Spotify API.
    avoid_api : boolean
        Flag to avoid Spotify API by reading data from local storage.

    Returns
    -------
    df : pd.DataFrame
        Transformed/formatted DF.

    """
    logging.info("Running transform for artist data")
    if avoid_api:
        df = pd.read_csv(DATA_DIR / "transformed_artists_data.csv")
        return df
    json_results = []
    artists = []
    ids = []
    names = []
    followers = []
    popularity = []
    genres = []
    urls = []

    for item in raw_data["items"]:
        artists_data = item["track"]["artists"]
        for art in artists_data:
            artists.append(art["id"])
    for art in artists:
        json_results.append(sp.artist(f"{art}"))

    for i in json_results:
        ids.append(i["id"])
        names.append(i["name"])
        followers.append(i["followers"]["total"])
        popularity.append(i["popularity"])
        genres.append(i["genres"])
        urls.append(i["external_urls"]["spotify"])

    df = pd.DataFrame()
    df["id"] = ids
    df["name"] = names
    df["followers"] = followers
    df["popularity"] = popularity
    df["genre"] = genres
    df["url"] = urls
    df = clean_songs_without_genre(df)
    df = df.drop_duplicates(subset=["id"])
    logging.info("TRANSFORMED DF")
    logging.info(df)
    return df
