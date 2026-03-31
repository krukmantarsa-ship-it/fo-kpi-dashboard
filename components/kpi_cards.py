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

    Row 1: [Overall Score (tall, colored)] [FRT] [AHT] [Volume]
    Row 2:                                 [ASAT] [QA]  [CPH]
    """
    pct = avg_score * 100
    if pct >= 70:
        color = "#22c55e"
        bg = "linear-gradient(135deg, #22c55e22, #16a34a11)"
    elif pct >= 50:
        color = "#eab308"
        bg = "linear-gradient(135deg, #eab30822, #ca8a0411)"
    else:
        color = "#ef4444"
        bg = "linear-gradient(135deg, #ef444422, #dc262611)"

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

    # Row 1: Overall Score (spans 2 rows visually) + FRT + AHT + Volume
    cols1 = st.columns(4)
    with cols1[0]:
        st.markdown(
            f"""<div style="
                background: {bg};
                border: 2px solid {color}66;
                border-radius: 12px;
                padding: 1.2rem 1rem;
                text-align: center;
                min-height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.5rem;
                            text-transform: uppercase; letter-spacing: 0.05em;">
                    {team_label} Overall Score
                </div>
                <div style="font-size: 3rem; font-weight: 800; color: {color};
                            line-height: 1;">
                    {pct:.1f}%
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    for col, (kpi, suffix, fmt) in zip(cols1[1:], row1_kpis):
        val = df[kpi].sum() if kpi == "Volume" else df[kpi].mean()
        val = val if not df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)

    # Row 2: (spacer under score card) + ASAT + QA + CPH
    cols2 = st.columns(4)
    for col, (kpi, suffix, fmt) in zip(cols2[1:], row2_kpis):
        val = df[kpi].mean() if not df.empty else 0
        display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
        col.metric(label=kpi, value=display)
