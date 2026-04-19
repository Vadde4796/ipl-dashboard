"""IPL Dashboard — Streamlit app."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.data_loader import load_matches, load_deliveries
from src.analysis import (
    team_win_stats, top_batsmen, top_bowlers,
    season_summary, head_to_head, toss_impact,
)

st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #0f3460;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #e94560; }
    .metric-label { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
    .section-header {
        font-size: 1.3rem; font-weight: 600;
        color: #e94560; margin: 1rem 0 0.5rem;
        border-bottom: 2px solid #e94560; padding-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading IPL data…")
def get_data():
    matches = load_matches()
    deliveries = load_deliveries()
    return matches, deliveries


matches, deliveries = get_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/IPL_2022_Logo.svg/640px-IPL_2022_Logo.svg.png",
    use_container_width=True,
)
st.sidebar.title("IPL Analytics")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "🏆 Teams", "🏏 Batsmen", "🎳 Bowlers", "📅 Seasons"],
)

seasons = sorted(matches["season"].unique())
selected_seasons = st.sidebar.multiselect(
    "Filter Seasons", seasons, default=seasons, key="seasons_filter"
)

if selected_seasons:
    matches_f = matches[matches["season"].isin(selected_seasons)]
    deliveries_f = deliveries[deliveries["match_id"].isin(matches_f["id"])]
else:
    matches_f, deliveries_f = matches, deliveries

# ─────────────────────────────────────────────────────────────────────────────
# 1. OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.title("🏏 IPL Dashboard — Overview")

    total_matches = len(matches_f)
    total_teams = len(pd.concat([matches_f["team1"], matches_f["team2"]]).unique())
    total_runs = deliveries_f["total_runs"].sum()
    total_wickets = deliveries_f["player_dismissed"].notna().sum()

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [
        (c1, total_matches, "Total Matches"),
        (c2, total_teams, "Teams"),
        (c3, f"{total_runs:,}", "Total Runs"),
        (c4, total_wickets, "Total Wickets"),
    ]:
        col.markdown(
            f'<div class="metric-card"><div class="metric-value">{val}</div>'
            f'<div class="metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<p class="section-header">Champions by Season</p>', unsafe_allow_html=True)
        ss = season_summary(matches_f)
        champ_counts = ss["champion"].value_counts().reset_index()
        champ_counts.columns = ["team", "titles"]
        fig = px.bar(
            champ_counts, x="titles", y="team", orientation="h",
            color="titles", color_continuous_scale="Reds",
            labels={"titles": "IPL Titles", "team": ""},
        )
        fig.update_layout(showlegend=False, height=380, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-header">Matches per Season</p>', unsafe_allow_html=True)
        fig2 = px.line(
            ss, x="season", y="matches",
            markers=True, color_discrete_sequence=["#e94560"],
            labels={"matches": "Matches", "season": "Season"},
        )
        fig2.update_layout(height=380, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Toss Decision Impact</p>', unsafe_allow_html=True)
    toss = toss_impact(matches_f)
    toss["win_rate_after_toss_win"] = (toss["win_rate_after_toss_win"] * 100).round(1)
    fig3 = px.bar(
        toss, x="toss_decision", y="win_rate_after_toss_win",
        text="win_rate_after_toss_win",
        color="toss_decision", color_discrete_sequence=["#e94560", "#0f3460"],
        labels={"win_rate_after_toss_win": "Win % After Toss Win", "toss_decision": "Toss Decision"},
    )
    fig3.update_traces(texttemplate="%{text}%", textposition="outside")
    fig3.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 2. TEAMS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🏆 Teams":
    st.title("🏆 Team Analysis")

    stats = team_win_stats(matches_f)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-header">Wins by Team</p>', unsafe_allow_html=True)
        fig = px.bar(
            stats, x="won", y="team", orientation="h",
            color="win_pct", color_continuous_scale="RdYlGn",
            labels={"won": "Wins", "team": "", "win_pct": "Win %"},
            hover_data=["played", "lost", "win_pct"],
        )
        fig.update_layout(height=460, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-header">Win Percentage</p>', unsafe_allow_html=True)
        fig2 = px.pie(
            stats.head(8), values="won", names="team",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.4,
        )
        fig2.update_layout(height=460, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Head-to-Head</p>', unsafe_allow_html=True)
    all_teams = sorted(pd.concat([matches_f["team1"], matches_f["team2"]]).unique())
    h2h_col1, h2h_col2 = st.columns(2)
    team_a = h2h_col1.selectbox("Team A", all_teams, index=0)
    team_b = h2h_col2.selectbox("Team B", all_teams, index=1)
    if team_a != team_b:
        h2h = head_to_head(matches_f, team_a, team_b)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Matches", h2h["total"])
        m2.metric(f"{team_a} Wins", h2h[team_a])
        m3.metric(f"{team_b} Wins", h2h[team_b])

    st.markdown('<p class="section-header">Full Stats Table</p>', unsafe_allow_html=True)
    st.dataframe(stats, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. BATSMEN
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🏏 Batsmen":
    st.title("🏏 Batting Analysis")

    bat = top_batsmen(deliveries_f)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-header">Top Run Scorers</p>', unsafe_allow_html=True)
        fig = px.bar(
            bat, x="runs", y="batsman", orientation="h",
            color="strike_rate", color_continuous_scale="Blues",
            labels={"runs": "Runs", "batsman": "", "strike_rate": "SR"},
            hover_data=["balls", "fifties", "hundreds"],
        )
        fig.update_layout(height=480, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-header">Runs vs Strike Rate</p>', unsafe_allow_html=True)
        fig2 = px.scatter(
            bat, x="runs", y="strike_rate", text="batsman",
            size="balls", color="hundreds",
            color_continuous_scale="Reds",
            labels={"runs": "Total Runs", "strike_rate": "Strike Rate", "hundreds": "100s"},
        )
        fig2.update_traces(textposition="top center")
        fig2.update_layout(height=480, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Batting Stats Table</p>', unsafe_allow_html=True)
    st.dataframe(bat.rename(columns={
        "batsman": "Batsman", "runs": "Runs", "balls": "Balls",
        "strike_rate": "SR", "fifties": "50s", "hundreds": "100s",
    }), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. BOWLERS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🎳 Bowlers":
    st.title("🎳 Bowling Analysis")

    bowl = top_bowlers(deliveries_f)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-header">Top Wicket Takers</p>', unsafe_allow_html=True)
        fig = px.bar(
            bowl, x="wickets", y="bowler", orientation="h",
            color="economy", color_continuous_scale="RdYlGn_r",
            labels={"wickets": "Wickets", "bowler": "", "economy": "Economy"},
            hover_data=["overs", "runs_conceded"],
        )
        fig.update_layout(height=480, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-header">Wickets vs Economy</p>', unsafe_allow_html=True)
        fig2 = px.scatter(
            bowl, x="wickets", y="economy", text="bowler",
            size="overs", color="wickets",
            color_continuous_scale="Blues",
            labels={"wickets": "Wickets", "economy": "Economy Rate"},
        )
        fig2.update_traces(textposition="top center")
        fig2.update_layout(height=480, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Bowling Stats Table</p>', unsafe_allow_html=True)
    st.dataframe(bowl.rename(columns={
        "bowler": "Bowler", "wickets": "Wkts", "runs_conceded": "Runs",
        "overs": "Overs", "economy": "Economy",
    }), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 5. SEASONS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📅 Seasons":
    st.title("📅 Season-by-Season Analysis")

    ss = season_summary(matches_f)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-header">Matches per Season</p>', unsafe_allow_html=True)
        fig = px.area(
            ss, x="season", y="matches",
            color_discrete_sequence=["#e94560"],
            labels={"matches": "Matches", "season": "Season"},
        )
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<p class="section-header">Avg Win Margin (Runs) per Season</p>', unsafe_allow_html=True)
        fig2 = px.bar(
            ss, x="season", y="avg_win_by_runs",
            color="avg_win_by_runs", color_continuous_scale="Blues",
            labels={"avg_win_by_runs": "Avg Margin (Runs)", "season": "Season"},
        )
        fig2.update_layout(height=320, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Season Champions</p>', unsafe_allow_html=True)
    champ_df = ss[["season", "champion", "matches"]].rename(
        columns={"season": "Season", "champion": "Champion", "matches": "Matches Played"}
    )
    st.dataframe(champ_df, use_container_width=True, hide_index=True)

    st.markdown('<p class="section-header">Deliveries Distribution by Over</p>', unsafe_allow_html=True)
    over_runs = (deliveries_f.groupby("over")["total_runs"]
                 .mean().reset_index(name="avg_runs"))
    fig3 = px.bar(
        over_runs, x="over", y="avg_runs",
        color="avg_runs", color_continuous_scale="Reds",
        labels={"avg_runs": "Avg Runs/Ball", "over": "Over"},
    )
    fig3.update_layout(height=320, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig3, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption(f"Data: IPL 2008–2024 | {len(matches_f):,} matches")
