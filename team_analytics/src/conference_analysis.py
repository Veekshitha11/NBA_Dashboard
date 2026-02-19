import pandas as pd
import os
import sys

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from data_loader import load_data

def conference_summary():
    df = load_data()

    summary = df.groupby(["season", "conference"]).agg(
        avg_points=("points_scored", "mean"),
        win_rate=("win", "mean")
    ).reset_index()

    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    summary.to_csv(os.path.join(out, "conference_summary.csv"), index=False)
    print("Saved:", os.path.join(out, "conference_summary.csv"))

if __name__ == "__main__":
    conference_summary()
    