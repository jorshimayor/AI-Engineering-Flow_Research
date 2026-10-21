# Notebooks

One or more notebooks per week. All outputs are saved, so each notebook can be read without running it. The notes for each week explain the results in [`../notes/`](../notes/README.md).

## On Your Machine

Set up the environment from the repository root first (see the [main README](../README.md#quick-start)), then:

```bash
uv run jupyter lab
```

| Notebook | What it does | Runtime on a laptop CPU |
|---|---|---|
| [`week1_transformer_probing.ipynb`](week1_transformer_probing.ipynb) | Tokeniser edge cases, embeddings, next-token distributions, attention rebuilt by hand, generation | about 1 minute |
| [`week2_in_context_learning.ipynb`](week2_in_context_learning.ipynb) | 140 few-shot experiments on SST-2, sampling, context-window tests | 2 to 3 hours the first time; cached afterwards |
| [`week3_react_agent.ipynb`](week3_react_agent.ipynb) | The ReAct agent vs direct, CoT and tool-only prompting at 0.5B | 1 to 2 hours; cached afterwards |
| [`week4_rigour_audit.ipynb`](week4_rigour_audit.ipynb) | Statistics audit of Weeks 2 and 3, winner's curse, cost-accuracy plot, power analysis | about 2 minutes (no models) |

Experiments save their results to [`../results/`](../results/README.md) as they go, so re-running a notebook only computes what's missing.

To run a notebook headless:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace jupyter/week1_transformer_probing.ipynb
```

## On a Free GPU (Colab or Kaggle)

| Notebook | What it does | Time on a T4 |
|---|---|---|
| [`week3_colab.ipynb`](week3_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week3_colab.ipynb) | Week 3 benchmark at Qwen2.5 1.5B and 3B | about 30 minutes plus downloads |
| [`week4_calibration_colab.ipynb`](week4_calibration_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week4_calibration_colab.ipynb) | Picks difficulty levels on the dev split (already done; results in `results/week4_dev_v2/`) | 60 to 90 minutes |
| [`week4_test_run_colab.ipynb`](week4_test_run_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week4_test_run_colab.ipynb) | The pre-registered test: 480 held-out problems per model | about 7.5 hours, resumable |

**Colab:**
1. Open the link.
2. Choose `Runtime → Change runtime type → T4 GPU`.
3. Choose `Runtime → Run all`.

Keep Google Drive switched on in the notebook: results are saved one problem at a time, so a disconnect only loses the problem in progress. Re-run the same cell to continue.

**Kaggle** (about 30 free GPU hours a week):
1. Import the notebook.
2. In Settings, set `Accelerator → GPU T4` and switch `Internet → On`.
3. Set `USE_DRIVE = False`.

The notebooks always fetch the latest code from GitHub's `main` branch, and the Week 4 notebooks check the generator version before running.

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv sync` tries to install a PyTorch that doesn't exist | Use Python 3.12 (`.python-version`). On Intel Macs, newer Python has no PyTorch 2.2.2 build |
| `jupyter` points to an old path after moving the folder | Recreate the environment: `rm -rf .venv && uv sync` |
| Colab can't find a notebook | Colab reads from GitHub's `main` branch, so the file must be merged there |
| Colab seems to run old code | `Runtime → Disconnect and delete runtime`, then run again |
| SSL certificate errors from Python scripts | macOS system Python may lack certificates; use `uv run python …` |
| A long GPU run disconnected | Re-run the same cell; finished problems are skipped |
