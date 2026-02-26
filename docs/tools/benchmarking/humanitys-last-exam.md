# Humanity's Last Exam (HLE)

## What it is
HLE is a benchmark designed to test the limits of LLMs on the most difficult human-level tasks. It consists of highly complex, multi-disciplinary questions that require deep expertise and advanced reasoning to solve. It is intended to remain challenging even as models continue to improve.

## What problem it solves
Addresses the saturation of easier benchmarks by providing a set of questions that push the boundaries of current LLM capabilities, helping track progress toward expert-level AI.

## Where it fits in the stack
**Benchmarking**. Serves as a frontier-difficulty benchmark for measuring the upper limits of LLM reasoning.

## Typical use cases
- Evaluating whether state-of-the-art models can handle the most difficult expert-level questions
- Tracking progress of frontier models over time
- Identifying remaining capability gaps in advanced reasoning

## Strengths
- Designed to remain challenging as models improve
- Multi-disciplinary, covering a broad range of expert knowledge
- Targets the frontier of LLM capabilities

## Limitations
- May become less informative if models saturate it over time
- Complex questions make it harder to diagnose specific failure modes
- Limited public detail on exact question composition

## When to use it
- When evaluating frontier models on the hardest available reasoning tasks
- When existing benchmarks like MMLU or GPQA are too easy for the models being tested

## When not to use it
- When evaluating practical, everyday LLM capabilities
- When you need domain-specific benchmarking rather than general difficulty

## Related tools / concepts
- [GPQA](gpqa.md)
- [MMLU](https://github.com/hendrycks/test)

## Sources / references
- [HLE Website](https://humanityslastexam.ai/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
