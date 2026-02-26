# GSM8K (Grade School Math 8K)

## What it is
GSM8K is a benchmark for evaluating the multi-step mathematical reasoning capabilities of LLMs. It contains 8.5K high-quality grade school math word problems that require 2 to 8 steps of basic arithmetic to solve. The key metric is Exact Match (EM), measuring the accuracy of the final numerical answer.

## What problem it solves
Provides a standardized way to measure whether LLMs can perform multi-step arithmetic reasoning, a fundamental capability for practical mathematical tasks.

## Where it fits in the stack
**Benchmarking**. Serves as a widely used reference for evaluating mathematical reasoning in LLMs.

## Typical use cases
- Evaluating LLM arithmetic and multi-step reasoning capabilities
- Measuring the impact of prompting strategies (e.g., Chain-of-Thought) on math performance
- Comparing models on fundamental mathematical problem-solving

## Strengths
- Large dataset (8.5K problems) provides statistically meaningful results
- Problems are well-defined with unambiguous numerical answers
- Widely adopted, enabling cross-model comparisons

## Limitations
- Limited to grade-school-level math; does not test advanced mathematics
- Problems are relatively formulaic compared to real-world math applications
- Exact Match scoring does not give partial credit for correct reasoning with minor errors

## When to use it
- When comparing LLMs on basic mathematical reasoning
- When evaluating the effect of different prompting techniques on math performance

## When not to use it
- When you need to evaluate advanced mathematical reasoning (use MATH Benchmark instead)
- When testing non-mathematical capabilities

## Related tools / concepts
- [MATH Benchmark](https://github.com/hendrycks/math)
- [ASDiv](https://github.com/chiahsuan/ASDiv)

## Sources / references
- [GitHub Repository](https://github.com/openai/grade-school-math)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
