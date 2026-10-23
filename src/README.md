# Source Code

| Module | Week | Purpose |
|---|---|---|
| [`icl.py`](icl.py) | 2 | Few-shot formats, KV-cached label scoring, calibration |
| [`react_agent.py`](react_agent.py) | 3, 4 | ReAct loop, safe calculator, local LLM wrapper (CPU or GPU), CLI |
| [`react_tasks.py`](react_tasks.py) | 3 | The 30 Week 3 problems |
| [`react_tasks_v2.py`](react_tasks_v2.py) | 4 | Harder problem generator: 4 levels, dev and held-out test splits, answer checks |
| [`run_react_bench.py`](run_react_bench.py) | 3, 4 | Resumable benchmark runner and summaries, CLI |
| [`stats.py`](stats.py) | 4 | Wilson CI, paired bootstrap, exact McNemar, sign-flip, Fisher, Holm, power |
| [`protocol_analysis.py`](protocol_analysis.py) | 4 | Pre-registered analysis for the test run |
| [`figures.py`](figures.py) | all | Rebuilds `results/figures/` from saved results |

## CLI

```bash
uv run python src/react_agent.py "A truck carries 1,284 boxes with 36 cans each. 2,050 are damaged. How many good cans?"
uv run python src/run_react_bench.py --model Qwen/Qwen2.5-1.5B-Instruct          # Week 3 benchmark
uv run python src/run_react_bench.py --task dev --level 2 --max-steps 8          # Week 4 dev split
uv run python src/run_react_bench.py --summary results/week3_gpu/*.jsonl         # accuracy, CIs, cost
uv run python src/figures.py                                                     # rebuild figures
```

The calculator never calls `eval`; tool errors go back to the model as observations; runners save one result per line and resume after interruptions.
