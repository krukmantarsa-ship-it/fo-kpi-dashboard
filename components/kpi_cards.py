"""KPI summary cards rendered as Streamlit metric columns."""

from __future__ import annotations
import streamlit as st
import pandas as pd


def render_kpi_cards(
    df: pd.DataFrame,
    avg_score: float,
    team_label: str,
):
    """Render Overall Score + KPI cards in a 2-row grid.

    Row 1: [Overall Score] [FRT] [AHT] [Volume]
    Row 2:                 [ASAT] [QA]  [CPH]
    """
    pct = avg_score * 100

    row1_kpis = [
        ("FRT", " min", ".2f"),
        ("AHT", " min", ".2f"),
        ("Volume", "", ",.0f"),
    ]
    row2_kpis = [
        ("ASAT", "/5", ".2f"),
        ("QA", "", ".0%"),
        ("CPH", "/hr", ".2f"),
    ]

    # Row 1: Overall Score + FRT + AHT + Volume
    cols1 = st.columns(4)
    with cols1[0]:
        st.metric(label=f"{team_label} Overall Score", value=f"{pct:.1f}%")

    for col, (kpi, suffix, fmt) in zip(cols1[1:], row1_kpis):
        val = df[kpi].sum() if kpi == "Volume" else df[kpi].mean()
        val = val if not df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)

    # Row 2: (spacer) + ASAT + QA + CPH
    cols2 = st.columns(4)
    for col, (kpi, suffix, fmt) in zip(cols2[1:], row2_kpis):
        val = df[kpi].mean() if not df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)
