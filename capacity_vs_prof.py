import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from main import load_data


# Load cleaned dataset
df = load_data()

# Scatter plot with regression line
"""Visually, the lower capacity centers have higher proficiency rate since 
lower capacity centers are more dense, meaning there are much more smaller schools then 
larger schools, skewing the data set."""
sns.set(style="whitegrid")
sns.regplot(
    x="Total Capacity",
    y="Percent Proficient",
    data=df,
    scatter_kws={'alpha':0.7, 's':60},
    line_kws={'color':'red'}
)
plt.title("Total Capacity vs Percent Proficient")
plt.xlabel("Total Capacity")
plt.ylabel("Percent Proficient (%)")
plt.xlim(0, 220)
plt.ylim(0, 100)
plt.show()

corr = df["Total Capacity"].corr(df["Percent Proficient"])
print(f"Correlation: {corr:.3f}")

print(df[["Total Capacity", "Percent Proficient"]].describe())
df.groupby("License Type")["Percent Proficient"].describe()


# Equal-width bins
""" More bins less than 200 since most centers have less than 100 capacity"""
bins = [0, 25, 50, 100, 200, 300]
labels = ["<25", "26-50", "51-100", "101-150", "150+"]
df["Capacity Group"] = pd.cut(df["Total Capacity"], bins=5, labels=labels)

avg = df.groupby("Capacity Group")["Percent Proficient"].mean().reset_index()
sns.barplot(x="Capacity Group", y="Percent Proficient", data=avg, color="blue")
plt.ylim(0, 100)
plt.title("Average Percent Proficient by Capacity Range")
plt.show()

# K-means Clustering
x = df[["Total Capacity", "Percent Proficient"]].dropna().to_numpy() # skips missing data
k = 3  # number of clusters

# random centroids
np.random.seed(42)
centroids = x[np.random.choice(range(len(x)), k, replace=False)]

def calc_euclidean_distance(X, centroids):
    return np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))

# Calculate K-means loop
for i in range(20):
    # assign points to the nearest centroid
    distance = calc_euclidean_distance(x, centroids)
    labels = np.argmin(distance, axis=0)  # labels each point to its nearest centroid

    # computes new centroids
    new_centroids = np.zeros_like(centroids)

    for j in range(k):
        cluster_points = []
        for y in range(len(x)):
            if labels[i] == j:
                cluster_points.append(x[i])

        # converts list to array
        cluster_points = np.array(cluster_points)

        # mean of points = new centroid
        new_centroids[j] = cluster_points.mean(axis=0)

    centroids = new_centroids

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
plt.show()







