import pandas as pd
import os
import sys

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from data_loader import load_data

def team_consistency():
    df = load_data()

    rankings = df.groupby("team")["points_scored"].std().reset_index()
    rankings.columns = ["team", "std_dev"]
    rankings = rankings.sort_values("std_dev")

    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    rankings.to_csv(os.path.join(out, "team_rankings.csv"), index=False)
    print("Saved:", os.path.join(out, "team_rankings.csv"))

if __name__ == "__main__":
    team_consistency()
