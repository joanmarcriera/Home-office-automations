# JudgeGPT

## What it is
JudgeGPT is an open-source benchmarking tool that implements the **LLM-as-a-judge** paradigm. It provides a framework for using large language models to evaluate and score the outputs of other models across various dimensions like accuracy, tone, and adherence to instructions. In late November/December 2026, it is natively integrated with the **MCP 3.1 Task Protocol** (and **FastMCP 3.1**), allowing for automated, standardized qualitative assessment of agentic task completion.

## What problem it solves
It addresses the limitations of traditional, static evaluation metrics (like BLEU or ROUGE) which fail to capture the nuance, creativity, and semantic correctness of modern LLM outputs. JudgeGPT automates the labor-intensive process of human evaluation while providing more consistent and scalable results. It specifically solves the "subjectivity gap" in evaluating agentic tool-use and multi-step reasoning traces.

## Where it fits in the stack
**Benchmarking / Evaluation**. It is used in the development and fine-tuning cycle to quantify model performance. It can be integrated into [Data Copilot](../../reference-implementations/data-copilot/answer-synthesis-schema.md) workflows to validate synthesized data quality or used within [Langsmith](langsmith.md) for production monitoring.

## Typical use cases
- **Model Comparison**: Automatically scoring two different models on the same set of prompts to determine which performs better.
- **MCP 3.1 Task Evaluation**: Judging the success of automated tasks executed via the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **RLHF (Reinforcement Learning from Human Feedback)**: Generating reward signals for fine-tuning by using a high-quality "judge" model.
- **Continuous Integration for AI**: Automatically running an evaluation suite using [Promptfoo](promptfoo.md) or custom scripts.

## Strengths
- **Open Source**: Allows for customization of judging criteria and prompt templates.
- **Scalable**: Can evaluate thousands of responses quickly using frontier models like `claude-5-1-sonnet`, GPT-5.5, or Gemini 4.0 Pro.
- **Semantic Understanding**: Judges based on intent and meaning rather than just exact character matches.
- **Explanation Generation**: Provides a rationale for its score, aiding in debugging and model alignment.

## Limitations
- **Judge Bias**: The evaluation is only as good as the model used as the judge; judges can exhibit "self-preference" or "length bias."
- **Cost**: High-quality judging requires expensive frontier models for reliable results.
- **Recursive Failure**: If the judge model is less capable than the model being evaluated, the results are unreliable.

## When to use it
- When you need a scalable way to evaluate open-ended model responses or complex agentic traces.
- When building custom evaluation datasets for specialized agents.
- To automate qualitative checks in a CI/CD pipeline for generative AI.

## When not to use it
- For simple tasks that can be evaluated with deterministic code (e.g., JSON schema validation).
- If you don't have access to a sufficiently powerful model (e.g., [Gemma 3](../ai_knowledge/local_llms.md), Qwen 3.6, Llama 4 or higher) to serve as a reliable judge.

## Getting started

### Installation
JudgeGPT can be installed via pip:

```bash
pip install judgegpt-eval
```

### Basic Setup
1. Define your evaluation rubric in YAML format.
2. Provide the reference (gold standard) and model outputs.
3. Select your judge model (e.g., `gpt-5.5` or `claude-5-1-sonnet`).

## CLI examples

### Simple Model Comparison
```bash
judgegpt compare \
  --ref ./gold_standard.json \
  --model_a ./model_a_outputs.json \
  --model_b ./model_b_outputs.json \
  --judge claude-5-1-sonnet
```

### MCP 3.1 Task Audit
```bash
judgegpt audit-task \
  --task_id "research-report-001" \
  --trace_log ./logs/trace.jsonl \
  --rubric ./rubrics/agent_efficiency.yaml
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

### Programmatic Judging (Python) with strict Pydantic v2 validation
Using GPT-5.5 or Claude 5.1 as a high-fidelity judge, validating the scoring output with a Pydantic v2 model.

```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError
from judgegpt import Judge

class CriterionScore(BaseModel):
    score: float = Field(..., ge=0.0, le=10.0)
    rationale: str = Field(..., min_length=10)

class JudgeEvalOutput(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=10.0)
    criteria_breakdown: Dict[str, CriterionScore]
    final_rationale: str = Field(..., min_length=20)
    judge_model: str

def evaluate_response_safely(prompt: str, response: str, rubric_path: str) -> Optional[JudgeEvalOutput]:
    """Queries JudgeGPT using SOTA GPT-5.5 and enforces strict structural validation."""
    try:
        # Initialize GPT-5.5 as high-fidelity judge
        judge = Judge(model="gpt-5.5")

        raw_result = judge.evaluate(
            prompt=prompt,
            response=response,
            rubric=rubric_path
        )

        # Enforce validation using strict Pydantic v2 parsing
        validated_output = JudgeEvalOutput.model_validate(raw_result)
        return validated_output
    except ValidationError as e:
        print(f"Validation error on judge evaluation output: {e}")
        return None
    except Exception as e:
        print(f"Execution error running JudgeGPT: {e}")
        return None

if __name__ == "__main__":
    result = evaluate_response_safely(
        prompt="Explain quantum entanglement.",
        response="It's when particles are linked regardless of distance.",
        rubric_path="./rubric.yaml"
    )
    if result:
        print(f"Overall Score: {result.overall_score}")
        print(f"Rationale: {result.final_rationale}")
```

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) — for crowd-sourced model rankings.
- [Promptfoo](promptfoo.md) — for test-driven prompt engineering.
- [AlpacaEval](alpaca-eval.md) — an automatic evaluator for instruction-following models.
- [MT-Bench](mt-bench.md) — for multi-turn conversation evaluation.
- [Langsmith](langsmith.md) — platform for LLM application development and monitoring.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — standard for agent-tool communication.
- [Claude 5.1](../ai_knowledge/claude.md) — frequently used as a benchmark judge.

## Sources / references
- [Project JudgeGPT: Open-source LLM-as-judge](https://github.com/example/judgegpt)
- [MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/docs/concepts/tasks)
- [LLM-as-a-judge Paper (arXiv:2306.05685)](https://arxiv.org/abs/2306.05685)

## Contribution Metadata
- Last reviewed: 2026-12-15
- Confidence: high
