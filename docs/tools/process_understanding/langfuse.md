# Langfuse

## What it is
Langfuse is an open-source LLM engineering platform designed for tracing, observability, metrics, prompt management, and automated evaluation. In early January 2027, it serves as a core control center for engineering teams building, debugging, and scaling complex multi-agent applications powered by frontier models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## What problem it solves
Non-deterministic LLM agent interactions, nested tool executions, and dynamic context retrieval make traditional application monitoring tools inadequate. Langfuse provides granular visibility into execution graphs:
- **Trace Transparency**: Visualizing multi-step agent loops, tool invocations, and retrieval steps in autonomous workflows.
- **Cost & Latency Auditing**: Accurate tracking of token consumption, API expenditures, and performance bottlenecks across diverse cloud and local providers.
- **Evaluation & Quality Assurance**: Automated LLM-as-a-judge pipelines, user feedback scoring, and offline dataset benchmarking.
- **Prompt Lifecycle Management**: Versioned prompt management with zero-code UI deployments to decouple prompt engineering from code production releases.
- **MCP Session Observability**: Auditing **Model Context Protocol (FastMCP 3.1)** connection lifetimes, tool executions, and context delivery.

## Where it fits in the stack
**Process Understanding / Observability & Evaluation**. Langfuse sits between LLMs, orchestration frameworks (like LangChain, LangGraph, and AutoGen), and gateways (like [LiteLLM](../../services/litellm.md)), capturing telemetry data in real time. It frequently utilizes [ClickHouse](clickhouse.md) as a high-speed columnar backend for scale analytics.

## Typical use cases
- **Debugging Multi-Agent Systems**: Tracing complex state transitions and identifying hallucination origins in frameworks like LangGraph or AutoGen.
- **Regression Benchmarking**: Running automated evaluation suites on custom datasets before deploying prompt revisions or model switches.
- **Production Performance Monitoring**: Tracking live latency, user feedback ratings, and operational costs across production models.
- **Centralized Prompt Engineering**: Managing versioned system prompts in the Langfuse UI and fetching them dynamically via API.
- **FastMCP Protocol Auditing**: Telemetry tracking for FastMCP 3.1 tool calls and server resource lookups.

## Strengths
- **Open-Source & Self-Hostable**: Full data governance and privacy control, supporting deployment in regulated enterprise environments.
- **Low-Overhead Asynchronous SDKs**: Non-blocking telemetry collectors designed to prevent latency penalties on user queries.
- **Extensive Framework Compatibility**: Native SDK wrappers for OpenTelemetry, OpenAI, Anthropic, LangChain, LlamaIndex, and FastMCP.
- **ClickHouse Analytics Engine**: Scalable backend supporting high-cardinality analytical queries across millions of daily traces.

## Limitations
- **Operational Infrastructure Requirements**: Self-hosting requires managing PostgreSQL (metadata), ClickHouse (analytics), and Redis (queue processing).
- **Analytics Queue Delays**: Under massive event ingestion spikes, live dashboard reporting can experience brief propagation delays.
- **Platform Learning Curve**: Mastering advanced features like multi-step dataset evaluations and custom judge scoring requires technical onboarding.

## When to use it
- When building non-trivial agentic applications requiring deep visual tracing across nested tool calls.
- When enterprise compliance or data residency rules demand a fully self-hosted observability solution.
- When you require structured LLM-as-a-judge automated benchmarking alongside human feedback collection.

## When not to use it
- For basic single-turn LLM completions where standard application logs are sufficient.
- If you prefer a fully managed SaaS platform and do not want to manage telemetry infrastructure (though Langfuse Cloud is available).

## Getting started

### 1. Installation
Install the Langfuse Python SDK:
```bash
pip install langfuse
```

### 2. Basic Integration (OpenAI / GPT-5.5)
Wrap the OpenAI client to automatically capture traces:

```python
import os
from langfuse.openai import openai

# Configure environment variables
# os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
# os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
# os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

response = openai.chat.completions.create(
    model="gpt-5.5-preview",
    messages=[{"role": "user", "content": "How does Langfuse enhance agent observability?"}],
    name="agent-obs-trace"
)

print(response.choices[0].message.content)
```

## CLI examples

### Installation & Setup
Install the Langfuse CLI helper tool:
```bash
npm install -g langfuse
```

### Health Check Execution
Verify connectivity to your local or cloud Langfuse server:
```bash
langfuse health
```

### Exporting Telemetry Traces
Export traces for offline audit or dataset construction:
```bash
langfuse export --from 2027-01-01 --to 2027-01-07 --format json > traces_jan2027.json
```

## API examples

### Python: Structured Trace Ingestion with Pydantic v2
Track custom agent steps using the native Python SDK and Pydantic v2 validation:

```python
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from langfuse import Langfuse

class TracePayload(BaseModel):
    user_id: str
    task_name: str
    input_text: str
    model_name: str = "claude-5.1"

class TraceResponse(BaseModel):
    status: str
    output_text: str
    trace_id: Optional[str] = None

langfuse_client = Langfuse()

async def execute_traced_task(payload: TracePayload) -> TraceResponse:
    trace = langfuse_client.trace(
        name=payload.task_name,
        user_id=payload.user_id,
        input={"text": payload.input_text}
    )

    span = trace.span(
        name="llm-processing-node",
        input={"model": payload.model_name, "prompt": payload.input_text}
    )

    try:
        await asyncio.sleep(0.1)  # Simulate LLM inference delay
        output = f"Processed response for '{payload.input_text}' via {payload.model_name}"
        span.end(output={"result": output})

        return TraceResponse(
            status="success",
            output_text=output,
            trace_id=trace.id
        )
    except Exception as e:
        span.end(level="ERROR", status_message=str(e))
        raise e

if __name__ == "__main__":
    request_data = TracePayload(
        user_id="usr_2027_99",
        task_name="agent-reasoning-step",
        input_text="Analyze Q4 financial trends."
    )
    res = asyncio.run(execute_traced_task(request_data))
    print(res.model_dump_json(indent=2))
```

## Related tools / concepts
- [AgentOps](agentops.md) - Specialized agent monitoring and session tracking.
- [Helicone](helicone.md) - Proxy-based LLM observability platform.
- [ClickHouse](clickhouse.md) - Analytical column-store database backend for Langfuse.
- [Arize AI](arize-ai.md) - Enterprise ML observability and evaluation platform.
- [W&B Weave](wandb-weave.md) - Lightweight tracing and versioning for AI developers.
- [LiteLLM](../../services/litellm.md) - LLM proxy gateway with native Langfuse telemetry exporter.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Multi-step agent execution design patterns.
- [Model Context Protocol](../automation_orchestration/mcp.md) - Standard protocol for model tools.

## Sources / references
- [Langfuse Official Documentation](https://langfuse.com/docs)
- [Langfuse GitHub Repository](https://github.com/langfuse/langfuse)
- [FastMCP 3.1 Integration Specs](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
