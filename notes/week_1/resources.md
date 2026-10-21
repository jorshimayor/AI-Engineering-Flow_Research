# Transformer Resources

A curated list for going deeper after Week 1. All links were checked on 2026-09-26.

**Legend:** ⭐ = start here · 🟢 beginner · 🟡 intermediate · 🔴 advanced · 💻 hands-on code

---

## Suggested path

If you only do a few things, do these in order:

1. ⭐ 3Blue1Brown, *Transformers, the tech behind LLMs* + *Attention in transformers* (videos, ~1 hr total) to build intuition.
2. ⭐ Jay Alammar, *The Illustrated Transformer* (article) for the architecture diagrams.
3. ⭐ Read *Attention Is All You Need* alongside *The Annotated Transformer*, which is the paper with runnable code.
4. ⭐ Karpathy, *Let's build the GPT Tokenizer* (video, 2 hr), which goes deep on Week 1's tokenisation topic.
5. ⭐ Karpathy, *Let's build GPT: from scratch* (video, 2 hr) to build one yourself.
6. Play with **Transformer Explainer** and **LLM Visualization** (interactive tools).

---

## 1. Papers

### The foundation
| Paper | Year | Why read it |
|---|---|---|
| ⭐ [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Vaswani et al. | 2017 | The Week 1 paper. Introduced the transformer |
| [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473), Bahdanau et al. | 2014 | The original attention mechanism (on RNNs) that transformers built on |
| [Efficient Estimation of Word Representations (word2vec)](https://arxiv.org/abs/1301.3781), Mikolov et al. | 2013 | Where the embedding intuition comes from |
| [Deep Residual Learning (ResNet)](https://arxiv.org/abs/1512.03385), He et al. | 2015 | Residual connections, a key part of every transformer block |
| [Layer Normalization](https://arxiv.org/abs/1607.06450), Ba et al. | 2016 | The "Norm" in "Add & Norm" |

### The GPT lineage (decoder-only, what we used in Week 1)
| Paper | Year | Why read it |
|---|---|---|
| [GPT-1: Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 2018 | Decoder-only pretraining + fine-tuning |
| ⭐ [GPT-2: Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | 2019 | **The model we probed.** Introduces byte-level BPE (section 2.2) |
| [GPT-3: Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) | 2020 | Scale leads to in-context learning |
| [BERT](https://arxiv.org/abs/1810.04805), Devlin et al. | 2018 | The encoder-only counterpart, for contrast |

### Tokenisation (Week 1 deep-dive)
| Paper / post | Why read it |
|---|---|
| ⭐ [Neural Machine Translation of Rare Words with Subword Units (BPE)](https://arxiv.org/abs/1508.07909), Sennrich et al. 2015 | The BPE algorithm GPT-2 uses |
| [SentencePiece](https://arxiv.org/abs/1808.06226), Kudo & Richardson 2018 | The tokeniser behind Llama, T5 and others |
| [Language Model Tokenizers Introduce Unfairness Between Languages](https://arxiv.org/abs/2305.15425), Petrov et al. 2023 | The "token tax" we measured (Hindi 5.4×) |
| [SolidGoldMagikarp (LessWrong)](https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/solidgoldmagikarp-plus-prompt-generation), Rumbelow & Watkins 2023 | The original glitch-token discovery |
| [Fishing for Magikarp: Detecting Under-trained Tokens](https://arxiv.org/abs/2405.05417), Land & Bartolo 2024 | Better detection than our centroid test |

### Architecture improvements since 2017
| Paper | Why read it |
|---|---|
| [On Layer Normalization in the Transformer Architecture (Pre-LN)](https://arxiv.org/abs/2002.04745) | Why GPT-2 moved the LayerNorm, and why it trains more stably |
| [RoFormer: Rotary Position Embedding (RoPE)](https://arxiv.org/abs/2104.09864) | The positional scheme used by most modern LLMs (Llama, Qwen, Mistral) |
| [Fast Transformer Decoding: Multi-Query Attention](https://arxiv.org/abs/1911.02150), Shazeer 2019 | Shrinks the KV cache |
| [GQA: Grouped-Query Attention](https://arxiv.org/abs/2305.13245) | The middle ground used in Llama 2/3 |
| 🔴 [FlashAttention](https://arxiv.org/abs/2205.14135), Dao et al. 2022 | Exact attention made fast and memory-efficient through IO-awareness |
| 🔴 [Formal Algorithms for Transformers](https://arxiv.org/abs/2207.09238), Phuong & Hutter 2022 | Precise pseudocode for every transformer variant |

### Generation and decoding
| Paper | Why read it |
|---|---|
| ⭐ [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751), Holtzman et al. 2019 | Introduces **top-p (nucleus) sampling** and explains why greedy decoding loops, as we saw |
| [Efficient Streaming Language Models with Attention Sinks (StreamingLLM)](https://arxiv.org/abs/2309.17453), Xiao et al. 2023 | The attention sinks we measured (82% on token 0) |

### Scaling
| Paper | Why read it |
|---|---|
| [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361), Kaplan et al. 2020 | Loss follows a power law in params, data and compute |
| [Training Compute-Optimal LLMs (Chinchilla)](https://arxiv.org/abs/2203.15556), Hoffmann et al. 2022 | About 20 tokens per parameter |

### Interpretability (what attention heads *actually* do)
| Paper | Why read it |
|---|---|
| 🔴 [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html), Anthropic 2021 | The residual-stream view of transformers |
| 🔴 [In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html), Anthropic 2022 | A head type you can find in GPT-2 yourself |
| [What Does BERT Look At?](https://arxiv.org/abs/1906.04341), Clark et al. 2019 | Classic attention-head analysis, including coreference heads |
| [Attention is not Explanation](https://arxiv.org/abs/1902.10186), Jain & Wallace 2019 | Why our "it → animal" head needed a caveat |
| [Tracing the Thoughts of a Large Language Model](https://www.anthropic.com/research/tracing-thoughts-language-model), Anthropic 2025 | Modern circuit tracing on a production model |

---

## 2. YouTube videos

### Intuition first 🟢
| Video | Channel | Length |
|---|---|---|
| ⭐ [Transformers, the tech behind LLMs (Ch. 5)](https://www.youtube.com/watch?v=wjZofJX0v4M) | 3Blue1Brown | ~27 min |
| ⭐ [Attention in transformers, step-by-step (Ch. 6)](https://www.youtube.com/watch?v=eMlx5fFNoYc) | 3Blue1Brown | ~26 min |
| [How might LLMs store facts (Ch. 7)](https://www.youtube.com/watch?v=9-Jl0dxWQs8) | 3Blue1Brown | ~23 min |
| [Full "Neural networks" playlist](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) | 3Blue1Brown | Chapters 1–4 cover backprop basics |
| [Transformer Neural Networks, Clearly Explained](https://www.youtube.com/watch?v=zxQyTK8quyY) | StatQuest (Josh Starmer) | ~36 min |
| [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) | Andrej Karpathy | 1 hr |
| [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) | Andrej Karpathy | 3.5 hr, covers pretraining to RLHF |

### Paper walkthroughs 🟡
| Video | Channel |
|---|---|
| [Attention Is All You Need (paper explained)](https://www.youtube.com/watch?v=iDulhoQ2pro) | Yannic Kilcher |
| [Attention is all you need: model explanation incl. math, inference and training](https://www.youtube.com/watch?v=bCz4OMemCcA) | Umar Jamil |

### Build it yourself 💻
| Video | Channel | Covers |
|---|---|---|
| ⭐ [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | Andrej Karpathy | BPE from scratch; explains *every* tokeniser quirk we found |
| ⭐ [Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY) | Andrej Karpathy | Self-attention and a full GPT in PyTorch |
| [Let's reproduce GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU) | Andrej Karpathy | Trains the exact model we probed |
| [Coding a Transformer from scratch on PyTorch](https://www.youtube.com/watch?v=ISNdQcPhsts) | Umar Jamil | The full encoder-decoder from the paper |
| [Neural Networks: Zero to Hero (playlist)](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) | Andrej Karpathy | The whole series, from backprop up to GPT |

---

## 3. Courses

### DeepLearning.AI
| Course | Level | Notes |
|---|---|---|
| ⭐ [How Transformer LLMs Work](https://www.deeplearning.ai/short-courses/how-transformer-llms-work/) | 🟢 | Jay Alammar & Maarten Grootendorst. Tokenisers, embeddings, attention, a direct match for Week 1 |
| [Attention in Transformers: Concepts and Code in PyTorch](https://www.deeplearning.ai/short-courses/attention-in-transformers-concepts-and-code-in-pytorch/) | 🟢💻 | Josh Starmer (StatQuest). Codes self-, masked and multi-head attention |
| [Sequence Models (Deep Learning Specialization, Course 5)](https://www.coursera.org/learn/nlp-sequence-models) | 🟡 | Andrew Ng. RNNs through attention and transformers |
| [Generative AI with Large Language Models](https://www.coursera.org/learn/generative-ai-with-llms) | 🟡 | With AWS. The LLM lifecycle: pretraining, fine-tuning, RLHF |

### University courses (free)
| Course | Level | Notes |
|---|---|---|
| ⭐ [Stanford CS224N: NLP with Deep Learning](https://web.stanford.edu/class/cs224n/) | 🟡 | [Lecture videos (Spring 2024)](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D). The gold-standard NLP course |
| [Stanford CS25: Transformers United](https://web.stanford.edu/class/cs25/) | 🟡 | Seminar series with talks from researchers |
| 🔴 [Stanford CS336: Language Modeling from Scratch](https://stanford-cs336.github.io/) | 🔴💻 | Build tokeniser, transformer, training and inference yourself. Hard |
| [MIT 6.S191: Intro to Deep Learning](https://introtodeeplearning.com/) | 🟢 | Fast, well-produced overview |
| [fast.ai Part 2: Deep Learning Foundations](https://course.fast.ai/Lessons/part2.html) | 🟡💻 | Builds from the foundations up, including attention |

### Other
| Course | Level | Notes |
|---|---|---|
| ⭐ [Hugging Face LLM Course](https://huggingface.co/learn/llm-course) | 🟢💻 | Practical `transformers` library usage. [Chapter 6 covers tokenisers in depth](https://huggingface.co/learn/llm-course/chapter6/1) |
| [ARENA](https://www.arena.education/) | 🔴💻 | Alignment Research Engineer Accelerator. Its Chapter 1 builds GPT-2 from scratch and then does interpretability on it (TransformerLens) |

---

## 4. Articles and blogs

| Article | Level | Notes |
|---|---|---|
| ⭐ [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), Jay Alammar | 🟢 | The famous visual explanation |
| ⭐ [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/), Jay Alammar | 🟢 | Decoder-only, masked self-attention: exactly our model |
| [The Illustrated Word2vec](https://jalammar.github.io/illustrated-word2vec/), Jay Alammar | 🟢 | Embeddings intuition |
| ⭐ [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/), Harvard NLP | 🟡💻 | The paper, line by line, with PyTorch code |
| [Transformers from Scratch](https://peterbloem.nl/blog/transformers), Peter Bloem | 🟡 | Very clear derivation of self-attention |
| [Understanding and Coding Self-Attention from Scratch](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html), Sebastian Raschka | 🟡💻 | |
| [Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/), Lilian Weng | 🟡 | The history of attention mechanisms |
| [The Transformer Family v2.0](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/), Lilian Weng | 🔴 | Survey of every variant since 2017 |
| [How to generate text: decoding methods](https://huggingface.co/blog/how-to-generate), Hugging Face | 🟢💻 | Greedy, beam, top-k and top-p with examples (Week 1 Section 5) |
| [Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/), kipply | 🔴 | KV-cache memory, FLOPs, latency maths |
| [Understanding LSTMs](https://colah.github.io/posts/2015-08-Understanding-LSTMs/), Chris Olah | 🟢 | What transformers replaced |
| [Attention and Augmented RNNs](https://distill.pub/2016/augmented-rnns/), Distill | 🟢 | Beautiful pre-transformer attention visuals |

---

## 5. Interactive tools (play with these!)

| Tool | What it does |
|---|---|
| ⭐ [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) (Georgia Tech) | Runs GPT-2 **in your browser**. Type a prompt and watch each step, including a temperature slider |
| ⭐ [LLM Visualization](https://bbycroft.net/llm) (Brendan Bycroft) | 3D walk-through of every matrix multiplication in nanoGPT and GPT-2 |
| [Tiktokenizer](https://tiktokenizer.vercel.app/) | Paste text and see its tokens under GPT-2, cl100k, o200k, Llama and others. Great for repeating Section 1 |

---

## 6. Books

| Book | Level | Notes |
|---|---|---|
| ⭐ *Build a Large Language Model (From Scratch)*, Sebastian Raschka ([code on GitHub](https://github.com/rasbt/LLMs-from-scratch)) | 🟡💻 | Tokeniser, attention, GPT, pretraining, fine-tuning, step by step |
| *Hands-On Large Language Models*, Alammar & Grootendorst ([site](https://www.llm-book.com/)) | 🟢💻 | Very visual. Same authors as the DeepLearning.AI course |
| [*Understanding Deep Learning*](https://udlbook.github.io/udlbook/), Simon Prince (free PDF) | 🟡 | Chapter 12 is an excellent transformer chapter with great figures |
| [*Dive into Deep Learning*, Ch. 11: Attention & Transformers](https://d2l.ai/chapter_attention-mechanisms-and-transformers/index.html) (free) | 🟡💻 | Textbook with runnable code |
| [*Speech and Language Processing* (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/), Jurafsky & Martin (free) | 🟡 | The standard NLP textbook. Its transformer and LLM chapters are excellent |

---

## 7. Code repositories 💻

| Repo | What it's for |
|---|---|
| ⭐ [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) | ~300-line GPT-2 implementation plus training loop |
| ⭐ [karpathy/minbpe](https://github.com/karpathy/minbpe) | Minimal BPE tokeniser, the companion to the tokenizer video |
| [openai/tiktoken](https://github.com/openai/tiktoken) | OpenAI's fast BPE tokeniser, for comparing vocabularies |
| [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | Code for Raschka's book, as notebooks |
| [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) | Library for interpretability on GPT-2 and others (hooks, attention patterns, activation patching) |
| [Karpathy, Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) | Course page with notebooks for every video |
