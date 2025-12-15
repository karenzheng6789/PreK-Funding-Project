import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from main import load_data

# LOAD AND CLEAN

df = load_data()

# Remove rows with missing key fields
df = df.dropna(subset=["Percent Proficient", "Funding Source", "Total Capacity"]).copy()

# Ensure Percent Proficient is numeric
df["Percent Proficient"] = pd.to_numeric(df["Percent Proficient"], errors="coerce")
df = df.dropna(subset=["Percent Proficient"])

# Encode funding source once and reuse
df["Funding_Code"] = pd.factorize(df["Funding Source"])[0]

# BOX PLOT

order = (
    df.groupby("Funding Source")["Percent Proficient"]
      .mean()
      .sort_values()
      .index
)

plt.figure(figsize=(10, 5))
plt.boxplot(
    [df.loc[df["Funding Source"] == fs, "Percent Proficient"].dropna() for fs in order],
    labels=order,
)
plt.title("Pre-K Reading/Writing Proficiency by Funding Source")
plt.xlabel("Funding Source")
plt.ylabel("Percent Proficient")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.show()

#CENTRAL TENDENCY

funding_summary = (
    df.groupby("Funding Source")["Percent Proficient"]
      .agg(["mean", "std", "count"])
      .sort_values("mean", ascending=False)
)

print("\nAverage Proficiency by Funding Source")
print(funding_summary)

# CORRELATION ANALYSIS

numeric_cols = ["Percent Proficient", "Total Capacity"]
corr = df[numeric_cols].corr()

print("\nCorrelation Matrix")
print(corr)


# CLUSTERING: K-MEANS

X = df[["Funding_Code", "Percent Proficient"]].to_numpy()

k = 3
np.random.seed(42)

# Initialize centroids by sampling k random points from X
centroids = X[np.random.choice(range(len(X)), k, replace=False)]

def calc_euclidean_distance(X, centroids):
    """
    X: (n_samples, n_features)
    centroids: (k, n_features)
    returns: (k, n_samples) distance matrix
    """
    return np.sqrt(((X - centroids[:, np.newaxis]) ** 2).sum(axis=2))

# K-means algorithm
for i in range(20):
    # Assign clusters
    distance = calc_euclidean_distance(X, centroids)  # shape (k, n)
    labels = np.argmin(distance, axis=0)              # shape (n,)

    # Update centroids
    new_centroids = np.zeros_like(centroids)
    for j in range(k):
        cluster_points = X[labels == j]
        if len(cluster_points) > 0:
            new_centroids[j] = cluster_points.mean(axis=0)
        else:
            # If a cluster loses all points, keep old centroid
            new_centroids[j] = centroids[j]

    centroids = new_centroids

#PLOT CLUSTER

plt.figure(figsize=(8, 6))
colors = ["blue", "green", "purple"]

for j in range(k):
    cluster_points = X[labels == j]
    plt.scatter(
        cluster_points[:, 0],   # Funding_Code
        cluster_points[:, 1],   # Percent Proficient
        color=colors[j % len(colors)],
        s=60,
        label=f"Cluster {j}",
    )

# Build a stable mapping from code → label for x-axis
code_label_map = (
    df[["Funding_Code", "Funding Source"]]
      .drop_duplicates()
      .sort_values("Funding_Code")
)

plt.xticks(
    ticks=code_label_map["Funding_Code"],
    labels=code_label_map["Funding Source"],
    rotation=20,
    ha="right",
)

plt.xlabel("Funding Source (Encoded)")
plt.ylabel("Percent Proficient (%)")
plt.title("K-Means Clustering: Funding Type vs Proficiency")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# QUICK SUMMARY REPORT

print("\nSUMMARY REPORT")
print(f"Total Schools Analyzed: {len(df)}")
print(f"Funding Types Compared: {df['Funding Source'].nunique()}")
print(
    f"Highest Performing Funding Source: "
    f"{funding_summary.index[0]} ({funding_summary['mean'].iloc[0]:.2f}% proficient)"
)
print(
    f"Lowest Performing Funding Source: "
    f"{funding_summary.index[-1]} ({funding_summary['mean'].iloc[-1]:.2f}% proficient)"
)

# LINEAR REGRESSION

x = df["Funding_Code"].to_numpy()
y = df["Percent Proficient"].to_numpy()

# Means
x_mean = np.mean(x)
y_mean = np.mean(y)

# Slope (m) and Intercept (b)
numerator = np.sum((x - x_mean) * (y - y_mean))
denominator = np.sum((x - x_mean) ** 2)

m = numerator / denominator
b = y_mean - m * x_mean

# Predictions
y_pred = m * x + b

# R-squared
ss_total = np.sum((y - y_mean) ** 2)
ss_resid = np.sum((y - y_pred) ** 2)
r_squared = 1 - (ss_resid / ss_total)

print("\nLINEAR REGRESSION RESULTS")
print(f"Slope (m): {m:.6f}")
print(f"Intercept (b): {b:.6f}")
print(f"R-squared: {r_squared:.6f}")

# Regression plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y, s=70)

x_line = np.linspace(x.min(), x.max(), 200)
y_line = m * x_line + b
plt.plot(x_line, y_line)

plt.xticks(
    ticks=code_label_map["Funding_Code"],
    labels=code_label_map["Funding Source"],
    rotation=20,
    ha="right",
)

plt.xlabel("Funding Source (Encoded)")
plt.ylabel("Percent Proficient (%)")
plt.title("Linear Regression: Funding Source vs Proficiency")
plt.grid(True)
plt.tight_layout()
plt.show()
