# Week 7 Articles

| # | Article | Covers | Outline |
|---|---|---|---|
| 1 | I Gave a Small Model 60 Invented Products and a Retriever | A minimal RAG pipeline from scratch: chunking, BM25, embeddings, the prompt, and what retrieval does to a model that cannot know the answers | [01-minimal-rag.md](01-minimal-rag.md) |
| 2 | My Retriever Found the Right Page and the Wrong Paragraph | Where a RAG pipeline's errors come from: chunk boundaries, question wording, k, sibling distractors, and the title-in-every-chunk fix | [02-where-rag-fails.md](02-where-rag-fails.md) |

**Order:** 1 then 2.
**Figures:** [`results/figures/week7_accuracy_by_condition.png`](../../../results/figures/week7_accuracy_by_condition.png), [`results/figures/week7_topk.png`](../../../results/figures/week7_topk.png), [`results/figures/week7_retrieval_sweep.png`](../../../results/figures/week7_retrieval_sweep.png), [`results/figures/week7_failures.png`](../../../results/figures/week7_failures.png).
**Hook:** asked about products that don't exist, the 1.5B model invented an answer for 154 of 200 questions. Given the right documents, it said "unknown" every single time the answer wasn't in them.
**Report honestly:** H1 holds by a mile because the facts are invented; H2 holds at 3B and misses at 1.5B on the boundary; the oracle scored 100%, so the task sits at a ceiling; everything after the two hypotheses is exploratory.

Each outline has self-check questions and one stretch experiment.
