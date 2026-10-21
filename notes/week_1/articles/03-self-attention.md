# Article 3: Self-attention (outline)

## Title options
- **I Rebuilt GPT-2's Attention by Hand. Here's What the Heads Actually Do.**
- Attention Is All You Need, Verified in 10 Lines of PyTorch
- softmax(QKᵀ/√d)·V: The Transformer's Core Equation, Explained With a Real Model

**Target reader:** has read Articles 1–2 or knows the basics, and wants to understand the equation and the 2017 paper.
**Promise:** you'll understand every symbol in the attention equation, see it reproduced exactly on a real model, and learn why attention heatmaps can mislead.
**Length:** ~1,800 words · **Figures:** `attention-it-animal.png`, a diagram of Q/K/V (draw it yourself), optionally `positional-embeddings.png`

*This article also serves as your write-up of the Week 1 paper.*

---

## Outline

### 1. Hook (~100 words)
In 2017, eight researchers replaced recurrence with one equation. I took GPT-2's weights, computed that equation by hand, and got the model's attention **exactly**. Then I found a head that seems to resolve "it", and learned why I shouldn't trust it.

### 2. The problem attention solves (~200 words)
- RNNs process tokens one at a time: they can't be parallelised, and long-range information has to survive many steps.
- Attention lets every token look directly at every earlier token in one step.
- Mention Bahdanau et al. (2014) as the origin, and the 2017 paper as "attention *only*".

### 3. The equation, piece by piece (~500 words)
Use the running sentence: *"The animal didn't cross the street because it was too tired."*
- **Q, K, V as a lookup:** Query = "what am I looking for", Key = "what do I contain", Value = "what I pass on". All three are linear projections of the same token vectors.
- **QKᵀ:** a similarity score between every pair of tokens.
- **Why divide by √dₖ:** without it, dot products grow with dimension, softmax saturates and gradients vanish. (dₖ = 64 in GPT-2.)
- **Softmax:** each row becomes weights that sum to 1.
- **Causal mask:** −∞ above the diagonal, so a token can't see the future. This is what makes GPT a *generator*.
- **Multi-head:** 12 heads × 64 dimensions, each free to learn a different pattern, then concatenated.
- Diagram: draw the T×T score matrix with its masked upper triangle.

### 4. Verifying it on a real model (~250 words)
- Show the ~10 lines of your manual layer-0 code (embeddings → LN → Q/K/V → scores → mask → softmax).
- Results: `torch.allclose(...) == True`, and the weight on future tokens is exactly 0.0.
- Point: the architecture isn't magic. It's matrix multiplication you can check yourself.

### 5. Paper vs GPT-2: what changed (~250 words)
The comparison table from `../README.md`:
- encoder-decoder → decoder-only
- sinusoidal → learned positions (and `positional-embeddings.png` shows GPT-2 learned smooth, wave-like patterns anyway)
- post-LN → pre-LN
- ReLU → GELU

One or two sentences on why each change was made.

### 6. What do the heads actually do? (~300 words)
- The search: across all 144 heads, which has `it → animal` > `it → street`? **Layer 4, head 3**: 0.85 vs 0.00.
- **The twist:** the heatmap shows that head sends *almost every* token to "animal". It isn't doing coreference; it attends to the main noun.
- Lesson: attention weights show *where* information flows, not *why*. Cite *Attention is not Explanation*.

### 7. Attention sinks (~200 words)
- Attention on token 0 rises from 19% (layer 0) to 82% (layer 10), against 13% if it were uniform.
- Why: softmax *must* sum to 1, so a head with nothing to attend to parks its weight on the first token.
- Practical consequence: StreamingLLM keeps the first few tokens in the KV cache for this reason.

### 8. Takeaways (~100 words)

### 9. Reproduce this

---

## Stretch experiment (new work)
**Find an induction head.** Feed GPT-2 a random token sequence repeated twice (`[A B C D … | A B C D …]`). In the second half, an induction head attends from each token to the token *after* its earlier occurrence. Then:
- Plot the "induction score" for every layer and head.
- Show that the loss on the repeated half drops sharply.

This reproduces a key result from Anthropic's *In-context Learning and Induction Heads*, and it's a real mechanism, unlike the "it → animal" head. That gives the article a satisfying ending: here is a head we *can* explain.

Rough recipe:
```python
seq = torch.randint(1000, 20000, (1, 50))
ids = torch.cat([seq, seq], dim=1)                 # repeat
att = torch.stack(model(ids, output_attentions=True).attentions)[:, 0]  # (L, H, 100, 100)
# induction score: mean attention from position i (second half) to position i-50+1
score = torch.stack([att[:, :, i, i - 49] for i in range(50, 100)]).mean(0)
```

## Self-check (answer closed-book before writing)
1. Write the attention equation from memory and give the shape of every matrix for T = 12, d_model = 768, 12 heads.
2. Why √dₖ and not dₖ? What happens to the softmax without scaling?
3. Why does the causal mask use −∞ rather than 0?
4. Without positional embeddings, what would self-attention be unable to tell apart? ("dog bites man" vs "man bites dog")
5. What are the advantages of multiple 64-dimensional heads over one 768-dimensional head?
6. Why can't an encoder-only model like BERT generate text the way GPT does?
7. Explain attention sinks in two sentences.
8. Why is a high attention weight not proof that a head "resolves coreference"?
