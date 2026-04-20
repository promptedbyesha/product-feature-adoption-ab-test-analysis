"""
06_visualizations.py
=====================
Generates all charts needed for the report and Power BI export.

Charts produced:
1. Bar chart — retention rates (control vs test) by user_type
2. Funnel chart — feature adoption funnel (new users vs returning users)
3. Confidence interval plot — lift with 95% CI for each segment
4. Chi-square p-value heatmap (segment × metric)
5. Stacked bar — group composition (new/returning × control/test)

Run AFTER:
python 02_simulate_dataset.py
python 03_statistical_analysis.py
python 05_funnel_analysis.py

Output: outputs/charts/ (PNG files, 300 dpi)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import os

os.makedirs("outputs/charts", exist_ok=True)

# ── Global style ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "font.size":        11,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "grid.linestyle":   "--",
    "figure.dpi":       150,
})

COLORS = {
    "control": "#5B8DB8",   # muted blue
    "test":    "#E07B39",   # warm orange
    "new":     "#4CAF82",   # green
    "returning":"#9B59B6",  # purple
    "neutral": "#AAAAAA",
}

# ── Load data ──────────────────────────────────────────────────────────────────
df       = pd.read_csv("data/ab_test_data.csv")
stats_df = pd.read_csv("outputs/stats_results.csv")
funnel_df= pd.read_csv("outputs/funnel_results.csv")

# ──────────────────────────────────────────────────────────────────────────────
# CHART 1: Retention rates — control vs test, by user_type
# ──────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

user_types = ["new", "returning"]
x = np.arange(len(user_types))
width = 0.35

ctrl_rates = [df[(df["user_type"]==ut)&(df["group"]=="control")]["retained_day7"].mean()
            for ut in user_types]
test_rates = [df[(df["user_type"]==ut)&(df["group"]=="test")]["retained_day7"].mean()
            for ut in user_types]

bars1 = ax.bar(x - width/2, ctrl_rates, width, label="Control", color=COLORS["control"],
            edgecolor="white", linewidth=0.5)
bars2 = ax.bar(x + width/2, test_rates, width, label="Test",    color=COLORS["test"],
            edgecolor="white", linewidth=0.5)

# Annotate bars
for bar, val in zip(list(bars1) + list(bars2), ctrl_rates + test_rates):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f"{val:.1%}", ha="center", va="bottom", fontsize=10, fontweight="bold")

# Significance annotations
for i, ut in enumerate(user_types):
    seg_row = stats_df[stats_df["segment"] == f"{ut.upper()} USERS"].iloc[0]
    label = f"p={seg_row['p_value']:.4f} {'✓' if seg_row['significant'] else '✗'}"
    y_pos = max(ctrl_rates[i], test_rates[i]) + 0.04
    ax.annotate(label, xy=(i, y_pos), ha="center", fontsize=9,
                color="#2ECC71" if seg_row["significant"] else "#E74C3C")

ax.set_xticks(x)
ax.set_xticklabels(["New Users", "Returning Users"], fontsize=12)
ax.set_ylabel("Day-7 Retention Rate")
ax.set_title("A/B Test: Day-7 Retention — Control vs Test\nby User Type", fontsize=13, pad=12)
ax.legend(fontsize=10)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.set_ylim(0, max(max(ctrl_rates), max(test_rates)) + 0.12)
plt.tight_layout()
plt.savefig("outputs/charts/01_retention_by_user_type.png", dpi=300, bbox_inches="tight")
plt.close()
print("Chart 1 saved: 01_retention_by_user_type.png")

# ──────────────────────────────────────────────────────────────────────────────
# CHART 2: Adoption funnel — New vs Returning (test group)
# ──────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
stages_clean = ["Feature\nSeen", "Feature\nClicked", "Feature\nUsed", "Retained\nDay 7"]
stage_keys   = ["1_feature_seen", "2_feature_clicked", "3_feature_used", "4_retained_day7"]

for ax, label, color in zip(axes, ["New users", "Returning users"],
                            [COLORS["new"], COLORS["returning"]]):
    seg = funnel_df[funnel_df["segment"] == label]
    pcts = []
    for sk in stage_keys:
        row = seg[seg["stage"] == sk]
        pcts.append(float(row["pct_of_total"].values[0]) if not row.empty else 0)

    x_pos = np.arange(len(stages_clean))
    bars  = ax.bar(x_pos, pcts, color=color, alpha=0.85, edgecolor="white")

    for bar, val in zip(bars, pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{val:.1%}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Drop-off arrows
    for j in range(len(pcts) - 1):
        drop = pcts[j] - pcts[j+1]
        mid_x = (x_pos[j] + x_pos[j+1]) / 2
        mid_y = (pcts[j] + pcts[j+1]) / 2 + 0.02
        ax.annotate(f"-{drop:.1%}", xy=(mid_x, mid_y), ha="center",
                    fontsize=8.5, color="#E74C3C", style="italic")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(stages_clean, fontsize=10)
    ax.set_title(f"Adoption Funnel — {label} (Test Group)", fontsize=12)
    ax.set_ylabel("% of Test Group Users")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax.set_ylim(0, 1.15)

plt.suptitle("Feature Adoption Funnel", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig("outputs/charts/02_adoption_funnel.png", dpi=300, bbox_inches="tight")
plt.close()
print("Chart 2 saved: 02_adoption_funnel.png")

# ──────────────────────────────────────────────────────────────────────────────
# CHART 3: Confidence interval plot — lift with 95% CI
# ──────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.5))

seg_rows = stats_df[stats_df["segment"].isin(["ALL USERS", "NEW USERS", "RETURNING USERS"])]
labels   = seg_rows["segment"].tolist()
lifts    = seg_rows["absolute_lift"].tolist()
ci_lows  = seg_rows["ci_95_low"].tolist()
ci_highs = seg_rows["ci_95_high"].tolist()
sigs     = seg_rows["significant"].tolist()

y_pos = np.arange(len(labels))
colors_ci = [COLORS["test"] if s else COLORS["neutral"] for s in sigs]

for i, (y, lift, ci_l, ci_h, sig, col) in enumerate(
        zip(y_pos, lifts, ci_lows, ci_highs, sigs, colors_ci)):
    ax.plot([ci_l, ci_h], [y, y], color=col, linewidth=3, solid_capstyle="round")
    ax.scatter([lift], [y], color=col, s=120, zorder=5)
    ax.text(ci_h + 0.002, y, f"+{lift:.1%}  (p={seg_rows.iloc[i]['p_value']:.4f})",
            va="center", fontsize=9.5)

ax.axvline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5, label="No lift (0)")
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=11)
ax.set_xlabel("Absolute Lift in Day-7 Retention (pp)")
ax.set_title("Lift Estimates with 95% Confidence Intervals\n(Test vs Control)", fontsize=13)
ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.set_xlim(-0.04, 0.16)

sig_patch   = mpatches.Patch(color=COLORS["test"],    label="Significant (p < 0.05)")
insig_patch = mpatches.Patch(color=COLORS["neutral"], label="Not significant")
ax.legend(handles=[sig_patch, insig_patch], fontsize=9, loc="lower right")

plt.tight_layout()
plt.savefig("outputs/charts/03_confidence_intervals.png", dpi=300, bbox_inches="tight")
plt.close()
print("Chart 3 saved: 03_confidence_intervals.png")

# ──────────────────────────────────────────────────────────────────────────────
# CHART 4: Retention lift comparison — visual summary
# ──────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))

segments = ["New users\n(Test)", "Returning users\n(Test)",
            "New users\n(Control)", "Returning users\n(Control)"]
ret_vals = [
    df[(df["user_type"]=="new")     & (df["group"]=="test")]["retained_day7"].mean(),
    df[(df["user_type"]=="returning")& (df["group"]=="test")]["retained_day7"].mean(),
    df[(df["user_type"]=="new")     & (df["group"]=="control")]["retained_day7"].mean(),
    df[(df["user_type"]=="returning")& (df["group"]=="control")]["retained_day7"].mean(),
]
bar_colors = [COLORS["test"], COLORS["test"], COLORS["control"], COLORS["control"]]
alphas     = [1.0, 0.6, 1.0, 0.6]

bars = ax.bar(segments, ret_vals, color=bar_colors,
            alpha=1.0, edgecolor="white")
for bar, val, alpha in zip(bars, ret_vals, alphas):
    bar.set_alpha(alpha)
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f"{val:.1%}", ha="center", va="bottom", fontsize=10.5, fontweight="bold")

ax.set_ylabel("Day-7 Retention Rate")
ax.set_title("Retention Rate — All 4 Segments", fontsize=13)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.set_ylim(0, 0.70)

ctrl_patch = mpatches.Patch(color=COLORS["control"], label="Control group")
test_patch = mpatches.Patch(color=COLORS["test"],    label="Test group")
ax.legend(handles=[ctrl_patch, test_patch], fontsize=10)

plt.tight_layout()
plt.savefig("outputs/charts/04_four_segment_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
print("Chart 4 saved: 04_four_segment_comparison.png")

# ──────────────────────────────────────────────────────────────────────────────
# CHART 5: Funnel drop-off waterfall — New users (for Power BI guide)
# ──────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 4.5))

new_test = df[(df["user_type"]=="new") & (df["group"]=="test")]
n = len(new_test)
funnel_vals = [
    n,
    new_test["feature_clicked"].sum(),
    new_test["feature_used"].sum(),
    new_test["retained_day7"].sum(),
]
stage_names = ["Feature Seen\n(All test users)", "Feature Clicked",
            "Feature Used", "Retained Day 7"]

bar_colors_f = [COLORS["new"]] * 3 + [COLORS["test"]]
bars = ax.bar(stage_names, funnel_vals, color=bar_colors_f,
            width=0.6, edgecolor="white", linewidth=0.5)

for bar, val in zip(bars, funnel_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"{val:,}\n({val/n:.1%})", ha="center", va="bottom",
            fontsize=10, fontweight="bold")

# Connector lines
for i in range(len(funnel_vals) - 1):
    x1 = bars[i].get_x()   + bars[i].get_width()
    x2 = bars[i+1].get_x()
    y  = funnel_vals[i+1]
    ax.plot([x1, x2], [y, y], color=COLORS["neutral"], linewidth=1, linestyle="--")

ax.set_ylabel("Number of Users")
ax.set_title(f"Feature Adoption Funnel — New Users, Test Group (n={n:,})", fontsize=12)
ax.set_ylim(0, max(funnel_vals) * 1.20)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.tight_layout()
plt.savefig("outputs/charts/05_funnel_waterfall_new_users.png", dpi=300, bbox_inches="tight")
plt.close()
print("Chart 5 saved: 05_funnel_waterfall_new_users.png")

print("\nAll 5 charts saved to: outputs/charts/")
print("These PNG files can be imported directly into Power BI.")
