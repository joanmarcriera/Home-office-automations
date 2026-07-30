# EvalPlus

## What it is
EvalPlus is a rigorous evaluation framework for Large Language Models (LLMs) focused on code generation (LLM4Code). It significantly expands existing benchmarks like HumanEval and MBPP with more comprehensive test cases to improve evaluation accuracy. As of November 2026, it is the industry standard for verifying the coding robustness of frontier models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0**.

## What problem it solves
Original coding benchmarks like [HumanEval](human-eval.md) often have very few test cases, allowing fragile or incorrect code to pass. EvalPlus addresses this "under-testing" problem by adding 80x more tests to HumanEval and 35x more tests to MBPP, revealing model weaknesses that simpler benchmarks miss.

## Where it fits in the stack
**Benchmarking**. It is a specialized tool for deeply evaluating the code generation capabilities and efficiency of LLMs. It sits between basic algorithmic benchmarks and full agentic benchmarks like [SWE-bench](swe-bench.md).

## Typical use cases
- **Rigorous Coding Evaluation**: Testing a model's true coding ability beyond simple benchmarks.
- **Fragility Detection**: Identifying if a model's generated code is robust across many different inputs.
- **Code Efficiency Benchmarking**: Using the EvalPerf extension to measure the execution speed of LLM-generated code.
- **Frontier Model Verification**: Confirming the coding reliability of Claude 5.1, GPT-5.5, and Gemini 4.0.

## Strengths
- **High Rigor**: Expanded test suites (HumanEval+, MBPP+) significantly reduce false positives.
- **Multi-backend Support**: Supports evaluation via vLLM, Hugging Face, OpenAI, Anthropic, Gemini, and Ollama.
- **Security**: Supports safe code execution within Docker containers to protect the host system.
- **Performance Evaluation**: Includes EvalPerf for measuring code efficiency.
- **MCP 3.1 Integration**: Supports [MCP 3.1](../../tools/automation_orchestration/mcp.md) for automated benchmarking workflows and the Task Protocol.

## Limitations
- **Focus**: Primarily limited to Python and coding-specific tasks.
- **Execution Cost**: Running 80x more tests naturally takes more time and compute than the original benchmarks.
- **Language Coverage**: While expanding, its primary strength remains in the Python ecosystem.

## When to use it
- When you are developing or fine-tuning an LLM for code generation and need high-confidence metrics.
- When you want to rank models based on their coding robustness and efficiency.
- When comparing against major industry models (many of which, like Llama 4 and Qwen 3.6, use EvalPlus).

## When not to use it
- For general knowledge or reasoning tasks (use [MMLU](mmlu.md) or [GPQA](gpqa.md) instead).
- For quick, non-rigorous evaluations of simple code snippets.

## Getting started

### Installation
You can install EvalPlus via pip. For full functionality including vLLM and performance benchmarking:

```bash
pip install "evalplus[vllm,perf]" --upgrade
```

### Setup
Ensure Docker is installed if you intend to run evaluations in a sandboxed environment (highly recommended).

```bash
# Verify installation
evalplus.evaluate --help
```

## CLI examples

### Functional Evaluation (vLLM)
To evaluate a model locally using the vLLM backend on the HumanEval dataset:

```bash
evalplus.evaluate --model "meta-llama/Llama-4-Maverick-8B" \
                  --dataset humaneval \
                  --backend vllm \
                  --greedy
```

### Docker Execution (Safe Sandboxing)
For security, it is highly recommended to run the evaluation inside a Docker container:

```bash
# Generate samples locally first
evalplus.codegen --model "anthropic/claude-5-1-sonnet-20261022" --dataset humaneval --backend anthropic

# Run evaluation inside the EvalPlus sandbox
docker run --rm -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval \
           --samples /app/humaneval/anthropic--claude-5-1-sonnet-20261022_temp_0.0.jsonl
```

## API examples

EvalPlus provides a Python API for programmatic access to datasets and evaluation utilities:

```python
from evalplus.data import get_human_eval_plus, get_mbpp_plus

# Load the enhanced HumanEval dataset
human_eval_plus = get_human_eval_plus()
first_task = human_eval_plus['HumanEval/0']

print(f"Task ID: {first_task['task_id']}")
print(f"Prompt: {first_task['prompt']}")
print(f"Number of Test Cases: {len(first_task['test_setup'])}")
```

### Custom Inference Example
```python
# samples = []
# for task_id, task in human_eval_plus.items():
#     code = my_model.generate(task['prompt'])
#     samples.append({"task_id": task_id, "solution": code})
# save_jsonl(samples, "my_model_samples.jsonl")
```

### Programmatic Generated Solution Verification using Pydantic v2
This Python script validates LLM-generated code solution items and the corresponding test-pass telemetry using **Pydantic v2**:

```python
import json
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ValidationError, field_validator

class EvalPlusCodeSolution(BaseModel):
    task_id: str = Field(..., description="Unique task identifier in the form 'HumanEval/X' or 'MBPP/X'")
    model_name: str = Field(..., description="Name of the evaluated model")
    prompt: str = Field(..., description="The original task prompt")
    solution: str = Field(..., description="The generated python code snippet")
    test_runs_count: int = Field(..., gt=0, description="Number of unique test cases executed (including original + plus tests)")
    pass_rate: float = Field(..., ge=0.0, le=1.0, description="The percentage of tests passed")
    is_fully_robust: bool = Field(..., description="True if 100% of standard and enhanced tests pass")

    @field_validator("task_id")
    @classmethod
    def validate_evalplus_task_id(cls, value: str) -> str:
        if not (value.startswith("HumanEval/") or value.startswith("MBPP/")):
            raise ValueError("task_id must start with 'HumanEval/' or 'MBPP/'")
        return value

def validate_solution_item(raw_json: str) -> Optional[EvalPlusCodeSolution]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2
        solution = EvalPlusCodeSolution.model_validate(data)
        return solution
    except json.JSONDecodeError:
        print("Error: JSON is invalid.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None
```

## Related tools / concepts
- [HumanEval](human-eval.md) — the foundational benchmark EvalPlus expands upon.
- [MBPP](mbpp.md) — the other major benchmark expanded by EvalPlus.
- [SWE-bench](swe-bench.md) — software engineering benchmark.
- [vLLM](../infrastructure/vllm.md) — optimized inference backend.
- [OpenCompass](opencompass.md) — evaluation platform.
- [HELM](helm.md) — holistic evaluation.
- [LM Evaluation Harness](lm-evaluation-harness.md) — standardized evaluation tool.
- [BigCodeBench](bigcodebench.md) — complex library-use benchmark.

## Sources / references
- [Official Website](https://evalplus.github.io/)
- [GitHub Repository](https://github.com/evalplus/evalplus)
- [NeurIPS 2023 Paper (arXiv 2305.01210)](https://arxiv.org/abs/2305.01210)

## Contribution Metadata
- Last reviewed: 2026-11-03
- Confidence: high
