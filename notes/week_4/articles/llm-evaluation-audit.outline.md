---
topic: Auditing my own LLM experiments with proper statistics, and what survived
user_need: Give Me Perspective
channel: blog
profile: jorshimayor
reader: Developers and ML engineers who run small LLM experiments (prompt tweaks, agent comparisons) and report the results, with programming literacy but little statistics training
level: intermediate
primary_keyword: LLM evaluation
secondary_keywords: [statistical significance, confidence intervals, sample size, paired comparison, LLM evaluation metrics]
title: I Audited 15 Of My Own LLM Evaluation Claims And Only 8 Survived
seo_title: I Audited 15 Of My LLM Evaluation Claims. 8 Survived
meta_description: I re-tested 15 claims from my own LLM evaluation experiments with confidence intervals and paired tests. Here is what survived, what didn't, and why.
slug: llm-evaluation-audit-statistics
cta: Subscribe on Substack for the follow-up, where I run the pre-registered protocol on bigger models
target_length: 1,600 to 1,900 words
keyword_source: Google and YouTube autocomplete (keyword_ideas.py) + SERP reading. No volume data
status: outline
---

# I Audited 15 Of My Own LLM Evaluation Claims And Only 8 Survived

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | I Audited 15 Of My Own LLM Evaluation Claims And Only 8 Survived | 64 | First-person proof + number | Honest, specific, a gap the piece closes (which 7?) |
| 2 | My LLM Experiment Had A 10% Chance Of Finding Anything | 54 | Result or surprise | The single most striking number |
| 3 | LLM Evaluation On 30 Examples: What The Statistics Actually Say | 63 | Question the reader has | Matches "how to do llm evaluation" intent |
| 4 | Half My LLM Evaluation Results Were Noise. Here's How I Found Out | 64 | Mistake | Mistake framing, strong for Substack |
| 5 | The LLM Evaluation Mistakes I Made In Three Weeks Of Experiments | 63 | Mistake + timeframe | Series continuity with Weeks 1 to 3 |
| 6 | 5 Statistics Checks Every LLM Evaluation Needs (From My Own Errors) | 66 | Number + list | List format; slightly long |
| 7 | Statistical Significance For LLM Evaluation, Tested On My Own Data | 66 | Keyword-led | Strong secondary keyword; long |
| 8 | I Picked The Best Prompt On My Test Set. 40% Of The Gain Was Noise | 65 | Result | Winner's-curse hook, great for X |

Recommended: **1** (title), with the shorter SEO title above. Use **2** as the newsletter subject line and **8** for social.

## Reader desires
- See a real example of results that looked solid falling apart (and which ones held), so they can judge their own experiments.
- Get a small set of checks they can run on their own LLM evaluation today, with code.
- Understand why small samples mislead, without a statistics course.

## Search intent
- Format that ranks: papers (ICML 2025 position paper on CLT at small n, Anthropic's error-bars paper), tool READMEs and a few practitioner blogs. Mostly abstract advice.
- Questions to answer: how many examples do I need for LLM evaluation? Is a difference between two prompts significant? How do I put error bars on accuracy? What are good LLM evaluation metrics at small scale?
- Gap: nobody shows a first-hand audit of their own published claims with before-and-after verdicts. Real data and an honest scorecard are the angle.

## Intro plan
- Setup: over three weeks I ran about 260 LLM experiments and wrote confident conclusions (one-shot hurts, ReAct equals Act, the calculator helps).
- Why it matters now: every team makes prompt and agent decisions on 30 to 150 test cases. If those numbers are noise, the decisions are guesses.
- Implied roadmap: hint that some conclusions held, some didn't, one test had almost no chance of working, and picking "the best" inflated results.
- Transition: so which of my claims were real?

## Outline
### H2: Which Of My LLM Evaluation Claims Survived?
- Purpose: deliver the headline scorecard immediately.
- Key points: 15 claims audited; 8 hold, 7 not established, 0 overturned. Show the forest plot. Name the three most surprising casualties: "16 shots beat 0 shots" (+2.7, CI −1.7 to +7.3), "ReAct equals Act" (CI −16.7 to +10.0), "calculator helps" (raw p 0.016, not significant after Holm correction).
- Keywords: LLM evaluation (first paragraph); confidence intervals.
- Links: [the full audit notebook](https://github.com/jorshimayor/AI-Engineering-Flow_Research)
- Visual: `results/week4/claim_audit.png`. Alt: "Forest plot of 15 LLM evaluation claims with 95% confidence intervals, coloured by verdict".
- Transition: how the audit worked.

### H2: How I Tested My LLM Evaluation Results
- Purpose: method in brief, enough to trust and reproduce.
- Key points: same items in both conditions (paired comparison); Wilson intervals for proportions; paired bootstrap and sign-flip tests; exact McNemar for 0/1 runs; ±5-point equivalence margin for "no difference" claims; Holm correction across 11 directional claims. No model re-runs: all from saved per-item results.
- Keywords: paired comparison; statistical significance.
- Links: [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640) (external)
- Visual: small table of which test fits which claim type.
- Transition: the first lesson came from the smallest experiment.

### H2: Why A Sample Size Of 30 Told Me Almost Nothing
- Purpose: supporting finding 1, power and intervals.
- Key points: 6/30 = 20% has a 95% interval of 9.5% to 37%. My ReAct vs Act comparison had 10% power to detect a 10-point difference. Absence of evidence is not evidence of absence: "no difference" needs an equivalence test. Show the CI-width chart.
- Keywords: sample size; confidence intervals.
- Visual: `results/week4/ci_width.png`. Alt: "Confidence interval width for LLM evaluation accuracy at sample sizes from 10 to 1,000".
- Transition: even with enough data, how you choose results can inflate them.

### H2: Picking The Best Prompt Inflated My Results
- Purpose: supporting finding 2, the winner's curse.
- Key points: best-vs-worst of 24 demo orderings reported as 8.0 and 9.3 points. Selected on half the data and measured on the other half (2,000 splits): 4.8 and 6.7 points. 28% to 40% of the gap was selection noise, though the effect stays positive in over 90% of splits.
- Keywords: LLM evaluation metrics (variation).
- Visual: `results/week4/winners_curse.png`. Alt: "Histogram comparing in-sample and held-out prompt ordering gaps".
- Transition: and some claims only look true until you correct for testing many at once.

### H2: Testing 11 Claims At Once Changes What Counts As Significant
- Purpose: supporting finding 3, multiple comparisons.
- Key points: a 7-to-0 split looks decisive (raw p 0.016) but after Holm correction across 11 claims, p = 0.08. What held strongly: recency bias (+10.9 points), calibration effects (±28 to 29 points), the one-shot dip (+13.5).
- Keywords: statistical significance.
- Transition: what I got wrong in how I wrote things up.

### H2: What I Got Wrong, And The Limits Of This Audit
- Purpose: honest caveats (required by the reader need).
- Key points: I overstated "below chance" (48.7% is indistinguishable from 50%); the robust finding was the collapse onto one label. Limits: one small model, synthetic and easy tasks, equivalence margin chosen by me, Holm is conservative. None of the 7 was shown false; they are unproven. Coda: I later ran the ReAct comparison at 1.5B on a GPU. A real difference appeared, 30 points in the opposite direction (p = 0.012). Calling the 0.5B result "the same" would have been wrong; "not established" was the honest label.
- Transition: what to do differently.

### H2: A Checklist For Your Own LLM Evaluation Before You Publish
- Purpose: takeaways the reader can apply, plus reproduction.
- Key points: a five-item checklist: (1) report a CI with every number; (2) compare on the same items; (3) run a power analysis first; (4) choose prompts on a dev split; (5) correct for many claims. Point to `src/stats.py` (about 150 lines, no scipy). Next in the chain: the Guide Me piece on designing an AI agent evaluation protocol.
- Keywords: LLM evaluation (closing); sample size.
- Links: [stats helpers on GitHub](https://github.com/jorshimayor/AI-Engineering-Flow_Research); [how to do AI agent evaluation step by step](https://jorshimayor.hashnode.dev) (the companion guide, URL to confirm)
- Visual: checklist as a short list.
- Transition: CTA to subscribe for the protocol run.

## Internal links
| Anchor text | URL | Section |
|---|---|---|
| the full audit notebook | https://github.com/jorshimayor/AI-Engineering-Flow_Research | Which Of My LLM Evaluation Claims Survived? |
| stats helpers on GitHub | https://github.com/jorshimayor/AI-Engineering-Flow_Research | A Checklist For Your Own LLM Evaluation |
| how to do AI agent evaluation step by step | https://jorshimayor.hashnode.dev (companion guide, final URL TBC) | A Checklist For Your Own LLM Evaluation |
| my few-shot prompting experiments | https://jorshimayor.hashnode.dev (Week 2 article, URL TBC) | How I Tested My LLM Evaluation Results |
| subscribe for the follow-up | https://jorshimayor.substack.com | Closing CTA |

## Sources
- https://arxiv.org/abs/2411.00640 : CIs and paired tests for evals (Miller, 2024).
- https://arxiv.org/abs/2010.06595 : most NLP comparisons are underpowered (Card et al., 2020).
- https://arxiv.org/abs/2407.01502 : holdouts and repeated runs (Kapoor et al.).
- Own data: `results/week4/claim_audit.json`.

## Repurposing plan
- Newsletter hook: "My ReAct experiment had a 10% chance of detecting the effect it was looking for. When I reran it properly, the effect was real and pointed the other way."
- Video chapters: one per H2; demo the split-half winner's-curse plot live.

## Open questions
- Final URLs for the Week 2 and Week 3 articles and the companion guide.
- Week 4 code isn't on GitHub's main branch yet: merge before publishing so the links resolve.
