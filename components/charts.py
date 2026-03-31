"""Plotly chart components for the FO KPI Dashboard."""

from __future__ import annotations
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

CHART_TEMPLATE = "plotly_dark"
COLOR_PALETTE = px.colors.qualitative.Set2


def _base_layout(fig: go.Figure, height: int = 380) -> go.Figure:
    fig.update_layout(
        template=CHART_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=40, r=20, t=40, b=40),
        font=dict(size=12),
        legend=dict(orientation="h", y=-0.15),
    )
    return fig


def kpi_bar_chart(df: pd.DataFrame, kpi: str, title: str = ""):
    """Horizontal bar chart of a single KPI across agents."""
    sorted_df = df.sort_values(kpi, ascending=True)
    fig = px.bar(
        sorted_df, x=kpi, y="agent", orientation="h",
        color="team", color_discrete_sequence=COLOR_PALETTE,
        title=title or f"{kpi} by Agent",
    )
    _base_layout(fig, height=max(300, len(df) * 28))
    fig.update_layout(yaxis_title="", xaxis_title=kpi)
    st.plotly_chart(fig, width="stretch")


def score_ranking_chart(df: pd.DataFrame):
    """Horizontal bar chart of overall scores with rank labels."""
    sorted_df = df.sort_values("score_total", ascending=True).copy()
    sorted_df["score_pct"] = sorted_df["score_total"] * 100

    fig = px.bar(
        sorted_df, x="score_pct", y="agent", orientation="h",
        color="team", color_discrete_sequence=COLOR_PALETTE,
        title="Agent Ranking (Overall Score %)",
        text="score_pct",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    _base_layout(fig, height=max(350, len(df) * 28))
    fig.update_layout(
        xaxis_title="Score (%)", yaxis_title="",
        xaxis=dict(range=[0, 105]),
    )
    st.plotly_chart(fig, width="stretch")


def weighted_breakdown_chart(df: pd.DataFrame, agent_name: str):
    """Stacked bar showing weighted KPI contribution for one agent."""
    row = df[df["agent"] == agent_name]
    if row.empty:
        st.info("Select an agent to view breakdown.")
        return

    weighted_cols = [c for c in df.columns if c.endswith("_weighted")]
    kpis = [c.replace("_weighted", "") for c in weighted_cols]
    values = [float(row[c].iloc[0]) * 100 for c in weighted_cols]

    fig = go.Figure()
    for i, (kpi, val) in enumerate(zip(kpis, values)):
        fig.add_trace(go.Bar(
            name=f"{kpi} ({val:.1f}%)",
            x=[val], y=["Score"],
            orientation="h",
            text=f"{kpi}" if val >= 5 else "",
            textposition="inside",
            textfont=dict(size=11),
            marker_color=COLOR_PALETTE[i % len(COLOR_PALETTE)],
        ))

    fig.update_layout(barmode="stack", title=f"Score Breakdown: {agent_name}")
    _base_layout(fig, height=180)
    fig.update_layout(
        xaxis=dict(range=[0, 105], title="Weighted Contribution (%)"),
        yaxis_title="",
        yaxis=dict(visible=False),
        showlegend=True,
        legend=dict(
            orientation="h", y=-0.35, x=0.5, xanchor="center",
            font=dict(size=11),
        ),
        margin=dict(l=10, r=20, t=40, b=60),
    )
    st.plotly_chart(fig, width="stretch")


def team_comparison_radar(df: pd.DataFrame):
    """Radar chart comparing team averages across KPIs."""
    kpis = ["FRT", "AHT", "CPH", "ASAT", "QA"]
    norm_cols = [f"{k}_norm" for k in kpis]

    teams = df["team"].unique()
    fig = go.Figure()

    for i, team in enumerate(teams):
        team_df = df[df["team"] == team]
        vals = [team_df[c].mean() * 100 for c in norm_cols]
        vals.append(vals[0])
        cats = kpis + [kpis[0]]

        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats, name=team,
            fill="toself", opacity=0.6,
            line=dict(color=COLOR_PALETTE[i % len(COLOR_PALETTE)]),
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor="rgba(0,0,0,0)",
        ),
        title="Team Comparison (Normalised %)",
    )
    _base_layout(fig, height=420)
    st.plotly_chart(fig, width="stretch")


def daily_trend_chart(daily_df: pd.DataFrame, kpi: str,
                      agents: list[str] | None = None):
    """Line chart of daily KPI trend."""
    plot_df = daily_df.copy()
    if agents:
        plot_df = plot_df[plot_df["agent"].isin(agents)]

    agg = plot_df.groupby("date")[kpi].mean().reset_index()
    fig = px.line(
        agg, x="date", y=kpi,
        title=f"Daily {kpi} Trend (Team Average)",
        markers=True,
    )
    _base_layout(fig)
    st.plotly_chart(fig, width="stretch")
