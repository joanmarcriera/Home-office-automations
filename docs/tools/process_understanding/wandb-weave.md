# W&B Weave

## What it is
W&B Weave is a lightweight toolkit for building and evaluating LLM applications, developed by Weights & Biases. It provides tools for tracing, versioning, and rigorous evaluation of AI workflows and agents.

## What problem it solves
It addresses the difficulty of debugging and optimizing complex, multi-step LLM chains and agents. Weave allows developers to capture every step of an AI interaction, compare model outputs side-by-side, and run automated evaluations to improve quality, cost, and latency. In late December 2026, it is a primary tool for **Agent Tracing** and performance optimization for frontier models like Claude 5.1, GPT-5.5, and Gemma 3.

## Where it fits in the stack
**Category**: Process & Understanding / AI Observability & Evaluation. It acts as the "black box recorder" for agentic reasoning and tool execution.

## Typical use cases
- **Agent Tracing**: Visualizing the inner "thinking" steps and tool calls of autonomous agents like [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, or GPT-5.5.
- **LLM Application Debugging**: Identifying where a prompt chain failed or where latency is accumulating.
- **Automated Evaluations**: Running scorers (e.g., toxicity, relevance, factual accuracy) against a dataset of model outputs.
- **Prompt Engineering**: Testing and versioning different prompt templates with visual comparisons.
- **MCP 3.1 Trace Analysis**: Auditing Model Context Protocol (MCP) tool executions and response fidelity using the MCP 3.1 and FastMCP 3.1 Task Protocols.

## Strengths
- **Easy Integration**: Start tracing with a single line of code (`weave.init`).
- **Standardized Traces**: Organizes logs into easy-to-navigate trace trees.
- **Agnostic**: Works with any LLM, framework (LangChain, LlamaIndex), or protocol (MCP).
- **Built-in Evaluations**: Includes out-of-the-box scorers and support for custom scoring functions.
- **Human-in-the-Loop**: Supports collecting human feedback on model outputs directly in the dashboard.
- **Native Support for O4/GPT-5.5/Claude 5.1**: Optimized for the latest reasoning traces from frontier models.

## Limitations
- **Cloud Dependency**: While highly integrated, it primarily relies on the Weights & Biases cloud platform for visualization.
- **Evolving Product**: As a newer addition to the W&B ecosystem, features and APIs are rapidly evolving.

## When to use it
- When building complex LLM applications where tracing internal state and tool calls is critical.
- When you need a lightweight way to run evaluations and score model performance across datasets.
- If you are already using Weights & Biases for traditional machine learning and want a unified observability platform.
- To audit the behavior of autonomous agents in production using FastMCP 3.1.

## When not to use it
- For simple, single-prompt applications where the overhead of tracing outweighs the benefits.
- If you require a fully air-gapped or self-hosted observability solution (though W&B offers enterprise self-hosting).

## Getting started

### Installation
```bash
pip install weave wandb pydantic>=2.0
```

## CLI examples
```bash
# Login to Weights & Biases
wandb login

# Initialize a new W&B project (Weave uses W&B projects for storage)
wandb init --project my-weave-app

# List runs in the current project
wandb runs
```

## API examples

### Basic Tracing with Decorators
```python
import weave
import openai

# Initialize Weave with a project name
weave.init("my-llm-app")

@weave.op()
def call_llm(prompt: str):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.5", # Optimized for late December 2026 models
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# This call will be automatically traced in the W&B dashboard
print(call_llm("What is AI observability?"))
```

### Trace Audits and Pydantic v2 Evaluation Validation
This script demonstrates how to define strict evaluation scorecards for agent evaluations and validate them using Pydantic v2 schemas before submitting trace logs to Weights & Biases Weave.

```python
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field
import weave

# 1. Define strict evaluation metrics with strict Pydantic v2 rules
class WeaveScorerMetric(BaseModel):
    metric_name: str = Field(..., min_length=2)
    score: float = Field(..., ge=0.0, le=1.0)
    passed: bool
    rationale: str = Field(..., min_length=10)

class EvaluationRecord(BaseModel):
    record_id: str = Field(..., min_length=5)
    model_version: str = Field(..., description="E.g. gpt-5.5, claude-5.1")
    latency_ms: float = Field(..., gt=0.0)
    metrics: List[WeaveScorerMetric] = Field(..., min_length=1)
    meta_tags: Dict[str, str] = Field(default_factory=dict)

# 2. Run and validate traces in Weave
weave.init("agentic-evaluations-v5")

@weave.op()
def publish_validated_eval(record_data: EvaluationRecord) -> dict:
    # Log evaluated telemetry parameters inside Weave's operation run
    log_payload = {
        "record_id": record_data.record_id,
        "model": record_data.model_version,
        "latency_ms": record_data.latency_ms,
        "aggregate_pass": all(m.passed for m in record_data.metrics),
        "tags": record_data.meta_tags
    }

    # Return structured summary for Weave tracing logs
    return log_payload

if __name__ == "__main__":
    try:
        # Create a validated Evaluation Record
        eval_record = EvaluationRecord(
            record_id="rec-88741",
            model_version="claude-5.1-sonnet",
            latency_ms=1250.5,
            metrics=[
                WeaveScorerMetric(
                    metric_name="factual_relevance",
                    score=0.98,
                    passed=True,
                    rationale="The response was 100% grounded in the input context docs."
                ),
                WeaveScorerMetric(
                    metric_name="safety_guardrail",
                    score=1.00,
                    passed=True,
                    rationale="No toxic phrases, PII leakage, or prompt-injection attempts detected."
                )
            ],
            meta_tags={"environment": "production-eval", "runner": "fastmcp-3.1"}
        )

        # Call the traced operation with the Pydantic validated object
        summary = publish_validated_eval(eval_record)
        print(f"Traced evaluation summary successfully logged: {summary}")
    except Exception as e:
        print(f"Validation failure: {e}")
```

## Related tools / concepts
- [Langfuse](langfuse.md)
- [AgentOps](agentops.md)
- [Braintrust](braintrust.md)
- [Comet Opik](comet-opik.md)
- [OpenRouter](../ai_knowledge/openrouter.md) (Streams traces to Weave)
- [Arize AI](arize-ai.md)
- [Ragas](ragas.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Weights & Biases (Core)](https://wandb.ai/)
- [Claude 5.1](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)

## Sources / references
- [W&B Weave Website](https://wandb.ai/site/weave/)
- [Weave Documentation](https://weave-docs.wandb.ai/)
- [OpenRouter Weave Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/wandb-weave)

## Contribution Metadata
- Last reviewed: 2026-12-06
- Confidence: high
