# Week 2 Resources: Context, Sampling and In-Context Learning

All links checked on 2026-10-07. **Legend:** ⭐ start here · 🟢 beginner · 🟡 intermediate · 🔴 advanced · 💻 hands-on

---

## Suggested path

1. ⭐ Read the GPT-3 paper: sections 1–3 and Figure 1.2 (accuracy vs number of shots). Skip the long benchmark tables.
2. ⭐ Yannic Kilcher's GPT-3 explainer video, to see the paper walked through.
3. ⭐ *Calibrate Before Use* (Zhao et al.): the paper behind E2 and E5 and behind our calibration column.
4. ⭐ *Rethinking the Role of Demonstrations* (Min et al.): the paper behind E4.
5. *Lost in the Middle*: the paper behind the passkey experiment.
6. Lilian Weng's *Prompt Engineering* post, to put it all together.

---

## 1. Papers

### The Week 2 paper
| Paper | Why |
|---|---|
| ⭐ [Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165), Brown et al. 2020 | Defined zero-, one- and few-shot "in-context learning" and showed it improves with scale |

### What makes few-shot prompts work, or break (our experiments map to these)
| Paper | Our experiment | Why |
|---|---|---|
| ⭐ [Calibrate Before Use](https://arxiv.org/abs/2102.09690), Zhao et al. 2021 | E2, E5, calibration | Majority-label, recency and common-token biases, plus the "N/A" calibration trick we used |
| ⭐ [Fantastically Ordered Prompts](https://arxiv.org/abs/2104.08786), Lu et al. 2021 | E2 order | Demo order alone can swing accuracy from near-random to near-SOTA |
| ⭐ [Rethinking the Role of Demonstrations](https://arxiv.org/abs/2202.12837), Min et al. 2022 | E4 labels | Random labels barely hurt: demos teach the format and label space more than the mapping |
| [Larger Language Models Do In-Context Learning Differently](https://arxiv.org/abs/2303.03846), Wei et al. 2023 | E4 flipped | Only big models override their priors when labels are flipped |
| [What Makes Good In-Context Examples for GPT-3?](https://arxiv.org/abs/2101.06804), Liu et al. 2021 | E1 which-demos | Pick demos *similar to the query* (retrieval) |
| [Quantifying LMs' Sensitivity to Spurious Features in Prompt Design](https://arxiv.org/abs/2310.11324), Sclar et al. 2023 | E3 format | Formatting alone causes swings of up to 76 points |
| [Many-Shot In-Context Learning](https://arxiv.org/abs/2404.11018), Agarwal et al. 2024 | E1 count | What happens with hundreds or thousands of shots in long contexts |

### Why ICL works at all (theory) 🔴
| Paper | Why |
|---|---|
| [An Explanation of In-context Learning as Implicit Bayesian Inference](https://arxiv.org/abs/2111.02080), Xie et al. 2021 | Demos help the model infer which "concept" or task it's in |
| [Transformers Learn In-Context by Gradient Descent](https://arxiv.org/abs/2212.07677), von Oswald et al. 2022 | Attention can implement a step of gradient descent |
| [In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html), Anthropic 2022 | The circuit-level mechanism (links to Week 1) |
| [A Survey on In-context Learning](https://arxiv.org/abs/2301.00234), Dong et al. | Overview of the whole field |

### Sampling
| Paper | Why |
|---|---|
| [The Curious Case of Neural Text Degeneration (top-p)](https://arxiv.org/abs/1904.09751), Holtzman et al. 2019 | Origin of nucleus sampling |
| [Min-p Sampling](https://arxiv.org/abs/2407.01082), Nguyen et al. 2024 | A newer truncation method that scales with model confidence |

### Context windows
| Paper / resource | Why |
|---|---|
| ⭐ [Lost in the Middle](https://arxiv.org/abs/2307.03172), Liu et al. 2023 | Models use the start and end of long contexts better than the middle |
| [RULER: What's the Real Context Size?](https://arxiv.org/abs/2404.06654), Hsieh et al. 2024 | Claimed context ≠ effective context; harder tests than passkey retrieval |
| [YaRN: Efficient Context Window Extension](https://arxiv.org/abs/2309.00071) | How RoPE models get stretched to long contexts |
| [Needle in a Haystack test (GitHub)](https://github.com/gkamradt/LLMTest_NeedleInAHaystack) 💻 | The popular test our passkey experiment is based on |

---

## 2. Videos
| Video | Channel |
|---|---|
| ⭐ [GPT-3: Language Models are Few-Shot Learners (Paper Explained)](https://www.youtube.com/watch?v=SY5PvZrJhLE) | Yannic Kilcher |
| [State of GPT](https://www.youtube.com/watch?v=bZQun8Y4L2A) | Andrej Karpathy (Microsoft Build). Base vs assistant models, why prompting works, "models need tokens to think" |
| [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) | Andrej Karpathy. Has sections on in-context learning and the context window as "working memory" |
| [In-Context Learning (Few-Shot Prompting), Explained](https://www.youtube.com/watch?v=MPWckSNZaJo) | Short 1-minute intro |
| [Stanford CS224N (Spring 2024)](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D) | The prompting, instruction-tuning and RLHF lecture |

---

## 3. Courses
| Course | Level |
|---|---|
| ⭐ [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) (DeepLearning.AI, Isa Fulford & Andrew Ng) | 🟢 1 hr |
| [Hugging Face LLM Course](https://huggingface.co/learn/llm-course) | 🟢💻 |
| [Stanford CS224N](https://web.stanford.edu/class/cs224n/) | 🟡 |

---

## 4. Articles and guides
| Article | Notes |
|---|---|
| ⭐ [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/), Lilian Weng | The best single survey: few-shot selection, ordering, calibration, CoT |
| [Prompting Guide: Few-shot](https://www.promptingguide.ai/techniques/fewshot) | Short and practical, includes the random-labels finding |
| [Anthropic prompt engineering docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | How a frontier lab recommends using examples ("multishot") |
| [Prompt engineering for long context](https://www.anthropic.com/news/prompting-long-context), Anthropic | Where to put documents vs questions in long prompts |
| [How to generate text](https://huggingface.co/blog/how-to-generate), Hugging Face | Temperature, top-k, top-p with code (revision from Week 1) |
