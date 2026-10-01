# Langfuse

Langfuse is an open-source LLM engineering platform designed for tracing, observability, metrics, prompt management, and automated evaluation. In early January 2027, it serves as a core control center for engineering teams building, debugging, and scaling complex multi-agent applications powered by frontier models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## System Architecture & Telemetry Pipeline

Langfuse decouples high-throughput trace ingestion from heavy analytical query execution through an asynchronous distributed architecture backed by ClickHouse and PostgreSQL.

```
+-----------------------------------------------------------------------------------+
|                            LANGFUSE TELEMETRY PIPELINE                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Client App / Agent Framework ]                                                 |
|  (LangChain, FastMCP 3.1, AutoGen, LiteLLM)                                       |
|           |                                                                       |
|           | (Non-blocking Async OTel / HTTP Ingestion API)                        |
|           v                                                                       |
|  +-----------------------+                                                        |
|  | Langfuse Web Server   |                                                        |
|  | (API Gateway)         |                                                        |
|  +-----------------------+                                                        |
|           |                                                                       |
|           +-----------------------+-----------------------+                       |
|           |                       |                       |                       |
|           v                       v                       v                       |
|  +-----------------+    +-------------------+    +------------------+             |
|  | Redis Queue     |    | PostgreSQL        |    | ClickHouse       |             |
|  | (Event Buffering)|    | (Users, Prompts,  |    | (Columnar Trace  |             |
|  +-----------------+    | Config Metadata)  |    | Storage & Analytics)            |
|           |             +-------------------+    +------------------+             |
|           v                                                ^                      |
|  +-----------------+                                       |                      |
|  | Ingestion Worker| --------------------------------------+                      |
|  | Processors      |                                                              |
|  +-----------------+                                                              |
|           |                                                                       |
|           v                                                                       |
|  [ LLM-as-a-Judge Evaluation Engine & Dashboard Analytics UI ]                    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

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

## Platform Capabilities & Performance Benchmarks

| Capability Domain | Scale / Target | Metric / Performance Benchmark | Storage Backend |
| :--- | :--- | :--- | :--- |
| **Event Ingestion Capacity** | 50,000+ events/sec | < 5ms ingestion overhead on host app | Redis + ClickHouse |
| **Trace Query Latency** | 100M+ historical spans | < 120ms aggregation response | ClickHouse Columnar |
| **Prompt Delivery Latency** | CDN Cached / In-Memory | < 2ms prompt fetch overhead | PostgreSQL + Redis Cache |
| **Eval Runner Throughput** | 1,000 parallel judge runs | 99.2% evaluation queue retention | Distributed Workers |

## Feature Comparison with Observability Platforms

| Feature / Metric | Langfuse (v3.x) | LangSmith | Arize Phoenix | AgentOps |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Self-Hosted / SaaS | SaaS Primary / Enterprise | Open Source / SaaS | Cloud SaaS |
| **Analytics Engine** | ClickHouse | Proprietary | In-Memory / DuckDB | Proprietary |
| **FastMCP 3.1 Support** | Native First-Class | Extension | Plugin | Native |
| **Prompt Management** | Full Lifecycle + UI | Full Lifecycle | Limited | Basic |
| **License** | Open Source (MIT / AGPL) | Proprietary | Open Source (Apache 2) | Proprietary |

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
Install the Langfuse Python SDK and FastMCP integration:
```bash
pip install langfuse fastmcp pydantic
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

### Deploying Versioned Prompts
Push local prompt templates directly to the Langfuse Prompt Registry:
```bash
langfuse prompts push --file ./prompts/financial_agent_v2.json --label production
```

## Production Deployment & Infrastructure Configuration

For self-hosting Langfuse in production environments using Docker Compose, utilize the optimized configuration below:

```yaml
version: '3.8'

services:
  langfuse-web:
    image: langfuse/langfuse:3
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://langfuse:secret@postgres:5432/langfuse
      - CLICKHOUSE_URL=http://clickhouse:8123
      - CLICKHOUSE_USER=default
      - CLICKHOUSE_PASSWORD=clickhouse_pass
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - NEXTAUTH_SECRET=super-secret-key-2027
      - SALT=super-secret-salt
    depends_on:
      - postgres
      - clickhouse
      - redis

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: langfuse
    volumes:
      - pgdata:/var/lib/postgresql/data

  clickhouse:
    image: clickhouse/clickhouse-server:24.3
    environment:
      CLICKHOUSE_DB: langfuse
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
      CLICKHOUSE_PASSWORD: clickhouse_pass
    volumes:
      - chdata:/var/lib/clickhouse

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
  chdata:
```

## API examples

### FastMCP 3.1 Instrumentation & Trace Verification with Pydantic v2
Track custom agent steps, tool executions, and evaluation scores using the native Python SDK and **Pydantic v2** validation within a **FastMCP 3.1** server:

```python
import asyncio
import time
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ValidationError
from langfuse import Langfuse
from fastmcp import FastMCP

mcp = FastMCP("Langfuse Observability Server")
langfuse_client = Langfuse()

class TracePayload(BaseModel):
    user_id: str = Field(..., description="Unique end-user identity")
    task_name: str = Field(..., description="Logical agent task identifier")
    input_text: str = Field(..., description="Prompt or query input text")
    model_name: str = Field("claude-5.1", description="Target model deployment")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom context key-value pairs")

class EvaluationMetric(BaseModel):
    metric_name: str = Field(..., description="Name of evaluation score")
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score value")
    reasoning: str = Field(..., description="Judge model justification")

class TraceResponse(BaseModel):
    status: str = Field(..., description="Execution status code")
    output_text: str = Field(..., description="Result generated by agent")
    trace_id: str = Field(..., description="Langfuse telemetry trace ID")
    latency_ms: float = Field(..., description="End-to-end execution latency")
    evaluations: List[EvaluationMetric] = Field(default_factory=list, description="Automated evaluation scores")

@mcp.tool()
async def execute_traced_task(user_id: str, task_name: str, input_text: str) -> str:
    """Execute an agent task with full Langfuse multi-span tracing and FastMCP 3.1 metadata capture."""
    start_time = time.time()

    payload = TracePayload(
        user_id=user_id,
        task_name=task_name,
        input_text=input_text,
        metadata={"fastmcp_version": "3.1", "environment": "production"}
    )

    trace = langfuse_client.trace(
        name=payload.task_name,
        user_id=payload.user_id,
        input={"text": payload.input_text},
        metadata=payload.metadata
    )

    span = trace.span(
        name="llm-reasoning-step",
        input={"model": payload.model_name, "prompt": payload.input_text}
    )

    try:
        await asyncio.sleep(0.08)  # Simulate model execution latency
        output = f"Processed response for '{payload.input_text}' via {payload.model_name}"
        span.end(output={"result": output})

        # Score the trace using automated judge evaluation
        eval_metric = EvaluationMetric(
            metric_name="faithfulness",
            score=0.96,
            reasoning="Output strictly adheres to context retrieved during tool call."
        )

        trace.score(
            name=eval_metric.metric_name,
            value=eval_metric.score,
            comment=eval_metric.reasoning
        )

        elapsed_ms = (time.time() - start_time) * 1000

        response_obj = TraceResponse(
            status="success",
            output_text=output,
            trace_id=trace.id,
            latency_ms=elapsed_ms,
            evaluations=[eval_metric]
        )

        return (
            f"Trace ID: {response_obj.trace_id}\n"
            f"Status: {response_obj.status}\n"
            f"Latency: {response_obj.latency_ms:.2f}ms\n"
            f"Eval Score ({eval_metric.metric_name}): {eval_metric.score}\n\n"
            f"Output:\n{response_obj.output_text}"
        )
    except Exception as e:
        span.end(level="ERROR", status_message=str(e))
        return f"Execution error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

## Troubleshooting & Operational Playbook

### Common Issues & Diagnostic Resolutions

#### Issue 1: ClickHouse Storage Growth Exceeding Disk Limits
- **Symptom**: Langfuse UI returns `500 Server Error` during trace dashboard aggregation queries.
- **Cause**: Uncompressed span attributes and high-frequency token events filling ClickHouse primary partition.
- **Resolution**: Configure automated trace TTL policies in ClickHouse: `ALTER TABLE traces MODIFY TTL created_at + INTERVAL 90 DAY;`.

#### Issue 2: Langfuse SDK Flushing Drops Spans on Process Exit
- **Symptom**: Traces generated near the end of short-lived CLI scripts do not appear in the dashboard.
- **Cause**: Asynchronous batch queue is killed before flushing events over HTTP.
- **Resolution**: Explicitly call `langfuse_client.flush()` before exiting background scripts or set `LANGFUSE_AUTO_FLUSH=true`.

#### Issue 3: Redis Queue Ingestion Delay During Traffic Spikes
- **Symptom**: Dashboard displays delayed trace timestamps up to 2 minutes behind real time.
- **Cause**: Worker processes overwhelmed by high concurrent FastMCP session payloads.
- **Resolution**: Scale worker container count (`docker compose scale langfuse-worker=4`) and increase Redis memory allocation.

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
