"""
Fix K-Means clustering to properly identify Strategy-Dominant circuits
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Load data
circuit_profile = pd.read_csv('data/processed/circuit_strategy_profile.csv')

print("="*80)
print("FIXING K-MEANS CLUSTERING")
print("="*80)

# Prepare clustering features
cluster_features = ['avg_delta', 'avg_qualifying_gap', 'lap_time_variance']
cluster_data = circuit_profile[cluster_features].dropna()
circuit_ids = circuit_profile.loc[cluster_data.index, 'circuitId']
circuit_names = circuit_profile.loc[cluster_data.index, 'circuit_name']

print(f'\nClustering {len(cluster_data)} circuits')

# OPTION 1: Remove extreme outliers (lap_time_variance > 200,000)
print("\n" + "="*80)
print("OPTION 1: Remove Mugello outlier and re-cluster")
print("="*80)

# Identify outliers
outlier_mask = cluster_data['lap_time_variance'] > 200000
outliers = circuit_profile.loc[cluster_data.index[outlier_mask], 'circuit_name'].tolist()
print(f"Removing outliers: {outliers}")

# Filter out outliers
cluster_data_clean = cluster_data[~outlier_mask]
circuit_ids_clean = circuit_ids[~outlier_mask]
circuit_names_clean = circuit_names[~outlier_mask]

# Standardize features
scaler = StandardScaler()
X_cluster = scaler.fit_transform(cluster_data_clean)

# Fit K-Means with K=3
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_cluster)

# Get centroids in original scale
centroids = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=cluster_features
)

print("\nCluster Centroids:")
print(centroids)

# Assign meaningful labels based on avg_delta
# Higher avg_delta = more position changes = Strategy-Dominant
# Lower avg_delta = fewer position changes = Qualifying-Dominant
sorted_by_delta = centroids.sort_values('avg_delta', ascending=True)
cluster_mapping = {
    sorted_by_delta.index[0]: 'Qualifying-Dominant',
    sorted_by_delta.index[1]: 'Mixed',
    sorted_by_delta.index[2]: 'Strategy-Dominant'
}

print("\n" + "="*80)
print("CLUSTER ASSIGNMENTS (based on avg_delta)")
print("="*80)
for cluster_id, label in cluster_mapping.items():
    count = (labels == cluster_id).sum()
    avg_delta = centroids.loc[cluster_id, 'avg_delta']
    print(f"Cluster {cluster_id} → {label:25s} ({count:2d} circuits, avg_delta={avg_delta:.2f})")

# Create results dataframe
results = pd.DataFrame({
    'circuitId': circuit_ids_clean.values,
    'circuit_name': circuit_names_clean.values,
    'cluster': labels,
    'cluster_label': [cluster_mapping[c] for c in labels],
    'avg_delta': cluster_data_clean['avg_delta'].values,
    'avg_qualifying_gap': cluster_data_clean['avg_qualifying_gap'].values,
    'lap_time_variance': cluster_data_clean['lap_time_variance'].values
})

# Show circuits in each cluster
print("\n" + "="*80)
print("CIRCUITS BY CLUSTER")
print("="*80)
for label in ['Qualifying-Dominant', 'Mixed', 'Strategy-Dominant']:
    circuits = results[results['cluster_label'] == label].sort_values('avg_delta', ascending=False)
    print(f"\n{label} ({len(circuits)} circuits):")
    print(circuits[['circuit_name', 'avg_delta']].to_string(index=False))

# Update the original circuit_profile
circuit_profile['cluster'] = -1
circuit_profile['cluster_label'] = None

for idx, row in results.iterrows():
    mask = circuit_profile['circuitId'] == row['circuitId']
    circuit_profile.loc[mask, 'cluster'] = row['cluster']
    circuit_profile.loc[mask, 'cluster_label'] = row['cluster_label']

# Save updated file
output_path = 'data/processed/circuit_strategy_profile.csv'
circuit_profile.to_csv(output_path, index=False)

print("\n" + "="*80)
print("SAVED UPDATED FILE")
print("="*80)
print(f"File: {output_path}")
print(f"Total circuits: {len(circuit_profile)}")
print(f"Clustered circuits: {len(results)}")
print(f"Outliers removed: {len(outliers)}")

print("\n✅ Clustering fixed! Now you have proper Strategy-Dominant circuits.")
