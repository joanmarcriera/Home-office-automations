# Humanity's Last Exam (HLE)

## What it is
HLE is a benchmark designed to test the limits of LLMs on the most difficult human-level tasks. It consists of 3,000 highly complex, multi-disciplinary questions across over a hundred subjects (Mathematics, Physics, Biology, Humanities, etc.). Created by the Center for AI Safety (CAIS) and Scale AI, it represents a "frontier" benchmark where June 2026 state-of-the-art models like Claude 4.8 and GPT-5.5 still perform poorly on the hardest subsets.

## What problem it solves
Addresses the "saturation" of existing benchmarks like MMLU and GPQA. As frontier models reach or exceed human-level performance on older tests, those tests lose their utility as measurement tools. HLE provides a new ceiling for June 2026 reasoning research, ensuring that progress toward expert-level agentic intelligence remains measurable.

## Where it fits in the stack
**Benchmarking**. Serves as a high-difficulty knowledge and reasoning benchmark for evaluating the upper limits of LLM and multi-modal model capabilities within agentic ingestion pipelines.

## Typical use cases
- **Frontier Model Evaluation**: Comparing the reasoning capabilities of state-of-the-art models (Claude 4.8 Opus, GPT-5.5, Gemini 3.5 Ultra).
- **Multi-modal Assessment**: Testing models on questions that require both textual reasoning and image understanding (14% of the dataset is multi-modal, evaluated using [ColQwen](../../knowledge_base/self-healing-agent-research.md)).
- **Calibration Testing**: Measuring whether models accurately estimate their own confidence in their answers.
- **Agentic Pre-training Validation**: Verifying that new pre-training runs have significantly moved the needle on expert-level reasoning.

## Strengths
- **Extreme Difficulty**: Designed to be the "last academic exam," remaining challenging even as models improve in June 2026.
- **Closed-ended & Verifiable**: Answers are precise, allowing for automated, low-cost evaluation via agentic satisfaction loops.
- **Subject Diversity**: Covers over 100 subjects with questions sourced from world-class experts.
- **Private Set**: Includes a held-out private set to combat data contamination and benchmark hacking (a core concern in June 2026).

## Limitations
- **Not for Everyday Tasks**: Does not measure "helpful assistant" capabilities or basic instruction following.
- **Low Signal for Small Models**: Smaller or older models often score near zero, making it difficult to distinguish between them.
- **Requires LLM Judge**: While answers are closed-ended, the variety of possible formats (decimals vs. fractions) often requires an LLM judge for automated scoring at scale.

## When to use it
- When evaluating frontier models on the hardest available reasoning tasks in June 2026.
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
```

### 2. Running the Benchmark
```bash
# Run HLE against a Claude 4.8 model
inspect eval inspect_evals/hle --model anthropic/claude-4-8-opus
```

## CLI examples

### Evaluation via Inspect CLI
Evaluate a specific subject within HLE:
```bash
inspect eval inspect_evals/hle \
    --model openai/gpt-5-5 \
    --limit 100 \
    --subject "quantum_physics"
```

### Running with LM Evaluation Harness
HLE is also supported as a task in the standard harness:
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-100b \
    --tasks hle \
    --batch_size auto
```

## API examples

### Python Integration (Inspect AI)
Automate HLE evaluation within a research pipeline:

```python
from inspect_ai import eval
from inspect_evals.hle import hle

# Run evaluation programmatically
results = eval(
    tasks=hle(),
    model="anthropic/claude-4-8-sonnet",
    limit=50,
    epochs=3
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
- [DeepSeek R1](../../knowledge_base/self-healing-agent-research.md) - Reasoning benchmark leader in June 2026.
- [Terminus 2](terminal-bench.md) - Terminal-based reasoning benchmark.

## Sources / references
- [Humanity's Last Exam - Official Site](https://humanityslastexam.org/)
- [Scale Labs Leaderboard](https://labs.scale.com/leaderboard/humanitys_last_exam)
- [Humanity's Last Exam - arXiv Paper (2025)](https://arxiv.org/abs/2501.14249)
- [Inspect AI Documentation](https://ukgovernmentbeis.github.io/inspect_evals/)

- Last reviewed: 2026-06-22
- Confidence: high
