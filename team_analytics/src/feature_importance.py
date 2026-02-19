import pandas as pd
import os
import sys
from sklearn.ensemble import RandomForestClassifier

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from data_loader import load_data

def compute_feature_importance():
    df = load_data()

    df["point_diff"] = df["points_scored"] - df["points_allowed"]

    features = ["points_scored", "points_allowed", "point_diff", "pace"]
    df = df.dropna(subset=features)

    X = df[features]
    y = df["win"]

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, y)

    importance_df = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)

    # Save output
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(os.path.dirname(base), "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "feature_importance.csv")
    importance_df.to_csv(out_path, index=False)

    print("Saved:", out_path)

if __name__ == "__main__":
    compute_feature_importance()
