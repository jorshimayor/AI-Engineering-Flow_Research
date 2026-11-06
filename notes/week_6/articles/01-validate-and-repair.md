# Article 1: Validate and repair (outline)

## Title options
- **My Agent Called the Calculator Before It Knew the Prices**
- Repairing Malformed Tool Calls: +9 Points, and the Failures It Can't Reach
- Schema Validation Catches Bad JSON, Not Bad Plans

**Target reader:** wires tools into an LLM app, trusts the function-calling format, hasn't counted how often it breaks.
**Promise:** how to build a tool-calling loop that never executes a bad reply, what a repair loop buys, and the failure that no schema can catch.
**Length:** ~1,500 words · **Hero:** `week6_success_by_route.png`

---

## Outline

### 1. Hook (~120 words)
A shopping question: 6 jars of pesto and 2 loaves. The model asks for both prices and, in the same breath, asks the calculator for `6 * lookup_price('basil pesto') + ...`. The calculator refuses. The model answers 80.90. The right answer is 56.92.

### 2. Toolformer in one paragraph (~150 words)
- A tool call is text the model writes, so it can be badly formed or badly timed.
- Toolformer learns *when* a call helps. Native function calling gives the format, not the judgement.

### 3. The pipeline (~300 words)
- Two tools: `lookup_price` (random prices, so the model must call it) and `calculate` (Week 3's safe parser).
- Every reply classified: tool calls, a final `{"answer": N}`, or one of four malformed types.
- A malformed reply is never run. The model is told what was wrong, up to 3 times.
- A well-formed call that fails is a tool error, returned as the result ("Did you mean 'lemons'?").
- Show `parse_reply`: about 40 lines that make the loop fail safe.

### 4. Testing repair honestly (~200 words)
- Fail-closed = the same runs, scored as failed at the first malformed reply. Paired, so no second run needed.
- H1 committed before the run: repair adds ≥ 5 points at each size.

### 5. Results (~250 words)
- 3B: +9.0 points (CI +5.5 to +13.0), 18 runs rescued, none broken. Supported.
- 1.5B: +0. It solves 3 of 200 either way, so there is nothing to rescue. Not supported, and not informative.
- Which shapes repair fixes (an answer as a string) and which it doesn't (a stray `>`, a call without tags, greedy repeats).

### 6. The failure a schema can't see (~250 words)
- 96% of 1.5B runs and 71% of 3B runs called `calculate` before any price came back.
- Valid JSON, valid schema, wrong order. It shows up as a tool error, so repair never touches it.
- Runs that never got a successful calculation: 4 of 409 correct.

### 7. What I'd change (~150 words)
Tell the model to wait for results (or allow one call per turn). Write a repair message per failure shape. Add a little sampling on retries. Put a minimum-success gate on the dev check: mine passed at 0 of 12.

### 8. Reproduce this
Colab link, about 1 hour on a free T4.

---

## Stretch experiment
**One call per turn.** Reject any reply with more than one tool call (as a new malformed type) and re-run 3B on the direct route. Measure how much of the planning failure disappears and what it costs in turns.

## Self-check (closed-book)
1. What is the difference between a malformed reply and a tool error in this pipeline, and why does it matter for repair?
2. Why can fail-closed be scored from the same runs as repair?
3. Why does the 1.5B H1 result say nothing about whether repair works?
4. Name two malformed shapes that repair fixed and two it didn't.
5. What does Toolformer learn that native function calling doesn't give you?
