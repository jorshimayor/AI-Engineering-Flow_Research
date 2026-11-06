# Article 2: Direct vs MCP (outline)

## Title options
- **What Moving Two Tools Behind MCP Actually Cost**
- 26 Lines vs 71: Re-exposing My Tools Through MCP
- MCP Was Level Until the Model Made a Mistake

**Target reader:** has heard MCP is "USB-C for AI tools" and wants to know what changes when their own tools go behind it.
**Promise:** the real integration effort, three traps in the Python SDK, and a measured comparison of the same model with and without MCP.
**Length:** ~1,400 words · **Hero:** `week6_success_by_route.png`

---

## Outline

### 1. Hook (~100 words)
The same two functions, the same 200 problems, the same model. Behind an MCP server the 3B model solved 6 points fewer. Before any repair, it was level.

### 2. The MCP spec in one paragraph (~150 words)
- JSON-RPC between hosts, clients and servers; tools have a name, a description and a JSON Schema.
- A failed tool call is reported in the result (`isError`), so the model can read it.

### 3. Integration effort (~300 words)
- Direct: 26 lines (hand-written schemas, a dispatcher). MCP: 71 (server 33, client 38).
- What MCP gives back: any MCP client can use the tools unchanged.
- Trap 1: `mcp` 2.x renamed `FastMCP` to `MCPServer` and moved fields to snake_case. v1 tutorials no longer run.
- Trap 2: only the SDK's `ToolError` reaches the model, and with an "Error executing tool" prefix. Any other exception hides the reason.
- Trap 3: generated schemas don't set `additionalProperties: false`, so extra arguments pass.
- Trap 4 (asyncio): the client connection must open and close in the same task.

### 4. The test (~150 words)
- H2 committed before the run: MCP within ±5 points of direct, paired bootstrap.
- What differs: the schema text, pretty-printed results, the error prefix. So it tests MCP with its defaults.

### 5. Results (~250 words)
- 1.5B: level at 1.5%, a floor, so equivalence there means little.
- 3B: −6.0 (CI −13.0 to +0.5). Inconclusive.
- Cost: 2.3 ms per call against 0.03 ms, next to 3 to 16 seconds of generation. Negligible.

### 6. Where the gap opened (~200 words)
- Fail-closed: MCP 24.5%, direct 22.5%. Level.
- Repair: direct rescued 18 of 78 malformed runs, MCP 2 of 54.
- MCP's malformed replies were mostly a stray `>` before the JSON, which doesn't recover; direct's were often answers as strings, which do.
- Which MCP difference causes this can't be told from one run. Say so.

### 7. Advice (~100 words)
Treat MCP's defaults as part of your prompt. Set strict schemas, keep results compact, check what error text the model sees. Measure after switching.

### 8. Reproduce this
Colab link; `tests/test_week6.py` runs both routes with no model.

---

## Stretch experiment
**One difference at a time.** Make the MCP client return compact JSON and strip the error prefix, then re-run 3B on 530 problems (enough for 80% power on a 6-point drop) to see whether the gap closes.

## Self-check (closed-book)
1. Why did the MCP route need 45 more lines, and what do they buy?
2. What happens in `mcp` 2.x if a tool raises a plain `ValueError`?
3. Why is "MCP within ±5 points" an equivalence test, and why did 200 problems fail to show it at 3B?
4. What does the fail-closed comparison tell you about where the gap came from?
5. Name the three ways the MCP route's context differed from the direct route's.
