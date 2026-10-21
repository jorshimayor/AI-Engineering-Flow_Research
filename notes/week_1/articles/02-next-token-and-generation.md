# Article 2: Next-token distributions and generation (outline)

## Title options
- **What an LLM Actually Outputs (It's Not Text)**
- GPT-2 Knows Paris Is the Capital of France. It Just Won't Say It.
- From Probabilities to Paragraphs: Next-Token Prediction, Temperature and Why Greedy Decoding Loops

**Target reader:** someone who has read Article 1, or who knows LLMs "predict the next word" but not what that means concretely.
**Promise:** you'll understand the model's one real output, and how facts, generated text, evals and temperature all come from it.
**Length:** ~1,700 words · **Figures:** `next-token-entropy.png`, `surprisal-perplexity.png`, `temperature-entropy-diversity.png`

---

## Outline

### 1. Hook (~100 words)
GPT-2 ranks " Paris" **5th** after "The capital of France is", behind " the", " now" and " a". Yet among {Paris, London, Berlin, Lyon} it picks Paris with **87%** confidence. Does it know the answer or not?

### 2. The model's one output (~250 words)
- Every forward pass → a vector of 50,257 logits → softmax → a probability distribution over the next token.
- That's the *whole* interface. Chat, code and reasoning are all this distribution applied in a loop.
- Introduce **entropy** in plain words: 0 bits = certain; 15.6 bits = picking at random from the vocabulary.

### 3. How certain is the model? (~300 words)
Use `next-token-entropy.png` plus a table:

| Prompt | Entropy | Top-1 |
|---|---|---|
| `A B C D E F` | 0.23 bits | ` G` 98% |
| `Actions speak louder than` | 0.87 | ` words` 93% |
| `The capital of France is` | 8.65 | ` the` 8.5% |
| `Yesterday I went to the` | 11.15 | ` store` 2.3% |

Point to make: memorised patterns are near-certain. "Factual" prompts are *not*, because many fluent continuations exist ("…is a city of…").

### 4. Knowledge vs generation: how evals score models (~300 words)
- The chain rule: P("Las Vegas") = P(" Las") × P(" Vegas" | " Las").
- Explain your `logprob()` helper and why benchmarks like MMLU score fixed answer options instead of free text.
- Arithmetic evidence: `17 + 25 =` prefers 32 over 42; `123 + 456 =` prefers 1000. Tie this back to number tokenisation (Article 1).

### 5. Prompt sensitivity (~200 words)
Table of perturbations: trailing space (rank 1,472), lowercase (rank 2), ALL CAPS (rank 306), Q/A format (rank 7).
- What the model predicts after a trailing space: `'\xa0'` 40%, `'ét'` 34%, which is nonsense.
- Lesson: small surface changes → different tokens → a different distribution.

### 6. Perplexity: grading a whole text (~150 words)
- One forward pass gives a prediction at every position; that's also why training is efficient.
- Natural sentence: perplexity 162. Same words shuffled: **7,728**. Use `surprisal-perplexity.png`.

### 7. Generation is a loop (~300 words)
- Show the ~15-line loop in pseudocode: predict → choose → append → repeat.
- **KV cache:** after step 1, only the new token is fed in, because earlier keys and values are reused.
- Proof: your hand-written loop matched HF `generate()` exactly.

### 8. Decoding strategies (~250 words)
Show real samples, trimmed:
- **Greedy:** "…I've been to a lot of places where I've been to a lot of places where…"
- **T = 0.3:** "You can get to know the people you love. You can get to know…"
- **T = 0.7 + top-p 0.9:** the most coherent sample.
- **T = 1.8:** "opensburghExuckedzeePat Resource Story…"

Then use `temperature-entropy-diversity.png`. Explain temperature as dividing the logits before softmax, and top-p as sampling only from the smallest set of tokens covering p of the probability.

### 9. Takeaways (~100 words)
- Don't judge a model's knowledge by one greedy sample.
- Temperature is a dial between repetitive and random.
- Evals measure probabilities, not what the model "says".

### 10. Reproduce this

---

## Stretch experiment (new work)
**Does a bigger or newer model fix the knowledge-vs-generation gap?** Re-run the France, arithmetic and trailing-space prompts on `gpt2-medium` (355M) and `gpt2-large` (774M). Both run on CPU; large is slow but fine. Add a table showing how P(Paris) and its rank change with model size. That's a mini scaling-law result of your own.

Optional: try `HuggingFaceTB/SmolLM2-360M`, a modern model at a similar size to GPT-2 medium. If it does much better, that shows training data and recipe matter as well as size.

## Self-check (answer closed-book before writing)
1. What exactly does `model(ids).logits[0, -1]` represent? What is its shape?
2. Why does one forward pass over T tokens give T training examples?
3. Compute the entropy of a distribution with P = [0.5, 0.25, 0.25]. (Answer: 1.5 bits.)
4. Why does temperature → 0 approach greedy decoding? What happens mathematically to the softmax?
5. What's the difference between top-k and top-p, and when would top-k be a bad choice?
6. Why does the KV cache give exactly the same output as recomputing everything? What would break without the causal mask?
7. Why does greedy decoding get stuck in loops?
