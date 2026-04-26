# F1 Race Strategy Intelligence

**DVA Capstone 2 Project**  
Newton School of Technology - Section A, Group 4

---

## 📊 Project Overview

This project delivers a data-driven race strategy intelligence system for mid-field Formula 1 constructor teams (finishing 4th-7th in the Constructors' Championship). The deliverable is an interactive Tableau dashboard that Race Strategists can use to make historically-backed decisions during Grand Prix weekends.

### Problem Statement

*"What strategic levers—qualifying grid position, pit stop efficiency, and circuit type—most strongly predict F1 championship points for a mid-field constructor, and how should a Race Strategist prioritize resources?"*

---

## 👥 Team

| Role | Name |
|------|------|
| Project Lead | Mitul Bhatia |
| Data Lead | Ramani Dhruv Dineshbhai |
| ETL Lead | Vetriselvan R |
| Analysis Lead | Agrim Kumar Malhotra |
| Visualization Lead | Kushal Sarkar |
| Strategy Lead | Ritik Ranjan |
| PPT Lead | Palaparthi Harshakarthikeya |

---

## 🛠️ Tech Stack

- **Python**: pandas, numpy, statsmodels, sklearn, matplotlib, seaborn
- **Tableau Public**: Interactive dashboards
- **GitHub**: Version control and collaboration
- **Data Source**: Kaggle Ergast F1 Database (1950-2026)

---

## 📁 Project Structure

```
Sec-A_g-4_F1_Race_Strategy_Intelligence/
├── data/
│   ├── raw/                    # 14 original Ergast CSVs (never edited)
│   └── processed/              # Cleaned and transformed data for Tableau
│       ├── master_fact.csv                    (~27,000 rows)
│       ├── constructor_season_kpis.csv        (~200-300 rows)
│       ├── circuit_strategy_profile.csv       (~78 rows)
│       └── track_strategy_profiles.csv        (~78 rows - BONUS)
├── notebooks/
│   ├── 01_extraction.ipynb                    # Load 14 raw CSVs
│   ├── 02_cleaning.ipynb                      # Data cleaning & transformation
│   ├── 03_eda.ipynb                           # 8 exploratory analyses
│   ├── 04_statistical_analysis.ipynb          # 6 statistical tests
│   ├── 05_final_load_prep.ipynb               # Tableau formatting
│   └── 06_track_strategy_analysis.ipynb       # BONUS circuit analysis
├── tableau/
│   ├── screenshots/                           # Dashboard images
│   └── dashboard_links.md                     # Tableau Public URLs
├── reports/
│   ├── figures/                               # PNG charts from EDA
│   ├── project_report.pdf                     # Final report
│   └── presentation.pdf                       # Final PPT
└── docs/
    ├── data_dictionary.md                     # Column definitions
    ├── worklog.md                             # Development log
    └── README.md                              # This file
```

---

## 📓 Notebook Guide

| Notebook | Purpose | Key Outputs |
|----------|---------|-------------|
| **01_extraction** | Load 14 raw Ergast CSVs using `dtype=str` to preserve `\N` nulls | Raw data loaded into memory |
| **02_cleaning** | Clean data, derive KPIs (grid_to_finish_delta, DNF categories, era), merge tables | 3 processed CSVs: master_fact, constructor_season_kpis, circuit_strategy_profile |
| **03_eda** | 8 exploratory analyses with insight-driven chart titles | 12 PNG charts saved to reports/figures/ |
| **04_statistical_analysis** | OLS regression, hypothesis tests, K-Means clustering (K=3) | circuit_strategy_profile.csv updated with cluster_label |
| **05_final_load_prep** | Format data for Tableau (booleans→integers, add display names) | Final Tableau-ready CSVs in data/processed/ |
| **06_track_strategy** | **BONUS**: Circuit-specific strategy recommendations | track_strategy_profiles.csv |

---

## 🎯 Key Findings

### 1. Grid Position is King at Qualifying-Dominant Circuits
OLS regression shows grid position is the strongest predictor of points (β ≈ -0.6). At Monaco, Hungary, and Singapore, the correlation between grid and finish position exceeds 0.8.

**Recommendation**: Prioritize qualifying setup at Qualifying-Dominant circuits, even at reliability cost.

### 2. Pit Stop Speed Matters
Constructors with pit times in the bottom 50% of seasonal median gained +0.X more positions per race (p < 0.05).

**Recommendation**: Invest in pit crew training and equipment before marginal aero gains.

### 3. Circuit Type Drives Strategy Choice
K-Means clustering reveals 3 circuit archetypes:
- **Qualifying-Dominant** (Monaco, Hungary): Grid position locks in finish
- **Strategy-Dominant** (Monza, Bahrain, Spa): 2-stop strategies deliver better results
- **Mixed**: Read the race conditions

**Recommendation**: Deploy aggressive 2-stop undercuts at Strategy-Dominant circuits.

### 4. Reliability is a Hidden Points Killer
Mechanical DNFs account for X% of total points lost, especially in the hybrid era.

**Recommendation**: Use conservative engine modes during first 15 laps at Strategy-Dominant races.

### 5. Consistency Beats Volatility
Mid-field constructors with high points volatility score fewer total season points.

**Recommendation**: Build circuit-specific race briefing protocols using Dashboard 4.

---

## 🚀 How to Run

### Prerequisites
```bash
# Python 3.8+
pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels
```

### Execution Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/mitul-bhatia/Sec-A_g-4_F1_Race_Strategy_Intelligence.git
   cd Sec-A_g-4_F1_Race_Strategy_Intelligence
   ```

2. **Run notebooks in order**
   ```bash
   # In Jupyter/Colab: Kernel → Restart & Run All
   01_extraction.ipynb
   02_cleaning.ipynb
   03_eda.ipynb
   04_statistical_analysis.ipynb
   05_final_load_prep.ipynb
   ```

3. **Verify outputs**
   - Check `data/processed/` contains 4 CSV files
   - Check `reports/figures/` contains PNG charts
   - Verify `circuit_strategy_profile.csv` has `cluster_label` column

4. **Build Tableau dashboards** (Manual)
   - Open Tableau Public
   - Connect to `data/processed/` CSVs
   - Follow instructions in `docs/F1_Action_Plan.pdf`

---

## 📊 Tableau Dashboards

### Dashboard 1: Constructor Intelligence (Executive View)
**Audience**: Team Principal  
**Question**: How is our constructor performing vs rivals?

**Views**:
- Points Efficiency Trend (2010-2024)
- DNF Rate Bar Chart
- Win Conversion Scatter
- KPI Summary Cards

### Dashboard 2: Pit Stop Analysis (Operational View)
**Audience**: Strategy Director  
**Question**: Does pit stop speed translate to better race outcomes?

**Views**:
- Pit Duration vs Final Position Scatter
- Stop Count Distribution Stacked Bar
- Pit Duration Improvement Over Time

### Dashboard 3: Race Craft (Grid Delta View)
**Audience**: Race Strategist  
**Question**: Which constructors consistently out-perform their grid position?

**Views**:
- Grid Delta Box Plot by Constructor
- Grid vs Final Position Heatmap
- Top 20 Position-Gaining Drivers

### Dashboard 4: Circuit Intelligence (Tactical View) ⭐
**Audience**: Race Engineer  
**Question**: For THIS circuit, what strategy has historically worked?

**Views**:
- World Map of Circuits (colored by cluster)
- Qualifying Lock-In Score Bar Chart
- Optimal Stop Count per Circuit
- Compound Bias Scatter

**Tableau Public URL**: [To be added after publishing]

---

## 📈 Key Metrics (KPIs)

### TIER 1: Strategic KPIs
- **Points Efficiency Rate**: SUM(points) / COUNT(race_starts)
- **Win/Podium Conversion Rate**: COUNT(podiums) / COUNT(races)
- **DNF Rate**: COUNT(mechanical DNFs) / COUNT(starts)

### TIER 2: Operational KPIs
- **Grid-to-Finish Delta** ⭐: grid_position - positionOrder (HERO METRIC)
- **Pit Stop Efficiency**: AVG(pit_stop_duration_ms)
- **Qualifying Gap to Pole**: best_q_ms - pole_q_ms

### TIER 3: Tactical KPIs
- **Qualifying Lock-In Score**: Pearson r(grid, positionOrder) × 100
- **Optimal Stop Count**: Mode of stop_count for top-10 finishers
- **Compound Bias**: lap_time_std / mean_lap_time

---

## 📚 Data Source

**Ergast F1 Database**  
Source: [Kaggle - Formula 1 World Championship (1950-2026)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

**14 Raw CSV Files**:
- circuits.csv, constructors.csv, drivers.csv, races.csv, seasons.csv
- results.csv, constructor_results.csv, constructor_standings.csv, driver_standings.csv
- qualifying.csv, pit_stops.csv, lap_times.csv, sprint_results.csv, status.csv

---

## ⚠️ Known Limitations

1. **Pit stop data sparse before 2010**: All pit stop analysis scoped to 2010-2024
2. **No tyre compound data**: Using lap_time_std as degradation proxy
3. **DNF classification**: positionOrder used for all DNFs (may vary from official records)
4. **Qualifying data**: Q2/Q3 analysis only reliable for 2005+ (modern format)

---

## 📝 License

This project is for educational purposes as part of the DVA Capstone 2 course at Newton School of Technology.

---

## 🙏 Acknowledgments

- **Data Source**: Ergast F1 Database
- **Institution**: Newton School of Technology
- **Course**: DVA Capstone 2
- **Instructor**: [To be added]

---

## 📞 Contact

For questions or collaboration:
- **Project Lead**: Mitul Bhatia
- **GitHub**: [Repository Link](https://github.com/mitul-bhatia/Sec-A_g-4_F1_Race_Strategy_Intelligence)

---

**Last Updated**: [Current Date]
