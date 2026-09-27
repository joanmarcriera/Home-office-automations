# GPQA (Graduate-Level Google-Proof Q&A)

## What it is
GPQA (Graduate-Level Google-Proof Q&A) is an expert-level benchmark dataset designed to evaluate high-order scientific reasoning, complex logic, and domain mastery in frontier Large Language Models (LLMs). First introduced in late 2023 by researchers from NYU, Anthropic, and Alignment Research Center (ARC), GPQA comprises 448 multiple-choice questions written and validated exclusively by PhD-level subject matter experts across Biology, Physics, and Chemistry.

The defining characteristic of GPQA is its "Google-proof" design criteria. Questions are engineered such that non-expert humans (even when given unrestricted high-speed internet search access and 30+ minutes per question) achieve less than 35% accuracy. Conversely, domain experts with PhDs achieve over 74% accuracy. In early 2027, GPQA (specifically its `gpqa_diamond` subset of 198 ultra-vetted questions) remains the definitive benchmark for distinguishing genuine scientific reasoning capabilities from superficial pattern matching in frontier LLMs like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## What problem it solves
Standard multi-subject benchmarks (such as MMLU or ARC-Challenge) suffer from severe limitations when evaluating modern frontier models:
- **Data Contamination & Memorization**: Public multiple-choice datasets are frequently scraped into massive pre-training corpora, inflating model scores through rote memorization rather than reasoning.
- **Search Saturated Questions**: Most conventional questions can be answered rapidly by querying search engines, making them ineffective at testing autonomous problem-solving.
- **Saturating Performance Ceilings**: Frontier models rapidly hit 90%+ scores on standard benchmarks, eliminating granular differentiation between model generations.

GPQA addresses these challenges by:
- **Requiring Multi-Step Expert Reasoning**: Solutions require synthesizing multiple graduate-level domain concepts, performing non-trivial calculations, and reasoning through subtle physical or biochemical mechanisms.
- **Adversarial Distractor Design**: Expert authors explicitly constructed subtle, mathematically plausible incorrect choices ("distractors") that penalize superficial logic leaps and hallucinations.
- **Contamination-Resistant Curation**: Maintaining gated release protocols and strict hashing to prevent inclusion in training datasets.

## System Architecture

```
                                    GPQA Expert Evaluation Flow

  +-----------------------+        +------------------------+        +--------------------------+
  |  GPQA Diamond Subset  | ---->  |  FastMCP 3.1 Task      | ---->  | Frontier Reasoning LLM   |
  |  (198 PhD-Level Qs)   |        |  Protocol Orchestrator  |        | (Claude 5.1 / GPT-5.5)   |
  +-----------------------+        +------------------------+        +--------------------------+
                                                                                  |
                                                                                  v
  +-----------------------+        +------------------------+        +--------------------------+
  | Expert Score Metrics  | <----  | Pydantic v2 Answer     | <----  | Chain-of-Thought (CoT)   |
  | & Domain Telemetry    |        | Validation Pipeline    |        | Solution & Option Selection|
  +-----------------------+        +------------------------+        +--------------------------+
```

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / High-Order Reasoning & Scientific Competence.

GPQA functions as the premier evaluation target for reasoning-dense LLM architectures, fine-tuning checkpoints, and extended Chain-of-Thought (CoT) inference systems. It measures whether an AI system possesses true domain expertise required for autonomous scientific discovery and complex enterprise research.

## Typical use cases
- **Frontier Reasoning Model Evaluation**: Differentiating performance between state-of-the-art LLMs on physics, chemistry, and biology reasoning tasks.
- **Chain-of-Thought (CoT) & Test-Time Compute Benchmarking**: Quantifying how extended reasoning tokens improve accuracy on expert-level questions.
- **Agentic Research Assistant Validation**: Testing autonomous research tools before deployment in enterprise biotech or physics research pipelines.
- **Post-Training Optimization**: Serving as a validation set for RLHF and Direct Preference Optimization (DPO) iterations focused on scientific accuracy.

## Strengths
- **PhD-Level Ground Truth**: Questions written and cross-verified by domain experts with verified PhD credentials.
- **Resistant to Search Shortcuts**: Designed so that search engines and retrieval tools do not trivially reveal answers without domain synthesis.
- **Strong Correlation with True Reasoning**: High scores strongly correlate with real-world capability in technical, scientific, and coding disciplines.
- **Clean Subsets**: Offers `gpqa_diamond` (198 highest-quality consensus questions) alongside `gpqa_main` and `gpqa_extended`.

## Limitations
- **Compact Dataset Scale**: 448 total questions (198 in Diamond) limits sub-discipline statistical granularity.
- **Narrow Discipline Range**: Strictly focused on hard natural sciences (Physics, Chemistry, Biology); excludes computer science, law, and social sciences.
- **Multiple-Choice Format**: Does not evaluate open-ended scientific report writing, multi-step lab protocol execution, or code implementation.
- **High Human Verification Cost**: Creating new questions requires compensating PhD experts, making benchmark expansion expensive.

## When to use it
- When evaluating frontier LLMs or reasoning models on graduate-level scientific problem-solving.
- When you require a benchmark resistant to pre-training memorization and simple search engine retrieval.
- To measure the benefits of extended test-time compute, reasoning models, and self-reflection loops.

## When not to use it
- For testing software engineering, repository editing, or code synthesis (use [HumanEval](human-eval.md) or [SWE-bench](swe-bench.md)).
- For general knowledge or multi-disciplinary high-school level tests (use [MMLU](mmlu.md)).
- For assessing live human-preference "vibes" or conversational fluency (use [Chatbot Arena](chatbot-arena.md)).

## Getting started

### 1. Install Evaluation Harness & FastMCP
Install LM Evaluation Harness along with Pydantic and FastMCP support:

```bash
pip install lm-eval pydantic fastmcp
```

### 2. Download GPQA Dataset
Inspect the dataset directly from Hugging Face Datasets:

```python
from datasets import load_dataset

dataset = load_dataset("Idavidrein/gpqa", "gpqa_diamond")
print(f"Loaded {len(dataset['train'])} GPQA Diamond questions.")
```

## CLI examples

### 1. Evaluate Local Model on GPQA Diamond via LM Evaluation Harness
Run zero-shot evaluation on GPQA Diamond using a local model:

```bash
python3 -m lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B,trust_remote_code=True \
    --tasks gpqa_diamond \
    --device cuda:0 \
    --batch_size 1
```

### 2. Evaluate API-Based Model with Few-Shot Chain-of-Thought
Run GPQA evaluation against an API endpoint with CoT prompting:

```bash
python3 -m lm_eval --model anthropic \
    --model_args model=claude-5-1-opus-20261031 \
    --tasks gpqa_diamond \
    --num_fewshot 0
```

### 3. Inspect Dataset via Hugging Face CLI
Download and cache the dataset locally:

```bash
huggingface-cli download Idavidrein/gpqa --repo-type dataset
```

## API examples

### 1. FastMCP 3.1 Server: GPQA Evaluation Gateway
The following complete FastMCP 3.1 Python server exposes a GPQA task evaluation tool for autonomous benchmark orchestrators:

```python
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(
    name="GPQA Evaluation Server",
    version="3.1.0",
    description="FastMCP server for orchestrating graduate-level GPQA benchmarks"
)

class EvaluationTask(BaseModel):
    question_id: str = Field(..., description="Unique question ID")
    discipline: str = Field(..., description="Physics, Chemistry, or Biology")
    question_text: str = Field(..., description="The graduate-level question string")
    options: Dict[str, str] = Field(..., description="Multiple choice choices A, B, C, D")
    model_choice: str = Field(..., description="Selected choice from model, e.g. 'A'")
    correct_choice: str = Field(..., description="Ground truth correct option")

class EvaluationResult(BaseModel):
    question_id: str
    is_correct: bool
    discipline: str
    explanation: str

@mcp.tool(description="Evaluates a model response against GPQA ground truth assertions.")
def evaluate_gpqa_answer(task: EvaluationTask) -> EvaluationResult:
    """Validates chosen option and returns telemetry status."""
    is_correct = (task.model_choice.strip().upper() == task.correct_choice.strip().upper())
    return EvaluationResult(
        question_id=task.question_id,
        is_correct=is_correct,
        discipline=task.discipline,
        explanation="Correct choice matched model answer." if is_correct else f"Model selected {task.model_choice}, expected {task.correct_choice}"
    )

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 GPQA Accuracy & Discipline Breakdown Pipeline
Validate and aggregate GPQA accuracy stats across domains:

```python
from typing import List, Dict
from pydantic import BaseModel, Field, field_validator, ValidationError

class QuestionResult(BaseModel):
    question_id: str
    discipline: str
    is_correct: bool

    @field_validator("discipline")
    def validate_domain(cls, v):
        allowed = {"physics", "chemistry", "biology"}
        if v.lower() not in allowed:
            raise ValueError(f"Discipline must be one of {allowed}")
        return v.lower()

class GPQAReport(BaseModel):
    model_name: str
    evaluations: List[QuestionResult]

    def compute_accuracy(self) -> float:
        if not self.evaluations:
            return 0.0
        correct = sum(1 for e in self.evaluations if e.is_correct)
        return correct / len(self.evaluations)

    def breakdown_by_discipline(self) -> Dict[str, float]:
        stats: Dict[str, List[bool]] = {}
        for e in self.evaluations:
            stats.setdefault(e.discipline, []).append(e.is_correct)
        return {disc: sum(res) / len(res) for disc, res in stats.items()}

# Early 2027 Benchmark Telemetry Execution
if __name__ == "__main__":
    data = {
        "model_name": "Claude 5.1 Opus",
        "evaluations": [
            {"question_id": "GPQA_BIO_001", "discipline": "biology", "is_correct": True},
            {"question_id": "GPQA_PHYS_002", "discipline": "physics", "is_correct": True},
            {"question_id": "GPQA_CHEM_003", "discipline": "chemistry", "is_correct": False},
            {"question_id": "GPQA_PHYS_004", "discipline": "physics", "is_correct": True}
        ]
    }
    report = GPQAReport.model_validate(data)
    print(f"Model: {report.model_name}")
    print(f"Overall GPQA Accuracy: {report.compute_accuracy():.2%}")
    print(f"By Discipline: {report.breakdown_by_discipline()}")
```

### 3. SOTA GPQA Diamond Benchmarks (Early 2027 Baseline)

| Model Name | Developer | GPQA Diamond Accuracy (%) | Baseline Release |
| :--- | :--- | :--- | :--- |
| **Claude 5.1 Opus** | Anthropic | 78.4% | Late 2026 |
| **GPT-5.5** | OpenAI | 75.1% | Late 2026 |
| **Gemini 4.0 Pro** | Google | 72.8% | Late 2026 |
| **Llama 4 Maverick (70B)** | Meta AI | 69.2% | Mid 2026 |
| **DeepSeek R1 / V3** | DeepSeek | 65.0% | Early 2025 |
| PhD Human Non-Expert | Benchmark Paper | 34.0% | Late 2023 |

## Related tools / concepts
- [MMLU (Massive Multitask Language Understanding)](mmlu.md) — Multi-domain general knowledge benchmark.
- [GSM8K](gsm8k.md) — Grade school math benchmark.
- [HumanEval](human-eval.md) — Python code generation benchmark.
- [SWE-bench](swe-bench.md) — Repository-level software engineering benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) — Unified framework for model testing.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol for LLM tool integration.

## Sources / references
- [Arxiv Paper: GPQA: A Graduate-Level Google-Proof Q&A Benchmark](https://arxiv.org/abs/2311.12022)
- [GPQA Dataset on Hugging Face](https://huggingface.co/datasets/Idavidrein/gpqa)
- [LMSYS Org Benchmark Leaderboard](https://arena.lmsys.org/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
