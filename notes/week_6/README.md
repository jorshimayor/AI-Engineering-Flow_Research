# Week 6: Structured Outputs, Tool Calling and MCP

**Papers:** [Toolformer](https://arxiv.org/abs/2302.04761) (Schick et al., 2023) · [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest) (Anthropic, 2024)
**Lab:** build a two-tool calling pipeline with schema validation and malformed-output handling, then re-expose the same tools behind an MCP server and compare the integration effort.
**Code:** [`src/tools.py`](../../src/tools.py) (tools, schemas, reply parser) · [`src/tool_agent.py`](../../src/tool_agent.py) (loop, repair, MCP client) · [`src/mcp_server.py`](../../src/mcp_server.py) · [`src/tool_tasks.py`](../../src/tool_tasks.py) (tasks) · [`src/run_tool_bench.py`](../../src/run_tool_bench.py) (runner and analysis) · [`tests/test_week6.py`](../../tests/test_week6.py)
**Notebook:** [`week6_tool_calling_colab.ipynb`](../../jupyter/week6_tool_calling_colab.ipynb) · [open in Colab](https://colab.research.google.com/github/jorshimayor/AI-Engineering-Flow_Research/blob/main/jupyter/week6_tool_calling_colab.ipynb) (about 1 hour on a free T4)

**Status:** plan fixed and committed; test run pending.

## The readings in brief

| | Toolformer | MCP specification |
|---|---|---|
| Question | Can a model teach itself when and how to call tools? | How should any app expose tools and context to any model client? |
| Method | The model inserts candidate API calls into its own training text and keeps those that make the following tokens easier to predict, then fine-tunes on them | JSON-RPC 2.0 between hosts, clients and servers. Servers offer tools, resources and prompts; each tool has a name, a description and a JSON Schema for its input |
| Tools | Calculator, question answering, Wikipedia search, translation, calendar | Anything a server implements |
| Lesson for this lab | Calling a tool is a decision the model makes in text, so it can be badly formed | A failed tool call is reported inside the result (`isError`), so the model can see it and try again |

## The pipeline

| Part | What it does |
|---|---|
| Tools | `lookup_price(item)` (prices are random, so the model can't know them) and `calculate(expression)` (Week 3's safe parser, never `eval`) |
| Tasks | 200 shopping questions in 6 shapes (two items, three items, change from a note, discount, budget, difference). Exact gold answers |
| Calls | Qwen2.5's native format: `<tool_call>{"name": ..., "arguments": {...}}</tool_call>`, schemas in the chat template |
| Final answer | Structured output: only `{"answer": <number>}`, validated against a JSON Schema |
| Validation | Every reply is parsed into tool calls, a final answer, or one of four malformed types: invalid JSON, unknown tool, arguments that fail the schema, final answer not valid JSON |
| Repair | A malformed reply is never executed. The model is told what was wrong and asked again, up to 3 times per problem |
| Tool errors | A well-formed call that fails (unknown item, bad expression) is returned to the model as the tool result, as the MCP spec recommends |
| Routes | **Direct:** tools called as Python functions, schemas written by hand. **MCP:** the same functions behind an MCP server over stdio, with the schemas the server generates |

## Integration effort (measured before the run, no model needed)

| | Direct | MCP |
|---|---|---|
| Code (non-blank, non-comment lines) | 26: hand-written schemas and a dispatcher | 71: server 33, client 38 |
| Where the schema comes from | Written by hand as JSON | Generated from type hints and docstrings |
| Schema differences | `additionalProperties: false` | Not set by default, so extra arguments pass; adds `title` fields |
| Tool errors reach the model | Yes | Only if the server raises the SDK's `ToolError`; any other exception becomes "Error executing tool <name>" with the reason hidden |
| Result text | Compact JSON | Pretty-printed JSON |
| Cost per call | About 0.01 ms | About 2 ms (stdio round trip), plus about 3 s to start the server |
| Reuse | This loop only | Any MCP client (desktop apps, IDEs, other agents) without changes |
| Version trap | | `mcp` 2.x renamed `FastMCP` to `MCPServer` and moved fields to snake_case (`input_schema`, `is_error`); v1 tutorials no longer run |

The model-free tests ([`tests/test_week6.py`](../../tests/test_week6.py)) check that both routes handle the same scripted cases the same way:
- 17 known-bad replies, each classified correctly.
- A clean run.
- A repaired run.
- A run that exhausts its repairs.
- A tool error.
- A final answer in prose.

## Plan (fixed before the test run)

**Data:** 200 test problems (fixed seed) using 24 catalogue items that no prompt or parser work ever saw. Development used 8 other items (`make_problems("dev")`).

**Models:** Qwen2.5-1.5B-Instruct and Qwen2.5-3B-Instruct, greedy decoding, up to 8 turns and 256 new tokens per turn.

| | Hypothesis | Test | Supported if |
|---|---|---|---|
| **H1** (confirmatory) | Validation with repair solves at least 5 points more problems than failing closed, at each size | Fail-closed = the same run, scored as failed at its first malformed reply. Exact McNemar, paired bootstrap CI, Holm across the 2 models | Holm p < 0.05, CI lower bound > 0, effect ≥ 5 points |
| **H2** (confirmatory) | Moving the tools behind MCP doesn't change success: MCP within ±5 points of direct, at each size | Paired bootstrap 95% CI on MCP − direct | Whole CI inside ±5. Outside it in either direction: the integration changed behaviour |
| Exploratory | Malformed reply types; share of malformed runs recovered; tool errors; turns; tokens; MCP latency | Counts, Wilson CIs | Reported, no significance claims |

**Power:**
- **H1:** the repair-minus-fail-closed difference can only be positive. With 200 problems, a true 5-point gain gives 80% power at Holm's α = 0.025.
- **H2:** routes that disagree on 5% of problems give a CI of about ±3 points, enough to show equivalence. At 15% disagreement, equivalence can't be shown.

**Threats:**
- The MCP route sees different schema text and result formatting from the direct route. That is the point of the comparison, but it means H2 tests "MCP with its defaults", not the transport alone.
- Generation is batched, and batches can differ between routes once conversations diverge, adding small numeric noise in fp16.
- One model family, one task family.

## Results

*Pending the Colab run.*

## Files

- Results (after the run): `results/week6/` (one JSONL per model: both routes, full transcripts, every malformed reply)
- Reading list: [`resources.md`](resources.md)
