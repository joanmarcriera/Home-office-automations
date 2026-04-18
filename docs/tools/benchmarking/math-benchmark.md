# MATH Benchmark

## What it is
The MATH benchmark is a dataset of 12,500 challenging competition mathematics problems. Each problem has a step-by-step solution and a final answer formatted in LaTeX. The problems range from introductory algebra to calculus and are drawn from various high school math competitions.

## What problem it solves
Traditional math benchmarks (like GSM8K) often focus on elementary arithmetic and simple word problems. The MATH benchmark provides a much higher "ceiling" for evaluation, testing a model's ability to perform complex symbolic reasoning, multi-step proofs, and advanced problem-solving across diverse mathematical fields.

## Where it fits in the stack
**Benchmarking**. It is the gold standard for evaluating high-level mathematical reasoning and symbolic logic in LLMs.

## Typical use cases
- **Deep Reasoning Evaluation**: Testing a model's ability to solve problems that require more than just arithmetic (e.g., number theory, geometry).
- **Prompt Engineering for Logic**: Evaluating the effectiveness of Chain-of-Thought (CoT) or program-aided reasoning on difficult tasks.
- **Model Specialized Training**: Using the MATH dataset (or the associated AMPS pretraining dataset) to fine-tune models for mathematical proficiency.

## Strengths
- **High Difficulty**: Challenges even the most capable models, providing a clear differentiation in reasoning ability.
- **Diverse Subjects**: Includes Algebra, Counting & Probability, Geometry, Number Theory, Prealgebra, Precalculus, and Intermediate Algebra.
- **Rich Context**: Every problem includes a full step-by-step human-written solution, not just the final answer.

## Limitations
- **Format Sensitivity**: Models often struggle with the LaTeX formatting required for answers.
- **Data Contamination**: As a widely used public dataset, there is a high risk that problems and solutions have leaked into the training data of newer models.
- **Rigid Scoring**: Typically uses Exact Match (EM) for the final LaTeX string, which can penalize models for mathematically correct but differently formatted answers.

## When to use it
- When comparing the reasoning capabilities of "frontier" models.
- When evaluating models specifically for scientific or mathematical applications.

## When not to use it
- For evaluating general conversational quality or creative writing.
- When testing basic arithmetic (use [GSM8K](gsm8k.md) instead).

## Related tools / concepts
- [GSM8K](gsm8k.md)
- [ASDiv](asdiv.md)
- [GPQA](gpqa.md)
- [HumanEval](human-eval.md)

## Sources / references
- [GitHub Repository](https://github.com/hendrycks/math)
- [MATH Dataset Paper: "Measuring Mathematical Problem Solving" (Hendrycks et al., 2021)](https://arxiv.org/abs/2103.03874)
- [Hugging Face Dataset](https://huggingface.co/datasets/competition_math)

## Contribution Metadata
- Last reviewed: 2026-04-08
- Confidence: high
