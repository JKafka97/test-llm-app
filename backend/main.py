"""FastAPI backend – Brno dynamic parking pricing."""

import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Brno Parking Dynamic Pricing",
    description="API for dynamic parking pricing in Brno based on ML-predicted occupancy.",
    version="1.0.0",
    docs_url="/docs",          # Swagger UI
    redoc_url="/redoc",        # ReDoc alternative
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Zone → base price mapping
# ---------------------------------------------------------------------------
ZONE_MAP: dict[str, float] = {
    "A": 60.0,  # Husova, Janáčkovo
    "B": 40.0,  # Veveří
    "C": 20.0,  # P+R
}
DEFAULT_PRICE = 30.0

# ---------------------------------------------------------------------------
# Load ML model once at startup
# ---------------------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "model.pkl")

model = None


@app.on_event("startup")
def _load_model() -> None:
    global model
    model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------
@app.get("/get-price")
def get_price(
    zone: str = Query(..., description="Parking zone: A, B, or C"),
    hour: int = Query(
        default_factory=lambda: datetime.now().hour,
        ge=0,
        le=23,
        description="Hour of day (0-23)",
    ),
):
    zone_upper = zone.upper()
    base_price = ZONE_MAP.get(zone_upper, DEFAULT_PRICE)

    # Predict occupancy
    day_of_week = datetime.now().weekday()
    predicted_occ: float = float(
        model.predict(np.array([[hour, day_of_week]]))[0]
    )
    predicted_occ = round(min(max(predicted_occ, 0.0), 100.0), 2)

    # Surge logic
    surge = False
    final_price = base_price
    if predicted_occ > 80:
        final_price = base_price * 1.5
        surge = True
    elif predicted_occ < 20:
        final_price = base_price * 0.7

    return {
        "zone": zone_upper,
        "predicted_occupancy": predicted_occ,
        "final_price": round(final_price, 2),
        "surge": surge,
    }
