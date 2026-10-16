"""Run the Week 3 benchmark (direct / cot / act / react) for one model. GPU if available.

Results are appended to a JSONL file one problem at a time, so an interrupted
run (a Colab disconnect, say) resumes where it stopped when re-launched.

    python src/run_react_bench.py --model Qwen/Qwen2.5-1.5B-Instruct
    python src/run_react_bench.py --model Qwen/Qwen2.5-3B-Instruct --modes act react
    python src/run_react_bench.py --summary results/week3_gpu/*.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from react_agent import LocalLLM, run_agent  # noqa: E402
from react_tasks import correct, make_problems  # noqa: E402
from stats import discordant, mcnemar_exact, paired_bootstrap_ci, wilson_ci  # noqa: E402

MODES = ["direct", "cot", "act", "react"]


def run(model: str, modes: list[str], n_per: int, seed: int, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"] for l in out.open()} if out.exists() else set()
    problems = make_problems(n_per, seed)
    todo = [(m, p) for m in modes for p in problems if f"{m}|{p['id']}" not in done]
    if not todo:
        print(f"{out}: nothing to do ({len(done)} runs already saved)")
        return out
    llm = LocalLLM(model)
    print(f"{model} on {llm.device} ({llm.model.dtype}); {len(todo)} runs to go, {len(done)} already saved -> {out}")
    t0 = time.time()
    for i, (mode, p) in enumerate(todo, 1):
        ti, to = llm.tokens_in, llm.tokens_out
        r = run_agent(llm, p["question"], mode=mode)
        row = dict(id=f"{mode}|{p['id']}", model=model, mode=mode, pid=p["id"], template=p["template"],
                   gold=p["gold"], answer=r.answer, correct=correct(r.answer, p["gold"]), status=r.status,
                   steps=r.steps, tool_calls=r.tool_calls, tokens_in=llm.tokens_in - ti,
                   tokens_out=llm.tokens_out - to, seconds=r.seconds, trajectory=r.trajectory,
                   observations=r.observations)
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
        print(f"{'mode':7} {'acc':>6} {'95% CI':>15} {'tokens/problem':>15} {'sec/problem':>12}")
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
            print(f"{m:7} {k/n:6.1%} {lo:6.1%} to {hi:5.1%} {tok:15.0f} {sec:12.1f}")
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
    ap.add_argument("--n-per", type=int, default=5, help="problems per template (6 templates; 5 = Week 3's 30 problems)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=Path, help="default: results/week3_gpu/<model>.jsonl")
    ap.add_argument("--summary", nargs="*", type=Path, help="only print summaries of these result files")
    args = ap.parse_args()
    if args.summary is not None:
        summary(args.summary)
        return
    out = args.out or Path("results/week3_gpu") / f"{args.model.split('/')[-1]}.jsonl"
    summary([run(args.model, args.modes, args.n_per, args.seed, out)])


if __name__ == "__main__":
    main()
