# InterCode

## What it is
InterCode is an interactive benchmarking framework designed for evaluating Large Language Models (LLMs) in real-world programming and shell environments. It focuses on multi-turn interactions where the model can execute code or commands and receive feedback from the environment.

## What problem it solves
Standard static benchmarks (like HumanEval) often fail to capture the interactive nature of software development. InterCode addresses this by providing an environment where models must reason over multiple steps, handle errors, and adapt based on actual execution results.

## Where it fits in the stack
**Benchmarking**. It sits in the "agentic" evaluation space, testing the model's ability to act as a coding assistant or terminal agent.

## Typical use cases
- Evaluating LLM performance in Bash/Shell environments.
- Testing SQL generation and execution capabilities.
- Benchmarking models on multi-step programming tasks that require execution feedback.

## Strengths
- **Interactivity**: Models can "try and fail," mirroring human developer workflows.
- **Diversity**: Supports multiple languages and environments (Bash, SQL, etc.).
- **Realism**: Uses actual Dockerized environments for safe, reproducible execution.

## Limitations
- **Complexity**: Harder to set up than static, text-only benchmarks.
- **Resource Intensive**: Requires running containers for evaluation.
- **Niche**: Primarily focused on code/terminal interaction rather than general knowledge.

## When to use it
- When developing coding agents or terminal-based AI assistants.
- When you need to measure how well a model handles real-world execution errors.

## When not to use it
- For quick, "shallow" evaluations of general model intelligence.
- When you don't have the infrastructure to run Docker-based evaluations safely.

## Related tools / concepts
- [SWE-bench](swe-bench.md)
- [Terminal-Bench](terminal-bench.md)
- [HumanEval](human-eval.md)
- [OpenHands](../development_ops/openhands.md)

## Sources / references
- [GitHub Repository](https://github.com/princeton-nlp/intercode)
- [Research Paper](https://arxiv.org/abs/2306.14898)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
