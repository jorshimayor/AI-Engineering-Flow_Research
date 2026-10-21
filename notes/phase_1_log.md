# Phase 1 Log: Foundations (Weeks 1 to 4)

The Phase 1 deliverable: a documented log of each week's probes and reproductions, plus the [rigour memo](week_4/rigour_memo.md). Each "reproduced?" verdict below uses the Week 4 audit standards (paired tests, 95% CIs, Holm correction).

## Exit artefacts
| Artefact required | Where |
|---|---|
| Reproduced-paper log | This file |
| Small prompted-agent demo | [`src/react_agent.py`](../src/react_agent.py) (`uv run python src/react_agent.py "question"`) |
| Memo on evaluating a claim rigorously | [week_4/rigour_memo.md](week_4/rigour_memo.md) |

## Week by week

### Week 1: Transformer mechanics
**Paper:** Attention Is All You Need (Vaswani et al., 2017) · **Model:** GPT-2 small · [notes](week_1/README.md) · [notebook](../jupyter/week1_transformer_probing.ipynb)

| Paper claim / concept | My probe | Result | Reproduced? |
|---|---|---|---|
| Attention = softmax(QKᵀ/√dₖ)·V with a causal mask | Rebuilt layer-0 attention by hand from the weights | Matches the model exactly; future weights are exactly 0 | **Yes**, exact |
| Positional information is added to token embeddings | Plotted GPT-2's learned position embeddings | Smooth, wave-like structure similar to the paper's sinusoids | **Qualitatively** |
| Generation is next-token prediction in a loop | Hand-written KV-cached greedy loop | Identical output to `model.generate` | **Yes**, exact |
| (Probe) Tokenisation shapes behaviour | Edge cases across languages, numbers, spaces | Trailing space drops P(Paris) from rank 5 to rank 1,472; Hindi costs 5.4× English tokens | Original finding |

### Week 2: In-context learning
**Paper:** Language Models are Few-Shot Learners (Brown et al., 2020) · **Model:** Qwen2.5-0.5B base · [notes](week_2/README.md) · [notebook](../jupyter/week2_in_context_learning.ipynb)

| Claim (paper or follow-up) | My probe | Result | Reproduced? |
|---|---|---|---|
| Few-shot beats zero-shot (Brown et al.) | k = 0 to 16, 5 demo sets each | 16-shot +2.7 pts, CI −1.7 to +7.3 | **Not established** at 0.5B on SST-2 |
| Demos teach format more than mapping (Min et al., 2022) | Gold vs random labels, k = 8 | Random labels cost 1.2 pts, CI inside ±5 | **Yes** |
| Small models ignore flipped labels (Wei et al., 2023) | All labels flipped | Still 84% accurate (≫ 50%) | **Yes** |
| Order and majority-label biases (Zhao et al., 2021; Lu et al., 2021) | 48 orderings; 0 to 4 positive demos | Recency +10.9 pts positive predictions; order gap 4.8 to 6.7 pts on held-out items | **Yes**, smaller than in Lu et al. |
| Contextual calibration fixes biased prompts (Zhao et al.) | Calibrated vs raw | Rescues a collapsed template (+29 pts) but breaks arbitrary labels (−28 pts) | **Partly** |
| Lost in the middle (Liu et al., 2023) | Passkey at 512 to 8,192 tokens | 100% retrieval everywhere | **Not reproduced** (test too easy) |

### Week 3: ReAct
**Paper:** ReAct (Yao et al., 2022) · **Model:** Qwen2.5-0.5B-Instruct · [notes](week_3/README.md) · [notebook](../jupyter/week3_react_agent.ipynb)

| Paper claim | My probe | Result | Reproduced? |
|---|---|---|---|
| CoT fails by hallucination; tools ground it | 30 big-number word problems, 4 modes | CoT 0/30 with near-miss arithmetic (median 4.9% off); tool modes 6 to 7/30 | **Direction yes**, not significant after correction (n = 30) |
| ReAct > Act-only | Paired comparison at 0.5B (laptop), 1.5B and 3B (Colab) | 0.5B: 20% vs 23% (inconclusive). 1.5B: **67% vs 97%, −30 pts, p = 0.012**. 3B: both 100%, ReAct 1.89× the tokens | **Not reproduced**: reasoning traces hurt at 1.5B; no headroom at 3B |
| Prompted ReAct needs a large model | 0.5B, 1.5B, 3B | ReAct goes 20% → 67% → 100%, but Act-only gets there first (23% → 97% → 100%) | **Partly**: ReAct does need size, but the task was too easy to show a benefit over Act |

### Week 4: Research methodology
**Paper:** AI Agents That Matter (Kapoor et al., 2025) · [notes](week_4/README.md) · [notebook](../jupyter/week4_rigour_audit.ipynb)

| Paper claim | My probe | Result | Reproduced? |
|---|---|---|---|
| Accuracy-only evals favour costly agents | Week 3 on a cost-accuracy plot | ReAct dominated by Act-only (26% more tokens, no gain) | **Yes**, on my own agent |
| Missing holdouts inflate results | Best-of-24 ordering, split-half | Gap shrank 28% to 40% on held-out items | **Yes** |
| Results need repeated runs and CIs | Audit of 15 of my claims | 7 of 15 not established once CIs and Holm were applied | **Yes** |

## Scorecard
| | Count |
|---|---|
| Paper claims probed | 15 |
| Reproduced (fully, partly or in direction) | 12 |
| Not established or untestable at my scale | 1 |
| Not reproduced | 2 (lost in the middle, because the test was too easy; ReAct > Act-only, reversed at 1.5B) |

## Habits carried into Phase 2
1. Every result gets a 95% CI and the N behind it.
2. Every comparison is paired, on the same items.
3. A power analysis comes before any experiment meant to settle a question.
4. Prompt and parser tuning happens on a dev split, never on test.
5. Accuracy is always plotted against cost.
