"""KPI summary cards rendered as Streamlit metric columns."""

from __future__ import annotations
import streamlit as st
import pandas as pd


def render_kpi_cards(
    df: pd.DataFrame,
    avg_score: float,
    team_label: str,
):
    """Render Overall Score + KPI cards in a 2-row × 4-column grid.

    Row 1: [Overall Score] [FRT] [AHT] [Volume]
    Row 2: [CPH]           [ASAT] [QA]
    """
    pct = avg_score * 100
    color = "#22c55e" if pct >= 70 else "#eab308" if pct >= 50 else "#ef4444"

    row1_kpis = [
        ("FRT", " min", ".2f"),
        ("AHT", " min", ".2f"),
        ("Volume", "", ",.0f"),
    ]
    row2_kpis = [
        ("CPH", "/hr", ".2f"),
        ("ASAT", "/5", ".2f"),
        ("QA", "", ".0%"),
    ]

    # Row 1: Overall Score + FRT + AHT + Volume
    cols1 = st.columns(4)
    with cols1[0]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {color}22, {color}11);
                border: 1px solid {color}44;
                border-radius: 12px;
                padding: 1rem 1.2rem;
                text-align: center;
            ">
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.15rem;">
                    {team_label} Overall Score
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: {color};">
                    {pct:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for col, (kpi, suffix, fmt) in zip(cols1[1:], row1_kpis):
        val = df[kpi].sum() if kpi == "Volume" else df[kpi].mean()
        val = val if not df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)

    # Row 2: CPH + ASAT + QA
    cols2 = st.columns([1, 1, 1, 1])
    for col, (kpi, suffix, fmt) in zip(cols2, row2_kpis):
        val = df[kpi].mean() if not df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)
