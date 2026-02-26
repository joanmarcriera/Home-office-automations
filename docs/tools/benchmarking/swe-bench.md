# SWE-bench

## What it is
SWE-bench is a benchmark for evaluating LLMs on real-world software engineering tasks. It uses actual issues from GitHub and requires the model to generate a functional patch that passes existing tests.

## What problem it solves
Measures whether LLMs can perform practical software engineering work -- understanding codebases, diagnosing issues, and producing working fixes -- rather than just solving isolated coding puzzles.

## Where it fits in the stack
**Benchmarking**. Used as a reference benchmark for evaluating real-world software engineering capabilities of LLMs and AI agents.

## Typical use cases
- Evaluating AI coding agents on their ability to resolve real GitHub issues
- Comparing models on practical software engineering tasks
- Tracking progress of AI agents toward autonomous software development

## Strengths
- Based on real-world GitHub issues, providing authentic evaluation
- Requires end-to-end engineering skills (reading code, understanding issues, writing patches)
- Validated by existing test suites from the source repositories

## Limitations
- Computationally expensive to run (requires setting up real repositories and test suites)
- Limited to Python repositories in the current dataset
- Pass rates can be influenced by the specific subset of issues selected

## When to use it
- When evaluating AI agents or LLMs on real-world software engineering capability
- When comparing coding agents that claim to autonomously resolve issues

## When not to use it
- When evaluating basic code generation from specifications (use [HumanEval](human-eval.md) instead)
- When you need quick, lightweight benchmarking

## Related tools / concepts
- [HumanEval](human-eval.md)
- [Terminal-Bench](terminal-bench.md)

## Sources / references
- [Official Website](https://www.swebench.com/)
- [GitHub Repository](https://github.com/princeton-nlp/SWE-bench)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
