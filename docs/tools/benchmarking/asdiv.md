# ASDiv (Academia Sinica Diverse MWP Dataset)

## What it is
ASDiv (Academia Sinica Diverse Math Word Problem) is a diverse corpus of 2,305 English Math Word Problems (MWPs). It is designed to evaluate the linguistic and problem-solving diversity of mathematical reasoning models, providing a more challenging and diverse set of problems than older benchmarks.

## What problem it solves
It addresses the lack of diversity in traditional math word problem datasets. By providing problems with high linguistic variety and different mathematical operations, it measures a model's ability to truly understand the problem description rather than relying on simple template matching.

## Where it fits in the stack
**Benchmarking**. It is used to evaluate the mathematical reasoning and language understanding capabilities of LLMs.

## Typical use cases
- Benchmarking LLM performance on diverse mathematical word problems.
- Evaluating the robustness of math solvers across different linguistic phrasings.
- Researching the intersection of natural language understanding and formal reasoning.

## Strengths
- **Linguistic Diversity**: Contains a wide range of vocabulary and sentence structures.
- **Problem Variety**: Covers various types of mathematical operations and reasoning steps.
- **Manual Annotation**: High-quality, human-annotated problems.

## Limitations
- **Size**: Smaller than some newer benchmarks like GSM8K.
- **Complexity**: Primarily focuses on grade-school level math, though with higher linguistic complexity.

## When to use it
- When evaluating the robustness of a model's mathematical reasoning against linguistic variation.
- As a complementary benchmark to [GSM8K](gsm8k.md) and [MATH](https://github.com/hendrycks/math).

## When not to use it
- When evaluating advanced collegiate-level mathematics (use MATH Benchmark instead).
- For general-purpose reasoning not focused on math.

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [GSM8K](gsm8k.md)
- [EvalPlus](evalplus.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)

## Sources / References
- [GitHub Repository](https://github.com/chiahsuan/ASDiv)
- [ACL 2020 Paper](https://aclanthology.org/2020.acl-main.92/)

## Contribution Metadata
- Last reviewed: 2026-03-30
- Confidence: high
