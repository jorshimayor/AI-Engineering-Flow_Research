# Week 8: Evaluation Mindset

**Reading:** [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) (Husain, 2024)
**Lab:** build a ten- to fifteen-case eval set for the Week 5 to 7 systems and score them.
**Code:** [`src/eval_cases.py`](../../src/eval_cases.py) (the 45 cases and my predictions) · [`src/run_evals.py`](../../src/run_evals.py) (runner, checks, model judge, scorecard, regression compare) · [`tests/test_week8.py`](../../tests/test_week8.py)
**Notebook:** [`week8_evals_colab.ipynb`](../../jupyter/week8_evals_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week8_evals_colab.ipynb) (about 25 minutes on a free T4)

**Status:** plan and predictions fixed, run pending.

## The reading in brief

| | Husain (2024) |
|---|---|
| Claim | AI products that stall share one root cause: no evaluation system, so nobody can tell whether a change helped |
| Level 1 | Unit tests: scoped assertions on each output, many cases per feature, run on every change and tracked over time. They need not all pass; the pass rate is a product decision |
| Level 2 | Human and model evaluation: log traces, read them, and use a model as judge only once its verdicts agree with a human's |
| Level 3 | A/B tests with real users, once the product is mature |
| For this lab | Weeks 5 to 7 each scored a system with one number on 200 to 400 items. That number never said which behaviours fail, whether a pass was luck, or what happens on inputs the test set lacked |

## The eval set

45 cases, 15 per system, each with the checks it must pass and a note on why it exists.

| System | Configuration | Typical (5) | Known failure (5) | Edge (5) |
|---|---|---|---|---|
| Week 5 prompts | Few-shot CoT, maths word problems | GSM8K-style problems | Large numbers, a decimal answer, chained percentages, an answer in the millions, distracting numbers | A negative answer, an **unanswerable** problem, unit conversion, clock times, a rounding instruction |
| Week 6 tool agent | Direct route with repair | One per question template | "bottle of maple syrup" (Week 6's unknown-item bug), budget rounding, three items (calculate before prices), a negative difference, 15% off | An item **not in the catalogue**, a single lookup, "half a kilogram", irrelevant numbers, discount plus change |
| Week 7 RAG | Dense, k = 3 | One per fact type | Colour and power questions (Week 7's wrong-chunk misses), a sibling-confusion town | A **misspelt** name, a product that **doesn't exist**, a fact the pages **never state**, a **two-page comparison**, a **prompt injection** in a retrieved notice |

**Checks** (Level 1), each a few lines of code on the saved output:

| System | Checks |
|---|---|
| Prompts | `format` (the answer line parses), `correct`, `not_truncated`; `flags_missing_info` for the unanswerable case |
| Tool agent | `correct`, `no_malformed`, `prices_first` (no `calculate` until every price is back), `known_items` (no unknown-item lookups); `no_answer` for the item that doesn't exist; `efficient` (2 turns) for a single lookup |
| RAG | `correct`, `no_sibling` (no other product's value), `answer_retrieved`; `abstains` for the unanswerable cases; `compares` for the two-page question; `ignores_injection` (never answers 999) |

**Runs:** every case runs 6 times per model: once greedy, as in Weeks 5 to 7, and 5 times sampled (temperature 0.7, top-p 0.8, fixed seeds). A pass on the greedy run alone can be luck.

**Level 2:** the 3B model judges every greedy answer against the reference (PASS or FAIL), and its verdicts are compared with the deterministic checks.

**Regression baseline:** the scorecard (each case's share of passing runs) is saved. `run_evals.py --compare old new` lists every case that moved from passing to flaky or failing and exits with an error if any did, so it can gate a change.

## Plan (fixed before the run)

**Models:** Qwen2.5-1.5B-Instruct and 3B-Instruct for all three systems, so the Week 5 system gains a size it never had.

**Decision rules:**
- A case **passes** if it passes in at least 5 of its 6 runs, **fails** if it passes in at most 1, and is **flaky** otherwise.
- With 15 cases, a pass rate's 95% interval is about ±25 points (8 of 15 gives 30% to 75%). So this week reports counts and named cases, with no significance tests. Comparisons between systems or models are descriptive.

**Predictions** (gut feel, written down before the run): cases expected to pass on the greedy run, out of 5 per group.

| System | Model | Typical | Known failure | Edge | Total (of 15) |
|---|---|---|---|---|---|
| Prompts | 1.5B | 4 | 2 | 2 | 8 |
| Prompts | 3B | 5 | 3 | 3 | 11 |
| Tool agent | 1.5B | 0 | 0 | 0 | 0 |
| Tool agent | 3B | 2 | 1 | 1 | 4 |
| RAG | 1.5B | 5 | 3 | 2 | 10 |
| RAG | 3B | 5 | 4 | 3 | 12 |

**What I expect to learn:**
- Which known failures still happen and which were one-offs.
- Whether any system can say "I can't answer that": the prompt and tool systems have no way to, by design.
- How many greedy passes are luck, i.e. flaky under sampling.
- Whether a 3B judge agrees with code-based checks well enough to use where code can't check.

**Threats:**
- I wrote the cases knowing each system's weaknesses, so the set is deliberately harder than the original test sets. Its pass rate is not an estimate of accuracy on real traffic.
- Sampled runs use one temperature. Five samples can show flakiness but not measure its rate precisely.
- The judge is from the same family as the systems it grades, and the 3B judge grades its own answers.

## Results

Pending the run.

## Files

| File | What |
|---|---|
| [`src/eval_cases.py`](../../src/eval_cases.py) | The 45 cases, the injected notice, and my predictions |
| [`src/run_evals.py`](../../src/run_evals.py) | Runs each system, applies the checks, the judge, the summary, the scorecard and the regression compare |
| [`tests/test_week8.py`](../../tests/test_week8.py) | Model-free checks, including a full run with a fake model |
| [`jupyter/week8_evals_colab.ipynb`](../../jupyter/week8_evals_colab.ipynb) | The Colab walkthrough and run |
| [`resources.md`](resources.md) | Reading list |
