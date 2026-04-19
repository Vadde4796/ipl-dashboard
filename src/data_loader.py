"""Load and validate IPL data; auto-generate if missing."""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MATCHES_PATH = os.path.join(DATA_DIR, "matches.csv")
DELIVERIES_PATH = os.path.join(DATA_DIR, "deliveries.csv")
PLAYERS_PATH = os.path.join(DATA_DIR, "players.csv")
SEASONS_PATH = os.path.join(DATA_DIR, "seasons.csv")

_ALL_PATHS = [MATCHES_PATH, DELIVERIES_PATH, PLAYERS_PATH, SEASONS_PATH]


def _ensure_data():
    if not all(os.path.exists(p) for p in _ALL_PATHS):
        from src.generate_data import main
        main()


def load_matches() -> pd.DataFrame:
    _ensure_data()
    df = pd.read_csv(MATCHES_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def load_deliveries() -> pd.DataFrame:
    _ensure_data()
    return pd.read_csv(DELIVERIES_PATH)


def load_players() -> pd.DataFrame:
    _ensure_data()
    return pd.read_csv(PLAYERS_PATH)


def load_seasons() -> pd.DataFrame:
    _ensure_data()
    return pd.read_csv(SEASONS_PATH)
