# Article 1: Chain-of-thought at small scale (outline)

## Title options
- **Chain-of-Thought Still Works at 0.5B**
- The Scale Threshold That Didn't Hold: Reproducing Chain-of-Thought on Small Models
- Five Prompts, 4,000 Answers: Testing Chain-of-Thought Before Trusting It

**Target reader:** builds with LLMs, has heard "let's think step by step", hasn't measured it.
**Promise:** what chain-of-thought buys on maths problems, how to test a prompt change properly, and why the paper's scale claim needs updating for instruction-tuned models.
**Length:** ~1,500 words · **Hero:** `week5_strategy_accuracy.png`

---

## Outline

### 1. Hook (~120 words)
Wei et al. (2022): chain-of-thought helped only near 100B parameters, and hurt smaller models. On Qwen2.5-0.5B, the same idea took GSM8K accuracy from 6.8% to 35.2%.

### 2. The paper in one paragraph (~150 words)
- Few-shot examples that show the working, not just the answer.
- PaLM 540B: 18% to 57% on GSM8K. Below about 10B: little or no gain.

### 3. The prompt library (~250 words)
- Five strategies: zero-shot direct, few-shot direct (the paper's baseline), zero-shot CoT, few-shot CoT, few-shot CoT + JSON.
- 8 original worked examples, checked by script. Examples as chat turns.
- Show the `Strategy` dataclass: a prompt is a template plus a parser.

### 4. Testing it like an experiment (~250 words)
- Hypotheses committed before the run (H1: ≥10 points at each size).
- Prompts and parsers fixed on GSM8K *train* problems only; 400 test problems run once.
- Paired design: every strategy sees the same 400 problems, compared with McNemar and Holm.
- Link back to Week 4's lesson: decide what would change your mind first.

### 5. Results (~250 words)
- H1 supported: +28.5 points at 0.5B (CI +23.0 to +34.0), +48.0 at 1.5B (CI +42.8 to +53.2).
- Direct answering: 2% to 10%. Examples without working barely help.
- The gain grows with size (28 → 48), which agrees with the paper's direction, if not its threshold.

### 6. Why the threshold moved (~200 words)
- The paper's small models were base models; Qwen2.5 is instruction-tuned on reasoning data.
- What this run can't tell apart: instruction tuning vs scale vs newer data. Say so plainly.

### 7. What I'd do in production (~150 words)
Default to few-shot CoT for multi-step maths at small sizes. Keep the examples short. Measure on your own task before trusting any paper's threshold.

### 8. Reproduce this
Colab link, about 40 minutes on a free T4.

---

## Stretch experiment
**Add self-consistency.** Sample 5 chain-of-thought answers at temperature 0.7 and take the majority vote (Wang et al., 2022). Measure the gain over greedy few-shot CoT at 0.5B and 1.5B, and the 5× token cost.

## Self-check (closed-book)
1. What is the difference between "standard prompting" and chain-of-thought prompting in the paper?
2. Why were prompts tuned on train problems, not test problems?
3. Why does a paired test need fewer problems than comparing two independent accuracy figures?
4. Name two reasons the scale threshold might not hold for a 2024 model.
5. Direct answering scored 2% to 10%. What does that say about whether the model "knows" the answers?
