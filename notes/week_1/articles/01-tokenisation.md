# Article 1: Tokenisation (outline)

## Title options
- **Your LLM Can't See Words: 7 Tokeniser Quirks I Found Probing GPT-2**
- One Trailing Space Broke My Prompt: A Field Guide to Tokenisation
- Why Hindi Costs 5× More Than English: What Tokenisers Do to Your Text

**Target reader:** a developer who uses LLM APIs but has never looked at tokens.
**Promise:** after reading, you'll know why LLMs struggle with maths, spelling and non-English text, and why a trailing space can break a prompt.
**Length:** ~1,500 words · **Figures:** `token-tax.png`, plus 2–3 token-split tables or screenshots.

---

## Outline

### 1. Hook (~100 words)
Open with the trailing-space result, which sets up Article 2 as well:
- `"The capital of France is"` → P(" Paris") = 3.2%, rank 5
- `"The capital of France is "` → P("Paris") ≈ 0%, rank **1,472**

Then say: "The model didn't get dumber. It never saw the text you think it saw."

### 2. What a tokeniser is (~250 words)
- Models see **integer IDs**, not characters or words. GPT-2 has 50,257 of them.
- **BPE in one paragraph:** start from bytes, repeatedly merge the most frequent adjacent pair, stop at the target vocabulary size.
- **Why "byte-level":** there's never an unknown token, and any string round-trips losslessly (you verified this).
- Diagram idea: `"tokenization"` → bytes → merges → `token | ization`.

### 3. The quirks, one short section each (~700 words)

For each quirk give: the example, the numbers, why it happens, and why it matters.

1. **Spaces belong to the next word.** `hello` ≠ ` hello`. These have separate embeddings. Cash in the hook here.
2. **Capitals split.** `Hello` = 1 token, `HELLO` = 3 (`HE|LL|O`).
3. **Numbers are chopped arbitrarily.** `1234567` → `123|45|67`; `2026` → `20|26`. This leads into "why LLMs are bad at arithmetic" (Article 2 has the evidence).
4. **Whitespace costs a lot.** 8-space indent = 8 tokens. Say what that means for the cost of code.
5. **Emoji and CJK split into partial bytes.** 🙂 = 2 tokens that each decode to `�`; the family emoji = 10 tokens.
6. **Token tax.** Hindi 5.4×, Russian 3.4×, Arabic 2.9× the English count. Use `token-tax.png`. Cover the implications: price, context length, fairness.
7. **Special tokens and glitch tokens.**
   - `<|endoftext|>` typed as plain text becomes the real EOS token, which is an injection risk.
   - `' SolidGoldMagikarp'` is a single token and a leftover from Reddit data.

### 4. What I got wrong (~150 words)
- Your hypothesis: glitch tokens sit near the embedding centroid.
- The result: not for the famous ones in GPT-2 (12th–50th percentile). But the closest-to-centroid tokens *are* junk (`externalToEVA`, `quickShip`, control bytes).
- Lesson: a published finding on one model (GPT-J) doesn't automatically transfer to another.

### 5. Embeddings: where tokens become meaning (~150 words)
- Each ID maps to a 768-dimensional vector.
- Nearest neighbours: ` king` → ` queen`, ` prince`, ` monarch`; ` 7` → ` 6`, ` 8`, ` 5`.
- The catch: ` Paris` and `Paris` had to be learned **separately**. Tokenisation choices create extra work for the model.

### 6. Practical takeaways (~100 words)
Bullet list for practitioners:
- Never end a prompt with a space.
- Count tokens, not characters, when budgeting.
- Expect weaker performance on digits and non-English text.
- Sanitise special tokens in user input.

### 7. Reproduce this
Link the notebook; name the model and library versions.

---

## Stretch experiment (new work, not in the notebook)
**Compare tokenisers across generations.** Use `tiktoken` to encode your 7-language sentence and a Python snippet with:
- GPT-2 (`gpt2`)
- GPT-4 (`cl100k_base`)
- GPT-4o (`o200k_base`)

Then add a table: *"Did newer tokenisers fix the token tax?"* This turns the article from "GPT-2 quirks" into "how tokenisers evolved", which is more current and more original.

```bash
uv add tiktoken
```

## Self-check (answer closed-book before writing)
1. Why can't a byte-level BPE tokeniser produce an unknown token?
2. Why is `" Paris"` a single token, but a prompt ending in a space breaks the prediction?
3. Why would a tokeniser trained on English text make Hindi expensive? What exactly gets merged, and what doesn't?
4. Why does decoding one token of an emoji give `�`, even though decoding all of them works?
5. How could inconsistent number splitting hurt arithmetic? Give an example.
6. What's the difference between the tokeniser's training data and the model's training data, and how does that gap create glitch tokens?
