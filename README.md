# AI Engineering: Learning in Public

Notebooks, code, raw results and notes from a 48-week applied AI engineering fellowship. Everything runs on a laptop or a free cloud GPU.

**Status:** Weeks 1 to 4 done. Week 4's pre-registered test run is pending.

![Week 3 accuracy by model size](results/figures/week3_accuracy_by_size.png)

## Weeks

| Week | Topic | Headline result | Notes |
|---|---|---|---|
| 1 | Transformer mechanics | One trailing space drops "Paris" from GPT-2's 5th choice to its 1,472nd | [notes](notes/week_1/README.md) |
| 2 | In-context learning | Prompt format moves few-shot accuracy by up to 41 points; example order by 9 | [notes](notes/week_2/README.md) |
| 3 | ReAct agents | A calculator lifts accuracy to 97% to 100% at 1.5B and 3B; reasoning steps cost 30 points at 1.5B | [notes](notes/week_3/README.md) |
| 4 | Research methodology | 8 of 15 earlier claims survive proper statistics; ReAct vs Act test frozen at 480 problems per model | [notes](notes/week_4/README.md) |

## Layout

| Folder | Contents |
|---|---|
| [`notes/`](notes/README.md) | Weekly write-ups, reading lists, article plans |
| [`jupyter/`](jupyter/README.md) | Notebooks (local and Colab) |
| [`src/`](src/README.md) | Code the notebooks import, plus CLIs |
| [`results/`](results/README.md) | Raw results and figures |
| [`protocol/`](protocol/README.md) | Frozen pre-registration for the Week 4 test |

## Quick start

```bash
git clone https://github.com/jorshimayor/AI-Engineering-Flow_Research.git
cd AI-Engineering-Flow_Research
uv sync
uv run jupyter lab
```

Python 3.12 and PyTorch 2.2.2 are pinned for Intel Macs. GPU notebooks run on Colab or Kaggle: see [`jupyter/`](jupyter/README.md).

## Licence

Code: [MIT](LICENSE). Notes, results and figures: [CC BY 4.0](LICENSE-CC-BY-4.0). Credit Joshua Obafemi and link back.

[Website](https://jorshimayor.is-a.dev) · [Articles](https://jorshimayor.hashnode.dev) · [Newsletter](https://jorshimayor.substack.com) · [YouTube](https://www.youtube.com/@jorshimayor) · [X](https://x.com/jorshimayor) · [LinkedIn](https://linkedin.com/in/jorshimayor)
