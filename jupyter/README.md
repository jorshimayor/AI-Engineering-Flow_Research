# Notebooks

Outputs are saved, so every notebook can be read without running it.

## Local

```bash
uv run jupyter lab
```

| Notebook | Runtime (laptop CPU) |
|---|---|
| [`week1_transformer_probing.ipynb`](week1_transformer_probing.ipynb) | 1 minute |
| [`week2_in_context_learning.ipynb`](week2_in_context_learning.ipynb) | 2 to 3 hours first run, then cached |
| [`week3_react_agent.ipynb`](week3_react_agent.ipynb) | 1 to 2 hours first run, then cached |
| [`week4_rigour_audit.ipynb`](week4_rigour_audit.ipynb) | 2 minutes (no models) |

Results cache to [`../results/`](../results/README.md), so re-runs only compute what's missing.

## GPU (Colab or Kaggle)

| Notebook | Time on a T4 |
|---|---|
| [`week3_colab.ipynb`](week3_colab.ipynb) · [Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week3_colab.ipynb) | 30 minutes |
| [`week4_calibration_colab.ipynb`](week4_calibration_colab.ipynb) · [Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week4_calibration_colab.ipynb) | 60 to 90 minutes (done) |
| [`week4_test_run_colab.ipynb`](week4_test_run_colab.ipynb) · [Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week4_test_run_colab.ipynb) | 7.5 hours, resumable |
| [`week5_prompt_library_colab.ipynb`](week5_prompt_library_colab.ipynb) · [Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week5_prompt_library_colab.ipynb) | about 40 minutes |
| [`week6_tool_calling_colab.ipynb`](week6_tool_calling_colab.ipynb) · [Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week6_tool_calling_colab.ipynb) | about 1 hour |
| [`week7_rag_colab.ipynb`](week7_rag_colab.ipynb) · [Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week7_rag_colab.ipynb) | about 30 minutes; shows code, retrieved chunks, tables and figures inline, and saves a copy of itself with outputs |

The GPU notebooks are walkthroughs as well as runners. Each one explains the step, shows the code from `src/`, the data, the prompts and the scoring on real examples, then the results as tables, the hypothesis tests, the figures and failure examples. Without a GPU they skip the model runs and read the saved results in `results/`, which is how the committed copies were executed, so their outputs are readable on GitHub.

**Colab:** `Runtime → Change runtime type → T4 GPU`, then `Run all`. Keep Drive on; a disconnect only loses the current problem.
**Kaggle:** enable GPU and Internet in Settings, set `USE_DRIVE = False`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv sync` can't find PyTorch | Use Python 3.12 (`.python-version`) |
| `jupyter` points to an old path | `rm -rf .venv && uv sync` |
| Colab can't find a notebook | It reads GitHub's `main` branch; merge first |
| Colab runs old code | `Runtime → Disconnect and delete runtime` |
| SSL errors | Use `uv run python …`, not the system Python |
