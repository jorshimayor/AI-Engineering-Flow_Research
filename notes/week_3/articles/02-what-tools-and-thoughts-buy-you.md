# Article 2: What tools and thoughts buy you (outline)

## Title options
- **My Agent Got the Math Right and the Answer Wrong**
- Tools Fix Arithmetic, Not Reasoning: Lessons From 120 Agent Runs
- Does Thinking + Acting Beat Thinking Alone? A Small-Model Reality Check on ReAct

**Target reader:** has read Article 1 or built an agent; wants evidence about *when* reasoning and tools help.
**Promise:** a clear picture of what each part of an agent contributes, the failure modes to watch for, and why model size matters.
**Length:** ~1,500 words · **Hero:** `accuracy_by_mode.png`

---

## Outline

### 1. Hook (~120 words)
Show the trajectory: the calculator returns **577016** (correct), then the model's next Thought subtracts 1,331 *again* and answers 575685. "The tool did its job. The reasoning undid it."

### 2. The experiment (~200 words)
- 30 big-number two-step word problems, 4 modes (Direct, CoT, Act, ReAct): the paper's ablation, reproduced on a 0.5B model.
- Same exemplar problems in every mode; only the trajectory format changes.

### 3. Results (~250 words)
The results table. Headline: **0%, 0%, 23%, 20%.**

### 4. Lesson 1: tools turn near misses into plan errors (~250 words)
- CoT's wrong answers: median **4.9%** off ("606 × 42 = 25,592"; truth 25,452).
- Act/ReAct wrong answers: **89–97%** off (dropped "140 employees", added instead of multiplied).
- Maps directly onto the paper: CoT fails by hallucination, ReAct by reasoning errors.

### 5. Lesson 2: thoughts need a capable thinker (~250 words)
- ReAct ≈ Act at 0.5B (6 vs 7 out of 30).
- The paper saw the same: prompted ReAct worked with PaLM-540B, while small models needed fine-tuning.
- Ignored-observation failures (3/30): reasoning *overriding* tool output.

### 6. Lesson 3: the agent can only do what its exemplars show (~200 words)
- Almost all successes are on the template that matches exemplar 2 (crates ≈ bolts-into-bags).
- Link to Week 2: demos teach format and *plan shape*. Exemplar coverage is a design decision.

### 7. Lesson 4: agents cost more (~150 words)
About 9× the input tokens, about 3 calls per problem, and why prompt caching exists.

### 8. What I'd do in production (~150 words)
A bigger model, native tool calling, exemplars covering each task shape, a verification step ("does the final answer equal the last observation?"), step caps, and logging every trajectory.

### 9. Reproduce this

---

## Stretch experiment (new work, makes the article much stronger)
**Scale it up.** Run `act` and `react` with **Qwen2.5-1.5B-Instruct** on 10–15 problems (about 3 min each on this CPU; run it overnight), or with a hosted model via API. Then add a "0.5B vs bigger" column.
- If ReAct overtakes Act at the larger size, you've reproduced the paper's scale finding.
- If not, you have a genuinely interesting counter-result.

Cheap alternative: add a **verifier rule**. If `finish[x]` ≠ the last observation, reject it and ask again. Measure how many of the 3 "ignored observation" failures it fixes.

## Self-check (closed-book)
1. Why can't CoT alone solve these problems, even with a perfect plan?
2. Why are tool-using agents' wrong answers *further* from the truth than CoT's?
3. What's the difference between a *hallucination* failure and a *reasoning* failure?
4. Why might adding Thoughts *hurt* a small model?
5. How would you design exemplars to cover more problem shapes without making the prompt huge?
6. Estimate the token cost of a 5-step ReAct episode with a 500-token prompt. Why does it grow faster than linearly?
