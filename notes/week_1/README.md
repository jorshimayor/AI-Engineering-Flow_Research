# Week 1: Transformer Mechanics

| | |
|---|---|
| **Topics** | Tokenisation, embeddings, self-attention intuition, autoregressive generation |
| **Paper** | *Attention Is All You Need* (Vaswani et al., 2017), [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| **Task** | Probe a pretrained model's tokeniser edge cases and next-token distributions across prompts |
| **Notebook** | [`jupyter/week1_transformer_probing.ipynb`](../../jupyter/week1_transformer_probing.ipynb) |
| **Model** | GPT-2 small: 124M params, 12 layers, 12 heads, d_model = 768, vocab 50,257, context 1024 |
| **Further reading** | [resources.md](resources.md) |

---

## 0. Setup

| Item | Choice | Why |
|---|---|---|
| Env manager | `uv` (project at repo root, `pyproject.toml` + `uv.lock`) | Reproducible, fast |
| Python | 3.11 | System Python is 3.14, which PyTorch doesn't support on Intel macOS |
| PyTorch | **2.2.2** (pinned) | Last release with x86_64 macOS wheels (this Mac has an Intel i7-8850H) |
| NumPy | `<2` | torch 2.2.2 was compiled against NumPy 1.x |
| Transformers | 4.49 | Loaded with `attn_implementation="eager"` so attention weights can be returned |
| Model | `gpt2` from Hugging Face | Small enough for CPU. It's the canonical decoder-only transformer and the direct ancestor of modern LLMs |

Run it:

```bash
uv sync
uv run jupyter lab   # open jupyter/week1_transformer_probing.ipynb
```

The whole notebook runs in about a minute on CPU. All randomness is seeded, so the numbers below are reproducible.

### How GPT-2 differs from the paper's transformer

Vaswani et al. describe an **encoder-decoder** model for translation. GPT-2 keeps only the **decoder stack** (without cross-attention) and changes a few things:

| Paper (2017) | GPT-2 (2019) |
|---|---|
| Encoder + decoder | Decoder only (causal self-attention) |
| Fixed sinusoidal positional encodings | **Learned** positional embeddings (`wpe`) |
| Post-LayerNorm (`x + LN(sublayer(x))`) | **Pre-LayerNorm** (`x + sublayer(LN(x))`), plus a final LN |
| ReLU in the FFN | GELU |
| WordPiece / BPE vocab ~37k | Byte-level BPE, 50,257 tokens |
| 6 layers, d_model = 512 | 12 layers, d_model = 768 (small) |

The core is unchanged: `Attention(Q,K,V) = softmax(QKᵀ/√dₖ)·V`, multi-head, residual stream, position-wise FFN.

---

## 1. Tokeniser edge cases

**What was done:** Encoded many strings with GPT-2's tokeniser and printed each token (using `repr` so leading spaces are visible). The cases covered spacing and case, numbers, whitespace in code, rare words, Unicode, emoji, special tokens and known "glitch" tokens.

**Concept:** Byte-level BPE. Text becomes UTF-8 bytes, and the most frequent adjacent pairs are merged again and again until the vocabulary reaches 50,257 entries. Because it starts from bytes, there's never an `<UNK>` token. How a string is split depends on how frequent it was in the tokeniser's training data.

### Results

| Case | Input → tokens | Lesson |
|---|---|---|
| Leading space | `hello` → `hello`; ` hello` → ` hello` (different IDs) | The space belongs to the *next* word. The two forms have separately learned embeddings |
| Case | `Hello` → 1 token; `HELLO` → `HE\|LL\|O` | ALL CAPS is rare in training data, so it gets split more |
| Years | `2026` → `20\|26` | |
| Long numbers | `1234567` → `123\|45\|67` | Digit chunks don't line up with place value, which hurts arithmetic |
| Decimals | `3.14159` → `3\|.\|14\|159` | |
| Indentation | 8 spaces + `return x` → 9 tokens | Each space is its own token, so code is expensive. Later tokenisers like `cl100k` added whitespace-run tokens |
| Long word | `antidisestablishmentarianism` → `ant\|idis\|establishment\|arian\|ism` | Sub-word pieces |
| Emoji | 🙂 → 2 tokens, each decodes to `�` | **Byte fallback**: a token can be part of a character |
| Family emoji | 👨‍👩‍👧 (18 bytes) → **10 tokens** | Zero-width joiners make it worse |
| Chinese | 你好 → 4 byte tokens | |
| Round-trip | `decode(encode(s)) == s` for every odd string tested | Byte-level BPE is lossless |

**Token tax** (same sentence translated):

| Language | Tokens | vs English |
|---|---|---|
| English | 17 | 1.0× |
| German | 28 | 1.6× |
| Chinese | 28 | 1.6× |
| French | 30 | 1.8× |
| Arabic | 50 | 2.9× |
| Russian | 57 | 3.4× |
| **Hindi** | **91** | **5.4×** |

Non-English users pay more per request and fit less text into the context window.

**Special-token injection:** the literal text `<|endoftext|>` inside user input is turned into the real EOS token (ID 50256). If an app passes untrusted text through the tokeniser without disabling special tokens, a user can inject control tokens.

**Glitch tokens:** `' SolidGoldMagikarp'` (43453), `' TheNitromeFan'`, `' davidjl'` and `' RandomRedditorWithNo'` are each a **single token**. They were frequent in the data the tokeniser was trained on (Reddit usernames and counting threads) but nearly absent from the data the model was trained on.

---

## 2. Embeddings

**What was done:** Looked at the token embedding matrix `wte` (50257 × 768) and the positional embedding matrix `wpe` (1024 × 768). Found each word's nearest neighbours by cosine similarity. Tested whether glitch tokens sit near the centre of the embedding space. Plotted the structure of the positional embeddings.

### Results

- **Nearest neighbours** are a mix of surface variants and meaning:
  - ` king` → ` kings`, ` King`, ` queen`, ` prince`, ` monarch`, ` emperor`
  - ` 7` → ` 6`, ` 8`, ` 5`, ` 9`: numbers cluster in order
  - ` Paris` → `Paris`, ` France`, ` London`, ` Copenhagen`, ` Brussels`
- **Glitch-token hypothesis: mixed result.**
  - Expected: under-trained tokens stay near the embedding centroid (their embeddings barely moved from initialisation).
  - Observed: the famous glitch tokens are **not** unusual in GPT-2 (12th–50th percentile of distance from the centroid). The original finding was reported for GPT-J.
  - However, the tokens that *are* closest to the centroid are all junk: control bytes (`\x07`, `\x1c`), partial UTF-8 bytes, and other known glitch tokens (`' externalToEVA'`, `'quickShip'`, `' TheNitrome'`).
  - Conclusion: distance to the centroid is a useful detector of under-trained tokens, but it misses some. (See *Fishing for Magikarp* in resources.md for better methods.)
- **Positional embeddings** come out smooth and wave-like, with nearby positions being similar. GPT-2 *learned* something close to the sinusoidal scheme the paper built in by hand.

---

## 3. Next-token distributions

**What was done:** For each prompt, ran one forward pass, took `softmax(logits[-1])`, and printed the top tokens with their probabilities and the **entropy** in bits (0 = certain; 15.6 = uniform over the vocabulary). Also wrote a `logprob(prompt, continuation)` helper that scores multi-token answers with the chain rule, which is how multiple-choice LLM evals work.

### Entropy across prompt types

| Prompt | Entropy | Top-1 |
|---|---|---|
| `A B C D E F` | 0.23 bits | ` G` 98% |
| `Actions speak louder than` | 0.87 | ` words` 93% |
| `1, 2, 3, 4, 5,` | 0.98 | ` 6` 91% |
| `Q: How are you today?\nA:` | 5.49 | ` I` 34% |
| `for i in range(` | 7.26 | `0` 16% |
| `The capital of France is` | 8.65 | ` the` 8.5% (` Paris` only 3.2%) |
| `17 + 25 =` | 8.52 | ` 0` 4.6% |
| `Yesterday I went to the` | 11.15 | ` store` 2.3% |

Memorised patterns (the alphabet, idioms, counting) are nearly deterministic. Open-ended prompts spread probability across thousands of tokens.

### Knowledge is present, but hidden under generic continuations

- On free generation, ` Paris` is only **rank 5** (3.2%) after `The capital of France is`.
- Restricted to {Paris, London, Berlin, Lyon}, it wins with **87%**.
- This is why benchmarks score a fixed set of options instead of relying on free generation.

### Arithmetic fails

- `17 + 25 =` prefers ` 32` (44%) over the correct ` 42` (23%).
- `123 + 456 =` prefers ` 1000`.
- The number-tokenisation issues from Section 1 are part of the reason.

### Prompt sensitivity (all tokenisation effects)

| Prompt | P(answer) | Rank |
|---|---|---|
| `The capital of France is` → ` Paris` | 3.22% | 5 |
| `The capital of France is ` *(trailing space)* → `Paris` | **~0%** | **1472** |
| `the capital of france is` → ` Paris` | 3.57% | 2 |
| `THE CAPITAL OF FRANCE IS` → ` PARIS` | 0.05% | 306 |
| `Q: What is the capital of France?\nA:` → ` Paris` | 1.77% | 7 |
| `Paris is the capital of` → ` France` | 4.13% | 3 |

**The trailing-space trap:** the prompt now ends in a standalone `' '` token, which the model rarely saw in training. Its top predictions become `'\xa0'` (40%) and `'ét'` (34%), which is nonsense. **Practical rule: never end a prompt with a space.**

### Perplexity

Surprisal = −log₂ P(token | prefix). Perplexity = 2^(mean surprisal).

| Text | Perplexity |
|---|---|
| "The quick brown fox jumps over the lazy dog." | 162 |
| Same words, shuffled | **7,728** (~48× higher) |
| A technical sentence about gradient descent | 162 |

One forward pass gives predictions at *every* position (thanks to the causal mask). That's why training is efficient: a sequence of T tokens provides T training examples.

---

## 4. Self-attention

**What was done:**
1. **Rebuilt layer-0 attention by hand** from the raw weights: embeddings → `ln_1` → `c_attn` projection → split into Q/K/V → reshape into 12 heads × 64 dims → `QKᵀ/√64` → causal mask → softmax.
2. Checked the result against the model's own attention weights.
3. Searched all 144 heads for one where `it` attends to `animal` more than to `street`, in the sentence *"The animal didn't cross the street because it was too tired"*.
4. Measured how much attention goes to the first token.

### Results

- **Manual attention matches the model exactly** (`torch.allclose` → `True`). The weight on future tokens is exactly `0.0`, which confirms the causal mask.
- **Layer 4, head 3** gives `it → animal` a weight of **0.85** (vs 0.00 to `street`).
  - **Caveat:** its heatmap shows it sends *almost every* token to `animal`, so it's more of a "main subject noun" head than a dedicated coreference resolver.
  - Lesson: an attention pattern suggests a mechanism but doesn't prove one (see *Attention is not Explanation* in resources.md).
- **Attention sinks:** the share of attention on token 0 grows with depth:

  | Layer | 0 | 3 | 5 | 7 | 10 |
  |---|---|---|---|---|---|
  | Share on token 0 | 19% | 49% | 70% | 77% | **82%** |

  The uniform baseline is about 13%. Softmax forces each row to sum to 1, so heads with nothing useful to attend to park their weight on the first token. This is the phenomenon StreamingLLM builds on.

---

## 5. Autoregressive generation

**What was done:** Wrote a generation loop from scratch with a **KV cache**. After the first step, only the newest token is fed in, because keys and values for earlier tokens are reused. Implemented greedy, temperature, top-k and top-p (nucleus) sampling, and compared the output quality of each.

### Results

- **The manual greedy loop reproduces HF `model.generate()` exactly** (`True`). So generation really is just next-token prediction in a loop.
- **Greedy** decoding falls into a repetition loop within about 30 tokens: *"I've been to a lot of places where I've been to a lot of places where…"*
- **T = 0.3** is fluent but repetitive: *"You can get to know the people you love. You can get to know the people you don't know…"*
- **T = 0.7 + top-p 0.9** gave the most coherent, human-like text.
- **T = 1.0** is creative but drifts off topic.
- **T = 1.8** is word salad: *"opensburghExuckedzeePat Resource Story…"*
- Plots show that first-step entropy and distinct-3-gram diversity both rise steadily with temperature.

---

## Key takeaways

1. **The model never sees text, only token IDs.** Many "LLM quirks" are tokenisation artefacts: arithmetic, spelling, trailing spaces, non-English cost, glitch tokens.
2. **Next-token prediction is the whole interface.** Facts, generation, evals and perplexity all come from the same `softmax(logits)`.
3. **Attention is just `softmax(QKᵀ/√d + mask)·V`,** and it can be reproduced in about 10 lines. Reading meaning into the patterns requires care.
4. **The decoding strategy matters as much as the model.** The same weights produce loops, prose or noise depending on temperature and top-p.
5. **Small models are weak and brittle.** GPT-2 small ranks the correct fact 5th and gets 17 + 25 wrong. Scale, instruction tuning and RLHF close these gaps. That's coming in later weeks.

## Open questions / ideas to try next

- [ ] Re-run Sections 1 and 3 with a modern model (e.g. `Qwen2.5-0.5B` or `SmolLM2-360M`) and compare its tokeniser and fact recall.
- [ ] Compare GPT-2 vs `cl100k_base` vs `o200k_base` token counts on the same multilingual sentences with [`tiktoken`](https://github.com/openai/tiktoken).
- [ ] Look for **induction heads** (a head that predicts `B` after seeing `A B … A`) using repeated random token sequences.
- [ ] Implement sinusoidal positional encodings from the paper and compare them with GPT-2's learned `wpe`.
- [ ] Watch Karpathy's *Let's build the GPT Tokenizer* and implement BPE from scratch (`minbpe`).
