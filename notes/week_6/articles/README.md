# Week 6 Articles

| # | Article | Covers | Outline |
|---|---|---|---|
| 1 | My Agent Called the Calculator Before It Knew the Prices | Native tool calling, schema validation, the repair loop, and why most failures were planning, not format | [01-validate-and-repair.md](01-validate-and-repair.md) |
| 2 | What Moving Two Tools Behind MCP Actually Cost | Integration effort, the SDK traps, and a 6-point gap that opened only in the repair loop | [02-direct-vs-mcp.md](02-direct-vs-mcp.md) |

**Order:** 1 then 2.
**Figures:** [`results/figures/week6_success_by_route.png`](../../../results/figures/week6_success_by_route.png), [`results/figures/week6_malformed_types.png`](../../../results/figures/week6_malformed_types.png).
**Hook:** 96% of the 1.5B model's runs asked the calculator for a total before it had looked up a single price.
**Report honestly:** H1 holds at 3B only, and the 1.5B result sits at a floor; H2 at 3B is inconclusive; the planning findings are exploratory.

Each outline has self-check questions and one stretch experiment.
