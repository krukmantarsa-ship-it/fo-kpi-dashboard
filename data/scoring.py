"""
Front Office scoring engine.

Max score = 100%.
Each KPI has a configurable weight. Raw values are normalised to a 0–1 scale
using target/threshold bands, then multiplied by their weight.

Lower-is-better KPIs (FRT, AHT) use inverse scaling.
Higher-is-better KPIs (CPH, ASAT, QA) use direct scaling.
"""

from __future__ import annotations
import pandas as pd

DEFAULT_WEIGHTS: dict[str, float] = {
    "FRT":    0.10,
    "AHT":    0.10,
    "CPH":    0.30,
    "ASAT":   0.30,
    "QA":     0.20,
}

# Normalisation bands: (min_val, target_val)
# For lower-is-better: score=1.0 at min_val, score=0.0 at 2×target
# For higher-is-better: score=1.0 at target_val, score=0.0 at min_val
DEFAULT_TARGETS: dict[str, dict] = {
    "FRT":    {"direction": "lower",  "best": 0.5,  "worst": 10.0},
    "AHT":   {"direction": "lower",  "best": 5.0,  "worst": 25.0},
    "CPH":   {"direction": "higher", "best": 10.0, "worst": 2.0},
    "ASAT":  {"direction": "higher", "best": 5.0,  "worst": 1.0},
    "QA":    {"direction": "higher", "best": 1.0,  "worst": 0.0},
}


def normalise_kpi(value: float | None, kpi: str,
                  targets: dict | None = None) -> float:
    """Normalise a raw KPI value to 0–1 scale."""
    if value is None:
        return 0.0
    t = (targets or DEFAULT_TARGETS).get(kpi, {})
    direction = t.get("direction", "higher")
    best = t.get("best", 1.0)
    worst = t.get("worst", 0.0)

    if direction == "lower":
        if value <= best:
            return 1.0
        if value >= worst:
            return 0.0
        return 1.0 - (value - best) / (worst - best)
    else:
        if value >= best:
            return 1.0
        if value <= worst:
            return 0.0
        return (value - worst) / (best - worst)


def compute_agent_score(
    kpis: dict[str, float | None],
    weights: dict[str, float] | None = None,
    targets: dict | None = None,
) -> dict:
    """
    Compute final score for one agent.

    Returns dict with:
      - normalised: {kpi: 0–1}
      - weighted:   {kpi: contribution to final}
      - total:      final score (0–1, display as %)
    """
    w = weights or DEFAULT_WEIGHTS
    t = targets or DEFAULT_TARGETS

    normalised = {}
    weighted = {}
    for kpi, weight in w.items():
        raw = kpis.get(kpi)
        n = normalise_kpi(raw, kpi, t)
        normalised[kpi] = round(n, 4)
        weighted[kpi] = round(n * weight, 4)

    total = sum(weighted.values())
    return {
        "normalised": normalised,
        "weighted": weighted,
        "total": round(total, 4),
    }


def score_all_agents(
    df: pd.DataFrame,
    kpi_cols: list[str],
    weights: dict[str, float] | None = None,
    targets: dict | None = None,
) -> pd.DataFrame:
    """
    Score every agent in the DataFrame.

    Expects df to have columns matching kpi_cols.
    Adds: score_total, rank, and per-KPI normalised/weighted columns.
    """
    w = weights or DEFAULT_WEIGHTS
    t = targets or DEFAULT_TARGETS

    records = []
    for _, row in df.iterrows():
        kpis = {k: row.get(k) for k in kpi_cols}
        result = compute_agent_score(kpis, w, t)
        rec = {"score_total": result["total"]}
        for kpi in kpi_cols:
            rec[f"{kpi}_norm"] = result["normalised"].get(kpi, 0)
            rec[f"{kpi}_weighted"] = result["weighted"].get(kpi, 0)
        records.append(rec)

    score_df = pd.DataFrame(records, index=df.index)
    out = pd.concat([df, score_df], axis=1)
    out["rank"] = out["score_total"].rank(ascending=False, method="min").astype(int)
    return out.sort_values("rank")
