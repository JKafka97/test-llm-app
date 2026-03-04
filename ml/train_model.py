"""Train a RandomForestRegressor to predict parking occupancy rate."""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "carparks_live1_479300718152875721.csv",
)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

PEAK_HOURS = set(range(8, 11)) | set(range(16, 20))  # 8-10, 16-19
NIGHT_HOURS = set(list(range(22, 24)) + list(range(0, 6)))  # 22-05


def train() -> None:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")

    # occupancy_rate = 100 - capacity_procent  (capacity_procent ≈ % free)
    df["occupancy_rate"] = 100.0 - df["capacity_procent"].astype(float)

    rows = []
    for _, row in df.iterrows():
        base_occ = row["occupancy_rate"]
        for hour in range(24):
            for day_of_week in range(7):
                occ = base_occ
                if hour in PEAK_HOURS:
                    occ = occ * 1.20  # increase by 20 %
                elif hour in NIGHT_HOURS:
                    occ = occ * 0.50  # decrease by 50 %
                occ = np.clip(occ, 0, 100)
                rows.append(
                    {
                        "hour": hour,
                        "day_of_week": day_of_week,
                        "occupancy_rate": occ,
                    }
                )

    train_df = pd.DataFrame(rows)

    X = train_df[["hour", "day_of_week"]]
    y = train_df["occupancy_rate"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
