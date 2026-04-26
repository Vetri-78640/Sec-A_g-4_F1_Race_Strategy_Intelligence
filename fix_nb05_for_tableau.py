"""
Fix Notebook 05 to add all Tableau-required columns and formatting
"""
import json

# Read notebook
with open('notebooks/05_final_load_prep.ipynb', 'r') as f:
    nb = json.load(f)

# Find Section 4 (Tableau formatting) and enhance it
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'source' in cell:
        source_text = ''.join(cell['source'])
        
        if 'Tableau-specific formatting' in source_text and 'constructor_short' in source_text:
            print(f"Found Tableau formatting cell at index {i}")
            
            # Add comprehensive Tableau preparation
            new_source = [
                "print(\"Applying Tableau-specific formatting...\")\n",
                "\n",
                "# ── Master Fact Formatting ─────────────────────────────────────────────────────\n",
                "master_fact['year']           = master_fact['year'].astype('int64')\n",
                "master_fact['grid']           = master_fact['grid'].fillna(0).astype('int64')\n",
                "master_fact['positionOrder']  = master_fact['positionOrder'].astype('int64')\n",
                "master_fact['points']         = master_fact['points'].astype('float64')\n",
                "\n",
                "# Convert booleans to 0/1 integers for Tableau calculations\n",
                "bool_cols = ['is_finisher', 'is_dnf', 'is_podium', 'is_win', 'is_pole', 'is_pitlane_start']\n",
                "for col in bool_cols:\n",
                "    if col in master_fact.columns:\n",
                "        master_fact[col] = master_fact[col].fillna(0).astype(int)\n",
                "\n",
                "# Driver name display: Surname, Forename\n",
                "master_fact['driver_name_display'] = master_fact['surname'].str.strip() + \", \" + master_fact['forename'].str.strip()\n",
                "\n",
                "# Constructor short names mapping (for tight layouts)\n",
                "constructor_map = {\n",
                "    'Red Bull': 'RBR', 'Mercedes': 'MER', 'Ferrari': 'FER', \n",
                "    'McLaren': 'MCL', 'Alpine F1 Team': 'ALP', 'Aston Martin': 'AST',\n",
                "    'AlphaTauri': 'ALT', 'Williams': 'WIL', 'Haas F1 Team': 'HAS',\n",
                "    'Alfa Romeo': 'ALF', 'Racing Point': 'RP', 'Renault': 'REN',\n",
                "    'Toro Rosso': 'STR', 'Force India': 'VJM', 'Sauber': 'SAU'\n",
                "}\n",
                "master_fact['constructor_short'] = master_fact['constructor_name'].map(constructor_map).fillna(master_fact['constructor_name'])\n",
                "\n",
                "# Era classification for filtering\n",
                "def classify_era(year):\n",
                "    if year < 2006:\n",
                "        return 'V10 Era'\n",
                "    elif year < 2014:\n",
                "        return 'V8 Era'\n",
                "    else:\n",
                "        return 'Turbo Hybrid Era'\n",
                "\n",
                "master_fact['era'] = master_fact['year'].apply(classify_era)\n",
                "\n",
                "# Grid Delta Category for Dashboard 3\n",
                "def categorize_delta(delta):\n",
                "    if pd.isna(delta):\n",
                "        return 'Unknown'\n",
                "    elif delta > 2:\n",
                "        return 'Gained 3+'\n",
                "    elif delta > 0:\n",
                "        return 'Gained 1-2'\n",
                "    elif delta == 0:\n",
                "        return 'Held Position'\n",
                "    else:\n",
                "        return 'Lost Positions'\n",
                "\n",
                "master_fact['grid_delta_category'] = master_fact['grid_to_finish_delta'].apply(categorize_delta)\n",
                "\n",
                "# Stop count bucket for Dashboard 2\n",
                "def bucket_stops(stops):\n",
                "    if pd.isna(stops):\n",
                "        return 'Unknown'\n",
                "    elif stops >= 3:\n",
                "        return '3+ stops'\n",
                "    elif stops == 2:\n",
                "        return '2 stops'\n",
                "    else:\n",
                "        return '1 stop'\n",
                "\n",
                "if 'stop_count' in master_fact.columns:\n",
                "    master_fact['stop_count_bucket'] = master_fact['stop_count'].apply(bucket_stops)\n",
                "\n",
                "# Convert pit times to seconds for readability\n",
                "if 'avg_pit_ms' in master_fact.columns:\n",
                "    master_fact['avg_pit_seconds'] = master_fact['avg_pit_ms'] / 1000\n",
                "\n",
                "if 'fastest_pit_ms' in master_fact.columns:\n",
                "    master_fact['fastest_pit_seconds'] = master_fact['fastest_pit_ms'] / 1000\n",
                "\n",
                "# Strip whitespace from key text fields\n",
                "master_fact['circuit_name'] = master_fact['circuit_name'].str.strip()\n",
                "master_fact['constructor_name'] = master_fact['constructor_name'].str.strip()\n",
                "\n",
                "# ── KPI Formatting ────────────────────────────────────────────────────────────\n",
                "rate_cols = ['points_efficiency', 'podium_rate', 'win_rate', 'pole_to_win_rate', 'dnf_rate']\n",
                "for col in rate_cols:\n",
                "    if col in kpis.columns:\n",
                "        kpis[col] = kpis[col].round(4)\n",
                "\n",
                "kpis['constructor_name'] = kpis['constructor_name'].str.strip()\n",
                "\n",
                "# Add era to KPIs\n",
                "kpis['era'] = kpis['year'].apply(classify_era)\n",
                "\n",
                "# ── Circuit Profile Enhancements ──────────────────────────────────────────────\n",
                "# Add qualifying_lock_in_score (higher = qualifying matters more)\n",
                "# Based on low avg_delta and high qualifying_gap\n",
                "if 'avg_delta' in profile.columns and 'avg_qualifying_gap' in profile.columns:\n",
                "    # Normalize to 0-100 scale\n",
                "    delta_norm = (profile['avg_delta'].max() - profile['avg_delta']) / (profile['avg_delta'].max() - profile['avg_delta'].min())\n",
                "    gap_norm = profile['avg_qualifying_gap'] / profile['avg_qualifying_gap'].max()\n",
                "    profile['qualifying_lock_in_score'] = ((delta_norm * 0.6 + gap_norm * 0.4) * 100).round(1)\n",
                "\n",
                "# Add optimal_stop_count (most common successful strategy)\n",
                "if 'best_strategy_stops' in profile.columns:\n",
                "    profile['optimal_stop_count'] = profile['best_strategy_stops'].fillna(2).astype(int)\n",
                "elif 'avg_1stop_position' in profile.columns and 'avg_2stop_position' in profile.columns:\n",
                "    # Choose strategy with better average position\n",
                "    profile['optimal_stop_count'] = profile.apply(\n",
                "        lambda row: 1 if pd.notna(row['avg_1stop_position']) and \n",
                "                        (pd.isna(row['avg_2stop_position']) or row['avg_1stop_position'] < row['avg_2stop_position'])\n",
                "                    else 2,\n",
                "        axis=1\n",
                "    )\n",
                "\n",
                "# Add compound_bias placeholder (for future tyre data integration)\n",
                "if 'compound_bias' not in profile.columns:\n",
                "    profile['compound_bias'] = 0  # Neutral baseline\n",
                "\n",
                "print(\"Formatting complete.\")\n",
                "print(f\"\\nTableau-ready columns added:\")\n",
                "print(f\"  - era (V10/V8/Turbo Hybrid)\")\n",
                "print(f\"  - grid_delta_category (Gained 3+, Gained 1-2, Held, Lost)\")\n",
                "print(f\"  - stop_count_bucket (1/2/3+ stops)\")\n",
                "print(f\"  - avg_pit_seconds (converted from ms)\")\n",
                "print(f\"  - qualifying_lock_in_score (0-100 scale)\")\n",
                "print(f\"  - optimal_stop_count (1 or 2)\")"
            ]
            
            cell['source'] = new_source
            cell['outputs'] = []
            cell['execution_count'] = None
            
            print("✅ Updated Tableau formatting section with all required columns")
            break

# Save updated notebook
with open('notebooks/05_final_load_prep.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✅ Notebook 05 updated with Tableau-specific enhancements!")
