# Source Code

| Module | Week | Purpose |
|---|---|---|
| [`icl.py`](icl.py) | 2 | Few-shot formats, KV-cached label scoring, calibration |
| [`react_agent.py`](react_agent.py) | 3, 4 | ReAct loop, safe calculator, local LLM wrapper (CPU or GPU), CLI |
| [`react_tasks.py`](react_tasks.py) | 3 | The 30 Week 3 problems |
| [`react_tasks_v2.py`](react_tasks_v2.py) | 4 | Harder problem generator: 4 levels, dev and held-out test splits, answer checks |
| [`run_react_bench.py`](run_react_bench.py) | 3, 4 | Resumable benchmark runner and summaries, CLI |
| [`stats.py`](stats.py) | 4 | Wilson CI, paired bootstrap, exact McNemar, sign-flip, Fisher, Holm, power |
| [`protocol_analysis.py`](protocol_analysis.py) | 4 | Pre-registered analysis for the test run |
| [`gsm8k.py`](gsm8k.py) | 5 | GSM8K download, fixed 400-problem test sample, train-split dev set |
| [`prompts.py`](prompts.py) | 5 | Prompt library: 5 strategies, worked examples, strict and lenient parsers |
| [`run_prompt_bench.py`](run_prompt_bench.py) | 5 | Batched, resumable GSM8K runner and paired summaries, CLI |
| [`tool_tasks.py`](tool_tasks.py) | 6 | Shopping problems that need both tools; random price catalogue; dev and test items |
| [`tools.py`](tools.py) | 6 | The two tools, hand-written schemas, reply parser with four malformed types |
| [`tool_agent.py`](tool_agent.py) | 6 | Batched tool-calling loop with validation and repair; MCP client |
| [`mcp_server.py`](mcp_server.py) | 6 | The same tools behind an MCP server (stdio) |
| [`run_tool_bench.py`](run_tool_bench.py) | 6 | Resumable runner over both routes; H1/H2 analysis and integration line counts, CLI |
| [`rag_corpus.py`](rag_corpus.py) | 7 | 60 fictional product pages (two editions) and questions with exact answers; dev and test brands |
| [`rag.py`](rag.py) | 7 | Chunking, BM25, dense embedder (bge-small), hybrid fusion, index, prompts, answer scoring |
| [`run_rag_bench.py`](run_rag_bench.py) | 7 | Resumable runner over 9 retrieval conditions; retrieval-only sweep; H1/H2 analysis and failure breakdown, CLI |
| [`figures.py`](figures.py) | all | Rebuilds `results/figures/` from saved results |

## CLI

```bash
uv run python src/react_agent.py "A truck carries 1,284 boxes with 36 cans each. 2,050 are damaged. How many good cans?"
uv run python src/run_react_bench.py --model Qwen/Qwen2.5-1.5B-Instruct          # Week 3 benchmark
uv run python src/run_react_bench.py --task dev --level 2 --max-steps 8          # Week 4 dev split
uv run python src/run_react_bench.py --summary results/week3/*.jsonl             # accuracy, CIs, cost
uv run python src/run_prompt_bench.py --model Qwen/Qwen2.5-1.5B-Instruct        # Week 5 prompt library (GPU)
uv run python src/run_tool_bench.py --model Qwen/Qwen2.5-1.5B-Instruct        # Week 6 tool calling, direct and MCP (GPU)
uv run python src/run_rag_bench.py --model Qwen/Qwen2.5-1.5B-Instruct         # Week 7 RAG, all conditions (GPU)
uv run python src/figures.py                                                     # rebuild figures
```

The calculator never calls `eval`; tool errors go back to the model as observations; runners save one result per line and resume after interruptions.
