# MATH Benchmark

## What it is
The MATH benchmark is a dataset of 12,500 challenging competition mathematics problems. Each problem has a step-by-step solution and a final answer formatted in LaTeX. The problems range from introductory algebra to calculus and are drawn from various high school math competitions (AMC 10, AMC 12, AIME, etc.). In June 2026, it remains a critical stress-test for the symbolic reasoning capabilities of frontier models like Claude 4.8 Opus and GPT-5.5.

## What problem it solves
Traditional math benchmarks (like GSM8K) often focus on elementary arithmetic and simple word problems. The MATH benchmark provides a much higher "ceiling" for evaluation, testing a model's ability to perform complex symbolic reasoning, multi-step proofs, and advanced problem-solving across diverse mathematical fields. It effectively differentiates models that "calculate" from those that "reason."

## Where it fits in the stack
**Benchmarking**. It is the gold standard for evaluating high-level mathematical reasoning and symbolic logic in LLMs, often used as a proxy for a model's general intelligence and planning ability.

## Typical use cases
- **Deep Reasoning Evaluation**: Testing a model's ability to solve problems that require more than just arithmetic (e.g., number theory, geometry).
- **Prompt Engineering for Logic**: Evaluating the effectiveness of Chain-of-Thought (CoT) or program-aided reasoning (PoT) on difficult tasks.
- **Model Specialized Training**: Using the MATH dataset to fine-tune models for mathematical proficiency or "System 2" reasoning.

## Strengths
- **High Difficulty**: Challenges even the most capable models, providing a clear differentiation in reasoning ability.
- **Diverse Subjects**: Includes Algebra, Counting & Probability, Geometry, Number Theory, Prealgebra, Precalculus, and Intermediate Algebra.
- **Rich Context**: Every problem includes a full step-by-step human-written solution, enabling multi-stage evaluation.
- **Symbolic Rigor**: Requires models to produce exact LaTeX-formatted answers, testing precision.

## Limitations
- **Format Sensitivity**: Models often struggle with the exact LaTeX formatting required for answers, leading to "false negatives."
- **Data Contamination**: As a widely used public dataset, there is a high risk that problems and solutions have leaked into the training data.
- **Rigid Scoring**: Standard Exact Match (EM) scoring can penalize models for mathematically correct but differently formatted answers.
- **English-Centric**: Most problems are phrased in English, which may not reflect a model's reasoning in other languages.

## When to use it
- When comparing the reasoning capabilities of "frontier" models (e.g., Claude 4.8 vs. GPT-5.5).
- When evaluating models specifically for scientific, engineering, or mathematical applications.
- To measure progress in automated theorem proving and symbolic logic.

## When not to use it
- For evaluating general conversational quality or creative writing.
- When testing basic arithmetic (use [GSM8K](gsm8k.md) instead).
- When high-throughput, low-latency performance is more important than deep reasoning.

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
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B \
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

## CLI examples
Using the LM Evaluation Harness CLI to run MATH evaluations:

```bash
# Run MATH benchmark with 5-shot prompts
python main.py --model hf --tasks math --num_fewshot 5

# Filter MATH results by subject (e.g., Geometry)
python main.py --model hf --tasks math_geometry

# Run with Chain-of-Thought (CoT) enabled
python main.py --model hf --tasks math --model_args use_cot=True

# Output results to a specific JSON file
python main.py --model hf --tasks math --output_path results_math.json
```

## API examples
Loading and processing the MATH benchmark programmatically in Python:

```python
from datasets import load_dataset
import re

def extract_boxed_answer(text):
    match = re.search(r'\\boxed{(.+?)}', text)
    return match.group(1) if match else None

# Load dataset
math_test = load_dataset("competition_math", split="test")

# Process an entry
entry = math_test[0]
print(f"Problem: {entry['problem']}")
print(f"Correct Answer: {entry['solution']}")

# Extract the target string for evaluation
target = extract_boxed_answer(entry['solution'])
print(f"Target: {target}")
```

## Technical Methodology
- **Subject Categorization**: Problems are divided into 7 subjects: Prealgebra, Algebra, Intermediate Algebra, Counting & Probability, Geometry, Number Theory, and Precalculus.
- **Difficulty Levels**: Problems are ranked from Level 1 (easiest) to Level 5 (hardest).
- **Evaluation Metric**: Typically use **Exact Match (EM)**. A model's output is parsed for the `\boxed{...}` content and compared to the ground truth.

## Challenges in Math Evaluation
- **Parsing**: LLMs often provide the correct logic but fail to format the final answer in the exact LaTeX string expected by the evaluator.
- **Symbolic Equivalence**: Identifying that `$1/2$` and `$0.5$` are equivalent requires specialized math-aware parsing logic (often using `SymPy`).
- **Chain of Thought (CoT)**: Performance on MATH is significantly higher when models are allowed to "think" or use a scratchpad before providing the final answer.

## Related tools / concepts
- [GSM8K](gsm8k.md) - Grade school math word problems.
- [ASDiv](asdiv.md) - Academic solver for diverse math word problems.
- [GPQA](gpqa.md) - Expert-level reasoning across science and math.
- [HumanEval](human-eval.md) - Coding benchmark (often correlates with math ability).
- [BigCodeBench](bigcodebench.md) - Complex coding tasks.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The standard runner for this benchmark.
- [OpenCompass](opencompass.md) - Includes MATH in its reasoning evaluation suite.
- [EvalPlus](evalplus.md) - Enhanced code generation testing.

## Sources / references
- [GitHub Repository (Hendrycks)](https://github.com/hendrycks/math)
- [MATH Dataset Paper: "Measuring Mathematical Problem Solving" (Hendrycks et al., 2021)](https://arxiv.org/abs/2103.03874)
- [Hugging Face Dataset (competition_math)](https://huggingface.co/datasets/competition_math)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
