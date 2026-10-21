# Pre-Registered Protocol

The Week 4 evaluation plan, frozen in a public commit before any test problem was run, so the result can't be shaped after the fact.

**Question:** at 1.5B and 3B parameters, does ReAct prompting solve at least 10 points more held-out multi-step calculator problems than tool-only prompting, at no more than 1.5× the tokens?

**Status:** frozen at version 1.3 (commit `5e8ad76`, 16 October 2026). The test run hasn't happened yet.

## Files

| File | Contents |
|---|---|
| [`week4_eval_protocol_v1.3.md`](week4_eval_protocol_v1.3.md) | The full protocol: claim, hypotheses, design, sample size, pass and fail rules, threats to validity, analysis plan, budget and revision history |
| [`week4_frozen_config.json`](week4_frozen_config.json) | The same settings in machine-readable form, read by the test-run notebook |

The analysis code was also written before the test: [`../src/protocol_analysis.py`](../src/protocol_analysis.py). The run itself is [`../jupyter/week4_test_run_colab.ipynb`](../jupyter/week4_test_run_colab.ipynb).

## Checking the Protocol Wasn't Changed

The test-run notebook records the protocol's SHA-256 next to the results and refuses to resume if it changes. To check it yourself:

```bash
shasum -a 256 protocol/week4_eval_protocol_v1.3.md
# 4fd25c86f19344dda5ecf77f6948390c359f7bb3073740aedd0901e9b7748cd4
```

How the protocol reached version 1.3 (a GPU pilot, two calibration runs and a generator fix) is in its revision history and in [`../notes/week_4/README.md`](../notes/week_4/README.md).

## Licence

[CC BY 4.0](../LICENSE-CC-BY-4.0).
