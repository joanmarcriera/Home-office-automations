# PydanticAI

## What it is
PydanticAI is a Python agent framework from the Pydantic team, designed for building production-grade Generative AI applications and workflows. It brings the same rigor, type-safety, and validation to AI agents that Pydantic brought to data modeling. As of July 2026, it features native support for **Gemma 3** via the **FastMCP 3.0** adapter.

## What problem it solves
It addresses the fragility and lack of structure often found in early AI agent frameworks. By leveraging Python type hints and Pydantic validation, it ensures that tool calls, agent responses, and complex multi-agent workflows are type-safe and reliable.

## Where it fits in the stack
**Framework / Agentic Workflow / Development & Ops**.

## Typical use cases
- **Structured Data Extraction**: Using **Gemma 3** or **Claude 4.8** agents to parse unstructured text into validated Pydantic models.
- **Production Agents**: Building agents that require strict adherence to schemas for tool usage and response formatting.
- **Multi-Agent Orchestration**: Coordinating multiple specialized agents with clear handoffs and state management.
- **Observability Integration**: Seamlessly integrating with tools like Pydantic Logfire for detailed tracing and monitoring.

## Strengths
- **Type Safety**: Full support for Python type hints throughout the agent lifecycle.
- **Validation**: Automatic validation of tool arguments and agent outputs.
- **Model Agnostic**: Supports multiple LLM providers (OpenAI, Anthropic, Gemini, etc.) through a unified interface.
- **Dependency Injection**: Allows for runtime injection of external objects (database connections, user context) into system prompts and tools.
- **Integration with Pydantic Ecosystem**: Built-in support for Logfire and other Pydantic-related tools.

## Limitations
- **Python Centric**: Primarily designed for Python developers (no native JS/TS support).
- **Learning Curve**: Requires familiarity with Pydantic and modern Python type hinting practices.
- **Maturity**: While growing rapidly, it is younger than frameworks like LangChain or AutoGen.

## When to use it
- When building production-ready AI applications where reliability and validation are paramount.
- If your team is already heavily invested in the Pydantic/FastAPI ecosystem.
- For complex workflows that benefit from strict type-safe interfaces.

## When not to use it
- For quick, throwaway scripts where type safety is an afterthought.
- If you require a framework with a massive library of pre-built integrations (e.g., LangChain) and don't want to build your own tools.

## Getting started

### Installation
```bash
pip install pydantic-ai
```

### Minimal Example
```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o',
    system_prompt='You are a helpful assistant.',
)

result = agent.run_sync('What is the capital of France?')
print(result.data)
```

### Running with Gemma 3 (July 2026)
```python
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel('gemma-3-27b')
agent = Agent(model=model)
```

## CLI examples

### Initializing a Project
```bash
pydantic-ai init my-agent-app
```

### Testing Agents
```bash
pydantic-ai test --agent my_agent.py
```

### Viewing Logs (via Logfire)
```bash
logfire auth login
logfire view
```

## API examples

### Structured Result Validation
```python
from pydantic import BaseModel
from pydantic_ai import Agent

class OrderDetails(BaseModel):
    order_id: int
    item_name: str
    quantity: int

agent = Agent('openai:gpt-4o', result_type=OrderDetails)

result = agent.run_sync("I want to order 5 coffee filters. Order #12345.")
# result.data is an instance of OrderDetails
```

### Dependency Injection (DI)
```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    user_name: str

agent = Agent('anthropic:claude-3-5-sonnet', deps_type=MyDeps)

@agent.tool
def get_user_data(ctx: RunContext[MyDeps], query: str) -> str:
    return f"Data for {ctx.deps.user_name}: {query}"

result = agent.run_sync("Get info", deps=MyDeps(user_name="Jules"))
```

## Related tools / concepts
- [Pydantic](https://docs.pydantic.dev/) — Core data validation library.
- [Logfire](https://pydantic.dev/logfire) — Native observability for Pydantic and PydanticAI.
- [FastAPI](https://fastapi.tiangolo.com/) — Often used together for building AI microservices.
- [LangGraph](langgraph.md) — Alternative graph-based orchestration framework.
- [CrewAI](crewai.md) — Focuses on role-playing and collaborative agents.
- [Agentic Design Patterns](../../knowledge_base/patterns/agentic-workflows.md) — Strategic patterns for reliable agent systems.
- [Gemma 3](../ai_knowledge/local_llms.md) — Canonical guide for the Gemma 3 model family.
- [Claude Code](../development_ops/claude-code.md): The primary CLI agent used for building PydanticAI apps.

## Sources / References
- [Official GitHub](https://github.com/pydantic/pydantic-ai)
- [Documentation](https://ai.pydantic.dev/)
- [Pydantic AI Skills](https://github.com/DougTrajano/pydantic-ai-skills)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
