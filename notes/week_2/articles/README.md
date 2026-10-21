# Week 2 Articles: Plan

## How many: 2 articles

Week 2 produced two kinds of material:
- a **measurement** (140 controlled prompt experiments)
- an **explanation** (why ICL works: the paper, the label experiments, biases, context and sampling)

Practitioners want the first and learners want the second, so they become two separate articles. A third article on sampling would repeat Week 1's Article 2 (temperature, top-k, top-p), so the sampling results go into Article 2 as a section instead.

| # | Working title | Core question | Notebook sections | Outline |
|---|---|---|---|---|
| 1 | **I Ran 140 Few-Shot Experiments. Here's What Actually Matters.** | Which prompt choices change accuracy, and by how much? | E1–E5 + summary chart | [01-what-moves-few-shot-accuracy.md](01-what-moves-few-shot-accuracy.md) |
| 2 | **Learning Without Training: Why Few-Shot Prompting Works, and Where It Breaks** | What is in-context learning actually doing? | GPT-3 paper, label mass, E4, biases, calibration, sampling, context window | [02-why-few-shot-works.md](02-why-few-shot-works.md) |

Write **Article 1 first**. It's results-driven, easy to structure, and the most shareable thing you have this week. Article 2 then explains the patterns Article 1 found.

## Figures
All in `results/week2/`. Copy the ones you use into this folder when you draft.

| File | Article |
|---|---|
| `summary_effects.png` | 1 (hero image) |
| `e1_count.png` | 1 and 2 |
| `e2_order.png` | 1 |
| `e3_format.png` | 1 |
| `e5_balance.png` | 1 or 2 |
| `sampling_icl.png` | 2 |
| `passkey.png` | 2 |

## Process (same as Week 1)
1. Answer the **Self-check** questions closed-book.
2. Run the **stretch experiment** for new, original material.
3. Draft at 1,200–1,800 words, verifying every number against `results/week2/icl_runs.jsonl` or the notebook.
4. Include the **honest results**: the passkey null result, calibration failing on `foo/bar`, and order effects smaller than the literature reports.

## Newsletter and video hooks
- **Newsletter hook:** "Adding a template that asks 'positive or negative?' made my model *worse than a coin flip*. It answered 'negative' 97% of the time."
- **Video demo:** show the summary bar chart, then flip every demo label live and show that the 0.5B model barely notices (90% → 84%).
