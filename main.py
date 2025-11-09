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

