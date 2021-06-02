import logging
import pickle
from datetime import datetime

from spotydash.cfg import sp
from spotydash.constants import DATA_DIR, USERNAME_ID


def get_playlist_audio_features(playlist_id: str):
    """Get info about songs for a certain playlist.

    Parameters
    ----------
    playlist_id : str
        Playlist ID

    Returns
    -------
    audio_features : list(JSON)
        List that contains info about songs.
    ids : list(str)
        List that containts songs IDs.

    """

    offset = 0
    songs = []
    ids = []
    content = sp.user_playlist_tracks(
        USERNAME_ID,
        playlist_id,
        fields=None,
        limit=None,
        offset=offset,
        market=None,
    )
    songs += content["items"]

    for i in songs:
        ids.append(i["track"]["id"])

    index = 0
    audio_features = []
    while index < len(ids):
        try:
            audio_features += sp.audio_features(ids[index : index + 50])  # noqa: E203
            index += 50
        except:  # noqa: E722
            pass
    return audio_features, ids


def extract_current_songs(execution_date: datetime, avoid_api=True, limit=None):
    """Get limit elements from last listen tracks

    Parameters
    ----------
    ds : Datetime object
        Date to query
    avoid_api : boolean
        Flag to avoid Spotify API by reading data from local storage.
    limit : int
        Limit of element to query

    Returns
    -------
    result : dict
        Result from Spotify API

    """
    if avoid_api:
        logging.info("avoid_api = True, reading data from local storage..")
        with open(DATA_DIR / "current_songs.pickle", "rb") as handle:
            result = pickle.load(handle)
    else:
        logging.info("avoid_api = False, reading data from Spotify API..")
        ds = int(execution_date.timestamp()) * 1000
        result = sp.current_user_recently_played(limit=limit, after=ds)
    return result
