# Week 4 Sources: Research Methodology for Applied AI

Sources behind the Week 4 notebook ([`jupyter/week4_rigour_audit.ipynb`](../jupyter/week4_rigour_audit.ipynb)), the statistics helpers ([`src/stats.py`](../src/stats.py)) and the eval protocol. All links checked on 15 October 2026.

## Anchor paper
- Kapoor, Stroebl, Siegel, Nadgir and Narayanan. [AI Agents That Matter](https://arxiv.org/abs/2407.01502). TMLR, 2025. Project site: [agents.cs.princeton.edu](https://agents.cs.princeton.edu/)
- Kapoor et al. [Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation](https://arxiv.org/abs/2510.11977). ICLR, 2026. [Poster](https://iclr.cc/virtual/2026/poster/10006806) · [Leaderboard and harness](https://hal.cs.princeton.edu/)

## Statistics for evaluation
- Miller. [Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations](https://arxiv.org/abs/2411.00640). 2024. Summary: [A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- Bowyer, Aitchison and Ivanova. [Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints](https://proceedings.mlr.press/v267/bowyer25a.html). ICML, 2025
- Card et al. [With Little Power Comes Great Responsibility](https://arxiv.org/abs/2010.06595). EMNLP, 2020
- Dror et al. [The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing](https://aclanthology.org/P18-1128/). ACL, 2018
- Madaan et al. [Quantifying Variance in Evaluation Benchmarks](https://arxiv.org/abs/2406.10229). 2024
- Dodge et al. [Show Your Work: Improved Reporting of Experimental Results](https://arxiv.org/abs/1909.03004). EMNLP, 2019
- [Statistical power in LLM evals](https://tianpan.co/blog/2026/04/15/statistical-power-llm-evals) (practitioner blog, used for context only)

## Benchmarks, holdouts and agent evaluation
- Zhu et al. [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825). 2025
- Recht et al. [Do ImageNet Classifiers Generalize to ImageNet?](https://arxiv.org/abs/1902.10811). ICML, 2019
- Kapoor and Narayanan. [Leakage and the Reproducibility Crisis in Machine-Learning-Based Science](https://arxiv.org/abs/2207.07048). Patterns, 2023
- [How to Build Effective Evals for AI Agents](https://www.kdnuggets.com/how-to-build-effective-evals-for-ai-agents), KDnuggets (practitioner context)
- [How to Evaluate AI Agents: The Eval Methodology](https://getwidget.dev/blog/how-to-evaluate-ai-agents/), GetWidget (practitioner context)

## Methods used in the code
| Method in `src/stats.py` | Reference |
|---|---|
| Wilson score interval | Wilson, 1927; recommended for small samples in Miller (2024) and Bowyer et al. (2025) |
| Exact McNemar test | McNemar, 1947; paired 0/1 outcomes, as recommended in Dror et al. (2018) |
| Paired bootstrap and sign-flip permutation test | Dror et al. (2018) |
| Holm-Bonferroni correction | Holm, 1979 |
| Power by simulation | Card et al. (2020); Miller (2024) |

## Talks
- [AI Agents: Substance or Snake Oil, with Arvind Narayanan](https://www.youtube.com/watch?v=HScABWB98Kw), TWIML AI Podcast
