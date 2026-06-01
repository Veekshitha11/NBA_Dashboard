import os
import sys
import pandas as pd

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert (0, script_dir)

from player_loader import load_player_data


def compute_player_consistency():
    df = load_player_data()

    # Ensure numeric
    df["pts"] = pd.to_numeric(df["pts"], errors="coerce").fillna(0)

    # Sort values to ensure proper rolling calculations
    df = df.sort_values(["player_name", "season"]).reset_index(drop=True)

    # ----------------------------------------------------------
    # CONSISTENCY METRICS
    # ----------------------------------------------------------

    # Standard deviation of scoring
    consistency = (
        df.groupby("player_name")["pts"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )

    consistency.rename(
        columns={
            "mean": "avg_pts",
            "std": "pts_std",
            "count": "games_played",
        },
        inplace=True,
    )

    # Stability index = lower STD & more games = more stable
    consistency["stability_index"] = consistency["games_played"] / (
        1 + consistency["pts_std"]
    )

    # Sort from MOST consistent → least
    consistency = consistency.sort_values(
        ["stability_index"], ascending=False
    )

    return consistency


if __name__ == "__main__":

    # Build safe output path
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    out_path = os.path.join(out, "player_consistency.csv")

    result_df = compute_player_consistency()
    result_df.to_csv(out_path, index=False)

    print(f"Saved player consistency → {out_path}")
