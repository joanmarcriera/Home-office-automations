# ASDiv (Academia Sinica Diverse MWP Dataset)

## What it is
ASDiv is a diverse corpus of 2,305 English Math Word Problems (MWPs) designed for evaluating the natural language understanding and problem-solving capabilities of AI solvers.

## What problem it solves
Many existing MWP datasets suffer from limited diversity in language patterns or problem types. ASDiv provides a broader range of text patterns and covers most problem types taught in elementary school, preventing models from over-fitting to specific phrasing.

## Where it fits in the stack
ASDiv belongs to the **Benchmarking** category, specifically focusing on mathematical reasoning and lexicon usage diversity.

## Typical use cases
- Benchmarking LLMs on elementary-level mathematical reasoning.
- Developing and testing specialized Math Word Problem solvers.
- Measuring the robustness of NLU systems against varied linguistic expressions of math problems.

## Strengths
- **High Diversity**: Features a wide range of vocabulary and sentence structures.
- **Detailed Annotation**: Each problem is annotated with its specific type and difficulty grade.
- **Lexicon Metric**: Includes a proposed metric for measuring the diversity of MWP corpora.

## Limitations
- **Scope**: Limited to elementary school mathematics.
- **Language**: Only available in English.
- **Scale**: Smaller than some newer, synthetic datasets, though more diverse.

## When to use it
Use ASDiv to verify that a model can handle varied phrasing in math problems without relying on superficial pattern matching.

## When not to use it
Do not use it for evaluating high-level mathematics (calculus, linear algebra) or for testing non-mathematical reasoning.

## Related tools / concepts
- [GSM8K](../benchmarking/gsm8k.md)
- [MATH Benchmark](https://github.com/hendrycks/math)
- [HumanEval](../benchmarking/human-eval.md)

## Sources / references
- [ASDiv GitHub Repository](https://github.com/chiahsuan/ASDiv)
- [ACL Anthology Paper](https://aclanthology.org/2020.acl-main.92.pdf)

---
**Last reviewed:** 2026-03-30
**Confidence:** high
