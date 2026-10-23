# Pre-Registered Protocol (Week 4)

**Claim:** at 1.5B and 3B, ReAct solves at least 10 points more held-out multi-step calculator problems than Act-only, at no more than 1.5× the tokens.
**Status:** frozen at v1.3 (commit `5e8ad76`, 16 October 2026). Test run pending.

| File | Contents |
|---|---|
| [`week4_eval_protocol_v1.3.md`](week4_eval_protocol_v1.3.md) | Claim, design, sample size, pass/fail rules, threats, analysis plan, revision history |
| [`week4_frozen_config.json`](week4_frozen_config.json) | Machine-readable settings used by the test-run notebook |

Analysis code: [`../src/protocol_analysis.py`](../src/protocol_analysis.py) (written before the test). Run: [`../jupyter/week4_test_run_colab.ipynb`](../jupyter/week4_test_run_colab.ipynb).

**Verify it wasn't changed:**

```bash
shasum -a 256 protocol/week4_eval_protocol_v1.3.md
# 4fd25c86f19344dda5ecf77f6948390c359f7bb3073740aedd0901e9b7748cd4
```
