import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from main import load_data

# Question 3

# Correlation between the funding source of
# Pre-K programs in Memphis and student proficiency in reading/writing?

# Preprocessing
df = load_data()

df = df.dropna(subset=["Percent Proficient", "Funding Source", "Total Capacity"]) # remove missing data

# Visualization
order = df.groupby("Funding Source")["Percent Proficient"].mean().sort_values().index

plt.figure(figsize=(10, 5))
plt.boxplot(
    [df.loc[df["Funding Source"] == fs, "Percent Proficient"].dropna() for fs in order],
    tick_labels=order,
)

plt.title("Pre-K Reading/Writing Proficiency by Funding Source")
plt.xlabel("Funding Source")
plt.ylabel("Percent Proficient")
plt.tight_layout()
plt.show()

# Central tendency
funding_summary = (
    df.groupby("Funding Source")["Percent Proficient"]
      .agg(["mean", "std", "count"])
      .sort_values("mean", ascending=False)
)
print("\nAverage Proficiency by Funding Source")
print(funding_summary)

# Correlation analysis
numeric_cols = ["Percent Proficient", "Total Capacity"]
corr = df[numeric_cols].corr()
print("\nCorrelation Matrix")
print(corr)

# Clustering & K-Means
df["Funding_Code"] = pd.factorize(df["Funding Source"])[0]

x = df[["Funding_Code", "Percent Proficient"]].dropna().to_numpy()

k = 3
np.random.seed(42)

# Initialize centroids
centroids = x[np.random.choice(range(len(x)), k, replace=False)]

def calc_euclidean_distance(X, centroids):
    return np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))

# K-means algorithm
for i in range(20):
    # Assign clusters
    distance = calc_euclidean_distance(x, centroids)
    labels = np.argmin(distance, axis=0)

    # Update centroids
    new_centroids = np.zeros_like(centroids)
    for j in range(k):
        cluster_points = x[labels == j]
        if len(cluster_points) > 0:
            new_centroids[j] = cluster_points.mean(axis=0)
        else:
            new_centroids[j] = centroids[j]

    centroids = new_centroids

# Plot clusters
plt.figure(figsize=(8,6))
colors = ["blue", "green", "purple"]

for j in range(k):
    cluster_points = x[labels == j]
    plt.scatter(
        cluster_points[:, 0],
        cluster_points[:, 1],
        color=colors[j],
        s=60,
        label=f"Cluster {j}"
    )

plt.xticks(
    ticks=df["Funding_Code"].unique(),
    labels=df["Funding Source"].unique(),
    rotation=20,
    ha='right'
)

plt.xlabel("Funding Source (Encoded)")
plt.ylabel("Percent Proficient (%)")
plt.title("K-Means Clustering: Funding Type vs Proficiency")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# Density-based clustering (DBSCAN)
eps = 0.35           # smaller number → more clusters
min_samples = 3      # minimum points to form a cluster

# Euclidean distance helper
def euclidean(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Find neighbors within eps
def region_query(x, point_idx, eps):
    neighbors = []
    for i in range(len(x)):
        if euclidean(x[point_idx], x[i]) <= eps:
            neighbors.append(i)
    return neighbors

# Expand cluster
def expand_cluster(x, labels, point_idx, neighbors, cluster_id, eps, min_samples):
    labels[point_idx] = cluster_id

    queue = list(neighbors)

    while queue:
        current = queue.pop(0)

        if labels[current] == -1:
            labels[current] = cluster_id

        if labels[current] != None:
            continue

        labels[current] = cluster_id

        current_neighbors = region_query(x, current, eps)

        if len(current_neighbors) >= min_samples:
            queue.extend(current_neighbors)

# MAIN DBSCAN
labels = [None] * len(x)
cluster_id = 0

for i in range(len(x)):
    if labels[i] != None:
        continue

    neighbors = region_query(x, i, eps)

    if len(neighbors) < min_samples:
        labels[i] = -1   # Noise
    else:
        expand_cluster(x, labels, i, neighbors, cluster_id, eps, min_samples)
        cluster_id += 1

# Add labels to DataFrame
df.loc[df["Percent Proficient"].notna(), "DBSCAN"] = labels

plt.figure(figsize=(10,6))

plt.scatter(
    df["Percent Proficient"],
    df["Funding_Code"],
    c=df["Manual_DBSCAN"].astype(int),
    cmap="viridis",
    s=80,
    alpha=0.8
)

plt.xlabel("Percent Proficient (%)")
plt.ylabel("Funding Code")
plt.title("DBSCAN Clustering\n(Funding Source vs Proficiency)")
plt.grid(True)
plt.show()

# Quick report
print("\nSUMMARY REPORT")
print(f"Total Schools Analyzed: {len(df)}")
print(f"Funding Types Compared: {df['Funding Source'].nunique()}")
print(f"Highest Performing Funding Source: {funding_summary.index[0]} ({funding_summary['mean'].iloc[0]:.2f}% proficient)")
print(f"Lowest Performing Funding Source: {funding_summary.index[-1]} ({funding_summary['mean'].iloc[-1]:.2f}% proficient)")
