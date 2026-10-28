**Title:** Week 1: joshua - transformer probing notebook and findings

## Task

Week 1, Transformer mechanics (anchor: *Attention Is All You Need*, Vaswani et al., 2017).
Lab: probe a pretrained model's tokeniser edge cases and next-token distributions across prompts.

## What I did

Probed GPT-2 small (124M) on CPU, then rebuilt its first attention layer and its generation loop by hand to check them against the model.

| Probe | Result |
|---|---|
| Leading space | `' hello'` and `'hello'` are different tokens with separate embeddings |
| Numbers | `1234567` splits as `123\|45\|67`; `2026` as `20\|26` |
| Token cost | Same sentence: English 17 tokens, Hindi 91 (5.4×) |
| Special tokens | The literal text `<\|endoftext\|>` becomes the real end-of-text token (an injection risk) |
| Trailing space | P(" Paris" \| "The capital of France is") = 3.2%, rank 5. With a trailing space: ~0%, rank 1,472 |
| Knowledge vs generation | "Paris" ranks 5th in free generation but wins 87% among four candidate cities |
| Attention | Layer 0 rebuilt by hand matches the model exactly; weight on future tokens is exactly 0 |
| Generation | A hand-written KV-cached loop reproduces `model.generate` exactly |

## Files (`Week1/joshua/`)

| File | Contents |
|---|---|
| `week1_transformer_probing.ipynb` | All probes, with outputs and an observation after each |
| `README.md` | Results table, findings and caveats |
| `figures/week1_token_tax.png` | Token cost by language |

## Limitations

- One model (GPT-2 small); larger models tokenise and attend differently.
- One prompt per probe, no statistics: these are demonstrations, not population estimates.

## Submission rules

- [x] Branch `week1_joshua`, created from the latest `research` (`934c27b`)
- [x] Files added only inside `Week1/joshua/`
- [x] No shared files or other fellows' folders edited
- [x] Notebook runs top to bottom on CPU in about 1 minute

Full notes and reading list: https://github.com/jorshimayor/AI-Engineering-Flow_Research/tree/main/notes/week_1
