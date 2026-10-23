"""Week 3 task set: two-step arithmetic word problems with big numbers.

Moved out of the Week 3 notebook so the same 30 problems can be regenerated
anywhere (laptop, Colab, Kaggle). make_problems(5, seed=0) reproduces the
exact problems behind results/week3/Qwen2.5-0.5B-Instruct.jsonl.
"""
from __future__ import annotations

import random

from react_agent import to_number


def make_problems(n_per: int = 5, seed: int = 0) -> list[dict]:
    rng = random.Random(seed); P = []
    R = rng.randint
    for _ in range(n_per):
        a, b, c = R(1200, 9800), R(24, 96), R(1000, 9000)
        P.append(("warehouse", f"A warehouse stores {a:,} boxes with {b} items in each box. It ships out {c:,} items. How many items are left?", a*b - c))
        a, b, c = R(312, 987), R(14, 58), R(150, 900)
        P.append(("train", f"A train travels {a} km each day for {b} days, then another {c} km. How many km does it travel in total?", a*b + c))
        a, b, c = R(37, 240), R(2100, 6900), R(3, 12)
        P.append(("salary", f"A company pays each of its {a} employees ${b:,} per month. What is the total salary bill for {c} months?", a*b*c))
        b, q, c = R(24, 75), R(120, 480), R(13, 48)
        P.append(("crates", f"A farm picks {b*q:,} apples and packs them into crates of {b}. Each crate sells for ${c}. How much money does the farm make?", q*c))
        a, b, c, d = R(2000, 9000), R(12, 60), R(18, 64), R(300, 1500)
        P.append(("library", f"A library has {a:,} books. It buys {b} boxes of {c} books each and then donates {d} books. How many books does it have now?", a + b*c - d))
        b, q, c = R(12, 48), R(1500, 9000), R(200, 1400)
        P.append(("charity", f"A charity raises ${b*q:,} and splits it equally among {b} schools. Each school spends ${c:,} on books. How much money does each school have left?", q - c))
    return [dict(id=i, template=t, question=q, gold=g) for i, (t, q, g) in enumerate(P)]


def correct(answer: str | None, gold: float) -> bool:
    v = to_number(answer)
    return v is not None and abs(v - gold) < 1e-6 * max(1, abs(gold)) + 1e-9
