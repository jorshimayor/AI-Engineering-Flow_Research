**Title:** Week 5: joshua - prompt library with five strategies on GSM8K

## Task

Week 5, Systematic prompt engineering (anchor: *Chain-of-Thought Prompting*, Wei et al., 2022).
Lab: build a small prompt library for a fixed task, comparing three or more strategies with documented deltas.

## What I did

- **Library:** a prompt library (`src/prompts.py`) of 5 strategies. Each strategy is a template plus a parser, with 8 original worked examples checked by script.
- **Task:** 400 fixed GSM8K test problems.
- **Models:** Qwen2.5-0.5B and 1.5B Instruct, run on a Colab T4.
- **Tuning:** prompts and parsers were tuned only on GSM8K *train* problems. Two hypotheses were committed before the test run.

| Strategy | 0.5B | 1.5B | Delta vs baseline (0.5B / 1.5B) |
|---|---|---|---|
| Zero-shot direct | 2.0% | 8.2% | −4.8 / −2.0 |
| Few-shot direct (baseline) | 6.8% | 10.2% | |
| Zero-shot CoT | 28.0% | 29.8% | +21.2 / +19.5 |
| Few-shot CoT | 35.2% | 58.2% | +28.5 / +48.0 |
| Few-shot CoT + JSON | 16.0% | 53.8% | +9.2 / +43.5 |

Strict accuracy (answer in the requested format). Paired bootstrap CIs, McNemar and Holm are in the README.

**Pre-registered hypotheses:**
- **H1 (few-shot CoT beats few-shot direct by ≥ 10 points at each size): supported.** +28.5 (CI +23.0 to +34.0) and +48.0 (CI +42.8 to +53.2).
- **H2 (JSON within ±5 points of plain CoT): fails at 0.5B, inconclusive at 1.5B.**
  - 0.5B: −19.3 points (CI −24.3 to −14.3), a real structure tax.
  - 1.5B: −4.5 (CI −9.3 to +0.3), which crosses the margin.

**Exploratory findings:**
- The 0.5B JSON tax is format, not reasoning: scored leniently (any final number), the gap shrinks to −2.3.
- Zero-shot CoT reasons well but ignores the answer format (46% to 59% format failures). The worked examples mainly buy format compliance and shorter answers.

## Files (`Week5/joshua/`)

| File | Contents |
|---|---|
| `src/prompts.py` | The prompt library: 5 strategies, examples, strict and lenient parsers |
| `src/gsm8k.py` | Fixed test sample and train-split dev set (data downloaded on first use) |
| `src/run_prompt_bench.py` | Batched runner and paired summary |
| `src/stats.py` | Wilson, bootstrap, McNemar, Holm (imported by the runner) |
| `week5_prompt_library_colab.ipynb` | The Colab run, about 40 minutes on a free T4 |
| `results/*.jsonl` | All 4,000 outputs (2 models × 5 strategies × 400), with predictions and token counts |
| `README.md` | Plan, results, confirmatory tests, exploratory findings, caveats |
| `figures/` | Accuracy by strategy; cost vs accuracy |

## Limitations

- One model family, two sizes, greedy decoding, 400 of the 1,319 test problems.
- Lenient scoring can credit a coincidental last number, so it is used only for exploratory points.
- One hand-written set of examples.
- There is no Week 5 brief in this repo yet, so the files follow the curriculum's lab description.

## Submission rules

- [x] Branch `week5_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week5/joshua/`
- [x] No shared files or other fellows' folders edited
- [x] Hypotheses committed before the test run: https://github.com/jorshimayor/AI-Engineering-Flow_Research/commit/81ef456

Full notes, reading list and article plans: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_5
