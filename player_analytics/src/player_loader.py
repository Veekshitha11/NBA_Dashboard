import os
import pandas as pd


def convert_minutes(v):
    """Convert MIN safely: handles 'MM:SS', floats, None, blanks."""
    if pd.isna(v) or str(v).strip() == "":
        return 0.0

    v = str(v).strip()

    if ":" in v:
        try:
            m, s = v.split(":")
            return float(m) + float(s) / 60
        except:
            return 0.0

    try:
        return float(v)
    except:
        return 0.0


def extract_season(game_id):
    """GAME_ID → season. Example: 22200477 → 2022."""
    try:
        return 2000 + int(str(game_id)[1:3])
    except:
        return None


def load_player_data():
    # Get correct path: root/player_analytics/data/games_details.csv
    base = os.path.dirname(os.path.abspath(__file__))          # .../player_analytics/src
    root = os.path.dirname(base)                               # .../player_analytics
    data_path = os.path.join(root, "data", "games_details.csv")

    print("Loading player data from:", data_path)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ games_details.csv NOT FOUND:\n{data_path}")

    df = pd.read_csv(data_path, low_memory=False)
    df.columns = df.columns.str.strip().str.lower()   # standardize

    # REQUIRED COLUMNS (your CSV has them)
    needed = ["game_id", "player_name", "pts", "min"]
    for col in needed:
        if col not in df.columns:
            raise KeyError(f"❌ Missing column in CSV: {col}")

    # Minutes → float
    df["minutes"] = df["min"].apply(convert_minutes)

    # Numeric stats
    for stat in ["pts", "reb", "ast", "stl", "blk", "to"]:
        if stat in df.columns:
            df[stat] = pd.to_numeric(df[stat], errors="coerce").fillna(0)
        else:
            df[stat] = 0

    # Add season column
    df["season"] = df["game_id"].apply(extract_season)

    return df
