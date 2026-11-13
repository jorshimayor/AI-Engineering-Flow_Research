# Article 1: A minimal RAG pipeline (outline)

## Title options
- **I Gave a Small Model 60 Invented Products and a Retriever**
- RAG From Scratch in About 200 Lines, Measured Properly
- From 3% to 98%: What Retrieval Does to a 1.5B Model

**Target reader:** has called a vector database from a framework, never built the pieces or measured them against a closed-book baseline and a perfect retriever.
**Promise:** every part of a RAG pipeline in plain Python, the two baselines that make its numbers mean something, and what changed when the model could read.
**Length:** ~1,500 words · **Hero:** `week7_accuracy_by_condition.png`

---

## Outline

### 1. Hook (~120 words)
"What colour is the Corvane C-200 sold in?" Closed-book, the 1.5B model says "Black". The C-200 doesn't exist; its page says sky blue. With three retrieved chunks it says "sky blue". With the wrong chunks it says "unknown".

### 2. Lewis et al. in one paragraph (~150 words)
- A retriever (DPR) and a generator (BART), trained together over 21 million Wikipedia passages.
- Two claims worth testing small: retrieval beats closed-book on knowledge questions; swapping the index updates the knowledge without retraining.
- What I changed: no training, a prompted instruct model reading the top k chunks.

### 3. Why invented documents (~150 words)
- A model can't know facts that don't exist, so closed-book is a true zero and every correct answer came from retrieval.
- 15 brands × 4 models; siblings share their wording and differ in the numbers. The trap for retrieval.

### 4. The pipeline (~400 words)
- Chunking: 64-word windows, 16 words of overlap. Show one page cut into three chunks.
- BM25 in about 30 lines; bge-small embeddings and cosine similarity; reciprocal rank fusion.
- The prompt: numbered chunks, the question, "reply with only the answer, or unknown".
- Scoring numbers as numbers, and flagging a sibling product's value.

### 5. Two baselines and two hypotheses (~200 words)
- Closed-book (the floor) and oracle (the gold page only, the ceiling).
- H1: RAG beats closed-book by ≥ 20 points. H2: RAG within ±5 of the oracle. Both fixed before the run, with a dev gate.

### 6. Results (~300 words)
- H1: +94.5 and +98.5 points. Supported, and expected.
- H2: −1.5 at 3B (equivalent), −2.5 at 1.5B with the interval ending exactly at −5 (inconclusive by the rule).
- The oracle scored 100%: the reader was never the bottleneck, which is the honest limit of this test.
- The index swap: new values 98 to 99% of the time, no stale answers.

### 7. The finding I didn't plan for (~150 words)
Closed-book, the 1.5B model invented 154 answers; the 3B said "unknown" 82% of the time. With documents, both said "unknown" every time the answer was missing (47 of 47 at k = 1). The instruction to abstain works when the context is the only source.

### 8. Reproduce this
Colab link, about 30 minutes on a free T4; the notebook shows every step's output.

---

## Stretch experiment
**Conflicting editions.** Put editions 1 and 2 in the same index, add "(2025 edition)" and "(2026 edition)" to the titles, and ask for the current value. Measure how often the model picks the newer page, and whether it says so.

## Self-check (closed-book)
1. Why does an invented corpus make closed-book a true zero?
2. What do the closed-book and oracle conditions each tell you that RAG accuracy alone can't?
3. Why was H2 inconclusive at 1.5B when RAG lost only 2.5 points?
4. What is reciprocal rank fusion, and why does it need no score calibration?
5. Which of Lewis et al.'s claims did the index swap test, and why was it easy here?
