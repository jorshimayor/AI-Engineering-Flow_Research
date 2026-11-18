# Week 8 Articles

| # | Article | Covers | Outline |
|---|---|---|---|
| 1 | Forty-Five Test Cases Told Me More Than 800 Benchmark Questions | Building a small eval set for three systems: typical, known-failure and edge cases, a check per behaviour, repeated runs, predictions on record, and a regression gate | [01-small-eval-set.md](01-small-eval-set.md) |
| 2 | The Right Answer, the Wrong Way | What process checks catch that accuracy hides, from the tool agent's lucky totals to a refusal that held only on the greedy run, plus a small model as judge | [02-right-answer-wrong-way.md](02-right-answer-wrong-way.md) |

**Order:** 1 then 2.
**Figures:** [`results/figures/week8_scorecard.png`](../../../results/figures/week8_scorecard.png), [`results/figures/week8_predicted_vs_actual.png`](../../../results/figures/week8_predicted_vs_actual.png), [`results/figures/week8_checks.png`](../../../results/figures/week8_checks.png).
**Hook:** the 3B shopping agent gave the right total in 15 of 90 runs. Only one case, a single-item budget question, also passed every process check; the rest got there by sending a calculation it couldn't run, asking for items that don't exist, and trying again.
**Report honestly:** 15 cases per system, so every comparison is descriptive; the cases were chosen to be hard; two cases (the injection and the comparison) tested less than intended, and the write-up says so.

Each outline has self-check questions and one stretch experiment.
