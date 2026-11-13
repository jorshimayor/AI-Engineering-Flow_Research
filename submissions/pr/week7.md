**Title:** Week 7: joshua - minimal RAG pipeline over a small document set, closed-book vs retrieval vs oracle

## Task

Week 7, Retrieval-augmented generation basics (anchor: *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, Lewis et al., 2020).
Lab: build a minimal RAG pipeline over a small document set.

## What I did

- **Documents:** 60 pages about fictional products (15 brands × 4 models, 7 facts each), so a model cannot answer from memory. Models in a family share their wording and differ in the numbers. A second edition with changed values tests the paper's index swap.
- **Pipeline:** 64-word chunks with 16 words of overlap; BM25 written from scratch; dense retrieval with bge-small-en-v1.5; a hybrid by reciprocal rank fusion; a prompt with the top k chunks that asks for the bare answer or "unknown".
- **Conditions:** closed-book, oracle (gold page only), dense k = 1, 3, 5, 10, BM25 and hybrid at k = 3, and the swapped index. 200 test questions each.
- **Models:** Qwen2.5-1.5B and 3B Instruct, greedy, on a Colab T4. Two hypotheses and a dev gate committed before the test run.

**Results** (200 questions, accuracy with 95% Wilson CI):

| Model | Closed-book | Dense, k = 3 (main) | BM25, k = 3 | Oracle | Swapped index |
|---|---|---|---|---|---|
| 1.5B | 3.0% (1.4 to 6.4) | 97.5% (94.3 to 98.9) | 99.5% | 100% | 98.0% |
| 3B | 0% (0 to 1.9) | 98.5% (95.7 to 99.5) | 99.5% | 100% | 99.0% |

**Pre-registered hypotheses:**
- **H1 (RAG beats closed-book by ≥ 20 points at each size): supported.** +94.5 (CI +91.0 to +97.5) and +98.5 (CI +96.5 to +100.0), Holm p < 10⁻⁵⁶.
- **H2 (RAG within ±5 points of the oracle): equivalent at 3B, inconclusive at 1.5B.** 3B: −1.5 (CI −3.5 to 0.0). 1.5B: −2.5 (CI −5.0 to −0.5), with the lower bound exactly on the margin.

**Exploratory findings:**
- Closed-book, the 1.5B model invented answers for 154 of 200 questions; the 3B model said "unknown" for 82%. With documents, both said "unknown" every time the answer was missing (47 of 47 at k = 1).
- All 47 k = 1 misses were colour or power questions: the retriever picked the right page and the wrong chunk.
- k = 3 matches k = 10 at a third of the tokens. At 1.5B, k = 5 gave a sibling product's value 6 times.
- Putting the page title in every chunk lifts small-chunk retrieval (32 words, top 3: BM25 50% → 97%, dense 68% → 92%).
- The swapped index gave the new values 98 to 99% of the time and never an old one.

## Files (`Week7/joshua/`)

| File | Contents |
|---|---|
| `src/rag_corpus.py` | The 60 pages (two editions) and the questions, with dev and test brands |
| `src/rag.py` | Chunking, BM25, dense embedder, hybrid fusion, index, prompts, answer scoring |
| `src/run_rag_bench.py` | Runner over the 9 conditions, retrieval-only sweep, H1/H2 tests, failure breakdown |
| `src/run_prompt_bench.py`, `src/stats.py`, `src/figures.py`, `src/gsm8k.py`, `src/prompts.py` | Earlier-week modules it imports (batched model, statistics, figures) |
| `tests/test_week7.py` | Model-free checks, including a full run with a fake model |
| `week7_rag_colab.ipynb` | Step-by-step walkthrough, executed on the test run (about 30 minutes on a free T4) |
| `results/*.jsonl` | All 3,600 answers (2 models × 9 conditions × 200) with retrieved chunk ids; `retrieval.json`; `dev/` gate |
| `README.md` | Paper summary, pipeline, plan, results, exploratory findings, caveats |
| `figures/` | Accuracy by condition; accuracy vs k; retrieval sweep; failure breakdown |

## Limitations

- The oracle scored 100%, so the task sits at a ceiling: templated pages and exact product names make it easier than real retrieval.
- One embedding model, one model family, greedy decoding, 200 questions.
- The index swap changes numbers only, so it is easier than Lewis et al.'s swap of whole Wikipedia dumps.
- There is no Week 7 brief in this repo yet, so the files follow the curriculum's lab description.

## Submission rules

- [x] Branch `week7_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week7/joshua/`
- [x] No shared files or other fellows' folders edited
- [x] Hypotheses committed before the test run: https://github.com/jorshimayor/AI-Engineering-Flow_Research/commit/174467a

Full notes, reading list and article plans: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_7
