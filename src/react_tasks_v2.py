"""Week 4 protocol task set (v1.1): harder multi-step calculator word problems.

The Week 3 problems were too easy once a model could read them (Act-only scored
97% at 1.5B and 100% at 3B), so these add the features that stress planning:

    level 1: 3 steps, 1 distractor quantity, facts in natural order
    level 2: 3 steps, 1 distractor, facts shuffled (text order != operation order)
    level 3: 4 steps (an extra operation or a unit conversion), 2 distractors, shuffled

Splits (protocol section 3.2):
    dev  : 2 templates  (bakery, parking)          free to inspect, used for calibration
    test : 8 templates  (never shown in prompts)   generated from a fixed seed, run once

Every problem carries a `solution` expression; check_problems() evaluates it with
the agent's own calculator and confirms it equals `gold`.
"""
from __future__ import annotations

import random
from typing import Callable

from react_agent import calculate

# Operation sequences of the two prompt exemplars (react_agent.EXEMPLARS):
#   pens:  125 * 48 then - 300      bolts: 2340 / 45 then * 7
EXEMPLAR_OPS = {("*", "-"), ("/", "*")}


def _fmt(n: int) -> str:
    return f"{n:,}"


def _assemble(rng: random.Random, level: int, facts: list[str], distractors: list[str], question: str) -> str:
    facts = list(facts)
    n_distract = 2 if level == 3 else 1
    extra = rng.sample(distractors, n_distract)
    if level == 1:
        body = facts + extra
    else:
        body = facts + extra
        rng.shuffle(body)
    return " ".join(body + [question])


# --------------------------------------------------------------------- templates
# Each returns (facts, distractors, question, gold, solution, ops).

def bakery(rng, level):
    a, b, d = rng.randint(12, 48), rng.randint(18, 36), rng.randint(5, 14)
    made = a * b * d
    s = rng.randint(made // 4, made // 2)
    dis = [f"The bakery employs {rng.randint(6, 25)} bakers.", f"The bakery opened {rng.randint(3, 40)} years ago.",
           f"Each roll sells for ${rng.randint(2, 6)}."]
    if level < 3:
        facts = [f"A bakery bakes {a} trays of rolls every day.", f"Each tray holds {b} rolls.",
                 f"Over {d} days the bakery sells {_fmt(s)} rolls in total."]
        return facts, dis, "How many rolls are left unsold after those days?", made - s, f"{a} * {b} * {d} - {s}", ("*", "*", "-")
    h = rng.randint(3, 8); per_h = a  # trays per hour, h hours a day
    made = per_h * h * b * d; s = rng.randint(made // 4, made // 2)
    facts = [f"A bakery bakes {per_h} trays of rolls per hour, for {h} hours every day.", f"Each tray holds {b} rolls.",
             f"Over {d} days the bakery sells {_fmt(s)} rolls in total."]
    return facts, dis, "How many rolls are left unsold after those days?", made - s, f"{per_h} * {h} * {b} * {d} - {s}", ("*", "*", "*", "-")


def parking(rng, level):
    f, s = rng.randint(4, 12), rng.randint(120, 480)
    total = f * s
    o = rng.randint(total // 20, total // 8)
    p = rng.randint((total - o) // 3, (total - o) * 2 // 3)
    dis = [f"Parking costs ${rng.randint(3, 12)} per hour.", f"The car park has {rng.randint(2, 6)} entrances.",
           f"The car park was built in {rng.randint(1985, 2020)}."]
    facts = [f"A car park has {f} floors.", f"Each floor has {s} spaces.", f"{_fmt(o)} spaces are reserved for staff and can't be used by visitors.",
             f"By noon, visitors have parked in {_fmt(p)} of the visitor spaces."]
    if level < 3:
        return facts, dis, "How many visitor spaces are still free at noon?", total - o - p, f"{f} * {s} - {o} - {p}", ("*", "-", "-")
    x = rng.randint(p // 10, p // 3)
    facts.append(f"Shortly after noon, {_fmt(x)} visitor cars leave.")
    return facts, dis, "How many visitor spaces are free after those cars leave?", total - o - p + x, f"{f} * {s} - {o} - {p} + {x}", ("*", "-", "-", "+")


def orchard(rng, level):
    r, t = rng.randint(18, 64), rng.randint(14, 40)
    dz = rng.randint(8, 25); per = dz * 12
    total = r * t * per; sp = rng.randint(total // 20, total // 6)
    dis = [f"The farm covers {rng.randint(20, 90)} hectares.", f"{rng.randint(5, 30)} pickers work there.",
           f"Apples sell for ${rng.randint(2, 5)} per kilogram."]
    if level < 3:
        facts = [f"An orchard has {r} rows of apple trees.", f"Each row has {t} trees.", f"Each tree gives {per} apples.",
                 f"{_fmt(sp)} apples are spoiled and thrown away."]
        return facts, dis, "How many good apples does the orchard harvest?", total - sp, f"{r} * {t} * {per} - {sp}", ("*", "*", "-")
    facts = [f"An orchard has {r} rows of apple trees.", f"Each row has {t} trees.", f"Each tree gives {dz} dozen apples.",
             f"{_fmt(sp)} apples are spoiled and thrown away."]
    return facts, dis, "How many good apples does the orchard harvest?", total - sp, f"{r} * {t} * {dz} * 12 - {sp}", ("*", "*", "*", "-")


def printing(rng, level):
    p, d = rng.randint(20, 75), rng.randint(5, 22)
    h = rng.randint(2, 8); m = h * 60
    j = rng.randint(100, 900)
    dis = [f"The printer cost ${_fmt(rng.randint(800, 4000))}.", f"Each page uses {rng.randint(2, 9)} millilitres of ink.",
           f"The office has {rng.randint(10, 60)} staff."]
    if level < 3:
        facts = [f"A printer prints {p} pages per minute.", f"The printer runs for {m} minutes each day.",
                 f"Over {d} days, {j} pages jam and are thrown away."]
        return facts, dis, "How many usable pages does it print over those days?", p * m * d - j, f"{p} * {m} * {d} - {j}", ("*", "*", "-")
    facts = [f"A printer prints {p} pages per minute.", f"The printer runs for {h} hours each day.",
             f"Over {d} days, {j} pages jam and are thrown away."]
    return facts, dis, "How many usable pages does it print over those days?", p * h * 60 * d - j, f"{p} * {h} * 60 * {d} - {j}", ("*", "*", "*", "-")


def water_tank(rng, level):
    t, r, h = rng.randint(3, 9), rng.randint(40, 180), rng.randint(4, 12)
    drained = t * r * h
    c = drained + rng.randint(1000, 9000)
    dis = [f"The tank is {rng.randint(3, 12)} metres tall.", f"Water costs ${rng.randint(2, 9)} per thousand litres.",
           f"The tank was last cleaned {rng.randint(2, 30)} days ago."]
    if level < 3:
        facts = [f"A tank holds {_fmt(c)} litres when full.", "The tank starts completely full.",
                 f"{t} taps are opened, and each drains {r} litres per hour.", f"The taps run for {h} hours."]
        return facts, dis, "How many litres are left in the tank?", c - drained, f"{c} - {t} * {r} * {h}", ("*", "*", "-")
    rm = rng.randint(1, 4); drained = t * rm * 60 * h; c = drained + rng.randint(1000, 9000)
    facts = [f"A tank holds {_fmt(c)} litres when full.", "The tank starts completely full.",
             f"{t} taps are opened, and each drains {rm} litres per minute.", f"The taps run for {h} hours."]
    return facts, dis, "How many litres are left in the tank?", c - drained, f"{c} - {t} * {rm} * 60 * {h}", ("*", "*", "*", "-")


def school_trip(rng, level):
    b, s, f = rng.randint(3, 9), rng.randint(32, 58), rng.randint(18, 75)
    d = rng.randint(2, 5)
    raised = b * s * f * (d if level == 3 else 1)
    c = rng.randint(raised // 3, raised * 4 // 5)
    dis = [f"The trip is {rng.randint(80, 400)} km away.", f"{rng.randint(6, 20)} teachers go along for free.",
           f"Each bus has {rng.randint(1, 3)} drivers."]
    if level < 3:
        facts = [f"{b} buses go on a school trip.", f"Each bus carries {s} students.", f"Each student pays ${f}.",
                 f"The trip costs the school ${_fmt(c)} in total."]
        return facts, dis, "How much money is left over after paying for the trip?", raised - c, f"{b} * {s} * {f} - {c}", ("*", "*", "-")
    facts = [f"{b} buses go on a school trip.", f"Each bus carries {s} students.", f"The trip lasts {d} days, and each student pays ${f} per day.",
             f"The trip costs the school ${_fmt(c)} in total."]
    return facts, dis, "How much money is left over after paying for the trip?", raised - c, f"{b} * {s} * {f} * {d} - {c}", ("*", "*", "*", "-")


def factory(rng, level):
    w, u, k = rng.randint(12, 60), rng.randint(15, 45), rng.randint(5, 14)
    n = rng.randint(2, 6)
    made = w * u * k * (n if level == 3 else 1)
    rj = rng.randint(made // 30, made // 10)
    dis = [f"The factory is {rng.randint(5, 50)} years old.", f"Each unit weighs {rng.randint(2, 15)} kg.",
           f"Each shift lasts {rng.randint(6, 10)} hours."]
    if level < 3:
        facts = [f"A factory has {w} workers.", f"Each worker assembles {u} units per shift.", f"There are {k} shifts each week.",
                 f"In that week, {_fmt(rj)} units fail inspection."]
        return facts, dis, "How many units pass inspection that week?", made - rj, f"{w} * {u} * {k} - {rj}", ("*", "*", "-")
    facts = [f"A factory has {w} workers.", f"Each worker assembles {u} units per shift.", f"There are {k} shifts each week.",
             f"Over {n} weeks, {_fmt(rj)} units fail inspection."]
    return facts, dis, f"How many units pass inspection over those {n} weeks?", made - rj, f"{w} * {u} * {k} * {n} - {rj}", ("*", "*", "*", "-")


def fundraiser(rng, level):
    e, g = rng.randint(3, 9), rng.randint(4, 12)
    q = rng.randint(400, 2500); c = rng.randint(q // 5, q // 2)
    t = e * g * q
    dis = [f"The club has {rng.randint(20, 120)} members.", f"Each event lasts {rng.randint(2, 6)} hours.",
           f"Last year the club raised ${_fmt(rng.randint(5000, 60000))}."]
    if level < 3:
        facts = [f"A club raises ${_fmt(t)} in total from {e} events, the same amount at each event.",
                 f"Each event's money is split equally among {g} groups.", f"Each group spends ${c} of its share from each event."]
        return facts, dis, "How much money does each group keep from one event?", q - c, f"{t} / {e} / {g} - {c}", ("/", "/", "-")
    facts = [f"A club raises ${_fmt(t)} in total from {e} events, the same amount at each event.",
             f"Each event's money is split equally among {g} groups.", f"Each group spends ${c} of its share from each event."]
    return facts, dis, f"How much money does each group keep in total across all {e} events?", (q - c) * e, f"({t} / {e} / {g} - {c}) * {e}", ("/", "/", "-", "*")


def shipping(rng, level):
    s = rng.choice([25, 40, 50]); k = rng.choice([20, 40, 60]); m = rng.randint(6, 40)
    c = rng.randint(150, 900)
    sacks = k * m; kg = sacks * s
    dis = [f"Each truck has {rng.randint(4, 18)} wheels.", f"The warehouse is {rng.randint(20, 300)} km from the port.",
           f"Rice sells for ${rng.randint(1, 4)} per kilogram."]
    if level < 3:
        facts = [f"A mill has {_fmt(kg)} kg of rice.", f"The rice is packed into sacks of {s} kg.",
                 f"Each truck carries {k} sacks.", f"Each full truck trip costs ${c}."]
        return facts, dis, "How much does it cost to ship all the rice?", m * c, f"{kg} / {s} / {k} * {c}", ("/", "/", "*")
    # whole tonnes: choose m so that kg is a multiple of 1,000
    while kg % 1000:
        m += 1; sacks = k * m; kg = sacks * s
    facts = [f"A mill has {kg // 1000} tonnes of rice.", f"The rice is packed into sacks of {s} kg.",
             f"Each truck carries {k} sacks.", f"Each full truck trip costs ${c}."]
    return facts, dis, "How much does it cost to ship all the rice?", m * c, f"{kg // 1000} * 1000 / {s} / {k} * {c}", ("*", "/", "/", "*")


def cinema(rng, level):
    r, s, f = rng.randint(12, 30), rng.randint(14, 28), rng.randint(3, 6)
    seats = r * s; e = rng.randint(seats // 8, seats // 3)
    dis = [f"Tickets cost ${rng.randint(8, 16)}.", f"The cinema has {rng.randint(2, 8)} snack counters.",
           f"Each film runs for about {rng.randint(90, 150)} minutes."]
    facts = [f"A cinema screen has {r} rows of {s} seats.", f"The screen shows {f} films every day.",
             f"On average, {e} seats are empty at each showing."]
    if level < 3:
        return facts, dis, "How many tickets does it sell per day?", (seats - e) * f, f"({r} * {s} - {e}) * {f}", ("*", "-", "*")
    return facts, dis, "How many tickets does it sell in one week?", (seats - e) * f * 7, f"({r} * {s} - {e}) * {f} * 7", ("*", "-", "*", "*")


DEV_TEMPLATES: dict[str, Callable] = {"bakery": bakery, "parking": parking}
TEST_TEMPLATES: dict[str, Callable] = {"orchard": orchard, "printing": printing, "water_tank": water_tank,
                                        "school_trip": school_trip, "factory": factory, "fundraiser": fundraiser,
                                        "shipping": shipping, "cinema": cinema}
DEV_SEED, TEST_SEED = 4100, 4200       # test seed is fixed now; test problems are generated, never read, before the run


def make_problems(split: str, level: int, n_per: int | None = None, seed: int | None = None) -> list[dict]:
    templates = DEV_TEMPLATES if split == "dev" else TEST_TEMPLATES
    n_per = n_per or (20 if split == "dev" else 50)
    rng = random.Random((seed if seed is not None else (DEV_SEED if split == "dev" else TEST_SEED)) + level)
    out = []
    for i in range(n_per):
        for name, fn in templates.items():
            facts, dis, q, gold, sol, ops = fn(rng, level)
            out.append(dict(id=len(out), split=split, level=level, template=name,
                            question=_assemble(rng, level, facts, dis, q), gold=gold, solution=sol, ops=list(ops)))
    return out


def check_problems(problems: list[dict]) -> dict:
    """Automatic checks (protocol gates 2 and 4 plus answer correctness). Never prints test questions."""
    errors = []
    for p in problems:
        val = calculate(p["solution"])
        if str(p["gold"]) != val:
            errors.append(f"{p['template']}#{p['id']}: solution {p['solution']} = {val}, gold {p['gold']}")
        if p["gold"] <= 0 or p["gold"] != int(p["gold"]):
            errors.append(f"{p['template']}#{p['id']}: gold {p['gold']} is not a positive integer")
        if tuple(p["ops"]) in EXEMPLAR_OPS:
            errors.append(f"{p['template']}#{p['id']}: operation sequence matches an exemplar")
        if len(p["ops"]) != (4 if p["level"] == 3 else 3):
            errors.append(f"{p['template']}#{p['id']}: expected {4 if p['level'] == 3 else 3} operations, got {len(p['ops'])}")
    return {"n": len(problems), "errors": errors,
            "templates": sorted({p["template"] for p in problems}),
            "gold_range": (min(p["gold"] for p in problems), max(p["gold"] for p in problems))}


def leakage_check() -> list[str]:
    """Gate 4: no test template is a dev template, and no test operation sequence matches an exemplar."""
    issues = [f"template {t} is in both dev and test" for t in set(DEV_TEMPLATES) & set(TEST_TEMPLATES)]
    for level in (1, 2, 3):
        for p in make_problems("test", level, n_per=1):
            if tuple(p["ops"]) in EXEMPLAR_OPS:
                issues.append(f"test template {p['template']} (level {level}) matches an exemplar's operations")
    return issues
