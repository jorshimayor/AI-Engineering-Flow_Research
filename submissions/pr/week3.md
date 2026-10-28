**Title:** Week 3: joshua - hand-built ReAct loop and results

## Task

Week 3, Reasoning and tool-use foundations (anchor: *ReAct*, Yao et al., 2022).
Lab: hand-implement a minimal single-tool ReAct-style loop on a small task.

## What I did

- **Agent:** `src/react_agent.py`, about 100 lines, no framework. One calculator tool with a safe parser (never `eval`).
- **Loop:** the model writes `Thought:` and `Action: calculate[expr]`; generation stops at `Observation:`; the code appends the real result. Up to 6 steps.
- **Comparison:** the four modes from the paper (direct, CoT, Act-only, ReAct) on 30 two-step word problems, at three model sizes.

| Model | Direct | CoT | Act | ReAct | ReAct − Act (95% CI) | Tokens ReAct / Act |
|---|---|---|---|---|---|---|
| Qwen2.5-0.5B | 0% | 0% | 23% | 20% | −3.3 (−16.7 to +10.0) | 1.26× |
| Qwen2.5-1.5B | 0% | 20% | 97% | 67% | −30.0 (−50.0 to −13.3), p = 0.012 | 1.43× |
| Qwen2.5-3B | 0% | 50% | 100% | 100% | 0 | 1.89× |

**Findings:**
- The calculator does the work: without it, even 3B reaches only 50%.
- Wrong CoT answers are near misses; wrong tool answers are wrong plans.
- At 1.5B, all 10 ReAct failures came from 2 templates, where the reasoning text dropped a quantity or invented tools.
- At 3B both modes hit the ceiling, and Act-only dominates on cost.

## Files (`Week3/joshua/`)

| File | Contents |
|---|---|
| `src/react_agent.py` | The agent loop and calculator |
| `week3_react_agent.ipynb` | 0.5B run on CPU, with traces and analysis |
| `week3_colab.ipynb` | 1.5B and 3B runs on a Colab T4 |
| `week3_results.json` | All 360 episodes (3 models × 4 modes × 30 problems) with full traces and token counts |
| `README.md` | How the agent works, results, failure analysis, caveats |
| `figures/` | Accuracy by size; cost vs accuracy |

## Limitations

- 30 problems from 6 templates: about 10% power to detect a 10-point gap, so ReAct vs Act is not settled here (this motivates my Week 4 protocol).
- Greedy decoding, one model family, and some problem shapes overlap the prompt examples.
- I wrote my own agent instead of using the shared Week 3 code, so the results file follows my format.

## Submission rules

- [x] Branch `week3_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week3/joshua/`
- [x] No shared files or other fellows' folders edited (the shared Week 3 code is untouched)
- [x] Results and traces included

Full notes: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_3
