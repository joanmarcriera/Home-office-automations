# JudgeGPT

## What it is
JudgeGPT is an open-source benchmarking framework that implements the **LLM-as-a-judge** paradigm. In the June 2026 landscape, it has become the standard for qualitative evaluation of frontier models like [GPT-5.5](../providers/gpt-5-5.md) and [Claude 4.8 Opus](../providers/claude.md), using high-intelligence "judge" models to score the outputs of other AI systems across complex dimensions like reasoning, nuance, and safety.

## What problem it solves
It addresses the failure of static metrics (BLEU, ROUGE) to capture semantic correctness in the era of reasoning models. JudgeGPT automates the human-in-the-loop evaluation process, providing scalable, consistent, and explainable scoring for thousands of responses. It is critical for detecting [hallucinations](../../knowledge_base/llm_security_privacy.md) and ensuring that agentic self-correction loops are actually improving output quality.

## Where it fits in the stack
**Category**: Benchmarking / Evaluation. It sits at the top of the development lifecycle, validating synthesized data in [Data Copilot](../../reference-implementations/data-copilot/answer-synthesis-schema.md) workflows and guiding [fine-tuning](../../knowledge_base/patterns/fine-tuning-open-models.md) iterations.

## Typical use cases
- **Frontier Model Comparison**: Using GPT-5.5 to score competitive outputs between Llama 4 and Mistral Large 3.
- **Agentic Quality Assurance**: Judging the multi-step execution logs of [Claude skills](../../knowledge_base/patterns/skills-best-practices.md).
- **Synthetic Data Filtering**: Automatically discarding low-quality generations during large-scale [synthetic data](../../knowledge_base/patterns/fine-tuning-open-models.md) runs.
- **Regression Testing**: Running "golden set" benchmarks in CI/CD to ensure new prompts don't degrade reasoning capabilities.

## Strengths
- **Explainability**: Provides a chain-of-thought rationale for every score, essential for debugging agent failures.
- **Rubric Flexibility**: Supports highly granular, multi-dimensional scoring rubrics (e.g., "Tone consistency" + "Technical accuracy").
- **Scalability**: Can evaluate entire datasets in minutes using high-throughput inference providers like [Fireworks AI](../providers/fireworks.md).
- **Alignment**: Allows for "Few-Shot Judging" to align the model's subjective scores with human preferences.

## Limitations
- **Judge Bias**: The evaluation is capped by the intelligence and bias of the judge model itself (e.g., the "self-preference" bias where a model favors its own style).
- **Cost**: High-fidelity judging requires frontier models which can be expensive at massive scale.
- **Verbosity Bias**: Judges can be prone to favoring longer, more confident-sounding responses even if they are factually incorrect.

## When to use it
- When you need to evaluate open-ended, creative, or reasoning-heavy model outputs where deterministic code validation is impossible.
- During the development of [autonomous agents](../agents/README.md) to verify the "correctness" of their tool-calling decisions.

## When not to use it
- For simple formatting tasks (e.g., "Is this valid JSON?") where [standard schema validators](../../knowledge_base/patterns/agentic-workflows.md) are faster and free.
- If you lack access to a model significantly more intelligent than the one being tested (the "Judge must be smarter" rule).

## Getting started

### Installation
JudgeGPT is typically used as a library or via a CLI wrapper.

```bash
pip install judgegpt-eval
```

### Initial Configuration
Set your evaluation model (e.g., GPT-5.5) and your target dataset.

```bash
export EVAL_MODEL="gpt-5-5-preview"
judgegpt init --project "homelab-evals"
```

## CLI examples

### Running a Pairwise Comparison
Compare two sets of model outputs (e.g., Llama 4 vs Claude 4.8).

```bash
judgegpt compare \
  --ref ./ground_truth.jsonl \
  --a ./llama4_results.jsonl \
  --b ./claude48_results.jsonl \
  --judge "gpt-5.5-opus"
```

### Batch Evaluation with Rubric
Run a single-model evaluation against a specific quality rubric.

```bash
judgegpt run-eval \
  --input ./agent_logs.json \
  --rubric ./rubrics/technical_support.yaml \
  --output ./eval_report.json
```

## API examples

### Python Programmatic Evaluation
Define a custom rubric and score a single response using the JudgeGPT SDK.

```python
from judgegpt import Evaluator, Rubric

# Define the criteria for the judge
rubric = Rubric(
    name="Code Quality",
    criteria={
        "correctness": "Does the code solve the problem?",
        "security": "Are there obvious injection vulnerabilities?",
        "efficiency": "Is the time complexity optimal?"
    }
)

evaluator = Evaluator(model="gpt-5.5-pro", rubric=rubric)

# Evaluate a model output
result = evaluator.evaluate(
    prompt="Write a fast prime sieve in Python.",
    response="def sieve(n): ..."
)

print(f"Score: {result.total_score}/10")
print(f"Rationale: {result.rationale}")
```

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) — Crowdsourced judge platform.
- [Promptfoo](promptfoo.md) — CLI tool for testing prompts and models.
- [AlpacaEval](alpaca-eval.md) — Simulated user-preference benchmark.
- [MT-Bench](mt-bench.md) — Multi-turn conversation benchmark.
- [GPT-5.5](../providers/gpt-5-5.md) — Premier judge-grade model.
- [Claude 4.8 Opus](../providers/claude.md) — Frontier reasoning model often used as a judge.
- [Data Copilot Synthesis](../../reference-implementations/data-copilot/answer-synthesis-schema.md) — Application of LLM-as-a-judge in synthesis.
- [AgentOps](../process_understanding/agentops.md) — Real-time monitoring of agent quality.

## Sources / references
- [LLM-as-a-judge Paper (arXiv:2306.05685)](https://arxiv.org/abs/2306.05685)
- [Project JudgeGPT GitHub](https://github.com/judgegpt/eval)
- [Evaluation in the Age of LLMs (Weights & Biases)](https://wandb.ai/site/articles/evaluation-in-the-age-of-llms)
- [GPT-5.5 Evaluation Guidelines](https://openai.com/index/gpt-5-5-evals/)

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
