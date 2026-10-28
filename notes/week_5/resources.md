# Week 5 Resources: Systematic Prompt Engineering

Links checked 28 October 2026. ⭐ = start here.

## Papers

| Paper | Why |
|---|---|
| ⭐ [Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903), Wei et al. 2022 | The anchor paper; also [Google's summary](https://research.google/blog/language-models-perform-reasoning-via-chain-of-thought/) |
| ⭐ [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916), Kojima et al. 2022 | "Let's think step by step" (our `zero_shot_cot`) |
| [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171), Wang et al. 2022 | Sample several reasoning paths and vote |
| [Least-to-Most Prompting](https://arxiv.org/abs/2205.10625), Zhou et al. 2022 | Decompose into easier sub-questions first |
| [PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435) · [Program of Thoughts](https://arxiv.org/abs/2211.12588) | Write code, let an interpreter compute (Week 3's lesson, as a prompt) |
| [Towards Understanding Chain-of-Thought Prompting](https://arxiv.org/abs/2212.10001), Wang et al. 2022 | Which parts of a reasoning example actually matter |
| ⭐ [Let Me Speak Freely? Format Restrictions and Performance](https://arxiv.org/abs/2408.02442), Tam et al. 2024 | Forcing JSON can cost reasoning accuracy (our H2) |
| [To CoT or not to CoT?](https://arxiv.org/abs/2409.12183), Sprague et al. 2024 | Chain-of-thought helps mainly on maths and symbolic tasks |
| [Language Models Don't Always Say What They Think](https://arxiv.org/abs/2305.04388) · [Measuring Faithfulness in CoT](https://arxiv.org/abs/2307.13702) | The written reasoning isn't always the real reason |
| [Training Verifiers to Solve Math Word Problems (GSM8K)](https://arxiv.org/abs/2110.14168), Cobbe et al. 2021 · [data](https://github.com/openai/grade-school-math) | The task |
| [GSM-Symbolic](https://arxiv.org/abs/2410.05229), Mirzadeh et al. 2024 | GSM8K scores drop when numbers and names change |
| [The Prompt Report](https://arxiv.org/abs/2406.06608), Schulhoff et al. 2024 | Survey of 58 prompting techniques |
| [Large Language Models Are Human-Level Prompt Engineers](https://arxiv.org/abs/2211.01910) · [DSPy](https://arxiv.org/abs/2310.03714) | Optimising prompts automatically |
| [Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115) | The models used here |

## Guides

| Resource | Notes |
|---|---|
| ⭐ [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/), Lilian Weng | Survey: few-shot, CoT, self-consistency |
| [Prompting Fundamentals](https://eugeneyan.com/writing/prompting/), Eugene Yan | Practical habits for production prompts |
| [Anthropic prompt engineering docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | Examples, step-by-step thinking, structured output |
| [Prompting Guide: Chain-of-Thought](https://www.promptingguide.ai/techniques/cot) | Short reference |
| [Chat templates](https://huggingface.co/docs/transformers/chat_templating), Hugging Face | How few-shot examples become chat turns |
| [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/), DeepLearning.AI | One-hour course |
| [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), Hamel Husain | Why every prompt change needs an eval (Week 8 reading) |

## Tools

| Tool | For |
|---|---|
| [Outlines](https://github.com/dottxt-ai/outlines) | Constrained generation: guarantee valid JSON |
| [Instructor](https://github.com/567-labs/instructor) | Validated structured outputs (Week 6) |
| [promptfoo](https://github.com/promptfoo/promptfoo) | Regression tests for prompts |
| [DSPy](https://github.com/stanfordnlp/dspy) | Programmatic prompt optimisation |
