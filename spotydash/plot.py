from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from spotydash.constants import CLUSTERING_SCATTERPLOT_FILENAME, DATA_DIR


def generate_scatter_plot(df: pd.DataFrame, centers: Iterable):
    """Generate scatter plot using clustering results.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to be plotted.
    centers : Array
        Array that contains centers for each cluster.

    """
    # Getting the values and plotting it
    f1 = df["followers"].values
    f2 = df["popularity"].values
    colores = ["red", "green", "blue", "cyan"]  # 'yellow', 'brown']
    asignar = []
    for row in list(df["label"]):
        asignar.append(colores[row])

    plt.scatter(f1, f2, c=asignar, s=70)
    plt.scatter(centers[:, 0], centers[:, 1], marker="*", c=colores, s=500)

    for i in range(df.shape[0]):
        plt.text(
            x=df.followers[i],
            y=df.popularity[i],
            s=df.name[i],
            fontdict=dict(color='red', size=10),
        )
    plt.savefig(
        DATA_DIR / CLUSTERING_SCATTERPLOT_FILENAME, dpi=300, bbox_inches="tight"
    )
