# Humanity's Last Exam (HLE)

## What it is
HLE is a benchmark designed to test the limits of LLMs on the most difficult human-level tasks. It consists of 3,000 highly complex, multi-disciplinary questions across over a hundred subjects (Mathematics, Physics, Biology, Humanities, etc.). Created by the Center for AI Safety (CAIS) and Scale AI, it represents a "frontier" benchmark where late November/December 2026 state-of-the-art models like Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6 still perform poorly on the hardest subsets.

## What problem it solves
Addresses the "saturation" of existing benchmarks like MMLU and GPQA. As frontier models reach or exceed human-level performance on older tests, those tests lose their utility as measurement tools. HLE provides a new ceiling for July 2026 reasoning research, ensuring that progress toward expert-level agentic intelligence remains measurable.

## Where it fits in the stack
**Benchmarking**. Serves as a high-difficulty knowledge and reasoning benchmark for evaluating the upper limits of LLM and multi-modal model capabilities within agentic ingestion pipelines.

## Typical use cases
- **Frontier Model Evaluation**: Comparing the reasoning capabilities of state-of-the-art models (Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6).
- **Multi-modal Assessment**: Testing models on questions that require both textual reasoning and image understanding (14% of the dataset is multi-modal, evaluated using [ColQwen](../../knowledge_base/self-healing-agent-research.md)).
- **Calibration Testing**: Measuring whether models accurately estimate their own confidence in their answers.
- **Agentic Pre-training Validation**: Verifying that new pre-training runs have significantly moved the needle on expert-level reasoning.

## Strengths
- **Extreme Difficulty**: Designed to be the "last academic exam," remaining challenging even as models improve in July 2026.
- **Closed-ended & Verifiable**: Answers are precise, allowing for automated, low-cost evaluation via agentic satisfaction loops.
- **Subject Diversity**: Covers over 100 subjects with questions sourced from world-class experts.
- **Private Set**: Includes a held-out private set with regular rotation (v2 canary splits as of July 2026) to combat data contamination and benchmark hacking.

## Limitations
- **Not for Everyday Tasks**: Does not measure "helpful assistant" capabilities or basic instruction following.
- **Low Signal for Small Models**: Smaller or older models often score near zero, making it difficult to distinguish between them.
- **Requires LLM Judge**: While answers are closed-ended, the variety of possible formats (decimals vs. fractions) often requires an LLM judge for automated scoring at scale.

## When to use it
- When evaluating frontier models on the hardest available reasoning tasks in July 2026.
- When existing benchmarks like MMLU or GPQA show signs of saturation (models scoring >90%).
- When testing a model's ability to handle world-class scientific or mathematical problems for agentic research.

## When not to use it
- When evaluating models for general-purpose chat or basic RAG tasks.
- When you need a lightweight, fast-running benchmark for early-stage development.
- When you are optimizing for speed or low-cost inference rather than peak intelligence.

## Getting started

HLE is typically executed via the UK Government's **Inspect** framework or the **LM Evaluation Harness**.

### 1. Environment Setup
```bash
# Install inspect and the evals package
pip install inspect-ai inspect_evals

# Configure API keys for frontier models
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-proj-..."
```

### 2. Running the Benchmark
```bash
# Run HLE against a Claude 5.1 model
inspect eval inspect_evals/hle --model anthropic/claude-5-1-opus
```

## CLI examples

### Evaluation via Inspect CLI with concurrency controls
Evaluate a specific subject within HLE with adjusted concurrency:
```bash
inspect eval inspect_evals/hle \
    --model openai/gpt-5-5 \
    --limit 100 \
    --subject "quantum_physics" \
    --concurrency 10 \
    --max-connections 5
```

### Running with LM Evaluation Harness
HLE is also supported as a task in the standard harness:
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-100b,tensor_parallel_size=4 \
    --tasks hle \
    --batch_size auto
```

## API examples

### Pydantic v2 Integration & Evaluator Verification
Below is a production-ready example of evaluating and validating HLE evaluation metadata programmatically with **Pydantic v2** and **FastMCP 3.1** before logging results into multi-agent databases.

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import datetime

class HLEQuestion(BaseModel):
    question_id: str = Field(..., description="Unique ID of the HLE question")
    subject: str = Field(..., description="Academic field (e.g., Quantum Physics, Topology)")
    difficulty: int = Field(5, description="Expert difficulty tier from 1-5", ge=1, le=5)
    has_image: bool = Field(False, description="Whether the question is multi-modal and requires a vision-native parser like ColQwen")
    correct_answer: str = Field(..., description="Ground truth answer string")

class HLEEvaluationResult(BaseModel):
    model_name: str = Field(..., description="Name of the model under evaluation")
    evaluation_date: datetime = Field(default_factory=datetime.utcnow, description="When the evaluation was performed")
    total_evaluated: int = Field(..., description="Total questions processed", ge=0)
    accuracy: float = Field(..., description="Pass rate accuracy", ge=0.0, le=1.0)
    validated_questions: List[HLEQuestion] = Field(default_factory=list, description="Validated subset of questions run")

# Execute a programmatic validation of an HLE score
def validate_and_log_hle_run(run_payload: dict) -> Optional[HLEEvaluationResult]:
    try:
        # Strict schema validation using Pydantic v2 model_validate
        validated_eval = HLEEvaluationResult.model_validate(run_payload)
        print(f"Validated HLE Run: {validated_eval.model_name} achieved {validated_eval.accuracy:.2%} accuracy.")
        return validated_eval
    except ValidationError as e:
        print(f"HLE payload verification failed: {e.errors()}")
        return None

# Test the function with simulated late 2026 run data
sample_eval = {
    "model_name": "claude-5-1-opus",
    "total_evaluated": 1,
    "accuracy": 1.0,
    "validated_questions": [
        {
            "question_id": "hle-math-40291",
            "subject": "Algebraic Topology",
            "difficulty": 5,
            "has_image": False,
            "correct_answer": "Z_2"
        }
    ]
}

validated_run = validate_and_log_hle_run(sample_eval)
```

### Python Integration (Inspect AI)
Automate HLE evaluation within a research pipeline:

```python
from inspect_ai import eval, Epochs
from inspect_evals.hle import hle

# Run evaluation programmatically with custom epoch settings and model arguments
results = eval(
    tasks=hle(),
    model="anthropic/claude-5-1-sonnet",
    limit=50,
    epochs=Epochs(3, "at_least_once"),
    model_args={
        "temperature": 0.0,
        "max_tokens": 4096
    }
)

# Access scores
print(f"HLE Accuracy: {results[0].metrics['accuracy'].value}")
```

### Custom Scorer Example
Using an LLM judge to verify HLE responses:

```python
from inspect_ai.scorer import scorer, ScorerResult
from inspect_ai.solver import TaskState

@scorer(metrics=["accuracy"])
def hle_judge():
    async def score(state: TaskState, target: str):
        # Use a frontier model as a judge for complex formats
        is_correct = await judge_response(state.output.completion, target)
        return ScorerResult(
            value="CORRECT" if is_correct else "INCORRECT",
            answer=state.output.completion
        )
    return score
```

## Related tools / concepts

- [GPQA](gpqa.md) - Graduate-level Google-proof Q&A.
- [MMLU](mmlu.md) - Massive Multitask Language Understanding.
- [ARC (AI2 Reasoning Challenge)](arc.md) - Challenging questions for reasoning.
- [GSM8K](gsm8k.md) - Grade school math word problems.
- [Chatbot Arena](chatbot-arena.md) - Crowdsourced ELO ratings for LLMs.
- [SWE-bench](swe-bench.md) - Software engineering benchmark for agents.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Unified framework for running multiple benchmarks.
- [ColQwen](../../knowledge_base/self-healing-agent-research.md) - Vision-native document parsing for multi-modal HLE tasks.
- [DeepSeek R1](../../knowledge_base/self-healing-agent-research.md) - Reasoning benchmark leader in July 2026.
- [Terminus 2](terminal-bench.md) - Terminal-based reasoning benchmark.

## Sources / references
- [Humanity's Last Exam - Official Site](https://humanityslastexam.org/)
- [Scale Labs Leaderboard](https://labs.scale.com/leaderboard/humanitys_last_exam)
- [Humanity's Last Exam - arXiv Paper (2025)](https://arxiv.org/abs/2501.14249)
- [Inspect AI Documentation](https://ukgovernmentbeis.github.io/inspect_evals/)

- Last reviewed: 2026-12-29
- Confidence: high
