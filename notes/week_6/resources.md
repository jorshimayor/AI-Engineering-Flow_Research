# Week 6 Resources: Structured Outputs, Tool Calling and MCP

Links checked 6 November 2026. ⭐ = start here.

## Papers

| Paper | Why |
|---|---|
| ⭐ [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761), Schick et al. 2023 | The anchor paper: a model learns when a tool call helps |
| [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334), Patil et al. 2023 | Fine-tuning for correct API calls; the Week 17 reading. Also the [function-calling leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) |
| [ToolLLM](https://arxiv.org/abs/2307.16789), Qin et al. 2023 | 16,000+ real APIs; multi-step tool use |
| [Tool Learning with Foundation Models](https://arxiv.org/abs/2304.08354), Qin et al. 2023 | Survey of tool use |
| [τ-bench](https://arxiv.org/abs/2406.12045), Yao et al. 2024 | Agents with tools and a simulated user; pass^k reliability |
| ⭐ [Let Me Speak Freely?](https://arxiv.org/abs/2408.02442), Tam et al. 2024 | Format restrictions can cost reasoning (Week 5's JSON tax) |
| [Efficient Guided Generation for LLMs](https://arxiv.org/abs/2307.09702), Willard and Louf 2023 | The method behind Outlines: valid JSON by construction |
| [Guiding LLMs the Right Way](https://arxiv.org/abs/2403.06988), Beurer-Kellner et al. 2024 | Fast constrained decoding without hurting accuracy |
| [MCP: Landscape, Security Threats, and Future Research Directions](https://arxiv.org/abs/2503.23278), Hou et al. 2025 | MCP's life cycle and attack surface |
| [ReAct](https://arxiv.org/abs/2210.03629), Yao et al. 2022 | Week 3: the loop this pipeline grows from |

## MCP

| Resource | Notes |
|---|---|
| ⭐ [MCP specification](https://modelcontextprotocol.io/specification/latest) | The anchor document; also the [2025-06-18 version](https://modelcontextprotocol.io/specification/2025-06-18) |
| [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture) | Hosts, clients, servers; tools, resources, prompts |
| [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server) | Official tutorial |
| [Python SDK](https://github.com/modelcontextprotocol/python-sdk) · [v2 migration guide](https://py.sdk.modelcontextprotocol.io/v2/migration/) | The SDK used here (`mcp` 2.3.0); v2 renamed `FastMCP` to `MCPServer` |
| [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol), Anthropic | Why MCP exists |
| ⭐ [Building Agents with MCP, full workshop](https://www.youtube.com/watch?v=kQmXtrmQ5Zg), Mahesh Murag (AI Engineer) | Video walkthrough from the MCP team |
| [MCP course](https://huggingface.co/learn/mcp-course/unit0/introduction), Hugging Face | Free course |
| [MCP: Build Rich-Context AI Apps](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/), DeepLearning.AI | Short course with Anthropic |
| [MCP has prompt injection security problems](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/), Simon Willison | Why tool descriptions and outputs are untrusted (Week 23) |
| [Tool poisoning attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), Invariant Labs | Hidden instructions in tool descriptions |

## Tool calling and structured output

| Resource | Notes |
|---|---|
| ⭐ [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents), Anthropic | Tool names, descriptions and error messages as prompts |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), Anthropic | When to use tools and workflows; the Week 17 reading |
| [Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview), Anthropic docs · [Function calling](https://platform.openai.com/docs/guides/function-calling), OpenAI docs | How hosted APIs do it |
| [Function calling with Qwen](https://qwen.readthedocs.io/en/latest/framework/function_call.html) | The `<tool_call>` format used here |
| [Tool use in chat templates](https://huggingface.co/docs/transformers/chat_extras), Hugging Face | Passing `tools=` to `apply_chat_template` |
| [Understanding JSON Schema](https://json-schema.org/understanding-json-schema) · [`jsonschema` for Python](https://python-jsonschema.readthedocs.io/en/stable/) | The validation used here |
| [Pydantic](https://docs.pydantic.dev/latest/) | How MCP generates schemas from type hints |
| [Functions, Tools and Agents with LangChain](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/), DeepLearning.AI | Short course |

## Tools

| Tool | For |
|---|---|
| [Instructor](https://github.com/567-labs/instructor) | Validated structured outputs with automatic retries (the repair loop, packaged) |
| [Outlines](https://github.com/dottxt-ai/outlines) | Constrained decoding: malformed JSON becomes impossible |
