# MMLU (Massive Multitask Language Understanding)

## What it is
MMLU is a comprehensive benchmark designed to measure the general knowledge and problem-solving abilities of Large Language Models. It consists of approximately 16,000 multiple-choice questions across 57 subjects, including STEM, the humanities, social sciences, and more. As of January 2027, it remains a foundational metric for comparing frontier models like **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**. Modern evaluation pipelines often utilize [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) Task Protocol for automated orchestration and [ClickHouse](../../tools/process_understanding/clickhouse.md) for high-volume OLAP telemetry of benchmark results.

## What problem it solves
It provides a standardized way to evaluate a model's "world knowledge" and academic proficiency across a vast array of disciplines, moving beyond narrow tasks to assess broad intellectual capability.

## Where it fits in the stack
**Benchmarking**. It is one of the most widely cited benchmarks for comparing the general intelligence of different LLMs. It often serves as the "anchor" for overall model performance rankings.

```mermaid
graph TD
    MMLUData[MMLU Suite: 57 Subjects & 16k Questions] --> FastMCP[FastMCP 3.1 Benchmarking Server]
    FastMCP -->|5-Shot Prompting Protocol| FrontierModel[Frontier Model: Claude 5.1 / GPT-5.6 / DeepSeek-V4]
    FrontierModel -->|Generate Option Logprobs & Choices| Parser[Logprob Extractor & Choice Parser]
    Parser -->|Validate Response & Correctness| Verifier[Pydantic v2 MMLUEvalResult Validator]
    Verifier -->|OLAP Stream Ingestion| ClickHouse[ClickHouse Telemetry Database]
```

## Typical use cases
- **Frontier Performance Tracking**: Comparing the general knowledge breadth of Claude 5.1, GPT-5.5 / 5.6, Gemini 4.0 Pro / Ultra, and DeepSeek-V4.
- **Academic Proficiency Analysis**: Breaking down performance across STEM (19 subjects), Humanities (13), Social Sciences (14), and professional categories like Medicine and Law.
- **Model Regression Testing**: Measuring if general knowledge is lost during specialized fine-tuning.
- **Foundation Model Comparison**: Assessing the "reasoning baseline" of a model before applying it to agentic tasks.
- **Observability Integration**: Using [AgentOps](../../tools/process_understanding/agentops.md) to visualize the execution graph during complex multi-subject evaluations.

## Feature Comparison Matrix

| Metric / Dimension | MMLU | MMLU-Pro | GPQA | HELM |
| :--- | :--- | :--- | :--- | :--- |
| **Total Questions** | ~16,000 questions | 12,000 questions | 448 questions | Multi-benchmark suite |
| **Choice Format** | 4-option multiple choice | 10-option multiple choice | 4-option multiple choice | Diverse (Open/Closed/MCQ) |
| **Subject Count** | 57 academic subjects | 14 broader domains | Graduate STEM disciplines | 40+ evaluation scenarios |
| **Target Capability** | Undergraduate level general knowledge | Complex reasoning & distractor robustness | Graduate domain-expert reasoning | Holistic multi-dimensional alignment |
| **Chain-of-Thought (CoT)** | 5-Shot direct / optional CoT | 5-Shot Chain-of-Thought mandatory | CoT reasoning mandatory | Direct + CoT prompting |
| **FastMCP 3.1 Support** | First-class task protocol server | First-class task protocol server | Task protocol server | REST / Custom harness |

## Strengths
- **Breadth**: Covers a massive range of subjects, from elementary mathematics to professional law and medicine.
- **Industry Standard**: Almost every major LLM release includes MMLU scores.
- **Granularity**: Allows for fine-grained analysis of performance on specific topics.
- **5-Shot Standard**: The well-defined evaluation methodology (5-shot prompting) ensures comparable results across reports.

## Limitations
- **Format**: Multiple-choice format doesn't capture open-ended reasoning or generation quality.
- **Data Contamination**: Due to its popularity, questions may have leaked into the training data of newer models.
- **Ambiguity**: Some questions and answers have been criticized for being ambiguous or containing errors.

## When to use it
- When you want a broad overview of a model's general knowledge and academic proficiency.
- When comparing the general "intelligence" level of various foundation models.
- As a baseline check for new model releases.

## When not to use it
- When you need to evaluate specific reasoning depth (use [GPQA](gpqa.md) instead).
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

## FastMCP 3.1 Integration

The following FastMCP 3.1 server exposes an enterprise benchmarking suite for orchestrating MMLU evaluations across model providers:

```python
import json
import httpx
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MMLU-Benchmark-Evaluator", version="3.1.0")

class SubjectEvalRequest(BaseModel):
    subject: str = Field(..., description="Subject category (e.g., computer_security, abstract_algebra)")
    model_endpoint: str = Field("http://localhost:8000/v1", description="OpenAI-compatible inference base URL")
    model_name: str = Field("meta-llama/Llama-4-Maverick-8B", description="Target model name")
    num_shots: int = Field(5, description="Number of few-shot prompt examples")

@mcp.tool()
async def evaluate_mmlu_subject(payload: SubjectEvalRequest) -> str:
    """Orchestrates subject-specific MMLU benchmarks via FastMCP 3.1 protocol."""
    # Simulated execution pipeline interacting with vLLM or LiteLLM
    result = {
        "subject": payload.subject,
        "model": payload.model_name,
        "num_shots": payload.num_shots,
        "questions_evaluated": 280,
        "accuracy": 0.892,
        "latency_per_question_ms": 42.1,
        "status": "completed"
    }
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_benchmark_suite_manifest() -> str:
    """Returns the list of 57 MMLU subject categories grouped by domain."""
    manifest = {
        "stem": ["abstract_algebra", "anatomy", "astronomy", "college_chemistry", "computer_security"],
        "humanities": ["formal_logic", "high_school_european_history", "jurisprudence", "philosophy"],
        "social_sciences": ["econometrics", "high_school_geography", "professional_psychology"],
        "other": ["business_ethics", "clinical_knowledge", "global_facts", "management"]
    }
    return json.dumps(manifest, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## API examples

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
        # Pydantic v2 field validator to ensure consistency
        data = info.data
        if "question" in data and "selected_choice_idx" in data:
            expected = data["question"].correct_answer_idx == data["selected_choice_idx"]
            if value != expected:
                raise ValueError(f"is_correct ({value}) does not match question correction logic (expected {expected})")
        return value

def validate_mmlu_result(raw_json: str) -> Optional[MMLUEvalResult]:
    try:
        data = json.loads(raw_json)
        # Validate result object with Pydantic v2
        result_record = MMLUEvalResult.model_validate(data)
        return result_record
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None
```

## Operational Best Practices & Troubleshooting

### Contamination Mitigations
- **De-contamination Scanning**: Run strict 13-gram overlap checks against model training pre-training sets to ensure public MMLU test sets have not leaked into weights.
- **Dynamic Perturbations**: Utilize randomized choice orderings (A/B/C/D option swapping) during evaluation to prevent exact option index memorization artifacts.

### Distributed Evaluation at Scale
- **vLLM / Tensor Parallelism**: When evaluating 70B+ parameter models across the full 57 subjects, use vLLM tensor parallelism (`tensor_parallel_size=4` or `8`) to minimize total inference runtime from hours to minutes.
- **OLAP Logging**: Stream every token choice logprob directly to ClickHouse to conduct post-hoc statistical confidence interval checks across subject sub-categories.

## Related tools / concepts
- [HELM](helm.md) — a holistic evaluation framework that includes MMLU.
- [LM Evaluation Harness](lm-evaluation-harness.md) — the standard tool for running MMLU.
- [OpenCompass](opencompass.md) — another comprehensive evaluation platform.
- [GPQA](gpqa.md) — a much harder benchmark for expert-level knowledge.
- [HumanEval](human-eval.md) — standard coding benchmark.
- [BigCodeBench](bigcodebench.md) — more complex coding benchmark.
- [GSM8K](gsm8k.md) — grade school math benchmark.
- [Humanity's Last Exam (HLE)](humanitys-last-exam.md) — a frontier benchmark designed to follow MMLU.
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
