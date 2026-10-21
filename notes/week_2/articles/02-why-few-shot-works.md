# Article 2: Why few-shot prompting works (outline)

## Title options
- **Learning Without Training: Why Few-Shot Prompting Works, and Where It Breaks**
- Your Examples Teach Format, Not Facts
- I Gave My Model Wrong Answers in Every Example. It Barely Noticed.

**Target reader:** has used few-shot prompts, has heard of GPT-3, and wants the "why".
**Promise:** understand what in-context learning is (and isn't), why model size matters, and the hidden biases you need to correct for.
**Length:** ~1,700 words · **Figures:** `e1_count.png` (label-mass panel), `sampling_icl.png`, `passkey.png`

*This article doubles as your write-up of the Week 2 paper (GPT-3).*

---

## Outline

### 1. Hook (~100 words)
"I flipped every label in my examples. Every 'positive' became 'negative'. Accuracy only fell from 90% to 84%. The model wasn't learning from my examples. So what *was* it doing?"

### 2. What GPT-3 claimed (~300 words)
- Zero-, one- and few-shot defined. "Learning" with no gradient updates.
- Meta-learning framing: pre-training is the outer loop, the prompt is the inner loop.
- The scale result (Fig. 1.2): the few-shot advantage grows with model size.
- The paper's own open question: does ICL learn *new* tasks, or *recognise* ones it already knows? The rest of the article answers that with your data.

### 3. Evidence 1: demos teach format (~250 words)
- **Label mass** goes from 0.62 (0-shot) to 0.99 (16-shot). Zero-shot, 38% of the probability goes to tokens that aren't answers at all.
- **Random labels** cost only about 1 point (Min et al. replicated).

### 4. Evidence 2: small models follow their prior (~250 words)
- **Flipped labels:** 84%. The model ignores the mapping you showed it.
- Contrast with Wei et al.: only the largest models follow flipped labels. That's the scale story from GPT-3, seen from the other side.
- `foo/bar` 56% → 72%: *some* new-mapping learning happens, but it's unstable.

### 5. How it works mechanically (~200 words)
- The Bayesian view: demos help the model infer *which* task this is (Xie et al.).
- Induction heads: copying patterns from context (link to your Week 1 attention article).

### 6. The biases (~250 words)
- Recency, majority label, and most-recently-mentioned label word (the 97%-"negative" collapse).
- **Contextual calibration:** how it works, where it rescued results (49% → 87%), and where it *failed* (`foo/bar` 72% → 44%).

### 7. Budget: context and sampling (~250 words)
- Each demo costs about 29 tokens. GPT-3's 2,048 window means about 71 demos.
- GPT-2's hard 1,024 limit (`IndexError` at token 1,025) vs RoPE models.
- **Passkey: 100% up to 8k tokens, an honest null result.** It's a copy task, which is exactly what induction heads are good at. Harder tests (RULER) show "effective ≪ claimed" context.
- **Sampling:** zero-shot at T=1 is a coin flip (47.5%); with 4 shots, 77%. Few-shot makes outputs robust to temperature. For classification, use T≈0.

### 8. Takeaways (~100 words)

### 9. Reproduce this

---

## Stretch experiment (new work)
**Find the scale threshold yourself.** Run E4 (flipped labels) on Qwen2.5 **0.5B → 1.5B → 3B** (3B is slow on CPU, so use ~60 test reviews). Plot "accuracy on flipped labels" against model size. If accuracy falls with size, the larger model is *following* your flipped demos, which is Wei et al.'s finding on hardware you own.

## Self-check (closed-book)
1. Define in-context learning in one sentence without the word "learning".
2. What does "label mass" measure, and why does it rise with k?
3. If random labels barely hurt, what *are* the demos contributing?
4. Why would a bigger model be *more* affected by flipped labels?
5. How does contextual calibration work? Why does it fail for `foo/bar`?
6. Why is passkey retrieval a weak test of long-context ability?
7. Why does few-shot prompting make sampling at T=1 safer?
