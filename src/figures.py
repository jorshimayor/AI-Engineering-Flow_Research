"""Regenerate every summary figure in results/figures/ from the saved results.

    uv run python src/figures.py

Colours: one fixed role per method across all figures (validated for colour-vision
deficiency); every bar carries its value as a label.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from stats import discordant, paired_bootstrap_ci, power_mcnemar, wilson_ci  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
OUT = RES / "figures"

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#9b9a95"
MODE_COLOUR = {"direct": GREY, "cot": ORANGE, "act": AQUA, "react": BLUE}
MODE_LABEL = {"direct": "Direct answer", "cot": "Reasoning only (CoT)", "act": "Tool only (Act)", "react": "ReAct"}
MODES = ["direct", "cot", "act", "react"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "legend.frameon": False, "lines.linewidth": 2,
})


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / name)


def jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open()]


# ------------------------------------------------------------------ week 1
def week1_token_tax() -> None:
    # Token counts for the same sentence under GPT-2's tokeniser (Week 1 notebook, section 1)
    counts = {"English": 17, "German": 28, "Chinese": 28, "French": 30, "Arabic": 50, "Russian": 57, "Hindi": 91}
    langs = sorted(counts, key=counts.get)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(langs, [counts[l] for l in langs], color=BLUE, height=0.6, edgecolor=SURFACE, linewidth=2)
    for i, l in enumerate(langs):
        ax.text(counts[l] + 1, i, f"{counts[l]} tokens  ({counts[l] / counts['English']:.1f}×)", va="center", fontsize=9, color=INK2)
    ax.set_xlim(0, 115); ax.grid(axis="y", visible=False)
    ax.set_xlabel("GPT-2 tokens for the same sentence")
    ax.set_title("Week 1: the same sentence costs up to 5.4× more tokens outside English")
    save(fig, "week1_token_tax.png")


# ------------------------------------------------------------------ week 2
def week2_what_moves_accuracy() -> None:
    R = jsonl(RES / "week2" / "icl_runs.jsonl")
    sel = lambda exp, **kw: [r for r in R if r["exp"] == exp and all(r.get(k) == v for k, v in kw.items())]
    mean = lambda rs: float(np.mean([r["acc"] for r in rs]))
    spread = lambda v: (max(v) - min(v)) * 100
    templates = ["review", "input/output", "minimal", "question", "review+instr"]
    labels = ["review", "great/terrible", "good/bad", "0/1", "foo/bar"]
    eff = {
        "Prompt template (0-shot)": spread([sel("format", fmt=n, k=0)[0]["acc"] for n in templates]),
        "Prompt template (4-shot)": spread([mean(sel("format", fmt=n, k=4)) for n in templates]),
        "Label words": spread([mean(sel("format", fmt=n, k=4)) for n in labels]),
        "Number of examples (0 to 16)": spread([mean(sel("count", k=k)) for k in (0, 1, 2, 4, 8, 16)]),
        "Label balance": spread([mean(sel("balance", n_pos=n)) for n in range(5)]),
        "Example order": max(spread([r["acc"] for r in sel("order", set=s)]) for s in (100, 101)),
        "Which examples": spread([r["acc"] for r in sel("count", k=4)]),
        "Label correctness": spread([mean(sel("labels", variant=v)) for v in ("gold", "random", "flipped")]),
    }
    names = sorted(eff, key=eff.get)
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.barh(names, [eff[n] for n in names], color=BLUE, height=0.6, edgecolor=SURFACE, linewidth=2)
    for i, n in enumerate(names):
        ax.text(eff[n] + 0.6, i, f"{eff[n]:.0f} pts", va="center", fontsize=9, color=INK2)
    ax.set_xlim(0, 48); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Accuracy range from changing this factor alone (percentage points)")
    ax.set_title("Week 2: prompt format moves few-shot accuracy far more than the examples")
    save(fig, "week2_what_moves_accuracy.png")


# ------------------------------------------------------------------ week 3
def week3_runs() -> dict[str, list[dict]]:
    return {size: jsonl(RES / "week3" / f"Qwen2.5-{size}-Instruct.jsonl") for size in ("0.5B", "1.5B", "3B")}


def week3_accuracy_by_size() -> None:
    data = week3_runs()
    sizes = list(data)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    w = 0.2
    for i, mode in enumerate(MODES):
        for j, size in enumerate(sizes):
            rs = [r for r in data[size] if r["mode"] == mode]
            k, n = sum(r["correct"] for r in rs), len(rs)
            lo, hi = wilson_ci(k, n)
            x = j + (i - 1.5) * w
            ax.bar(x, k / n * 100, w, color=MODE_COLOUR[mode], edgecolor=SURFACE, linewidth=2,
                   label=MODE_LABEL[mode] if j == 0 else None)
            ax.plot([x, x], [lo * 100, hi * 100], color=INK2, linewidth=1)
            ax.text(x, k / n * 100 + 2.5, f"{k / n:.0%}", ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(range(len(sizes))); ax.set_xticklabels([f"Qwen2.5-{s}" for s in sizes])
    ax.set_ylim(0, 112); ax.set_ylabel("Accuracy on 30 word problems (%)"); ax.grid(axis="x", visible=False)
    ax.legend(ncol=4, loc="upper left", fontsize=9)
    ax.set_title("Week 3: with a calculator, accuracy rises from 23% (0.5B) to 97% to 100% (1.5B, 3B)")
    ax.text(0, -0.16, "Thin lines: 95% Wilson confidence intervals. 0.5B on a laptop CPU; 1.5B and 3B on a Colab T4.",
            transform=ax.transAxes, fontsize=8, color=INK2)
    save(fig, "week3_accuracy_by_size.png")


def week3_cost_vs_accuracy() -> None:
    data = week3_runs()
    markers = {"0.5B": "o", "1.5B": "s", "3B": "^"}
    fig, ax = plt.subplots(figsize=(8, 4.4))
    for size, R in data.items():
        for mode in MODES:
            rs = [r for r in R if r["mode"] == mode]
            tok = np.mean([r["tokens_in"] + r["tokens_out"] for r in rs]); acc = np.mean([r["correct"] for r in rs]) * 100
            ax.scatter(tok, acc, s=70, marker=markers[size], color=MODE_COLOUR[mode], edgecolor=SURFACE, linewidth=1.5, zorder=3)
            if mode in ("act", "react") and size != "0.5B":
                ax.annotate(f"{MODE_LABEL[mode].split(' (')[0]} {size}", (tok, acc), textcoords="offset points",
                            xytext=(8, -3), fontsize=8, color=INK2)
    for mode in MODES:
        ax.scatter([], [], color=MODE_COLOUR[mode], label=MODE_LABEL[mode], s=50)
    for size, mk in markers.items():
        ax.scatter([], [], color=INK2, marker=mk, label=f"Qwen2.5-{size}", s=50)
    ax.set_xlabel("Tokens per problem (cost)"); ax.set_ylabel("Accuracy (%)"); ax.set_ylim(-5, 108)
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax.set_title("Week 3: tool-only matches or beats ReAct, at lower cost")
    save(fig, "week3_cost_vs_accuracy.png")


# ------------------------------------------------------------------ week 4
def week4_claim_audit() -> None:
    claims = [c for c in json.loads((RES / "week4" / "claim_audit.json").read_text()) if c["lo"] == c["lo"]][::-1]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for i, c in enumerate(claims):
        held = c["verdict"] == "holds"
        col = BLUE if held else GREY
        ax.plot([c["lo"] * 100, c["hi"] * 100], [i, i], color=col, linewidth=3, solid_capstyle="round")
        ax.plot(c["effect"] * 100, i, "o", color=INK, markersize=4)
    ax.axvline(0, color=INK2, linewidth=1)
    ax.axvspan(-5, 5, color=GRID, alpha=0.6, zorder=0)
    short = {"W2-1": "16 examples beat 0", "W2-2": "1 example is worse than 0", "W2-3": "Random labels barely matter",
             "W2-4": "Flipped labels hurt", "W2-5": "0.5B ignores flipped labels", "W2-6": "great/terrible beats positive/negative",
             "W2-7": "'Question' template below chance", "W2-8": "Calibration rescues 'question' template",
             "W2-9": "Calibration hurts foo/bar labels", "W2-10": "Instruction doesn't help a base model",
             "W2-11": "Recency bias from the last example", "W3-1": "Calculator helps (Act vs CoT)",
             "W3-2": "Calculator helps (ReAct vs CoT)", "W3-3": "ReAct and Act equal at 0.5B"}
    ax.set_yticks(range(len(claims))); ax.set_yticklabels([f"{c['id']}  {short.get(c['id'], c['claim'])}" for c in claims], fontsize=8.5)
    ax.grid(axis="y", visible=False)
    ax.plot([], [], color=BLUE, linewidth=3, label="Holds (8)"); ax.plot([], [], color=GREY, linewidth=3, label="Not established (7)")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_xlabel("Effect in percentage points, 95% CI (grey band: ±5-point equivalence margin)")
    ax.set_title("Week 4: 8 of 15 earlier claims survive proper statistics")
    save(fig, "week4_claim_audit.png")


def week4_difficulty_calibration() -> None:
    cal = json.loads((RES / "week4" / "calibration_v2" / "calibration.json").read_text())
    levels = [int(l) for l in cal["selection_table"]]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.axhspan(40, 85, color=GRID, alpha=0.6, zorder=0)
    ax.text(3.35, 41.5, "target band: 40% to 85%", fontsize=8, color=INK2)
    for model, col in [("Qwen/Qwen2.5-1.5B-Instruct", GREY), ("Qwen/Qwen2.5-3B-Instruct", INK)]:
        ys = [cal["selection_table"][str(l)]["act"][model] * 100 for l in levels]
        ax.plot(levels, ys, "-o", color=col, markersize=7, label=model.split("/")[1].replace("-Instruct", ""))
        chosen = cal["chosen_levels"][model]
        y = cal["selection_table"][str(chosen)]["act"][model] * 100
        ax.plot(chosen, y, "o", markersize=15, markerfacecolor="none", markeredgecolor=col, markeredgewidth=2)
        ax.annotate(f"chosen: level {chosen} ({y:.1f}%)", (chosen, y), textcoords="offset points",
                    xytext=(12, 10) if col == INK else (-118, -22), fontsize=8.5, color=INK2)
    ax.set_xticks(levels); ax.set_xlim(0.7, 4.6); ax.set_ylim(-5, 108)
    ax.set_xlabel("Difficulty level"); ax.set_ylabel("Tool-only (Act) accuracy on 40 dev problems (%)")
    ax.legend(loc="lower left", fontsize=9)
    ax.set_title("Week 4: harder problems remove the ceiling; each model gets an in-band level")
    save(fig, "week4_difficulty_calibration.png")


def week4_react_minus_act() -> None:
    """ReAct minus Act-only (paired) across everything run so far. Exploratory only."""
    rows = []
    for size, R in week3_runs().items():
        rows.append((f"{size}  Week 3 problems", R))
    cal = json.loads((RES / "week4" / "calibration_v2" / "calibration.json").read_text())
    for model, level in cal["chosen_levels"].items():
        name = model.split("/")[1]
        R = jsonl(RES / "week4" / "calibration_v2" / f"{name}-L{level}.jsonl")
        rows.append((f"{name.split('-')[1]}  harder dev, level {level}", R))
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, (label, R) in enumerate(rows[::-1]):
        by = {m: {r["pid"]: r["correct"] for r in R if r["mode"] == m} for m in ("act", "react")}
        pids = sorted(by["act"])
        a = [by["react"][p] for p in pids]; b = [by["act"][p] for p in pids]
        eff, lo, hi = paired_bootstrap_ci(a, b)
        col = BLUE
        ax.plot([lo * 100, hi * 100], [i, i], color=col, linewidth=3, solid_capstyle="round")
        ax.plot(eff * 100, i, "o", color=INK, markersize=5)
        ax.text(hi * 100 + 2, i, f"{eff * 100:+.1f} pts (n = {len(pids)})", va="center", fontsize=8.5, color=INK2)
    ax.axvline(0, color=INK2, linewidth=1)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontsize=9); ax.grid(axis="y", visible=False)
    ax.set_xlim(-62, 62); ax.set_xlabel("ReAct minus tool-only accuracy (percentage points, 95% CI)")
    ax.set_title("ReAct vs tool-only so far: harmful at 1.5B, ahead at 3B on harder problems")
    ax.text(0, -0.24, "Exploratory: small samples, and the dev problems also chose the levels. The pre-registered test (480 problems per model) decides.",
            transform=ax.transAxes, fontsize=8, color=INK2)
    save(fig, "week4_react_minus_act.png")


def week4_power() -> None:
    Ns = list(range(40, 801, 40))
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for disc, col in [(0.32, "#86b6ef"), (0.40, "#2a78d6"), (0.48, "#104281")]:
        ax.plot(Ns, [power_mcnemar(n, 0.10, disc, alpha=0.025, sims=6000) * 100 for n in Ns], color=col,
                label=f"{disc:.0%} of problems disagree")
    ax.axhline(80, color=INK2, linewidth=1, linestyle="--"); ax.text(812, 82, "80% target", fontsize=8, color=INK2)
    ax.axvline(480, color=INK2, linewidth=1); ax.text(488, 30, "N = 480\n(protocol)", fontsize=8, color=INK2)
    ax.axvline(30, color=GREY, linewidth=1); ax.text(38, 92, "Week 3:\nN = 30", fontsize=8, color=INK2)
    ax.set_ylim(0, 102); ax.set_xlim(0, 900)
    ax.set_xlabel("Problems per model"); ax.set_ylabel("Power to detect +10 points (%)")
    ax.legend(loc="lower right", fontsize=9)
    ax.set_title("Week 4: 480 problems give at least 81% power; Week 3's 30 gave about 10%")
    save(fig, "week4_power.png")


# ------------------------------------------------------------------ week 5
W5_ORDER = ["zero_shot_direct", "few_shot_direct", "zero_shot_cot", "few_shot_cot", "few_shot_cot_json"]
W5_LABEL = {"zero_shot_direct": "Zero-shot\ndirect", "few_shot_direct": "Few-shot\ndirect", "zero_shot_cot": "Zero-shot\nCoT",
            "few_shot_cot": "Few-shot\nCoT", "few_shot_cot_json": "Few-shot\nCoT + JSON"}
W5_MODELS = [("Qwen2.5-0.5B-Instruct", GREY), ("Qwen2.5-1.5B-Instruct", INK)]


def week5_runs() -> dict[str, list[dict]]:
    return {m: jsonl(RES / "week5" / f"{m}.jsonl") for m, _ in W5_MODELS if (RES / "week5" / f"{m}.jsonl").exists()}


def week5_strategy_accuracy() -> None:
    data = week5_runs()
    if not data:
        print("skip week5_strategy_accuracy: no results/week5 yet"); return
    fig, ax = plt.subplots(figsize=(9, 4.4))
    w = 0.36
    for j, (m, col) in enumerate(W5_MODELS):
        if m not in data:
            continue
        for i, s in enumerate(W5_ORDER):
            rs = [r for r in data[m] if r["strategy"] == s]
            if not rs:
                continue
            k, n = sum(r["correct"] for r in rs), len(rs)
            lo, hi = wilson_ci(k, n)
            lenient = sum(r["correct_lenient"] for r in rs) / n * 100
            x = i + (j - 0.5) * w
            ax.bar(x, k / n * 100, w, color=col, edgecolor=SURFACE, linewidth=2, label=m.replace("-Instruct", "") if i == 0 else None)
            ax.plot([x, x], [lo * 100, hi * 100], color=INK2, linewidth=1)
            if lenient - k / n * 100 >= 1:
                ax.plot(x, lenient, marker="_", markersize=14, color=BLUE, markeredgewidth=2.5,
                        label="Lenient (any number format)" if i == W5_ORDER.index("few_shot_cot_json") and j == 1 else None)
            ax.text(x, max(k / n * 100, lenient) + 3, f"{k / n:.0%}", ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(range(len(W5_ORDER))); ax.set_xticklabels([W5_LABEL[s] for s in W5_ORDER])
    ax.set_ylim(0, 105); ax.set_ylabel("GSM8K accuracy, strict format (%)"); ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Week 5: chain-of-thought prompting on 400 GSM8K problems")
    ax.text(0, -0.2, "Thin lines: 95% Wilson intervals. Blue ticks: accuracy if any final number counts, showing format failures.",
            transform=ax.transAxes, fontsize=8, color=INK2)
    save(fig, "week5_strategy_accuracy.png")


def week5_cost_vs_accuracy() -> None:
    data = week5_runs()
    if not data:
        print("skip week5_cost_vs_accuracy: no results/week5 yet"); return
    markers = {"Qwen2.5-0.5B-Instruct": "o", "Qwen2.5-1.5B-Instruct": "s"}
    fig, ax = plt.subplots(figsize=(8, 4.4))
    for m, col in W5_MODELS:
        for s in W5_ORDER:
            rs = [r for r in data.get(m, []) if r["strategy"] == s]
            if not rs:
                continue
            tok = np.mean([r["tokens_in"] + r["tokens_out"] for r in rs]); acc = np.mean([r["correct"] for r in rs]) * 100
            ax.scatter(tok, acc, s=70, marker=markers[m], color=col, edgecolor=SURFACE, linewidth=1.5, zorder=3)
            ax.annotate(W5_LABEL[s].replace("\n", " "), (tok, acc), textcoords="offset points", xytext=(7, -3), fontsize=7.5, color=INK2)
    for m, col in W5_MODELS:
        ax.scatter([], [], marker=markers[m], color=col, label=m.replace("-Instruct", ""), s=50)
    ax.set_xlabel("Tokens per problem, prompt + answer (cost)"); ax.set_ylabel("Accuracy, strict (%)")
    ax.set_ylim(-5, 105); ax.legend(fontsize=9, loc="upper left")
    ax.set_title("Week 5: what each prompting strategy costs")
    save(fig, "week5_cost_vs_accuracy.png")


FIGURES = [week1_token_tax, week2_what_moves_accuracy, week3_accuracy_by_size, week3_cost_vs_accuracy,
           week4_claim_audit, week4_difficulty_calibration, week4_react_minus_act, week4_power,
           week5_strategy_accuracy, week5_cost_vs_accuracy]

if __name__ == "__main__":
    for f in FIGURES:
        f()
