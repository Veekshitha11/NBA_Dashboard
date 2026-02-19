# import os
# import pandas as pd


# def generate_player_insights():
#     base = os.path.dirname(os.path.abspath(__file__))
#     out_dir = os.path.join(os.path.dirname(base), "outputs", "insights")
#     os.makedirs(out_dir, exist_ok=True)

#     # ---------------------------
#     # Load necessary tables
#     # ---------------------------
#     tables_dir = os.path.join(os.path.dirname(base), "outputs", "tables")

#     season_path = os.path.join(tables_dir, "player_season_summary.csv")
#     cluster_path = os.path.join(tables_dir, "player_clusters.csv")
#     predict_path = os.path.join(tables_dir, "player_predictions.csv")

#     season_df = pd.read_csv(season_path)
#     cluster_df = pd.read_csv(cluster_path)
#     pred_df = pd.read_csv(predict_path)

#     insights = []
#     insights.append("🏀 PLAYER ANALYTICS – AUTO-GENERATED INSIGHTS\n")

#     # ------------------------------------------------
#     # 1. Top Scorers Insight
#     # ------------------------------------------------
#     top_scorers = season_df.sort_values("avg_pts", ascending=False).head(5)

#     insights.append("🔥 Top 5 Scorers in the League:")
#     for _, row in top_scorers.iterrows():
#         insights.append(f"- {row['player_name']} averaged {row['avg_pts']:.1f} PPG.")

#     insights.append("\n")

#     # ------------------------------------------------
#     # 2. Player Roles (Clusters)
#     # ------------------------------------------------
#     insights.append("🎯 Player Roles (Cluster-Based):")
#     role_counts = cluster_df["role"].value_counts()

#     for role, count in role_counts.items():
#         insights.append(f"- {role}: {count} players")

#     insights.append("\n")

#     # ------------------------------------------------
#     # 3. Most Consistent Players (using low std dev)
#     # ------------------------------------------------
#     season_df["pts_variability"] = season_df["std_pts"]

#     consistent = season_df.sort_values("pts_variability").head(5)

#     insights.append("📉 Most Consistent Players:")
#     for _, row in consistent.iterrows():
#         insights.append(f"- {row['player_name']} (Std Dev: {row['pts_variability']:.2f})")

#     insights.append("\n")

#     # ------------------------------------------------
#     # 4. Predicted High Performers
#     # ------------------------------------------------
#     pred_df_grouped = pred_df.groupby("player_name")["predicted_pts"].mean().reset_index()
#     top_predicted = pred_df_grouped.sort_values("predicted_pts", ascending=False).head(5)

#     insights.append("🔮 Players Projected to Score Highly in Future Games:")
#     for _, row in top_predicted.iterrows():
#         insights.append(f"- {row['player_name']} is projected {row['predicted_pts']:.1f} PTS per game.")

#     insights.append("\n✓ End of insights.\n")

#     # Save insights file
#     out_path = os.path.join(out_dir, "player_insights.txt")
#     with open(out_path, "w") as f:
#         f.write("\n".join(insights))

#     print("Saved:", out_path)


# if __name__ == "__main__":
#     generate_player_insights()






import os
import pandas as pd


def generate_player_insights():
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(os.path.dirname(base), "outputs", "insights")
    os.makedirs(out_dir, exist_ok=True)

    # ---------------------------
    # Load necessary tables
    # ---------------------------
    tables_dir = os.path.join(os.path.dirname(base), "outputs", "tables")

    season_path = os.path.join(tables_dir, "player_season_summary.csv")
    cluster_path = os.path.join(tables_dir, "player_clusters.csv")
    predict_path = os.path.join(tables_dir, "player_predictions.csv")
    consistency_path = os.path.join(tables_dir, "player_consistency.csv")

    season_df = pd.read_csv(season_path)
    cluster_df = pd.read_csv(cluster_path)
    pred_df = pd.read_csv(predict_path)
    consistency_df = pd.read_csv(consistency_path)

    insights = []
    insights.append("🏀 PLAYER ANALYTICS – AUTO-GENERATED INSIGHTS\n")

    # ------------------------------------------------
    # 1. Top Scorers Insight
    # ------------------------------------------------
    top_scorers = season_df.sort_values("avg_pts", ascending=False).head(5)

    insights.append("🔥 Top 5 Scorers in the League:")
    for _, row in top_scorers.iterrows():
        insights.append(f"- {row['player_name']} averaged {row['avg_pts']:.1f} PPG.")

    insights.append("\n")

    # ------------------------------------------------
    # 2. Player Roles (Clusters)
    # ------------------------------------------------
    insights.append("🎯 Player Roles (Cluster-Based):")
    role_counts = cluster_df["role"].value_counts()

    for role, count in role_counts.items():
        insights.append(f"- {role}: {count} players")

    insights.append("\n")

    # ------------------------------------------------
    # 3. Most Consistent Players (using low std dev)
    # ------------------------------------------------
    consistent = consistency_df.sort_values("pts_std").head(5)

    insights.append("📉 Most Consistent Players:")
    for _, row in consistent.iterrows():
        insights.append(f"- {row['player_name']} (Std Dev: {row['pts_std']:.2f})")

    insights.append("\n")

    # ------------------------------------------------
    # 4. Predicted High Performers
    # ------------------------------------------------
    pred_df_grouped = pred_df.groupby("player_name")["predicted_pts"].mean().reset_index()
    top_predicted = pred_df_grouped.sort_values("predicted_pts", ascending=False).head(5)

    insights.append("🔮 Players Projected to Score Highly in Future Games:")
    for _, row in top_predicted.iterrows():
        insights.append(f"- {row['player_name']} is projected {row['predicted_pts']:.1f} PTS per game.")

    insights.append("\n✓ End of insights.\n")

    # Save insights file
    out_path = os.path.join(out_dir, "player_insights.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(insights))

    print("Saved:", out_path)


if __name__ == "__main__":
    generate_player_insights()