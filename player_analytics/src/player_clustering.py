import os
import sys
import pandas as pd
from sklearn.cluster import KMeans

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from player_performance import player_season_summary


def run_player_clustering(n_clusters=3):
    df = player_season_summary().copy()

    # Select features for clustering
    features = df[["avg_pts", "avg_reb", "avg_ast", "avg_minutes"]].fillna(0)

    # Fit K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    df["cluster"] = kmeans.fit_predict(features)

    # Map cluster names (simple role interpretation)
    role_map = {
        0: "Role Player",
        1: "Star Player",
        2: "Bench Player"
    }

    df["role"] = df["cluster"].map(role_map)

    return df


if __name__ == "__main__":
    # Output directory
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    out_path = os.path.join(out, "player_clusters.csv")

    df = run_player_clustering()
    df.to_csv(out_path, index=False)

    print("Saved:", out_path)
