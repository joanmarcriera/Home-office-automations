# FastAPI

## What it is
FastAPI is a modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints. It is designed to be easy to use, fast to code, and ready for production.

## What problem it solves
It allows for rapid development of robust, high-performance APIs with automatic interactive documentation (Swagger UI/ReDoc). It significantly reduces developer error through type validation via **Pydantic v2** and provides native support for asynchronous programming (async/await), making it ideal for I/O-bound tasks like calling frontier LLM APIs such as **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0**.

## Where it fits in the stack
**Framework / Backend**. Often used as the orchestration or serving layer for AI agents, [Model Context Protocol (MCP 3.1)](../automation_orchestration/mcp.md) servers, and custom homelab microservices. It bridges the gap between Python's data science ecosystem and web-standard production environments.

## Typical use cases
- Building RESTful APIs for AI agents and tools (e.g., [CrewAI](crewai.md) or [LangGraph](langgraph.md)).
- Serving machine learning models with low latency using [NVIDIA NIM](../providers/nvidia.md).
- Creating backends for internal dashboards and automation triggers.
- Building custom [MCP servers](../automation_orchestration/mcp.md) for specialized data sources.
- Implementing webhook handlers for services like [Supabase](../infrastructure/supabase.md).

## Strengths
- **Performance**: On par with NodeJS and Go, thanks to Starlette and Pydantic.
- **Developer Experience**: Fast to code, easy to learn, and provides excellent editor support (autocompletion).
- **Validation**: Automatic data validation and serialization using **Pydantic v2**.
- **Documentation**: Automatic interactive API documentation (OpenAPI and JSON Schema).
- **Dependency Injection**: Powerful and easy-to-use dependency injection system for managing database sessions, security, and shared resources.
- **Native Async**: First-class support for `async/await`, crucial for high-concurrency LLM interactions.

## Limitations
- **Python Ecosystem**: Limited to the Python ecosystem (though this is a strength for AI/ML).
- **Asynchronous Complexity**: While it supports sync code, fully leveraging its performance requires understanding `asyncio`.
- **Boilerplate**: Compared to micro-frameworks like Flask, it can feel more verbose due to type hints, though this pays off in maintainability.

## When to use it
- When you need a high-performance Python-based API.
- When building servers that will be consumed by LLMs or agents using [Pydantic AI](pydantic-ai.md).
- When you want to leverage Python's AI/ML ecosystem while maintaining web-standard performance.
- When you require automatic API documentation for external developers or agents.

## When not to use it
- If you are building a simple static site with no dynamic API needs.
- If your team is more proficient in another language (e.g., Go, Rust) and there's no specific need for Python's libraries.
- For extremely simple scripts where a basic `http.server` or Flask would suffice.

## Getting started

### Installation
Install FastAPI with standard dependencies:

```bash
pip install "fastapi[standard]"
```

### Hello-world
Create a file `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World", "framework": "FastAPI"}
```

Run the server:
```bash
fastapi dev main.py
```

## CLI examples

```bash
# Run a FastAPI app with Uvicorn (development mode with hot-reload)
fastapi dev main.py

# Run in production
fastapi run main.py

# Generate OpenAPI schema to a file
python -c "import json; from main import app; print(json.dumps(app.openapi()))" > openapi.json
```

## API examples

### Pydantic Model Validation (Pydantic v2 Compliance)
```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

class AgentTask(BaseModel):
    id: str = Field(..., min_length=3, description="Unique task identifier")
    goal: str = Field(..., description="High-level objective for the agent")
    priority: int = Field(default=1, ge=1, le=5)

    @field_validator("id")
    @classmethod
    def validate_id_prefix(cls, v: str) -> str:
        if not v.startswith("task_"):
            raise ValueError("Task ID must start with 'task_'")
        return v

app = FastAPI()

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: AgentTask) -> dict:
    return {"status": "created", "task_id": task.id}
```

### Dependency Injection (Auth Example with Explicit Type Hints)
```python
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API Key credentials"
        )
    return api_key

app = FastAPI()

@app.get("/secure")
async def secure_route(key: str = Depends(get_api_key)) -> dict:
    return {"data": "protected", "api_key_status": "verified"}
```

## Related tools / concepts
- [Pydantic AI](pydantic-ai.md) — Agentic framework built on Pydantic and FastAPI.
- [Agno](../agents/agno.md) — Multi-agent framework that integrates well with FastAPI.
- [LangGraph](langgraph.md) — State-machine based agent orchestration.
- [CrewAI](crewai.md) — Role-based multi-agent framework.
- [Smolagents](smolagents.md) — Minimalist agent library.
- [Docker](../infrastructure/docker.md) — Containerization standard.
- [K3s](../infrastructure/k3s.md) — Lightweight Kubernetes for orchestration.
- [Supabase](../infrastructure/supabase.md) — Backend-as-a-service often used as a FastAPI database.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool-calling protocol.

## Sources / references
- [Official Website](https://fastapi.tiangolo.com/)
- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Starlette Framework](https://www.starlette.io/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
