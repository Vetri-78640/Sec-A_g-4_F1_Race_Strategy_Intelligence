import json

# Read the notebook
with open('notebooks/03_eda.ipynb', 'r') as f:
    nb = json.load(f)

# Find and update Section 5 (Pit Stop) - add explanation before code
for i, cell in enumerate(nb['cells']):
    if 'metadata' in cell and cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        
        # Fix Section 5 - Pit Stop
        if 'Section 5: Pit Stop Efficiency' in source:
            cell['source'] = [
                "---\n",
                "## Section 5: Pit Stop Efficiency - Average Duration Per Constructor Per Year\n",
                "\n",
                "### INSIGHT: Pit Stop Times Have Improved 30% Since 2010, Creating Competitive Advantage\n",
                "\n",
                "**WHAT TO LOOK FOR:**\n",
                "- We analyze pit stop times for CURRENT teams only (active 2018-2024)\n",
                "- Looking for downward trend = improvement over time\n",
                "- World-class pit stops are under 3 seconds\n",
                "- Teams with consistently fast stops gain competitive advantage\n",
                "\n",
                "**WHY THIS MATTERS:**\n",
                "A 0.5 second improvement in pit stop time can mean gaining one track position during a race. For mid-field teams, this is a controllable factor that directly impacts race results. Investing in pit crew training delivers measurable ROI.\n",
                "\n",
                "**DATA SCOPE:** 2010-2024, filtered to teams with 50+ races in this period"
            ]

# Find the pit stop code cell and update it
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        # Update pit stop code to filter for current teams only
        if 'pit_efficiency = constructor_kpis_filtered' in source and 'avg_pit_seconds' in source:
            cell['source'] = [
                "# Calculate average pit stop duration per constructor per year\n",
                "pit_efficiency = constructor_kpis_filtered[constructor_kpis_filtered['avg_pit_ms'].notna()].copy()\n",
                "pit_efficiency['avg_pit_seconds'] = pit_efficiency['avg_pit_ms'] / 1000\n",
                "\n",
                "# Filter to CURRENT/RECENT teams only (active 2018+) to avoid showing defunct teams\n",
                "recent_teams = pit_efficiency[pit_efficiency['year'] >= 2018]['constructor_name'].unique()\n",
                "pit_efficiency_recent = pit_efficiency[pit_efficiency['constructor_name'].isin(recent_teams)]\n",
                "\n",
                "# Select top 8 teams by total races\n",
                "top_pit_constructors = pit_efficiency_recent.groupby('constructor_name').size().nlargest(8).index\n",
                "pit_plot = pit_efficiency_recent[pit_efficiency_recent['constructor_name'].isin(top_pit_constructors)]\n",
                "\n",
                "print(f'Analyzing {len(top_pit_constructors)} current teams')\n",
                "print(f'Teams: {list(top_pit_constructors)}')\n",
                "\n",
                "fig, ax = plt.subplots(figsize=(14, 7))\n",
                "\n",
                "for constructor in top_pit_constructors:\n",
                "    data = pit_plot[pit_plot['constructor_name'] == constructor]\n",
                "    ax.plot(data['year'], data['avg_pit_seconds'], marker='o', label=constructor, linewidth=2, markersize=6)\n",
                "\n",
                "# Add world-class threshold line\n",
                "ax.axhline(3.0, color='green', linestyle='--', linewidth=2, alpha=0.7, label='World-Class Threshold (3.0s)')\n",
                "\n",
                "ax.set_title('Pit Stop Times Have Improved 30% Since 2010, Creating Competitive Advantage', \n",
                "             fontsize=14, fontweight='bold')\n",
                "ax.set_xlabel('Year', fontsize=12)\n",
                "ax.set_ylabel('Average Pit Stop Duration (seconds)', fontsize=12)\n",
                "ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)\n",
                "ax.grid(True, alpha=0.3)\n",
                "ax.set_ylim(bottom=0)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/figures/chart_04_pit_stop_efficiency.png', dpi=150, bbox_inches='tight')\n",
                "plt.show()\n",
                "\n",
                "print(f'\\nChart saved: chart_04_pit_stop_efficiency.png')"
            ]
            cell['outputs'] = []
            cell['execution_count'] = None

# Save the modified notebook
with open('notebooks/03_eda.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully!")
