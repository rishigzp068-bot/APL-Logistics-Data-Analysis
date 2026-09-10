# APL Logistics Data Analysis

## Machine Learning-Based Late Delivery Risk Prediction in Global Supply Chain Operations

### Project Overview

This project analyzes global supply chain and logistics data to identify factors associated with late deliveries and develop a predictive risk intelligence solution.

The objective is to help logistics and operations teams identify high-risk shipments in advance and take proactive actions to reduce delivery delays.

### Objectives

- Perform data cleaning and exploratory data analysis.
- Identify key factors contributing to late deliveries.
- Engineer meaningful operational features.
- Build machine learning models for late-delivery risk prediction.
- Classify orders into Low, Medium, and High risk categories.
- Analyze regional and shipping-mode risks.
- Develop an interactive Streamlit dashboard.
- Provide actionable recommendations for logistics operations.

### Tools & Technologies

- Python
- Google Colab
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Excel
- Power Query
- SQL / MySQL
- Plotly
- Streamlit
- GitHub

### Project Files

| File | Description |
|---|---|
| `APL_Logistics.xlsx` | Logistics dataset |
| `APL_Logistics EDA .xlsx` | Excel-based exploratory data analysis |
| `APL_Logistics_Analysis.ipynb` | Python analysis and machine learning notebook |
| `APL_Logistics.sql` | SQL analysis and business queries |
| `APL_Logistics_Project_Report.docx` | Final project report |
| `app.py` | Streamlit dashboard |
| `requirements.txt` | Python dependencies |

### Feature Engineering

- Shipping Delay
- Shipping Pressure Index
- High Quantity Flag
- Profit Flag
- Discount Impact
- Shipping Mode Risk Indicators
- Regional Risk Indicators
- Order Complexity Indicators

### Machine Learning

The project includes:

- Logistic Regression
- Random Forest
- Gradient Boosting / XGBoost

Evaluation metrics:

- ROC-AUC
- Precision
- Recall
- F1 Score
- Confusion Matrix

### Streamlit Dashboard

The dashboard provides:

- Delay Risk Overview
- Order-Level Risk Prediction
- Region & Shipping Mode Analysis
- Market Risk Analysis
- High-Risk Order List
- Key Risk Drivers
- Operations Action Panel
- Interactive filters and risk threshold

### Business Value

The project helps logistics teams identify potentially delayed shipments early, prioritize operational resources, monitor risky regions and shipping modes, improve customer communication, and support data-driven supply chain decisions.

### Project Workflow

```text
Raw Logistics Data
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
SQL Analysis
        ↓
Machine Learning
        ↓
Risk Prediction
        ↓
Streamlit Dashboard
        ↓
Operational Recommendations
