import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main import load_data

# Load cleaned dataset
df = load_data()

# Plot diagram
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
plt.title("Relationship Between Total Capacity and Percent Proficient")
plt.xlabel("Total Capacity")
plt.ylabel("Percent Proficient (%)")
plt.xlim(0, 150)
plt.show()



# Equal-width bins
bins = [0, 25, 50, 100, 200, 400]
labels = ["<25", "25-50", "50-100", "100-200", "200+"]
df["Capacity Group"] = pd.cut(df["Total Capacity"], bins=5, labels=labels)

# Plot average proficiency by group
grouped = df.groupby("Capacity Group")["Percent Proficient"].mean().reset_index()

sns.barplot(x="Capacity Group", y="Percent Proficient", data=grouped)
plt.title("Average Percent Proficient by Capacity Group")
plt.xlabel("Total Capacity Range")
plt.ylabel("Average Percent Proficient (%)")
plt.show()




