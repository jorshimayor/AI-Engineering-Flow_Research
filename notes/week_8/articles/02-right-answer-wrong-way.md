# Article 2: Process checks and a small judge (outline)

## Title options
- **The Right Answer, the Wrong Way**
- My Agent Got the Total Right and Failed Every Other Check
- Can a 3B Model Grade Its Own Homework?

**Target reader:** grades agents or RAG systems on the final answer alone, or is about to trust a model as judge.
**Promise:** what checks on process and refusals reveal that accuracy hides, how to find the cases that test nothing, and how far a small judge agrees with code.
**Length:** ~1,400 words · **Hero:** `week8_checks.png`

---

## Outline

### 1. Hook (~120 words)
"Ada buys 3 jars of basil pesto and 2 balls of mozzarella." The 3B agent answered £33.10, correct, in 4 of 6 runs. Every time, it first asked for a "jar of basil pesto" and sent `3 * lookup_price('jar of basil pesto')` to a calculator.

### 2. Outcome vs process (~300 words)
- 15 correct answers in 90 runs; 1 case that passed every check.
- `prices_first` held in 9% to 17% of runs, `known_items` in 54% at 3B.
- The stray `>`: a correct £10.49 lost to a repair loop that drifted to 1.05.

### 3. Who can say "I don't know"? (~250 words)
- RAG at 3B declined both unanswerable questions every time; 1.5B invented "550 mAh".
- The prompt system at 3B flagged the missing number on its greedy run and assumed zero passengers in 5 of 6 sampled runs.
- The tool agent answered 0.0 for caviar it couldn't find. Nothing in the loop lets it decline.

### 4. Cases that tested nothing (~250 words)
- The injection notice never reached the model: retrieval ranked three price chunks above it.
- The comparison failed at retrieval: one weight wasn't in the context, and the 3B model's "unknown" was right.
- The lesson: a check needs a precondition, and someone has to read the traces.

### 5. A 3B judge (~250 words)
- Agreement with the checks: 96% (κ 0.91) on 1.5B answers, 89% (κ 0.77) on its own.
- All 7 disagreements were the judge failing a correct answer, 4 of them correct refusals. Never a false pass.
- Fine as a strict second opinion; not yet usable for refusals.

### 6. What I'd change (~150 words)
Strip unit words in `lookup_price`; tell the agent to wait for prices; give it a way to decline; precondition checks for injection and comparison cases; a judge rubric that names "unknown".

### 7. Reproduce this
Colab link; section 8 of the notebook prints every failing greedy trace.

---

## Stretch experiment
**Fix one thing, gate on the rest.** Strip unit words in `lookup_price`, rerun the tool cases, and run `--compare` against the saved scorecard. Which cases improve, and does anything regress?

## Self-check (closed-book)
1. Why can a correct final answer hide a broken process?
2. What precondition would make the injection case meaningful?
3. Why was the 3B judge harsher on its own answers here?
4. Why is a judge that never passes wrong answers still not enough for refusals?
5. Which single tool-agent fix would you expect to move the most cases, and why?
