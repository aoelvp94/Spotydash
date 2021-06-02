import logging
from datetime import datetime, timedelta

import mlflow

from spotydash.cfg import MLFLOW_TRACKING_URI
from spotydash.clustering import fit_clustering
from spotydash.extract import extract_current_songs
from spotydash.load import load
from spotydash.transform import transform_artist_data


def run_etfl_artists_data(execution_date: datetime):
    """Run Extract-Transform-Fit-Load process.

    Parameters
    ----------
    execution_date : Datetime Object
        Execution date / Date to query.

    """
    # Extract
    extracted_df = extract_current_songs(execution_date)

    # Transform
    transformed_df = transform_artist_data(extracted_df)

    # Fit
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("kmeans_clustering")
    with mlflow.start_run(run_name=f"kmeans_{execution_date}"):
        results_df = fit_clustering(transformed_df)

    # Load
    load(results_df, "Artist")
    logging.info("Done")


if __name__ == "__main__":
    date = datetime.today() - timedelta(days=1)
    run_etfl_artists_data(date)
