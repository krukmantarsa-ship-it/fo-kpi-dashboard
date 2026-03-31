"""Agent ranking table and detail panel."""

from __future__ import annotations
import streamlit as st
import pandas as pd


def _score_color(score: float) -> str:
    if score >= 0.70:
        return "#22c55e"
    if score >= 0.50:
        return "#eab308"
    return "#ef4444"


def render_ranking_table(df: pd.DataFrame):
    """Render the ranked agent table with KPI values."""
    display_df = df[[
        "rank", "agent", "team",
        "FRT", "AHT", "Volume", "CPH", "ASAT", "QA",
        "score_total",
    ]].copy()

    display_df["Score %"] = (display_df["score_total"] * 100).round(1)
    display_df["QA"] = (display_df["QA"] * 100).round(0).astype(int)
    display_df = display_df.rename(columns={
        "rank": "Rank",
        "agent": "Agent",
        "team": "Team",
        "QA": "QA %",
    })
    display_df = display_df.drop(columns=["score_total"])

    st.dataframe(
        display_df,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Agent": st.column_config.TextColumn("Agent", width="medium"),
            "Team": st.column_config.TextColumn("Team", width="medium"),
            "FRT": st.column_config.NumberColumn("FRT", format="%.2f"),
            "AHT": st.column_config.NumberColumn("AHT", format="%.2f"),
            "Volume": st.column_config.NumberColumn("Volume", format="%d"),
            "CPH": st.column_config.NumberColumn("CPH", format="%.2f"),
            "ASAT": st.column_config.NumberColumn("ASAT", format="%.2f"),
            "QA %": st.column_config.NumberColumn("QA %", format="%d%%"),
            "Score %": st.column_config.ProgressColumn(
                "Score %", min_value=0, max_value=100, format="%.1f%%"
            ),
        },
        hide_index=True,
        height=min(800, 40 + len(display_df) * 35),
    )


def render_agent_detail(df: pd.DataFrame, selected_agent: str):
    """Render editable agent detail panel with QA/ASAT improvement topics."""
    row = df[df["agent"] == selected_agent]
    if row.empty:
        st.info("Select an agent from the table above.")
        return

    r = row.iloc[0]
    score_pct = r["score_total"] * 100
    color = _score_color(r["score_total"])

    st.markdown(f"### {r['agent']}")
    st.markdown(
        f"**Team:** {r['team']}  |  **Rank:** #{int(r['rank'])}  |  "
        f"**Score:** <span style='color:{color}'>{score_pct:.1f}%</span>",
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### KPI Values")
        for kpi in ["FRT", "AHT", "Volume", "CPH", "ASAT", "QA"]:
            val = r[kpi]
            norm = r.get(f"{kpi}_norm", 0) * 100
            weighted = r.get(f"{kpi}_weighted", 0) * 100
            if kpi == "QA":
                st.markdown(
                    f"**{kpi}:** {val:.0%}  "
                    f"<span style='color:#94a3b8; font-size:0.8rem'>"
                    f"(norm: {norm:.0f}% → contrib: {weighted:.1f}%)</span>",
                    unsafe_allow_html=True,
                )
            elif kpi == "Volume":
                st.markdown(
                    f"**{kpi}:** {val:,.0f}  "
                    f"<span style='color:#94a3b8; font-size:0.8rem'>"
                    f"(informational)</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"**{kpi}:** {val:.2f}  "
                    f"<span style='color:#94a3b8; font-size:0.8rem'>"
                    f"(norm: {norm:.0f}% → contrib: {weighted:.1f}%)</span>",
                    unsafe_allow_html=True,
                )

    with col2:
        st.markdown("#### Manual Fields")
        training = st.text_area(
            "Training Focus",
            value=r.get("training_focus", ""),
            key=f"training_{selected_agent}",
            height=80,
        )
        vert = st.text_input(
            "Verticalization",
            value=r.get("verticalization", ""),
            key=f"vert_{selected_agent}",
        )

    st.divider()

    qa_col, asat_col = st.columns(2)
    with qa_col:
        st.markdown("#### QA Improvement Topics")
        st.caption("Areas to improve Quality Assurance score")
        qa_topics = st.text_area(
            "QA topics",
            value=r.get("qa_topics", ""),
            key=f"qa_topics_{selected_agent}",
            height=120,
            placeholder="e.g.\n- Greeting & closing script adherence\n- Accurate issue categorisation\n- Follow-up completeness",
            label_visibility="collapsed",
        )

    with asat_col:
        st.markdown("#### ASAT Improvement Topics")
        st.caption("Areas to improve Agent Satisfaction rating")
        asat_topics = st.text_area(
            "ASAT topics",
            value=r.get("asat_topics", ""),
            key=f"asat_topics_{selected_agent}",
            height=120,
            placeholder="e.g.\n- Empathy & tone of voice\n- Faster resolution communication\n- Proactive follow-up",
            label_visibility="collapsed",
        )

    return {
        "training_focus": training,
        "verticalization": vert,
        "qa_topics": qa_topics,
        "asat_topics": asat_topics,
    }
