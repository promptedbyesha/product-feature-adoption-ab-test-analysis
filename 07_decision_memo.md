# Decision Memo — Feature Adoption A/B Test
## SHIP / ITERATE / ROLL BACK Recommendation

**To:** Product Leadership  
**From:** Product Analyst  
**Date:** [Insert date]  
**Re:** New Feature — 7-Day Retention A/B Test Results

---

## Recommendation: ITERATE → SHIP FOR NEW USERS, REDESIGN FOR RETURNING

**Short version:** The feature significantly improves Day-7 retention for new users
(~23% relative lift, p < 0.05). It shows no meaningful effect on returning users.
We recommend an immediate phased rollout to new users, while iterating the experience
for returning users before expanding.

---

## What We Tested

We ran a randomized A/B test exposing 50% of users to a new in-app feature (test group)
versus the standard experience (control group). Success metric: Day-7 retention rate.
Total sample: ~5,000 users. Experiment duration: 14-day exposure window.

---

## Results Summary

| Segment | Control Retention | Test Retention | Absolute Lift | Relative Lift | p-value | Significant? |
|---|---|---|---|---|---|---|
| All users | ~32% | ~37% | +5pp | +16% | < 0.05 | ✓ YES |
| **New users** | **~28%** | **~34.5%** | **+6.5pp** | **+23%** | **< 0.05** | **✓ YES** |
| Returning users | ~52% | ~53.5% | +1.5pp | +3% | > 0.05 | ✗ NO |

*95% CI for new users: [+3.5pp, +9.5pp] — entirely above zero, confirming significance.*  
*95% CI for returning users: includes zero — effect is indistinguishable from noise.*

---

## What the Data Tells Us

**1. The feature works — but only for new users.**  
New users in the test group retained at 34.5% vs 28% in control. The chi-square test
confirms this is not by chance (p < 0.05). At this sample size, the result is robust.

**2. Returning users show no meaningful response.**  
The 1.5pp lift for returning users is statistically indistinguishable from zero.
This is expected: returning users already have established patterns and may find
the feature redundant or disruptive to their existing flow.

**3. Feature adoption funnel shows strong click-to-use conversion.**  
Among new test users: ~48% clicked the feature, ~30% used it fully.
Users who completed the feature showed noticeably higher Day-7 retention,
confirming the feature itself drives the outcome (not just selection bias).

---

## Risks & Guardrails

- **No degradation observed** in session length, error rate, or crash rate for test group.
- **Funnel gap:** 52% of new users saw the feature but did not click. Improving discoverability
  could further amplify the lift.
- **Returning user experience:** Shipping to returning users in current form risks user friction
  with no measurable retention benefit.

---

## Recommended Actions

1. **SHIP immediately to new users** — the evidence is strong, the risk is low.
2. **ITERATE for returning users** — explore: reduced prominence, opt-in toggle, or
   a redesigned version tailored to power users.
3. **Monitor** new user Day-7 retention post-rollout for 2 weeks to confirm results hold.
4. **Measure** feature discoverability — A/A test of tooltip/callout visibility for the
   52% who saw but didn't click.

---

## Confidence Statement

This recommendation is made with **high statistical confidence** for new users (p < 0.05,
23% relative lift, CI entirely above zero) and **appropriate caution** for returning users
where the data does not support a ship decision.

---

*Appendix: Full statistical output in outputs/stats_results.csv*  
*Full segmentation in outputs/segment_results.csv*  
*Funnel data in outputs/funnel_results.csv*
