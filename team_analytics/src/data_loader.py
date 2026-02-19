import pandas as pd
import os

def load_data():
    # Get absolute path to this file → then to team_analytics folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)

    data_path = os.path.join(root_dir, "data", "processed_nba_data.csv")
    conf_path = os.path.join(root_dir, "data", "team_conference_map.csv")

    df = pd.read_csv(data_path)

    df.columns = df.columns.str.lower().str.strip()

    conf_map = pd.read_csv(conf_path)
    conf_map["team"] = conf_map["team"].str.lower()

    home_df = pd.DataFrame({
        "season": df["season"],
        "team": df["home_name"].str.lower(),
        "points_scored": df["homepoints"],
        "points_allowed": df["awaypoints"],
        "win": df["home_win"],
        "home_away": "Home",
        "pace": df.get("home_pace")
    })

    away_df = pd.DataFrame({
        "season": df["season"],
        "team": df["away_name"].str.lower(),
        "points_scored": df["awaypoints"],
        "points_allowed": df["homepoints"],
        "win": df["away_win"],
        "home_away": "Away",
        "pace": df.get("away_pace")
    })

    long_df = pd.concat([home_df, away_df], ignore_index=True)
    long_df = long_df.merge(conf_map, on="team", how="left")

    return long_df
