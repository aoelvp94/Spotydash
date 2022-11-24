import logging
import pickle

import mlflow
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)

from sklearn.preprocessing import MinMaxScaler

from spotydash.cfg import KMEANS_PARAMS
from spotydash.constants import (
    CLUSTERING_SCATTERPLOT_FILENAME,
    DATA_DIR,
    ESTIMATOR_ARTIFACT,
)
from spotydash.plot import generate_scatter_plot


def fit_clustering(df: pd.DataFrame):
    """ Run a clustering algorithm and log metrics/artifacts/params/model.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to process clustering.

    Returns
    -------
    df : pd.DataFrame
        Df with results.

    """
    logging.info("Going to process clustering..")
    X = df[["followers", "popularity"]]
    s = MinMaxScaler()
    Scaled_X = s.fit_transform(X)
    # df_X_reduced = pd.DataFrame(Scaled_X, index=X.index, columns=X.columns)
    mlflow.log_params(KMEANS_PARAMS)
    kmeans = KMeans(**KMEANS_PARAMS).fit(Scaled_X)
    mlflow.sklearn.log_model(kmeans, "kmeans_model")
    with open(DATA_DIR / ESTIMATOR_ARTIFACT, "wb") as file:
        pickle.dump(kmeans, file)
    mlflow.log_artifact(DATA_DIR / ESTIMATOR_ARTIFACT)
    # y_kmeans = kmeans.predict(X)
    df["label"] = kmeans.labels_
    Scaled_X = pd.DataFrame(Scaled_X, columns=["followers", "popularity"])
    Scaled_X["label"] = kmeans.labels_
    centers = kmeans.cluster_centers_
    Scaled_X["name"] = list(df["name"])
    generate_scatter_plot(Scaled_X, centers)
    mlflow.log_artifact(DATA_DIR / CLUSTERING_SCATTERPLOT_FILENAME)
    del Scaled_X["name"]
    ch_score = calinski_harabasz_score(Scaled_X, df["label"])
    db_score = davies_bouldin_score(Scaled_X, df["label"])
    s_score = silhouette_score(Scaled_X, df["label"])
    mlflow.log_metric("calinski_harabasz_score", ch_score)
    mlflow.log_metric("davies_bouldin_score", db_score)
    mlflow.log_metric("silhouette_score", s_score)

    return df
