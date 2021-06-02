""" Data validations using Pandera """

import pandera as pa
from pandera import Check, Column, DataFrameSchema

null_schema_artists_data = DataFrameSchema(
    {
        "id": Column(pa.Object, Check(lambda x: len(x) > 0), nullable=False),
        "name": Column(pa.Object, Check(lambda x: len(x) > 0), nullable=False),
        "followers": Column(pa.Int, Check(lambda x: x >= 0), nullable=False),
        "popularity": Column(pa.Int, Check(lambda x: x >= 0), nullable=False),
        "genre": Column(pa.Object, Check(lambda x: len(x) > 0), nullable=False),
        "url": Column(pa.Object, Check(lambda x: len(x) > 0), nullable=False),
    }
)
