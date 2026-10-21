# Week 3 Resources: Reasoning and Tool-Use Foundations

All links checked on 2026-10-07. **Legend:** ⭐ start here · 🟢 beginner · 🟡 intermediate · 🔴 advanced · 💻 hands-on

---

## Suggested path

1. ⭐ Read the ReAct paper: sections 1–3, Figure 1 (the HotpotQA trajectories) and Table 1 (the ablation we reproduced).
2. ⭐ Read the [ReAct project page](https://react-lm.github.io/) and browse the [official prompts](https://github.com/ysymyth/ReAct). You'll see that their format is almost identical to ours.
3. ⭐ Read Anthropic's *Building Effective Agents*: when *not* to build an agent.
4. ⭐ Watch Shunyu Yao (ReAct's first author) on Latent Space.
5. Read Simon Willison's ~50-line ReAct implementation and compare it with `src/react_agent.py`.
6. Read Lilian Weng's *LLM Powered Autonomous Agents* for the bigger map.

---

## 1. Papers

### The Week 3 paper and its ancestors
| Paper | Why |
|---|---|
| ⭐ [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629), Yao et al. 2022 | The Week 3 paper |
| ⭐ [Chain-of-Thought Prompting Elicits Reasoning](https://arxiv.org/abs/2201.11903), Wei et al. 2022 | The "reason only" baseline (our `cot` mode) |
| [Large Language Models are Zero-Shot Reasoners ("Let's think step by step")](https://arxiv.org/abs/2205.11916), Kojima et al. 2022 | CoT without exemplars |
| [Self-Consistency](https://arxiv.org/abs/2203.11171), Wang et al. 2022 | Sample many CoTs and vote. ReAct's best results combine it with CoT |
| [MRKL Systems](https://arxiv.org/abs/2205.00445), Karpas et al. 2022 | Early "LLM + router + tools" design, including a calculator |
| [WebGPT](https://arxiv.org/abs/2112.09332), Nakano et al. 2021 | Trained (not prompted) browsing-with-actions |

### Tool use
| Paper | Why |
|---|---|
| ⭐ [Toolformer](https://arxiv.org/abs/2302.04761), Schick et al. 2023 | The model *teaches itself* when to call tools (calculator, search, etc.) |
| ⭐ [PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435), Gao et al. 2022 | The model writes Python and the interpreter computes. The closest relative of our calculator task |
| [Gorilla: LLM Connected with Massive APIs](https://arxiv.org/abs/2305.15334) | Choosing among thousands of tools/APIs |
| [ReWOO](https://arxiv.org/abs/2305.18323) | Plan all tool calls up front to save tokens (vs ReAct's step by step) |

### Beyond ReAct
| Paper | Why |
|---|---|
| [Reflexion](https://arxiv.org/abs/2303.11366), Shinn et al. 2023 | The agent critiques its own failed attempts and retries |
| [Tree of Thoughts](https://arxiv.org/abs/2305.10601), Yao et al. 2023 | Search over reasoning paths (same first author as ReAct) |
| 🔴 [SWE-agent: Agent-Computer Interfaces](https://arxiv.org/abs/2405.15793), Yang et al. 2024 | Tool *design* matters as much as the model. ReAct applied to coding |
| [τ-bench](https://arxiv.org/abs/2406.12045), Yao et al. 2024 | Evaluating tool-using agents in realistic customer-service settings |
| [The Rise and Potential of LLM-Based Agents (survey)](https://arxiv.org/abs/2309.07864) | Overview of the whole field |

### Safety of tool-using agents
| Paper / post | Why |
|---|---|
| ⭐ [Not What You've Signed Up For: Indirect Prompt Injection](https://arxiv.org/abs/2302.12173), Greshake et al. 2023 | Tool outputs are untrusted input. That's why our calculator never uses `eval` |
| [Prompt injection: what's the worst that can happen?](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/), Simon Willison | Very readable intro to the threat |

---

## 2. Videos
| Video | Channel |
|---|---|
| ⭐ [Language Agents: From Reasoning to Acting](https://www.youtube.com/watch?v=8t65bss7U74) | Latent Space, with **Shunyu Yao** (ReAct author) and Harrison Chase (LangChain) |
| ⭐ [Tips for building AI agents](https://www.youtube.com/watch?v=LP5OCa20Zpg) | Anthropic |
| [What's next for AI agentic workflows](https://www.youtube.com/watch?v=sal78ACtGTc) | Andrew Ng (Sequoia). The reflection, tool-use, planning and multi-agent patterns |
| [State of GPT](https://www.youtube.com/watch?v=bZQun8Y4L2A) | Karpathy. "Models need tokens to think", which is why Thought steps help |
| [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) | Karpathy. The tool-use section (calculator, browser, Python) |

---

## 3. Courses
| Course | Level | Notes |
|---|---|---|
| ⭐ [Hugging Face Agents Course](https://huggingface.co/learn/agents-course) | 🟢💻 | Free and certified. Unit 1 is the Thought → Action → Observation loop |
| [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) (DeepLearning.AI, Andrew Ng) | 🟡💻 | Reflection, tool use, planning, evaluating agents |
| [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) (DeepLearning.AI) | 🟡💻 | Starts by building a ReAct agent from scratch, then rebuilds it in LangGraph |
| 🔴 [Berkeley LLM Agents MOOC (Fall 2024)](https://llmagents-learning.org/f24) | 🔴 | Lectures by Shunyu Yao, Denny Zhou and others |

---

## 4. Articles
| Article | Notes |
|---|---|
| ⭐ [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents), Anthropic | Workflows vs agents. Start simple, add complexity only when it pays |
| [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents), Anthropic | Tool naming, descriptions, error messages (our calculator returns helpful errors for this reason) |
| ⭐ [A simple Python implementation of the ReAct pattern](https://til.simonwillison.net/llms/python-react-pattern), Simon Willison | About 50 lines. Compare it with ours |
| [ReAct: Synergizing Reasoning and Acting (Google Research blog)](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/) | The authors' summary |
| [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/), Lilian Weng | The classic map: planning, memory, tool use |
| [Agents](https://huyenchip.com/2025/01/07/agents.html), Chip Huyen | Tools, planning and failure modes from a production perspective |
| [Prompting Guide: ReAct](https://www.promptingguide.ai/techniques/react) | Short summary with examples |
| [Open-source LLMs as agents](https://huggingface.co/blog/open-source-llms-as-agents), Hugging Face | How well open models follow ReAct, with benchmarks |

---

## 5. Code and docs 💻
| Resource | What for |
|---|---|
| [ysymyth/ReAct](https://github.com/ysymyth/ReAct) | The official prompts and notebooks |
| [smolagents](https://huggingface.co/docs/smolagents/index) | A minimal agent library. Read its source after writing your own |
| [SWE-agent](https://github.com/princeton-nlp/SWE-agent) | A production-grade ReAct-style agent for code |
| [Anthropic tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) | How *native* tool calling replaced text parsing of `Action: x[...]` |
| [Model Context Protocol](https://modelcontextprotocol.io/) | The standard for exposing tools to agents |
