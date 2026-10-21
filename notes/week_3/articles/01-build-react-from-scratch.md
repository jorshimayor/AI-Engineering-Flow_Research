# Article 1: Build a ReAct agent from scratch (outline)

## Title options
- **Build a ReAct Agent From Scratch: ~100 Lines, No Framework**
- What Is an AI Agent, Really? A Loop, a Parser and a Stop Sequence
- I Built an Agent Without LangChain. Here's Every Line That Matters.

**Target reader:** a developer who has used ChatGPT or agent frameworks and wants to know what's underneath.
**Promise:** by the end you can write an agent loop yourself and understand what frameworks and native tool-calling APIs do for you.
**Length:** ~1,600 words, code-heavy · **Hero:** your loop diagram

*This article doubles as your write-up of the Week 3 paper (ReAct).*

---

## Outline

### 1. Hook (~100 words)
"Agent frameworks have thousands of lines. The idea at their core fits on a napkin." Show the 8-line pseudocode loop.

### 2. The idea: ReAct in plain words (~300 words)
- Three ways to solve a problem: think only (CoT), act only, or interleave both (ReAct). Use the comparison table from the notes.
- The paper's insight: thoughts help the model *plan and track progress*, actions help it *get facts right*.
- One example trajectory (warehouse problem: Thought → `calculate[7511 * 77 - 1331]` → 577016).

### 3. Building it, four pieces (~800 words, with code)
1. **The tool:** the safe calculator.
   - Why `eval()` is dangerous; show the `rm -rf` example being rejected.
   - Return errors as text so the model can recover.
2. **The prompt:** instructions, tool description, 2 exemplar trajectories (show one). Exemplars define the format.
3. **The LLM call with a stop sequence:** `stop=["Observation:"]`. **The most important line in the article.**
   - Show the no-stop demo: the model writes its own `Observation: 45840`. It's a guess, not a result.
4. **The loop:** parse `Action: name[arg]` with a regex, dispatch, append the observation, repeat, cap the steps.

### 4. Run it (~150 words)
The CLI command and a full printed trajectory. Mention it runs on a laptop CPU with a 0.5B model.

### 5. What frameworks and APIs add (~250 words)
- **Native tool calling** (Anthropic/OpenAI): JSON tool schemas replace text parsing, and the provider handles the stop.
- Frameworks: retries, memory, multiple tools, tracing, parallel calls. **MCP:** a standard way to plug tools in.
- Point: after this article, those are conveniences rather than magic.

### 6. Takeaways and reproduce (~100 words)

---

## Stretch experiment (new work)
**Add a second tool.** Add `lookup[name]` returning facts from a small dict (e.g. city populations), then ask questions that need *both*: "How many people live in Lagos and Accra combined, times 2?" Show a trajectory that uses both tools. That makes it a multi-tool agent, which is closer to the paper's HotpotQA setup.

## Self-check (closed-book)
1. Write the ReAct loop from memory in pseudocode.
2. What exactly happens if you remove the stop sequence?
3. Why must the tool's errors be *returned to the model* instead of raised?
4. Why is `eval()` on model output dangerous even if *you* wrote the prompt? (Think about prompt injection via documents.)
5. What do the exemplars teach the model?
6. How does native JSON tool calling map onto Thought / Action / Observation?
