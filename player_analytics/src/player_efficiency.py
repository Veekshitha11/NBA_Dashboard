import os
import sys
import pandas as pd

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from player_loader import load_player_data


def compute_player_efficiency():
    df = load_player_data()

    # Convert columns to numeric safely
    numeric_cols = ["pts", "oreb", "dreb", "reb", "ast", "stl", "blk", "to", "minutes"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ----------------------------------------------------------
    # BASIC PLAYER EFFICIENCY FORMULA (NBA EFF)
    # EFF = (PTS + REB + AST + STL + BLK) − (MISS FG + MISS FT + TO)
    # ----------------------------------------------------------
    df["fg_miss"] = df["fga"] - df["fgm"]
    df["ft_miss"] = df["fta"] - df["ftm"]

    df["EFF"] = (
        df["pts"]
        + df["reb"]
        + df["ast"]
        + df["stl"]
        + df["blk"]
        - df["fg_miss"]
        - df["ft_miss"]
        - df["to"]
    )

    # Per minute efficiency
    df["EFF_per_min"] = df["EFF"] / df["minutes"].replace(0, pd.NA)
    df["EFF_per_min"] = df["EFF_per_min"].fillna(0).astype(float)


    # Aggregate per player per season
    summary = (
        df.groupby(["season", "player_name"])
        .agg(
            games_played=("game_id", "count"),
            total_eff=("EFF", "sum"),
            avg_eff=("EFF", "mean"),
            avg_eff_per_min=("EFF_per_min", "mean"),
            avg_pts=("pts", "mean"),
            avg_reb=("reb", "mean"),
            avg_ast=("ast", "mean"),
        )
        .reset_index()
    )

    # Ranking
    summary = summary.sort_values("avg_eff", ascending=False)

    return summary


if __name__ == "__main__":

    # Output folder path
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    out_path = os.path.join(out, "player_efficiency.csv")

    df = compute_player_efficiency()
    df.to_csv(out_path, index=False)

    print(f"Saved player efficiency → {out_path}")
