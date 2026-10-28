# Week 5: Systematic Prompt Engineering

**Paper:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) (Wei et al., 2022)
**Lab:** build a small prompt library for a fixed task, comparing three or more strategies with documented deltas.
**Code:** [`src/prompts.py`](../../src/prompts.py) (library) · [`src/gsm8k.py`](../../src/gsm8k.py) (data) · [`src/run_prompt_bench.py`](../../src/run_prompt_bench.py) (batched runner)
**Notebook:** [`week5_prompt_library_colab.ipynb`](../../jupyter/week5_prompt_library_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week5_prompt_library_colab.ipynb) (about 40 minutes on a free T4)

**Status:** plan fixed and committed; test run pending.

## The paper in brief

| | |
|---|---|
| Method | Few-shot prompts whose examples show intermediate reasoning steps, not just answers |
| Main result | Large gains on GSM8K and other reasoning benchmarks for models around 100B parameters (PaLM 540B: 18% to 57% on GSM8K) |
| Scale claim | Below roughly 10B parameters, chain-of-thought gave little or no gain, or hurt |
| Why test it now | Modern small models are instruction-tuned on reasoning data. Does the scale threshold still hold at 0.5B and 1.5B? |

## The prompt library

| Strategy | Prompt | Output the parser requires |
|---|---|---|
| `zero_shot_direct` | Instruction only | `The answer is N.` |
| `few_shot_direct` | 8 worked examples showing only answers (the paper's "standard prompting"; **baseline**) | `The answer is N.` |
| `zero_shot_cot` | Instruction plus "Let's think step by step." (Kojima et al., 2022) | Reasoning, then `The answer is N.` |
| `few_shot_cot` | 8 worked examples with reasoning steps (Wei et al., 2022) | Reasoning, then `The answer is N.` |
| `few_shot_cot_json` | Same examples, output as JSON | `{"reasoning": "...", "answer": N}` |

- The 8 examples are original, in the paper's style. Every step was checked by script.
- Chat models get the examples as alternating user and assistant turns.
- Decoding: greedy, a 512-token budget for every reasoning strategy, 24 tokens for direct answers.

Scoring:
- **strict:** the answer in the requested format (the primary metric)
- **lenient:** the last number in the output, whatever the format
- The gap between strict and lenient is the cost of format failures.

## Plan (fixed before the test run)

**Data:** 400 GSM8K test problems (fixed seed). Prompts and parsers were developed only on GSM8K **train** problems (`gsm8k.dev()`). The test set is run once.

**Models:** Qwen2.5-0.5B-Instruct and Qwen2.5-1.5B-Instruct.

| | Hypothesis | Test | Supported if |
|---|---|---|---|
| **H1** (confirmatory) | Few-shot CoT beats few-shot direct by at least 10 points, at each size | Exact McNemar, paired bootstrap CI, Holm across the 2 models | Holm p < 0.05, CI lower bound > 0, effect ≥ 10 points |
| **H2** (confirmatory) | Asking for JSON costs little: few-shot CoT JSON within ±5 points of plain few-shot CoT (strict) | Paired bootstrap 95% CI | Whole CI inside ±5 points. Outside it in either direction: a real structure tax or gain |
| Exploratory | Zero-shot vs few-shot; strict vs lenient; format-failure rates; tokens per answer (cost) | Wilson CIs, paired CIs | Reported, no significance claims |

**Power:** the paper and the Week 3 runs suggest direct answering scores far below reasoning (at least 20 points apart), so 400 paired problems gives more than 99% power for H1. For H2 the CI half-width is expected to be about 4 points, enough to establish equivalence only if the true gap is near zero.

**Changes made on dev before freezing** (library v1.1): the answer-line parser accepts LaTeX wrappers the model adds (`the answer is \( \boxed{9} \)`). The reasoning budget was raised from 384 to 512 tokens after truncated outputs.

## Results

*Pending the Colab run.*

## Files

- Results (after the run): `results/week5/` (one JSONL per model)
- Reading list: [`resources.md`](resources.md)
