# Fellowship Submissions

Copies of what I submit to [Flow-Research/applied-ai-engineering-labs-26](https://github.com/Flow-Research/applied-ai-engineering-labs-26), one folder per week, kept here as a reference and for self-review. Each folder matches the `Week<N>/joshua/` folder on its `week<N>_joshua` branch. The full work behind each week lives in [`notes/`](../notes/README.md).

Rebuild a folder from the main repo after changing the source files, then copy it into the fellowship branch. Don't edit these copies directly.

## Status

PR descriptions for the fellowship repo, ready to paste: [`pr/`](pr/).

| Week | Task | Files | PR |
|---|---|---|---|
| [1](week1/) | Probe tokeniser edge cases and next-token distributions | Notebook, README, figure | Not opened |
| [2](week2/) | Vary few-shot count, order and format on a fixed task | Notebook, `src/icl.py`, README, figure | Not opened |
| [3](week3/) | Hand-build a single-tool ReAct loop | 2 notebooks, `src/react_agent.py`, `week3_results.json`, README, figures | Not opened |
| [4](week4/) | Eval protocol on paper ([brief](https://github.com/Flow-Research/applied-ai-engineering-labs-26/blob/research/Week4/Week4_Brief_Eval_Protocol.md)) | `protocol.md`, `lesson_memo.md`, `results_original.json` | Not opened |
| 5 | Prompt library, 3+ strategies with documented deltas | Pending the Colab run | Not opened |

## Self-review

### Week 1

| Check | Met? | Evidence or gap |
|---|---|---|
| Tokeniser edge cases probed | Yes | Spaces, numbers, emoji, special tokens, cross-language token cost |
| Next-token distributions compared across prompts | Yes | Trailing-space effect, constrained vs free ranking, entropy by prompt |
| Observations written up | Yes | README results and findings tables |
| Gap | | One model (GPT-2); the lead's example compared two. Single prompts, no statistics |

### Week 2

| Check | Met? | Evidence or gap |
|---|---|---|
| Count, order and format varied on a fixed task | Yes | 140 configurations, same 150 test reviews |
| What moves quality documented | Yes | Format moved accuracy by up to 41 points; order and examples by 6 to 9 |
| Sampling and context limits | Yes | Temperature vs P(correct); GPT-2 fails at token 1,025 |
| Gap | | One main model (Qwen2.5-0.5B base); an easy task. Week 4 re-audit: 3 of its claims not established |

### Week 3

| Check | Met? | Evidence or gap |
|---|---|---|
| Hand-written ReAct loop, single tool, no framework | Yes | `react_agent.py`, about 100 lines, safe calculator |
| Compared against baselines | Yes | Direct, CoT, Act-only, ReAct at 0.5B, 1.5B and 3B |
| Traces read, failures explained | Yes | Wrong plans vs near-miss arithmetic; 2 templates caused the 1.5B gap |
| Gap | | 30 problems: 10% power for a 10-point gap. Own code, not the shared Week 3 code |

### Week 4 (judged against the brief)

| Criterion | Met? | Evidence or gap |
|---|---|---|
| Falsifiable hypothesis with effect size | Yes | ReAct ≥ +10 points over Act-only at ≤ 1.5× tokens |
| Confounds identified; a control isolating one | Yes | Act-only isolates the reasoning text; held-out templates remove exemplar overlap; leave-one-template-out for clustering |
| Sample size justified, honest uncertainty | Yes | N = 480 per model: 81% power after Holm at 48% dev discordance |
| Success, failure, inconclusive fixed in advance | Yes | Five outcomes, frozen at v1.3 (hash `4fd25c86…`) |
| Cost as a first-class metric | Yes | 1.5× token bound; "too costly" is its own outcome |
| Limitations stated honestly | Yes | Threats to validity table |
| Gap: length | No | About 7 pages against 2 to 3 asked |
| Gap: shared code | No | Pilot used my own Week 3 agent; say so in the PR |
| Gap: peer review (step 4) | To do | Comment on a peer's protocol PR |
| Gap: talk (5 minutes) | To do | Claim and pilot, biggest flaw, protocol, what would change my mind |
