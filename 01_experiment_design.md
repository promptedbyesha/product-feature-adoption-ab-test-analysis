# 01_experiment_design.md
# Experiment Design Document — Feature Adoption A/B Test

---

## Hypothesis

**H0 (Null):** The new onboarding feature has no effect on 7-day user retention.
**H1 (Alternative):** Users exposed to the new feature will show higher 7-day retention than control.

---

## Background

The product team hypothesizes that an improved in-app feature (e.g., personalized dashboard widget)
will improve early engagement and retention. Before a full rollout, we run a controlled experiment.

---

## Test Design

| Parameter | Value |
|---|---|
| Test type | Two-sample A/B test (randomized) |
| Randomization unit | Individual user (user_id) |
| Control group | Standard experience (no new feature) |
| Test group | New feature enabled |
| Traffic split | 50% control / 50% test |
| Sample size | ~5,000 users |
| Test duration | 14 days exposure + 7-day retention window |

---

## Primary Success Metric

**Day-7 Retention Rate** — proportion of users who return and perform a key action within 7 days of signup.

Formula: retained_day7 users / total users in group

---

## Secondary Metrics

- Feature adoption funnel: seen → clicked → used → retained
- Segment-level lift: new users vs returning users

---

## Minimum Detectable Effect (MDE)

- Baseline retention (control): ~30% for new users, ~52% for returning
- MDE: 5 percentage points (absolute) — i.e., we want to detect a move from 30% → 35%
- Statistical power: 80%
- Significance level (alpha): 0.05 (two-tailed)

At these parameters, required sample size per group ≈ 800 users (calculated via proportion z-test).
Our 5,000-user sample (~1,500+ new users per group) provides well above sufficient power.

---

## Guardrail Metrics

- No significant increase in feature errors or crash rate in test group
- No degradation in session length for returning users

---

## Decision Rules

| Outcome | Decision |
|---|---|
| p < 0.05, lift in both segments | SHIP to all users |
| p < 0.05, lift only in new users | ITERATE — ship for new users, redesign for returning |
| p > 0.05 | DO NOT SHIP — iterate or roll back |
| Negative lift | ROLL BACK immediately |

---

## Segments of Interest

- **New users** (first visit ≤ 7 days): Likely to benefit most from onboarding features
- **Returning users** (first visit > 7 days): Already familiar — feature may be redundant or disruptive

---

## Statistical Test

Chi-square test of proportions (2×2 contingency table):
- Rows: group (control / test)
- Columns: retained (yes / no)
- Reported: chi-square statistic, p-value, 95% confidence interval on lift

---

*Designed before data collection. Updated post-experiment with actual results.*
