# Article 1: What moves few-shot accuracy (outline)

## Title options
- **I Ran 140 Few-Shot Experiments. Here's What Actually Matters.**
- Format > Examples: A Controlled Study of Few-Shot Prompting
- Your Few-Shot Examples Matter Less Than Your Template

**Target reader:** a developer who writes prompts with examples and has never measured whether they help.
**Promise:** a ranked list of what to worry about when building a few-shot prompt, backed by controlled experiments.
**Length:** ~1,600 words · **Hero figure:** `summary_effects.png`

---

## Outline

### 1. Hook (~100 words)
"Everyone says 'add a few examples'. I changed one thing at a time (number, order, template, label words, even whether the labels were *correct*) across 140 runs. The thing people obsess over least mattered most."

Show the summary chart right away.

### 2. Setup (~200 words)
- One task (SST-2 sentiment), one model (Qwen2.5-0.5B base), the same 150 test reviews every time.
- Scoring: compare P(" positive") vs P(" negative"). It's deterministic, so every difference comes from the prompt.
- Show an example prompt (2 demos plus a query).
- Mention the KV-cache trick in one sentence (it made 140 runs feasible on a laptop CPU).

### 3. Results, one section per factor (~900 words)
For each: the claim, a table or chart, and one practical takeaway.

1. **Template: 36–41 points.** The "question" template scored 49%, *below chance*, because it predicted "negative" 97% of the time. Explain why: the template ends in "positive or negative?", so "negative" is the most recently mentioned label. Use `e3_format.png`.
2. **Label words: 31 points.** `great/terrible` 89% > `positive/negative` 85% ≫ `1/0` 58%. Natural words carry a prior; digits don't.
3. **Number of shots: 16 points, but not how you'd expect.** **One-shot (74%) is worse than zero-shot (87%).** More shots mostly reduce variance (std 0.10 → 0.01). Use `e1_count.png`.
4. **Label balance: 12 points.** Each extra positive demo adds about 8 points of "positive" predictions. Use `e5_balance.png`.
5. **Order: 8–9 points.** Same 4 demos, 24 orderings, 82%–90%. Recency bias: last demo positive → +10 pts positive predictions. Use `e2_order.png`.
6. **Which demos: 7 points.**
7. **Label correctness: 6 points.** Random labels cost about 1 point. (Tease Article 2: "Why? Next article.")

### 4. Caveats (~150 words)
- One small model and one easy task. Order effects are known to be bigger for harder tasks and other models (Lu et al.).
- 150 test examples gives a standard error of about ±2.7 points. Treat differences under ~5 points as noise.

### 5. A checklist for practitioners (~150 words)
1. Try 3–5 templates before you touch the examples.
2. Use natural label words.
3. Use ≥4 balanced shots, or none. Avoid exactly one.
4. Alternate labels and don't end on the majority class.
5. Measure: build a 100-example eval before you tune prompts.

### 6. Reproduce this
Link the notebook, `src/icl.py` and `results/week2/icl_runs.jsonl`.

---

## Stretch experiment (new work)
**Is it the model or the task?** Re-run E2 (order) and E3 (format) with **Qwen2.5-1.5B**. If format sensitivity shrinks with scale, that's a headline result of your own. If it doesn't, that's just as interesting.

## Self-check (closed-book)
1. Why score with label log-probs instead of generating text? What does that rule out?
2. Why reuse the same 150 test reviews across all runs?
3. Give two reasons one-shot could do worse than zero-shot.
4. What is recency bias, and how would you design demos to cancel it?
5. Why would `great/terrible` beat `positive/negative`?
6. With 150 test examples, how big must a difference be before you believe it?
