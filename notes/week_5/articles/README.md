# Week 5 Articles

| # | Article | Covers | Outline |
|---|---|---|---|
| 1 | Chain-of-Thought Still Works at 0.5B | The paper, the prompt library, the pre-registered test, and the scale threshold that didn't hold | [01-cot-at-small-scale.md](01-cot-at-small-scale.md) |
| 2 | Half My Model's Wrong Answers Were Right | Strict vs lenient scoring, the JSON tax, what few-shot examples actually buy | [02-format-is-half-the-score.md](02-format-is-half-the-score.md) |

**Order:** 1 then 2.
**Figures:** [`results/figures/week5_strategy_accuracy.png`](../../../results/figures/week5_strategy_accuracy.png), [`results/figures/week5_cost_vs_accuracy.png`](../../../results/figures/week5_cost_vs_accuracy.png).
**Hook:** the paper found chain-of-thought useless below about 10B parameters; on a 0.5B model it added 28 points.
**Report honestly:** one model family, greedy decoding, 400 problems; H2 at 1.5B is inconclusive; lenient-score findings are exploratory.

Each outline has self-check questions and one stretch experiment.
