# core/secondary_agent.py


def secondary_reasoning_agent(prepared: dict, signals: dict, econ: dict, shocks: dict) -> str:
    return (
        f"Alt-Agent Interpretation:\n"
        f"- Shocks suggest price movement of {shocks['price_shock']:.2%}.\n"
        f"- Econometric baseline margin: €{econ['econometric_prediction']:.2f}.\n"
        f"- Jetstream relevance peak: {signals['Jetstream Relevance']:.1f}.\n"
        f"Conclusion: monitor volatility clusters; diversify policy portfolio."
    )
