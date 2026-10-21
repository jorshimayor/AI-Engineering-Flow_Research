# Week 1 Articles: Plan

## How many: 3 articles

Write one article for each distinct idea the notebook produced **original data** on. Three is the right number because:

- **Each one has its own findings.** An article built on your own experiments shows you did the work and understood it; a re-explanation of the paper doesn't. All three below are backed by numbers and charts that only your notebook has.
- **Each is small enough to finish.** 1,200–1,800 words each is easier to complete, review and publish than a single 6,000-word piece.
- **They map to the video and newsletter.** Each article can become one chapter of the overview video and one section of the newsletter, with a "read the deep dive" link.
- **Each concept gets retrieval practice.** Explaining tokens, then probabilities, then attention in your own words is what makes them stick. That's the assessment part.

One flagship article would be too long and would bury the good findings. Five or more would stretch thin material and take weeks away from Week 2.

## The three articles

| # | Working title | Core question | Notebook sections | Difficulty | Outline |
|---|---|---|---|---|---|
| 1 | **Your LLM Can't See Words** | What does a language model actually receive as input, and why does it matter? | §1 Tokeniser, §2 Embeddings | 🟢 easiest | [01-tokenisation.md](01-tokenisation.md) |
| 2 | **What an LLM Actually Outputs** | What is a next-token distribution, and how do we get text, facts and evals out of it? | §3 Next-token, §5 Generation | 🟡 | [02-next-token-and-generation.md](02-next-token-and-generation.md) |
| 3 | **Rebuilding Self-Attention by Hand** | What is attention mathematically, and what do real heads actually do? | §4 Attention + the paper | 🔴 hardest | [03-self-attention.md](03-self-attention.md) |

Together they follow the model's data flow: **input (tokens) → output (probabilities) → the machinery in between (attention)**. That's also the running order for the video.

### Suggested writing order and schedule

Write them in the order 1 → 2 → 3, from easiest to hardest. Each one builds vocabulary the next uses.

| When | Do |
|---|---|
| Days 1–2 | Article 1: draft, self-check, publish |
| Days 3–4 | Article 2 |
| Days 5–6 | Article 3 (it's the one that also covers the paper) |
| Day 7 | Newsletter + overview video, linking all three |

## Writing process for each article (this is the assessment)

1. **Closed-book first.** Before rereading anything, answer the article's *Self-check* questions from memory on paper. Wherever you get stuck is where your understanding has a gap.
2. **Fill the gaps.** Reread the notebook and the relevant resources ([../resources.md](../resources.md)).
3. **Run the stretch experiment.** Each outline includes one new experiment that isn't in the notebook. Adding it makes the article more than a recap, and it's the strongest proof of work.
4. **Draft from the outline.** Use your own words and your own numbers.
5. **Verify every number** against the notebook output. Anything you claim, a reader should be able to reproduce.
6. **Explain it to someone.** If you can't explain a section out loud in 60 seconds, it isn't ready. This also rehearses the video.

## Shared conventions

- **Length:** 1,200–1,800 words, plus 2–4 figures.
- **Reproducibility:** end each article with a *Reproduce this* box linking the notebook (put it on GitHub) and naming the model (GPT-2 small, 124M).
- **Figures:** already exported to [`figures/`](figures/):

  | File | Use in |
  |---|---|
  | `token-tax.png` | Article 1 |
  | `positional-embeddings.png` | Article 1 (or 3) |
  | `next-token-entropy.png` | Article 2 |
  | `surprisal-perplexity.png` | Article 2 |
  | `temperature-entropy-diversity.png` | Article 2 |
  | `attention-it-animal.png` | Article 3 |

- **Honesty section:** each article should include a "what I got wrong / caveats" part. You have real ones (the glitch-token centroid result, the "it → animal" head). This builds credibility and is uncommon in AI writing.
- **Drafts:** write them in this folder as `01-tokenisation-draft.md` etc., next to the outlines.

## How the video and newsletter use these

```
                 ┌──────────── Newsletter (overview, ~600 words) ────────────┐
                 │ 1 hook + 3 short sections, each ending "Read the deep dive →"│
                 └──────────────────────────────────────────────────────────┘
Article 1 ◄──────┤
Article 2 ◄──────┼──── Video (overview, 8–12 min): 3 chapters, same order
Article 3 ◄──────┘     each chapter = 1 surprising result + 1 chart + link in description
```

**Newsletter outline:** *"I spent a week inside GPT-2. Here's what surprised me."*
1. Hook: a single trailing space turns "Paris" from the model's 5th-choice answer into its 1,472nd. (Use this; it's the most surprising result you have.)
2. Section per article: 2–3 sentences, 1 chart, "Read more →".
3. What's next: Week 2 teaser.

**Video outline** (one chapter per article, each with a live demo):
- 0:00 Hook (the trailing-space demo, run live)
- Ch. 1 Tokens: show Tiktokenizer, Hindi vs English cost
- Ch. 2 Probabilities: temperature from 0.3 up to 1.8, live
- Ch. 3 Attention: the "it → animal" heatmap, and the twist that it isn't really coreference
- Outro: links to all three articles

The overview formats hand off the *why* to the articles, so the articles are where the depth lives. Don't repeat the full explanation in the video.
