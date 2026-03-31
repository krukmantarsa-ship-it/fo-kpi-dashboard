"""KPI summary cards rendered as Streamlit metric columns."""

from __future__ import annotations
import streamlit as st
import pandas as pd


def render_kpi_cards(df: pd.DataFrame, title: str = "Team KPI Summary"):
    """Render KPI summary cards in a 2-row × 3-column grid."""
    st.subheader(title)

    row1 = [
        ("FRT",    " min",  ".2f"),
        ("AHT",    " min",  ".2f"),
        ("Volume", "",      ",.0f"),
    ]
    row2 = [
        ("CPH",    "/hr",   ".2f"),
        ("ASAT",   "/5",    ".2f"),
        ("QA",     "",      ".0%"),
    ]

    for row_kpis in [row1, row2]:
        cols = st.columns(3)
        for col, (kpi, suffix, fmt) in zip(cols, row_kpis):
            val = df[kpi].mean() if kpi != "Volume" else df[kpi].sum()
            display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
            col.metric(label=kpi, value=display)


def render_score_card(avg_score: float, team_label: str):
    """Render the overall weighted score card."""
    pct = avg_score * 100
    color = "#22c55e" if pct >= 70 else "#eab308" if pct >= 50 else "#ef4444"
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}11);
            border: 1px solid {color}44;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        ">
            <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.25rem;">
                {team_label} Overall Score
            </div>
            <div style="font-size: 2.5rem; font-weight: 700; color: {color};">
                {pct:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
