"""Pre-registered analysis for the Week 4 eval protocol (v1.3), section 8.

Written and committed before any test problem was run. Given the test-run
JSONL files, it applies the protocol's rules mechanically:

  1. validity gates            (section 6.1)
  2. paired ReAct vs Act test  (exact McNemar + paired bootstrap CI)
  3. Holm across the two model sizes, then the outcome table (section 6.2)
  4. leave-one-template-out robustness (section 8, step 4)
  5. cost ratio with a paired bootstrap CI
  6. cost-accuracy points for the Pareto plot
  7. exploratory breakdowns (failure categories, per-template accuracy)
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

from react_agent import calculate
from run_react_bench import failure_type, is_format_failure
from stats import discordant, holm, mcnemar_exact, paired_bootstrap_ci, wilson_ci


def load_config(path: str | Path = "notes/week_4/eval_protocol_config.json") -> dict:
    return json.loads(Path(path).read_text())


def load_runs(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open()] if path.exists() else []


def by_mode(rows: list[dict]) -> dict[str, dict[int, dict]]:
    out: dict[str, dict[int, dict]] = {}
    for r in rows:
        out.setdefault(r["mode"], {})[r["pid"]] = r
    return out


def calculator_unit_tests() -> bool:
    """Gate 2: the tool is correct, including the injection and overflow cases."""
    cases = {"(1284 * 36) - 2050": "44174", "1,284 * 36": "46224", "$52 * 7": "364", "2340 / 45": "52", "10 / 4": "2.5"}
    ok = all(calculate(e) == v for e, v in cases.items())
    for bad in ["__import__('os').system('ls')", "2 ** 100000", "1 / 0", "twelve times 7"]:
        ok &= calculate(bad).startswith("Error")
    return ok


def paired(rows_by_mode: dict, pids: list[int]) -> dict:
    a = np.array([rows_by_mode["react"][p]["correct"] for p in pids])
    b = np.array([rows_by_mode["act"][p]["correct"] for p in pids])
    eff, lo, hi = paired_bootstrap_ci(a, b, n_boot=10_000)
    react_only, act_only = discordant(a, b)
    return dict(n=len(pids), react=float(a.mean()), act=float(b.mean()), effect=eff, ci=(lo, hi),
                p=mcnemar_exact(react_only, act_only), react_only=react_only, act_only=act_only,
                discordance=(react_only + act_only) / len(pids))


def cost_ratio(rows_by_mode: dict, pids: list[int], n_boot: int = 10_000, seed: int = 0) -> dict:
    tr = np.array([rows_by_mode["react"][p]["tokens_in"] + rows_by_mode["react"][p]["tokens_out"] for p in pids], float)
    ta = np.array([rows_by_mode["act"][p]["tokens_in"] + rows_by_mode["act"][p]["tokens_out"] for p in pids], float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(pids), size=(n_boot, len(pids)))
    boots = tr[idx].mean(1) / ta[idx].mean(1)
    return dict(ratio=float(tr.mean() / ta.mean()), ci=tuple(np.quantile(boots, [0.025, 0.975])))


def outcome(effect: float, ci: tuple, p_holm: float, cost: float, cfg: dict) -> str:
    """Section 6.2, applied in order."""
    a = cfg["analysis"]
    lo, hi = ci
    significant = p_holm < a["alpha"]
    if significant and lo > 0 and effect * 100 >= a["min_effect_points"]:
        return "supported" if cost <= a["max_cost_ratio"] else "supported, but too costly"
    if significant and hi < 0:
        return "harmful"
    if hi * 100 < a["refute_upper_bound_points"]:
        return "refuted"
    return "inconclusive"


def gates(rows_by_mode: dict, cfg: dict) -> dict:
    g = cfg["analysis"]["gates"]
    direct = np.mean([r["correct"] for r in rows_by_mode.get("direct", {}).values()]) if rows_by_mode.get("direct") else float("nan")
    ff = {m: float(np.mean([is_format_failure(r) for r in rows_by_mode[m].values()])) for m in ("act", "react")}
    return {"1_task_needs_tool": bool(direct <= g["direct_max"]), "2_calculator_correct": calculator_unit_tests(),
            "3_format_fail_le_20pct": all(v <= g["format_fail_max"] for v in ff.values()),
            "direct_accuracy": float(direct), "format_fail": ff}


def analyse(results_dir: str | Path, cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    results_dir = Path(results_dir)
    report = {"protocol_version": cfg["protocol_version"], "models": {}}
    models = list(cfg["models"])
    data = {}
    for m in models:
        level = cfg["models"][m]["level"]
        rows = load_runs(results_dir / f"{m.split('/')[-1]}-L{level}.jsonl")
        bm = by_mode(rows)
        pids = sorted(set(bm.get("act", {})) & set(bm.get("react", {})))
        data[m] = (bm, pids, level)
        complete = len(pids) == cfg["n_problems_per_model"] and len(bm.get("direct", {})) == cfg["n_problems_per_model"]
        report["models"][m] = {"level": level, "complete": complete, "n_paired": len(pids)}
    if not all(v["complete"] for v in report["models"].values()):
        report["status"] = "incomplete run: no confirmatory analysis"
        return report

    # primary test + Holm
    prim = {m: paired(data[m][0], data[m][1]) for m in models}
    for m, ph in zip(models, holm([prim[m]["p"] for m in models])):
        prim[m]["p_holm"] = ph

    for m in models:
        bm, pids, level = data[m]
        g = gates(bm, cfg)
        valid = g["1_task_needs_tool"] and g["2_calculator_correct"] and g["3_format_fail_le_20pct"]
        cost = cost_ratio(bm, pids)
        res = prim[m]
        verdict = outcome(res["effect"], res["ci"], res["p_holm"], cost["ratio"], cfg) if valid else "invalid run (gate failed)"

        # leave-one-template-out: same Holm multiplier as the full analysis (the other model's p held fixed)
        loto = {}
        other = [prim[o]["p"] for o in models if o != m]
        for t in sorted({bm["act"][p]["template"] for p in pids}):
            keep = [p for p in pids if bm["act"][p]["template"] != t]
            r2 = paired(bm, keep)
            p_h = holm([r2["p"]] + other)[0]
            c2 = cost_ratio(bm, keep)
            loto[t] = dict(effect=r2["effect"], ci=r2["ci"], p_holm=p_h, outcome=outcome(r2["effect"], r2["ci"], p_h, c2["ratio"], cfg))
        template_dependent = valid and any(v["outcome"] != verdict for v in loto.values())

        acc = {mode: dict(acc=float(np.mean([r["correct"] for r in bm[mode].values()])),
                          ci=wilson_ci(sum(r["correct"] for r in bm[mode].values()), len(bm[mode])),
                          tokens=float(np.mean([r["tokens_in"] + r["tokens_out"] for r in bm[mode].values()])),
                          seconds=float(np.mean([r["seconds"] for r in bm[mode].values()])))
               for mode in ("direct", "act", "react") if mode in bm}
        per_template = {t: {mode: float(np.mean([r["correct"] for r in bm[mode].values() if r["template"] == t]))
                            for mode in ("act", "react")} for t in sorted({r["template"] for r in bm["act"].values()})}
        failures = {mode: dict(Counter(failure_type(r) for r in bm[mode].values() if not r["correct"])) for mode in ("act", "react")}
        report["models"][m].update(gates=g, valid=valid, primary=res, cost=cost, outcome=verdict,
                                   template_dependent=template_dependent, leave_one_template_out=loto,
                                   accuracy=acc, per_template=per_template, failures=failures)

    outs = [report["models"][m]["outcome"] for m in models]
    if all(o == "supported" for o in outs):
        overall = "C supported"
    elif any(o == "supported" for o in outs):
        overall = "C partially supported"
    elif all(o in ("refuted", "harmful") for o in outs):
        overall = "C refuted"
    elif all(o in ("supported", "supported, but too costly") for o in outs):
        overall = "C not supported: ReAct is more accurate but exceeds the 1.5x cost bound"
    else:
        overall = "C not settled"
    report["overall"] = overall
    report["status"] = "complete"
    return report


def print_report(rep: dict) -> None:
    print(f"Protocol {rep['protocol_version']}: {rep['status']}")
    for m, r in rep["models"].items():
        print(f"\n=== {m} (level {r['level']}), {r['n_paired']} paired problems")
        if "primary" not in r:
            continue
        g = r["gates"]
        print(f"gates: task needs tool {g['1_task_needs_tool']} (direct {g['direct_accuracy']:.1%}), calculator {g['2_calculator_correct']}, "
              f"format failures ok {g['3_format_fail_le_20pct']} (Act {g['format_fail']['act']:.1%}, ReAct {g['format_fail']['react']:.1%})")
        for mode, a in r["accuracy"].items():
            print(f"  {mode:6} {a['acc']:6.1%} (95% CI {a['ci'][0]:.1%} to {a['ci'][1]:.1%})  {a['tokens']:7.0f} tokens  {a['seconds']:5.1f} s")
        p = r["primary"]
        print(f"ReAct - Act: {p['effect']*100:+.1f} pts (95% CI {p['ci'][0]*100:+.1f} to {p['ci'][1]*100:+.1f}); "
              f"ReAct-only {p['react_only']}, Act-only {p['act_only']}; p = {p['p']:.4f}, Holm p = {p['p_holm']:.4f}; discordance {p['discordance']:.0%}")
        print(f"cost ratio ReAct/Act: {r['cost']['ratio']:.2f} (95% CI {r['cost']['ci'][0]:.2f} to {r['cost']['ci'][1]:.2f})")
        print(f"OUTCOME: {r['outcome'].upper()}" + ("  (template-dependent)" if r["template_dependent"] else ""))
    if "overall" in rep:
        print(f"\nOVERALL: {rep['overall']}")
