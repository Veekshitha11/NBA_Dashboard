import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="NBA Analytics Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create tabs for Player and Team analytics
tab1, tab2 = st.tabs(["👤 Player Analytics", "👥 Team Analytics"])

# ============================================================================
# PLAYER ANALYTICS TAB
# ============================================================================
with tab1:
    # Load player data
    BASE = os.path.dirname(os.path.abspath(__file__))
    PLAYER_TABLES = os.path.join(BASE, "..", "player_analytics", "outputs", "tables")
    
    def load_player_csv(name):
        path = os.path.join(PLAYER_TABLES, name)
        if not os.path.exists(path):
            return None
        return pd.read_csv(path)
    
    def extract_season(game_id):
        """GAME_ID → season. Example: 22200477 → 2022."""
        try:
            return 2000 + int(str(game_id)[1:3])
        except:
            return None
    
    # Load player data
    season_df = load_player_csv("player_season_summary.csv")
    eff_df = load_player_csv("player_efficiency.csv")
    cons_df = load_player_csv("player_consistency.csv")
    pred_df = load_player_csv("player_predictions.csv")
    raw_df = load_player_csv("preprocessed_player_data.csv")
    
    if season_df is not None:
        # Add season column to dataframes that have game_id but no season
        if eff_df is not None and "season" not in eff_df.columns and "game_id" in eff_df.columns:
            eff_df["season"] = eff_df["game_id"].apply(extract_season)
        
        if pred_df is not None and "season" not in pred_df.columns and "game_id" in pred_df.columns:
            pred_df["season"] = pred_df["game_id"].apply(extract_season)
        
        # Compute games played from raw data
        if raw_df is not None:
            raw_df["season"] = raw_df["game_id"].apply(extract_season)
            if "player_name" in raw_df.columns:
                raw_df["player_name"] = raw_df["player_name"].str.strip()
            
            gp = (
                raw_df.groupby(["season", "player_name"])
                      .size()
                      .reset_index(name="games_played")
            )
            
            season_df = season_df.merge(gp, on=["season", "player_name"], how="left")
            season_df["games_played"] = season_df["games_played"].fillna(0).astype(int)
        else:
            season_df["games_played"] = 0
        
        # Filters for player (in main area)
        col_filter1, col_filter2 = st.columns(2)
        players = sorted(season_df["player_name"].unique())
        seasons = sorted(season_df["season"].unique())
        
        with col_filter1:
            player = st.selectbox("Select Player", players, key="player_select")
        with col_filter2:
            season = st.selectbox("Select Season", seasons, key="player_season")
        
        # Filter selected
        p_data = season_df[(season_df["player_name"] == player) & 
                          (season_df["season"] == season)]
        
        if not p_data.empty:
            st.title("👤 Player Analytics Dashboard")
            st.caption("Explore player performance, efficiency, consistency, and predictions.")
            
            # Player Overview
            st.header("🧍 Player Overview")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Average Points", f"{p_data['avg_pts'].values[0]:.1f}")
            col2.metric("Average Rebounds", f"{p_data['avg_reb'].values[0]:.1f}")
            col3.metric("Average Assists", f"{p_data['avg_ast'].values[0]:.1f}")
            col4.metric("Games Played", int(p_data["games_played"].values[0]) if pd.notna(p_data["games_played"].values[0]) else 0)
            
            # Player Performance Trends Over Seasons
            st.header("📈 Performance Trends")
            player_all_seasons = season_df[season_df["player_name"] == player].sort_values("season")
            if not player_all_seasons.empty and len(player_all_seasons) > 1:
                trend_data = player_all_seasons[["season", "avg_pts", "avg_reb", "avg_ast"]].set_index("season")
                st.line_chart(trend_data)
                st.markdown(
                    "**Insight:** Track how this player's performance has evolved across different seasons."
                )
            else:
                st.info("Multiple seasons of data needed to show trends.")
            
            # Efficiency Section with Visualizations
            st.header("⚡ Efficiency Metrics")
            if eff_df is not None:
                if "season" in eff_df.columns:
                    eff_p = eff_df[(eff_df["player_name"] == player) & (eff_df["season"] == season)]
                    eff_all = eff_df[eff_df["player_name"] == player].sort_values("season")
                else:
                    eff_p = eff_df[eff_df["player_name"] == player]
                    eff_all = eff_p
                
                if not eff_p.empty:
                    # Show efficiency metrics as bar chart
                    if "avg_eff" in eff_p.columns or "avg_eff_per_min" in eff_p.columns:
                        eff_cols = []
                        if "avg_eff" in eff_p.columns:
                            eff_cols.append("avg_eff")
                        if "avg_eff_per_min" in eff_p.columns:
                            eff_cols.append("avg_eff_per_min")
                        if "avg_pts" in eff_p.columns:
                            eff_cols.append("avg_pts")
                        if "avg_reb" in eff_p.columns:
                            eff_cols.append("avg_reb")
                        if "avg_ast" in eff_p.columns:
                            eff_cols.append("avg_ast")
                        
                        if eff_cols:
                            # Take first row only (efficiency is aggregated per player/season)
                            eff_row = eff_p[eff_cols].iloc[0:1]
                            eff_chart_data = eff_row.T
                            eff_chart_data.columns = ["Value"]
                            st.bar_chart(eff_chart_data)
                    
                    # Show dataframe
                    cols_to_show = ["player_name", "pts", "reb", "ast", "ts_percent", "efg_percent", "pts_per_min"]
                    if "season" in eff_p.columns:
                        cols_to_show.insert(1, "season")
                    display_cols = [c for c in cols_to_show if c in eff_p.columns]
                    st.dataframe(eff_p[display_cols].head(20), use_container_width=True)
                else:
                    st.info("No efficiency metrics available for this player/season.")
            
            # Consistency Section with Visualization
            st.header("📉 Consistency")
            if cons_df is not None:
                c = cons_df[cons_df["player_name"] == player]
                if not c.empty:
                    # Show consistency metrics as bar chart if available
                    if "pts_std" in c.columns or "stability_index" in c.columns:
                        cons_cols = []
                        if "avg_pts" in c.columns:
                            cons_cols.append("avg_pts")
                        if "pts_std" in c.columns:
                            cons_cols.append("pts_std")
                        if "stability_index" in c.columns:
                            cons_cols.append("stability_index")
                        
                        if cons_cols:
                            # Take first row only (consistency is per player, not per season)
                            cons_row = c[cons_cols].iloc[0:1]
                            cons_chart_data = cons_row.T
                            cons_chart_data.columns = ["Value"]
                            st.bar_chart(cons_chart_data)
                    
                    display_df = c.drop(columns=["season"], errors="ignore")
                    st.dataframe(display_df, use_container_width=True)
                    st.markdown(
                        "**Insight:** Lower standard deviation indicates more consistent performance across games."
                    )
            else:
                st.warning("Consistency data not loaded.")
            
            # Predictions Section with Visualization
            st.header("🎯 Predictions (Expected Points)")
            if pred_df is not None:
                if "season" in pred_df.columns:
                    pred_p = pred_df[(pred_df["player_name"] == player) & (pred_df["season"] == season)]
                else:
                    pred_p = pred_df[pred_df["player_name"] == player]
                
                if not pred_p.empty:
                    # Show predictions comparison chart
                    pred_cols = []
                    if "pts" in pred_p.columns:
                        pred_cols.append("pts")
                    if "predicted_pts" in pred_p.columns:
                        pred_cols.append("predicted_pts")
                    if "pts_last" in pred_p.columns:
                        pred_cols.append("pts_last")
                    if "pts_last3" in pred_p.columns:
                        pred_cols.append("pts_last3")
                    if "pts_last5" in pred_p.columns:
                        pred_cols.append("pts_last5")
                    
                    if len(pred_cols) > 1 and len(pred_p) > 1:
                        # Create chart with proper index
                        if "game_id" in pred_p.columns:
                            pred_chart_data = pred_p[pred_cols + ["game_id"]].set_index("game_id")
                        else:
                            pred_chart_data = pred_p[pred_cols].reset_index(drop=True)
                        st.line_chart(pred_chart_data.head(50))
                    
                    cols_to_show = ["player_name", "pts", "predicted_pts", "pts_last", "pts_last3", "pts_last5"]
                    if "season" in pred_p.columns:
                        cols_to_show.insert(1, "season")
                    display_cols = [c for c in cols_to_show if c in pred_p.columns]
                    st.dataframe(pred_p[display_cols].head(20), use_container_width=True)
        else:
            st.error("No data found for the selected player/season.")
    else:
        st.error("Player data not available.")

# ============================================================================
# TEAM ANALYTICS TAB
# ============================================================================
with tab2:
    # Load team data
    BASE = os.path.dirname(os.path.abspath(__file__))
    TEAM_TABLES = os.path.join(BASE, "..", "team_analytics", "outputs", "tables")
    
    def load_team_csv(name):
        path = os.path.join(TEAM_TABLES, name)
        if not os.path.exists(path):
            return None
        return pd.read_csv(path)
    
    # Load team data
    season_df = load_team_csv("team_season_summary.csv")
    rankings_df = load_team_csv("team_rankings.csv")
    conference_df = load_team_csv("conference_summary.csv")
    home_away_df = load_team_csv("home_away_summary.csv")
    feature_imp_df = load_team_csv("feature_importance.csv")
    
    if season_df is not None:
        # Filters for team (in main area)
        col_filter1, col_filter2 = st.columns(2)
        teams = sorted(season_df["team"].unique())
        seasons = sorted(season_df["season"].unique())
        
        with col_filter1:
            team = st.selectbox("Select Team", teams, key="team_select")
        with col_filter2:
            season = st.selectbox("Select Season", seasons, key="team_season")
        
        # Filter selected
        team_data = season_df[(season_df["team"] == team) & (season_df["season"] == season)]
        
        if not team_data.empty:
            st.title("👥 Team Analytics Dashboard")
            st.caption("Explore team performance, rankings, conference comparisons, and key insights.")
            
            # League Overview (like visual_check.py)
            st.header("📊 League Overview")
            league_trend = season_df.groupby("season")["avg_points"].mean().reset_index()
            st.line_chart(league_trend.set_index("season"))
            st.markdown(
                "**Insight:** League-wide scoring trends help understand how the NBA game pace has evolved over time."
            )
            
            # Team Overview
            st.header("🏠 Team Performance")
            col1, col2 = st.columns(2)
            avg_points = team_data["avg_points"].values[0]
            win_pct = team_data["win_pct"].values[0]
            
            col1.metric("Win Percentage", f"{win_pct*100:.1f}%")
            col2.metric("Avg Points Scored", f"{avg_points:.1f}")
            
            # Home/Away Performance with Bar Chart (like visual_check.py)
            if home_away_df is not None:
                team_home_away = home_away_df[home_away_df["team"] == team]
                if not team_home_away.empty:
                    st.bar_chart(team_home_away.set_index("home_away")[["win_rate"]])
                    st.markdown(
                        "**Insight:** Home vs Away comparison highlights how location affects team performance."
                    )
            
            # Conference Comparison (exactly like visual_check.py)
            st.header("🌍 Conference Comparison")
            if conference_df is not None:
                conf_plot = conference_df[conference_df["season"] == season]
                if not conf_plot.empty:
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
            
            # Team Consistency Ranking (like visual_check.py)
            st.header("📉 Team Consistency")
            if rankings_df is not None:
                top_consistent = rankings_df.sort_values("std_dev", ascending=True).head(10).reset_index(drop=True)
                st.dataframe(top_consistent, use_container_width=True)
                st.markdown(
                    "**Insight:** Teams with lower scoring variability tend to perform more reliably across games."
                )
        else:
            st.error("No data found for the selected team/season.")
    else:
        st.error("Team data not available.")
