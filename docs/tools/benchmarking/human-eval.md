# HumanEval

## What it is
HumanEval is a benchmark released by OpenAI to evaluate the code generation capabilities of Large Language Models. It consists of 164 handwritten programming problems, each including a function signature, docstring, body, and several unit tests. The problems are designed to be self-contained and assess the model's ability to solve basic algorithmic tasks. The key metric is Pass@k, the probability that at least one of the top k generated code samples passes all unit tests.

## What problem it solves
Provides a standardized measure of whether LLMs can generate functionally correct code from natural language descriptions.

## Where it fits in the stack
**Benchmarking**. Used as a primary reference benchmark for code generation capabilities of LLMs.

## Typical use cases
- Evaluating LLM code generation accuracy on self-contained programming tasks
- Comparing models on their ability to produce correct Python code
- Measuring improvements in code generation across model versions

## Strengths
- Well-established and widely cited benchmark
- Problems are self-contained with clear unit test validation
- Pass@k metric accounts for sampling variability

## Limitations
- Only 164 problems, which may not cover the full range of programming tasks
- Focuses on Python and basic algorithmic tasks
- Does not test real-world software engineering skills like debugging or working with existing codebases

## When to use it
- When comparing LLMs on their ability to generate correct code from specifications
- When evaluating a model for coding assistant use cases

## When not to use it
- When you need to evaluate real-world software engineering capability (use [SWE-bench](swe-bench.md) instead)
- When you need multilingual code generation evaluation

## Related tools / concepts
- [MBPP (Mostly Basic Python Problems)](mbpp.md)
- [BigCodeBench](https://github.com/bigcode-project/bigcodebench)

## Sources / references
- [GitHub Repository](https://github.com/openai/human-eval)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
