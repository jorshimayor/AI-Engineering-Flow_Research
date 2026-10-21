# Week 4 Resources: Research Methodology for Applied AI

All links checked on 2026-10-15. **Legend:** ⭐ start here · 🟢 beginner · 🟡 intermediate · 🔴 advanced · 💻 hands-on

---

## Suggested path

1. ⭐ Read *AI Agents That Matter*: sections 2 (cost), 4 (holdouts) and 5 (reproducibility).
2. ⭐ Read Anthropic's *A statistical approach to model evaluations*, the short version of *Adding Error Bars to Evals*. It covers the CIs and paired tests used in this week's audit.
3. ⭐ Watch StatQuest on p-values, then on power analysis (about 20 minutes total).
4. ⭐ Read *With Little Power Comes Great Responsibility*: why underpowered NLP experiments are the norm.
5. Read Hamel Husain's *Your AI Product Needs Evals* for the practitioner's view.
6. Skim *Establishing Best Practices for Building Rigorous Agentic Benchmarks* as a checklist for the protocol.

---

## 1. Papers

### The Week 4 paper and its follow-up
| Paper | Why |
|---|---|
| ⭐ [AI Agents That Matter](https://arxiv.org/abs/2407.01502), Kapoor et al. (TMLR 2025) | Cost-aware evaluation, holdouts by generality level, reproducibility |
| [Holistic Agent Leaderboard (HAL)](https://arxiv.org/abs/2510.11977), Kapoor et al. (ICLR 2026) · [site](https://hal.cs.princeton.edu/) | The infrastructure answer: 21,730 rollouts, 9 models, 9 benchmarks, all logs released. Also the Week 11 and 18 reading |

### Statistics for LLM evaluation
| Paper | Why |
|---|---|
| ⭐ [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640), Miller 2024 (Anthropic) | CIs, clustered standard errors, paired differences, power analysis for evals |
| ⭐ [With Little Power Comes Great Responsibility](https://arxiv.org/abs/2010.06595), Card et al. 2020 | Most NLP comparisons are underpowered; how to compute power |
| [The Hitchhiker's Guide to Testing Statistical Significance in NLP](https://aclanthology.org/P18-1128/), Dror et al. 2018 | Which test to use when (McNemar, bootstrap, permutation) |
| [Quantifying Variance in Evaluation Benchmarks](https://arxiv.org/abs/2406.10229), Madaan et al. 2024 | How much scores move with seeds and small changes |
| [Show Your Work: Improved Reporting of Experimental Results](https://arxiv.org/abs/1909.03004), Dodge et al. 2019 | Report the budget spent tuning, not just the best result (the winner's curse) |
| [Are Emergent Abilities of LLMs a Mirage?](https://arxiv.org/abs/2304.15004), Schaeffer et al. 2023 | How the choice of metric can create or erase an "effect" |

### Benchmarks, holdouts and leakage
| Paper | Why |
|---|---|
| ⭐ [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825), Zhu et al. 2025 | A checklist for agent benchmark validity. Use it to review a protocol |
| [Do ImageNet Classifiers Generalize to ImageNet?](https://arxiv.org/abs/1902.10811), Recht et al. 2019 | What happens on a truly fresh test set |
| [Leakage and the Reproducibility Crisis in ML-based Science](https://arxiv.org/abs/2207.07048), Kapoor and Narayanan 2023 | A taxonomy of leakage; the same authors' earlier work |
| [Lessons from the Trenches on Reproducible Evaluation of LMs](https://arxiv.org/abs/2405.14782), Biderman et al. 2024 | Practical reproducibility from the lm-evaluation-harness team |
| [HELM: Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110), Liang et al. 2022 | Multi-metric evaluation (accuracy, calibration, robustness, cost) |

### Research methodology in general
| Reading | Why |
|---|---|
| [Why Most Published Research Findings Are False](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124), Ioannidis 2005 | Small samples + small effects + flexible analysis = mostly false positives |
| [The Garden of Forking Paths](http://www.stat.columbia.edu/~gelman/research/unpublished/p_hacking.pdf), Gelman and Loken | You can p-hack without trying, just by choosing the analysis after seeing data |
| [How to Read a Paper](http://ccr.sigcomm.org/online/files/p83-keshavA.pdf), Keshav | The three-pass method. Also placed at Week 17 in the fellowship guide |
| [You and Your Research](https://www.cs.columbia.edu/~nieh/teaching/gradguide/hamming.html), Hamming | Choosing important problems (Week 25 reading) |
| [Research Debt](https://distill.pub/2017/research-debt/), Olah and Carter | Clear explanation is part of the research job (Week 47 reading) |

---

## 2. Videos
| Video | Channel |
|---|---|
| ⭐ [p-values: What they are and how to interpret them](https://www.youtube.com/watch?v=vemZtEM63GY) | StatQuest |
| ⭐ [Statistical Power, Clearly Explained](https://www.youtube.com/watch?v=Rsc5znwR5FA) | StatQuest |
| ⭐ [Power Analysis, Clearly Explained](https://www.youtube.com/watch?v=VX_M3tIyiYk) | StatQuest |
| [AI Agents: Substance or Snake Oil, with Arvind Narayanan](https://www.youtube.com/watch?v=HScABWB98Kw) | TWIML AI Podcast. Narayanan discusses *AI Agents That Matter* |

---

## 3. Courses and interactive
| Resource | Level | Notes |
|---|---|---|
| [Seeing Theory](https://seeing-theory.brown.edu/) (Brown University) | 🟢 | Interactive visual intro to probability, CIs and inference |
| [Khan Academy: Statistics and Probability](https://www.khanacademy.org/math/statistics-probability) | 🟢 | Full refresher on CIs, hypothesis tests and significance |

---

## 4. Articles
| Article | Notes |
|---|---|
| ⭐ [A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals), Anthropic | Five recommendations, including paired differences and power analysis |
| ⭐ [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), Hamel Husain | Week 8 reading; worth reading now for context |
| [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/), Hamel Husain | Error analysis first, metrics second |
| [Task-Specific LLM Evals that Do and Don't Work](https://eugeneyan.com/writing/evals/), Eugene Yan | Which metrics hold up for classification, summarisation and more |
| [New paper: AI agents that matter](https://www.aisnakeoil.com/p/new-paper-ai-agents-that-matter), AI Snake Oil | The authors' own plain-language summary |
| [How Not To Run an A/B Test](https://www.evanmiller.org/how-not-to-run-an-ab-test.html), Evan Miller | Why peeking at results and stopping early breaks significance. Same author as *Adding Error Bars* |
| [Preregistration](https://www.cos.io/initiatives/prereg), Center for Open Science | How and why to write down the analysis before the data |
| [Design doc library](https://www.designdocs.dev/) | Examples of real design docs (the fellowship's Week 25 resource) |

---

## 5. Tools 💻
| Tool | What for |
|---|---|
| [`src/stats.py`](../../src/stats.py) | This week's helpers: Wilson CI, McNemar, bootstrap, Holm, power |
| [Inspect](https://inspect.aisi.org.uk/) (UK AI Security Institute) | Open-source eval framework with built-in standard errors |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Standard harness for model benchmarks |
| [HAL harness](https://github.com/princeton-pli/hal-harness) | The standardised agent harness from the HAL paper |
