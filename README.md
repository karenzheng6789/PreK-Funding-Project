# Data Mining Study of Pre-K Literacy in Memphis
**Examining the Effects of Capacity, Funding Source, Licensing Type, and Geopraphic District**

**Authors**
Karen Zheng - zheka-26@rhodes.edu
Aiden Nguyen - nguhn1-27@rhodes.edu

---

## Project Overview
Early childhood literacy proficiency is a strong predictor of long-term academic success, yet large disparities persist across Pre-K programs in Memphis and the Mid-South.  
This project applies **data mining and statistical analysis techniques** to evaluate whether **funding source, licensing type, program capacity, and geographic district** are associated with differences in early literacy proficiency across Pre-K centers.

Using open data from **DataMidSouth**, we performed data cleaning, exploratory data analysis, regression modeling, clustering, and hypothesis testing to identify which structural factors most strongly relate to early learning outcomes.

---

## Research Questions
- - Does total program capacity correlate with literacy proficiency?
- Does funding source predict proficiency outcomes?
- Do Commission Districts differ significantly in proficiency performance?
- Does licensing type (DOE, DHS, Unlicensed) influence proficiency?

---

## Dataset
**Source:** DataMidSouth Open Data Portal  
- *Pre-K Capacity 2024 Dataset*  
- *First 8 Memphis Pre-K Capacity Overview*

--- 

**Scope:**
- 300+ original Pre-K centers across the Mid-South
- 194 centers retained after preprocessing with complete proficiency and capacity data

**Key Features:**
- Total Capacity (3- and 4-year-old enrollment)
- Percent Proficient
- Funding Source
- Licensing Type
- Commission District
- Geographic attributes (ZIP code, latitude, longitude)

---

## Data Cleaning & Preprocessing
- Parsed malformed CSV files with inconsistent delimiters
- Converted numeric fields from strings to numeric data types
- Removed records with missing proficiency values
- Filtered dataset to centers with complete capacity and proficiency data

---

## Methods
- **Exploratory Data Analysis (EDA)**  
  Boxplots, bar charts, and scatter plots
- **Linear Regression**  
  - Capacity vs. proficiency  
  - Encoded funding source vs. proficiency
- **K-Means Clustering (k = 3)**  
  - Capacity and proficiency  
  - Funding source and proficiency
- **Geographic Analysis**  
  Commission District comparisons
- **Statistical Testing**  
  One-way ANOVA to test district-level differences

---

## Key Findings
- **Program capacity does not predict literacy proficiency**
- **Funding source alone does not meaningfully predict outcomes**
- **Commission District is the strongest predictor of proficiency**
- Districts 1–4 consistently outperform Districts 5–13
- Licensing comparisons were limited due to missing proficiency data for non-DOE centers
![Average Literacy Proficiency by Commission District](figures/avg_proficiency_by_district.png)
---

## Interpretation
Higher-performing districts align with areas of higher median household income, tax revenue, and access to licensed Pre-K programs.  
Lower-performing districts show reduced access to assessment coverage and early education resources, highlighting structural and geographic inequities rather than differences driven by funding labels or center size.

---

## Conclusions
This study suggests that **geographic and structural factors play a larger role in early literacy outcomes** than funding source, licensing type, or program capacity alone.  
Future analyses should expand assessment coverage across all licensing types and examine classroom-level factors such as curriculum quality and teacher qualifications.

---

## Tech Stack
- **Python**
- pandas, NumPy
- matplotlib, seaborn
- scikit-learn
- SciPy / statsmodels
- Jupyter Notebook

## 📄 Full Report
A detailed academic report with full statistical results and figures is available here:  
**[Data Mining Study of Pre-K Literacy in Memphis – Full Report](report/PreK_Literacy_Data_Mining_Report.pdf)**

