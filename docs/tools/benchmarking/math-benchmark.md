# MATH Benchmark

## What it is
The MATH benchmark is a dataset of 12,500 challenging competition mathematics problems. Each problem has a step-by-step solution and a final answer formatted in LaTeX. In the late 2026 landscape, it remains a critical stress-test for the symbolic reasoning capabilities of frontier models like [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, and GPT-5.5, often executed via the [MCP 3.1](../automation_orchestration/mcp.md) Task Protocol for automated verification.

## What problem it solves
Traditional math benchmarks (like [GSM8K](gsm8k.md)) often focus on elementary arithmetic. The MATH benchmark provides a much higher "ceiling" for evaluation, testing a model's ability to perform complex symbolic reasoning, multi-step proofs, and advanced problem-solving across diverse mathematical fields. It is essential for differentiating models that perform simple calculation from those capable of "System 2" reasoning.

## Where it fits in the stack
**Benchmarking**. It is the gold standard for evaluating high-level mathematical reasoning and symbolic logic, frequently used to validate the reasoning modules of [autonomous agents](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## Typical use cases
- **Deep Reasoning Evaluation**: Testing a model's ability to solve problems in number theory, geometry, and intermediate algebra.
- **Prompt Engineering for Logic**: Evaluating the effectiveness of Chain-of-Thought (CoT) or program-aided reasoning (PoT) on difficult tasks.
- **Model Specialized Training**: Using the MATH dataset to fine-tune models for mathematical proficiency or scientific reasoning.
- **Automated Verification**: Using the [MCP 3.1](../automation_orchestration/mcp.md) Task Protocol to automate the solving and checking of competition-level problems.

## Strengths
- **High Difficulty**: Challenges even the most capable models, providing a clear differentiation in reasoning ability.
- **Diverse Subjects**: Includes Algebra, Counting & Probability, Geometry, Number Theory, Prealgebra, Precalculus, and Intermediate Algebra.
- **Rich Context**: Every problem includes a full step-by-step human-written solution.
- **Symbolic Rigor**: Requires exact LaTeX-formatted answers, testing model precision and formatting adherence.

## Limitations
- **Format Sensitivity**: Models often provide correct logic but fail the exact LaTeX formatting required for "Exact Match" scoring.
- **Data Contamination**: As a widely used public dataset, there is a high risk that problems have leaked into the training data of newer models.
- **Rigid Scoring**: Standard Exact Match (EM) scoring can penalize mathematically correct but differently formatted answers.
- **Parsing Challenges**: Identifying symbolic equivalence (e.g., `$1/2$` vs `$0.5$`) requires specialized math-aware logic like `SymPy`.

## When to use it
- When comparing the reasoning capabilities of "frontier" models (e.g., [Gemma 3](../ai_knowledge/local_llms.md) vs. Claude 5.1 or GPT-5.5).
- When evaluating models specifically for scientific, engineering, or mathematical applications.
- To measure progress in automated theorem proving and symbolic logic.

## When not to use it
- For evaluating general conversational quality or creative writing.
- When testing basic arithmetic (use [GSM8K](gsm8k.md) or [ASDiv](asdiv.md) instead).
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
# Evaluate a Gemma 3 model on the MATH benchmark
python main.py \
    --model hf \
    --model_args pretrained=google/gemma-3-27b-it \
    --tasks math \
    --device cuda:0
```

### 3. Manual Verification (Example Problem)
```text
Problem: Let f(x) = x^2 + 2x + 1. Find f(3).
Answer: \boxed{16}
Solution: Substituting x = 3 into the expression, we get 3^2 + 2(3) + 1 = 9 + 6 + 1 = 16.
```

## CLI examples
Using the [LM Evaluation Harness](lm-evaluation-harness.md) CLI to run MATH evaluations:

```bash
# Run MATH benchmark with 5-shot prompts
python main.py --model hf --tasks math --num_fewshot 5

# Filter MATH results by subject (e.g., Geometry)
python main.py --model hf --tasks math_geometry

# Run with Chain-of-Thought (CoT) enabled (Recommended for Gemma 3 and Claude 5.1)
python main.py --model hf --tasks math --model_args use_cot=True

# Output results to a specific JSON file for MCP 3.1 ingestion
python main.py --model hf --tasks math --output_path results_math.json
```

## API examples
Loading, processing, and parsing the MATH benchmark in Python. This December 2026 update leverages strict **Pydantic v2** validation to model problems and structure LaTeX verification results.

```python
from pydantic import BaseModel, Field, condecimal
from typing import Optional, List
import re

# Model the math problem structure using Pydantic v2
class MathProblem(BaseModel):
    problem_id: str
    subject: str = Field(..., pattern="^(Algebra|Geometry|Number Theory|Counting & Probability|Precalculus|Prealgebra|Intermediate Algebra)$")
    question_text: str = Field(..., min_length=15)
    latex_solution: str
    correct_boxed_answer: str

# Model evaluation verification report
class MathVerifyReport(BaseModel):
    problem_id: str
    extracted_model_answer: Optional[str]
    target_answer: str
    is_exact_match: bool
    evaluation_time_sec: condecimal(gt=0)

# Helper to isolate latex boxed answer
def extract_boxed_answer(text: str) -> Optional[str]:
    match = re.search(r'\\boxed{(.+?)}', text)
    return match.group(1) if match else None

# Verifier function using the schemas
def verify_math_submission(prob_data: dict, model_ans_raw: str) -> MathVerifyReport:
    problem = MathProblem.model_validate(prob_data)
    extracted_ans = extract_boxed_answer(model_ans_raw)
    is_match = (extracted_ans == problem.correct_boxed_answer)

    report = MathVerifyReport(
        problem_id=problem.problem_id,
        extracted_model_answer=extracted_ans,
        target_answer=problem.correct_boxed_answer,
        is_exact_match=is_match,
        evaluation_time_sec=1.45
    )
    print(f"Verified problem {report.problem_id}. Match result: {report.is_exact_match}")
    return report

# Mock problem data
problem_source = {
    "problem_id": "math_alg_001",
    "subject": "Algebra",
    "question_text": "Let $f(x) = x^2 + 2x + 1$. Find the value of $f(3)$.",
    "latex_solution": "Substituting $x = 3$, we have $3^2 + 2(3) + 1 = 9 + 6 + 1 = 16$.",
    "correct_boxed_answer": "16"
}

# Verified against mock output from Llama 4
llama_submission = "The value substitutions lead to \\boxed{16} as the final evaluation."
report = verify_math_submission(problem_source, llama_submission)
```

## Related tools / concepts
- [GSM8K](gsm8k.md) - Grade school math word problems.
- [ASDiv](asdiv.md) - Academic solver for diverse math word problems.
- [GPQA](gpqa.md) - Expert-level reasoning across science and math.
- [HumanEval](human-eval.md) - Coding benchmark (often correlates with math ability).
- [BigCodeBench](bigcodebench.md) - Complex coding tasks.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The standard runner for this benchmark.
- [OpenCompass](opencompass.md) - Includes MATH in its reasoning evaluation suite.
- [MCP 3.1](../automation_orchestration/mcp.md) - Protocol for automated task execution and verification.
- [SharpAI Security Benchmark](sharp-ai.md) - Evaluation suite for security robustness and red-teaming.

## Sources / references
- [GitHub Repository (Hendrycks)](https://github.com/hendrycks/math)
- [MATH Dataset Paper: "Measuring Mathematical Problem Solving" (Hendrycks et al., 2021)](https://arxiv.org/abs/2103.03874)
- [Hugging Face Dataset (competition_math)](https://huggingface.co/datasets/competition_math)
- [Gemma 3 Technical Report](https://storage.googleapis.com/deepmind-media/gemma/gemma-3-report.pdf)

## Contribution Metadata
- Last reviewed: 2026-12-19
- Confidence: high
