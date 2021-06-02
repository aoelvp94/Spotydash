from spotydash.cfg import _p

MAPPER_PG_IS_LOCAL = {
    "yes": "true",
    "no": "false",
}

POPULARITY_DEFAULT_VALUE = 50

RESOURCES_PATH = _p / "resources"
DATA_DIR = RESOURCES_PATH / "data"
DAGS_DIR = _p / "dags"
USERNAME_ID = 11100099447
LIMIT_PLAYLISTS = 10

CLUSTERING_SCATTERPLOT_FILENAME = "scatter_clustering_plot.png"
ESTIMATOR_ARTIFACT = "kmeans_model.pkl"
