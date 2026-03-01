# DREAM: Deep Research Evaluation with Agentic Metrics

## What it is
DREAM (Deep Research Evaluation with Agentic Metrics) is an agentic evaluation framework for deep research agents. It uses tool-calling agents to independently verify the factual correctness and temporal validity of research reports.

## What problem it solves
It addresses the "Mirage of Synthesis"—a defect in static LLM evaluation where fluent writing and plausible citations hide factual errors or reasoning flaws. Static judges cannot verify claims against real-world evidence; DREAM solves this by making the evaluator as capable (agentic) as the agent it is testing.

## Where it fits in the stack
**Eval**: It is a framework for benchmarking and evaluating advanced LLM agentic performance.

## Typical use cases
- **Benchmarking Research Agents**: Comparing how well different models or agent architectures (like OpenHands or custom research loops) generate accurate analyst-grade reports.
- **Reasoning Probes**: Systematically identifying reasoning defects in long-form generation.

## Strengths
- **Parity-based Evaluation**: Uses agents to evaluate agents, ensuring the evaluator has the tools necessary to verify modern information.
- **Sensitivity to Decay**: Significantly more sensitive to factual and temporal decay than static benchmarks.
- **Scalable and Reference-Free**: Does not require a pre-defined ground truth for every query, allowing for flexible evaluation of open-ended research.

## Limitations
- **Operational Complexity**: Requires a tool-calling environment for the evaluation agent, making it more complex to run than static Q&A.
- **Cost**: Agentic evaluation involves multiple LLM turns, increasing the cost of benchmarking.

## When to use it
- When evaluating agents that perform active research or use external tools.
- When static benchmarks are suspected of suffering from data contamination or lack of temporal awareness.

## When not to use it
- For evaluating simple base models on static knowledge.
- When a fast, low-cost evaluation signal is needed for iterative model tuning.

## Related tools / concepts
- [Humanity's Last Exam (HLE)](./humanitys-last-exam.md)
- [LM Evaluation Harness](./lm-evaluation-harness.md)
- [GPQA](./gpqa.md)

## Sources / references
- [Hugging Face Paper Page](https://huggingface.co/papers/2602.18940)
- [arXiv Preprint (arXiv:2602.18940)](https://arxiv.org/abs/2602.18940)


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01