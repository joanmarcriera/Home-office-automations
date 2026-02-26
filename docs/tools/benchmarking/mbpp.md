# MBPP (Mostly Basic Python Problems)

## What it is
MBPP is a benchmark designed to evaluate the code generation performance of LLMs on basic Python tasks. It consists of around 1,000 crowd-sourced Python programming problems, designed to be solvable by entry-level programmers. Each problem includes a task description, a code solution, and three automated test cases. Key metrics are Pass@1 (accuracy on the first attempt) and Pass@k (success rate with multiple samples).

## What problem it solves
Provides a large-scale, standardized evaluation of LLM code generation on entry-level Python problems, complementing more difficult benchmarks like HumanEval.

## Where it fits in the stack
**Benchmarking**. Used as a reference benchmark for evaluating basic code generation capabilities of LLMs.

## Typical use cases
- Evaluating LLM performance on straightforward Python coding tasks
- Comparing code generation accuracy across models at the entry level
- Complementing HumanEval results with a larger problem set

## Strengths
- Large dataset (around 1,000 problems) for statistically robust evaluation
- Problems are straightforward and well-defined
- Includes automated test cases for objective scoring

## Limitations
- Limited to basic Python problems; does not test advanced programming
- Crowd-sourced problems may have inconsistent quality
- Does not evaluate real-world software engineering tasks

## When to use it
- When evaluating basic code generation capabilities alongside HumanEval
- When you need a larger problem set than HumanEval for more robust statistics

## When not to use it
- When evaluating advanced programming or real-world engineering tasks
- When testing non-Python code generation

## Related tools / concepts
- [HumanEval](human-eval.md)
- [EvalPlus](https://github.com/evalplus/evalplus)

## Sources / references
- [GitHub Repository](https://github.com/google-research/google-research/tree/master/mbpp)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
