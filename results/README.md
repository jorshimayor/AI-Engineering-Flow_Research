# Results

**Summary figures:** [`figures/`](figures/), rebuilt by `uv run python src/figures.py`.

| Folder | Contents |
|---|---|
| [`week1/`](week1/) | Week 1 charts |
| [`week2/`](week2/) | `icl_runs.jsonl` (140 few-shot configurations), `passkey.json`, charts |
| [`week3/`](week3/) | One file per model (0.5B, 1.5B, 3B): 4 modes × 30 problems each, with trajectories |
| [`week4/`](week4/) | `claim_audit.json`, `power_table.json`, charts; `calibration_v1/` and `calibration_v2/` (difficulty calibration); `test/` (pre-registered test, once run) |
| [`week5/`](week5/) | One file per model: 5 strategies × 400 GSM8K problems, with every output |

## Agent run format (JSONL, one episode per line)

`id` (`mode|problem`), `model`, `mode` (direct, cot, act, react), `pid`, `template`, `split`, `level`, `gold`, `answer`, `correct`, `status`, `steps`, `tool_calls`, `tokens_in`, `tokens_out`, `seconds`, `trajectory`, `observations`.

## Few-shot run format (`week2/icl_runs.jsonl`)

`id`, `exp`, `fmt`, `k`, `seed`, `acc`, `acc_cal`, `pos_rate`, `label_mass`, `prefix_tokens`, and per-review `logp` and `cf_logp` for recomputing any metric.

## Prompt run format (`week5/*.jsonl`)

`id` (`strategy|problem`), `model`, `strategy`, `library_version`, `pid`, `gold`, `output`, `pred_strict`, `pred_lenient`, `format_ok`, `correct`, `correct_lenient`, `tokens_in`, `tokens_out`, `seconds`.
