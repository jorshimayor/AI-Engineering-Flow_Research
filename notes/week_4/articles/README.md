# Week 4 Articles: Plan

Outlines were built with the `writing-studio` skill (Mode A, profile `jorshimayor`) and pass `outline_check.py --strict` with 0 failures and 0 warnings.

## How many: 2 articles

Week 4 produced two kinds of material: an **audit** of my own results (a finding) and a **protocol** (a method). They serve different reader needs, so they become two pieces that chain together: the audit shows why rigour matters, and the guide shows how to get it.

| # | Topic | Reader need | Channel | Primary keyword | Recommended title | Outline file | Check result |
|---|---|---|---|---|---|---|---|
| 1 | Auditing 15 of my own claims with proper statistics | Give Me Perspective | blog (+ Substack) | LLM evaluation | I Audited 15 Of My Own LLM Evaluation Claims And Only 8 Survived | [outlines/llm-evaluation-audit.outline.md](outlines/llm-evaluation-audit.outline.md) | 0 failed, 0 warnings |
| 2 | Designing an eval protocol before running it | Guide Me | blog (+ Substack) | AI agent evaluation | How To Do AI Agent Evaluation: Design The Protocol Before You Run It | [outlines/ai-agent-evaluation-protocol.outline.md](outlines/ai-agent-evaluation-protocol.outline.md) | 0 failed, 0 warnings |

**Keyword evidence:** Google and YouTube autocomplete via `keyword_ideas.py`, plus reading the current search results. No volume data was available, so treat both keywords as reasoned choices, not measured ones.
- "ai agent evaluation" appeared on both Google and YouTube, with "how to do ai agent evaluation", "framework", "criteria" and "metrics" as variants.
- "llm evaluation" appeared on both, with "how to do llm evaluation" and "llm evaluation metrics".

**Overlap check:** the two keywords are distinct (LLM evaluation vs AI agent evaluation) and the needs differ (perspective vs guide), so they won't compete.

**Order:** write and publish **Article 1 first**. It's the stronger hook and it creates the reason to read Article 2. Article 1 closes by pointing to Article 2; Article 2 closes by pointing back to Article 1 and to the results follow-up.

## Before you write: self-check (closed-book)
### Article 1
1. Why does a Wilson interval behave better than p ± 1.96·√(p(1−p)/n) at 0/30?
2. Why does pairing increase power? What does McNemar ignore, and why is that fine?
3. What's the difference between "not established" and "overturned"?
4. Explain the winner's curse with the split-half experiment in two sentences.
5. Why did a 7-to-0 result stop being significant? Is the effect therefore absent?

### Article 2
1. State the four generality levels from Kapoor et al. and the holdout each needs.
2. Why does McNemar power depend on discordance, not on the two accuracies?
3. Why must N be fixed before the run? What goes wrong with "add data until significant"?
4. What makes a "refuted" rule different from an "inconclusive" one?
5. Why plot cost against accuracy instead of reporting accuracy alone?

## Stretch experiments (new, original material)
- **Article 1:** re-run the two closest calls (W2-1, 16 vs 0 shots; W2-6, great/terrible vs positive/negative) with 500 test reviews instead of 150, and report whether they move to "holds". About 1 to 2 hours on this CPU.
- **Article 2:** ~~measure real discordance on a GPU~~ done: the 16 October Colab pilot measured 37% discordance at 1.5B and a ceiling at 3B, which produced protocol v1.1 (N = 400). Next stretch: write the harder generator and run the dev-set difficulty calibration, so the guide can show the gate passing.

## Figures
All in `results/week4/`:

| File | Article |
|---|---|
| `claim_audit.png` | 1 (hero) |
| `ci_width.png` | 1 |
| `winners_curse.png` | 1 |
| `pareto.png` | 2 (and 1) |
| `power.png` | 2 |
| `../week3_gpu/accuracy_by_size.png` | 2 (the pilot step), and 1 (the coda) |

## Newsletter and video hooks
- **Newsletter subject:** "My Experiment Had A 10% Chance Of Working" (41 characters). Preview: "I audited 15 of my own AI claims. Here's what survived."
- **Video:** live split-half demo (pick the "best" prompt, watch the gap shrink on held-out data), then the GPU pilot chart, then the power calculation for the protocol.

## Hand-off
Draft with `writing-studio` Mode B: "write it from `outlines/llm-evaluation-audit.outline.md`". The skill runs `seo_check.py --strict --spelling british` and the outline-alignment check before delivery.
