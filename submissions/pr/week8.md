**Title:** Week 8: joshua - a 45-case eval set for the Week 5 to 7 systems, with checks, repeated runs, a model judge and a regression scorecard

## Task

Week 8, Evaluation mindset (anchor: *Your AI Product Needs Evals*, Husain, 2024).
Lab: build a ten- to fifteen-case eval set for the Week 5 to 7 systems and score them.

## What I did

- **Cases:** 15 per system (prompting, tool agent, RAG), each 5 typical, 5 known failures from earlier weeks' traces, and 5 edge cases (unanswerable questions, an item not in the catalogue, a misspelt name, a two-page comparison, a prompt injection). Each case names its checks and why it exists.
- **Checks (Husain's Level 1):** a few lines of code each, on outcome and process: `correct`, `prices_first` (no calculation before prices arrive), `known_items`, `no_sibling`, `abstains`, `ignores_injection` and more.
- **Runs:** each case 6 times per model (1 greedy, 5 sampled at temperature 0.7), Qwen2.5-1.5B and 3B Instruct on a Colab T4. A case passes in 5 or more runs, fails in 1 or fewer, and is flaky otherwise.
- **Predictions** on record before the run. **Level 2:** the 3B model judges every greedy answer, compared with the checks. **Regression gate:** the scorecard is saved, and `run_evals.py --compare` fails if any case gets worse.

**Results** (greedy passes out of 15, prediction in brackets):

| System | 1.5B | 3B |
|---|---|---|
| Week 5 prompts (few-shot CoT) | 12 (8) | 14 (11) |
| Week 6 tool agent | 0 (0) | 1 (4) |
| Week 7 RAG (dense, k = 3) | 12 (10) | 14 (12) |

**Findings:**
- The 3B tool agent gave the right total in 15 of 90 runs, but only one case passed every process check. It sends `calculate` before prices arrive in over 80% of runs and asks for unit-prefixed items ("jar of basil pesto") in 46%.
- The tool agent cannot decline: asked for caviar, which isn't sold, it answered 0.0. RAG at 3B declined both unanswerable questions every time; RAG at 1.5B invented "550 mAh".
- 3 of 53 greedy passes did not hold under sampling. The 3B prompt system flagged a missing number on its greedy run and assumed zero in 5 of 6 sampled runs.
- My predictions were too low for prompts and RAG and too high for the tool agent. Week 7's colour and power misses were a k = 1 problem and don't recur at k = 3.
- The 3B judge agreed with the checks 89 to 96% of the time (κ 0.77 to 0.91) and never passed a wrong answer, but failed 4 correct refusals.
- Reading the traces showed two cases testing less than intended: the injection notice was never retrieved, and the comparison failed because one product's weight was never retrieved. Both are fixed in the plan for version 1.1.

## Files (`Week8/joshua/`)

| File | Contents |
|---|---|
| `src/eval_cases.py` | The 45 cases, the injected notice, my predictions |
| `src/run_evals.py` | Runner for all three systems, the checks, the judge, summary, scorecard and `--compare` |
| `src/run_prompt_bench.py`, `src/tool_agent.py`, `src/tools.py`, `src/tool_tasks.py`, `src/rag.py`, `src/rag_corpus.py` and others | The Week 5 to 7 systems it evaluates, plus statistics and figures |
| `tests/test_week8.py` | Model-free checks, including a full run with a fake model |
| `week8_evals_colab.ipynb` | Step-by-step walkthrough, executed on the run (about 25 minutes on a free T4) |
| `results/` | 540 runs with every output and check, judge verdicts, `scorecard.json` |
| `README.md` | Reading summary, the eval set, plan, results, judge, caveats |
| `figures/` | Every case and run; predicted vs measured; pass rate by check |

## Limitations

- 15 cases per system, chosen to be hard: every comparison is descriptive, and pass rates say nothing about accuracy on real questions.
- One sampling temperature; one judge from the same model family, with a one-line rubric.
- There is no Week 8 brief in this repo yet, so the files follow the curriculum's lab description.

## Submission rules

- [x] Branch `week8_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week8/joshua/`
- [x] No shared files or other fellows' folders edited
- [x] Cases, decision rules and predictions committed before the run: https://github.com/jorshimayor/AI-Engineering-Flow_Research/commit/063b855

Full notes, reading list and article plans: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_8
