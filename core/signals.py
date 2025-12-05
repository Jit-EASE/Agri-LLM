# core/signals.py
from .nlu import stable_score


def compute_signals(prepared: dict, retrieved: dict) -> dict:
    key = prepared["normalized"]
    s = {}
    s["Base Ranking"] = stable_score("BASE::" + key)
    s["Gecko Similarity"] = stable_score("GECKO::" + key)
    s["Jetstream Relevance"] = stable_score("JET::" + key)
    s["BM25 Keyword Match"] = stable_score("BM25::" + key)
    s["Tier1 Popularity"] = stable_score("P1::" + key)
    s["Tier2 PCTR"] = stable_score("P2::" + key)
    s["Tier3 Personalized PCTR"] = stable_score("P3::" + key)
    s["Freshness"] = stable_score("FRESH::" + key)

    boost = 0.0
    for term, val in {
        "resilience": 10.0,
        "sustainability": 8.0,
        "women": 6.0,
        "mental health": 7.0,
        "bioeconomy": 6.0,
    }.items():
        if term in key.lower():
            boost += val

    s["Boost/Bury Adjustment"] = boost

    s["Overall Score"] = (
        0.2 * s["Base Ranking"]
        + 0.15 * s["Gecko Similarity"]
        + 0.15 * s["Jetstream Relevance"]
        + 0.10 * s["BM25 Keyword Match"]
        + 0.15 * s["Tier2 PCTR"]
        + 0.10 * s["Tier3 Personalized PCTR"]
        + 0.10 * s["Freshness"]
        + 0.05 * s["Boost/Bury Adjustment"]
    )
    return s
