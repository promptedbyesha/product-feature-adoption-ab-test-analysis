"""
03_statistical_analysis.py
===========================
Performs chi-square test of proportions on the A/B test dataset.
Reports: p-value, chi-square stat, 95% confidence interval on absolute lift,
relative lift %, and significance verdict.

Run AFTER: python 02_simulate_dataset.py
Output:    outputs/stats_results.csv
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, norm
import os

os.makedirs("outputs", exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("data/ab_test_data.csv")

# ── Helper: run chi-square + compute CI on lift ───────────────────────────────
def analyze_segment(df_seg: pd.DataFrame, label: str) -> dict:
    """
    Runs a 2x2 chi-square test for a given dataframe segment.
    Returns a dict of all relevant stats.
    """
    ctrl  = df_seg[df_seg["group"] == "control"]
    test  = df_seg[df_seg["group"] == "test"]

    n_ctrl  = len(ctrl)
    n_test  = len(test)
    r_ctrl  = ctrl["retained_day7"].sum()
    r_test  = test["retained_day7"].sum()

    p_ctrl  = r_ctrl / n_ctrl
    p_test  = r_test / n_test

    # ── 2x2 Contingency table ─────────────────────────────────────────────────
    # Rows = [control, test], Cols = [retained, not_retained]
    contingency = np.array([
        [r_ctrl,  n_ctrl - r_ctrl],
        [r_test,  n_test  - r_test],
    ])
    chi2, p_value, dof, expected = chi2_contingency(contingency, correction=False)

    # ── Absolute lift & 95% CI ────────────────────────────────────────────────
    # Wilson-score-based CI on the difference of proportions
    abs_lift = p_test - p_ctrl
    se = np.sqrt(p_ctrl * (1 - p_ctrl) / n_ctrl + p_test * (1 - p_test) / n_test)
    z_95 = norm.ppf(0.975)
    ci_low  = abs_lift - z_95 * se
    ci_high = abs_lift + z_95 * se

    # ── Relative lift ─────────────────────────────────────────────────────────
    rel_lift = abs_lift / p_ctrl if p_ctrl > 0 else np.nan

    # ── Verdict ───────────────────────────────────────────────────────────────
    significant = p_value < 0.05
    verdict = "SIGNIFICANT ✓" if significant else "NOT SIGNIFICANT ✗"

    return {
        "segment":          label,
        "n_control":        n_ctrl,
        "n_test":           n_test,
        "retained_control": r_ctrl,
        "retained_test":    r_test,
        "retention_ctrl":   round(p_ctrl, 4),
        "retention_test":   round(p_test, 4),
        "absolute_lift":    round(abs_lift, 4),
        "relative_lift_pct":round(rel_lift * 100, 2),
        "ci_95_low":        round(ci_low, 4),
        "ci_95_high":       round(ci_high, 4),
        "chi2_stat":        round(chi2, 4),
        "p_value":          round(p_value, 6),
        "dof":              int(dof),
        "significant":      significant,
        "verdict":          verdict,
    }

# ── Run analyses ──────────────────────────────────────────────────────────────
results = []

# 1. Overall (all users)
results.append(analyze_segment(df, "ALL USERS"))

# 2. New users only
results.append(analyze_segment(df[df["user_type"] == "new"], "NEW USERS"))

# 3. Returning users only
results.append(analyze_segment(df[df["user_type"] == "returning"], "RETURNING USERS"))

# ── Save results ──────────────────────────────────────────────────────────────
results_df = pd.DataFrame(results)
results_df.to_csv("outputs/stats_results.csv", index=False)

# ── Pretty print ──────────────────────────────────────────────────────────────
DIVIDER = "=" * 65

for r in results:
    print(DIVIDER)
    print(f"  SEGMENT: {r['segment']}")
    print(DIVIDER)
    print(f"  Sample size       : Control={r['n_control']}, Test={r['n_test']}")
    print(f"  Retained (Control): {r['retained_control']}  ({r['retention_ctrl']:.1%})")
    print(f"  Retained (Test)   : {r['retained_test']}  ({r['retention_test']:.1%})")
    print()
    print(f"  Absolute lift     : {r['absolute_lift']:+.1%}")
    print(f"  Relative lift     : {r['relative_lift_pct']:+.1f}%")
    print(f"  95% CI            : [{r['ci_95_low']:.1%}, {r['ci_95_high']:.1%}]")
    print()
    print(f"  Chi-square stat   : {r['chi2_stat']}")
    print(f"  p-value           : {r['p_value']}")
    print(f"  Degrees of freedom: {r['dof']}")
    print()
    print(f"  ► VERDICT         : {r['verdict']}")
    print()

print(DIVIDER)
print("Results saved to: outputs/stats_results.csv")
print(DIVIDER)

# ── Interpretation guide ──────────────────────────────────────────────────────
print("""
INTERPRETATION NOTES
──────────────────────────────────────────────────
p-value < 0.05  → Reject H0. The difference is unlikely by chance.
p-value ≥ 0.05  → Fail to reject H0. No statistically significant effect.

Absolute lift   → Direct percentage-point change in retention.
                e.g., 28% → 34.5% = +6.5pp absolute lift
Relative lift   → Lift as % of baseline.
                e.g., +6.5pp on 28% base = +23.2% relative lift
95% CI          → If this range does NOT include 0, the lift is significant.

Chi-square test → Tests whether the distribution of retained/not-retained
                differs significantly between control and test groups.
──────────────────────────────────────────────────
""")
