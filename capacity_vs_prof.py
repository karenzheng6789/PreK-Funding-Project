import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler

from main import load_data


# Load cleaned dataset
def load_data():
    return pd.read_csv("prek_capacity_2024.csv", delimiter=';')

# Scatter plot with regression line
def regression_line(df):
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
def equal_width_partitioning(df):
    """ More bins less than 200 since most centers have less than 100 capacity"""
    bins = [0, 25, 50, 100, 200, 300]
    labels = ["<25", "26-50", "51-100", "101-150", "150+"]
    df["Capacity Group"] = pd.cut(df["Total Capacity"], bins=5, labels=labels)

    avg = df.groupby("Capacity Group")["Percent Proficient"].mean().reset_index()
    sns.barplot(x="Capacity Group", y="Percent Proficient", data=avg, color="blue")
    plt.ylim(0, 100)
    plt.title("Average Percent Proficient by Capacity Range")
    plt.show()

def calc_euclidean_distance(X, centroids):
        return np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))

# K-means Clustering
def k_means_clustering(df):
    data = df[["Total Capacity", "Percent Proficient"]].dropna().to_numpy() # skips missing data
    # scale data for K-means
    scaler = StandardScaler()
    x = scaler.fit_transform(data)

    k = 3  # number of clusters

    # random centroids
    np.random.seed(42)
    centroids = x[np.random.choice(range(len(x)), k, replace=False)]

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
                if labels[y] == j:
                    cluster_points.append(x[y])

            # converts list to array
            cluster_points = np.array(cluster_points)

            # mean of points = new centroid
            new_centroids[j] = cluster_points.mean(axis=0)

            # Protect against empty cluster
            if len(cluster_points) > 0:
                new_centroids[j] = cluster_points.mean(axis=0)
            else:
                new_centroids[j] = centroids[j]

        centroids = new_centroids

    # Convert centroids back to ORIGINAL scale
    real_centroids = scaler.inverse_transform(centroids)

    plt.figure(figsize=(8,6))
    colors = ["blue", "green", "purple"]

    # plot points by cluster
    for j in range(k):
        plt.scatter(
            data[labels == j, 0],
            data[labels == j, 1],
            color=colors[j],
            s=60,
            label=f"Cluster {j}"
        )

    plt.scatter(
        real_centroids[:, 0],     # centroid capacity
        real_centroids[:, 1],     # centroid proficiency
        c="red",
        s=200,
        marker="X",
        label="Centroids"
    )

    plt.xlabel("Total Capacity")
    plt.ylabel("Percent Proficient (%)")
    plt.title("K-Means Clustering (Manual NumPy)")
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)

    plt.show()







