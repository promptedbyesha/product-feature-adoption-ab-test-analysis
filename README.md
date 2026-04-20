# 📊 Product Feature Adoption & A/B Test Analysis

## Overview
Simulated and analyzed a randomized A/B test to measure the impact of a new
in-app feature on 7-day user retention. Segmented results by new vs returning
users and delivered a data-backed ship/iterate decision memo.

## Key Finding
- New users: **+23.7% relative lift** in Day-7 retention (p = 0.000046) ✓ Significant
- Returning users: +5.9% lift (p = 0.179) ✗ Not significant
- Decision: **Ship for new users. Iterate for returning users.**

---

## 📈 Dashboard Preview



---

## 🧪 Methodology

- A/B testing with **Control vs Test groups**
- **Chi-square hypothesis testing**
- **95% Confidence Intervals (CI)**
- Segmentation analysis across:
  - User type (new vs returning)
  - Device (desktop, mobile, tablet)
  - Region
- Funnel analysis for feature adoption behavior

---

## 📊 Key Metrics Tracked

- Retention rate (control vs test)
- Absolute lift
- Relative lift (%)
- p-value (statistical significance)
- Chi-square statistic
- Confidence intervals (CI)

---

## 📊 Dashboard Structure (Power BI)

### 1. Executive Summary
- KPI cards (Retention lift, p-value, relative lift)
- Retention comparison chart
- Decision callout

### 2. Statistical Deep Dive
- Segment-wise statistical results
- Significance visualization
- Confidence interval interpretation

### 3. Segmentation Breakdown
- Performance across devices and regions
- Interactive filters (device, region)
- Highlight: highest lift segment

### 4. Adoption Funnel
- Feature usage funnel (New vs Returning users)
- Impact of feature usage on retention

---

## 🛠 Tools & Technologies

- **Python** → Data simulation & statistical analysis  
- **Power BI** → Dashboard & visualization  
- **CSV / Excel** → Data handling  
- **Git & GitHub** → Version control  

---

## Project Structure
| File_Type | File_Name | Description |
| --- | --- | --- |
| Directory | P2_AB_Test_Analysis/ | Main project directory |
| File | ab_test_data.csv | 5000-row simulated dataset |
| Directory | outputs/ | Output results directory |
| File | stats_results.csv | Chi-square results + p-values |
| File | segment_results.csv | New vs returning + device + region |
| File | funnel_results.csv | Adoption funnel data |
| File | 01_experiment_design.md | Hypothesis + test design |
| File | 02_simulate_dataset.py | Data generation script |
| File | 03_statistical_analysis.py | Chi-square + CI analysis |
| File | 04_segmentation_analysis.py | Segment breakdown |
| File | 05_funnel_analysis.py | Funnel drop-off analysis |
| File | 06_visualizations.py | All chart exports |
| File | 07_decision_memo.md | Ship/iterate recommendation |
## How to Run
```bash
pip install pandas scipy matplotlib numpy
python 02_simulate_dataset.py
python 03_statistical_analysis.py
python 04_segmentation_analysis.py
python 05_funnel_analysis.py
python 06_visualizations.py
```


## 🚀 How to Use Dashboard

1. Download the `.pbix` file  
2. Open in Power BI Desktop  
3. Explore the dashboard interactively  

---

## 📌 Key Learning

Statistical significance is critical in product decisions.  
A visible lift in metrics does not always imply a meaningful impact — **validation through hypothesis testing is essential**.

---
## Results Summary

| Segment | Control | Test | Lift | p-value | Significant |
|---|---|---|---|---|---|
| All users | 38.0% | 43.4% | +14.2% | 0.0001 | ✓ |
| New users | 29.5% | 36.5% | +23.7% | 0.000046 | ✓ |
| Returning users | 50.8% | 53.8% | +5.9% | 0.179 | ✗ |
---

## 🔗 Connect

If you found this project interesting or have feedback, feel free to connect or reach out!

