# Logfire

## What it is
**Logfire** is Pydantic's observability, tracing, and logging platform tailored specifically for Python applications, FastAPI microservices, and LLM agent pipelines. Built on top of OpenTelemetry standards and powered by a high-performance ClickHouse backend, Logfire provides deep, zero-overhead visibility into Pydantic v2 data validation, database queries, and multi-agent execution spans.

## What problem it solves
Traditional logging tools treat logs as flat text strings or detached JSON objects, making it difficult to visualize complex, nested LLM tool calls and Pydantic validation hierarchies. Logfire solves this by auto-instrumenting Pydantic models, FastAPI routes, HTTP clients (httpx/requests), and OpenAI/Anthropic/LangChain calls, presenting them as structured, interactive execution trees without requiring manual telemetry boilerplate.

## Where it fits in the stack
**Category**: Process Understanding / Observability & Telemetry. It operates at the **Telemetry & Observability Layer**, connecting Python application runtimes, FastMCP 3.1 servers, and LLM orchestrators ([Pydantic AI](../frameworks/pydantic-ai.md), [Instructor](../frameworks/instructor.md)) to cloud or self-hosted observability backends.

## Typical use cases
- **LLM Agent & FastMCP 3.1 Tracing**: Visualizing nested tool invocations, prompt token counts, and model latencies in agentic loops.
- **Pydantic Validation Error Debugging**: Inspecting real-time validation failures, field schema mismatches, and data drift across backend endpoints.
- **FastAPI Endpoint Analytics**: Monitoring request latencies, status codes, and SQL query execution spans within API routes.
- **Distributed Python Microservice Telemetry**: Exporting OpenTelemetry spans across asynchronous worker nodes.

## Strengths
- **Native Pydantic v2 Integration**: Auto-traces model instantiations, schema validations, and serialization events out-of-the-box.
- **OpenTelemetry Native**: Native OTLP exporter support guarantees no vendor lock-in; traces can be redirected to Grafana, Datadog, or Jaeger.
- **Zero-Boilerplate Auto-Instrumentation**: Simple `logfire.configure()` instruments popular libraries (`fastapi`, `httpx`, `asyncio`, `openai`, `anthropic`, `sqlalchemy`).
- **Developer-Centric Dashboard**: High-speed SQL search over structured trace spans with rich tree-view rendering.

## Limitations
- **Python Ecosystem Focused**: Deepest auto-instrumentation hooks are currently exclusive to Python and Pydantic runtime environments.
- **Cloud SaaS Tier Retention**: Long-term historical telemetry retention on free cloud tiers requires upgrading or self-hosting OTLP collectors.
- **Sampling Overhead at Extreme Volume**: Ultra-high-frequency logging requires configuring tail-sampling rules to manage bandwidth.

## When to use it
- When developing Python LLM applications using Pydantic, Pydantic AI, FastAPI, or FastMCP 3.1.
- When requiring rich execution trees and field-level validation tracing for AI agent workflows.
- When standardizing on OpenTelemetry-compliant observability infrastructure.

## When not to use it
- For non-Python microservice stacks (e.g., pure Node.js/TypeScript or Go applications).
- When simple local file logging or lightweight stdout logging is sufficient without external dashboard management.

## Getting started

### Installation
Install the Logfire SDK via pip:
```bash
pip install logfire
```

### Authentication & Initial Configuration
Authenticate your local environment with the Logfire cloud service:
```bash
logfire auth
```

### Basic Setup in Python
Initialize Logfire tracing in your application entrypoint:
```python
import logfire

# Configure Logfire with project token or environment variables
logfire.configure(project_name="home-office-automations")
logfire.info("Logfire instrumentation initialized successfully.")
```

## CLI examples

### CLI Project Verification
```bash
logfire check
```

### Stream Live Logs via CLI
```bash
logfire projects list
```

## API examples

### FastAPI Auto-Instrumentation and Pydantic v2 Tracing
The following code demonstrates auto-instrumenting a FastAPI application with Pydantic v2 model validation tracing using Logfire:

```python
import logfire
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Initialize Logfire
logfire.configure(project_name="agent-api")

app = FastAPI(title="Logfire-Instrumented Agent API")
logfire.instrument_fastapi(app)

class AgentTaskRequest(BaseModel):
    task_id: str = Field(..., description="Unique task identifier")
    prompt: str = Field(..., description="Prompt string for the agent")
    max_steps: int = Field(default=5, ge=1, le=20)

class AgentTaskResponse(BaseModel):
    status: str
    result_summary: str

@app.post("/api/v1/execute", response_model=AgentTaskResponse)
async def execute_task(payload: AgentTaskRequest):
    with logfire.span("agent.execute_task", task_id=payload.task_id):
        logfire.info("Processing task {task_id}", task_id=payload.task_id)
        # Simulated agent task execution logic
        return AgentTaskResponse(
            status="completed",
            result_summary=f"Processed prompt of length {len(payload.prompt)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Related tools / concepts
- [Datadog](datadog.md)
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Pydantic AI](../frameworks/pydantic-ai.md)
- [Grafana Cloud](grafana-cloud.md)
- [Instructor](../frameworks/instructor.md)

## Sources / references
- [Pydantic Logfire Official Documentation](https://docs.pydantic.dev/logfire/)
- [Pydantic GitHub Repository](https://github.com/pydantic/logfire)
- [FastAPI Observability Guide with Logfire](https://fastapi.tiangolo.com/tutorial/telemetry/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
