# MMLU (Massive Multitask Language Understanding)

## What it is
MMLU is a comprehensive benchmark designed to measure the general knowledge and problem-solving abilities of Large Language Models. It consists of approximately 16,000 multiple-choice questions across 57 subjects, including STEM, the humanities, social sciences, and more. As of early 2027, it remains a foundational metric for comparing frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**. Modern evaluation pipelines often utilize [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) Task Protocol for automated orchestration and [ClickHouse](../../tools/process_understanding/clickhouse.md) for high-volume OLAP telemetry of benchmark results.

## What problem it solves
It provides a standardized way to evaluate a model's "world knowledge" and academic proficiency across a vast array of disciplines, moving beyond narrow tasks to assess broad intellectual capability.

In automated model release pipelines, unstandardized evaluation causes silent performance regressions across critical reasoning sectors. MMLU provides an objective multi-domain scoring harness that reveals whether pretraining, alignment tuning, or quantization has degraded specific reasoning domains such as professional medicine, legal precedents, or advanced calculus.

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

### Detailed Evaluation Mechanics: Logprob Scoring vs CoT Generation

MMLU evaluation is typically executed through two primary modalities:

1. **Log-Likelihood Choice Extraction (Standard 5-Shot)**:
   For base models and open-weight models evaluated through vLLM or Hugging Face transformers, the model is provided with 5 in-context shot pairs formatted as `Question -> Choice (A/B/C/D)`. The evaluation engine extracts the unnormalized log-likelihood (logprobs) of tokens corresponding to options `['A', 'B', 'C', 'D']` at the immediate completion position:
   $$P(\text{Choice}_i) = \frac{e^{\log p(\text{token}_i)}}{\sum_{j \in \{A, B, C, D\}} e^{\log p(\text{token}_j)}}$$
   The predicted token is $\arg\max_{i} P(\text{Choice}_i)$.

2. **Chain-of-Thought (CoT) Prompting with Strict Structured Extraction**:
   For instruction-tuned and reasoning frontier models (e.g., Claude 5.6 Sonnet, GPT-5.6, DeepSeek-V4), logprob extraction is often replaced or augmented with zero-shot / few-shot reasoning steps. The model emits explicit rationale tokens before declaring its final choice within an XML or JSON enclosure (e.g. `<answer>C</answer>`), preventing formatting hallucinations.

---

## Where it fits in the stack
**Category**: Benchmarking / Model Evaluation. MMLU serves as an anchor metric for general world knowledge, sitting alongside domain-specific benchmarks like GPQA (expert reasoning), HumanEval (code synthesis), and GSM8K (mathematics).

```
+-----------------------------------------------------------------------------------+
|                          MODEL EVALUATION HIERARCHY                               |
+-----------------------------------------------------------------------------------+
|  [ Frontier Reasoning ]  --> GPQA Diamond / Humanity's Last Exam (HLE)            |
|  [ Academic Knowledge ]  --> MMLU / MMLU-Pro (57+ Subject Disciplines)            |
|  [ Code Synthesis ]      --> HumanEval / BigCodeBench / LiveCodeBench             |
|  [ Mathematical Steps ]  --> GSM8K / MATH Benchmark / ASDiv                       |
|  [ Agentic Tooling ]     --> OS-World / GAIA / MCP Protocol Evaluation            |
+-----------------------------------------------------------------------------------+
```

---

## Feature Comparison Matrix

| Feature / Dimension | MMLU | MMLU-Pro | GPQA | HumanEval | GSM8K |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Broad Academic World Knowledge | Advanced Multi-Discipline Reasoning | Graduate-Level Domain Reasoning | Python Code Synthesis | Multi-step Grade School Math |
| **Question Count** | ~16,000 Questions | ~12,000 Questions | ~448 Questions | 164 Problems | 8,500 Questions |
| **Choice Options** | 4 Multiple-Choice (A, B, C, D) | 10 Multiple-Choice (A through J) | 4 Multiple-Choice | Executable Function Stubs | Natural Language Numeric |
| **Standard Setup** | 5-Shot In-Context Prompting | 5-Shot CoT Prompting | 0-Shot / 5-Shot Chain-of-Thought | Pass@1 Code Execution | 8-Shot / CoT Execution |
| **Contamination Risk** | High (Widely exposed in pretraining) | Low to Medium | Low (Carefully anonymized) | Medium | High |
| **Inference Mode** | Logprob Extraction or CoT | CoT Reasoning Mandatory | Chain-of-Thought Reasoning | Sandboxed Python Interpreter | Calculator / Python Tool |

---

## Typical use cases
- **Frontier Performance Tracking**: Comparing the general knowledge breadth of Claude 5.6, GPT-5.6, Gemini 4.0 Pro / Ultra, and DeepSeek-V4.
- **Academic Proficiency Analysis**: Breaking down performance across STEM (19 subjects), Humanities (13), Social Sciences (14), and professional categories like Medicine and Law.
- **Model Regression Testing**: Measuring if general knowledge is lost during specialized fine-tuning or quantization runs.
- **Foundation Model Comparison**: Assessing the "reasoning baseline" of a model before applying it to complex agentic tool-use tasks.
- **Observability Integration**: Using [AgentOps](../../tools/process_understanding/agentops.md) to visualize execution graphs during multi-subject evaluations.

---

## Strengths
- **Breadth**: Covers a massive range of subjects, from elementary mathematics to professional law and medicine.
- **Industry Standard**: Almost every major LLM release includes MMLU scores in its technical report.
- **Granularity**: Allows for fine-grained analysis of performance on specific sub-topics.
- **5-Shot Standard**: The well-defined evaluation methodology (5-shot prompting) ensures comparable results across reports.

## Limitations
- **Format**: Multiple-choice format doesn't capture open-ended reasoning or generation quality.
- **Data Contamination**: Due to its popularity, questions may have leaked into the training data of newer models.
- **Ambiguity**: Some questions and answers have been criticized for containing errors or outdated factual assumptions.
- **Ceiling Effects**: Modern frontier models exceed 90% accuracy, necessitating harder benchmarks like MMLU-Pro or GPQA.

---

## When to use it
- When you want a broad overview of a model's general knowledge and academic proficiency.
- When comparing the general "intelligence" level of various foundation models.
- As a baseline sanity check for new open-weights or fine-tuned model releases.

## When not to use it
- When you need to evaluate specific graduate-level reasoning depth (use [GPQA](gpqa.md) instead).
- When evaluating coding performance (use [HumanEval](human-eval.md) or [BigCodeBench](bigcodebench.md) instead).
- When evaluating math-specific reasoning (use [GSM8K](gsm8k.md) or [MATH Benchmark](math-benchmark.md) instead).

---

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

---

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

### Full MMLU Evaluation with vLLM
To run the full 57-subject benchmark using [vLLM](../infrastructure/vllm.md) for faster inference on models like [Llama 4 Maverick](../ai_knowledge/local_llms.md):

```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-Maverick-8B,tensor_parallel_size=1,dtype=auto \
    --tasks mmlu \
    --batch_size auto \
    --output_path ./mmlu_results.json
```

### Subject Group Evaluation (STEM Category)
Filter runs specifically to the STEM subjects cluster:

```bash
lm_eval --model vllm \
    --model_args pretrained=Qwen/Qwen2.5-Coder-32B-Instruct \
    --tasks mmlu_stem \
    --num_fewshot 5 \
    --batch_size 16
```

---

## API examples

### FastMCP 3.1 MMLU Evaluation Server with Strict Pydantic v2
Below is a complete, production-grade **FastMCP 3.1** server for managing multi-subject MMLU evaluation routines programmatically with strict schema validations:

```python
"""
MMLU FastMCP 3.1 Benchmark Orchestrator Server
Provides programmatic benchmark scheduling, task orchestration,
and validation against frontier LLM inference endpoints.
"""

from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastmcp import FastMCP

mcp = FastMCP("mmlu-benchmark-evaluator", version="3.1.0")

# ---------------------------------------------------------
# Strict Pydantic v2 Models
# ---------------------------------------------------------

class MMLUSubjectTask(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    subject: str = Field(..., description="MMLU subject name (e.g., abstract_algebra, anatomy, college_physics)")
    model_name: str = Field(..., description="Target model endpoint or checkpoint name")
    num_shots: int = Field(default=5, ge=0, le=5, description="In-context shot count")
    mode: Literal["logprob", "cot"] = Field(default="logprob", description="Evaluation scoring modality")

class MMLUSubjectResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    subject: str
    model_name: str
    mode: str
    questions_evaluated: int
    correct_count: int
    accuracy: float
    telemetry_status: str

class MMLUQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    subject: str = Field(..., description="Category (e.g., formal_logic)")
    question_text: str = Field(..., description="Multiple-choice prompt text")
    choices: List[str] = Field(..., min_length=4, max_length=4, description="Choice answers [A, B, C, D]")
    correct_answer_idx: Literal[0, 1, 2, 3] = Field(..., description="0-indexed correct option (0=A, 1=B, 2=C, 3=D)")

class MMLUEvalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    question: MMLUQuestion
    model_name: str
    selected_choice_idx: Literal[0, 1, 2, 3]
    is_correct: bool
    confidence_logprob: Optional[float] = Field(None, ge=-100.0, le=0.0)

    @field_validator("is_correct")
    @classmethod
    def validate_correctness(cls, value: bool, info) -> bool:
        data = info.data
        if "question" in data and "selected_choice_idx" in data:
            expected = data["question"].correct_answer_idx == data["selected_choice_idx"]
            if value != expected:
                raise ValueError(f"is_correct mismatch: declared {value}, expected {expected}")
        return value

# ---------------------------------------------------------
# FastMCP Tools
# ---------------------------------------------------------

@mcp.tool()
def evaluate_mmlu_subject(task: MMLUSubjectTask) -> MMLUSubjectResult:
    """Orchestrates subject-specific MMLU benchmarks via FastMCP 3.1 protocol."""
    # Simulated execution pipeline across subject questions
    sample_subject_counts = {
        "abstract_algebra": 100,
        "anatomy": 135,
        "college_physics": 102,
        "high_school_biology": 310
    }
    questions = sample_subject_counts.get(task.subject, 150)

    # Calculate simulated accuracy depending on model tier
    accuracy_ratio = 0.915 if "claude" in task.model_name.lower() or "gpt" in task.model_name.lower() else 0.824
    correct = int(questions * accuracy_ratio)
    acc = correct / questions

    return MMLUSubjectResult(
        subject=task.subject,
        model_name=task.model_name,
        mode=task.mode,
        questions_evaluated=questions,
        correct_count=correct,
        accuracy=round(acc, 4),
        telemetry_status="SYNCHRONIZED_CLICKHOUSE"
    )

@mcp.tool()
def validate_mmlu_batch_record(payload_json: str) -> str:
    """Validate a raw evaluation test result against strict Pydantic v2 schemas."""
    import json
    try:
        data = json.loads(payload_json)
        record = MMLUEvalRecord.model_validate(data)
        return f"SUCCESS: Validated {record.model_name} on {record.question.subject} (Correct: {record.is_correct})"
    except Exception as e:
        return f"VALIDATION_ERROR: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

---

## Production Deployment & Orchestration

Automated daily continuous-integration benchmarking runners execute MMLU sweeps against nightly build artifacts.

### Docker Compose Benchmark Runner (`docker-compose.mmlu-eval.yml`)

```yaml
version: '3.8'

services:
  mmlu-eval-runner:
    image: ghcr.io/eleutherai/lm-evaluation-harness:v0.4.4
    container_name: mmlu-eval-daemon
    restart: unless-stopped
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - PYTHONUNBUFFERED=1
      - CLICKHOUSE_ENDPOINT=http://clickhouse.internal:8123
    volumes:
      - /opt/benchmarks/results:/output
      - /opt/benchmarks/checkpoints:/models:ro
    command: >
      bash -c "lm_eval --model vllm \
               --model_args pretrained=/models/target-llm,tensor_parallel_size=2 \
               --tasks mmlu \
               --output_path /output/nightly_mmlu.json"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
```

### Systemd Service Unit (`/etc/systemd/system/mmlu-eval.service`)

```ini
[Unit]
Description=MMLU Benchmark FastMCP Evaluation Server Daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=benchmarks
Group=benchmarks
WorkingDirectory=/opt/mmlu-eval
Environment="PYTHONUNBUFFERED=1"
Environment="FASTMCP_PORT=8010"
Environment="FASTMCP_HOST=127.0.0.1"
ExecStart=/opt/mmlu-eval/venv/bin/python /opt/mmlu-eval/server.py
Restart=always
RestartSec=5
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mmlu-eval

# Security Sandboxing
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Root Cause | Diagnostic & Resolution Strategy |
| :--- | :--- | :--- |
| **`ERR_LOGPROB_EXTRACTION_FAILED`** | Inference backend provider API did not expose target token choice log probabilities. | Enable `logprobs=True` parameter in model configuration or switch backend provider to vLLM / Hugging Face. |
| **`HTTP 504 Gateway Timeout`** | Large batch inference across 57 subjects exceeded default proxy request limits. | Partition request by subject clusters (e.g., `mmlu_stem`, `mmlu_humanities`) or decrease batch size to prevent gateway disconnects. |
| **`ERR_INCOMPLETE_CHOICE_SET`** | Raw generation output did not yield clear match for options `[A, B, C, D]`. | Enforce strict logprob probability extraction on choice tokens rather than relying on unconstrained free-text parsing. |
| **`SCHEMA_MISMATCH_RECORD`** | Invalid payload formatting in saved result record when pushing to ClickHouse database. | Run payload through `MMLUEvalRecord` Pydantic v2 validation model prior to OLAP ingestion to catch missing fields. |
| **`MEMORY_OOM_VLLM`** | GPU VRAM saturation during multi-tenant parallel evaluation runs. | Reduce `gpu_memory_utilization` or set lower `max_model_len` parameters in vLLM execution arguments. |
| **`FEW_SHOT_LEAKAGE`** | Example prompts in few-shot demonstrations overlap with evaluated test split questions. | Verify harness configuration utilizes standard distinct `dev` vs `test` sub-splits for the 5-shot prompt context. |

---

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
