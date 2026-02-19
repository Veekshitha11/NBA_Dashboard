import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Add script directory to path so imports work when run from base directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from data_loader import load_data

def train_models():
    df = load_data()

    # Feature engineering
    df["point_diff"] = df["points_scored"] - df["points_allowed"]

    features = ["points_scored", "points_allowed", "point_diff", "pace"]
    df = df.dropna(subset=features)

    X = df[features]
    y = df["win"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # Save model accuracy
    base = os.path.dirname(os.path.abspath(__file__))
    insights_dir = os.path.join(os.path.dirname(base), "outputs", "insights")
    os.makedirs(insights_dir, exist_ok=True)

    with open(os.path.join(insights_dir, "model_insights.txt"), "w") as f:
        f.write(f"Win prediction accuracy: {acc:.4f}")

    print("Model insights saved.")

if __name__ == "__main__":
    train_models()
