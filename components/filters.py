"""Sidebar filter components."""

from __future__ import annotations
from datetime import date, timedelta
import streamlit as st
from data.agent_mapping import PARENT_TEAMS, TEAM_LIST


def render_filters() -> dict:
    """Render sidebar filters and return filter state."""
    st.sidebar.header("Filters")

    period = st.sidebar.selectbox(
        "Time Period",
        ["Day", "Week", "Month"],
        index=2,
        key="period",
    )

    today = date.today()
    if period == "Day":
        ref_date = st.sidebar.date_input("Date", value=today, key="ref_date")
    elif period == "Week":
        week_start = today - timedelta(days=today.weekday())
        ref_date = st.sidebar.date_input(
            "Week starting", value=week_start, key="ref_date"
        )
    else:
        ref_date = st.sidebar.date_input(
            "Month of", value=today.replace(day=1), key="ref_date"
        )

    st.sidebar.divider()

    parent_team = st.sidebar.selectbox(
        "Team Group",
        PARENT_TEAMS,
        index=0,
        key="parent_team",
    )

    if parent_team == "SME":
        sub_options = ["All SME", "SME - Veru", "SME - Adhi"]
    elif parent_team == "Retail":
        sub_options = ["Retail (FO)"]
    else:
        sub_options = ["All"] + TEAM_LIST

    team_filter = st.sidebar.selectbox(
        "Sub-team",
        sub_options,
        key="team_filter",
    )

    st.sidebar.divider()

    channel = st.sidebar.selectbox(
        "Channel",
        ["All (Chat + Email)", "Chat only", "Email only"],
        index=0,
        key="channel",
    )

    channel_map = {
        "All (Chat + Email)": "all",
        "Chat only": "chat",
        "Email only": "email",
    }

    return {
        "period": period.lower(),
        "ref_date": ref_date,
        "parent_team": parent_team,
        "team_filter": team_filter,
        "channel": channel_map[channel],
    }


def render_weight_editor(current_weights: dict[str, float]) -> dict[str, float]:
    """Render KPI weight editor in the sidebar."""
    st.sidebar.divider()
    st.sidebar.header("KPI Weights")
    st.sidebar.caption("Must sum to 100%")

    new_weights = {}
    for kpi, w in current_weights.items():
        new_weights[kpi] = st.sidebar.slider(
            kpi,
            min_value=0,
            max_value=100,
            value=int(w * 100),
            step=5,
            key=f"weight_{kpi}",
        ) / 100.0

    total = sum(new_weights.values())
    if abs(total - 1.0) > 0.01:
        st.sidebar.warning(f"Weights sum to {total:.0%} — should be 100%")
    else:
        st.sidebar.success(f"Weights: {total:.0%} ✓")

    return new_weights
