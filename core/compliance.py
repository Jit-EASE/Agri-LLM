# core/compliance.py


def eu_ai_act_scanner(prepared: dict, retrieved: dict, econ: dict, qubo: dict) -> dict:
    issues = []
    if not prepared["raw"]:
        issues.append("Missing user intent transparency.")
    if len(retrieved.get("chunks", [])) == 0:
        issues.append("No document provenance available.")
    if econ.get("summary", "") == "Econometric model unavailable.":
        issues.append("Missing econometric model traceability.")
    if qubo.get("qubo_energy", 0) == 0.0:
        issues.append("QUBO energy zero — optimisation unverifiable.")

    compliance_score = 100 - (len(issues) * 15)
    return {"ai_act_score": max(0, compliance_score), "ai_act_issues": issues}
