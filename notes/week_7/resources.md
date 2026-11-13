# Week 7 Resources: Retrieval-Augmented Generation

Links checked 13 November 2026. ⭐ = start here.

## Papers

| Paper | Why |
|---|---|
| ⭐ [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401), Lewis et al. 2020 | The anchor paper: a retriever and a generator trained together; index hot-swapping |
| [REALM](https://arxiv.org/abs/2002.08909), Guu et al. 2020 | Retrieval during pre-training, published the same year |
| ⭐ [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906), Karpukhin et al. 2020 | The retriever inside RAG; the Week 12 reading |
| [Fusion-in-Decoder](https://arxiv.org/abs/2007.01282), Izacard and Grave 2020 | Read many passages at once; close to pasting the top k into one prompt |
| [RETRO](https://arxiv.org/abs/2112.04426), Borgeaud et al. 2021 | Retrieval from trillions of tokens at training and inference time |
| ⭐ [Lost in the Middle](https://arxiv.org/abs/2307.03172), Liu et al. 2023 | Models use passages at the start and end of the context best; why k and order matter |
| [Retrieval-Augmented Generation for LLMs: A Survey](https://arxiv.org/abs/2312.10997), Gao et al. 2023 | Naive, advanced and modular RAG |
| [BEIR](https://arxiv.org/abs/2104.08663), Thakur et al. 2021 | BM25 is a strong baseline across domains; the Week 14 reading |
| [C-Pack](https://arxiv.org/abs/2309.07597), Xiao et al. 2023 | The paper behind the BGE embedding models used here |
| [MTEB](https://arxiv.org/abs/2210.07316), Muennighoff et al. 2022 | How embedding models are compared |

## Methods used in the lab

| Resource | Notes |
|---|---|
| [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf), Robertson and Zaragoza 2009 | Where the BM25 formula in `src/rag.py` comes from |
| [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf), Cormack et al. 2009 | The hybrid: add 1 / (60 + rank) from each retriever |
| [bge-small-en-v1.5 model card](https://huggingface.co/BAAI/bge-small-en-v1.5) | [CLS] pooling, normalised vectors, and the query instruction prefix |
| ⭐ [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval), Anthropic | Chunks lose their context; prepending it helps. The title-in-every-chunk variant in the sweep is the simplest version |
| [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Choosing an embedding model |
| [RAG in Hugging Face Transformers](https://huggingface.co/docs/transformers/model_doc/rag) | The original RAG-Sequence and RAG-Token models, ready to load |
