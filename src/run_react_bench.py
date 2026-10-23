"""Run the Week 3 benchmark (direct / cot / act / react) for one model. GPU if available.

Results are appended to a JSONL file one problem at a time, so an interrupted
run (a Colab disconnect, say) resumes where it stopped when re-launched.

    python src/run_react_bench.py --model Qwen/Qwen2.5-1.5B-Instruct
    python src/run_react_bench.py --model Qwen/Qwen2.5-3B-Instruct --modes act react
    python src/run_react_bench.py --summary results/week3/*.jsonl

Week 4 protocol task set (harder problems, src/react_tasks_v2.py):
    python src/run_react_bench.py --task dev --level 2 --modes act --max-steps 8
    python src/run_react_bench.py --task test --level 2 --max-steps 8     # only after the protocol is frozen
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from react_agent import LocalLLM, run_agent, to_number  # noqa: E402
from react_tasks import correct, make_problems  # noqa: E402
import react_tasks_v2  # noqa: E402
from stats import discordant, mcnemar_exact, paired_bootstrap_ci, wilson_ci  # noqa: E402

MODES = ["direct", "cot", "act", "react"]


def load_problems(task: str, n_per: int | None, seed: int | None, level: int) -> list[dict]:
    if task == "week3":
        return make_problems(n_per or 5, 0 if seed is None else seed)
    return react_tasks_v2.make_problems(task, level, n_per, seed)


def failure_type(row: dict) -> str:
    """Week 4 protocol failure categories (section 5)."""
    if row["correct"]:
        return "correct"
    traj = row.get("trajectory", "")
    if "Unknown action" in traj:
        return "invented tool"
    if any(seg.count("Action:") > 1 for seg in traj.split("Observation:")[:-1]):
        return "multiple actions per step"
    if row["answer"] is None:
        return {"max_steps": "step limit", "invalid_action": "invalid action"}.get(row["status"], "no answer")
    obs = [o for o in row.get("observations", []) if not o.startswith("Error")]
    if obs and to_number(obs[-1]) is not None and to_number(row["answer"]) != to_number(obs[-1]):
        return "ignored or overrode observation"
    return "misread problem / wrong expression"


def is_format_failure(row: dict) -> bool:
    """Gate 3: the agent didn't follow the action protocol (invented tool, invalid action, or never finished)."""
    if row["mode"] not in ("act", "react"):
        return False
    traj = row.get("trajectory", "")
    return row["answer"] is None or "Unknown action" in traj or "Invalid action" in traj


def run(model: str, modes: list[str], problems: list[dict], out: Path, max_steps: int = 6, llm=None) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"] for l in out.open()} if out.exists() else set()
    todo = [(m, p) for m in modes for p in problems if f"{m}|{p['id']}" not in done]
    if not todo:
        print(f"{out}: nothing to do ({len(done)} runs already saved)")
        return out
    llm = llm or LocalLLM(model)
    print(f"{model} on {llm.device} ({llm.model.dtype}); {len(todo)} runs to go, {len(done)} already saved -> {out}")
    t0 = time.time()
    for i, (mode, p) in enumerate(todo, 1):
        ti, to = llm.tokens_in, llm.tokens_out
        r = run_agent(llm, p["question"], mode=mode, max_steps=max_steps)
        row = dict(id=f"{mode}|{p['id']}", model=model, mode=mode, pid=p["id"], template=p["template"],
                   split=p.get("split", "week3"), level=p.get("level"), gold=p["gold"], answer=r.answer,
                   correct=correct(r.answer, p["gold"]), status=r.status, steps=r.steps, tool_calls=r.tool_calls,
                   tokens_in=llm.tokens_in - ti, tokens_out=llm.tokens_out - to, seconds=r.seconds,
                   trajectory=r.trajectory, observations=r.observations)
        with out.open("a") as f:
            f.write(json.dumps(row) + "\n")
        eta = (time.time() - t0) / i * (len(todo) - i)
        print(f"[{i}/{len(todo)}] {row['id']:10} {'✓' if row['correct'] else '✗'} ans={str(r.answer)[:12]:12} "
              f"gold={p['gold']:<9} {r.seconds:5.1f}s  ETA {eta/60:4.1f} min", flush=True)
    return out


def summary(paths: list[Path]) -> None:
    for path in paths:
        R = [json.loads(l) for l in path.open()]
        if not R:
            continue
        print(f"\n=== {R[0].get('model', path.stem)}  ({path})")
        print(f"{'mode':7} {'acc':>6} {'95% CI':>15} {'tokens/problem':>15} {'sec/problem':>12} {'format fail':>12}")
        by = {}
        for m in MODES:
            rs = sorted((r for r in R if r["mode"] == m), key=lambda r: r["pid"])
            if not rs:
                continue
            by[m] = rs
            k, n = sum(r["correct"] for r in rs), len(rs)
            lo, hi = wilson_ci(k, n)
            tok = sum(r["tokens_in"] + r["tokens_out"] for r in rs) / n
            sec = sum(r["seconds"] for r in rs) / n
            ff = sum(is_format_failure(r) for r in rs) / n
            print(f"{m:7} {k/n:6.1%} {lo:6.1%} to {hi:5.1%} {tok:15.0f} {sec:12.1f} {ff:12.1%}")
        if "act" in by and "react" in by and len(by["act"]) == len(by["react"]):
            a = [r["correct"] for r in by["react"]]; b = [r["correct"] for r in by["act"]]
            eff, lo, hi = paired_bootstrap_ci(a, b)
            only_react, only_act = discordant(a, b)
            print(f"ReAct - Act: {eff*100:+.1f} pts (95% CI {lo*100:+.1f} to {hi*100:+.1f}); "
                  f"ReAct-only wins {only_react}, Act-only wins {only_act}; exact McNemar p = {mcnemar_exact(only_react, only_act):.3f}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--modes", nargs="+", default=MODES, choices=MODES)
    ap.add_argument("--task", default="week3", choices=["week3", "dev", "test"],
                    help="week3 = original 30 problems; dev/test = Week 4 protocol task set")
    ap.add_argument("--level", type=int, default=2, choices=[1, 2, 3], help="difficulty for dev/test")
    ap.add_argument("--n-per", type=int, help="problems per template (week3: 5, dev: 20, test: 50)")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--max-steps", type=int, default=6, help="6 for week3, 8 for the protocol (v1.1)")
    ap.add_argument("--out", type=Path, help="default: results/week3/<model>.jsonl or results/week4/{calibration,test}/<model>-L<level>.jsonl")
    ap.add_argument("--summary", nargs="*", type=Path, help="only print summaries of these result files")
    args = ap.parse_args()
    if args.summary is not None:
        summary(args.summary)
        return
    name = args.model.split("/")[-1]
    if args.task == "week3":
        default_out = Path("results/week3") / f"{name}.jsonl"
    else:
        default_out = Path("results/week4") / ("calibration" if args.task == "dev" else "test") / f"{name}-L{args.level}.jsonl"
    problems = load_problems(args.task, args.n_per, args.seed, args.level)
    summary([run(args.model, args.modes, problems, args.out or default_out, args.max_steps)])


if __name__ == "__main__":
    main()
