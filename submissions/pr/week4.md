**Title:** Week 4: joshua - eval protocol and memo

## Task

Week 4, Research methodology for applied AI (anchor: *AI Agents That Matter*, Kapoor et al., 2025). Brief: `Week4/Week4_Brief_Eval_Protocol.md`.

**Claim chosen:** ReAct's gain is worth its extra cost.
**Hypothesis:** at 1.5B and 3B, ReAct solves at least 10 points more held-out multi-step calculator problems than Act-only, at no more than 1.5× the tokens.

## Pilot (step 1)

From my Week 3 results (`results_original.json`, 360 episodes):

| Model | Act-only | ReAct | ReAct − Act (95% CI) | Tokens ReAct / Act |
|---|---|---|---|---|
| 0.5B | 23% | 20% | −3.3 (−16.7 to +10.0) | 1.26× |
| 1.5B | 97% | 67% | −30.0 (−50.0 to −13.3), p = 0.012 | 1.43× |
| 3B | 100% | 100% | 0 | 1.89× |

**Biggest flaws found:**
- 30 problems gave 10% power to detect a 10-point gap.
- Act-only was at the ceiling at 1.5B and 3B.
- The whole 1.5B gap came from 2 of 6 templates.

## Protocol (step 2), against the brief's judging criteria

| Criterion | Where it's met in `protocol.md` |
|---|---|
| Falsifiable hypothesis with effect size | +10 points, two-sided, at each size |
| Confounds and a control | Act-only is the control: same tool and examples, no reasoning text. Held-out templates remove exemplar overlap. A leave-one-template-out check tests clustering |
| Sample size with honest uncertainty | N = 480 per model: 81% power after Holm at the 48% discordance measured on dev |
| Success, failure, inconclusive fixed in advance | Five outcomes (supported, too costly, harmful, refuted, inconclusive), frozen at v1.3 before any test run |
| Cost as a first-class metric | Tokens per problem; above 1.5× Act-only is the "too costly" outcome |
| Limitations stated | Threats-to-validity table |

## Files (`Week4/joshua/`), named as in the brief

| File | Contents |
|---|---|
| `protocol.md` | The frozen protocol (v1.3) |
| `lesson_memo.md` | What I learned about evaluating claims, with this protocol as the worked example |
| `results_original.json` | My Week 3 results and traces, the pilot data |

`results_modified.json`, `CHANGES.md` and `week3_react_modified.py` are absent because I didn't do the optional rerun. My fixes went into a new task generator, calibrated on held-out dev templates (in my repo).

## Notes for the reviewer

- **Unchanged since freezing:** `protocol.md` is copied byte for byte. `shasum -a 256 protocol.md` prints `4fd25c86f19344dda5ecf77f6948390c359f7bb3073740aedd0901e9b7748cd4`, matching the freeze commit: https://github.com/jorshimayor/AI-Engineering-Flow_Research/commit/5e8ad76
- **Broken links:** its relative links point into my repo, so they don't resolve here.
- **Length:** it runs to about 7 pages against the 2 to 3 asked, because it includes the analysis plan and revision history. The table above is the short version.
- **Own code:** the pilot used my own Week 3 agent, not the shared code, so the results file follows my format.

## Submission rules

- [x] Branch `week4_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week4/joshua/`, using the brief's file names
- [x] No shared files or other fellows' folders edited
- [x] `results_original.json` not overwritten

Full notes, calibration data and analysis code: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_4
