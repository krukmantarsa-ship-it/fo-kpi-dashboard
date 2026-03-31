"""
Mock data generator for Front Office KPI Dashboard.

Values are calibrated from actual ANALYTICS_DB.EMART_CC.CHAT_TOUCH patterns
and 'SME Team Sheet_Feb_Trial Calculator 2.xlsx'.

Realistic ranges observed:
  FRT:    0.5 – 8 min  (agent first response in touch)
  AHT:    5 – 20 min   (agent handling duration)
  Volume: 200 – 800+   (touches per month per agent)
  CPH:    4 – 10       (closed chats+emails per hour)
  ASAT:   2.5 – 4.5    (1–5 scale)
  QA:     0.45 – 0.95  (0–1 scale from coaching file)
"""

from __future__ import annotations
import random
import pandas as pd
from datetime import date, timedelta
from data.agent_mapping import get_all_agents


# Seeded for reproducibility but agent-specific offsets give variety
_BASE_SEED = 42


def _agent_seed(name: str) -> int:
    return sum(ord(c) for c in name) + _BASE_SEED


def _generate_agent_kpis(agent: dict, period: str,
                         ref_date: date) -> dict:
    """Generate realistic KPI values for one agent in one period."""
    rng = random.Random(_agent_seed(agent["display"]) + ref_date.toordinal())

    team = agent["team"]
    is_sme = "SME" in team

    frt = round(rng.uniform(0.5, 3.5) if is_sme else rng.uniform(0.8, 5.0), 2)
    aht = round(rng.uniform(6.0, 16.0) if is_sme else rng.uniform(7.0, 18.0), 2)

    if period == "day":
        volume = rng.randint(15, 55)
    elif period == "week":
        volume = rng.randint(80, 280)
    else:
        volume = rng.randint(350, 900)

    cph = round(rng.uniform(4.5, 9.5) if is_sme else rng.uniform(3.5, 8.5), 2)
    asat = round(rng.uniform(2.8, 4.8), 2)
    qa = round(rng.uniform(0.50, 0.95), 2)

    return {
        "FRT": frt,
        "AHT": aht,
        "Volume": volume,
        "CPH": cph,
        "ASAT": asat,
        "QA": qa,
    }


def _generate_daily_series(agent: dict, start: date, end: date) -> list[dict]:
    """Generate daily KPI rows for chart data."""
    rows = []
    current = start
    while current <= end:
        rng = random.Random(
            _agent_seed(agent["display"]) + current.toordinal()
        )
        is_sme = "SME" in agent["team"]
        rows.append({
            "date": current.isoformat(),
            "agent": agent["display"],
            "team": agent["team"],
            "FRT": round(rng.uniform(0.4, 4.0), 2),
            "AHT": round(rng.uniform(5.0, 20.0), 2),
            "Volume": rng.randint(12, 60),
            "CPH": round(
                rng.uniform(4.0, 10.0) if is_sme else rng.uniform(3.0, 9.0),
                2),
            "ASAT": round(rng.uniform(2.5, 5.0), 2),
        })
        current += timedelta(days=1)
    return rows


def generate_agent_data(
    period: str = "month",
    ref_date: date | None = None,
    channel: str = "all",
) -> pd.DataFrame:
    """
    Build the full agent KPI DataFrame.

    Args:
        period: 'day', 'week', or 'month'
        ref_date: reference date for the period
        channel: 'chat', 'email', or 'all' (scales volume)
    """
    if ref_date is None:
        ref_date = date.today()

    agents = get_all_agents()
    rows = []
    for agent in agents:
        kpis = _generate_agent_kpis(agent, period, ref_date)

        if channel == "chat":
            kpis["Volume"] = int(kpis["Volume"] * 0.75)
            kpis["CPH"] = round(kpis["CPH"] * 0.75, 2)
        elif channel == "email":
            kpis["Volume"] = int(kpis["Volume"] * 0.25)
            kpis["CPH"] = round(kpis["CPH"] * 0.25, 2)

        rows.append({
            "agent": agent["display"],
            "sf_name": agent["sf_name"],
            "team": agent["team"],
            "parent_team": agent["parent_team"],
            "training_focus": "",
            "verticalization": "",
            "qa_topics": "",
            "asat_topics": "",
            **kpis,
        })

    return pd.DataFrame(rows)


def generate_daily_chart_data(
    start: date, end: date
) -> pd.DataFrame:
    """Generate daily KPI data for all agents for charting."""
    agents = get_all_agents()
    all_rows = []
    for agent in agents:
        all_rows.extend(_generate_daily_series(agent, start, end))
    return pd.DataFrame(all_rows)
