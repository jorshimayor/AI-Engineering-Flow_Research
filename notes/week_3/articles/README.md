# Week 3 Articles: Plan

## How many: 2 articles

Week 3 produced **an artefact** (the agent) and **an evaluation** (120 runs with failure analysis). These are naturally two articles:

| # | Working title | Core question | Outline |
|---|---|---|---|
| 1 | **Build a ReAct Agent From Scratch: ~100 Lines, No Framework** | What *is* an agent, mechanically? | [01-build-react-from-scratch.md](01-build-react-from-scratch.md) |
| 2 | **My Agent Got the Math Right and the Answer Wrong** | What do reasoning and tools actually each contribute, and how do agents fail? | [02-what-tools-and-thoughts-buy-you.md](02-what-tools-and-thoughts-buy-you.md) |

Article 1 is the **tutorial**: evergreen, very shareable, good for building credibility. Article 2 is the **research note**: honest, data-driven, and it includes the "ReAct didn't beat Act at 0.5B" result, which most tutorials would leave out. Write 1 first, because Article 2 relies on readers knowing the loop.

**Optional third (later):** after running the 1.5B / API-model stretch experiment, a short follow-up: *"Same agent, bigger brain: does ReAct start to win?"*

## Figures
- `results/week3/accuracy_by_mode.png` (Article 2 hero)
- Trajectory screenshots from the notebook: a success, the "ignored observation" failure, the hallucinated-observation demo
- **Draw yourself:** a loop diagram (LLM → parse → tool → observation → LLM). This is the hero for Article 1

## Process (same as before)
Self-check closed-book → stretch experiment → draft (1,200–1,800 words) → verify numbers against `results/week3/runs.jsonl`.

## Newsletter and video hooks
- **Newsletter hook:** "My agent called the calculator, got the right number, then 'reasoned' its way to the wrong answer."
- **Video demo:** run `src/react_agent.py` live. Then run it again with `--no-stop` and show the model inventing its own tool result.
