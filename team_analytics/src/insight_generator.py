import os
import pandas as pd

def generate_team_insights():
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(os.path.dirname(base), "outputs", "insights")
    os.makedirs(out_dir, exist_ok=True)

    table_dir = os.path.join(os.path.dirname(base), "outputs", "tables")

    season = pd.read_csv(os.path.join(table_dir, "team_season_summary.csv"))
    home_away = pd.read_csv(os.path.join(table_dir, "home_away_summary.csv"))

    text = []

    best_team = season.sort_values("win_pct", ascending=False).iloc[0]
    text.append(f"Top performing team: {best_team['team']} ({best_team['win_pct']:.2f})")

    out_path = os.path.join(out_dir, "team_insights.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(text))

    print("Saved:", out_path)

if __name__ == "__main__":
    generate_team_insights()
