# Notes

Everything I wrote while working through the fellowship: what I did each week, what I found, what went wrong, what to read next, and plans for the public write-ups.

## How To Use These Notes

1. Read the week's `README.md`. It opens with a one-page summary of the paper, then walks through each experiment.
2. Open the matching notebook in [`../jupyter/`](../jupyter/) alongside it. Outputs are saved, so you can read without running anything.
3. Use `resources.md` for further reading. Each list starts with a short "suggested path" for when time is tight.
4. Try the self-check questions in `articles/` without looking at the notes.

**Short on time?** Read these four:
- Week 1, section 4: self-attention rebuilt by hand
- Week 2: the "what actually moves accuracy" chart
- Week 3: the GPU results, where reasoning hurt a 1.5B model
- the [rigour memo](week_4/rigour_memo.md)

## Weeks

| Week | Topic | Paper | Notes | Reading | Article plans |
|---|---|---|---|---|---|
| 1 | Transformer mechanics | Attention Is All You Need (2017) | [README](week_1/README.md) | [resources](week_1/resources.md) | [articles](week_1/articles/README.md) |
| 2 | Context, sampling and in-context learning | Language Models are Few-Shot Learners (2020) | [README](week_2/README.md) | [resources](week_2/resources.md) | [articles](week_2/articles/README.md) |
| 3 | Reasoning and tool-use foundations | ReAct (2022) | [README](week_3/README.md) | [resources](week_3/resources.md) | [articles](week_3/articles/README.md) |
| 4 | Research methodology for applied AI | AI Agents That Matter (2025) | [README](week_4/README.md) · [rigour memo](week_4/rigour_memo.md) · [protocol drafts](week_4/eval_protocol.md) | [resources](week_4/resources.md) | [articles](week_4/articles/README.md) |

[`phase_1_log.md`](phase_1_log.md) lists every paper claim probed in Weeks 1 to 4 and whether I reproduced it.

## Headline Findings

| Week | Finding | Holds up? |
|---|---|---|
| 1 | One trailing space drops "Paris" from GPT-2's 5th choice to its 1,472nd. Hindi costs 5.4× more tokens than English for the same sentence | Exact measurement |
| 1 | Self-attention rebuilt by hand matches GPT-2 to within floating-point error | Exact |
| 2 | Prompt template and label words move few-shot accuracy by up to 41 points; example order by 8 to 9; label correctness by 6 | Mostly; see the Week 4 audit |
| 2 | With every example label flipped, a 0.5B model still scores 84% | Yes (audited) |
| 3 | At 1.5B, ReAct scored 30 points *below* tool-only prompting (p = 0.012); at 3B both hit 100% | Pilot (30 problems) |
| 4 | 8 of my 15 Week 2 and 3 claims survived proper statistics; 7 weren't established | Yes |
| 4 | Does ReAct beat tool-only prompting on harder held-out problems? | Pending: pre-registered test not yet run |

Results written before Week 4 are kept as they were; the Week 4 audit's verdicts are noted beside them.

## What's in Each Week's Folder

| File | Contents |
|---|---|
| `README.md` | Paper summary, setup, every result with tables and charts, what went wrong, takeaways, next experiments |
| `resources.md` | Papers, videos, courses, articles, tools and code, marked by level. Links were checked when written |
| `articles/README.md` | How many articles and why, writing order, figures, newsletter and video hooks |
| `articles/*.md` or `articles/outlines/` | One outline per article, with self-check questions and a stretch experiment |

## Licence

The notes are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0): reuse and adapt them freely, with credit to Joshua Obafemi and a link back to this repository.
