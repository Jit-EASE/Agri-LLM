# core/monte_carlo.py
import numpy as np


def monte_carlo_module(csv_result=None) -> dict:
    if csv_result is None or csv_result.get("status") != "ok" or not csv_result.get("numeric_cols"):
        sims = 500
        prices = np.random.normal(0, 0.12, sims)
        costs = np.random.normal(0, 0.10, sims)
        margins = prices - costs
    else:
        df = csv_result["raw"]
        num_col = csv_result["numeric_cols"][0]
        ts = df[num_col].dropna().values

        if len(ts) < 10:
            base = ts if len(ts) > 0 else np.array([0])
            sims = np.random.normal(
                np.mean(base),
                np.std(base) if np.std(base) > 0 else 0.05,
                500,
            )
        else:
            sims_list = []
            for _ in range(500):
                sample = np.random.choice(ts, size=len(ts), replace=True)
                shock = np.random.normal(0, np.std(ts) * 0.3)
                sims_list.append(np.mean(sample) + shock)
            sims = np.array(sims_list)

    return {
        "mc_mean": float(np.mean(sims)),
        "mc_std": float(np.std(sims)),
        "mc_p05": float(np.percentile(sims, 5)),
        "mc_p25": float(np.percentile(sims, 25)),
        "mc_p50": float(np.percentile(sims, 50)),
        "mc_p75": float(np.percentile(sims, 75)),
        "mc_p95": float(np.percentile(sims, 95)),
    }
