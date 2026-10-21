<div align="center">

<img src="docs/images/hero.png" width="640" alt="Probability distributions → statistical learning → sampling and inference">

# Free Energy to LLMs

### Generative Models and Probability: From Variational Free Energy to LLM Training and Inference

[![Download PDF](https://img.shields.io/github/v/release/refraction-ray/free-energy-to-llms?label=Download%20PDF&color=0E7490)](https://github.com/refraction-ray/free-energy-to-llms/releases/latest)
[![build](https://github.com/refraction-ray/free-energy-to-llms/actions/workflows/build.yml/badge.svg)](https://github.com/refraction-ray/free-energy-to-llms/actions/workflows/build.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-14324A.svg)](LICENSE)

[中文](README.md) | English

</div>

---

A textbook on generative models that runs from mathematical derivation all the way to engineering practice, with statistical physics and probability as the common thread. The book is written in Chinese.

The knowledge behind generative models and LLMs is scattered across the curricula of several disciplines:

- Students of mathematics and statistics know probability theory, KL divergence, the calculus of variations and stochastic differential equations, but rarely see how these tools land on an LLM that is actually being trained: which gradient GRPO estimates, along which path Flow Matching regresses a velocity field, how MLA squeezes K/V into a single low-dimensional cache.
- Physics students know the Boltzmann distribution, free energy, Langevin dynamics and the renormalization group, yet may not know that each has a direct counterpart in machine learning: variational inference minimizes a free energy, energy-based models are Boltzmann distributions, diffusion sampling is Langevin dynamics, and Born machines encode probabilities in quantum amplitudes.
- Computer science students and LLM engineers know Transformers, training pipelines and inference engines, and they feel the weight of KV caches, memory bandwidth and parallelism, but seldom get to derive from probability what distribution these models fit, where the objective comes from, and why sampling works the way it does.

This book joins these pieces on one thread. Every model is examined through the same four questions: what distribution it represents, what objective trains it, how it samples, and where the real bottleneck lies. Along this thread the book moves from VAEs, flows, GANs, diffusion and energy-based models to Transformers, multimodal models and RL post-training, then to training systems, inference systems, agent systems and recent architectural innovations from DeepSeek and Kimi, and finally back to generative models in scientific computing.

- About 150 pages: 11 chapters and 2 appendices
- 34 original vector figures, all written in TikZ, with source included
- 134 references, from classic papers to 2025–2026 technical reports

## Contents

| Ch. | Topic | Highlights |
|---|---|---|
| 1 | From function fitting to probability distributions | Discrimination, generation and inverse design; Bayesian conditioning; directions of KL; maximum likelihood and variational free energy |
| 2 | Generative model families: representation, training, sampling | Autoregressive models, VAE, normalizing flows, GAN, MMD, Born machines, energy-based models and MCMC, score matching, diffusion and Flow Matching |
| 3 | Transformer | Tokens and embeddings, Q/K/V, causal masking, attention variants, normalization, FFN, MoE |
| 4 | Multimodal understanding and generation | Visual token budgets, CLIP and mutual information, VLM connectors, conditioning, unified multimodal models |
| 5 | Training: from pre-training to verifiable rewards | Pre-training, SFT, LoRA, PPO, DPO, GRPO, verifiable rewards |
| 6 | Training systems | AdamW and Muon, QK-Norm, mixed precision, training memory budget, data/tensor/expert parallelism |
| 7 | Inference systems | Prefill and decode, KV cache sizing, FlashAttention, speculative decoding, prefill–decode disaggregation and serving metrics |
| 8 | Agent systems | The agent loop and tool calls, cost of context caching, skills and memory, agentic search, sub-agents, pass@k |
| 9 | Case studies: DeepSeek and Kimi architectures | MLA, DSA, mHC, CSA/HCA, KDA, AttnRes, Stable LatentMoE |
| 10 | Statistical pitfalls in data and evaluation | Mode coverage, FID, precision/recall, perplexity, out-of-distribution generalization |
| 11 | Generative models back in scientific computing | Finite-temperature sampling and variational autoregressive networks, flows and neural renormalization group, molecule and crystal generation, quantum circuit search, quantum states and tensor networks |
| App. | Reading index; formulas and notation | |

## Download and build

Release PDFs are on the [Releases](https://github.com/refraction-ray/free-energy-to-llms/releases/latest) page; each version tag triggers GitHub Actions to rebuild the book from source and publish it. The compiled PDFs are also kept in the repository next to their sources, so they open directly on GitHub: the book is [`book/free-energy-to-llms.pdf`](book/free-energy-to-llms.pdf), and each figure's PDF sits beside its TikZ source in [`figures/`](figures/).

Building from source needs TeX Live (XeLaTeX, Biber) and the open-source font Noto Sans CJK SC (identical to Source Han Sans SC):

```bash
# macOS
brew install --cask font-noto-sans-cjk-sc
# Ubuntu / Debian
sudo apt install fonts-noto-cjk

make            # figures and book → figures/*.pdf, book/free-energy-to-llms.pdf
make figures    # figures only
make clean      # remove the intermediate build/ directory
```

Layout: `book/` holds the text (`main.tex`, one source file per chapter, `references.bib`); `figures/` holds one standalone TikZ source per figure, its compiled PDF, and the shared style `figstyle.sty`.

## Author

Shi-Xin Zhang is a Distinguished Research Fellow and doctoral supervisor at the Institute of Physics, Chinese Academy of Sciences, working on quantum computing, quantum many-body physics and machine learning for both, and the creator and maintainer of the open-source quantum software platform [TensorCircuit-NG](https://github.com/tensorcircuit/tensorcircuit-ng).

[Homepage](https://re-ra.xyz/) · [Group](https://sxzgroup.github.io/) · [IOP profile](https://iop.cas.cn/rcjy/tpyjy/?id=6789) · [Google Scholar](https://scholar.google.com/citations?user=Ut8nVqIAAAAJ) · [GitHub](https://github.com/refraction-ray)

## Errata and feedback

Please report errors or suggestions in [Issues](https://github.com/refraction-ray/free-energy-to-llms/issues), with the PDF version and page number. Pull requests against the sources in `book/` are welcome.

## Citation

```bibtex
@misc{zhang2026freeenergy,
  author       = {Zhang, Shi-Xin},
  title        = {Free Energy to {LLMs}: Generative Models and Probability, from Variational Free Energy to {LLM} Training and Inference},
  year         = {2026},
  howpublished = {\url{https://github.com/refraction-ray/free-energy-to-llms}}
}
```

## License

The text, figures and figure sources are licensed under [CC BY-NC-SA 4.0](LICENSE): you may copy, adapt and redistribute them with attribution, for non-commercial purposes only, and derivative works must carry the same license.
