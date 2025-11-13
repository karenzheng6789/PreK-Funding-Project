import csv
import pandas as pd

from sqlalchemy.sql.sqltypes import NULLTYPE

df = pd.read_csv("prek_capacity_2024.csv", delimiter=';')
print(df.head())

preK_names = df["Prek Center Name"].tolist()
license_type = df["License Type"].tolist()
three_year_old_capacity = df["3 Year Old Capacity"].tolist()
four_year_old_capacity = df["4 Year Old Capacity"].tolist()
total_capacity = df["Total Capacity"].tolist()
test_type = df["Test"].tolist()
valid_tests = df["Valid Tests"].tolist()
proficient_tests = df["Proficient Tests"].tolist()
percent_proficient = df["Percent Proficient"].tolist()
funding_source = df["Funding Source"].tolist()
city_council_district = df["City Council District"].tolist()
commission_district = df["Commission District"].tolist()
super_district = df["Super District"].tolist()

total_capacity = pd.to_numeric(df["Total Capacity"])
proficient_tests = pd.to_numeric(df["Percent Proficient"])

# Question 3

# Correlation between the funding source of
# Pre-K programs in Memphis and student proficiency in reading/writing?

# Preprocessing
df = df.dropna(subset=["Percent Proficient", "Funding Source", "Total Capacity"]) # remove missing data

# Visualization
order = df.groupby("Funding Source")["Percent Proficient"].mean().sort_values().index

plt.figure(figsize=(10, 5))
plt.boxplot(
    [df.loc[df["Funding Source"] == fs, "Percent Proficient"].dropna() for fs in order],
    labels=order,
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

# Density-based clustering (DBSCAN)

# Synthesis & Interpretation

# Outlier Detection

# Quick report
print("\nSUMMARY REPORT")
print(f"Total Schools Analyzed: {len(df)}")
print(f"Funding Types Compared: {df['Funding Source'].nunique()}")
print(f"Highest Performing Funding Source: {funding_summary.index[0]} ({funding_summary['mean'].iloc[0]:.2f}% proficient)")
print(f"Lowest Performing Funding Source: {funding_summary.index[-1]} ({funding_summary['mean'].iloc[-1]:.2f}% proficient)")

