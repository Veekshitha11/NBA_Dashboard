import os
import sys
import pandas as pd

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from player_loader import load_player_data


def player_season_summary():
    df = load_player_data()
    print("✔ Player data loaded.")

    # FIX: Ensure season exists
    if "season" not in df.columns:
        raise KeyError("❌ season column missing — check GAME_ID format in CSV.")

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "outputs", "tables", "player_season_summary.csv"
    )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    summary = df.groupby(["season", "player_name"], as_index=False).agg({
        "pts": "mean",
        "reb": "mean",
        "ast": "mean",
        "stl": "mean",
        "blk": "mean",
        "to": "mean",
        "minutes": "mean"
    })

    summary.rename(columns={
        "pts": "avg_pts",
        "reb": "avg_reb",
        "ast": "avg_ast",
        "stl": "avg_stl",
        "blk": "avg_blk",
        "to": "avg_to",
        "minutes": "avg_minutes"
    }, inplace=True)

    summary.to_csv(out_path, index=False)
    print("✔ Saved:", out_path)

    return summary


if __name__ == "__main__":
    player_season_summary()
