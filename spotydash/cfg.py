from pathlib import Path

import spotipy
from decouple import config
from pkg_resources import resource_filename
from spotipy import SpotifyOAuth

_p = Path(resource_filename("spotydash", "/"))

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = config("SPOTIPY_REDIRECT_URI")
DB_CONNSTR = config("DB_CONNSTR")

PG_CFG = {
    "dialect": config("POSTGRES_DIALECT", default="postgres", cast=str),
    "driver": config("POSTGRES_DRIVER", default="psycopg2", cast=str),
    "username": config("POSTGRES_USER", default="spotydash", cast=str),
    "password": config("POSTGRES_PASSWORD", default="spotydash", cast=str),
    "host": config("POSTGRES_HOST", default="postgres-db", cast=str),
    "port": config("POSTGRES_PORT", default=5432, cast=int),
    "database": config("POSTGRES_DB", default="db", cast=str),
    "db_type": config("POSTGRES_DB_TYPE", default="postgres", cast=str),
}


MLFLOW_CFG = {
    "host": config("MLFLOW_HOST", default="mlflow-server", cast=str),
    "ui_port": config("MLFLOW_UI_PORT", default=80, cast=int),
    "server_port": config("MLFLOW_SERVER_PORT", default=5000, cast=int),
    "username": config("MLFLOW_POSTGRES_USER", default="mlflow", cast=str),
    "password": config("MLFLOW_POSTGRES_PASSWORD", default="mlflow", cast=str),
    "database": config("MLFLOW_POSTGRES_DB", default="mlflowdb", cast=str),
    "artifact_root": config(
        "MLFLOW_ARTIFACT_ROOT", default="/spotydash/resources/tmp/mlruns/", cast=str
    ),
    "tracking_user": config("MLFLOW_TRACKING_USER", default="mlflow", cast=str),
    "tracking_password": config("MLFLOW_TRACKING_PASSWORD", default="mlflow", cast=str),
}


MLFLOW_TRACKING_URI = (
    "http://{tracking_user}:{tracking_password}@{host}:{server_port}".format(
        **MLFLOW_CFG
    )
)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-read-recently-played",
    )
)

KMEANS_PARAMS = {"n_clusters": 4, "random_state": 0}
