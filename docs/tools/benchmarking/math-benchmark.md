# MATH Benchmark

## What it is
The MATH benchmark is a dataset of 12,500 challenging competition mathematics problems. Each problem has a step-by-step solution and a final answer formatted in LaTeX. The problems range from introductory algebra to calculus and are drawn from various high school math competitions (AMC 10, AMC 12, AIME, etc.).

## What problem it solves
Traditional math benchmarks (like GSM8K) often focus on elementary arithmetic and simple word problems. The MATH benchmark provides a much higher "ceiling" for evaluation, testing a model's ability to perform complex symbolic reasoning, multi-step proofs, and advanced problem-solving across diverse mathematical fields.

## Where it fits in the stack
**Benchmarking**. It is the gold standard for evaluating high-level mathematical reasoning and symbolic logic in LLMs.

## Typical use cases
- **Deep Reasoning Evaluation**: Testing a model's ability to solve problems that require more than just arithmetic (e.g., number theory, geometry).
- **Prompt Engineering for Logic**: Evaluating the effectiveness of Chain-of-Thought (CoT) or program-aided reasoning on difficult tasks.
- **Model Specialized Training**: Using the MATH dataset (or the associated AMPS pretraining dataset) to fine-tune models for mathematical proficiency.

## Getting started

### 1. Accessing the Data
The dataset is available on Hugging Face and can be loaded easily using the `datasets` library.

```python
from datasets import load_dataset

# Load the competition math dataset
dataset = load_dataset("competition_math")
print(dataset['test'][0])
```

### 2. Evaluating with LM Evaluation Harness
The easiest way to run the MATH benchmark is using the [LM Evaluation Harness](lm-evaluation-harness.md).

```bash
# Evaluate a model on the MATH benchmark
python main.py \
    --model hf \
    --model_args pretrained=meta-llama/Llama-3-8B \
    --tasks math \
    --device cuda:0 \
    --batch_size 8
```

### 3. Manual Verification (Example Problem)
```text
Problem: Let f(x) = x^2 + 2x + 1. Find f(3).
Answer: \boxed{16}
Solution: Substituting x = 3 into the expression, we get 3^2 + 2(3) + 1 = 9 + 6 + 1 = 16.
```

## Technical Methodology
- **Subject Categorization**: Problems are divided into 7 subjects: Prealgebra, Algebra, Intermediate Algebra, Counting & Probability, Geometry, Number Theory, and Precalculus.
- **Difficulty Levels**: Problems are ranked from Level 1 (easiest) to Level 5 (hardest).
- **Evaluation Metric**: Typically use **Exact Match (EM)**. A model's output is parsed for the `\boxed{...}` content and compared to the ground truth.

## Challenges in Math Evaluation
- **Parsing**: LLMs often provide the correct logic but fail to format the final answer in the exact LaTeX string expected by the evaluator.
- **Symbolic Equivalence**: Identifying that `$1/2$` and `$0.5$` are equivalent requires specialized math-aware parsing logic (often using `SymPy`).
- **Chain of Thought (CoT)**: Performance on MATH is significantly higher when models are allowed to "think" or use a scratchpad before providing the final answer.

## Strengths
- **High Difficulty**: Challenges even the most capable models, providing a clear differentiation in reasoning ability.
- **Diverse Subjects**: Includes Algebra, Counting & Probability, Geometry, Number Theory, Prealgebra, Precalculus, and Intermediate Algebra.
- **Rich Context**: Every problem includes a full step-by-step human-written solution, not just the final answer.

## Limitations
- **Format Sensitivity**: Models often struggle with the LaTeX formatting required for answers.
- **Data Contamination**: As a widely used public dataset, there is a high risk that problems and solutions have leaked into the training data of newer models.
- **Rigid Scoring**: Standard EM scoring can penalize models for mathematically correct but differently formatted answers.

## When to use it
- When comparing the reasoning capabilities of "frontier" models.
- When evaluating models specifically for scientific, engineering, or mathematical applications.

## When not to use it
- For evaluating general conversational quality or creative writing.
- When testing basic arithmetic (use [GSM8K](gsm8k.md) instead).

## Related tools / concepts
- [GSM8K](gsm8k.md) - Grade school math word problems.
- [ASDiv](asdiv.md) - Academic solver for diverse math word problems.
- [GPQA](gpqa.md) - Expert-level reasoning across science and math.
- [HumanEval](human-eval.md) - Coding benchmark (often correlates with math ability).
- [BigCodeBench](bigcodebench.md) - Complex coding tasks.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The standard runner for this benchmark.
- [OpenCompass](opencompass.md) - Includes MATH in its reasoning evaluation suite.

## Sources / references
- [GitHub Repository](https://github.com/hendrycks/math)
- [MATH Dataset Paper: "Measuring Mathematical Problem Solving" (Hendrycks et al., 2021)](https://arxiv.org/abs/2103.03874)
- [Hugging Face Dataset](https://huggingface.co/datasets/competition_math)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
