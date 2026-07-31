# Braintrust

Braintrust is an enterprise-grade platform for evaluating, logging, and continuous improvement of AI applications. In the late October / November 2026 landscape, it has established itself as the premier solution for "Agent Observability," providing the high-fidelity tracing infrastructure necessary to monitor complex reasoning chains, nested execution spans, and multi-step tool interactions in frontier models like [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5, and Gemini 4.0.

## What it is
Braintrust is a comprehensive, developer-first AI evaluation and observability platform that combines automated playground evaluations, high-fidelity tracing, datasets management, and dynamic prompt versioning into a single, cohesive workflow. It provides highly ergonomic SDKs and a cloud/hybrid platform designed to move AI applications from heuristic-based testing to rigorous, data-driven engineering. By late 2026, it features native support for **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**, allowing autonomous agents to automatically report their own reasoning steps, tool calls, and state transitions directly to nested Braintrust spans via Agentic Session Orchestration.

## What problem it solves
It solves the fundamental challenge of generative AI reliability: knowing whether a change to a prompt, base model, routing logic, or retrieval strategy actually improved or degraded system performance. Braintrust eliminates the "black box" of agentic behavior by providing structured, nested tracing that captures every decision point, tool execution, and state change, making it possible to debug autonomous agents that might otherwise fail silently in production environments.

## Where it fits in the stack
**Category**: Process & Understanding / Evaluation & Observability
Braintrust sits at the intersection of the development environment and production monitoring. It acts as the "source of truth" for prompt versioning and deployment, and serves as the "evaluation plane" that scores model output across the entire lifecycle (local development, CI/CD regression testing, and production telemetry). It integrates seamlessly with FastMCP 3.1 to monitor tool discovery and low-latency execution.

## Typical use cases
- **Agent Execution Tracing**: Capturing nested, asynchronous execution graphs of multi-agent workflows to pinpoint exactly where reasoning broke down.
- **Automated Regression Testing**: Running "Golden Sets" of evaluation datasets in CI/CD pipelines whenever a system prompt or model version is updated.
- **Prompt Management & Deployment**: Versioning prompts as code and deploying them dynamically, enabling instant rollbacks and zero-downtime A/B testing.
- **Production Feedback Loops**: Automatically capturing low-confidence production traces and promoting them directly to the evaluation suite for regression tests or fine-tuning.
- **Resource Optimization**: Comparing token utilization, response times, and costs across different model providers (e.g., comparing [Gemma 3](../ai_knowledge/local_llms.md) vs. Claude 5.1).

## Strengths
- **Superior Developer Experience**: Ergonomic SDKs (Python and TypeScript) and a powerful CLI that integrate seamlessly with modern build systems and CI/CD.
- **High-Fidelity Tracing**: Industry-leading visualization of complex, multi-turn agent spans utilizing the MCP 3.1 Task Protocol.
- **Inference Proxy Compatibility**: Out-of-the-box support for logging traffic from proxy layers like [LiteLLM](../../services/litellm.md).
- **LLM-as-a-Judge Automation**: Capability to run automated, real-time evaluation scorers on production data with minimal latency.
- **Agentic Session Orchestration**: Specialized structures to log and analyze long-running agent sessions with dynamic context loading.

## Limitations
- **Pricing**: Primarily a commercial SaaS service; while it offers a generous free tier for developer sandboxes, enterprise scale logs require substantial investment.
- **Configuration Overhead**: Constructing detailed, nested traces for highly complex or recursive agentic applications requires careful SDK instrumenting.
- **Proprietary Core**: While SDKs are open-source, the main analytical dashboards, embedding projectors, and prompt playgrounds are closed-source SaaS.

## When to use it
- When building production-ready AI agents that require strict reliability, automated regressions testing, and continuous optimization.
- When teams need a shared, collaborative platform to iterate on prompt structures and compare model outputs.
- When you need to integrate LLM evaluations directly into automated Git-based CI/CD workflows.

## When not to use it
- For trivial, single-file scripts or simple hobby applications where terminal outputs or basic console logs are sufficient.
- If strict compliance demands a 100% air-gapped environment with absolutely zero telemetry sent to third-party dashboards (unless utilizing Braintrust Private Cloud options).

## Getting started

Install the Braintrust SDK along with Pydantic for validation support:

```bash
pip install braintrust pydantic
```

Initialize a project and track a basic experiment:

```python
import braintrust

# Login and initialize project logging
logger = braintrust.init_logger(project="Customer Intelligence Agent")

# Log a simple run
logger.log(
    input="Analyze customer churn risk for account-402",
    output="Medium risk detected. Recommending outreach.",
    expected="Medium risk detected.",
    scores={"correctness": 1.0}
)
```

## CLI examples

### braintrust login
Authenticate your local environment with the Braintrust cloud or private instance:
```bash
braintrust login --api-key YOUR_BRAINTRUST_API_KEY
```

### braintrust push
Deploys local prompt configurations to the registry:
```bash
braintrust push --project "support-agent-mcp-3.1" --file prompts.json
```

### bt eval
Use the `bt` command-line utility to run local evaluation suites in your terminal:
```bash
bt eval --file evals/test_reasoning.py
```

## API examples

### Python (Asynchronous Nested Tracing & Pydantic v2 Schema Validation)
This example shows how to configure detailed, nested agent trace spans for a tool-use cycle leveraging FastMCP 3.1, validating telemetry payloads with Pydantic v2:

```python
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from braintrust import init_logger, traced, current_span

# Initialize the project logger
init_logger(project="Multi-Agent-MCP-3.1")

# Define our trace schema using Pydantic v2
class ToolExecutionTelemetry(BaseModel):
    tool_name: str = Field(..., description="The name of the tool executed.")
    arguments: Dict[str, Any] = Field(..., description="The arguments passed to the tool.")
    output: str = Field(..., description="The stringified response from the tool.")
    execution_time_ms: float = Field(..., ge=0.0, description="Latency of tool execution.")
    success: bool = Field(default=True, description="Status of the tool execution.")

class AgentStepTelemetry(BaseModel):
    step_id: int = Field(..., description="Sequential index of reasoning step.")
    reasoning: str = Field(..., description="The thought process or raw reasoning chain of the agent.")
    executed_tools: List[ToolExecutionTelemetry] = Field(default_factory=list, description="All tools executed during this step.")

# Use the @traced decorator to automatically generate parent/child trace spans
@traced
def log_tool_span(tool_data: Dict[str, Any]) -> str:
    # Validate the tool telemetry with Pydantic v2
    validated_tool = ToolExecutionTelemetry(**tool_data)

    # Access the active Braintrust trace span and record metadata
    span = current_span()
    span.log(
        metadata={
            "span_type": "tool_execution",
            "mcp_version": "3.1",
            "tool_name": validated_tool.tool_name
        },
        metrics={
            "latency": validated_tool.execution_time_ms / 1000.0
        },
        output=validated_tool.output
    )
    return validated_tool.output

@traced
async def run_agent_reasoning_chain(task_description: str, step_data: Dict[str, Any]):
    span = current_span()
    span.log(input=task_description)

    # Process reasoning steps and execute tools
    validated_step = AgentStepTelemetry(**step_data)

    span.log(metadata={"reasoning_chain": validated_step.reasoning})

    for tool_payload in validated_step.executed_tools:
        # Calling the traced tool function establishes a child span automatically
        log_tool_span(tool_payload)

    span.log(output="Completed task successfully.")

# Mock telemetry data
mock_step = {
    "step_id": 1,
    "reasoning": "Determined that database querying is required for user history.",
    "executed_tools": [
        {
            "tool_name": "fetch_user_history",
            "arguments": {"user_id": "usr-889"},
            "output": "Returned 3 orders in last 30 days.",
            "execution_time_ms": 145.2,
            "success": True
        }
    ]
}

# Run the async tracing loop
asyncio.run(run_agent_reasoning_chain("Summarize recent history for usr-889", mock_step))
```

## Related tools / concepts
- [Arize AI](./arize-ai.md) — Real-time production MPM and Phoenix developer tools.
- [Fiddler AI](./fiddler.md) — Focuses on enterprise explainability and model governance.
- [Comet Opik](./comet-opik.md) — Open-source LLM tracing and dataset management.
- [LangSmith](../benchmarking/langsmith.md) — Observability platform built specifically for the LangChain ecosystem.
- [Promptfoo](../benchmarking/promptfoo.md) — CLI-first tool for prompt testing and evaluations.
- [LiteLLM](../../services/litellm.md) — Standardized multi-model gateway often serving as Braintrust's logging source.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Open protocol defining standardized tool use.

## Sources / references
- [Braintrust Platform Homepage](https://www.braintrust.dev/)
- [Braintrust Official SDK & API Reference Documentation](https://www.braintrust.dev/docs)
- [Braintrust GitHub Repositories](https://github.com/braintrustdata)
- [Braintrust Agentic Tracing Guide (2026)](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
