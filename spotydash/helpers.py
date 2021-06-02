"""
Project dependant helper code used in multiple files.
"""


import logging
import pickle

from spotydash.cfg import sp
from spotydash.constants import DATA_DIR, LIMIT_PLAYLISTS, USERNAME_ID


def get_user_playlist(avoid_api=True):
    """From a given user, get his playlists.

    Parameters
    ----------
    avoid_api : bool
        Flag to avoid call to Spotify API.

    Returns
    -------
    playlists_list : list(str)
        List that contains ids playlists for a given user.

    """
    if avoid_api:
        logging.info("avoid_api = True, reading data from local storage..")
        with open(DATA_DIR / "playlists.pickle", "rb") as handle:
            playlists_list = pickle.load(handle)
    else:
        logging.info("avoid_api = False, reading data from Spotify API..")
        playlists = sp.user_playlists(USERNAME_ID)
        playlists_list = []
        for playlist in playlists["items"]:
            playlists_list.append(playlist["id"])
    return playlists_list[:LIMIT_PLAYLISTS]
