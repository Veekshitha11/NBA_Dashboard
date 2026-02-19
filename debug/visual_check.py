import streamlit as st
import pandas as pd

st.set_page_config(page_title="Statistella – Team Analytics Check", layout="wide")

st.title("🏀 Team Analytics – Visual Sanity Check")
st.caption("This app is only for verifying analytics outputs. Final UI will be built later.")

# ----------------------------
# Load data
# ----------------------------
team_season = pd.read_csv("team_analytics/outputs/tables/team_season_summary.csv")
home_away = pd.read_csv("team_analytics/outputs/tables/home_away_summary.csv")
conference = pd.read_csv("team_analytics/outputs/tables/conference_summary.csv")
rankings = pd.read_csv("team_analytics/outputs/tables/team_rankings.csv")

# ----------------------------
# Sidebar filters
# ----------------------------
st.sidebar.header("Filters")
season = st.sidebar.selectbox("Select Season", sorted(team_season["season"].unique()))
team = st.sidebar.selectbox("Select Team", sorted(team_season["team"].unique()))

# ----------------------------
# PAGE 1: League Overview
# ----------------------------
st.header("📊 League Overview")

league_trend = team_season.groupby("season")["avg_points"].mean().reset_index()
st.line_chart(league_trend.set_index("season"))

st.markdown(
    "**Insight:** League-wide scoring trends help understand how the NBA game pace has evolved over time."
)

# ----------------------------
# PAGE 2: Team Performance
# ----------------------------
st.header("🏠 Team Performance")

team_data = team_season[(team_season["season"] == season) & (team_season["team"] == team)]
st.metric("Win Percentage", f"{team_data['win_pct'].values[0]*100:.1f}%")
st.metric("Avg Points Scored", f"{team_data['avg_points'].values[0]:.1f}")

home_away_team = home_away[home_away["team"] == team]
st.bar_chart(home_away_team.set_index("home_away")[["win_rate"]])

st.markdown(
    "**Insight:** Home vs Away comparison highlights how location affects team performance."
)

# # ----------------------------
# # PAGE 3: Conference Comparison
# # ----------------------------
# st.header("🌍 Conference Comparison")

# conf_plot = conference[conference["season"] == season]
# st.bar_chart(conf_plot.set_index("conference")["avg_points"])

# st.markdown(
#     "**Insight:** Comparing conferences reveals differences in scoring style and competitiveness."
# )
st.header("🌍 Conference Comparison")

conf_plot = conference[conference["season"] == season]

st.subheader("Average Points Scored (East vs West)")

# Show numbers FIRST so users understand scale
st.dataframe(conf_plot[["conference", "avg_points"]])

# Clear horizontal bar chart
st.bar_chart(
    conf_plot.set_index("conference")[["avg_points"]],
    horizontal=True
)

st.subheader("Win Rate (East vs West)")

st.dataframe(conf_plot[["conference", "win_rate"]])

st.bar_chart(
    conf_plot.set_index("conference")[["win_rate"]],
    horizontal=True
)

st.markdown(
    "**What this shows:** A direct comparison between Eastern and Western Conferences.\n\n"
    "**Why it matters:** Even small differences reflect long-term differences in play style and competitiveness."
)

# ----------------------------
# PAGE 4: Consistency Ranking
# ----------------------------
st.header("📉 Team Consistency")

top_consistent = rankings.head(10)
st.dataframe(top_consistent)

st.markdown(
    "**Insight:** Teams with lower scoring variability tend to perform more reliably across games."
)

# ----------------------------
# Insights text
# ----------------------------
st.header("📝 Auto-Generated Insights")

with open("outputs/insights/team_insights.txt") as f:
    st.text(f.read())
