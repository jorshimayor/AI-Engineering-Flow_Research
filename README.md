# AI Engineering: Learning in Public

My work through a 48-week applied AI engineering fellowship, published so others can learn from it: notebooks, code, raw results, detailed notes and reading lists, including the experiments that went wrong. Everything runs on a laptop or a free cloud GPU.

**Status:** Phase 1 (Weeks 1 to 4) complete. The Week 4 pre-registered test run is pending.

## Start Here

| If you want to… | Go to |
|---|---|
| Learn the material week by week | [`notes/`](notes/README.md) |
| Run or read the experiments | [`jupyter/`](jupyter/README.md) |
| Use or read the code | [`src/`](src/README.md) |
| Inspect the raw results | [`results/`](results/README.md) |
| See the pre-registered Week 4 test | [`protocol/`](protocol/README.md) |
| Check which paper claims I reproduced | [`notes/phase_1_log.md`](notes/phase_1_log.md) |

## Weeks

| Week | Topic | Notes | Notebook |
|---|---|---|---|
| 1 | Transformer mechanics | [notes](notes/week_1/README.md) | [week1_transformer_probing](jupyter/week1_transformer_probing.ipynb) |
| 2 | Context, sampling and in-context learning | [notes](notes/week_2/README.md) | [week2_in_context_learning](jupyter/week2_in_context_learning.ipynb) |
| 3 | Reasoning and tool-use foundations | [notes](notes/week_3/README.md) | [week3_react_agent](jupyter/week3_react_agent.ipynb) · [GPU run](jupyter/week3_colab.ipynb) |
| 4 | Research methodology for applied AI | [notes](notes/week_4/README.md) · [rigour memo](notes/week_4/rigour_memo.md) | [week4_rigour_audit](jupyter/week4_rigour_audit.ipynb) · [test run](jupyter/week4_test_run_colab.ipynb) |

Headline findings and how well each held up are summarised in [`notes/README.md`](notes/README.md#headline-findings).

## Quick Start

Needs [uv](https://docs.astral.sh/uv/) and Git.

```bash
git clone https://github.com/jorshimayor/AI-Engineering-Flow_Research.git
cd AI-Engineering-Flow_Research
uv sync
uv run jupyter lab
```

Versions are pinned for an Intel Mac (Python 3.12, PyTorch 2.2.2). GPU notebooks run on free Colab or Kaggle. Runtimes, GPU instructions and troubleshooting are in [`jupyter/README.md`](jupyter/README.md).

## Licence

- **Code** (`src/`, notebooks' code): [MIT](LICENSE)
- **Notes, documentation, results and charts**: [CC BY 4.0](LICENSE-CC-BY-4.0)

You're free to reuse and adapt both. Please credit Joshua Obafemi and link back here.

## Contact

[Website](https://jorshimayor.is-a.dev) · [Articles](https://jorshimayor.hashnode.dev) · [Newsletter](https://jorshimayor.substack.com) · [YouTube](https://www.youtube.com/@jorshimayor) · [X](https://x.com/jorshimayor) · [LinkedIn](https://linkedin.com/in/jorshimayor)

Corrections and "I tried this and got something different" are welcome as issues.
