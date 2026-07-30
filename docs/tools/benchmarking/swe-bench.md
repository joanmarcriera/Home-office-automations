# SWE-bench

## What it is
SWE-bench is a benchmark for evaluating LLMs on real-world software engineering tasks. It uses actual issues from GitHub and requires the model to generate a functional patch that passes existing tests. As of November 2026, it remains the industry standard for measuring the autonomous coding capabilities of frontier models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0**.

## What problem it solves
Measures whether LLMs can perform practical software engineering work—understanding codebases, diagnosing issues, and producing working fixes—rather than just solving isolated coding puzzles. It identifies "stalling" behaviors and evaluates the robustness of agentic loops in a terminal environment, often leveraging **Model Context Protocol (MCP 3.1)** for dynamic tool discovery.

## Where it fits in the stack
**Benchmarking / Eval**. It is used as a reference benchmark for evaluating real-world software engineering capabilities of AI agents and coding assistants.

## Typical use cases
- Evaluating AI coding agents on their ability to resolve real GitHub issues.
- Comparing models on practical software engineering tasks.
- Tracking progress of AI agents toward autonomous software development.
- Choosing whether an agent is ready for repository-maintenance work that requires reading tests, editing files, and producing a valid patch.

## Strengths
- **Authenticity**: Based on real-world GitHub issues, providing high-fidelity evaluation.
- **End-to-End Skill Assessment**: Requires reading code, understanding issues, and writing functional patches.
- **Objective Validation**: Results are verified against existing test suites from the source repositories.
- **Large Dataset**: Over 2,000 tasks across multiple popular Python repositories.

## Limitations
- **Computational Cost**: Requires a Docker environment and significant compute to run full test suites.
- **Language Bias**: Primarily focused on Python repositories in the standard dataset.
- **Static Nature**: While updated, older subsets can suffer from data contamination in newer model training sets.
- **Limited Scope**: Does not typically evaluate documentation-only changes or complex multi-repository dependencies.

## When to use it
- When evaluating AI agents or LLMs on real-world software engineering capability.
- When comparing coding agents that claim to autonomously resolve issues.
- When performing high-signal regression testing on agentic coding frameworks.

## When not to use it
- When evaluating basic code generation from simple specifications (use [HumanEval](human-eval.md) instead).
- When you need quick, lightweight benchmarking without Docker infrastructure.
- For testing non-Python languages (unless using specific extensions).

## Getting started
SWE-bench requires a Docker environment to safely execute untrusted code and run test suites.

### 1. Installation
```bash
pip install swebench
```

### 2. Basic Inference
To get started, you can run an inference pass using a lightweight model or a specific subset:
```bash
python -m swebench.inference.run_api \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --model_name claude-5-1-sonnet-20261022 \
    --output_dir ./predictions
```

## CLI examples
The following commands demonstrate how to interact with the SWE-bench evaluation harness.

```bash
# Install the SWE-bench package from source for the latest updates
pip install git+https://github.com/princeton-nlp/SWE-bench.git

# Run predictions for the 'Verified' subset using a local model endpoint
python -m swebench.inference.run_api --dataset_name princeton-nlp/SWE-bench_Verified --output_dir ./eval_results

# Execute evaluation using the Docker harness to verify generated patches
docker run -v $(pwd)/predictions:/predictions swebench/swe-bench-eval --predictions /predictions/predictions.jsonl --output_dir /results
```

## API examples

### Loading the Dataset (Python)
```python
from datasets import load_dataset

# Load the human-verified subset (500 high-quality tasks)
dataset = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")

# Access a specific task instance
task = dataset[0]
print(f"Task ID: {task['instance_id']}")
print(f"Problem: {task['problem_statement']}")
```

### Running an Evaluation Instance (Python)
```python
from swebench.harness.test_spec import make_test_spec
from swebench.harness.run_evaluation import run_instance

# Define a task instance with a proposed patch
instance = {
    "repo": "django/django",
    "instance_id": "django__django-12345",
    "base_commit": "abc12345",
    "patch": "diff --git a/django/db/models/fields/__init__.py...",
    "test_patch": "diff --git a/tests/model_fields/tests.py..."
}

# Run evaluation within the Docker environment
spec = make_test_spec(instance)
result = run_instance(spec)
print(f"Issue Resolved: {result['resolved']}")
```

### Programmatic Prediction Validation using Pydantic v2
This Python script validates predicting patches and evaluation inputs for SWE-bench instances using **Pydantic v2** prior to kicking off Docker execution runs:

```python
import json
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError, field_validator

class SWEBenchPrediction(BaseModel):
    instance_id: str = Field(..., description="The unique SWE-bench task identifier (e.g. django__django-12345)")
    model_name: str = Field(..., description="Name of the model generating the patch")
    patch: str = Field(..., description="The generated git diff patch proposing the bugfix")
    explanation: Optional[str] = Field(None, description="Optional reasoning chain leading to this fix")
    tokens_used: Optional[int] = Field(None, ge=0, description="Inference token count consumed")

    @field_validator("patch")
    @classmethod
    def validate_is_git_patch(cls, value: str) -> str:
        if value and not value.startswith("diff --git"):
            raise ValueError("Patch must be a valid unified diff starting with 'diff --git'")
        return value

def validate_prediction_file(raw_json_line: str) -> Optional[SWEBenchPrediction]:
    try:
        data = json.loads(raw_json_line)
        # Validate prediction using Pydantic v2
        prediction = SWEBenchPrediction.model_validate(data)
        return prediction
    except json.JSONDecodeError:
        print("Error: Line is not valid JSON.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

# Example usage:
# if __name__ == "__main__":
#     sample_prediction = """
#     {
#         "instance_id": "django__django-12345",
#         "model_name": "claude-5-1-sonnet-20261022",
#         "patch": "diff --git a/django/db/models/fields/__init__.py b/django/db/models/fields/__init__.py\\n--- a/django/db/models/fields/__init__.py\\n+++ b/django/db/models/fields/__init__.py\\n@@ -1,1 +1,2 @@\\n",
#         "tokens_used": 14205
#     }
#     """
#     validated = validate_prediction_file(sample_prediction)
#     if validated:
#         print("SWE-bench prediction schema is valid!")
#         print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [HumanEval](human-eval.md) — Basic code generation benchmark.
- [LongCLI-Bench](longcli-bench.md) — Long-horizon CLI task evaluation.
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md) — Agentic research evaluation.
- [Aider](../development_ops/aider.md) — Terminal-based AI coding assistant.
- [Claude Code](../development_ops/claude-code-setup.md) — Anthropic's official coding agent.
- [OpenHands](../development_ops/openhands.md) — Open-source agentic platform.
- [Terminal-Bench](terminal-bench.md) — Evaluating tool use in CLI environments.
- [Benchmarking](index.md) — Overview of AI evaluation frameworks.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for agentic tool discovery.

## Sources / references
- [Official Website](https://www.swebench.com/)
- [GitHub Repository](https://github.com/princeton-nlp/SWE-bench)
- [SWE-bench Paper (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770)
- [SWE-bench Verified Announcement](https://openai.com/index/introducing-swe-bench-verified/)

## Contribution Metadata
- Last reviewed: 2026-11-03
- Confidence: high
