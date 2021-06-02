import logging

import pandas as pd
from pangres import upsert
from sqlalchemy import create_engine

from spotydash.cfg import DB_CONNSTR
from spotydash.schemas import SCHEMAS


def load(df: pd.DataFrame, table: str):
    """Insert data to certain table using pangres (PostgreSQL).

    Parameters
    ----------
    df : pd.DataFrame
        Df to be inserted.

    """
    logging.info(f"Uploading {df.shape[0]} to pg")
    engine = create_engine(DB_CONNSTR)

    logging.info("DF to be loaded")
    logging.info(df)
    df.set_index(SCHEMAS[table]["KEY_COLS"], inplace=True)
    upsert(engine=engine, df=df, table_name=table, if_row_exists="update")
