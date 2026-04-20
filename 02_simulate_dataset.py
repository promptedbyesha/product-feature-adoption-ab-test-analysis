"""
02_simulate_dataset.py
======================
Generates a realistic A/B test dataset (~5000 rows) for feature adoption analysis.

Story baked into the data:
- New users  → test group shows ~21-28% lift in Day-7 retention (significant)
- Returning users → test group shows ~2-4% lift (NOT significant)
- Funnel has realistic drop-off rates

Run: python 02_simulate_dataset.py
Output: data/ab_test_data.csv
"""

import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

# ── Reproducibility ──────────────────────────────────────────────────────────
SEED = 42
rng = np.random.default_rng(SEED)

# ── Output path ──────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)

# ── Parameters ───────────────────────────────────────────────────────────────
N_TOTAL        = 5000
NEW_USER_FRAC  = 0.60          # 60% new, 40% returning

# Retention rates by (user_type, group)
RETENTION = {
    ("new",       "control"): 0.28,
    ("new",       "test"):    0.345,   # ~23% relative lift
    ("returning", "control"): 0.52,
    ("returning", "test"):    0.535,   # ~2.9% relative lift → NOT significant
}

# Funnel rates (conditional probabilities for TEST group; control is slightly lower)
# feature_seen is 1 for all test users (they get it), 0 for all control users
# For test users: seen=1 always; clicked | seen ~ 0.45; used | clicked ~ 0.62
# For control:    seen=0 always (no feature); clicked/used = 0 always
CLICK_RATE_NEW_TEST       = 0.48
CLICK_RATE_RETURNING_TEST = 0.41
USE_RATE_GIVEN_CLICK      = 0.62

DEVICES  = ["mobile", "desktop", "tablet"]
DEV_PROB = [0.55, 0.35, 0.10]
REGIONS  = ["north", "south", "east", "west"]
REG_PROB = [0.30, 0.25, 0.25, 0.20]

START_DATE = datetime(2024, 6, 1)
END_DATE   = datetime(2024, 6, 14)

# ── Build rows ────────────────────────────────────────────────────────────────
rows = []

n_new       = int(N_TOTAL * NEW_USER_FRAC)
n_returning = N_TOTAL - n_new

for user_type, n in [("new", n_new), ("returning", n_returning)]:
    for group in ["control", "test"]:
        n_group = n // 2  # 50/50 split

        for i in range(n_group):
            uid = f"U_{user_type[0].upper()}_{group[0].upper()}_{i:04d}"

            # ── Signup date ──────────────────────────────────────────────────
            delta = rng.integers(0, (END_DATE - START_DATE).days)
            signup_date = (START_DATE + timedelta(days=int(delta))).strftime("%Y-%m-%d")

            # ── Device & region ──────────────────────────────────────────────
            device = rng.choice(DEVICES, p=DEV_PROB)
            region = rng.choice(REGIONS, p=REG_PROB)

            # ── Funnel flags ─────────────────────────────────────────────────
            if group == "test":
                feature_seen = 1
                click_rate = (CLICK_RATE_NEW_TEST if user_type == "new"
                            else CLICK_RATE_RETURNING_TEST)
                feature_clicked = int(rng.random() < click_rate)
                feature_used    = int(feature_clicked and rng.random() < USE_RATE_GIVEN_CLICK)
            else:
                feature_seen    = 0
                feature_clicked = 0
                feature_used    = 0

            # ── Retention ────────────────────────────────────────────────────
            ret_prob = RETENTION[(user_type, group)]

            # Small boost if user actually used the feature
            if feature_used:
                ret_prob = min(ret_prob + 0.08, 0.95)

            retained_day7 = int(rng.random() < ret_prob)

            rows.append({
                "user_id":        uid,
                "group":          group,
                "user_type":      user_type,
                "feature_seen":   feature_seen,
                "feature_clicked":feature_clicked,
                "feature_used":   feature_used,
                "retained_day7":  retained_day7,
                "signup_date":    signup_date,
                "device":         device,
                "region":         region,
            })

df = pd.DataFrame(rows)

# ── Shuffle rows (so it's not ordered by group) ───────────────────────────────
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = "data/ab_test_data.csv"
df.to_csv(out_path, index=False)

# ── Quick sanity check ────────────────────────────────────────────────────────
print("=" * 55)
print("DATASET GENERATED SUCCESSFULLY")
print("=" * 55)
print(f"Shape         : {df.shape}")
print(f"Output file   : {out_path}")
print()
print("Group split:")
print(df.groupby(["user_type", "group"]).size().to_string())
print()
print("Day-7 retention rates:")
summary = (df.groupby(["user_type", "group"])["retained_day7"]
            .agg(["sum", "count", "mean"])
            .rename(columns={"sum": "retained", "count": "total", "mean": "rate"}))
summary["rate"] = summary["rate"].round(3)
print(summary.to_string())
print()
print("Funnel (test group only):")
test_df = df[df["group"] == "test"]
print(f"  feature_seen    : {test_df['feature_seen'].mean():.1%}")
print(f"  feature_clicked : {test_df['feature_clicked'].mean():.1%} of all test users")
print(f"  feature_used    : {test_df['feature_used'].mean():.1%} of all test users")
print(f"  retained_day7   : {test_df['retained_day7'].mean():.1%} of all test users")
print()
print("Columns:", list(df.columns))
