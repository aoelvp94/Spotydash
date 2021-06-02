SONG_COLUMNS = [
    "id",
    "name",
    "artist",
    "energy",
    "liveness",
    "tempo",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "time_signature",
    "danceability",
    "key",
    "duration_ms",
    "loudness",
    "valence",
    "mode",
    "uri",
]

ARTIST_COLUMNS = ["id", "name", "followers", "popularity", "genre", "url", "label"]


SCHEMAS = {
    "Song": {
        "SCHEMA": SONG_COLUMNS,
        "KEY_COLS": ["id"],
    },
    "Artist": {
        "SCHEMA": ARTIST_COLUMNS,
        "KEY_COLS": ["id"],
    },
}
