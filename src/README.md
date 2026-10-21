# Source Code

The Python modules the notebooks import. Run anything here with `uv run` from the repository root.

## Modules

| Module | Used in | What's in it | Key functions |
|---|---|---|---|
| [`icl.py`](icl.py) | Week 2 | Few-shot prompting experiments | `Format`, `sample_demos`, `score` (KV-cached label log-probs), `evaluate`, `summarise` |
| [`react_agent.py`](react_agent.py) | Weeks 3, 4 | The ReAct agent | `calculate` (safe calculator), `system_prompt`, `LocalLLM` (CPU or GPU, stop strings), `run_agent` (the loop) |
| [`react_tasks.py`](react_tasks.py) | Week 3 | The 30 Week 3 word problems | `make_problems`, `correct` |
| [`react_tasks_v2.py`](react_tasks_v2.py) | Week 4 | Harder problem generator: 4 difficulty levels, dev and held-out test splits | `make_problems(split, level)`, `check_problems`, `leakage_check` |
| [`run_react_bench.py`](run_react_bench.py) | Weeks 3, 4 | Resumable benchmark runner and command-line interface | `run`, `summary`, `failure_type`, `is_format_failure` |
| [`stats.py`](stats.py) | Week 4 onwards | Small-sample statistics, no scipy | `wilson_ci`, `paired_bootstrap_ci`, `mcnemar_exact`, `sign_flip_test`, `fisher_exact`, `holm`, `power_mcnemar`, `n_for_power` |
| [`protocol_analysis.py`](protocol_analysis.py) | Week 4 | The pre-registered analysis for the test run | `analyse`, `print_report` |

## Command Line

```bash
# Ask the agent a question (uses a GPU if one is available)
uv run python src/react_agent.py "A truck carries 1,284 boxes with 36 cans each. 2,050 are damaged. How many good cans?"

# Watch the model invent its own tool result when the stop sequence is removed
uv run python src/react_agent.py --no-stop "..."

# Week 3 benchmark for any model: direct, CoT, tool-only (act) and ReAct
uv run python src/run_react_bench.py --model Qwen/Qwen2.5-1.5B-Instruct

# Week 4 dev split at a difficulty level
uv run python src/run_react_bench.py --task dev --level 2 --modes act react --max-steps 8

# Summaries: accuracy with 95% CIs, cost, format failures, paired ReAct vs tool-only test
uv run python src/run_react_bench.py --summary results/week3_gpu/*.jsonl
```

## Design Choices

- **The calculator never calls `eval`.** It walks the expression's syntax tree and allows only numbers and arithmetic, because model output is untrusted input.
- **Tool errors go back to the model as observations**, so the agent can recover instead of crashing.
- **The stop sequence `Observation:`** hands control back to the code before the model can invent a tool result.
- **Every Week 4 problem carries a solution expression**, and `check_problems` verifies each answer with the agent's own calculator.
- **Runners append one JSON line per problem** and skip finished ones, so long GPU runs survive disconnects.

## Licence

The code is licensed under [MIT](../LICENSE).
