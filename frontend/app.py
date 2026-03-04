"""Streamlit frontend – Brno Parking Dynamic Pricing."""

import os

import requests
import pandas as pd
import streamlit as st

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000").rstrip("/")
CSV_PATH = "carparks_live1_479300718152875721.csv"

st.set_page_config(page_title="Brno Parking – AI Pricing", layout="wide")
st.title("🅿️ Brno Parking – AI Dynamic Pricing")

# ── Sidebar inputs ──────────────────────────────────────────────────────────
zone = st.sidebar.selectbox(
    "Parking Zone",
    options=["A", "B", "C"],
    format_func=lambda z: {
        "A": "A – Husova, Janáčkovo (60 CZK)",
        "B": "B – Veveří (40 CZK)",
        "C": "C – P+R (20 CZK)",
    }[z],
)
hour = st.sidebar.slider("Hour of day", min_value=0, max_value=23, value=12)

# ── API call ────────────────────────────────────────────────────────────────
if st.sidebar.button("Get Price", type="primary"):
    try:
        resp = requests.get(
            f"{API_BASE}/get-price", params={"zone": zone, "hour": hour}, timeout=5
        )
        resp.raise_for_status()
        data = resp.json()

        col1, col2, col3 = st.columns(3)
        col1.metric("Zone", data["zone"])
        col2.metric("Predicted Occupancy", f"{data['predicted_occupancy']:.1f} %")
        col3.metric(
            "Final Price",
            f"{data['final_price']:.0f} CZK",
            delta="SURGE" if data["surge"] else None,
            delta_color="inverse" if data["surge"] else "off",
        )
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend API at 127.0.0.1:8000. Is the server running?")
    except Exception as exc:
        st.error(f"Error: {exc}")

# ── Map ─────────────────────────────────────────────────────────────────────
st.subheader("Parking Locations in Brno")

df = pd.read_csv(CSV_PATH, encoding="utf-8")
df = df.dropna(subset=["Latitude", "Longitude"])

# st.map expects columns named 'latitude' and 'longitude' (or 'lat'/'lon')
map_df = df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
st.map(map_df[["latitude", "longitude"]])
