**Title:** Week 2: joshua - few-shot count, order and format experiments

## Task

Week 2, Context, sampling and in-context learning (anchor: *Language Models are Few-Shot Learners*, Brown et al., 2020).
Lab: systematically vary few-shot examples (count, order, format) on a fixed task and document what actually moves output quality.

## What I did

Qwen2.5-0.5B (base) on SST-2 sentiment. The same 150 test reviews in every run, scored by label log-probability (deterministic, so only the prompt changes). 140 configurations.

| Factor varied | Effect on accuracy |
|---|---|
| Number of examples | 0: 87.3%, 1: 73.9%, 4: 85.5%, 16: 90.0%. Spread across example sets falls from 10.4 to 0.9 points |
| Order (24 orderings) | 81% to 91%; a positive last example raises positive predictions by 11 points |
| Template | 48.7% to 85.1% at 4-shot |
| Label words | great/terrible 89.1%, positive/negative 85.1%, foo/bar 71.6%, 0/1 58.2% |
| Label correctness (k = 8) | Gold 89.6%, random 88.4%, all flipped 83.6% |
| Sampling, temperature 1 | P(correct label) 47.5% at 0-shot, 77.1% at 4-shot |
| Context | GPT-2 fails at token 1,025; passkey retrieval 100% up to 8,192 tokens |

**Main finding:** format moved accuracy most (template and label words, up to 41 points). Order, choice of examples and label correctness moved it 6 to 9 points. The examples mainly teach the answer format: probability on valid labels rises from 0.62 to 0.99.

## Files (`Week2/joshua/`)

| File | Contents |
|---|---|
| `week2_in_context_learning.ipynb` | All experiments, with outputs, charts and observations |
| `src/icl.py` | Prompt builder, label scorer and sampling filters the notebook imports |
| `README.md` | Results, findings, a later re-audit and caveats |
| `figures/week2_what_moves_accuracy.png` | Effect size by factor |

## Limitations

- One small model on an easy task; order effects are larger on harder tasks in the literature.
- 150 test items: differences under about 5 points are within noise. A Week 4 re-audit with paired tests found 3 of these claims not established (listed in the README).

## Submission rules

- [x] Branch `week2_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week2/joshua/`
- [x] No shared files or other fellows' folders edited
- [x] Code the notebook needs is copied into the folder (`src/icl.py`)

Full notes and raw runs: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_2
