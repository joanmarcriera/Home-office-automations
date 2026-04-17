# MATH Benchmark

## What it is
The MATH benchmark is a dataset of 12,500 challenging competition mathematics problems. Each problem has a full step-by-step solution, which can be used to teach models to generate explanations and self-correct.

## What problem it solves
It measures a model's ability to perform complex multi-step reasoning and symbolic manipulation in mathematics, which is significantly more difficult than the elementary arithmetic found in many other datasets.

## Where it fits in the stack
**Benchmarking / Reasoning**. It specifically targets deep mathematical reasoning and formal problem-solving capabilities.

## Typical use cases
- Evaluating models on advanced mathematical tasks (Algebra, Calculus, Geometry, etc.).
- Fine-tuning models for better step-by-step reasoning.
- Testing the robustness of symbolic reasoning in LLMs.

## Strengths
- **Difficulty**: Problems range from high school to competition level (AMC 10, AMC 12, AIME).
- **Step-by-step Solutions**: Provides ground truth for reasoning chains, not just final answers.
- **Categorization**: Problems are divided into 7 subjects.

## Limitations
- **Format**: Parsing mathematical notation (LaTeX) can be a secondary challenge for models.
- **Data Contamination**: As a popular benchmark, it is at high risk of being included in pre-training corpora.

## When to use it
- To evaluate models designed for high-level reasoning and STEM tasks.
- When benchmarking the difference between simple arithmetic and deep mathematical logic.

## When not to use it
- For models intended for simple conversational or creative writing tasks.
- If you only need to evaluate basic numeracy.

## Related tools / concepts
- [GSM8K](gsm8k.md)
- [ASDiv](asdiv.md)
- [Human Eval](human-eval.md)

## Sources / References
- [Measuring Mathematical Problem Solving With the MATH Dataset (Paper)](https://arxiv.org/abs/2103.03874)
- [GitHub Repository](https://github.com/hendrycks/math)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
