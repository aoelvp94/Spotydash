import logging

from sqlalchemy import ARRAY, BigInteger, Column, Float, MetaData, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from spotydash.cfg import DB_CONNSTR

engine = create_engine(DB_CONNSTR) if DB_CONNSTR else None
meta = MetaData(engine)
Base = declarative_base(metadata=meta)


class Song(Base):
    __tablename__ = "Song"

    id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    energy = Column(Float, nullable=False)
    liveness = Column(Float, nullable=False)
    tempo = Column(Float, nullable=False)
    speechiness = Column(Float, nullable=False)
    acousticness = Column(Float, nullable=False)
    instrumentalness = Column(Float, nullable=False)
    time_signature = Column(BigInteger, nullable=False)
    danceability = Column(Float, nullable=False)
    key = Column(BigInteger, nullable=False)
    duration_ms = Column(BigInteger, nullable=False)
    loudness = Column(Float, nullable=False)
    valence = Column(Float, nullable=False)
    mode = Column(BigInteger, nullable=False)
    uri = Column(String(255), nullable=False)


class Artist(Base):
    __tablename__ = "Artist"

    id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    followers = Column(BigInteger, nullable=False)
    popularity = Column(BigInteger, nullable=False)
    genre = Column(ARRAY(String), nullable=False)
    url = Column(String(255), nullable=False)
    label = Column(BigInteger, nullable=False)


if __name__ == "__main__":
    logging.info("Creating tables..")
    Base.metadata.create_all()
