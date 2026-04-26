# F1 Race Strategy Intelligence - Work Log

## Project Overview
DVA Capstone 2 - Section A, Group 4
Newton School of Technology

**Goal**: Create a data-driven race strategy intelligence system for mid-field F1 constructors with Tableau dashboards.

---

## Session 1: Initial Assessment and Planning

### Date: [Current Session]

#### 1. Requirements Analysis Completed
- ✅ Read complete F1 Action Plan document
- ✅ Read complete F1 Master Captain Doc
- ✅ Analyzed current notebook structure (01-06)
- ✅ Identified data outputs needed for Tableau

#### 2. Current State Assessment

**Notebooks Status:**
- `01_extraction.ipynb` - Loads 14 raw CSVs ✓
- `02_cleaning.ipynb` - Creates master_fact.csv, constructor_season_kpis.csv, circuit_strategy_profile.csv ✓
- `03_eda.ipynb` - Has 12 charts, needs restructuring to 8 sections ⚠️
- `04_statistical_analysis.ipynb` - Partially complete, needs 6 clear sections ⚠️
- `05_final_load_prep.ipynb` - Needs Tableau-specific transformations ⚠️
- `06_track_strategy_analysis.ipynb` - BONUS notebook, needs documentation ⚠️

**Data Files Required for Tableau:**
1. `master_fact.csv` (~27,000 rows) - Main fact table
2. `constructor_season_kpis.csv` (~200-300 rows) - Constructor aggregates
3. `circuit_strategy_profile.csv` (~78 rows) - Circuit analysis with cluster_label
4. `track_strategy_profiles.csv` (~78 rows) - BONUS detailed circuit data

#### 3. Key Issues Identified

**Notebook 03 (EDA):**
- Current: 12 charts with descriptive titles
- Required: Exactly 8 sections with INSIGHT-DRIVEN titles
- Example BAD: "Points by Constructor"
- Example GOOD: "McLaren and Alpine Have Highest Points Efficiency Among Mid-Field Teams Since 2018"

**Notebook 04 (Statistical Analysis):**
- Needs 6 clear sections with plain English conclusions
- Must export circuit_strategy_profile.csv with cluster_label column
- K-Means clustering (K=3) must label circuits as: Qualifying-Dominant, Strategy-Dominant, Mixed

**Notebook 05 (Final Load Prep):**
- Must convert booleans to 0/1 integers for Tableau
- Must add driver_name_display = "Surname, Forename"
- Must add constructor_short codes (MCL, RBR, FER, MER, etc.)
- Must fill grid NaN with 0 (pit lane starts)
- Must round pit stop columns to 1 decimal

#### 4. Tableau Dashboard Requirements

**4 Dashboards to Build (Manual - User will do this):**

1. **Dashboard 1: Constructor Intelligence** (Executive View)
   - Data: master_fact.csv + constructor_season_kpis.csv
   - Views: Points Efficiency Trend, DNF Rate Bar, Win Conversion Scatter, KPI Cards
   - Filters: Constructor multi-select, Year range slider

2. **Dashboard 2: Pit Stop Analysis** (Operational View)
   - Data: master_fact.csv
   - Views: Pit Duration vs Position Scatter, Stop Count Stacked Bar, Duration Improvement Over Time
   - Filters: Year range, Constructor, Circuit archetype

3. **Dashboard 3: Race Craft** (Grid Delta View)
   - Data: master_fact.csv
   - Views: Grid Delta Box Plot, Grid vs Final Position Heatmap, Top 20 Position-Gaining Drivers
   - Filters: Constructor, Year, Era

4. **Dashboard 4: Circuit Intelligence** (Tactical View - THE STAR)
   - Data: circuit_strategy_profile.csv
   - Views: World Map, Lock-In Score Bar Chart, Optimal Stop Count Bar, Compound Bias Scatter
   - Filters: Cluster dropdown

**Critical Tableau Columns Needed:**
- `cluster_label` (from K-Means in notebook 04)
- `qualifying_lock_in_score` (Pearson r × 100)
- `optimal_stop_count` (mode of stop_count for top-10 finishers)
- `lat`, `lng` (for world map)
- `is_win`, `is_dnf`, `is_podium`, `is_pole` (as 0/1 integers)
- `driver_name_display` (formatted name)
- `constructor_short` (3-4 letter codes)

#### 5. Next Steps

**Phase 1: Documentation (CURRENT)**
- ✅ Create worklog.md
- ⏳ Create README.md in /docs folder
- ⏳ Create data_dictionary.md

**Phase 2: Notebook Fixes (NEXT)**
- Fix Notebook 03: Restructure to 8 sections with insight-driven titles
- Fix Notebook 04: Add 6 clear sections, export cluster_label
- Fix Notebook 05: Add Tableau transformations
- Document Notebook 06: Add BONUS banner and section headers

**Phase 3: Validation**
- Run notebooks 01→05 in order
- Verify all 4 CSV files are created correctly
- Check that cluster_label column exists in circuit_strategy_profile.csv
- Verify boolean columns are 0/1 integers in master_fact.csv

**Phase 4: Tableau Preparation**
- User will manually build 4 dashboards in Tableau Public
- User will publish and get URL
- User will take 4 screenshots

---

## Important Notes

### The 8 Required EDA Sections (Notebook 03)
1. Points Efficiency trend per constructor (2010-2024)
2. DNF Rate by constructor and by dnf_category
3. Grid-to-Finish Delta distribution per constructor (box plot)
4. Pit Stop Efficiency: avg pit duration per constructor per year trend
5. Win/Podium Conversion Rate by constructor
6. Qualifying Gap to Pole by constructor (violin plot)
7. Correlation matrix of all numeric KPIs
8. Era comparison: key KPIs split by era column

### The 6 Required Statistical Sections (Notebook 04)
1. Analysis Scope Definition (already exists)
2. OLS Regression (points ~ grid + stop_count + avg_pit_ms)
3. Hypothesis Test (fast vs slow pit stops → grid_to_finish_delta)
4. K-Means Circuit Clustering (K=3)
5. Pearson Correlation by Cluster + Stop Count Analysis
6. Summary of Findings (5 Key Findings)

### Critical: Grid-to-Finish Delta
This is the HERO metric of the entire project. It isolates race strategy from car pace.
Formula: `grid_to_finish_delta = grid - positionOrder`
Positive value = gained positions

---

## Changes Made

### [Session 1 - Current]
- Created IMPLEMENTATION_PLAN.md
- Created docs/worklog.md (this file)
- Next: Create docs/README.md

---

## Questions/Issues to Resolve
- None yet

---

## Team Members
- Project Lead: Mitul Bhatia
- Data Lead: Ramani Dhruv Dineshbhai
- ETL Lead: Vetriselvan R
- Analysis Lead: Agrim Kumar Malhotra
- Visualization Lead: Kushal Sarkar
- Strategy Lead: Ritik Ranjan
- PPT Lead: Palaparthi Harshakarthikeya
