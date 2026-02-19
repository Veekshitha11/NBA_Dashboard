import os
import sys
import pandas as pd

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from player_loader import load_player_data


def preprocess_player_data():

    # Load raw player data
    df = load_player_data()

    # Clean column formats
    df.columns = df.columns.str.lower()

    # Fill missing values safely
    num_cols = ["fgm", "fga", "fg3m", "fg3a", "ftm", "fta",
                "oreb", "dreb", "reb", "ast", "stl", "blk",
                "to", "pf", "pts", "plus_minus"]

    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Return cleaned DF
    return df


if __name__ == "__main__":

    # Output directory
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    out_path = os.path.join(out, "preprocessed_player_data.csv")

    df = preprocess_player_data()
    df.to_csv(out_path, index=False)

    print(f"Saved preprocessed player data → {out_path}")
