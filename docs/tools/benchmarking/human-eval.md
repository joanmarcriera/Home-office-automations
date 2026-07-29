# HumanEval

## What it is
HumanEval is a benchmark released by OpenAI to evaluate the code generation capabilities of Large Language Models. It consists of 164 handwritten programming problems, each including a function signature, docstring, body, and several unit tests. As of late October / November 2026, it remains a foundational metric for assessing the core algorithmic reasoning of models like **Claude 5.1** and **GPT-5.5**.

## What problem it solves
Provides a standardized, non-contaminated measure of whether LLMs can generate functionally correct code from natural language descriptions. Since the problems were handwritten, it provides a cleaner evaluation of zero-shot coding ability than benchmarks derived from public repositories which may have been seen during training.

## Where it fits in the stack
**Benchmarking**. Used as a primary reference benchmark for code generation and algorithmic reasoning capabilities of LLMs.

## Typical use cases
- Evaluating LLM code generation accuracy on self-contained programming tasks.
- Comparing models on their ability to produce correct Python code.
- Measuring improvements in code generation across model versions or fine-tuning runs.
- Assessing the "coding intelligence" of frontier reasoning models.

## Strengths
- **Well-Established**: Widely cited and used as an industry standard.
- **Automated Validation**: Problems include clear unit tests for functional correctness.
- **Pass@k Metric**: Accounts for sampling variability and model creativity.
- **Zero-Shot Focus**: Designed to test raw logic rather than library-specific knowledge.

## Limitations
- **Small Scale**: Only 164 problems, which may not cover modern software complexity.
- **Python-Centric**: Primarily focuses on Python and basic algorithmic tasks.
- **Limited Realism**: Does not test debugging, refactoring, or multi-file engineering (use [SWE-bench](swe-bench.md) for this).
- **Contamination Risk**: Due to its popularity, newer models may have inadvertently included it in training data.

## When to use it
- When comparing frontier LLMs on their ability to generate correct code from specifications.
- When evaluating a model for "coding assistant" use cases.
- As a fast, automated check for coding regression in model pipelines.

## When not to use it
- When you need to evaluate real-world software engineering capability (use [SWE-bench](swe-bench.md) instead).
- When you need multilingual code generation evaluation (use MultiPL-E instead).
- For evaluating complex system design or library-specific knowledge.

## Getting started

HumanEval can be run using the official OpenAI execution environment or through broader harnesses like the LM Evaluation Harness.

1. Clone the HumanEval repository or use `lm-eval`.
2. Install dependencies: `pip install human-eval`
3. Run the evaluation script (warning: this executes model-generated code in a sandbox).

## CLI examples

### 1. Running HumanEval via LM Evaluation Harness
Evaluate a local model's coding performance with required code execution permission:

```bash
python -m lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4 \
    --tasks humaneval \
    --device cuda:0 \
    --allow_code_execution
```

### 2. Evaluating Samples with OpenAI's Tool
If you have a file of generated samples (`samples.jsonl`), run the official evaluator:

```bash
python evaluate_functional_correctness.py samples.jsonl
```

### 3. Generating Samples with Aider
Use [Aider](../development_ops/aider.md) to generate solutions for a specific HumanEval problem:
```bash
aider --message "Solve HumanEval problem 0 in Python"
```

## API examples

### 1. Python: Calculating Pass@k
A utility snippet to calculate the Pass@k metric manually:

```python
import math

def calculate_pass_at_k(n: int, c: int, k: int) -> float:
    """
    n: total samples
    c: number of correct samples
    k: k in pass@k
    """
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)

# Example: 100 samples, 40 correct, Pass@1
print(f"Pass@1: {calculate_pass_at_k(100, 40, 1):.2%}")
```

### 2. Python: Programmatic Parsing and Validation with Pydantic v2
Validate generated Python code artifacts and unit test suites using modern Pydantic v2 specifications with strict type-hints:

```python
import json
from typing import List
from pydantic import BaseModel, Field, TypeAdapter

class CodingTaskSolution(BaseModel):
    function_name: str = Field(..., description="The name of the target Python function.")
    implementation: str = Field(..., description="The full, runnable Python implementation code block.")
    unit_tests: List[str] = Field(..., description="A list of assert statements used for testing.")
    is_sandboxed_exec_allowed: bool = Field(default=True, description="Whether sandboxed code execution is permitted.")

# Simulated model JSON output response
raw_response: str = """{
  "function_name": "calculate_pass_at_k",
  "implementation": "def calculate_pass_at_k(n, c, k):\\n    import math\\n    if n - c < k:\\n        return 1.0\\n    return 1.0 - math.comb(n - c, k) / math.comb(n, k)",
  "unit_tests": [
    "assert calculate_pass_at_k(100, 40, 1) == 0.4",
    "assert calculate_pass_at_k(100, 100, 5) == 1.0"
  ],
  "is_sandboxed_exec_allowed": true
}"""

# Use Pydantic v2 TypeAdapter for validation
adapter: TypeAdapter[CodingTaskSolution] = TypeAdapter(CodingTaskSolution)
solution: CodingTaskSolution = adapter.validate_json(raw_response)

print(f"Validated function name: {solution.function_name}")
assert "calculate_pass_at_k" in solution.implementation
```

### 3. Performance Comparison (November 2026 SOTA)
| Model | HumanEval Pass@1 (%) | Notes |
| :--- | :--- | :--- |
| **Claude 5.1 Opus** | 98.4% | SOTA Coding Reasoning (October 2026) |
| **GPT-5.5** | 97.6% | SOTA algorithmic density |
| **Gemini 4.0 Ultra** | 96.9% | Strong multi-lingual capabilities |
| **Qwen 3.6 Instruct** | 94.8% | Best-in-class Chinese-open model |
| **Gemma 3 27B** | 93.1% | Outstanding small open-weights model |
| **Llama 4** | 92.5% | Industry baseline for local reasoning |
| Claude 3.5 Sonnet | 92.0% | Released June 2024 |
| GPT-4o | 90.2% | Released May 2024 |

## Related tools / concepts
- [MBPP (Mostly Basic Python Problems)](mbpp.md)
- [BigCodeBench](bigcodebench.md)
- [SWE-bench](swe-bench.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [Aider](../development_ops/aider.md)
- [Cursor](../development_ops/cursor.md)
- [Claude Code](../development_ops/claude-code.md)
- [PydanticAI](../frameworks/pydantic-ai.md)

## Sources / references
- [OpenAI HumanEval GitHub](https://github.com/openai/human-eval)
- [Hugging Face HumanEval Dataset](https://huggingface.co/datasets/openai/humaneval)
- [Arxiv: Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
