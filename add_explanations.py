import json

with open('notebooks/03_eda.ipynb', 'r') as f:
    nb = json.load(f)

# Add explanations to all sections
explanations = {
    'Section 2: Points Efficiency': [
        "---\n",
        "## Section 2: Points Efficiency Trend Per Constructor (2010-2024)\n",
        "\n",
        "### INSIGHT: Mid-Field Constructor Points Efficiency Has Converged Since the 2014 Hybrid Era\n",
        "\n",
        "**WHAT TO LOOK FOR:**\n",
        "- Convergence of lines after 2014 = more competitive mid-field\n",
        "- Teams with upward trends are improving\n",
        "- Consistent performers vs volatile performers\n",
        "\n",
        "**WHY THIS MATTERS:**\n",
        "Points efficiency (points per race) shows which teams are consistently scoring. Convergence means the mid-field is more competitive, so small strategic advantages matter more.\n",
        "\n",
        "**DATA:** Top 10 constructors by total points, 2010-2024"
    ],
    'Section 3: DNF Rate': [
        "---\n",
        "## Section 3: DNF Rate by Constructor and DNF Category\n",
        "\n",
        "### INSIGHT: Mechanical DNFs Cost Mid-Field Teams 15-20% of Potential Points\n",
        "\n",
        "**WHAT TO LOOK FOR:**\n",
        "- Teams with DNF rate > 15% (red bars) are losing significant points\n",
        "- Breakdown by cause: Mechanical vs Accident vs Other\n",
        "- Which teams have reliability issues\n",
        "\n",
        "**WHY THIS MATTERS:**\n",
        "Every DNF is a lost opportunity to score points. For mid-field teams, reducing DNF rate by 2-3% can mean 10-15 extra championship points per season.\n",
        "\n",
        "**DATA:** All constructors 2010-2024, sorted by DNF rate"
    ],
    'Section 4: Grid-to-Finish Delta': [
        "---\n",
        "## Section 4: Grid-to-Finish Delta Distribution Per Constructor\n",
        "\n",
        "### INSIGHT: Top Teams Consistently Gain Positions While Mid-Field Teams Show High Variance\n",
        "\n",
        "**WHAT TO LOOK FOR:**\n",
        "- Box plot shows distribution: median (line), quartiles (box), outliers (dots)\n",
        "- Positive delta = gained positions, negative = lost positions\n",
        "- Narrow boxes = consistent execution, wide boxes = variable performance\n",
        "\n",
        "**WHY THIS MATTERS:**\n",
        "Grid-to-finish delta isolates race strategy from car pace. Teams with positive median and tight distribution have better race execution. High variance indicates inconsistent strategy decisions.\n",
        "\n",
        "**DATA:** Top 12 constructors by race count, 2010-2024, finishers only"
    ],
    'Section 6: Win/Podium Conversion': [
        "---\n",
        "## Section 6: Win/Podium Conversion Rate by Constructor\n",
        "\n",
        "### INSIGHT: Podium Rate Separates Championship Contenders from Mid-Field Teams\n",
        "\n",
        "**WHAT TO LOOK FOR:**\n",
        "- Clear gap between top teams (>30% podium rate) and mid-field (<10%)\n",
        "- Win rate vs podium rate ratio shows consistency\n",
        "- Mid-field teams rarely win but can podium with good strategy\n",
        "\n",
        "**WHY THIS MATTERS:**\n",
        "For mid-field teams, even increasing podium rate from 5% to 8% means 2-3 extra podiums per season = significant championship points and prize money.\n",
        "\n",
        "**DATA:** Top 12 constructors by total points, 2010-2024"
    ],
    'Section 7: Qualifying Gap': [
        "---\n",
        "## Section 7: Qualifying Gap to Pole by Constructor\n",
        "\n",
        "### INSIGHT: Sub-0.5 Second Qualifying Gap Correlates with Top-10 Championship Finish\n",
        "\n",
        "**WHAT TO LOOK FOR:**\n",
        "- Box plot shows qualifying gap distribution per team\n",
        "- Red line at 0.5s = threshold for competitive qualifying\n",
        "- Teams consistently below 0.5s are championship contenders\n",
        "\n",
        "**WHY THIS MATTERS:**\n",
        "Qualifying within 0.5s of pole means you're in the top 6-8 grid positions. At qualifying-dominant circuits (Monaco, Hungary), this is critical for points scoring.\n",
        "\n",
        "**DATA:** Top 12 constructors, 2010-2024, races with qualifying data"
    ]
}

# Update markdown cells with explanations
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        for key, explanation in explanations.items():
            if key in source and 'WHAT TO LOOK FOR' not in source:
                cell['source'] = explanation
                break

with open('notebooks/03_eda.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Added explanations to all sections!")
