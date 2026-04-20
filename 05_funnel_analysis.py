"""
05_funnel_analysis.py
======================
Builds the feature adoption funnel:
feature_seen → feature_clicked → feature_used → retained_day7

Computes:
- Funnel steps for test group (overall + by user_type)
- Drop-off rates at each stage
- Retained rates for users who completed vs skipped each step

Run AFTER: python 02_simulate_dataset.py
Output:    outputs/funnel_results.csv
"""

import pandas as pd
import numpy as np
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/ab_test_data.csv")

# ── Helper: build funnel for a given slice ─────────────────────────────────────
def build_funnel(df_slice: pd.DataFrame, label: str) -> pd.DataFrame:
    """
    Returns a DataFrame with the funnel stages for the given slice.
    Only test group users are relevant for the feature funnel.
    Control group users are shown for context at the 'retained_day7' stage.
    """
    test = df_slice[df_slice["group"] == "test"]
    ctrl = df_slice[df_slice["group"] == "control"]

    n_test = len(test)
    if n_test == 0:
        return pd.DataFrame()

    stages = {
        "1_feature_seen":    test["feature_seen"].sum(),
        "2_feature_clicked": test["feature_clicked"].sum(),
        "3_feature_used":    test["feature_used"].sum(),
        "4_retained_day7":   test["retained_day7"].sum(),
    }

    rows = []
    prev_count = n_test
    for stage, count in stages.items():
        rows.append({
            "segment":          label,
            "stage":            stage,
            "users":            int(count),
            "pct_of_total":     round(count / n_test, 4),
            "pct_of_prev_step": round(count / prev_count, 4) if prev_count > 0 else np.nan,
            "drop_off_pct":     round(1 - count / prev_count, 4) if prev_count > 0 else np.nan,
        })
        prev_count = count

    # Add control retention for comparison
    ctrl_retained = ctrl["retained_day7"].sum()
    rows.append({
        "segment":          f"{label} (CONTROL)",
        "stage":            "4_retained_day7",
        "users":            int(ctrl_retained),
        "pct_of_total":     round(ctrl_retained / len(ctrl), 4) if len(ctrl) > 0 else np.nan,
        "pct_of_prev_step": np.nan,
        "drop_off_pct":     np.nan,
    })

    return pd.DataFrame(rows)

# ── Run funnels ────────────────────────────────────────────────────────────────
all_funnels = []

for label, mask in [
    ("All users",       df["user_type"].isin(["new", "returning"])),
    ("New users",       df["user_type"] == "new"),
    ("Returning users", df["user_type"] == "returning"),
]:
    funnel = build_funnel(df[mask], label)
    all_funnels.append(funnel)

funnel_df = pd.concat(all_funnels, ignore_index=True)
funnel_df.to_csv("outputs/funnel_results.csv", index=False)

# ── Print funnels ──────────────────────────────────────────────────────────────
DIVIDER = "─" * 65

for label in ["All users", "New users", "Returning users"]:
    print(f"\n{'='*65}")
    print(f"  FUNNEL — {label.upper()}")
    print(f"{'='*65}")
    print(f"  {'Stage':<30} {'Users':>7}  {'% of Total':>12}  {'% of Prev':>12}  {'Drop-off':>10}")
    print(DIVIDER)

    seg_funnel = funnel_df[funnel_df["segment"] == label]
    for _, row in seg_funnel.iterrows():
        pct_total = f"{row['pct_of_total']:.1%}" if not pd.isna(row['pct_of_total']) else "—"
        pct_prev  = f"{row['pct_of_prev_step']:.1%}" if not pd.isna(row['pct_of_prev_step']) else "—"
        drop      = f"-{row['drop_off_pct']:.1%}" if not pd.isna(row['drop_off_pct']) else "—"

        stage_clean = row['stage'].replace("_", " ").replace("1 ", "").replace("2 ", "").replace("3 ", "").replace("4 ", "")
        print(f"  {stage_clean:<30} {row['users']:>7}  {pct_total:>12}  {pct_prev:>12}  {drop:>10}")

    # Control comparison row
    ctrl_row = funnel_df[(funnel_df["segment"] == f"{label} (CONTROL)")]
    if not ctrl_row.empty:
        r = ctrl_row.iloc[0]
        pct = f"{r['pct_of_total']:.1%}" if not pd.isna(r['pct_of_total']) else "—"
        print(DIVIDER)
        print(f"  {'CONTROL: retained_day7':<30} {r['users']:>7}  {pct:>12}  {'—':>12}  {'—':>10}")

# ── Additional insight: uplift from feature usage ─────────────────────────────
print(f"\n{'='*65}")
print("  IMPACT OF FEATURE USAGE ON RETENTION (TEST GROUP)")
print(f"{'='*65}")
test_df = df[df["group"] == "test"]

for ut in ["new", "returning"]:
    seg = test_df[test_df["user_type"] == ut]
    used_ret   = seg[seg["feature_used"] == 1]["retained_day7"].mean()
    unused_ret = seg[seg["feature_used"] == 0]["retained_day7"].mean()
    n_used     = (seg["feature_used"] == 1).sum()
    n_unused   = (seg["feature_used"] == 0).sum()

    print(f"\n  [{ut.upper()} USERS — Test group]")
    print(f"  Used feature     (n={n_used:4d}) → Day-7 retention: {used_ret:.1%}")
    print(f"  Did NOT use      (n={n_unused:4d}) → Day-7 retention: {unused_ret:.1%}")
    print(f"  Uplift from use  : {(used_ret - unused_ret):+.1%}")

print(f"\nFunnel results saved to: outputs/funnel_results.csv\n")
