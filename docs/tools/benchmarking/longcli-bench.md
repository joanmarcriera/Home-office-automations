# LongCLI-Bench

## What it is
LongCLI-Bench is a preliminary benchmark and study focused on evaluating AI agents in long-horizon programming tasks within command-line interfaces (CLIs). It measures an agent's ability to plan and execute multi-step engineering workflows.

## What problem it solves
It addresses the gap in agent evaluation for realistic software engineering tasks. Most existing benchmarks are limited by short horizons, data contamination, or lack of fine-grained metrics. LongCLI-Bench tests agents on complex, multi-step tasks fromCS assignments and real-world workflows, highlighting failures in planning and long-term execution.

## Where it fits in the stack
**Eval**: It is a specialized benchmark for evaluating the **Agentic** and **Execution** layers of AI coding systems.

## Typical use cases
- **Coding Assistant Benchmarking**: Testing tools like [Aider](../development_ops/aider.md) or [OpenHands](../development_ops/openhands.md) on complex, multi-tool tasks.
- **Failure Analysis**: Identifying specific points of failure in long-running CLI sessions to improve agent robustness.
- **Human-Agent Collaboration Study**: Evaluating how plan injection and guidance from humans can improve agent success rates.

## Strengths
- **Long-Horizon focus**: Specifically targets tasks that require sustained reasoning and multiple sequential actions.
- **Step-Level Scoring**: Pinpoints exactly where an agent stalls or deviates from the task requirements.
- **Realistic Tasks**: Includes "from scratch" development, feature addition, bug fixing, and refactoring scenarios.

## Limitations
- **CLI-Centric**: Focused on terminal interactions, which may not capture all agentic modalities.
- **Nascent Benchmark**: As a preliminary study, it may still be expanding its set of evaluation instances.

## When to use it
- When testing agents designed for autonomous coding or system administration.
- When you need a more rigorous evaluation of an agent's ability to follow complex, multi-step instructions without stalling.

## When not to use it
- For testing general chat capabilities or single-turn information retrieval.
- When evaluation does not involve terminal or shell access.

## Related tools / concepts
- [SWE-bench](./swe-bench.md)
- [Terminal-Bench](./terminal-bench.md)
- [Aider](../development_ops/aider.md)

## Sources / references
- [Hugging Face Paper Page](https://huggingface.co/papers/2602.14337)
- [arXiv Preprint (arXiv:2602.14337)](https://arxiv.org/abs/2602.14337)
- [LongCLI-Bench GitHub Repository](https://github.com/finyorko/longcli-bench)


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01