# AI Engineering: Learning in Public

A week-by-week record of a 48-week applied AI engineering fellowship: every experiment, every result (including the ones that went wrong), the notes, the reading lists and the article plans. Everything here runs on a laptop or a free cloud GPU, and every number in the notes can be regenerated from the code and the saved results.

I'm publishing the notes, not just the code, so that anyone learning the same material can follow the same path, check my working and avoid my mistakes.

**Author:** Joshua Obafemi ([jorshimayor](https://jorshimayor.is-a.dev)) · **Started:** September 2026 · **Status:** Phase 1 (Weeks 1 to 4) complete; the Week 4 pre-registered test run is pending.

---

## Contents

1. [What This Repository Is](#1-what-this-repository-is)
2. [How To Use It To Learn](#2-how-to-use-it-to-learn)
3. [Results at a Glance](#3-results-at-a-glance)
4. [Week by Week](#4-week-by-week)
5. [Repository Map](#5-repository-map)
6. [Setup](#6-setup)
7. [Running Things](#7-running-things)
8. [The Code](#8-the-code)
9. [Results and Data Formats](#9-results-and-data-formats)
10. [How I Report Results](#10-how-i-report-results)
11. [Notes, Resources and Articles](#11-notes-resources-and-articles)
12. [Known Limitations](#12-known-limitations)
13. [Roadmap](#13-roadmap)
14. [Troubleshooting](#14-troubleshooting)
15. [Acknowledgements and Contact](#15-acknowledgements-and-contact)

---

## 1. What This Repository Is

The fellowship (run by the Applied AI Engineering team at Flow Research) moves from first principles of language models to an original research contribution over 48 weeks. Each week has a topic, an anchor paper and a lab. This repository holds my work on each one:

| For every week | Where |
|---|---|
| A runnable notebook with all outputs saved | [`jupyter/`](jupyter/) |
| Reusable Python code the notebooks import | [`src/`](src/) |
| Raw results (per-item JSONL), charts and summaries | [`results/`](results/) |
| Detailed notes: what I did, what I found, what went wrong | [`notes/week_N/README.md`](notes/) |
| A curated reading list (papers, videos, courses, articles), every link checked | [`notes/week_N/resources.md`](notes/) |
| Article plans and outlines for the write-ups | [`notes/week_N/articles/`](notes/) |

Two principles run through all of it:
- **Show the evidence.** Each claim links to the notebook cell and the raw data behind it.
- **Report what didn't work.** Wrong predictions, failed runs and bugs stay in the record, with what they taught me. Week 4 audits my own earlier claims and finds that 7 of 15 weren't supported by the data.

---

## 2. How To Use It To Learn

**If you're following the same curriculum or teaching yourself LLM engineering:**

1. **Read the week's notes first** (`notes/week_N/README.md`). Each starts with a one-page summary of the paper, then walks through what was built and why.
2. **Open the notebook** and read it alongside the notes. All outputs are saved, so you can read without running anything.
3. **Run it yourself** (section 6). Change one thing and see if you get the same result.
4. **Use the reading list** (`notes/week_N/resources.md`). Each has a "suggested path" of five or six items if you're short on time.
5. **Try the self-check questions** in `notes/week_N/articles/` without looking at the notes. They're the questions I used to test my own understanding.

**Suggested order if you only have an afternoon:**
- Week 1, section 4: self-attention rebuilt by hand in about 10 lines of PyTorch.
- Week 2, the "what actually moves accuracy" chart: 140 prompt experiments in one picture.
- Week 3: the ~100-line ReAct agent in [`src/react_agent.py`](src/react_agent.py), then the GPU results showing reasoning traces *hurting* a 1.5B model.
- Week 4: [the rigour memo](notes/week_4/rigour_memo.md), 12 rules for not fooling yourself, each tied to a mistake I made.

---

## 3. Results at a Glance

| Week | Question | Headline finding | Holds up? |
|---|---|---|---|
| 1 | What does a model actually see? | One trailing space drops "Paris" from rank 5 to rank 1,472 in GPT-2. The same sentence costs 5.4× more tokens in Hindi than in English | Exact measurements |
| 1 | Does the attention formula match the real model? | Rebuilt by hand, layer-0 attention matches GPT-2 to within floating-point error | Exact |
| 2 | What moves few-shot accuracy? | Prompt template (36 to 41 points) and label words (31) matter far more than example order (8 to 9) or even correct labels (6) | Mostly. Some single claims didn't survive the Week 4 audit (see below) |
| 2 | Do small models learn from the labels in examples? | With every example label flipped, a 0.5B model still scores 84%: it follows its prior, as Wei et al. (2023) predicted | Yes (audited) |
| 3 | Does ReAct beat tool use without reasoning? | 0.5B: no difference detectable. 1.5B: ReAct **30 points worse** (p = 0.012). 3B: both 100% (ceiling) | Pilot only (30 problems); led to the Week 4 protocol |
| 4 | How many of my own claims survive proper statistics? | 8 of 15 hold, 7 are not established, 0 are overturned. Choosing the "best" prompt on test data overstated its advantage by 28% to 40% | Yes |
| 4 | Does ReAct beat Act-only on harder, held-out problems? | Pre-registered protocol frozen; 480 problems per model at 1.5B and 3B | **Pending** (test run not yet done) |

---

## 4. Week by Week

### Week 1: Transformer Mechanics

| | |
|---|---|
| Anchor paper | *Attention Is All You Need* (Vaswani et al., 2017) |
| Lab | Probe a pretrained model's tokeniser edge cases and next-token distributions across prompts |
| Model | GPT-2 small (124M), on CPU |
| Notebook | [`jupyter/week1_transformer_probing.ipynb`](jupyter/week1_transformer_probing.ipynb) |
| Notes | [`notes/week_1/README.md`](notes/week_1/README.md) · [resources](notes/week_1/resources.md) · [article plans](notes/week_1/articles/README.md) |

What I did and found:
- **Tokenisation:**
  - `' hello'` and `'hello'` are different tokens.
  - `1234567` splits as `123|45|67`.
  - An emoji can take 2 to 10 tokens of partial bytes.
  - The literal text `<|endoftext|>` becomes the real end-of-text token, a prompt-injection risk.
  - The same sentence costs 1.6× to 5.4× more tokens in other languages.
- **The trailing-space trap:** after "The capital of France is ", the probability of "Paris" drops from 3.2% to almost zero. GPT-2 attaches spaces to the *next* word, so a prompt ending in a space is rare in training.
- **Knowledge vs generation:** "Paris" is only GPT-2's fifth choice, yet among four cities it wins 87% of the probability. This is why benchmarks score answer options instead of free text.
- **Attention:**
  - Rebuilt by hand, it matches the model exactly.
  - Head 3 of layer 4 sends "it" to "animal" with weight 0.85, but it does that from almost every token, so it isn't really resolving "it".
  - Deep layers park up to 82% of their attention on the first token ("attention sinks").
- **Generation:** a hand-written loop with a KV cache reproduces the library's output exactly. Greedy decoding falls into repetition loops.

### Week 2: Context, Sampling and In-Context Learning

| | |
|---|---|
| Anchor paper | *Language Models are Few-Shot Learners* (Brown et al., 2020) |
| Lab | Systematically vary few-shot examples (count, order, format) on a fixed task and document what actually moves output quality |
| Model and task | Qwen2.5-0.5B (base) on SST-2 movie-review sentiment, 150 fixed test reviews |
| Notebook and code | [`jupyter/week2_in_context_learning.ipynb`](jupyter/week2_in_context_learning.ipynb) · [`src/icl.py`](src/icl.py) |
| Notes | [`notes/week_2/README.md`](notes/week_2/README.md) · [resources](notes/week_2/resources.md) · [article plans](notes/week_2/articles/README.md) |

140 configurations, each changing one thing at a time. A KV-cache trick (encode the shared examples once, reuse them for every test review) made this feasible on a laptop CPU, and I verified it matches full scoring to within 1e-5.

- **Format matters most:** the template and the label words moved accuracy by up to 41 points.
- **Examples mainly teach the answer format:** zero-shot, 38% of the probability lands on tokens that aren't valid answers; with 16 examples, almost none.
- **Wrong labels barely matter:** random labels cost about 1 point (replicating Min et al., 2022).
- **Flipped labels:** a 0.5B model still scores 84%; small models follow their prior (Wei et al., 2023).
- **Predictable biases:**
  - A positive last example shifts predictions positive by about 11 points.
  - Each extra positive example adds about 8 points of positive predictions.
- **Calibration (Zhao et al., 2021):** it rescued a prompt that had collapsed onto one label, but broke arbitrary labels like "foo/bar".
- **Sampling:** zero-shot at temperature 1 gets the right label only 47.5% of the time; with 4 examples, 77%.
- **Context window:** GPT-2 crashes at token 1,025. Passkey retrieval was 100% up to 8,192 tokens, an honest null result: the test is a copy task and too easy.

*Week 4 later audited these claims (section 4, Week 4). "16 examples beat 0", "great/terrible beats positive/negative" and "the question template is below chance" were not statistically established.*

### Week 3: Reasoning and Tool-Use Foundations

| | |
|---|---|
| Anchor paper | *ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022) |
| Lab | Hand-implement a minimal single-tool ReAct-style loop on a small task |
| Agent | [`src/react_agent.py`](src/react_agent.py): about 100 lines, no framework, one calculator tool |
| Notebooks | [`jupyter/week3_react_agent.ipynb`](jupyter/week3_react_agent.ipynb) (CPU, 0.5B) · [`jupyter/week3_colab.ipynb`](jupyter/week3_colab.ipynb) (GPU, 1.5B and 3B) |
| Notes | [`notes/week_3/README.md`](notes/week_3/README.md) · [resources](notes/week_3/resources.md) · [article plans](notes/week_3/articles/README.md) |

The agent is a loop:
1. The model writes a Thought and an Action, and generation stops at `Observation:`.
2. My code runs the tool and appends the real result.
3. Repeat until the model calls `finish[...]`.

The calculator uses a safe expression evaluator (never `eval`), so model output can't run code. I compared four modes from the paper on 30 two-step word problems with big numbers:

| Model | Direct answer | Reasoning only (CoT) | Tool only (Act) | ReAct |
|---|---|---|---|---|
| Qwen2.5-0.5B (laptop CPU) | 0% | 0% | 23% | 20% |
| Qwen2.5-1.5B (Colab T4) | 0% | 20% | **97%** | **67%** |
| Qwen2.5-3B (Colab T4) | 0% | 50% | 100% | 100% |

- **The calculator does the heavy lifting.** Without it, wrong answers are near misses (about 5% off). With it, wrong answers are wrong plans (about 90% off).
- **At 1.5B, the reasoning trace introduced the errors.** It misread "for 46 days" in one problem type and invented tools like `add[...]` in another.
- **At 3B, both modes hit the ceiling,** and ReAct cost 1.89× the tokens.
- **Without the stop sequence, the model writes its own fake `Observation:`.**

### Week 4: Research Methodology for Applied AI

| | |
|---|---|
| Anchor paper | *AI Agents That Matter* (Kapoor et al., 2025) |
| Lab | Design, on paper, an eval protocol for a specific claim, with explicit success and failure criteria |
| Notebooks | [`jupyter/week4_rigour_audit.ipynb`](jupyter/week4_rigour_audit.ipynb) · [`jupyter/week4_calibration_colab.ipynb`](jupyter/week4_calibration_colab.ipynb) · [`jupyter/week4_test_run_colab.ipynb`](jupyter/week4_test_run_colab.ipynb) |
| Code | [`src/stats.py`](src/stats.py) · [`src/react_tasks_v2.py`](src/react_tasks_v2.py) · [`src/protocol_analysis.py`](src/protocol_analysis.py) |
| Protocol (frozen) | [`protocol/week4_eval_protocol_v1.3.md`](protocol/week4_eval_protocol_v1.3.md) · [`protocol/week4_frozen_config.json`](protocol/week4_frozen_config.json) |
| Notes | [`notes/week_4/README.md`](notes/week_4/README.md) · [rigour memo](notes/week_4/rigour_memo.md) · [resources](notes/week_4/resources.md) · [sources](sources/week_4.md) · [article outlines](notes/week_4/articles/README.md) |
| Phase 1 log | [`notes/phase_1_log.md`](notes/phase_1_log.md): every paper claim from Weeks 1 to 4 and whether I reproduced it |

**Part 1: auditing my own claims.** I re-tested 15 claims from Weeks 2 and 3 using:
- confidence intervals
- comparisons on the same items
- a correction for testing many claims at once

8 held up and 7 weren't established. My Week 3 ReAct comparison had only a **10% chance** of detecting a 10-point difference. Picking the best prompt ordering on the test data overstated its advantage by 28% to 40%.

**Part 2: the protocol.** The claim under test: *at 1.5B and 3B, ReAct solves at least 10 points more held-out problems than tool-only prompting, at no more than 1.5× the tokens.* The plan went through four versions, each change recorded with its reason:

| Version | What changed it |
|---|---|
| 1.0 | First design, from the 0.5B result |
| 1.1 | The GPU pilot showed a ceiling (97% to 100%), so the problems became harder |
| 1.2 | Calibration v1 found no usable level, and showed my sentence shuffling made the text incoherent |
| 1.3 | Calibration v2 picked levels by a rule written in advance (1.5B: level 2, 3B: level 3) and raised N to 480 for enough power |

The protocol was frozen in a public commit before any test problem was run. The analysis code was written and tested on synthetic data before the test run, so it can't be tuned to the result.

---

## 5. Repository Map

```
.
├── README.md                     you are here
├── pyproject.toml, uv.lock       dependencies (managed with uv)
├── .python-version               3.12
├── jupyter/                      one or more notebooks per week, outputs saved
│   ├── week1_transformer_probing.ipynb
│   ├── week2_in_context_learning.ipynb
│   ├── week3_react_agent.ipynb   CPU run (0.5B)
│   ├── week3_colab.ipynb         GPU run (1.5B, 3B) on Colab or Kaggle
│   ├── week4_rigour_audit.ipynb  statistics audit, winner's curse, power analysis
│   ├── week4_calibration_colab.ipynb   difficulty calibration on the dev split
│   └── week4_test_run_colab.ipynb      the pre-registered test run
├── src/                          code imported by the notebooks
│   ├── icl.py                    few-shot formats, KV-cached label scoring, calibration
│   ├── react_agent.py            the ReAct agent, safe calculator, local LLM wrapper, CLI
│   ├── react_tasks.py            Week 3 problem set (30 problems)
│   ├── react_tasks_v2.py         Week 4 problem generator (4 difficulty levels, dev/test splits)
│   ├── run_react_bench.py        resumable benchmark runner and summaries (CLI)
│   ├── stats.py                  small-sample statistics (no scipy)
│   └── protocol_analysis.py      the pre-registered Week 4 analysis
├── protocol/                     frozen pre-registration for the Week 4 test run
├── results/                      raw per-item results and charts, by week
│   ├── week2/  week3/  week3_gpu/  week4/  week4_dev_v1/  week4_dev_v2/
├── sources/                      bibliography for the Week 4 work
└── notes/                        everything I wrote while learning
    ├── phase_1_log.md            reproduction log for Weeks 1 to 4
    └── week_1/ … week_4/
        ├── README.md             detailed notes for the week
        ├── resources.md          reading list, every link checked
        └── articles/             article plans, outlines, self-check questions
```

---

## 6. Setup

**Requirements:** [uv](https://docs.astral.sh/uv/) and Git. Python 3.12 is installed automatically by uv. No GPU is needed for Weeks 1, 2 and 4's audit; Weeks 3 and 4 use a free cloud GPU for the larger models.

```bash
git clone https://github.com/jorshimayor/AI-Engineering-Flow_Research.git
cd AI-Engineering-Flow_Research
uv sync
uv run jupyter lab
```

Models download from Hugging Face on first use and are cached (GPT-2 about 0.5 GB, Qwen2.5-0.5B about 1 GB; the 1.5B and 3B models are used on GPU only).

**Why the versions are pinned:**

| Pin | Reason |
|---|---|
| Python 3.12 | PyTorch 2.2.2 has no builds for newer Python on Intel macOS |
| `torch==2.2.2` | The last PyTorch release with Intel (x86_64) macOS wheels. This was developed on an Intel Mac |
| `numpy<2` | torch 2.2.2 was compiled against NumPy 1.x |
| `transformers<4.50` | Results were produced with 4.49; the Colab notebooks install exactly 4.49.0 |

On Apple Silicon, Linux or Windows you can loosen these pins, but results may differ slightly from the saved ones.

---

## 7. Running Things

### Notebooks on your machine

| Notebook | Runtime on a laptop CPU | Notes |
|---|---|---|
| Week 1 | about 1 minute | |
| Week 2 | about 2 to 3 hours the first time | Results are cached in `results/week2/`, so re-runs take minutes |
| Week 3 (CPU) | about 1 to 2 hours | Cached in `results/week3/` |
| Week 4 audit | about 2 minutes | No models: it reads saved results |

Run a notebook headless with:
```bash
uv run jupyter nbconvert --to notebook --execute --inplace jupyter/week1_transformer_probing.ipynb
```

### Notebooks on a free GPU (Colab or Kaggle)

| Notebook | What it does | GPU time on a T4 |
|---|---|---|
| [Week 3 on GPU](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week3_colab.ipynb) | Week 3 benchmark at 1.5B and 3B | about 30 minutes plus model downloads |
| [Week 4 calibration](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week4_calibration_colab.ipynb) | Picks difficulty levels on the dev split | about 60 to 90 minutes |
| [Week 4 test run](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week4_test_run_colab.ipynb) | The pre-registered test (480 problems per model) | about 7.5 hours, resumable |

On Colab: open the link, `Runtime → Change runtime type → T4 GPU`, then `Runtime → Run all`. Every runner saves one result at a time to Google Drive, so a disconnect only loses the problem in progress. On Kaggle (about 30 free GPU hours a week): import the notebook, enable GPU and Internet in Settings, and set `USE_DRIVE = False`.

### The agent from the command line

```bash
uv run python src/react_agent.py "A truck carries 1,284 boxes with 36 cans each. 2,050 are damaged. How many good cans?"
uv run python src/react_agent.py --no-stop "..."      # see the model invent its own tool result
```

### The benchmark runner

```bash
# Week 3's 30 problems, all four modes, any model (uses a GPU if present)
uv run python src/run_react_bench.py --model Qwen/Qwen2.5-1.5B-Instruct

# Week 4 dev split at a difficulty level
uv run python src/run_react_bench.py --task dev --level 2 --modes act react --max-steps 8

# Summaries (accuracy with 95% CIs, cost, format failures, paired ReAct vs Act test)
uv run python src/run_react_bench.py --summary results/week3_gpu/*.jsonl
```

---

## 8. The Code

| Module | What's in it | Key functions |
|---|---|---|
| [`src/icl.py`](src/icl.py) | Few-shot prompting experiments | `Format` (template, labels, separators), `sample_demos`, `score` (KV-cached label log-probs), `evaluate`, `summarise` |
| [`src/react_agent.py`](src/react_agent.py) | The ReAct agent | `calculate` (safe AST evaluator), `system_prompt`, `LocalLLM` (CPU or GPU, stop strings), `run_agent` (the loop) |
| [`src/react_tasks.py`](src/react_tasks.py) | Week 3 task set | `make_problems` (the 30 Week 3 problems), `correct` |
| [`src/react_tasks_v2.py`](src/react_tasks_v2.py) | Week 4 task generator | `make_problems(split, level)`, `check_problems` (answers verified against solution expressions), `leakage_check` |
| [`src/run_react_bench.py`](src/run_react_bench.py) | Benchmark runner and CLI | `run` (resumable), `summary`, `failure_type`, `is_format_failure` |
| [`src/stats.py`](src/stats.py) | Small-sample statistics | `wilson_ci`, `paired_bootstrap_ci`, `mcnemar_exact`, `sign_flip_test`, `fisher_exact`, `holm`, `power_mcnemar`, `n_for_power` |
| [`src/protocol_analysis.py`](src/protocol_analysis.py) | Pre-registered Week 4 analysis | `analyse` (gates, McNemar, Holm, outcome rules, leave-one-template-out, cost ratio), `print_report` |

Design choices worth knowing:
- **The calculator never calls `eval`.** It walks the expression's syntax tree and allows only numbers and arithmetic, because model output is untrusted input.
- **Tool errors are returned to the model as observations**, so the agent can recover instead of crashing.
- **Every Week 4 problem carries a solution expression**, and `check_problems` verifies each answer with the agent's own calculator.
- **Runners append one JSON line per problem** and skip finished ones, so long GPU runs survive disconnects.

---

## 9. Results and Data Formats

| Folder | Contents |
|---|---|
| `results/week2/` | `icl_runs.jsonl` (140 few-shot configurations), `passkey.json`, charts |
| `results/week3/` | `runs.jsonl` (0.5B, 120 runs with full trajectories), chart |
| `results/week3_gpu/` | 1.5B and 3B runs (120 each), comparison chart |
| `results/week4/` | `claim_audit.json`, `power_table.json`, five charts |
| `results/week4_dev_v1/`, `results/week4_dev_v2/` | Difficulty calibration runs and `calibration.json` records |

**Agent run records** (one JSON object per line):

| Field | Meaning |
|---|---|
| `id` | `"<mode>\|<problem id>"`, unique within a file |
| `model`, `mode` | Model name; `direct`, `cot`, `act` or `react` |
| `pid`, `template`, `split`, `level` | Problem id, problem type, dataset split and difficulty |
| `gold`, `answer`, `correct` | The right answer, the agent's answer, whether they match exactly |
| `status`, `steps`, `tool_calls` | `ok`, `max_steps` or `invalid_action`; LLM calls; calculator calls |
| `tokens_in`, `tokens_out`, `seconds` | Cost of the episode |
| `trajectory`, `observations` | The full Thought/Action/Observation text, and the tool results |

**Few-shot run records** (`results/week2/icl_runs.jsonl`): `id`, `exp` (count, order, format, labels or balance), `fmt`, `k`, `seed`, `acc`, `acc_cal` (after calibration), `pos_rate`, `label_mass`, `prefix_tokens`, and per-review label log-probs (`logp`, `cf_logp`), so every metric can be recomputed.

---

## 10. How I Report Results

Since Week 4, every result follows these rules (from the [rigour memo](notes/week_4/rigour_memo.md)):

- **Every accuracy has a 95% confidence interval** (Wilson intervals for proportions).
- **Comparisons are paired:** both conditions run on the same items, tested with exact McNemar or a paired bootstrap.
- **"No difference" needs an equivalence test**, not just a non-significant p-value.
- **Many claims, one correction:** Holm adjustment when testing several things at once.
- **Cost sits next to accuracy**, on a cost-accuracy plot, following Kapoor et al.
- **Pre-register confirmatory tests:** claim, sample size, analysis and pass/fail rules are fixed and committed before the data exists. Anything else is labelled exploratory.

Results from before Week 4 are kept as they were, with the audit's verdict noted beside them.

---

## 11. Notes, Resources and Articles

**Notes** (`notes/week_N/README.md`) are the main write-up for each week:
- a one-page summary of the paper
- setup and design decisions
- every result with its table and chart
- what went wrong
- key takeaways and next experiments

**Resources** (`notes/week_N/resources.md`) list papers, YouTube videos, courses, articles, interactive tools and code, each marked by level. Every link was checked when the list was written.

**Articles** (`notes/week_N/articles/`) are plans for public write-ups. For each week:
- how many articles and why
- an outline per article, with word budgets and the exact numbers to use
- self-check questions to answer before writing
- one new "stretch" experiment
- hooks for a newsletter and a video

Week 4's outlines follow a reader-needs format with SEO metadata.

**Phase 1 log** ([`notes/phase_1_log.md`](notes/phase_1_log.md)) lists every paper claim probed in Weeks 1 to 4 and whether it was reproduced: 12 reproduced fully, partly or in direction; 1 not established; 2 not reproduced.

---

## 12. Known Limitations

- **Small models only** (GPT-2 small, Qwen2.5 0.5B to 3B), chosen to run on free hardware. Some findings are known to change with scale.
- **Single model families** (GPT-2 in Week 1, Qwen2.5 after that).
- **Small or synthetic tasks:** SST-2 sentiment, and generated arithmetic word problems.
- **Greedy decoding** for most comparisons, which hides run-to-run variance.
- **Early results are weaker than later ones.** Weeks 1 to 3 were written before the Week 4 standards; where the audit found a claim unsupported, that's noted.
- **Version pins** are set for an Intel Mac. Other platforms may give slightly different numbers.

---

## 13. Roadmap

| Weeks | Phase | Focus |
|---|---|---|
| 1 to 4 | Phase 1: Foundations | Done (Week 4's test run pending) |
| 5 to 8 | Phase 2: Applied Foundation | Systematic prompting, structured outputs and tool calling (including MCP), retrieval-augmented generation (RAG) basics, building eval sets |
| 9 to 11 | Phase 3: Agentic Systems | Multi-step agents, memory and context management, agent evaluation and failure analysis |
| 12 to 14 | Phase 4: Retrieval Systems | Vector search, hybrid search and reranking, retrieval evaluation |
| 15 to 16 | Capstone 1 | One complete research loop |
| 17 to 48 | Deep dive | Chosen specialisation, research proposal, build, hardening, write-up |

Next immediate step: run the Week 4 test (`jupyter/week4_test_run_colab.ipynb`) and publish the pre-registered result, whichever way it goes.

---

## 14. Troubleshooting

| Problem | Fix |
|---|---|
| `uv sync` tries to install a PyTorch that doesn't exist | Make sure uv uses Python 3.12 (`.python-version`). On Intel Macs, newer Python has no PyTorch 2.2.2 build |
| `jupyter` command points to an old path after moving the folder | Recreate the environment: `rm -rf .venv && uv sync` |
| Colab says it can't find a notebook | Colab reads from GitHub's `main` branch: the file has to be merged there first |
| Colab runs old code after an update | The notebooks now always fetch the latest code; if in doubt, `Runtime → Disconnect and delete runtime` and run again |
| SSL certificate errors from Python scripts | The system Python on macOS may lack certificates; use `uv run python …` instead |
| A long GPU run disconnected | Re-run the same cell: finished problems are skipped |

---

## 15. Acknowledgements and Contact

- **Curriculum:** the Applied AI Engineering Fellowship at Flow Research. Each week's anchor paper and lab come from its guide.
- **Papers reproduced or probed:** Vaswani et al. (2017), Brown et al. (2020), Yao et al. (2022), Kapoor et al. (2025), and the follow-up work cited in each week's notes and in [`sources/`](sources/).
- **Models and data:** GPT-2 (OpenAI), Qwen2.5 (Alibaba), SST-2 (Stanford), via Hugging Face.

Find me here:
- Website and portfolio: [jorshimayor.is-a.dev](https://jorshimayor.is-a.dev)
- Articles: [jorshimayor.hashnode.dev](https://jorshimayor.hashnode.dev)
- Newsletter: [jorshimayor.substack.com](https://jorshimayor.substack.com)
- Videos: [youtube.com/@jorshimayor](https://www.youtube.com/@jorshimayor)
- X: [@jorshimayor](https://x.com/jorshimayor)
- LinkedIn: [jorshimayor](https://linkedin.com/in/jorshimayor)

Questions, corrections and "I tried this and got something different" are all welcome: open an issue on this repository.
