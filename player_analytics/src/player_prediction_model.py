import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from player_loader import load_player_data


def train_player_prediction_model():

    df = load_player_data()

    # Keep only relevant columns
    required_cols = ["season", "player_name", "pts", "reb", "ast", "minutes"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    df["pts"] = pd.to_numeric(df["pts"], errors="coerce").fillna(0)
    df["reb"] = pd.to_numeric(df["reb"], errors="coerce").fillna(0)
    df["ast"] = pd.to_numeric(df["ast"], errors="coerce").fillna(0)
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce").fillna(0)

    # -----------------------------------------------
    # FIXED: Rolling features WITHOUT MultiIndex crash
    # -----------------------------------------------

    df = df.sort_values(["player_name", "season"]).reset_index(drop=True)

    df["pts_last3"] = (
        df.groupby("player_name")["pts"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean().shift(1))
    )

    df["reb_last3"] = (
        df.groupby("player_name")["reb"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean().shift(1))
    )

    df["ast_last3"] = (
        df.groupby("player_name")["ast"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean().shift(1))
    )

    # Fill initial NaNs after shifting
    df.fillna(0, inplace=True)

    # Model features
    features = ["pts_last3", "reb_last3", "ast_last3", "minutes"]
    target = "pts"

    X = df[features]
    y = df[target]

    # Train simple regression
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict
    df["predicted_pts"] = model.predict(X)

    return df[["season", "player_name", "pts", "predicted_pts"]]


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out, exist_ok=True)

    out_path = os.path.join(out, "player_predictions.csv")

    pred_df = train_player_prediction_model()
    pred_df.to_csv(out_path, index=False)

    print(f"Saved player predictions → {out_path}")
