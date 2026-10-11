# MATH Benchmark

## What it is
The **MATH Benchmark** (Hendrycks et al.) is a premier dataset of 12,500 challenging competition-level mathematics problems across seven subdisciplines (Algebra, Counting & Probability, Geometry, Intermediate Algebra, Number Theory, Prealgebra, and Precalculus). Each problem features a detailed, step-by-step human proof solution and a canonical LaTeX `\boxed{...}` answer. In the 2027 evaluation landscape, the MATH benchmark serves as a primary stress-test for advanced "System 2" symbolic reasoning, Chain-of-Thought (CoT) trajectory consistency, and automated theorem-proving in frontier models (Claude 3.7 Sonnet, GPT-4.5, Llama 4, Gemma 3, DeepSeek-R1) via standard **FastMCP 3.1** benchmarking pipelines.

## What problem it solves
Elementary math benchmarks (such as [GSM8K](gsm8k.md) or [SVAMP](svamp.md)) focus on multi-step arithmetic word problems that lack ceiling height for evaluating advanced reasoning. GSM8K scores for frontier models often saturate near 95%+, rendering it incapable of differentiating superior reasoning architectures.

The MATH benchmark solves the evaluation saturation problem by presenting high-school competition problems (AMC 10, AMC 12, AIME) that require multi-stage symbolic derivations, geometric spatial transformations, modulo arithmetic proofs, and rigorous formula simplification.

## Evaluation Pipeline Architecture

```
+-----------------------------------------------------------------------------------+
|                        MATH Competition Problem Repository                        |
|        (12,500 AMC 10/12 & AIME Problems across 7 Mathematical Fields)           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       FastMCP 3.1 Automated Benchmarking Runner                   |
|  +-------------------------------------+     +---------------------------------+  |
|  | CoT / Program-Aided Prompt Engine   |     | Temperature / Seed Normalizer   |  |
|  +-------------------------------------+     +---------------------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Target Model Reasoning Execution                           |
|        (Claude 3.7 Sonnet, GPT-4.5, Llama 4 70B CoT, DeepSeek-R1)                |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     LaTeX Regex Extraction & SymPy Canonicalization               |
|  - Isolate \boxed{...} Expressions                                                |
|  - SymPy Equivalence Check (e.g., \frac{1}{\sqrt{2}} == \frac{\sqrt{2}}{2})        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Pydantic v2 MathVerifyReport Engine                        |
|       (Exact Match % / Symbolic Equivalence % / Subject Breakdown Scorecard)      |
+-----------------------------------------------------------------------------------+
```

## Comparison Matrix

| Metric / Feature | MATH Benchmark | GSM8K | GPQA | SVAMP |
| :--- | :--- | :--- | :--- | :--- |
| **Target Level** | High School Competition (AMC/AIME) | Grade School Word Math | Graduate-Level Biology/Physics/Math | Elementary Arithmetic |
| **Problem Count** | 12,500 | 8,500 | 448 | 1,000 |
| **Answer Format** | LaTeX `\boxed{...}` Symbolic | Short Numeric Integer | Multiple Choice (A/B/C/D) | Short Numeric Value |
| **Evaluation Type** | SymPy Equivalence / Regex | Regex Integer Match | Exact Choice Match | Regex Numeric Match |
| **Reasoning Ceiling** | Very High (System 2 CoT) | Moderate | Extremely High (Domain Graduate) | Low to Moderate |
| **Primary Failure Mode**| LaTeX Formatting / Symbol Mismatch | Calculation Errors | Misleading Distractor Choices | Variable Misinterpretation |

## Where it fits in the stack
**Category**: Benchmarking / Symbolic Reasoning Evaluation.

The MATH benchmark sits in the **model evaluation and quality assurance layer**, providing standardized accuracy metrics that inform model selection for reasoning agents (`docs/tools/agents/`) and data copilot systems (`docs/reference-implementations/data-copilot/`).

## Typical use cases
- **Frontier Model Reasoning Benchmarking**: Evaluating System 2 multi-step reasoning capabilities across open-weights and commercial frontier LLMs.
- **Program-Aided Language (PAL) Evaluation**: Measuring accuracy improvements when models are allowed to write and execute Python scripts (`SymPy`, `NumPy`) during problem solving.
- **Chain-of-Thought (CoT) Prompt Tuning**: Testing whether zero-shot CoT, few-shot CoT, or tree-of-thought search strategies yield higher LaTeX extraction scores.
- **Fine-Tuning Dataset Verification**: Utilizing the MATH train set (7,500 problems) to train mathematical specialization adapters via [Axolotl](../frameworks/axolotl.md) or [LLaMA-Factory](../frameworks/llama-factory.md).

## Strengths
- **Substantial Reasoning Ceiling**: Uncontaminated competition problems prevent artificial benchmark score inflation.
- **Multi-Disciplinary Coverage**: Comprehensive coverage across 7 foundational subdisciplines prevents over-fitting to basic algebra.
- **Step-by-Step Proof Ground Truth**: Includes full human latex derivations for training reflection and process-reward models (PRMs).
- **Symbolic Rigor**: Forces models to produce rigorous, unambiguously formatted LaTeX outputs.

## Limitations
- **Formatting Rigidness**: Models may derive the correct numerical result but fail exact match evaluation due to formatting variances (e.g., `\frac{1}{2}` vs `0.5`).
- **Data Contamination Exposure**: Extensive public usage requires contamination audits for recently trained open-weights models.
- **SymPy Parsing Overhead**: Testing symbolic equivalence for complex algebraic expressions requires compute-heavy SymPy simplification.

## When to use it
- When evaluating frontier reasoning models or mathematical fine-tunes.
- When benchmarking code-augmented reasoning engines that leverage Python execution environments.
- To compare reasoning models on complex symbolic logic and proof generation.

## When not to use it
- When evaluating simple numerical extraction or conversational instruction following.
- When minimal latency and low token usage are mandatory during evaluation.

## Getting started

### 1. Load Dataset via Hugging Face `datasets`
```python
from datasets import load_dataset

math_dataset = load_dataset("competition_math")
sample = math_dataset["test"][0]
print(f"Problem: {sample['problem']}")
print(f"Solution: {sample['solution']}")
```

### 2. Run Evaluation with LM Evaluation Harness
```bash
python -m lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-3.3-70B-Instruct \
    --tasks math \
    --device cuda:0 \
    --batch_size 8
```

## CLI examples

### 1. Evaluate Competition Math with 5-Shot CoT
```bash
lm-eval --model hf --model_args pretrained=Qwen/Qwen2.5-Math-72B-Instruct --tasks math --num_fewshot 5
```

### 2. Filter Evaluation to Number Theory Subfield
```bash
lm-eval --model hf --model_args pretrained=deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --tasks math_number_theory
```

### 3. Save Evaluation Output JSON for FastMCP Processing
```bash
lm-eval --model hf --tasks math --output_path ./reports/math_eval_results.json
```

## API examples

### FastMCP 3.1 MATH Solution Verification Server with SymPy (Python)
This complete FastMCP 3.1 service extracts LaTeX boxed answers, verifies symbolic equivalence using SymPy, and returns structured Pydantic v2 evaluation reports.

```python
import json
import re
from typing import Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
import sympy as sp

# Initialize FastMCP 3.1 Server
mcp = FastMCP("math-benchmark-evaluator")

class MathProblemSubmission(BaseModel):
    problem_id: str = Field(..., min_length=3)
    subject: str = Field(..., pattern="^(Algebra|Geometry|Number Theory|Counting & Probability|Precalculus|Prealgebra|Intermediate Algebra)$")
    question_text: str = Field(..., min_length=10)
    target_boxed_answer: str = Field(..., min_length=1)
    model_output_raw: str = Field(..., min_length=1)

class EvaluationReport(BaseModel):
    problem_id: str
    extracted_answer: Optional[str]
    target_answer: str
    is_exact_match: bool
    is_symbolic_match: bool

def extract_boxed(text: str) -> Optional[str]:
    match = re.search(r"\\boxed\{([^{}]+)\}", text)
    if match:
        return match.group(1).strip()
    return None

def check_symbolic_equivalence(target: str, predicted: str) -> bool:
    try:
        expr_target = sp.sympify(target.replace("\\frac", "").replace("{", "(").replace("}", ")"))
        expr_pred = sp.sympify(predicted.replace("\\frac", "").replace("{", "(").replace("}", ")"))
        return sp.simplify(expr_target - expr_pred) == 0
    except Exception:
        return target.strip() == predicted.strip()

@mcp.tool()
def verify_math_problem(payload_json: str) -> str:
    """Verifies a model solution against ground truth competition MATH boxed answer.

    Args:
        payload_json: JSON string matching MathProblemSubmission schema.
    """
    try:
        data = json.loads(payload_json)
        sub = MathProblemSubmission.model_validate(data)

        extracted = extract_boxed(sub.model_output_raw)
        if not extracted:
            report = EvaluationReport(
                problem_id=sub.problem_id,
                extracted_answer=None,
                target_answer=sub.target_boxed_answer,
                is_exact_match=False,
                is_symbolic_match=False
            )
            return json.dumps(report.model_dump(), indent=2)

        exact_match = (extracted == sub.target_boxed_answer)
        symbolic_match = exact_match or check_symbolic_equivalence(sub.target_boxed_answer, extracted)

        report = EvaluationReport(
            problem_id=sub.problem_id,
            extracted_answer=extracted,
            target_answer=sub.target_boxed_answer,
            is_exact_match=exact_match,
            is_symbolic_match=symbolic_match
        )
        return json.dumps(report.model_dump(), indent=2)

    except Exception as e:
        return json.dumps({"status": "ERROR", "error": str(e)})

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Failure Diagnostics

### 1. Handling LaTeX Substring Parsing Errors
Models frequently output nested LaTeX brackets like `\boxed{\frac{1}{2}}`. Standard non-greedy regex (`\\boxed\{(.+?)\}`) can fail on closing braces. Implement a recursive brace-counting stack parser in production to reliably isolate the outer `\boxed{}` content.

### 2. Mitigating Contamination with Transformed Problems
To detect model memorization, run parallel evaluation sets where variables and numerical constants are systematically perturbed using automated SymPy transformation scripts while preserving problem structure.

### 3. Temperature & Sampling Settings
When evaluating reasoning models on competition MATH, set `temperature=0.0` for deterministic zero-shot baseline benchmarks, or `temperature=0.7` with Majority Voting (pass@k, k=32) for deep CoT reasoning evaluations.

## Related tools / concepts
- [GSM8K](gsm8k.md) — Grade school arithmetic math benchmark.
- [GPQA](gpqa.md) — Graduate-level reasoning evaluation across STEM fields.
- [LM Evaluation Harness](lm-evaluation-harness.md) — Canonical framework for running LLM benchmarks.
- [OpenCompass](opencompass.md) — Multi-dimensional model evaluation framework.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for automated tool execution and verification.

## Sources / references
- [MATH Dataset Paper (Hendrycks et al., 2021)](https://arxiv.org/abs/2103.03874)
- [MATH Benchmark GitHub Repository](https://github.com/hendrycks/math)
- [Hugging Face Competition Math Dataset](https://huggingface.co/datasets/competition_math)
- [LM Evaluation Harness Documentation](https://github.com/EleutherAI/lm-evaluation-harness)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
