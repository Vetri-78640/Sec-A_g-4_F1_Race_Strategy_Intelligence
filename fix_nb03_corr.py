import json

# Read the notebook
with open('notebooks/03_eda.ipynb', 'r') as f:
    nb = json.load(f)

# Find and update Section 8 (Correlation Matrix)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        
        # Fix Section 8 - Correlation Matrix
        if 'Section 8: Correlation Matrix' in source or 'Section 9: Correlation Matrix' in source:
            cell['source'] = [
                "---\n",
                "## Section 8: Correlation Matrix of Numeric KPIs\n",
                "\n",
                "### INSIGHT: Grid Position and Pit Stop Efficiency Are the Strongest Controllable Predictors of Points\n",
                "\n",
                "**WHAT TO LOOK FOR:**\n",
                "- Strong negative correlation between grid and points (lower grid number = more points)\n",
                "- Correlation between pit stop efficiency and race outcome\n",
                "- Relationship between qualifying gap and final points\n",
                "\n",
                "**WHY THIS MATTERS:**\n",
                "This heatmap shows which factors are most strongly related to scoring points. Negative correlations with grid position confirm that starting position is critical. We focus ONLY on continuous numeric variables for valid correlation analysis.\n",
                "\n",
                "**NOTE:** Binary variables (is_dnf, is_podium, is_win) are EXCLUDED as they don't provide meaningful correlation with continuous variables."
            ]

# Find the correlation code cell and update it
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        # Update correlation matrix code
        if 'correlation_matrix = corr_data.corr()' in source:
            cell['source'] = [
                "# Select ONLY continuous numeric columns for correlation\n",
                "# EXCLUDE binary variables (is_dnf, is_podium, is_win) as they don't provide meaningful correlation\n",
                "corr_columns = ['points', 'grid', 'stop_count', 'avg_pit_ms', 'qualifying_gap_ms', 'grid_to_finish_delta']\n",
                "\n",
                "corr_data = master_fact_filtered[corr_columns].dropna()\n",
                "correlation_matrix = corr_data.corr()\n",
                "\n",
                "print(f'Correlation analysis on {len(corr_data):,} race results')\n",
                "print(f'Variables analyzed: {corr_columns}')\n",
                "\n",
                "fig, ax = plt.subplots(figsize=(10, 8))\n",
                "\n",
                "sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,\n",
                "            square=True, linewidths=1, cbar_kws={\"shrink\": 0.8}, ax=ax,\n",
                "            vmin=-1, vmax=1)\n",
                "\n",
                "ax.set_title('Grid Position and Pit Stop Efficiency Are the Strongest Controllable Predictors of Points', \n",
                "             fontsize=13, fontweight='bold', pad=20)\n",
                "\n",
                "# Add interpretation text\n",
                "ax.text(0.5, -0.15, 'Red = Positive Correlation | Blue = Negative Correlation | Darker = Stronger',\n",
                "        ha='center', transform=ax.transAxes, fontsize=10, style='italic')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('../reports/figures/chart_07_correlation_matrix.png', dpi=150, bbox_inches='tight')\n",
                "plt.show()\n",
                "\n",
                "print(f'\\nChart saved: chart_07_correlation_matrix.png')"
            ]
            cell['outputs'] = []
            cell['execution_count'] = None

# Save the modified notebook
with open('notebooks/03_eda.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Correlation matrix section updated!")
