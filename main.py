import csv

from sqlalchemy.sql.sqltypes import NULLTYPE

preK_names = []
license_type = []
three_year_old_capacity = []
four_year_old_capacity = []
total_capacity = []
test = []
grade_and_subject = []
valid_tests = []
proficient_tests = []
percent_proficient = []
funding_source = []
city_council_district = []
commission_district = []
super_district = []

with open("prek_capacity_2024.csv", "r", newline="") as prek_file:
    for line in prek_file:
        line.strip()
        parts = line.split(";")
        print(parts)
        for i in parts:
            #if parts[i] != "-" :
            preK_names.append(parts[0])


