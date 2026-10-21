---
topic: How to design an AI agent evaluation protocol before running it, using AI Agents That Matter and a worked ReAct example
user_need: Guide Me
channel: blog
profile: jorshimayor
reader: Developers building or comparing LLM agents (prompts, scaffolds, models) who want results they can trust and defend, comfortable with Python, new to experimental design
level: intermediate
primary_keyword: AI agent evaluation
secondary_keywords: [AI agent evaluation framework, AI agent evaluation metrics, AI agent evaluation criteria, eval protocol, power analysis]
title: How To Do AI Agent Evaluation: Design The Protocol Before You Run It
seo_title: How To Do AI Agent Evaluation: Design The Protocol First
meta_description: A step-by-step AI agent evaluation protocol: a falsifiable claim, held-out tasks, cost metrics, a power analysis and pass or fail rules, with a worked example.
slug: ai-agent-evaluation-protocol
cta: Clone the protocol template and the stats helpers from GitHub, then subscribe for the results when I run it
target_length: 1,800 to 2,200 words
keyword_source: Google and YouTube autocomplete (keyword_ideas.py: "ai agent evaluation" on both; "how to do ai agent evaluation", "framework", "criteria", "metrics") + SERP reading. No volume data
status: outline
---

# How To Do AI Agent Evaluation: Design The Protocol Before You Run It

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | How To Do AI Agent Evaluation: Design The Protocol Before You Run It | 68 | Guide + keyword | Matches the autocomplete query "how to do ai agent evaluation" exactly |
| 2 | AI Agent Evaluation In 9 Steps: A Protocol You Write Before The Data | 67 | Number | Clear promise and scope |
| 3 | A Practical AI Agent Evaluation Framework, With A Worked ReAct Example | 70 | Keyword + proof | Uses the "framework" variant; long |
| 4 | Why Your AI Agent Evaluation Needs A Protocol (And How To Write One) | 67 | Question | Pulls in the "why" searcher too |
| 5 | AI Agent Evaluation Criteria: Pass, Fail And Inconclusive Before You Start | 74 | Keyword | Distinctive angle; too long for SEO |
| 6 | The AI Agent Evaluation Checklist I Use After Fooling Myself Twice | 64 | Mistake + first person | Strong for Substack and social |
| 7 | How Many Test Cases Does Your AI Agent Evaluation Need? | 54 | Question | Narrow; good for a section-level snippet |
| 8 | AI Agents That Matter, Applied: An Evaluation Protocol You Can Copy | 65 | Paper name + template | Catches readers of the paper |

Recommended: **1** for the article and **6** for Substack and social. SEO title shortened above to fit 50 to 60 characters.

## Reader desires
- Clear steps from "I think my agent is better" to a written protocol, in order, with a template to copy.
- Answers to the follow-up questions before they ask them: how many test cases, which test, what counts as a pass.
- Confidence that the protocol is sound, via a checklist at the end.

## Search intent
- Format that ranks: practitioner guides (KDnuggets, vendor blogs) on metrics and tools, the AI Agents That Matter site, plus framework READMEs. Mostly "which metrics and tools" content.
- Questions to answer: how do you do AI agent evaluation? Which AI agent evaluation metrics matter? What are good evaluation criteria? How many test cases do I need? What's a held-out set for an agent?
- Gap: the guides list metrics and tools but skip design: falsifiable claims, holdouts matched to the claim, power analysis and pre-registered pass or fail rules. None shows a complete worked protocol.

## Intro plan
- Setup: most AI agent evaluation starts with running the agent and looking at the score. The decisions about what counts as better get made after seeing the numbers.
- Why it matters now: agents are expensive to run, and Kapoor et al. found simple baselines matching complex agents at a fraction of the cost. Evaluations without design can't tell the difference.
- What you'll have at the end: a one-page protocol (claim, design, sample size, metrics, pass or fail rules) and a template. About two hours for a first one.
- Transition: before step one, what you need in hand.

## Outline
### H2: Prerequisites For An AI Agent Evaluation Protocol
- Purpose: what to have before starting.
- Key points: the agent or both variants you want to compare; a way to generate or collect tasks with known answers; a small pilot run (even 30 tasks) to estimate variance; Python with NumPy for the power analysis (`src/stats.py`).
- Keywords: AI agent evaluation (first H2 and first paragraph).
- Links: [the stats helpers and protocol on GitHub](https://github.com/jorshimayor/AI-Engineering-Flow_Research)
- Visual: a one-line summary diagram of the 9 steps. Alt: "Nine steps of an AI agent evaluation protocol from claim to pre-registration".
- Transition: start with the claim.

### H2: Step 1: Write A Claim That Can Fail
- Purpose: falsifiable claim with effect size and cost bound.
- Key points: bad vs good example. Good: "At 1.5B and 3B, ReAct solves at least 10 points more held-out problems than Act-only at no more than 1.5× the tokens." Why 10 points and 1.5×.
- Keywords: AI agent evaluation criteria.

### H2: Step 2: Choose A Paired Comparison
- Purpose: independent variable, blocking factors and baselines.
- Key points: run every task under both conditions; same exemplars; greedy decoding for the primary comparison; include a direct-answer baseline to prove the task needs tools.
- Visual: conditions table.

### H2: Step 3: Build A Held-Out Task Set Matched To Your Claim
- Purpose: holdouts from Kapoor's four generality levels.
- Key points: distribution-specific, task-specific, domain-general, general-purpose and the holdout each needs. Worked example: 2 exemplar templates, 2 dev templates, 8 held-out test templates. The confound it fixes: in my pilot almost all successes came from the one template shaped like a prompt example.
- Links: [AI Agents That Matter](https://arxiv.org/abs/2407.01502) (external)
- Visual: split table.

### H2: Step 4: Pick AI Agent Evaluation Metrics, Including Cost
- Purpose: primary, secondary and diagnostic metrics.
- Key points: accuracy (exact match), tokens per task as the primary cost metric, calls and latency, failure categories. Report a cost-accuracy plot with the Pareto frontier. Example: in my pilot, ReAct used 26% more tokens than Act-only with no gain.
- Keywords: AI agent evaluation metrics.
- Visual: `results/week4/pareto.png`. Alt: "Cost versus accuracy plot for four agent modes with the Pareto frontier".

### H2: Step 5: Pilot The Task To Check For Ceiling Effects
- Purpose: measure headroom and variance before sizing or freezing anything.
- Key points: my pilot reran the Week 3 task at 1.5B and 3B on a free Colab T4. Act-only scored 97% and 100%, a ceiling, so a +10-point gain could never appear. ReAct was 30 points worse at 1.5B (p = 0.012), but all of it came from 2 of 6 templates. Fixes: a harder task (3 to 4 steps, distractors), a difficulty gate (Act-only 40% to 85% on dev), and a leave-one-template-out check. A pilot measures the design, not the effect.
- Keywords: AI agent evaluation (variation).
- Visual: `results/week3_gpu/accuracy_by_size.png`. Alt: "AI agent evaluation pilot accuracy by model size and prompting mode".
- Links: [the Colab notebook that ran the pilot](https://github.com/jorshimayor/AI-Engineering-Flow_Research)

### H2: Step 6: Size The Evaluation With A Power Analysis
- Purpose: how many test cases.
- Key points: paired 0/1 outcomes → exact McNemar. Power depends on the effect and on discordance (the share of tasks where the variants disagree). Table: 180, 260 and 330 tasks for +10 points at 20%, 30% and 40% discordance, without correction. The GPU pilot measured 37% discordance; with Holm correction across two models that needs 400 per model for 83% power. My original 30-task run had 10% power. Fix N before running.
- Keywords: power analysis.
- Visual: `results/week4/power.png`. Alt: "Power curves for an AI agent evaluation by number of tasks".
- Code: the 15-line `power_mcnemar` simulation.

### H2: Step 7: Write Pass, Fail And Inconclusive Rules
- Purpose: success and failure criteria before the data.
- Key points: supported, too costly, harmful (ReAct reliably worse, as the pilot hinted at 1.5B), refuted (CI upper bound below +5 points), inconclusive. Holm correction across models. Equivalence margin for "no difference".
- Keywords: AI agent evaluation criteria.
- Visual: outcomes table.

### H2: Step 8: List Threats And Add Validity Gates
- Purpose: confounds and checks that invalidate a run.
- Key points: threats table (exemplar overlap, prompt length, tuning on test, best-of-N selection, parser bias). Gates: task needs the tool (direct ≤ 10%), calculator unit tests pass, format failures ≤ 20%, no template leakage, and no ceiling (Act-only 40% to 85% on dev).

### H2: Step 9: Freeze And Pre-Register The Protocol
- Purpose: commit before running.
- Key points: dev-set iteration only; commit the protocol and note the hash; generate test tasks from a fixed seed; one run per condition; save all outputs including failures. Budget from measured T4 speeds: about 5 to 7 GPU hours and 2.3M to 3.4M tokens. Keep a revision history: every change made after the pilot, with its reason.
- Keywords: eval protocol.

### H2: How To Check Your AI Agent Evaluation Protocol Before Running It
- Purpose: verify the protocol is sound; next steps.
- Key points: an 11-item checklist from the rigour memo; the most common gap (no power analysis); next in the chain: run it, then a Give Me Perspective piece with results. CTA to clone the template.
- Keywords: AI agent evaluation framework; AI agent evaluation (closing).
- Links: [my audit of 15 LLM evaluation claims](https://jorshimayor.hashnode.dev) (companion piece, URL TBC); [subscribe for the results](https://jorshimayor.substack.com)

## Internal links
| Anchor text | URL | Section |
|---|---|---|
| the stats helpers and protocol on GitHub | https://github.com/jorshimayor/AI-Engineering-Flow_Research | Prerequisites |
| the ReAct agent I'm evaluating | https://github.com/jorshimayor/AI-Engineering-Flow_Research | Step 2 |
| my audit of 15 LLM evaluation claims | https://jorshimayor.hashnode.dev (URL TBC) | How To Check Your Protocol |
| subscribe for the results | https://jorshimayor.substack.com | Closing |

## Sources
- https://arxiv.org/abs/2407.01502 : cost-aware evaluation, holdouts by generality level, HumanEval baselines (Warming 93.2% at $2.45 vs LATS 88.0% at $134.50).
- https://arxiv.org/abs/2510.11977 : HAL harness and its findings.
- https://arxiv.org/abs/2507.02825 : agentic benchmark checklist.
- Own data: `notes/week_4/eval_protocol.md`, `results/week4/power_table.json`.

## Repurposing plan
- Newsletter hook: "LATS scored 88% for $134.50. A retry loop scored 93% for $2.45. Here's how to design evaluations that notice."
- Video chapters: one per step; show the pilot chart and the power calculation live.

## Open questions
- Confirm the companion article URL before publishing.
- Merge Week 4 to GitHub's main branch so the code links resolve.
