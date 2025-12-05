# core/shocks.py
import numpy as np


def shock_forecast_module() -> dict:
    try:
        shocks = {
            "price_shock": float(np.random.uniform(-0.12, 0.18)),
            "feed_cost_shock": float(np.random.uniform(-0.08, 0.16)),
            "weather_shock": float(np.random.uniform(-0.15, 0.20)),
        }
        return shocks
    except Exception:
        return {
            "price_shock": 0.0,
            "feed_cost_shock": 0.0,
            "weather_shock": 0.0,
        }
