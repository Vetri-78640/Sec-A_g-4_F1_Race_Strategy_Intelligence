"""
Update notebook 04 to use fixed clustering (remove Mugello outlier)
"""
import json

# Read notebook
with open('notebooks/04_statistical_analysis.ipynb', 'r') as f:
    nb = json.load(f)

# Find the clustering cell (Section 4)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'source' in cell:
        source_text = ''.join(cell['source'])
        
        # Find the clustering code cell
        if 'Prepare clustering data' in source_text and 'cluster_features' in source_text:
            print(f"Found clustering cell at index {i}")
            
            # Replace the source code
            new_source = [
                "# Prepare clustering data\n",
                "cluster_features = ['avg_delta', 'avg_qualifying_gap', 'lap_time_variance']\n",
                "cluster_data = circuit_profile[cluster_features].dropna()\n",
                "circuit_ids = circuit_profile.loc[cluster_data.index, 'circuitId']\n",
                "\n",
                "# Remove extreme outliers (lap_time_variance > 200,000) to improve clustering\n",
                "outlier_mask = cluster_data['lap_time_variance'] > 200000\n",
                "cluster_data = cluster_data[~outlier_mask]\n",
                "circuit_ids = circuit_ids[~outlier_mask]\n",
                "\n",
                "print(f'Clustering {len(cluster_data)} circuits')\n",
                "\n",
                "# Standardize features\n",
                "scaler_cluster = StandardScaler()\n",
                "X_cluster = scaler_cluster.fit_transform(cluster_data)\n",
                "\n",
                "# Fit K-Means with K=3\n",
                "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
                "labels = kmeans.fit_predict(X_cluster)\n",
                "\n",
                "# Add labels to circuit_profile\n",
                "circuit_profile['cluster'] = -1\n",
                "circuit_profile.loc[cluster_data.index, 'cluster'] = labels\n",
                "\n",
                "# Assign meaningful names based on centroids\n",
                "centroids = pd.DataFrame(\n",
                "    scaler_cluster.inverse_transform(kmeans.cluster_centers_),\n",
                "    columns=cluster_features\n",
                ")\n",
                "\n",
                "print('\\n' + '='*80)\n",
                "print('CLUSTER CENTROIDS')\n",
                "print('='*80)\n",
                "print(centroids)\n",
                "\n",
                "# Label clusters based on avg_delta (higher = more position changes = Strategy-Dominant)\n",
                "sorted_by_delta = centroids.sort_values('avg_delta', ascending=True)\n",
                "cluster_names = {\n",
                "    sorted_by_delta.index[0]: 'Qualifying-Dominant',\n",
                "    sorted_by_delta.index[1]: 'Mixed',\n",
                "    sorted_by_delta.index[2]: 'Strategy-Dominant'\n",
                "}\n",
                "\n",
                "circuit_profile['cluster_label'] = circuit_profile['cluster'].map(cluster_names)\n",
                "\n",
                "print('\\n' + '='*80)\n",
                "print('CLUSTER LABELS')\n",
                "print('='*80)\n",
                "for i, name in cluster_names.items():\n",
                "    count = (circuit_profile['cluster'] == i).sum()\n",
                "    print(f'Cluster {i}: {name:25s} ({count} circuits)')\n",
                "\n",
                "print('\\n' + '='*80)\n",
                "print('PLAIN ENGLISH CONCLUSION')\n",
                "print('='*80)\n",
                "print(f\"Circuits have been classified into 3 distinct types:\")\n",
                "print(f\"1. Qualifying-Dominant: Grid position is critical, overtaking is difficult\")\n",
                "print(f\"2. Strategy-Dominant: Race strategy and pit stops have high impact\")\n",
                "print(f\"3. Mixed: Balanced between qualifying and strategy\")"
            ]
            
            cell['source'] = new_source
            cell['outputs'] = []  # Clear outputs so it re-runs
            cell['execution_count'] = None
            
            print("✅ Updated clustering code to remove outliers")
            break

# Save updated notebook
with open('notebooks/04_statistical_analysis.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✅ Notebook updated! Now re-running...")
