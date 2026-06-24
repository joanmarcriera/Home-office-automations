# JudgeGPT

## What it is
JudgeGPT is an open-source benchmarking tool that implements the **LLM-as-a-judge** paradigm. It provides a framework for using large language models to evaluate and score the outputs of other models across various dimensions like accuracy, tone, and adherence to instructions. It is often used alongside other [benchmarking tools](../benchmarking/index.md) to provide qualitative analysis.

## What problem it solves
It addresses the limitations of traditional, static evaluation metrics (like BLEU or ROUGE) which fail to capture the nuance, creativity, and semantic correctness of modern LLM outputs. JudgeGPT automates the labor-intensive process of human evaluation while providing more consistent and scalable results. It helps in identifying [hallucinations](../../knowledge_base/llm_security_privacy.md) and regressions in complex reasoning tasks.

## Where it fits in the stack
**Benchmarking / Evaluation**. It is used in the development and fine-tuning cycle to quantify model performance. It can be integrated into [Data Copilot](../../reference-implementations/data-copilot/answer-synthesis-schema.md) workflows to validate synthesized data quality.

## Typical use cases
- **Model Comparison**: Automatically scoring two different models on the same set of prompts to determine which performs better.
- **RLHF (Reinforcement Learning from Human Feedback)**: Generating reward signals for [fine-tuning](../../knowledge_base/patterns/fine-tuning-open-models.md) by using a high-quality "judge" model.
- **Continuous Integration for AI**: Automatically running an evaluation suite using [Promptfoo](promptfoo.md) or custom scripts.
- **Skill Validation**: Evaluating the effectiveness of [Claude skills](../../knowledge_base/patterns/skills-best-practices.md) by judging their execution logs.

## Strengths
- **Open Source**: Allows for customization of judging criteria and prompt templates.
- **Scalable**: Can evaluate thousands of responses quickly using frontier models like `claude-4-8-opus-20260528`.
- **Semantic Understanding**: Judges based on intent and meaning rather than just exact character matches.
- **Explanation Generation**: Provides a rationale for its score, aiding in debugging and model alignment.

## Limitations
- **Judge Bias**: The evaluation is only as good as the model used as the judge; judges can exhibit their own biases or "self-preference."
- **Cost**: High-quality judging requires expensive models (e.g., [Claude 4.8 Opus](../ai_knowledge/claude.md) or GPT-5.5).
- **Length Bias**: Judges sometimes favor longer responses regardless of quality, requiring careful rubric calibration.

## When to use it
- When you need a scalable way to evaluate open-ended model responses.
- When building custom evaluation datasets for specialized [agents](../agents/index.md).
- To automate qualitative checks in a CI/CD pipeline for generative AI.

## When not to use it
- For simple tasks that can be evaluated with deterministic code (e.g., JSON schema validation).
- If you don't have access to a sufficiently powerful model (e.g., Llama 4 Maverick or higher) to serve as a reliable judge.

## Getting started

### Installation
JudgeGPT can be installed via pip (example for a hypothetical CLI):

```bash
pip install judgegpt-eval
```

### Basic Setup
1. Define your evaluation rubric in YAML format.
2. Provide the reference (gold standard) and model outputs.
3. Select your judge model (e.g., `gpt-5.5` or `claude-4-8-opus`).

## CLI examples

### Simple Model Comparison
```bash
judgegpt compare \
  --ref ./gold_standard.json \
  --model_a ./model_a_outputs.json \
  --model_b ./model_b_outputs.json \
  --judge claude-4-8-opus
```

### Run Evaluation Suite
```bash
judgegpt run --config ./eval_config.yaml --output results.json
```

## API examples

### Custom Evaluation Rubric (YAML)
Define how the judge should evaluate the responses.

```yaml
rubric:
  name: "Technical Support Quality"
  criteria:
    accuracy:
      weight: 0.5
      description: "Is the technical advice correct and safe to follow?"
    empathy:
      weight: 0.2
      description: "Does the model acknowledge the user's frustration?"
    actionability:
      weight: 0.3
      description: "Are the steps provided clear and numbered?"
```

### Programmatic Judging (Python)
```python
from judgegpt import Judge

judge = Judge(model="claude-4-8-opus-20260528")

result = judge.evaluate(
    prompt="Explain quantum entanglement.",
    response="It's when particles are linked regardless of distance.",
    rubric="./rubric.yaml"
)

print(f"Score: {result.score}")
print(f"Rationale: {result.rationale}")
```

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) — for crowd-sourced model rankings
- [Promptfoo](promptfoo.md) — for test-driven prompt engineering
- [AlpacaEval](alpaca-eval.md) — an automatic evaluator for instruction-following models
- [MT-Bench](mt-bench.md) — for multi-turn conversation evaluation
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — for improving model performance
- [Claude Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — for developing agentic capabilities
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md) — for safety benchmarking
- [Data Copilot Synthesis](../../reference-implementations/data-copilot/answer-synthesis-schema.md) — for generating high-quality training data

## Sources / references
- [Project JudgeGPT: Open-source LLM-as-judge](https://www.reddit.com/r/MachineLearning/comments/1rsxcl3/project_judgegpt_opensource_llmasjudge/)
- [LLM-as-a-judge Paper (arXiv)](https://arxiv.org/abs/2306.05685)
- [Evaluation in the Age of LLMs (Weights & Biases)](https://wandb.ai/site/articles/evaluation-in-the-age-of-llms)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
