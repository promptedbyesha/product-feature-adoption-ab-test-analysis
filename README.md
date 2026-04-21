# 📊 Product Feature Adoption & A/B Test Analysis
> Most A/B tests answer one question: *Did the feature work?*  
> This project answers a better one: **For whom did it work, and should you ship it?**

A new product feature showed a clear lift in retention at the aggregate level.  
But segmentation revealed a critical nuance:

👉 It significantly improved retention for **new users**  
👉 It had **no meaningful impact** on returning users  

Instead of a blanket rollout, this analysis leads to a **targeted product decision**:
**Ship where it works. Iterate where it doesn’t.**

📖 [Full Case Study on Notion](https://eshasharma.notion.site/Product-Feature-Adoption-A-B-Test-Analysis-34899496b51c80f88bb8f09bd396ac0c?source=copy_link)

---

### 🎯 What to Expect

This project walks through a complete, real-world A/B testing workflow:

- Designing a controlled experiment with a clear hypothesis  
- Simulating realistic product data (~5,000 users)  
- Running statistical tests (chi-square, p-value, confidence intervals)  
- Segmenting results to uncover hidden insights  
- Analyzing feature adoption through a retention funnel  
- Delivering a **decision memo** backed by data  

> **End result:** Not just analysis — a defensible product decision backed by chi-square testing, confidence intervals, and segment-level evidence.

---
## 📌 Overview

Designed and analyzed a full A/B experiment on product feature adoption, from hypothesis design to statistical testing to a segmented ship/iterate decision memo, using Python (pandas, scipy) and Power BI. The dataset was simulated in Python to reflect realistic product behavior patterns across 5,000 users.

---

## 📑 Key Finding
- New users showed a **statistically significant lift** in Day-7 retention ✓
- Returning users showed **no meaningful impact** ✗
- Decision: **Ship for new users. Iterate for returning users.**

→ Full numbers and p-values in the [Results Summary](#results-summary) below.
## 🎯 Final Decision

This analysis goes beyond measuring uplift — it evaluates **where**, **for whom**, and **whether** the feature should be shipped.

- ✅ Ship for new users  
- ⚠ Iterate for returning users  
- ❌ Do not roll out universally without segmentation  

This ensures data-driven and context-aware product decisions.


---
## 🧪 **Experiment Design**

This experiment simulates a controlled A/B test to evaluate the impact of a new product feature on 7-day user retention.

- **Hypothesis:** The new feature improves Day-7 retention
- **Control Group:** Users without feature exposure
- **Test Group:** Users exposed to the feature
- **Primary Metric:** Day-7 retention rate
- **Minimum Detectable Effect (MDE):** ~5% absolute lift  
  (Chosen as a practically meaningful improvement for product decisions)

## 📋 Assumptions

- Users are randomly assigned to control and test groups  
- Observations are independent across users  
- Sample size (~5000 users) is sufficient for chi-square test validity  
- No major external factors influencing user behavior during the experiment  

These assumptions ensure the statistical results are valid and interpretable.

## 📈 Statistical Interpretation

- **New Users:**  
  95% CI: [+3.6pp, +10.4pp]  
  → Does NOT include zero → effect is statistically significant  

- **Returning Users:**  
  95% CI: [-1.4pp, +7.4pp]  
  → Includes zero → effect is NOT statistically distinguishable from no impact  

This confirms that the observed lift for new users is reliable, while for returning users it may be due to random variation.

---
## 💡Business Impact

- A +23.7% relative lift in retention for new users suggests strong early-stage engagement improvement  
- If scaled, this could significantly increase user activation and long-term retention (LTV)  
- No significant impact on returning users indicates the feature may not improve behavior for already engaged users  
 
👉 Strategic takeaway:  
A targeted rollout — rather than a universal one — maximizes growth impact while preserving the opportunity to improve the experience for returning users.

---
## 🔎 Deeper Product Insight

Although users who engage with the feature show higher retention, the overall effect for returning users is not statistically significant.

This suggests:
- Possible behavioral differences between new and returning users  
- Feature may be more effective during onboarding than for habitual usage  
- Potential selection bias — more engaged users are more likely to use the feature
  
👉 Key takeaway:  
Not all statistically significant results translate into universal product wins, segmentation is critical to avoid misleading aggregate conclusions. 

👉 Implication:  
The feature is likely an **activation driver**, not a **retention enhancer** for mature users.

---
## 📊 Dashboard Structure (Power BI)

- **Executive Summary:** Key metrics, retention lift, final decision  
- **Statistical Deep Dive:** Significance testing, p-values, confidence intervals  
- **Segmentation Breakdown:** Performance by user type, device, and region  
- **Adoption Funnel:** Feature usage flow and retention impact
  
---

## 📈 Dashboard Preview

### Executive Summary
![Executive Dashboard](images/dashboard-executive.png)

### Statistical Deep Dive
![Statistical Dashboard](images/dashboard-statistical.png)

### Segmentation Breakdown
![Segmentation Dashboard](images/dashboard-segmentation.png)

### Adoption Funnel
![Funnel Dashboard](images/dashboard-funnel.png)

---

## 📊 Explore the Dashboard

**🔎 Quick view (no setup needed):**  
👉 [View Dashboard as PDF](./outputs/AB_Test_Dashboard.pdf)  
*A static snapshot to quickly understand the key insights and final decision*

**💻 Interactive analysis (recommended):**  
👉 [Download Power BI File (.pbix)](https://drive.google.com/file/d/1uTDF4gmt2eBWq7VLDVz7wvWJI9ZE8Fr7/view?usp=sharing)  
*Open in Power BI Desktop to explore filters, segments, and drilldowns on your own system*

---
## 🚀 How to Explore the Dashboard

If you're new to Power BI, follow this:

1. Download the `.pbix` file from the link above  
2. Open it using **Power BI Desktop** (free to install)  
3. Use filters (device, region, user type) to explore segments  
4. Navigate across 4 pages:
   - Executive Summary → key decision
   - Statistical Deep Dive → significance & confidence
   - Segmentation → where the feature works
   - Funnel → how users adopt the feature  

💡 Tip: Start with the **Executive Summary**, then drill down into segments.

---


## 🛠 Tools & Technologies
- ![Python](https://img.shields.io/badge/Python-3.12-blue)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)
![pandas](https://img.shields.io/badge/pandas-2.0-green)
![scipy](https://img.shields.io/badge/scipy-stats-orange)

- **Python** → Data simulation, statistical analysis, and chart exports  
- **pandas + numpy** → Data manipulation and dataset generation  
- **scipy** → Chi-square hypothesis testing and confidence interval calculation  
- **matplotlib** → Data visualization and chart exports  
- **Power BI** → Interactive 4-page dashboard and data storytelling  
- **Excel / CSV** → Data validation, output review, and tabular analysis  
- **Git + GitHub** → Version control and project documentation  


---

## Project Structure
| Type  | File | Description |
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

---

## ⚠ Limitations & Next Steps

**Limitations**
- Simulated dataset may not capture full real-world variability  
- External factors (seasonality, product changes) not modeled  
- Feature exposure treated as binary (not depth of usage)

**Next Steps**
- Validate results on real production data  
- Test redesigned feature for returning users  
- Analyze longer-term retention (Day-14 / Day-30)  
- Improve feature discoverability for new users  

👉 Goal: evolve from **insight → experimentation → product strategy**

---
## Results Summary

| Segment | Control | Test | Lift | p-value | Significant |
|---|---|---|---|---|---|
| All users | 38.0% | 43.4% | +14.2% | 0.0001 | ✓ |
| New users | 29.5% | 36.5% | +23.7% | 0.000046 | ✓ |
| Returning users | 50.8% | 53.8% | +5.9% | 0.179 | ✗ |
---

## 🤝 Let’s Connect

Interested in product analytics, experimentation, or data-driven product decisions?  
I’m always open to meaningful conversations, feedback, or collaboration opportunities.

- LinkedIn: https://www.linkedin.com/in/workwitheesha/
- Email: workwitheesha@gmail.com
- 🗂 Portfolio: [Notion Case Study](https://eshasharma.notion.site/Product-Feature-Adoption-A-B-Test-Analysis-34899496b51c80f88bb8f09bd396ac0c?source=copy_link)


