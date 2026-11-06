**Title:** Week 6: joshua - two-tool calling pipeline with schema validation, repair and an MCP server

## Task

Week 6, Structured outputs, tool calling and MCP (anchors: *Toolformer*, Schick et al., 2023; the MCP specification).
Lab: build a two-tool calling pipeline with schema validation and malformed-output handling, then re-expose the tools behind an MCP server and compare the integration effort.

## What I did

- **Tools:** `lookup_price` (random prices, so the model must call it) and `calculate` (a safe parser, never `eval`).
- **Validation:** every reply is parsed into tool calls, a final `{"answer": N}` checked against a JSON Schema, or one of four malformed types (invalid JSON, unknown tool, arguments that fail the schema, final answer not valid JSON).
- **Malformed-output handling:** a malformed reply is never executed. The model is told what was wrong and retries, up to 3 times. A well-formed call that fails is returned to the model as the tool result.
- **MCP:** the same functions behind an MCP server (`mcp` 2.3.0, stdio), run on the same 200 problems as the direct route.
- **Models:** Qwen2.5-1.5B and 3B Instruct, greedy decoding, on a Colab T4. Two hypotheses committed before the test run.

**Integration effort:**

| | Direct | MCP |
|---|---|---|
| Code | 26 lines | 71 lines (server 33, client 38) |
| Schemas | Hand-written, strict | Generated from type hints; extra arguments allowed by default |
| Tool errors | Reach the model | Only via the SDK's `ToolError`, prefixed "Error executing tool <name>:" |
| Cost per call | 0.03 to 0.05 ms | About 2.3 ms, plus about 3 s server start |

**Results** (200 problems, success with 95% Wilson CI):

| Model | Direct, fail-closed | Direct, with repair | MCP, with repair |
|---|---|---|---|
| 1.5B | 1.5% | 1.5% (0.5 to 4.3) | 1.5% (0.5 to 4.3) |
| 3B | 22.5% | 31.5% (25.5 to 38.2) | 25.5% (20.0 to 32.0) |

**Pre-registered hypotheses:**
- **H1 (repair adds ≥ 5 points over fail-closed at each size): supported at 3B, not at 1.5B.**
  - 3B: +9.0 points (CI +5.5 to +13.0), 18 runs rescued, none broken, Holm p = 1.5 × 10⁻⁵.
  - 1.5B: +0. The model solves 3 of 200 either way, so there was nothing to rescue.
- **H2 (MCP within ±5 points of direct): inconclusive at 3B.**
  - 3B: −6.0 (CI −13.0 to +0.5).
  - 1.5B: level, but at a floor.

**Exploratory findings:**
- The main failure is planning, not format: 96% of 1.5B runs and 71% of 3B runs called `calculate` before any price came back. These are valid calls, so validation can't catch them.
- MCP was level before repair (fail-closed 24.5% vs 22.5%) and fell behind in the repair loop: 2 of 54 malformed runs recovered, against 18 of 78 direct.

## Files (`Week6/joshua/`)

| File | Contents |
|---|---|
| `src/tools.py` | The two tools, hand-written schemas, the reply parser and repair message |
| `src/tool_agent.py` | Batched tool-calling loop with repair; MCP client |
| `src/mcp_server.py` | The same tools as an MCP server |
| `src/tool_tasks.py` | 200 shopping problems with exact gold answers; dev and test item splits |
| `src/run_tool_bench.py` | Runner, summary, H1 and H2 tests, failure breakdown |
| `src/run_prompt_bench.py`, `src/stats.py`, `src/react_agent.py`, `src/gsm8k.py`, `src/prompts.py` | Earlier-week modules it imports (batched model, statistics, safe calculator) |
| `tests/test_week6.py` | Model-free checks: 17 bad replies, and a scripted loop over both routes |
| `week6_tool_calling_colab.ipynb` | The Colab run, about 1 hour on a free T4 |
| `results/*.jsonl` | All 800 runs (2 models × 2 routes × 200) with full transcripts and every malformed reply; `dev/` setup check |
| `README.md` | Plan, integration effort, results, exploratory findings, caveats |
| `figures/` | Success by route; malformed reply types |

## Limitations

- The 1.5B floor makes both hypotheses uninformative at that size. My dev check passed at 0 of 12 because it had no minimum-success gate.
- H2 tests MCP with its defaults (schema text, result formatting, error prefix), not the transport alone.
- One model family, greedy decoding, 200 problems, one task family. One question template reads "loaves of sourdough loaf".
- There is no Week 6 brief in this repo yet, so the files follow the curriculum's lab description.

## Submission rules

- [x] Branch `week6_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week6/joshua/`
- [x] No shared files or other fellows' folders edited
- [x] Hypotheses committed before the test run: https://github.com/jorshimayor/AI-Engineering-Flow_Research/commit/036ecbd

Full notes, reading list and article plans: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_6
