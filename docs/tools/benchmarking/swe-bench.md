# SWE-bench

## What it is
SWE-bench (Software Engineering Benchmark) is a data-driven benchmark for evaluating Large Language Models on their ability to resolve real-world GitHub issues.

## What problem it solves
It moves beyond simple code generation to evaluate repo-scale software engineering, where models must understand a large codebase, navigate multiple files, and produce valid fixes for actual reported bugs.

## Where it fits in the pipeline
**Act / Reason (Benchmark)**

## Typical use cases (in this homelab / family automation context)
- Assessing the autonomy of AI coding agents like OpenHands or Aider in handling complex homelab development tasks.
- Verifying the effectiveness of different reasoning models (e.g., o1, o3) for software maintenance.

## Integration points
- **GitHub**: Built on thousands of real-world issues and pull requests.
- **Docker**: Usually requires an isolated environment to run and verify the generated fixes.

## Licensing and cost
- **Open Source**: The benchmark dataset and evaluation harness are open source.
- **Cost**: Free to run; requires significant compute for verification.

## Strengths
- High ecological validity (uses real GitHub issues).
- Hard to game; requires genuine understanding and debugging skills.

## Limitations
- Very difficult for most models to achieve high scores.
- Verification process can be slow and resource-intensive.

## Alternatives / Related tools
- **HumanEval**
- **MBPP** (Mostly Basic Python Problems)

## Links
- [Official Website](https://www.swebench.com/)
- [GitHub](https://github.com/princeton-nlp/swe-bench)
