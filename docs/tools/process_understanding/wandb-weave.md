# W&B Weave

## What it is
W&B Weave is a lightweight toolkit for building and evaluating LLM applications, developed by Weights & Biases. It provides tools for tracing, versioning, and rigorous evaluation of AI workflows and agents.

## What problem it solves
It addresses the difficulty of debugging and optimizing complex, multi-step LLM chains and agents. Weave allows developers to capture every step of an AI interaction, compare model outputs side-by-side, and run automated evaluations to improve quality, cost, and latency. In late November / December 2026, it is a primary tool for **Agent Tracing** and performance optimization for frontier models.

## Where it fits in the stack
**Category**: Process & Understanding / AI Observability & Evaluation. It acts as the "black box recorder" for agentic reasoning and tool execution.

## Typical use cases
- **Agent Tracing**: Visualizing the inner "thinking" steps and tool calls of autonomous agents like [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, Gemini 4.0, Llama 4, or GPT-5.5.
- **LLM Application Debugging**: Identifying where a prompt chain failed or where latency is accumulating.
- **Automated Evaluations**: Running scorers (e.g., toxicity, relevance, factual accuracy) against a dataset of model outputs.
- **Prompt Engineering**: Testing and versioning different prompt templates with visual comparisons.
- **MCP 3.1 / FastMCP 3.1 Trace Analysis**: Auditing Model Context Protocol (MCP) tool executions and response fidelity using the MCP 3.1 Task Protocol.

## Strengths
- **Easy Integration**: Start tracing with a single line of code (`weave.init`).
- **Standardized Traces**: Organizes logs into easy-to-navigate trace trees.
- **Agnostic**: Works with any LLM, framework (LangChain, LlamaIndex), or protocol (MCP).
- **Built-in Evaluations**: Includes out-of-the-box scorers and support for custom scoring functions.
- **Human-in-the-Loop**: Supports collecting human feedback on model outputs directly in the dashboard.
- **Native Support for GPT-5.5 and Claude 5.1**: Optimized for the latest reasoning traces from frontier models.

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
        model="gpt-5.5", # Optimized for late 2026 models
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# This call will be automatically traced in the W&B dashboard
print(call_llm("What is AI observability?"))
```

### Programmatic Trace Evaluation Verification with Strict Pydantic v2 Validation
This example demonstrates how to validate a list of trace evaluations and model scorecard scores programmatically before exporting them to downstream reporting engines.

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define strict Pydantic v2 schemas for Weave evaluation runs
class WeaveScorerResult(BaseModel):
    scorer_name: str = Field(..., pattern=r"^[a-zA-Z0-9_\-]+$")
    score: float = Field(..., ge=0.0, le=1.0)
    passed: bool

class WeaveTraceSpan(BaseModel):
    span_id: str = Field(..., pattern=r"^span_[a-f0-9]{16}$")
    trace_id: str = Field(..., pattern=r"^trace_[a-f0-9]{16}$")
    model_id: str = Field("gpt-5.5")
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    latency_sec: float = Field(..., ge=0.0)
    evaluation_scores: List[WeaveScorerResult] = Field(default_factory=list)

    @field_validator("latency_sec")
    @classmethod
    def check_unusual_latency(cls, v: float) -> float:
        if v > 10.0:
            print(f"[Warning] High execution latency recorded: {v}s")
        return v

# 2. Strict run parsing and validation
def validate_weave_trace(raw_span_data: dict) -> Optional[WeaveTraceSpan]:
    try:
        validated_span = WeaveTraceSpan.model_validate(raw_span_data)
        return validated_span
    except Exception as e:
        print(f"Weave evaluation trace validation failed: {e}")
        return None

if __name__ == "__main__":
    sample_trace_payload = {
        "span_id": "span_f8d7e6c5b4a39201",
        "trace_id": "trace_01928374abcdefab",
        "model_id": "claude-5.1-sonnet",
        "inputs": {"prompt": "Analyze the log stream for FastMCP handshakes."},
        "outputs": {"response": "Handshake succeeded under protocol version 3.1."},
        "latency_sec": 1.42,
        "evaluation_scores": [
            {
                "scorer_name": "factual-accuracy",
                "score": 0.98,
                "passed": True
            },
            {
                "scorer_name": "latency-budget",
                "score": 0.85,
                "passed": True
            }
        ]
    }

    trace_span = validate_weave_trace(sample_trace_payload)
    if trace_span:
        print(f"Weave Trace Span {trace_span.span_id} successfully validated.")
        print(f"Model Under Test: {trace_span.model_id}")
        for scorer in trace_span.evaluation_scores:
            print(f"  - Scorer: {scorer.scorer_name} | Score: {scorer.score * 100}% | Passed: {scorer.passed}")
```

### Tracing MCP 3.1 / FastMCP 3.1 Tool Calls
```python
@weave.op()
def execute_mcp_tool(tool_name: str, args: dict):
    # Tracing the tool execution step using MCP 3.1 Task Protocol
    print(f"Executing {tool_name} with {args}")
    # ... execution logic ...
    return "Tool output"
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
