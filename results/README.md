# Results

Raw per-item results and charts from every experiment. The notebooks in [`../jupyter/`](../jupyter/README.md) write here and read their caches from here; the notes in [`../notes/`](../notes/README.md) interpret them.

## Folders

| Folder | Contents |
|---|---|
| [`week2/`](week2/) | `icl_runs.jsonl` (140 few-shot configurations), `passkey.json`, charts |
| [`week3/`](week3/) | `runs.jsonl`: Qwen2.5-0.5B, 4 modes × 30 problems with full trajectories |
| [`week3_gpu/`](week3_gpu/) | Qwen2.5 1.5B and 3B runs (120 each) and the comparison chart |
| [`week4/`](week4/) | `claim_audit.json` (15 audited claims), `power_table.json`, five charts |
| [`week4_dev_v1/`](week4_dev_v1/) | Difficulty calibration v1 (no level qualified; showed a generator flaw) |
| [`week4_dev_v2/`](week4_dev_v2/) | Difficulty calibration v2 (levels chosen: 1.5B level 2, 3B level 3) and `calibration.json` |

## Agent Run Records

`week3/`, `week3_gpu/` and `week4_dev_*` hold JSONL files, one episode per line:

| Field | Meaning |
|---|---|
| `id` | `"<mode>\|<problem id>"`, unique within a file |
| `model`, `mode` | Model name; `direct`, `cot`, `act` or `react` |
| `pid`, `template`, `split`, `level` | Problem id, problem type, dataset split, difficulty |
| `gold`, `answer`, `correct` | Right answer, agent's answer, exact match |
| `status`, `steps`, `tool_calls` | `ok`, `max_steps` or `invalid_action`; LLM calls; calculator calls |
| `tokens_in`, `tokens_out`, `seconds` | Cost of the episode |
| `trajectory`, `observations` | Full Thought/Action/Observation text; tool results |

Summarise any of them with:

```bash
uv run python src/run_react_bench.py --summary results/week3_gpu/*.jsonl
```

## Few-Shot Run Records

`week2/icl_runs.jsonl` has one configuration per line:

| Field | Meaning |
|---|---|
| `id`, `exp` | Configuration id; experiment (count, order, format, labels, balance) |
| `fmt`, `k`, `seed` | Prompt format, number of examples, demo-set seed |
| `acc`, `acc_cal` | Accuracy, and accuracy after contextual calibration |
| `pos_rate`, `label_mass`, `prefix_tokens` | Share predicted positive, probability on valid labels, prompt length |
| `logp`, `cf_logp` | Per-review label log-probs, so every metric can be recomputed |

## Licence

Data and charts are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0).
