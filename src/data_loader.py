"""Load and validate IPL data; auto-generate if missing."""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MATCHES_PATH = os.path.join(DATA_DIR, "matches.csv")
DELIVERIES_PATH = os.path.join(DATA_DIR, "deliveries.csv")


def _ensure_data():
    if not os.path.exists(MATCHES_PATH) or not os.path.exists(DELIVERIES_PATH):
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
