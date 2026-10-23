# Results

**Summary figures:** [`figures/`](figures/), rebuilt by `uv run python src/figures.py`.

| Folder | Contents |
|---|---|
| [`week1/`](week1/) | Week 1 charts |
| [`week2/`](week2/) | `icl_runs.jsonl` (140 few-shot configurations), `passkey.json`, charts |
| [`week3/`](week3/) | `runs.jsonl`: 0.5B, 4 modes × 30 problems |
| [`week3_gpu/`](week3_gpu/) | 1.5B and 3B runs, 120 each |
| [`week4/`](week4/) | `claim_audit.json`, `power_table.json`, charts |
| [`week4_dev_v1/`](week4_dev_v1/), [`week4_dev_v2/`](week4_dev_v2/) | Difficulty calibration runs and `calibration.json` |

## Agent run format (JSONL, one episode per line)

`id` (`mode|problem`), `model`, `mode` (direct, cot, act, react), `pid`, `template`, `split`, `level`, `gold`, `answer`, `correct`, `status`, `steps`, `tool_calls`, `tokens_in`, `tokens_out`, `seconds`, `trajectory`, `observations`.

## Few-shot run format (`week2/icl_runs.jsonl`)

`id`, `exp`, `fmt`, `k`, `seed`, `acc`, `acc_cal`, `pos_rate`, `label_mass`, `prefix_tokens`, and per-review `logp` and `cf_logp` for recomputing any metric.
