"""KPI summary cards rendered as Streamlit metric columns."""

from __future__ import annotations
import streamlit as st
import pandas as pd


def render_kpi_cards(
    df: pd.DataFrame,
    avg_score: float,
    team_label: str,
):
    """Render Overall Score (left, tall) + 2×3 KPI grid (right).

    [Overall Score]  [Volume] [FRT]  [AHT]
    [  (spans 2)  ]  [CPH]   [ASAT] [QA]
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
        ("Volume", "", ",.0f"),
        ("FRT", " min", ".2f"),
        ("AHT", " min", ".2f"),
    ]
    row2_kpis = [
        ("CPH", "/hr", ".2f"),
        ("ASAT", "/5", ".2f"),
        ("QA", "", ".0%"),
    ]

    col_score, col_kpis = st.columns([1, 3])

    with col_score:
        st.markdown(
            f"""<div style="
                background: {bg};
                border: 2px solid {color}66;
                border-radius: 12px;
                padding: 1.5rem 1rem;
                text-align: center;
                min-height: 185px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.5rem;
                            text-transform: uppercase; letter-spacing: 0.05em;">
                    Overall Score
                </div>
                <div style="font-size: 3.2rem; font-weight: 800; color: {color};
                            line-height: 1;">
                    {pct:.1f}%
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.4rem;">
                    {team_label}
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    with col_kpis:
        r1 = st.columns(3)
        for col, (kpi, suffix, fmt) in zip(r1, row1_kpis):
            val = df[kpi].sum() if kpi == "Volume" else df[kpi].mean()
            val = val if not df.empty else 0
            display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
            col.metric(label=kpi, value=display)

        r2 = st.columns(3)
        for col, (kpi, suffix, fmt) in zip(r2, row2_kpis):
            val = df[kpi].mean() if not df.empty else 0
            display = f"{val:{fmt}}{suffix}" if val is not None else "N/A"
            col.metric(label=kpi, value=display)
