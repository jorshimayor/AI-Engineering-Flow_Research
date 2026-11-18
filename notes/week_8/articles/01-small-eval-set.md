# Article 1: A small eval set (outline)

## Title options
- **Forty-Five Test Cases Told Me More Than 800 Benchmark Questions**
- Write Down Your Predictions Before You Run the Eval
- Husain's Level 1, Applied to Three Small Systems

**Target reader:** has scored an LLM system with one accuracy number and isn't sure what to test next.
**Promise:** how to write 15 cases per system that each test one behaviour, check them in a few lines of code, run them enough times to spot luck, and keep the result as a regression gate.
**Length:** ~1,500 words · **Hero:** `week8_scorecard.png`

---

## Outline

### 1. Hook (~120 words)
Weeks 5 to 7 gave me three headline numbers: 58% on maths prompts, 31.5% for a shopping agent, 97.5% for RAG. None of them said which behaviours fail. Forty-five hand-written cases did.

### 2. Husain in one paragraph (~150 words)
- Stalled AI products share a cause: no way to tell whether a change helped.
- Three levels: unit-test assertions, human and model review of traces, A/B tests.
- The pass rate doesn't have to be 100%; it is a product decision.

### 3. Writing the cases (~300 words)
- Five typical, five known failures, five edge cases per system, each with a one-line reason.
- Known failures come from earlier weeks' traces: "bottle of maple syrup", calculate before prices, the colour question that retrieved the wrong chunk.
- Edge cases: unanswerable questions, a misspelt name, a two-page comparison, a prompt injection.

### 4. A check per behaviour (~250 words)
- `correct` is one check among several: `prices_first`, `known_items`, `no_sibling`, `abstains`.
- Show `tool_checks` in full; it fits on a screen.

### 5. Six runs per case (~200 words)
- One greedy run plus five sampled. Passes in 5 or more is a pass, 1 or fewer a fail, anything else flaky.
- 83 of 90 case-model pairs were all-or-nothing; 3 of 53 greedy passes were luck.

### 6. Predictions on record (~250 words)
- `week8_predicted_vs_actual.png`: too pessimistic on prompts and RAG, too optimistic on the tool agent.
- Past failures belonged to past conditions (k = 1 retrieval). An eval set needs rebuilding when the system changes.

### 7. The regression gate (~150 words)
`--compare old new` exits with an error if any case got worse. That turns 45 cases into a test that runs before every change.

### 8. Reproduce this
Colab link, about 25 minutes on a free T4.

---

## Stretch experiment
**Grow the set from traces.** Run the Week 6 test set, read 20 failing traces, and turn each new failure pattern into a case. How many new patterns appear after the first 10 traces?

## Self-check (closed-book)
1. Why does a known-failure case need a note on where the failure came from?
2. What does a flaky case tell you that a single greedy run can't?
3. Why report counts and named cases here instead of significance tests?
4. When should a case leave the eval set?
5. Why write predictions down before the run?
