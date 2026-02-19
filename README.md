# 🏀 NBA Analytics Dashboard

A comprehensive data analytics project for NBA team and player performance analysis. This project includes data processing scripts and an interactive Streamlit dashboard for exploring player and team analytics.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Generating Analytics Data](#-generating-analytics-data)
- [Running the Dashboard](#-running-the-dashboard)
- [Project Structure](#project-structure)
- [Data Files](#data-files)
- [Dashboard Features](#dashboard-features)
- [Regenerating Analytics Data](#-regenerating-analytics-data)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

- **Player Analytics**: Performance metrics, efficiency analysis, consistency tracking, and predictions
- **Team Analytics**: Season summaries, rankings, conference comparisons, home/away splits, and key performance indicators
- **Interactive Dashboard**: User-friendly Streamlit interface with filtering and data visualization
- **Comprehensive Data Analysis**: Pre-processed data with multiple analytics dimensions

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- **Git** (optional, for cloning the repository)

## 📦 Installation

### Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project directory:

```bash
cd path/to/Statistella_NBA
```

### Step 2: Create Virtual Environment

Create a virtual environment to isolate project dependencies:

**On Windows:**
```bash
python -m venv venv
```

**On macOS/Linux:**
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your command prompt, indicating the virtual environment is active.

### Step 4: Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install the following packages:
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- streamlit
- plotly

### Step 5: Verify Installation

Verify that Streamlit is installed correctly:

```bash
streamlit --version
```

## 📊 Generating Analytics Data

**⚠️ Important**: The output data files are **not included** in this repository (due to file size). You **must** generate them before running the dashboard.

All scripts can be run from the base directory (`Statistella_NBA`). Make sure your virtual environment is activated.

### Step 1: Generate Player Analytics Outputs

Run the following scripts in order to generate all player analytics data:

```bash
# From the base directory (Statistella_NBA)
python player_analytics/src/player_preprocessing.py
python player_analytics/src/player_performance.py
python player_analytics/src/player_efficiency.py
python player_analytics/src/player_consistency.py
python player_analytics/src/player_prediction_model.py
python player_analytics/src/player_clustering.py
python player_analytics/src/player_insight_generator.py
```

This will create all necessary CSV files in `player_analytics/outputs/tables/` and insights in `player_analytics/outputs/insights/`.

### Step 2: Generate Team Analytics Outputs

Run the following scripts to generate all team analytics data:

```bash
# From the base directory (Statistella_NBA)
python team_analytics/src/team_performance_analysis.py
python team_analytics/src/team_consistency.py
python team_analytics/src/conference_analysis.py
python team_analytics/src/home_away_analysis.py
python team_analytics/src/outcome_modeling.py
python team_analytics/src/feature_importance.py
python team_analytics/src/insight_generator.py
```

This will create all necessary CSV files in `team_analytics/outputs/tables/` and insights in `team_analytics/outputs/insights/`.

### Quick Generate Script (Optional)

You can also create a simple batch/shell script to run all scripts at once. For Windows (PowerShell), you can run:

```powershell
# Generate all player analytics
python player_analytics/src/player_preprocessing.py
python player_analytics/src/player_performance.py
python player_analytics/src/player_efficiency.py
python player_analytics/src/player_consistency.py
python player_analytics/src/player_prediction_model.py
python player_analytics/src/player_clustering.py
python player_analytics/src/player_insight_generator.py

# Generate all team analytics
python team_analytics/src/team_performance_analysis.py
python team_analytics/src/team_consistency.py
python team_analytics/src/conference_analysis.py
python team_analytics/src/home_away_analysis.py
python team_analytics/src/outcome_modeling.py
python team_analytics/src/feature_importance.py
python team_analytics/src/insight_generator.py
```

## 🚀 Running the Dashboard

**⚠️ Important**: Make sure you have generated all analytics data (see [Generating Analytics Data](#-generating-analytics-data)) before running the dashboard.

Once all output files have been generated, run the Streamlit dashboard:

```bash
streamlit run dashboards/main_dashboard.py
```

The dashboard will start and automatically open in your default web browser at `http://localhost:8501`.

If it doesn't open automatically, you can manually navigate to:
- **Local URL**: http://localhost:8501
- **Network URL**: Will be displayed in the terminal (e.g., http://192.168.x.x:8501)

### Stopping the Dashboard

To stop the dashboard, press `Ctrl + C` in the terminal where Streamlit is running.

## 📁 Project Structure

```
Statistella_NBA/
│
├── dashboards/
│   └── main_dashboard.py          # Main Streamlit dashboard (Player & Team analytics)
│
├── player_analytics/
│   ├── data/
│   │   └── games_details.csv      # Raw player game data
│   ├── src/                        # Player analytics scripts
│   │   ├── player_loader.py
│   │   ├── player_preprocessing.py
│   │   ├── player_performance.py
│   │   ├── player_efficiency.py
│   │   ├── player_consistency.py
│   │   ├── player_prediction_model.py
│   │   └── player_clustering.py
│   └── outputs/
│       ├── tables/                 # Processed data tables
│       └── insights/               # Generated insights
│
├── team_analytics/
│   ├── data/                       # Team data files
│   │   ├── games_details.csv
│   │   ├── processed_nba_data.csv
│   │   └── team_conference_map.csv
│   ├── src/                        # Team analytics scripts
│   │   ├── data_loader.py
│   │   ├── team_performance_analysis.py
│   │   ├── team_consistency.py
│   │   ├── conference_analysis.py
│   │   ├── home_away_analysis.py
│   │   ├── outcome_modeling.py
│   │   └── feature_importance.py
│   └── outputs/
│       ├── tables/                 # Processed data tables
│       └── insights/               # Generated insights
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 📊 Data Files

The dashboard uses pre-processed CSV files that are generated by running the analytics scripts. These files are located in:

- **Player Analytics**: `player_analytics/outputs/tables/`
  - `player_season_summary.csv` - Season averages per player
  - `player_efficiency.csv` - Efficiency metrics
  - `player_consistency.csv` - Consistency analysis
  - `player_predictions.csv` - Performance predictions
  - `player_clusters.csv` - Player role clustering
  - `preprocessed_player_data.csv` - Preprocessed raw data

- **Team Analytics**: `team_analytics/outputs/tables/`
  - `team_season_summary.csv` - Team season summaries
  - `team_rankings.csv` - Team rankings and consistency
  - `conference_summary.csv` - Conference comparisons
  - `home_away_summary.csv` - Home/away performance
  - `feature_importance.csv` - Key performance indicators

**Note**: These files must be generated by running the analytics scripts (see [Generating Analytics Data](#-generating-analytics-data)) as they are not included in the repository.

## 🎯 Dashboard Features

### Player Analytics Tab

- **Player Overview**: Average points, rebounds, assists, and games played
- **Efficiency Metrics**: TS%, eFG%, points per minute, and more
- **Consistency Analysis**: Standard deviations and stability indices
- **Performance Predictions**: Expected points based on recent performance

### Team Analytics Tab

- **Team Overview**: Points scored/allowed, point differential, win percentage
- **Team Rankings**: Consistency metrics and team rankings
- **Conference Comparison**: East vs West performance comparisons
- **Home/Away Performance**: Home and away game splits
- **Key Performance Indicators**: Feature importance for team success

## 🔄 Regenerating Analytics Data

If you need to regenerate the analytics data files (e.g., after updating source data), you can run the scripts again. All scripts can be run from the base directory:

### Player Analytics Scripts

```bash
# From the base directory (Statistella_NBA)
python player_analytics/src/player_preprocessing.py
python player_analytics/src/player_performance.py
python player_analytics/src/player_efficiency.py
python player_analytics/src/player_consistency.py
python player_analytics/src/player_prediction_model.py
python player_analytics/src/player_clustering.py
python player_analytics/src/player_insight_generator.py
```

### Team Analytics Scripts

```bash
# From the base directory (Statistella_NBA)
python team_analytics/src/team_performance_analysis.py
python team_analytics/src/team_consistency.py
python team_analytics/src/conference_analysis.py
python team_analytics/src/home_away_analysis.py
python team_analytics/src/outcome_modeling.py
python team_analytics/src/feature_importance.py
python team_analytics/src/insight_generator.py
```

**Note**: All scripts are designed to be run from the base directory (`Statistella_NBA`), and outputs will be saved to the respective `outputs/` folders automatically.

## 🐛 Troubleshooting

### Issue: `streamlit: command not found`

**Solution**: Make sure your virtual environment is activated and Streamlit is installed:
```bash
pip install streamlit
```

### Issue: `ModuleNotFoundError`

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Dashboard shows "Missing file" errors

**Solution**: This means the output data files haven't been generated yet. You must run all the analytics scripts first to generate the required CSV files (see [Generating Analytics Data](#-generating-analytics-data)). Make sure to run all scripts for both player and team analytics.

### Issue: Port already in use

**Solution**: Streamlit will try to use port 8501. If it's occupied, specify a different port:
```bash
streamlit run dashboards/main_dashboard.py --server.port 8502
```

## 📝 Notes

- The virtual environment should be activated whenever you work with this project
- **Output data files are NOT included** in the repository (due to file size constraints). You must generate them by running the analytics scripts before using the dashboard
- All scripts can be run from the base directory (`Statistella_NBA`) - no need to navigate into subdirectories
- The dashboard requires all output files to be generated first (see [Generating Analytics Data](#-generating-analytics-data))
- Output files are automatically saved to the respective `outputs/tables/` and `outputs/insights/` directories

## 🤝 Contributing

Feel free to explore the codebase, modify analytics, or add new features to the dashboard!

## 📄 License

This project is for educational and analytical purposes.

---

**Happy Analyzing! 🏀📊**

