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
- Choosing whether an agent is ready for repository-maintenance work that requires reading tests, editing files, and producing a valid patch

## Strengths
- Based on real-world GitHub issues, providing authentic evaluation
- Requires end-to-end engineering skills (reading code, understanding issues, writing patches)
- Validated by existing test suites from the source repositories

## Limitations
- Computationally expensive to run (requires setting up real repositories and test suites)
- Limited to Python repositories in the current dataset
- Pass rates can be influenced by the specific subset of issues selected
- Public leaderboard results do not automatically prove performance on private repositories, unusual stacks, or documentation-heavy maintenance work

## When to use it
- When evaluating AI agents or LLMs on real-world software engineering capability
- When comparing coding agents that claim to autonomously resolve issues

## When not to use it
- When evaluating basic code generation from specifications (use [HumanEval](human-eval.md) instead)
- When you need quick, lightweight benchmarking

## Practical evaluation notes

Use SWE-bench as a high-signal engineering benchmark, but interpret it as one part of an agent-readiness picture:

- **Patch correctness**: The benchmark rewards changes that satisfy existing test suites, which is useful for bug-fix agents but less direct for docs, taxonomy, and knowledge-base tasks.
- **Repository navigation**: Strong results imply the model or harness can locate relevant files, reason over issue text, and make coherent edits in a real repo.
- **Harness quality**: Tooling around the model matters. Search, edit, test execution, retries, and patch application can change outcomes as much as the base model.
- **Local validation**: For private repo adoption, run a small internal task set alongside SWE-bench-style metrics so results reflect local languages, CI shape, and review expectations.

## Agent comparison checklist

When using SWE-bench results to compare coding agents, record:

1. The exact benchmark split and date.
2. The model, agent harness, tool access, and retry budget.
3. Whether the run used public issue text only or any extra retrieval.
4. Pass rate plus failure classes: setup failure, wrong file, incomplete patch, flaky test, or unsafe behavior.
5. Cost per resolved issue, not only raw pass rate.

## Related tools / concepts

- [HumanEval](human-eval.md)
- [Terminal-Bench](terminal-bench.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [LongCLI-Bench](longcli-bench.md)
## Sources / references
- [Official Website](https://www.swebench.com/)
- [GitHub Repository](https://github.com/princeton-nlp/SWE-bench)
- [SWE-bench paper](https://arxiv.org/abs/2310.06770)
- [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)

## Contribution Metadata

- Last reviewed: 2026-05-07
- Confidence: medium
