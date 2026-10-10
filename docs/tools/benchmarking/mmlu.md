# MMLU (Massive Multitask Language Understanding)

## What it is
MMLU is a comprehensive benchmark designed to measure the general knowledge and problem-solving abilities of Large Language Models. It consists of approximately 16,000 multiple-choice questions across 57 subjects, including STEM, the humanities, social sciences, and more. As of early 2027, it remains a foundational metric for comparing frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**. Modern evaluation pipelines often utilize [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) Task Protocol for automated orchestration and [ClickHouse](../../tools/process_understanding/clickhouse.md) for high-volume OLAP telemetry of benchmark results.

## What problem it solves
It provides a standardized way to evaluate a model's "world knowledge" and academic proficiency across a vast array of disciplines, moving beyond narrow tasks to assess broad intellectual capability.

## Architecture & Evaluation Pipeline

```
+-----------------------------------------------------------------------------------+
|                            MMLU Benchmark Suite (16k Questions)                   |
|              (57 Subjects: STEM, Humanities, Social Sciences, Professional)       |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  5-Shot Prompting Protocol
+-----------------------------------------+-----------------------------------------+
|                              FastMCP 3.1 Benchmarking Engine                      |
|                                                                                   |
|  +-----------------------------------+   +-------------------------------------+  |
|  |     Batch Prompt Generator        |   |       Logprob Extractor             |  |
|  |  - 5-Shot Context Injection       |   |  - Choice Probabilities (A, B, C, D)|  |
|  |  - Subject-Specific Normalization |   |  - Logprob Verification & Parsing   |  |
|  +-----------------+-----------------+   +------------------+------------------+  |
|                    |                                        |                     |
|                    +--------------------+-------------------+                     |
|                                         |                                         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  Inference & Logprobs
+-----------------------------------------------------------------------------------+
|               Evaluated Models (Claude 5.6, GPT-5.6, Llama 4, vLLM Engine)        |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  Response JSON & Logprobs
+-----------------------------------------+-----------------------------------------+
|                                    Telemetry & Storage                            |
|                                                                                   |
|  +-----------------------------------+   +-------------------------------------+  |
|  |    Pydantic v2 Schema Validator   |   |       ClickHouse OLAP Storage       |  |
|  |  - Correctness Assertion          |   |  - Subject-Level Analytics          |  |
|  |  - Result Verification            |   |  - Historical Benchmark Telemetry   |  |
|  +-----------------------------------+   +-------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Benchmarking / Model Evaluation. MMLU serves as an anchor metric for general world knowledge, sitting alongside domain-specific benchmarks like GPQA (expert reasoning), HumanEval (code synthesis), and GSM8K (mathematics).

## Feature Comparison Matrix

| Feature / Dimension | MMLU | GPQA | HumanEval | GSM8K |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Broad Academic World Knowledge | Graduate-Level Domain Reasoning | Python Code Synthesis | Multi-step Grade School Math |
| **Question Count** | ~16,000 Questions | ~448 Questions | 164 Problems | 8,500 Questions |
| **Format** | Multiple Choice (4 choices) | Multiple Choice (4 choices) | Code Generation & Unit Tests | Free-form Chain-of-Thought |
| **Standard Setup** | 5-Shot In-Context Prompting | 0-Shot / 5-Shot Chain-of-Thought | Pass@1 Code Execution | 8-Shot / CoT Execution |
| **Contamination Risk** | High (Widely exposed in pretraining) | Low (Carefully anonymized) | Medium | High |

## Typical use cases
- **Frontier Performance Tracking**: Comparing the general knowledge breadth of Claude 5.6, GPT-5.6, Gemini 4.0 Pro / Ultra, and DeepSeek-V4.
- **Academic Proficiency Analysis**: Breaking down performance across STEM (19 subjects), Humanities (13), Social Sciences (14), and professional categories like Medicine and Law.
- **Model Regression Testing**: Measuring if general knowledge is lost during specialized fine-tuning or quantization runs.
- **Foundation Model Comparison**: Assessing the "reasoning baseline" of a model before applying it to complex agentic tool-use tasks.
- **Observability Integration**: Using [AgentOps](../../tools/process_understanding/agentops.md) to visualize execution graphs during multi-subject evaluations.

## Strengths
- **Breadth**: Covers a massive range of subjects, from elementary mathematics to professional law and medicine.
- **Industry Standard**: Almost every major LLM release includes MMLU scores in its technical report.
- **Granularity**: Allows for fine-grained analysis of performance on specific sub-topics.
- **5-Shot Standard**: The well-defined evaluation methodology (5-shot prompting) ensures comparable results across reports.

## Limitations
- **Format**: Multiple-choice format doesn't capture open-ended reasoning or generation quality.
- **Data Contamination**: Due to its popularity, questions may have leaked into the training data of newer models.
- **Ambiguity**: Some questions and answers have been criticized for containing errors or outdated factual assumptions.

## When to use it
- When you want a broad overview of a model's general knowledge and academic proficiency.
- When comparing the general "intelligence" level of various foundation models.
- As a baseline sanity check for new open-weights or fine-tuned model releases.

## When not to use it
- When you need to evaluate specific graduate-level reasoning depth (use [GPQA](gpqa.md) instead).
- When evaluating coding performance (use [HumanEval](human-eval.md) or [BigCodeBench](bigcodebench.md) instead).
- When evaluating math-specific reasoning (use [GSM8K](gsm8k.md) or [MATH Benchmark](math-benchmark.md) instead).

## Getting started

### Installation (via LM Evaluation Harness)
The easiest way to run MMLU is using the [LM Evaluation Harness](lm-evaluation-harness.md).

```bash
pip install "lm_eval[hf,vllm]" --upgrade
```

### Setup
Ensure you have the appropriate model weights or API keys configured.

```bash
# Verify the harness is installed
lm_eval --help
```

## CLI examples

### Hello-world Evaluation
Run a subset of MMLU (e.g., elementary mathematics) on a small model to verify your setup:

```bash
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks mmlu_elementary_mathematics \
    --device cuda:0 \
    --batch_size 8
```

### Full MMLU Evaluation
To run the full 57-subject benchmark using [vLLM](../infrastructure/vllm.md) for faster inference on models like [Llama 4 Maverick](../ai_knowledge/local_llms.md):

```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-Maverick-8B,tensor_parallel_size=1,dtype=auto \
    --tasks mmlu \
    --batch_size auto
```

## API examples

### FastMCP 3.1 MMLU Evaluation Server
Below is a **FastMCP 3.1** server pattern for managing multi-subject MMLU evaluation routines programmatically:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List

mcp = FastMCP("mmlu-benchmark-evaluator")

class MMLUSubjectTask(BaseModel):
    subject: str = Field(..., description="MMLU subject name (e.g., abstract_algebra, anatomy)")
    model_name: str = Field(..., description="Target model endpoint or name")
    num_shots: int = Field(default=5, ge=0, le=5, description="In-context shot count")

class MMLUSubjectResult(BaseModel):
    subject: str
    model_name: str
    questions_evaluated: int
    correct_count: int
    accuracy: float

@mcp.tool()
def evaluate_mmlu_subject(task: MMLUSubjectTask) -> MMLUSubjectResult:
    """Orchestrates subject-specific MMLU benchmarks via FastMCP 3.1 protocol."""
    # Simulated batch inference execution
    questions = 280
    correct = 250
    acc = correct / questions

    return MMLUSubjectResult(
        subject=task.subject,
        model_name=task.model_name,
        questions_evaluated=questions,
        correct_count=correct,
        accuracy=round(acc, 4)
    )

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Question and Evaluation Validation using Pydantic v2
This Python script validates MMLU benchmark question structures and evaluation execution logs using **Pydantic v2** prior to storing or analyzing results:

```python
import json
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

class MMLUQuestion(BaseModel):
    subject: str = Field(..., description="Subject category of the question (e.g., abstract_algebra, anatomy)")
    question_text: str = Field(..., description="The multiple-choice question prompt text")
    choices: List[str] = Field(..., min_length=4, max_length=4, description="List of exactly 4 multiple-choice answers")
    correct_answer_idx: Literal[0, 1, 2, 3] = Field(..., description="0-indexed correct answer (0=A, 1=B, 2=C, 3=D)")

class MMLUEvalResult(BaseModel):
    question: MMLUQuestion
    model_name: str = Field(..., description="Name of the model evaluated")
    selected_choice_idx: Literal[0, 1, 2, 3] = Field(..., description="0-indexed choice selected by the model")
    is_correct: bool = Field(..., description="Whether the selected choice was correct")
    raw_response: str = Field(..., description="Raw output generated by the LLM")

    @field_validator("is_correct")
    @classmethod
    def validate_correctness_logic(cls, value: bool, info) -> bool:
        data = info.data
        if "question" in data and "selected_choice_idx" in data:
            expected = data["question"].correct_answer_idx == data["selected_choice_idx"]
            if value != expected:
                raise ValueError(f"is_correct ({value}) does not match question correction logic (expected {expected})")
        return value

def validate_mmlu_result(raw_json: str) -> Optional[MMLUEvalResult]:
    try:
        data = json.loads(raw_json)
        result_record = MMLUEvalResult.model_validate(data)
        return result_record
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

if __name__ == "__main__":
    sample_payload = json.dumps({
        "question": {
            "subject": "abstract_algebra",
            "question_text": "What is the order of the group Z_6?",
            "choices": ["4", "5", "6", "12"],
            "correct_answer_idx": 2
        },
        "model_name": "claude-5-6-sonnet",
        "selected_choice_idx": 2,
        "is_correct": True,
        "raw_response": "The answer is C: 6."
    })
    res = validate_mmlu_result(sample_payload)
    if res:
        print(f"Validated MMLU result for {res.model_name} on {res.question.subject}: {res.is_correct}")
```

## Related tools / concepts
- [HELM](helm.md) — a holistic evaluation framework that includes MMLU.
- [LM Evaluation Harness](lm-evaluation-harness.md) — the standard tool for running MMLU.
- [OpenCompass](opencompass.md) — comprehensive evaluation platform.
- [GPQA](gpqa.md) — a benchmark for graduate-level expert knowledge.
- [HumanEval](human-eval.md) — standard coding benchmark.
- [BigCodeBench](bigcodebench.md) — complex coding benchmark.
- [GSM8K](gsm8k.md) — grade school math benchmark.
- [Humanity's Last Exam (HLE)](humanitys-last-exam.md) — frontier benchmark following MMLU.
- [ARC (AI2 Reasoning Challenge)](arc.md) — reasoning-focused benchmark.
- [ASDiv](asdiv.md) — adversarial math word problems.
- [MCP](../../tools/automation_orchestration/mcp.md) — protocol for agentic tool and task orchestration.
- [ClickHouse](../../tools/process_understanding/clickhouse.md) — high-performance OLAP database for telemetry.
- [AgentOps](../../tools/process_understanding/agentops.md) — observability for agentic workflows.

## Sources / references
- [Original Paper: Measuring Massive Multitask Language Understanding (Hendrycks et al. arXiv 2009.03300)](https://arxiv.org/abs/2009.03300)
- [GitHub Repository (cais/mmlu)](https://github.com/hendrycks/test)
- [Hugging Face Dataset Card](https://huggingface.co/datasets/cais/mmlu)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
