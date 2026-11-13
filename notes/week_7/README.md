# Week 7: Retrieval-Augmented Generation Basics

**Paper:** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) (Lewis et al., 2020)
**Lab:** build a minimal RAG pipeline over a small document set.
**Code:** [`src/rag_corpus.py`](../../src/rag_corpus.py) (documents and questions) · [`src/rag.py`](../../src/rag.py) (chunking, BM25, dense embeddings, index, prompts, scoring) · [`src/run_rag_bench.py`](../../src/run_rag_bench.py) (runner and analysis) · [`tests/test_week7.py`](../../tests/test_week7.py)
**Notebook:** [`week7_rag_colab.ipynb`](../../jupyter/week7_rag_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week7_rag_colab.ipynb) (about 30 minutes on a free T4). It walks through each step with the code, the intermediate output and the figures inline.

**Status:** plan fixed, test run pending.

## The paper in brief

| | Lewis et al. (2020) |
|---|---|
| Question | Can a generator that reads retrieved passages beat a model that has to hold every fact in its weights? |
| Method | A DPR retriever (two BERT encoders) finds the top k of 21 million 100-word Wikipedia passages; a BART generator conditions on each. RAG-Sequence uses one passage per whole answer, RAG-Token can switch passage per token, and both marginalise over the k passages. The query encoder and generator are trained together; the passage index stays fixed |
| Results | State of the art on four open-domain QA sets at the time, and answers that human raters judged more factual and specific than BART alone |
| Two claims I can test | (1) Retrieval beats closed-book on knowledge-intensive questions. (2) Swapping the index (a 2016 Wikipedia dump for a 2018 one) updates what the model knows with no retraining |
| What I change | No training: a prompted instruct model reads the top k chunks pasted into its prompt, best first. That is how most RAG systems are built today, and it is what the lab asks for |

## The pipeline

| Step | What it does |
|---|---|
| Documents | 60 product pages for fictional products: 15 brands × 4 models (for example "Corvane C-200, camera drone"), about 154 words each, in three paragraphs. Each page states 7 facts: release year, assembly town, weight, power rating, colour, list price, warranty. Every brand, town and number is made up, so a model **cannot** know them without retrieval |
| Hard part | The four models in a family share almost all their wording and differ only in the numbers. Later paragraphs say "the C-200" or "it", never the full name |
| Questions | One question per (product, fact), worded differently from the page where it reads naturally ("first come out" for "first released", "how much does it weigh" for "weighs"). **Test:** 200 questions about 12 brands (48 products). **Dev:** questions about 3 other brands, never used in the test |
| Chunking | Windows of 64 words overlapping by 16 words: 180 chunks, about 3 per page |
| Retrieval | **Dense:** [`bge-small-en-v1.5`](https://huggingface.co/BAAI/bge-small-en-v1.5) (33M parameters), [CLS] vector, cosine similarity. **Sparse:** BM25 written from scratch (k1 = 1.5, b = 0.75). **Hybrid:** reciprocal rank fusion of the two |
| Generation | Qwen2.5-1.5B-Instruct and 3B-Instruct, greedy, up to 24 new tokens. The prompt lists the k chunks as `[1] … [2] …`, then the question, and asks for the bare answer or `unknown` |
| Scoring | Numbers are compared as numbers (`€2,339`, `2339 euros` and `2,339` all count). Colours and towns must name the right option and no other option. The product's own code is removed first, so "The C-200 weighs 16.1 kg" is read as 16.1 |

**Conditions**, the same 200 questions each:

| Condition | Context in the prompt | Role |
|---|---|---|
| `closed` | None | The model's own knowledge: should be near 0 |
| `oracle` | The whole gold page, nothing else | The ceiling: perfect retrieval |
| `dense_k3` | Top 3 chunks, dense | **The main pipeline** |
| `dense_k1`, `dense_k5`, `dense_k10` | Top 1, 5, 10 chunks, dense | How much context helps or distracts |
| `bm25_k3`, `hybrid_k3` | Top 3 chunks, BM25 or hybrid | Other retrievers |
| `swap_dense_k3` | Top 3 chunks from **edition 2** of the pages, where weight, power, colour, price and warranty all changed | The index swap: gold answers are the new values |

**Measured before the run (no model needed):** with 64-word chunks, BM25 puts the answer-bearing chunk first for 55% of test questions and in the top 3 for 100%. The product code ("C-200") is a rare, exact token, which suits BM25. How the dense retriever handles codes that differ by one digit is open.

## Plan (fixed before the test run)

**Data:** 200 test questions (fixed seed) about 48 products that no prompt or scoring work ever used. Development used the 3 dev brands only.

**Models:** Qwen2.5-1.5B-Instruct and Qwen2.5-3B-Instruct, greedy decoding. Embeddings: bge-small-en-v1.5.

| | Hypothesis | Test | Supported if |
|---|---|---|---|
| **H1** (confirmatory, Lewis et al. claim 1) | RAG answers at least 20 points more questions than closed-book, at each size | `dense_k3` vs `closed`, paired. Exact McNemar, paired bootstrap CI, Holm across the 2 models | Holm p < 0.05, CI lower bound > 0, effect ≥ 20 points |
| **H2** (confirmatory) | The retriever is not the bottleneck: `dense_k3` is within ±5 points of `oracle`, at each size | Paired bootstrap 95% CI on `dense_k3` − `oracle` | Whole CI inside ±5. Below it: retrieval or distractors cost accuracy. Above it: chunks are easier to read than whole pages |
| Exploratory | k from 1 to 10; BM25 and hybrid vs dense; the index swap (Lewis et al. claim 2), including answers that give the old value; where wrong answers come from (answer not retrieved, a sibling product's value, `unknown`, other); accuracy by fact; a retrieval-only sweep over chunk size (32, 64, 128 words, whole page), title-in-every-chunk and method | Counts, Wilson CIs, paired CIs | Reported, no significance claims |

**Dev gate** (the lesson from Week 6, where a model at its floor made a hypothesis meaningless): before the test run, 24 dev questions on the 1.5B model under `closed`, `dense_k3` and `oracle`. If `oracle` is below 50%, the test run does not start; the reason and any change go into a new commit first.

**Power:**
- **H1:** closed-book should sit near 0, so any RAG accuracy above 25% gives a McNemar p far below 0.001.
- **H2:** if RAG and oracle disagree on 5% of questions, the CI is about ±3 points and equivalence can be shown. At 10% it is about ±4.3. Beyond about 12% disagreement, equivalence can't be shown even with no real difference.

**Threats:**
- The documents are templated and uniform. Real pages vary far more in length and structure, so the absolute numbers here say little about real corpora. The comparisons between conditions are the point.
- Questions name the product exactly, which favours BM25. Real users misspell and paraphrase names.
- `oracle` passes a whole page (about 154 words) while `dense_k3` passes about 190 words of chunks. H2 compares two realistic configurations, not equal context lengths.
- The swap changes numbers only. Lewis et al. swapped whole Wikipedia dumps; here the wording stays the same, which makes the swap easier.
- One model family, one embedding model, one document type.

## Results

Pending the test run.

## Files

| File | What |
|---|---|
| [`src/rag_corpus.py`](../../src/rag_corpus.py) | The 60 product pages (two editions) and the questions |
| [`src/rag.py`](../../src/rag.py) | Chunking, BM25, dense embedder, index, prompts, answer scoring |
| [`src/run_rag_bench.py`](../../src/run_rag_bench.py) | Runs every condition, the retrieval sweep, and the analysis |
| [`tests/test_week7.py`](../../tests/test_week7.py) | Model-free checks, including a full run with a fake model |
| [`jupyter/week7_rag_colab.ipynb`](../../jupyter/week7_rag_colab.ipynb) | The Colab walkthrough and run |
| [`resources.md`](resources.md) | Reading list |
