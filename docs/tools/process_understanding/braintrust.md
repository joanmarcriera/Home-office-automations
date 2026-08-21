# Braintrust

Braintrust is an enterprise-grade platform for evaluating, logging, and continuous improvement of AI applications. In January 2027, it serves as an industry-standard solution for "Agent Observability," providing high-fidelity tracing infrastructure to monitor complex reasoning chains, nested execution spans, and multi-step tool interactions across frontier models like **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**.

## What it is
Braintrust is a developer-first AI evaluation and observability platform that combines interactive playground evaluation, high-fidelity agentic tracing, dataset management, and dynamic prompt versioning into a unified workflow. Featuring ergonomic Python and TypeScript SDKs, it transitions AI engineering from heuristic prompt tweaking to data-driven, quantitative software development. It features native support for **FastMCP 3.1**, allowing autonomous agents to automatically stream reasoning steps, tool invocations, and state transitions directly to nested Braintrust trace spans.

## What problem it solves
Non-deterministic AI agent failures present a primary engineering hurdle in production. Braintrust eliminates "black box" agent behavior by capturing every decision boundary, tool call, and state transition in structured, nested traces. This enables developers to pinpoint non-deterministic reasoning failures, catch regressions before deployment, and debug long-running autonomous workflows that would otherwise fail silently.

## Where it fits in the stack
**Category**: Process & Understanding / Evaluation & Observability. Braintrust sits between local development, automated CI/CD build pipelines, and production inference gateways (e.g., [LiteLLM](../../services/litellm.md)). It serves as the primary prompt management registry and the "evaluation plane" that scores model outputs across the entire application lifecycle.

## Typical use cases
- **Multi-Agent Execution Tracing**: Capturing nested asynchronous execution graphs to isolate reasoning breakdowns and tool invocation errors.
- **Automated CI/CD Regression Testing**: Executing "Golden Set" evaluation suites in Git pipelines whenever system prompts or model versions are updated.
- **Prompt Registry & Dynamic Deployment**: Managing prompt versions as code and deploying them dynamically with zero-downtime rollbacks and A/B testing.
- **Production-to-Eval Datasets**: Automatically capturing low-confidence production traces and promoting them to evaluation sets for model fine-tuning.
- **Cost & Latency Optimization**: Benchmark token expenditures, response latencies, and accuracy across provider models (e.g., comparing local **Gemma 3** / **DeepSeek-V4** vs. cloud Claude 5.1).

## Strengths
- **Developer-First Ergonomics**: Native Python and TypeScript SDKs designed for seamless integration with build tools and CI/CD pipelines.
- **High-Fidelity Agentic Tracing**: Visualization of multi-turn agent execution trees, tool parameters, and FastMCP 3.1 context payloads.
- **AI Gateway Integration**: Out-of-the-box trace logging compatibility with proxy gateways like [LiteLLM](../../services/litellm.md).
- **Automated LLM-as-a-Judge**: Custom and pre-built automated evaluation scorers running directly on real-time production streams.
- **Long-Running Session Analytics**: Built-in constructs for logging long-running agent sessions and dynamic context updates.

## Limitations
- **Commercial SaaS Core**: While client SDKs are open-source, the central analytics dashboard, prompt playground, and storage engine require commercial SaaS or private cloud hosting.
- **Instrumentation Overhead**: Deeply nested, recursive agent workflows require upfront schema design and trace annotation.
- **Storage Scaling**: High-volume real-time tracing across high-throughput agent clusters requires managed trace retention policies.

## When to use it
- When developing production autonomous agents requiring automated regression testing and continuous evaluation.
- When engineering teams require a centralized prompt management registry with dynamic versioning and A/B rollout controls.
- When integrating quantitative LLM evaluations directly into automated Git CI/CD test suites.

## When not to use it
- For single-file scripts or basic prototypes where terminal outputs and standard console loggers are sufficient.
- In air-gapped environments prohibiting third-party telemetry (unless deploying Braintrust Enterprise Private Cloud).

## Getting started

Install the Braintrust Python SDK alongside Pydantic v2:

```bash
pip install braintrust pydantic
```

Initialize project logging and record a basic evaluation event:

```python
import braintrust

# Initialize project logger
logger = braintrust.init_logger(project="Customer Intelligence Agent")

# Log evaluation record
logger.log(
    input="Analyze customer churn risk for account-402",
    output="Medium risk detected. Recommending proactive outreach.",
    expected="Medium risk detected.",
    scores={"correctness": 1.0, "latency_score": 0.95}
)
```

## CLI examples

### braintrust login
Authenticate your local shell environment with Braintrust cloud or enterprise tenant:
```bash
braintrust login --api-key YOUR_BRAINTRUST_API_KEY
```

### braintrust push
Sync local prompt definitions to the central Braintrust prompt registry:
```bash
braintrust push --project "agentic-support-v3" --file prompts.json
```

### bt eval
Run local evaluation test suites directly from terminal:
```bash
bt eval --file evals/test_agent_reasoning.py
```

## API examples

### Python: Asynchronous Nested Tracing with Pydantic v2 & FastMCP 3.1
This example demonstrates logging nested agent execution spans and validating trace payloads using **Pydantic v2** (`BaseModel`, `Field`, `model_validate`).

```python
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel, Field, ValidationError
from braintrust import init_logger, traced, current_span

init_logger(project="Agent-Tracing-2027")

class ToolExecutionTelemetry(BaseModel):
    tool_name: str = Field(..., description="Name of the executed FastMCP tool")
    arguments: Dict[str, Any] = Field(..., description="Arguments passed to the tool function")
    output: str = Field(..., description="Output string returned by the tool")
    execution_time_ms: float = Field(..., ge=0.0, description="Tool execution latency in milliseconds")
    success: bool = Field(default=True, description="Execution success status")

class AgentStepTelemetry(BaseModel):
    step_id: int = Field(..., description="Sequential index of reasoning step")
    reasoning: str = Field(..., description="Agent internal thought chain")
    executed_tools: List[ToolExecutionTelemetry] = Field(default_factory=list, description="List of tool executions")

@traced
def log_tool_span(tool_data: Dict[str, Any]) -> str:
    # Validate payload strictly with Pydantic v2
    validated_tool = ToolExecutionTelemetry.model_validate(tool_data)

    span = current_span()
    span.log(
        metadata={
            "span_type": "tool_execution",
            "mcp_version": "3.1",
            "tool_name": validated_tool.tool_name
        },
        metrics={
            "latency_seconds": validated_tool.execution_time_ms / 1000.0
        },
        output=validated_tool.output
    )
    return validated_tool.output

@traced
async def execute_agent_workflow(task_prompt: str, step_payload: Dict[str, Any]):
    span = current_span()
    span.log(input=task_prompt)

    try:
        validated_step = AgentStepTelemetry.model_validate(step_payload)
        span.log(metadata={"reasoning": validated_step.reasoning})

        for tool_data in validated_step.executed_tools:
            log_tool_span(tool_data.model_dump())

        span.log(output="Task completed successfully.")
    except ValidationError as err:
        span.log(output=f"Validation error: {err}", metrics={"failed": 1.0})

# Sample execution
sample_step = {
    "step_id": 1,
    "reasoning": "Determined user account query requires database lookup.",
    "executed_tools": [
        {
            "tool_name": "fetch_user_history",
            "arguments": {"user_id": "usr-889"},
            "output": "Found 3 recent orders.",
            "execution_time_ms": 112.4,
            "success": True
        }
    ]
}

asyncio.run(execute_agent_workflow("Fetch history for user usr-889", sample_step))
```

## Related tools / concepts
- [Arize AI](./arize-ai.md) — Enterprise ML observability and Phoenix LLM tracing platform.
- [Fiddler AI](./fiddler.md) — Enterprise explainability, guardrail evaluation, and model governance platform.
- [Comet Opik](./comet-opik.md) — Open-source LLM tracing and dataset evaluation tool.
- [Promptfoo](../benchmarking/promptfoo.md) — CLI-driven tool for local prompt evaluations and red-teaming.
- [LiteLLM](../../services/litellm.md) — AI Gateway integration layer for trace collection.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized protocol for agentic tool execution.

## Sources / references
- [Braintrust Official Platform](https://www.braintrust.dev/)
- [Braintrust Documentation & SDK Reference](https://www.braintrust.dev/docs)
- [Braintrust GitHub Repositories](https://github.com/braintrustdata)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
