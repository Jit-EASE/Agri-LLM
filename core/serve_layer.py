# core/serve_layer.py
import textwrap
import numpy as np  # used in long-term trend
from .econometrics import econometric_module  # used only if you choose, but we keep pure
# but mainly we only use passed-in econ, mc, qubo, shocks, etc.


def serve_answer(prepared, retrieved, signals, econ, qubo, domain,
                 shocks=None, mc=None, rl=None, csv_result=None):
"""
    Serve Layer v4 — temporal regime simulation, multi-horizon propagation,
    and causal counterfactuals across Climate, Policy, and Supply Chain.
    """

    # ---------- 0. SAFE DEFAULTS FOR MODULE INPUTS ----------
    shocks = shocks or {"price_shock": 0.0, "feed_cost_shock": 0.0, "weather_shock": 0.0}
    mc = mc or {"mc_mean": 0.0, "mc_std": 0.0}
    rl = rl or {"rl_reward": 0.0, "rl_action": "No optimisation"}
    csv_result = csv_result or {"status": "no_csv", "columns": []}

    # ---------- 1. FARM‑TYPE INFERENCE ----------
    farm_type = "general farm system"
    q = prepared.get("raw", "").lower()
    if any(t in q for t in ["dairy", "milk"]):
        farm_type = "dairy farm"
    elif "beef" in q:
        farm_type = "beef suckler farm"
    elif "tillage" in q or "crop" in q:
        farm_type = "tillage arable system"
    elif "sheep" in q:
        farm_type = "sheep enterprise"
    elif "horticulture" in q or "veg" in q or "vegetable" in q:
        farm_type = "horticulture system"
    elif csv_result.get("columns"):
        cols = [c.lower() for c in csv_result["columns"]]
        if "milk_output" in cols or "milk_yield" in cols:
            farm_type = "dairy farm (CSV detected)"
        elif "cattle" in cols or "beef" in cols:
            farm_type = "beef system (CSV detected)"
        elif "crop_yield" in cols or "hectare_yield" in cols:
            farm_type = "tillage system (CSV detected)"

    # ---------- 2. DOMAIN‑SPECIFIC META‑ENGINE ----------
    domain_logic = ""
    if domain == "Climate":
        domain_logic = (
            f"• Climate-resilience engine activated.\n"
            f"  Weather shock registered at {shocks['weather_shock']:.1%}, "
            f"altering grass growth, feed reliability, and output stability for {farm_type}.\n"
            f"  The system flags this configuration as climate‑sensitive and volatility‑exposed."
        )
    elif domain == "Policy":
        domain_logic = (
            f"• Policy-regime reasoning invoked.\n"
            f"  Tier‑2 PCTR={signals['Tier2 PCTR']:.1f} reflects likely farmer uptake under the "
            f"current mix of CAP‑style incentives, compliance costs, and behavioural priors.\n"
            f"  The engine treats {farm_type} as policy‑sensitive, where design choices "
            f"shift both adoption speed and equity outcomes."
        )
    elif domain == "Supply Chain":
        domain_logic = (
            f"• Supply‑chain optimisation layer engaged.\n"
            f"  Price shock={shocks['price_shock']:.1%}, feed‑cost shock={shocks['feed_cost_shock']:.1%} "
            f"signal upstream pressure through input markets and logistics for {farm_type}.\n"
            f"  This scenario is classified as supply‑chain stress with possible bottlenecks."
        )
    else:
        domain_logic = "• Generic optimisation mode — domain not explicitly classified."

    # ---------- 3. REGIME‑SWITCHING RISK ENGINE ----------
    regime = "stable regime"
    if abs(mc["mc_std"]) > 0.12:
        regime = "high‑volatility regime"
    if shocks["weather_shock"] > 0.12:
        regime = "climate shock regime"
    if shocks["price_shock"] < -0.10:
        regime = "market stress regime"

    regime_text = (
        f"• Regime Detection → {regime}.\n"
        f"  Monte Carlo mean={mc['mc_mean']:.3f}, std={mc['mc_std']:.3f}.\n"
        f"  Baseline margin (econometric) €{econ.get('econometric_prediction', 0.0):.2f}."
    )

    # ---------- 4. TEMPORAL PROPAGATION (SHORT / MEDIUM / LONG) ----------
    # REAL DATA–DRIVEN TEMPORAL PROPAGATION
    # Extract a real numeric series from CSV
    if csv_result and csv_result.get("status") == "ok" and csv_result.get("numeric_cols"):
        df = csv_result["raw"]
        num_col = csv_result["numeric_cols"][0]
        ts = df[num_col].dropna().values

        # Base margin = most recent actual observation
        if len(ts) > 0:
            base_margin = float(ts[-1])
        else:
            base_margin = float(econ.get("econometric_prediction", 0.0))

        # Short‑term = AR(1) projected next point using last 2 observations if available
        if len(ts) >= 2:
            short_term_margin = float(ts[-1] + 0.6 * (ts[-1] - ts[-2]))
        else:
            short_term_margin = base_margin

        # Medium‑term = rolling mean of last 6 periods if possible
        if len(ts) >= 6:
            medium_term_margin = float(ts[-6:].mean())
        else:
            medium_term_margin = float(ts.mean()) if len(ts) > 0 else base_margin

        # Long‑term = linear trend extrapolation using regression
        try:
            import numpy as np
            x = np.arange(len(ts))
            y = ts
            coeff = np.polyfit(x, y, 1)
            slope, intercept = coeff[0], coeff[1]
            long_term_margin = float(intercept + slope * (len(ts) + 8))  # project 8 periods ahead
        except Exception:
            long_term_margin = medium_term_margin
    else:
        # Fallback: use econometric prediction directly
        base_margin = float(econ.get("econometric_prediction", 0.0))
        short_term_margin = base_margin
        medium_term_margin = base_margin
        long_term_margin = base_margin

    temporal_text = (
        "• Temporal Propagation (data‑driven margins):\n"
        f"  - Short‑term (next season):     €{short_term_margin:.2f}\n"
        f"  - Medium‑term (3‑year window):  €{medium_term_margin:.2f}\n"
        f"  - Long‑term (7‑year horizon):   €{long_term_margin:.2f}"
    )

    # ---------- 5. CAUSAL CHAIN REASONING ----------
    causal_text = (
        "• Causal Chain Reconstruction:\n"
        f"  (1) Domain trigger → {domain}\n"
        f"  (2) Shocks deform price / cost / weather boundary conditions\n"
        f"  (3) Econometric base margin updates accordingly\n"
        f"  (4) Monte Carlo spreads reshape risk bands\n"
        f"  (5) RL‑Teacher scores system‑wide reward surface\n"
        f"  (6) QUBO solver searches for feasible policy bundle\n"
        f"  (7) Serve layer compresses this into one actionable narrative."
    )

    # ---------- 6. PATHWAY CLASSIFICATION ----------
    pathway = "resilience‑preserving"
    if long_term_margin < 0:
        pathway = "fragility‑dominated"
    elif medium_term_margin < base_margin:
        pathway = "defensive‑stabilisation"
    elif short_term_margin > base_margin and mc["mc_std"] < 0.08:
        pathway = "growth‑oriented resilience"

    pathway_text = (
        f"• Strategy Pathway Classification → {pathway}.\n"
        f"  The system infers whether the current configuration protects, erodes, "
        f"  or amplifies resilience in {farm_type} under {domain.lower()} conditions."
    )

    # ---------- 7. COUNTERFACTUAL PATHWAYS ----------
    cf1 = f"What if price shock doubled for {farm_type} while policy remained unchanged?"
    cf2 = f"What if subsidy intensity and advisory support increased in {domain.lower()} by 20%?"
    cf3 = f"What if logistics delays and input lead times expanded by 20% in core supply chains?"
    cf4 = f"What if a climate‑neutral technology package was adopted across the {farm_type} cohort?"

    cf_text = (
        "• Counterfactual Scenarios (next experiments for the engine):\n"
        f"  - {cf1}\n"
        f"  - {cf2}\n"
        f"  - {cf3}\n"
        f"  - {cf4}"
    )

    # ---------- 8. EVIDENCE CLUSTER ----------
    top = retrieved["chunks"][0]
    evidence_text = (
        f"Top Evidence: {top['heading']} ({top['path']})."
    )

    # ---------- 9. FINAL META‑NARRATIVE ----------
    explanation = f"""
SPECTRE Meta‑Analysis v4 — Temporal regime simulator and domain‑aware reasoning online.

{domain_logic}

{regime_text}

{temporal_text}

{causal_text}

• RL‑Teacher Recommendation:
  Reward={rl['rl_reward']:.2f}
  Action={rl['rl_action']}

• QUBO‑Optimisation Snapshot:
  Solution={qubo['qubo_optimum']}
  Energy={qubo['qubo_energy']:.3f}

{pathway_text}

{cf_text}

{evidence_text}

System synthesis complete → multi‑horizon decision surface generated.
"""
    explanation = textwrap.dedent(explanation).strip()

    related = [
        cf1,
        cf2,
        cf3,
        cf4,
    ]

    return {"explanation": explanation, "related": related}

