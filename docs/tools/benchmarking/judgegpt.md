# JudgeGPT

## What it is
JudgeGPT is an open-source benchmarking tool that implements the **LLM-as-a-judge** paradigm. It provides a framework for using large language models to evaluate and score the outputs of other models across various dimensions like accuracy, tone, and adherence to instructions. It is often used alongside other [benchmarking tools](../benchmarking/README.md) to provide qualitative analysis.

## What problem it solves
It addresses the limitations of traditional, static evaluation metrics (like BLEU or ROUGE) which fail to capture the nuance, creativity, and semantic correctness of modern LLM outputs. JudgeGPT automates the labor-intensive process of human evaluation while providing more consistent and scalable results. It helps in identifying [hallucinations](../../knowledge_base/llm_security_privacy.md) and regressions in complex reasoning tasks.

## Where it fits in the stack
**Benchmarking / Evaluation**. It is used in the development and fine-tuning cycle to quantify model performance. It can be integrated into [Data Copilot](../../reference-implementations/data-copilot/answer-synthesis-schema.md) workflows to validate synthesized data quality.

## Typical use cases
- **Model Comparison**: Automatically scoring two different models on the same set of prompts to determine which performs better.
- **RLHF (Reinforcement Learning from Human Feedback)**: Generating reward signals for [fine-tuning](../../knowledge_base/patterns/fine-tuning-open-models.md) by using a high-quality "judge" model.
- **Continuous Integration for AI**: Automatically running an evaluation suite using [Promptfoo](promptfoo.md) or custom scripts.
- **Skill Validation**: Evaluating the effectiveness of [Claude skills](../../knowledge_base/patterns/skills-best-practices.md) by judging their execution logs.

## Key Features
- **Customizable Rubrics**: Define specific criteria (e.g., "conciseness", "technical accuracy") for the judge to follow.
- **Few-Shot Prompting**: Provide examples of "good" and "bad" judging to align the model's behavior.
- **Pairwise Ranking**: Ask the judge to choose the best of two outputs (Head-to-head) similar to [Chatbot Arena](chatbot-arena.md).
- **Explanation Generation**: The judge provides a rationale for its score, aiding in debugging.

## Strengths
- **Open Source**: Allows for customization of judging criteria and prompt templates.
- **Scalable**: Can evaluate thousands of responses quickly.
- **Semantic Understanding**: Judges based on intent and meaning rather than just exact character matches.

## Limitations
- **Judge Bias**: The evaluation is only as good as the model used as the judge; judges can exhibit their own biases.
- **Cost**: High-quality judging often requires expensive models (e.g., [Claude 3.5 Opus](../providers/claude.md)).
- **Length Bias**: Judges sometimes favor longer responses regardless of quality.

## When to use it
- When you need a scalable way to evaluate open-ended model responses.
- When building custom evaluation datasets for specialized [agents](../agents/README.md).

## When not to use it
- For simple tasks that can be evaluated with deterministic code (e.g., JSON schema validation).
- If you don't have access to a sufficiently powerful model (e.g., [Qwen](qwen.md) 72B or higher) to serve as a reliable judge.

## Getting started

### Installation
JudgeGPT can be installed via pip (example for a hypothetical CLI):

```bash
pip install judgegpt-eval

# Run a simple evaluation between two model outputs
judgegpt compare --ref ./gold_standard.json --model_a ./model_a_outputs.json --model_b ./model_b_outputs.json
```

## Technical examples

### Evaluation Rubric (YAML)
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

### Judging Prompt Template
The underlying prompt used to instruct the LLM-as-a-judge.

```text
You are an expert technical reviewer. Evaluate the following AI response based on the provided rubric.
Response: {{model_output}}
Context: {{system_prompt}}

Score each criterion from 1-10 and provide a brief rationale.
Output your evaluation in JSON format.
```

## Maintenance & Troubleshooting
- **Inter-Rater Reliability**: Periodically compare JudgeGPT's scores with human scores to ensure alignment.
- **Judge Upgrade**: When a more powerful model (like [Claude 3.5 Sonnet](../providers/claude.md)) is released, re-run evaluations to see if the "truth" has changed.

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md)
- [Promptfoo](promptfoo.md)
- [AlpacaEval](alpaca-eval.md)
- [MT-Bench](mt-bench.md)
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md)
- [Claude Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md)
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md)
- [Data Copilot Synthesis](../../reference-implementations/data-copilot/answer-synthesis-schema.md)

## Sources / References
- [Project JudgeGPT: Open-source LLM-as-judge](https://www.reddit.com/r/MachineLearning/comments/1rsxcl3/project_judgegpt_opensource_llmasjudge/)
- [LLM-as-a-judge Paper (arXiv)](https://arxiv.org/abs/2306.05685)
- [Evaluation in the Age of LLMs (Weights & Biases)](https://wandb.ai/site/articles/evaluation-in-the-age-of-llms)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
