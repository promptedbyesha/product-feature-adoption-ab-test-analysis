"""
04_segmentation_analysis.py
============================
Deep-dive segmentation of the A/B test results:
- New vs returning users (primary)
- Device breakdown
- Region breakdown
- Interaction check: user_type × group

Run AFTER: python 02_simulate_dataset.py
Output:    outputs/segment_results.csv
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, norm
import os

os.makedirs("outputs", exist_ok=True)

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/ab_test_data.csv")

# ── Reuse the analysis helper ─────────────────────────────────────────────────
def quick_stats(df_seg: pd.DataFrame, label: str) -> dict:
    ctrl = df_seg[df_seg["group"] == "control"]
    test = df_seg[df_seg["group"] == "test"]
    if len(ctrl) == 0 or len(test) == 0:
        return None

    n_c, n_t = len(ctrl), len(test)
    r_c = ctrl["retained_day7"].sum()
    r_t = test["retained_day7"].sum()
    p_c = r_c / n_c
    p_t = r_t / n_t

    contingency = np.array([[r_c, n_c - r_c], [r_t, n_t - r_t]])
    chi2, p_val, _, _ = chi2_contingency(contingency, correction=False)

    abs_lift = p_t - p_c
    se = np.sqrt(p_c*(1-p_c)/n_c + p_t*(1-p_t)/n_t)
    z95 = norm.ppf(0.975)

    return {
        "segment":          label,
        "n_control":        n_c,
        "n_test":           n_t,
        "retention_ctrl":   round(p_c, 4),
        "retention_test":   round(p_t, 4),
        "absolute_lift":    round(abs_lift, 4),
        "relative_lift_pct":round((abs_lift / p_c) * 100, 2) if p_c > 0 else np.nan,
        "ci_low":           round(abs_lift - z95*se, 4),
        "ci_high":          round(abs_lift + z95*se, 4),
        "p_value":          round(p_val, 6),
        "significant":      p_val < 0.05,
    }

rows = []

# ──────────────────────────────────────────────────────────────────────────────
# 1.  PRIMARY: New vs Returning
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("1. PRIMARY SEGMENTATION: new vs returning")
print("="*60)

for ut in ["new", "returning"]:
    r = quick_stats(df[df["user_type"] == ut], f"user_type={ut}")
    rows.append(r)
    print(f"\n  [{ut.upper()} USERS]")
    print(f"  Control retention : {r['retention_ctrl']:.1%}")
    print(f"  Test retention    : {r['retention_test']:.1%}")
    print(f"  Absolute lift     : {r['absolute_lift']:+.1%}")
    print(f"  Relative lift     : {r['relative_lift_pct']:+.1f}%")
    print(f"  95% CI            : [{r['ci_low']:.1%}, {r['ci_high']:.1%}]")
    print(f"  p-value           : {r['p_value']}")
    print(f"  Significant?      : {'YES ✓' if r['significant'] else 'NO ✗'}")

# ──────────────────────────────────────────────────────────────────────────────
# 2.  DEVICE BREAKDOWN
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. DEVICE BREAKDOWN")
print("="*60)

for device in df["device"].unique():
    r = quick_stats(df[df["device"] == device], f"device={device}")
    if r:
        rows.append(r)
        sig = "✓" if r["significant"] else "✗"
        print(f"  {device:10s} | ctrl={r['retention_ctrl']:.1%}  test={r['retention_test']:.1%}"
            f"  lift={r['relative_lift_pct']:+.1f}%  p={r['p_value']:.4f}  {sig}")

# ──────────────────────────────────────────────────────────────────────────────
# 3.  REGION BREAKDOWN
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. REGION BREAKDOWN")
print("="*60)

for region in df["region"].unique():
    r = quick_stats(df[df["region"] == region], f"region={region}")
    if r:
        rows.append(r)
        sig = "✓" if r["significant"] else "✗"
        print(f"  {region:8s} | ctrl={r['retention_ctrl']:.1%}  test={r['retention_test']:.1%}"
            f"  lift={r['relative_lift_pct']:+.1f}%  p={r['p_value']:.4f}  {sig}")

# ──────────────────────────────────────────────────────────────────────────────
# 4.  CROSS: user_type × device (for new users only)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. NEW USERS × DEVICE (interaction check)")
print("="*60)

new_df = df[df["user_type"] == "new"]
for device in new_df["device"].unique():
    r = quick_stats(new_df[new_df["device"] == device], f"new+{device}")
    if r:
        rows.append(r)
        sig = "✓" if r["significant"] else "✗"
        print(f"  new+{device:10s} | ctrl={r['retention_ctrl']:.1%}  test={r['retention_test']:.1%}"
            f"  lift={r['relative_lift_pct']:+.1f}%  p={r['p_value']:.4f}  {sig}")

# ──────────────────────────────────────────────────────────────────────────────
# 5.  OVERALL SUMMARY TABLE
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. OVERALL RETENTION SUMMARY (by group × user_type)")
print("="*60)
summary = (df.groupby(["user_type", "group"])["retained_day7"]
            .agg(total="count", retained="sum", rate="mean")
            .round({"rate": 3}))
print(summary.to_string())

# ── Save ──────────────────────────────────────────────────────────────────────
seg_df = pd.DataFrame([r for r in rows if r is not None])
seg_df.to_csv("outputs/segment_results.csv", index=False)
print(f"\nSegment results saved to: outputs/segment_results.csv")

# ──────────────────────────────────────────────────────────────────────────────
# 6.  KEY INSIGHT CALL-OUT
# ──────────────────────────────────────────────────────────────────────────────
new_r = quick_stats(df[df["user_type"] == "new"], "new")
ret_r = quick_stats(df[df["user_type"] == "returning"], "ret")

print("""
╔══════════════════════════════════════════════════════════════╗
║                    KEY INSIGHT                               ║
╠══════════════════════════════════════════════════════════════╣""")
print(f"║  New users     : +{new_r['relative_lift_pct']:.1f}% lift   p={new_r['p_value']:.4f}   {'SIGNIFICANT ✓' if new_r['significant'] else 'NOT SIGNIFICANT ✗':<20}║")
print(f"║  Returning     : +{ret_r['relative_lift_pct']:.1f}% lift   p={ret_r['p_value']:.4f}   {'SIGNIFICANT ✓' if ret_r['significant'] else 'NOT SIGNIFICANT ✗':<20}║")
print("""╠══════════════════════════════════════════════════════════════╣
║  DECISION: SHIP for new users, ITERATE for returning users   ║
╚══════════════════════════════════════════════════════════════╝
""")
