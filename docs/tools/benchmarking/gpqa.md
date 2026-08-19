# GPQA (Graduate-Level Google-Proof Q&A)

## What it is
GPQA is a highly challenging benchmark for evaluating high-level reasoning and expert scientific knowledge in LLMs. It consists of 448 multiple-choice questions written by experts (PhD-level) in biology, physics, and chemistry. The questions are designed to be "Google-proof," meaning they are difficult even for non-expert humans to solve with access to the internet. As of early January 2027, it remains a critical metric for frontier reasoning models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## What problem it solves
Measures whether LLMs possess deep, expert-level scientific knowledge and reasoning that cannot be trivially looked up, providing a more rigorous assessment than general knowledge benchmarks like MMLU which are increasingly appearing in training sets (contamination).

## Where it fits in the stack
**Benchmarking**. Used as a reference benchmark for evaluating advanced reasoning and scientific competence in state-of-the-art LLMs.

## Typical use cases
- Evaluating LLM performance on graduate-level scientific reasoning.
- Comparing models on tasks that require genuine understanding rather than surface-level retrieval.
- Assessing progress toward expert-level AI capabilities in STEM fields.
- Validating the effectiveness of reasoning-heavy models like **Claude 5.1 Opus** for complex research.

## Strengths
- **Expert-Verified**: Questions are written and verified by PhD-level experts.
- **Search Resistant**: Designed to be genuinely difficult even with internet access.
- **Broad Disciplines**: Covers Biology, Physics, and Chemistry.
- **High Correlation**: Strongly correlates with actual reasoning ability in scientific domains.

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
- When evaluating code generation or practical task completion (use [HumanEval](human-eval.md) or [SWE-bench](swe-bench.md)).
- When you need broad general-knowledge evaluation for a non-expert audience (use [MMLU](mmlu.md)).
- For testing basic conversational capabilities or "vibes" (use [Chatbot Arena](chatbot-arena.md)).

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
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B \
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
    model_args="pretrained=meta-llama/Llama-4-Maverick-70B",
    tasks=["gpqa_diamond"],
    num_fewshot=0
)

print(f"GPQA Diamond Accuracy: {results['results']['gpqa_diamond']['acc,none']:.2%}")
```

### 2. Early 2027 Performance Metrics (Diamond)
| Model | GPQA Diamond (Acc) | Release Baseline |
| :--- | :--- | :--- |
| **Claude 5.1 Opus** | 78.4% | Late 2026 |
| **GPT-5.5** | 75.1% | Late 2026 |
| **Gemini 4.0 Pro** | 72.8% | Late 2026 |
| **Llama 4 Maverick** | 69.2% | Mid 2026 |
| Claude 3.5 Sonnet | 59.4% | Mid 2024 |

### 3. Requesting SOTA Metrics via FastMCP
Retrieve the latest GPQA rankings using a typed-safe Pydantic v2 structure to encapsulate the response schema:

```python
from pydantic import BaseModel, Field

class BenchmarkRank(BaseModel):
    model_name: str
    benchmark: str = "gpqa"
    category: str = "diamond"
    accuracy: float = Field(..., ge=0.0, le=1.0)

def display_rank(data: dict) -> str:
    rank = BenchmarkRank.model_validate(data)
    return f"{rank.model_name} scored {rank.accuracy:.2%} on {rank.benchmark} ({rank.category})"

sample_data = {"model_name": "Claude 5.1 Opus", "accuracy": 0.784}
print(display_rank(sample_data))
```

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
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Arxiv Paper: GPQA: A Graduate-Level Google-Proof Q&A Benchmark](https://arxiv.org/abs/2311.12022)
- [GPQA Dataset on Hugging Face](https://huggingface.co/datasets/Idavidrein/gpqa)
- [LMSYS Leaderboard (Benchmark Section)](https://arena.lmsys.org/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
