# core/nlu.py
import hashlib
from datetime import datetime


def stable_score(seed: str, scale: int = 100) -> float:
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    val = int(h[:8], 16)
    return (val % (scale * 100)) / 100.0


def prepare_query(raw_query: str, domain: str) -> dict:
    q = (raw_query or "").strip()
    now = datetime.utcnow().strftime("%Y-%m-%d")

    domain_tags = {
        "Dairy": ["milk price", "co-op", "grass", "processor"],
        "Climate": ["emissions", "resilience", "weather shock"],
        "Policy": ["CAP", "subsidy", "regulation"],
        "Supply Chain": ["logistics", "ports", "inventory"],
    }
    extra = ", ".join(domain_tags.get(domain, []))

    enriched = f"{q} [domain={domain}; tags={extra}; time={now}]"

    synonyms = [
        ("price crash", "negative price shock"),
        ("AI", "agentic decision system"),
        ("farmer", "primary producer"),
        ("subsidy", "support scheme"),
    ]
    synonym_notes = []
    normalized = enriched
    for src, tgt in synonyms:
        if src.lower() in normalized.lower():
            normalized = normalized.replace(src, tgt)
            synonym_notes.append(f"{src} → {tgt}")

    return {
        "raw": q,
        "enriched": enriched,
        "normalized": normalized,
        "synonym_notes": synonym_notes,
    }
