# orchestrator.py
from typing import Optional, Dict, Any

from core.nlu import prepare_query
from core.retrieval import rag_retrieve
from core.signals import compute_signals
from core.econometrics import econometric_module
from core.shocks import shock_forecast_module
from core.qubo_engine import qubo_policy_optimizer, quantum_annealing_module
from core.monte_carlo import monte_carlo_module
from core.rl_teacher import rl_teacher_optimize
from core.secondary_agent import secondary_reasoning_agent
from core.compliance import eu_ai_act_scanner
from core.extra_metrics import extra_metrics_graph
from core.serve_layer import serve_answer


def run_policy_pipeline(
    query: str,
    domain: str,
    csv_result: Optional[dict] = None,
) -> Dict[str, Any]:
    """
    Master orchestrator: Prepare → Retrieve → Signals → Models → Serve.
    Designed to be UI-agnostic (Dash / Streamlit / API can all call this).
    """

    csv_result = csv_result or {"status": "no_csv", "columns": []}

    prepared = prepare_query(query or "", domain or "Climate")
    retrieved = rag_retrieve(prepared)
    signals = compute_signals(prepared, retrieved)

    shocks = shock_forecast_module()
    qa = quantum_annealing_module()

    econ = econometric_module(prepared, csv_result)
    mc = monte_carlo_module(csv_result)
    qubo = qubo_policy_optimizer(prepared)
    rl = rl_teacher_optimize(prepared, signals, econ, mc)

    serve = serve_answer(
        prepared, retrieved, signals, econ, qubo, domain,
        shocks=shocks, mc=mc, rl=rl, csv_result=csv_result
    )
    alt_agent_text = secondary_reasoning_agent(prepared, signals, econ, shocks)
    ai_act = eu_ai_act_scanner(prepared, retrieved, econ, qubo)
    extra_fig = extra_metrics_graph(signals, mc, rl)

    return {
        "prepared": prepared,
        "retrieved": retrieved,
        "signals": signals,
        "econ": econ,
        "mc": mc,
        "qubo": qubo,
        "rl": rl,
        "shocks": shocks,
        "qa": qa,
        "serve": serve,
        "alt_agent_text": alt_agent_text,
        "ai_act": ai_act,
        "extra_metrics_fig": extra_fig,
    }
