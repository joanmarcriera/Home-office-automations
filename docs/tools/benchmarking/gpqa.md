# GPQA (Graduate-Level Google-Proof Q&A)

## What it is
GPQA is a highly challenging benchmark for evaluating high-level reasoning and scientific knowledge in LLMs. It consists of 448 multiple-choice questions written by experts (PhD-level) in biology, physics, and chemistry. The questions are designed to be "Google-proof," meaning they are exceptionally difficult even for non-expert humans to solve with access to the internet. As of late October / November 2026, it remains a critical metric for frontier reasoning models like **Claude 5.1** and **GPT-5.5**.

## What problem it solves
Measures whether LLMs possess deep, expert-level scientific knowledge and reasoning that cannot be trivially looked up, providing a more rigorous assessment than general knowledge benchmarks like MMLU which are increasingly appearing in training sets (contamination).

## Where it fits in the stack
**Benchmarking**. Used as a primary reference benchmark for evaluating advanced reasoning and scientific competence in state-of-the-art LLMs.

## Typical use cases
- Evaluating LLM performance on graduate-level scientific reasoning.
- Comparing models on tasks that require genuine understanding rather than surface-level retrieval.
- Assessing progress toward expert-level AI capabilities in STEM fields.
- Validating the effectiveness of reasoning-heavy models like **Claude 5.1 Opus** for complex research.

## Strengths
- **Expert-Verified**: Questions are written and verified by PhD-level experts.
- **Search Resistant**: Designed to be genuinely difficult even with internet access.
- **Broad Disciplines**: Covers Biology, Physics, and Chemistry.
- **High Correlation**: Strongly correlates with actual reasoning ability in scientific domains and autonomous research.

## Limitations
- **Limited Scale**: Small dataset (448 questions) may not cover all scientific sub-domains.
- **Domain Focus**: Primarily "hard" sciences; does not cover humanities or social sciences.
- **Format**: Multiple-choice format may not fully capture open-ended reasoning ability.
- **Expert Requirement**: High barrier to entry for human verification (requires PhDs).

## When to use it
- When comparing frontier LLMs on their ability to handle difficult, expert-level scientific questions.
- When you need a benchmark that is resistant to memorization and search-engine shortcuts.
- To evaluate models designed specifically for deep research and reasoning.

## When not to use it
- When evaluating code generation or practical task completion (use [HumanEval](human-eval.md) or [SWE-bench](swe-bench.md) instead).
- When you need broad general-knowledge evaluation for a non-expert audience (use [MMLU](mmlu.md) instead).
- For testing basic conversational capabilities or "vibes" (use [Chatbot Arena](chatbot-arena.md) instead).

## Getting started

GPQA is typically run using evaluation frameworks like the LM Evaluation Harness or proprietary evaluation pipelines for closed models.

1. Install the LM Evaluation Harness: `pip install lm-eval`
2. Prepare your model (Hugging Face or API-based).
3. Run the GPQA task against your model using the CLI.

## CLI examples

### 1. Running GPQA via LM Evaluation Harness
Evaluate a local Hugging Face model on the primary GPQA dataset:

```bash
python -m lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4 \
    --tasks gpqa_diamond \
    --device cuda:0 \
    --batch_size 1
```

### 2. Evaluating an API-based model
Compare performance of a reasoning model via an API provider:

```bash
python -m lm_eval --model anthropic \
    --model_args model=claude-5-1-opus-20261031 \
    --tasks gpqa_main \
    --limit 50
```

### 3. Inspecting the dataset
Use `huggingface-cli` to download and inspect:
```bash
huggingface-cli download Idavidrein/gpqa --repo-type dataset
```

## API examples

### 1. Python: Programmatic Evaluation
Using the `lm_eval` library to run benchmarks within a Python script:

```python
import lm_eval

results = lm_eval.simple_evaluate(
    model="hf",
    model_args="pretrained=meta-llama/Llama-4",
    tasks=["gpqa_diamond"],
    num_fewshot=0
)

print(f"GPQA Diamond Accuracy: {results['results']['gpqa_diamond']['acc,none']:.2%}")
```

### 2. Python: Structured Response Validation with Pydantic v2
Validate multiple-choice reasoning outputs for graduate-level scientific responses using modern Pydantic v2 specifications with strict type-hints:

```python
import json
from typing import List, Literal
from pydantic import BaseModel, Field, TypeAdapter

class ScientificResponse(BaseModel):
    reasoning_trace: List[str] = Field(..., description="Decomposed step-by-step scientific validation traces.")
    selected_option: Literal["A", "B", "C", "D"] = Field(..., description="The chosen answer option.")
    confidence_score: float = Field(..., description="Self-reported confidence level between 0.0 and 1.0.")

# Simulated model JSON output response
raw_response: str = """{
  "reasoning_trace": [
    "Identify the compound structure and lone pair distribution.",
    "Calculate steric number: 5 valence electrons + 3 single bonds - 1 charge.",
    "Apply VSEPR theory to find the molecular geometry."
  ],
  "selected_option": "B",
  "confidence_score": 0.95
}"""

# Use Pydantic v2 TypeAdapter for validation
adapter: TypeAdapter[ScientificResponse] = TypeAdapter(ScientificResponse)
scientific_validation: ScientificResponse = adapter.validate_json(raw_response)

print(f"Validated Option: {scientific_validation.selected_option}")
print(f"Confidence Score: {scientific_validation.confidence_score:.2f}")
assert scientific_validation.selected_option == "B"
```

### 3. November 2026 Performance Metrics (Diamond)
| Model | GPQA Diamond (Acc) | Release Date |
| :--- | :--- | :--- |
| **Claude 5.1 Opus** | 82.4% | October 2026 |
| **GPT-5.5** | 79.5% | April 2026 |
| **Gemini 4.0 Ultra** | 78.1% | September 2026 |
| **Qwen 3.6 Instruct** | 73.2% | August 2026 |
| **Llama 4** | 72.8% | June 2026 |
| Claude 3.5 Sonnet | 59.4% | June 2024 |
| GPT-4o | 53.6% | May 2024 |

## Related tools / concepts
- [MMLU (Massive Multitask Language Understanding)](mmlu.md)
- [GSM8K (Grade School Math 8K)](gsm8k.md)
- [HumanEval](human-eval.md)
- [Chatbot Arena](chatbot-arena.md)
- [SWE-bench](swe-bench.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [Anthropic](../providers/anthropic.md)
- [OpenAI](../ai_knowledge/openai.md)
- [Hugging Face](../providers/huggingface.md)
- [Math Benchmark](math-benchmark.md)

## Sources / references
- [Arxiv Paper: GPQA: A Graduate-Level Google-Proof Q&A Benchmark](https://arxiv.org/abs/2311.12022)
- [GPQA Dataset on Hugging Face](https://huggingface.co/datasets/Idavidrein/gpqa)
- [LMSYS Leaderboard (Benchmark Section)](https://arena.lmsys.org/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
