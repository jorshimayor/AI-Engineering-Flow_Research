# Article 2: Format is half the score (outline)

## Title options
- **Half My Model's Wrong Answers Were Right**
- The JSON Tax: What Structured Output Costs a Small Model
- Your Eval Is Grading the Format: Strict vs Lenient Scoring on GSM8K

**Target reader:** writes evals or parsers for LLM output; uses JSON mode or "answer in this format" instructions.
**Promise:** how format failures hide inside accuracy numbers, how to measure them separately, and what few-shot examples are really for.
**Length:** ~1,400 words · **Hero:** `week5_strategy_accuracy.png` (the blue lenient ticks)

---

## Outline

### 1. Hook (~120 words)
The model's answer: "Therefore, Cindy had a total of 27 eggs." Correct. My parser marked it wrong, because I asked for "The answer is N." At 1.5B, zero-shot CoT scored 30% strict and 66% lenient.

### 2. Two scores for every answer (~200 words)
- Strict: the answer in the requested format. Lenient: the last number in the output.
- The gap is the cost of format failures, separate from reasoning.
- Caveat up front: lenient can credit a coincidence, so it's exploratory.

### 3. Zero-shot CoT reasons fine and ignores the format (~250 words)
- Format failures: 46% at 0.5B, 59% at 1.5B (`\boxed{}`, "Therefore, ...").
- Scored leniently, it beats few-shot CoT: +7.5 points at 0.5B, +5.8 at 1.5B (exploratory).
- So what do the 8 worked examples buy? Format compliance and 2.5 to 3.2 times shorter answers.

### 4. The JSON tax (~300 words)
- Pre-registered H2: JSON within ±5 points of plain CoT.
- 0.5B: −19.3 points (CI −24.3 to −14.3), a real tax. Leniently, only −2.3: the reasoning survived; the JSON didn't (62% unparseable or missing `answer`).
- 1.5B: −4.5 (CI −9.3 to +0.3), inconclusive. Explain why "not significant" isn't "no difference", and what sample would settle it (about 1,010 problems).
- Link to Tam et al. (2024), "Let Me Speak Freely?".

### 5. Cost per correct answer (~150 words)
- Few-shot prompts add about 650 prompt tokens but cut answer tokens: 174 vs 842 per correct answer at 1.5B.
- Prompt tokens are cheaper and cacheable; answer tokens set latency.

### 6. What I'd do in production (~200 words)
- Report strict and lenient side by side in every eval.
- Use constrained decoding (Outlines, JSON mode) instead of asking nicely, especially below 1B.
- Put the format in the examples, not only the instructions.
- Reason first in plain text, then convert to JSON in a second step if the model is small.

### 7. Reproduce this

---

## Stretch experiment
**Constrained JSON.** Rerun few-shot CoT + JSON at 0.5B with Outlines enforcing the schema. If strict accuracy returns to about 35%, the whole tax was format; if not, constraining the output also costs reasoning.

## Self-check (closed-book)
1. Why report strict and lenient accuracy separately instead of only the higher one?
2. How can lenient scoring overstate accuracy?
3. What does a CI of −9.3 to +0.3 against a ±5 margin let you conclude?
4. Why might JSON hurt a 0.5B model more than a 1.5B model?
5. Prompt tokens vs answer tokens: which dominates latency, and why?
