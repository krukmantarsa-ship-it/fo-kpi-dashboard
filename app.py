"""
Front Office KPI Dashboard — Main Application.

Launch: streamlit run app.py
Route:  This serves the /front-office dashboard.
"""

from __future__ import annotations
from datetime import date, timedelta
import streamlit as st
import pandas as pd

from data.mock_data import generate_agent_data, generate_daily_chart_data
from data.scoring import score_all_agents, DEFAULT_WEIGHTS, DEFAULT_TARGETS
from data.agent_mapping import TEAM_SME_VERU, TEAM_SME_ADHI, TEAM_RETAIL
from components.filters import render_filters, render_weight_editor
from components.kpi_cards import render_score_card
from components.agent_table import render_ranking_table, render_agent_detail
from components.charts import (
    score_ranking_chart,
    weighted_breakdown_chart,
    team_comparison_radar,
    kpi_bar_chart,
    daily_trend_chart,
)

st.set_page_config(
    page_title="Front Office KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Minimal CSS overrides ─────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px 16px;
    }
    [data-testid="stMetricValue"] { font-size: 1.6rem; }
    section[data-testid="stSidebar"] > div { padding-top: 1rem; }
    .block-container { padding-top: 2rem; }
    table td, table th {
        padding: 8px 12px !important;
        border-bottom: 1px solid #334155 !important;
    }
    table tr:hover { background: #1e293b !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar filters ───────────────────────────────────────────────────
filters = render_filters()
weights = render_weight_editor(DEFAULT_WEIGHTS)


# ── Data loading ──────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(period: str, ref_date, channel: str):
    return generate_agent_data(period=period, ref_date=ref_date, channel=channel)


raw_df = load_data(filters["period"], filters["ref_date"], filters["channel"])

# Allow user to edit KPI values in session state
if "edited_kpis" not in st.session_state:
    st.session_state.edited_kpis = {}

for _, row in raw_df.iterrows():
    agent = row["agent"]
    if agent in st.session_state.edited_kpis:
        for kpi, val in st.session_state.edited_kpis[agent].items():
            raw_df.loc[raw_df["agent"] == agent, kpi] = val


# ── Filter by team ────────────────────────────────────────────────────
def apply_team_filter(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    tf = filters["team_filter"]
    pt = filters["parent_team"]

    if pt == "All" and tf == "All":
        return df
    if tf in [TEAM_SME_VERU, TEAM_SME_ADHI, TEAM_RETAIL]:
        return df[df["team"] == tf]
    if tf == "All SME":
        return df[df["parent_team"] == "SME"]
    if pt == "Retail":
        return df[df["parent_team"] == "Retail"]
    if pt == "SME":
        return df[df["parent_team"] == "SME"]
    return df


filtered_df = apply_team_filter(raw_df, filters)

# ── Scoring (Volume kept in data but excluded from weight/scoring) ────
scored_kpis = ["FRT", "AHT", "Volume", "CPH", "ASAT", "QA"]
scoring_weights = {**weights, "Volume": 0.0}
scored_df = score_all_agents(filtered_df, scored_kpis, scoring_weights, DEFAULT_TARGETS)


# ══════════════════════════════════════════════════════════════════════
# MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════

st.title("Front Office KPI Dashboard")

period_label = filters["period"].capitalize()
team_label = filters["team_filter"]
channel_label = filters["channel"].upper() if filters["channel"] != "all" else "All Channels"

st.caption(
    f"Period: **{period_label}** · Team: **{team_label}** · "
    f"Channel: **{channel_label}** · "
    f"Agents: **{len(scored_df)}** · "
    f"Data source: EMART_CC.CHAT_TOUCH (mock)"
)

# ── Row 1: KPI summary (row 1) + Overall Score (center) + KPI summary (row 2)
avg_score = scored_df["score_total"].mean() if not scored_df.empty else 0

kpi_row1 = [
    ("FRT", " min", ".2f"),
    ("AHT", " min", ".2f"),
]
kpi_row2 = [
    ("CPH", "/hr", ".2f"),
    ("ASAT", "/5", ".2f"),
]
kpi_row3 = [
    ("Volume", "", ",.0f"),
    ("QA", "", ".0%"),
]

col_left, col_center, col_right = st.columns([2, 1, 2])

with col_left:
    c1, c2 = st.columns(2)
    for col, (kpi, suffix, fmt) in zip([c1, c2], kpi_row1):
        val = scored_df[kpi].mean() if not scored_df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)
    c3, c4 = st.columns(2)
    for col, (kpi, suffix, fmt) in zip([c3, c4], kpi_row2):
        val = scored_df[kpi].mean() if not scored_df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)

with col_center:
    render_score_card(avg_score, team_label)

with col_right:
    c5, c6 = st.columns(2)
    for col, (kpi, suffix, fmt) in zip([c5, c6], kpi_row3):
        val = scored_df[kpi].sum() if kpi == "Volume" else scored_df[kpi].mean()
        val = val if not scored_df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)


# ── Row 2: Ranking table ─────────────────────────────────────────────
st.divider()
st.subheader("Agent Ranking")
render_ranking_table(scored_df)


# ── Row 3: Charts ─────────────────────────────────────────────────────
st.divider()

tab_rank, tab_radar, tab_kpi, tab_trend = st.tabs([
    "Score Ranking", "Team Comparison", "KPI Breakdown", "Daily Trend"
])

with tab_rank:
    score_ranking_chart(scored_df)

with tab_radar:
    if len(scored_df["team"].unique()) > 1:
        team_comparison_radar(scored_df)
    else:
        st.info("Select 'All' teams to see comparison radar chart.")

with tab_kpi:
    kpi_choice = st.selectbox(
        "Select KPI", scored_kpis, index=3, key="kpi_bar_select"
    )
    kpi_bar_chart(scored_df, kpi_choice)

with tab_trend:
    ref = filters["ref_date"]
    if isinstance(ref, date):
        start = ref - timedelta(days=30)
        end = ref
    else:
        start = ref - timedelta(days=30)
        end = ref

    daily_df = generate_daily_chart_data(start, end)
    agents_in_scope = scored_df["agent"].tolist()
    trend_kpi = st.selectbox(
        "Trend KPI", ["CPH", "FRT", "AHT", "ASAT"], key="trend_kpi"
    )
    daily_trend_chart(daily_df, trend_kpi, agents_in_scope)


# ── Row 4: Agent detail panel ─────────────────────────────────────────
st.divider()
st.subheader("Agent Detail")

agent_options = scored_df["agent"].tolist()
selected_agent = st.selectbox(
    "Select Agent", agent_options, key="agent_select"
)

if selected_agent:
    col_detail, col_chart = st.columns([1, 1])

    with col_detail:
        manual = render_agent_detail(scored_df, selected_agent)

    with col_chart:
        weighted_breakdown_chart(scored_df, selected_agent)

    # ── Editable KPI override ─────────────────────────────────────
    st.divider()
    st.subheader("Edit KPI Values")
    st.caption("Override computed values. Changes recalculate scores dynamically.")

    edit_cols = st.columns(6)
    edits = {}
    current = scored_df[scored_df["agent"] == selected_agent].iloc[0]

    for col, kpi in zip(edit_cols, scored_kpis):
        with col:
            default = float(current[kpi])
            if kpi == "QA":
                val = st.number_input(
                    kpi, min_value=0.0, max_value=1.0,
                    value=default, step=0.01, format="%.2f",
                    key=f"edit_{kpi}_{selected_agent}",
                )
            elif kpi == "Volume":
                val = st.number_input(
                    kpi, min_value=0, value=int(default), step=1,
                    key=f"edit_{kpi}_{selected_agent}",
                )
            elif kpi == "ASAT":
                val = st.number_input(
                    kpi, min_value=0.0, max_value=5.0,
                    value=default, step=0.1, format="%.2f",
                    key=f"edit_{kpi}_{selected_agent}",
                )
            else:
                val = st.number_input(
                    kpi, min_value=0.0,
                    value=default, step=0.1, format="%.2f",
                    key=f"edit_{kpi}_{selected_agent}",
                )
            edits[kpi] = val

    if st.button("Apply Changes", type="primary", key="apply_edits"):
        st.session_state.edited_kpis[selected_agent] = edits
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Data layer: Mock data calibrated from ANALYTICS_DB.EMART_CC.CHAT_TOUCH "
    "and REPORT_DB.CC.EXPERT_ASAT_DETAILS. "
    "QA scores sourced from Coaching Sessions file. "
    "See README for schema mapping and missing data documentation."
)
