# PydanticAI

## What it is
PydanticAI is a Python agent framework from the Pydantic team, designed for building production-grade Generative AI applications and workflows. It brings the same rigor, type-safety, and validation to AI agents that Pydantic brought to data modeling.

## What problem it solves
It addresses the fragility and lack of structure often found in early AI agent frameworks. By leveraging Python type hints and Pydantic validation, it ensures that tool calls, agent responses, and complex multi-agent workflows are type-safe and reliable.

## Where it fits in the stack
**Framework / Agentic Workflow / Development & Ops**.

## Typical use cases
- **Structured Data Extraction**: Using **Claude 4.8** or **GPT-5.5** agents to parse unstructured text into validated Pydantic models.
- **Production Agents**: Building agents that require strict adherence to schemas for tool usage and response formatting.
- **Multi-Agent Orchestration**: Coordinating multiple specialized agents with clear handoffs and state management.
- **Observability Integration**: Seamlessly integrating with tools like Pydantic Logfire for detailed tracing and monitoring.

## Strengths
- **Type Safety**: Full support for Python type hints throughout the agent lifecycle.
- **Validation**: Automatic validation of tool arguments and agent outputs.
- **Model Agnostic**: Supports multiple LLM providers (OpenAI, Anthropic, Gemini, etc.) through a unified interface.
- **Modular Design**: Encourages the use of "Capabilities" and "Skills" that can be shared across agents.
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

## Advanced Patterns

### Dependency Injection (DI)
PydanticAI allows for runtime injection of external objects (database connections, user context, config) into system prompts, tools, and validators.

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    user_name: str
    db_conn: any

agent = Agent('anthropic:claude-3-5-sonnet', deps_type=MyDeps)

@agent.system_prompt
def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"Hello {ctx.deps.user_name}, I am your assistant."

@agent.tool
def get_user_data(ctx: RunContext[MyDeps], query: str) -> str:
    return ctx.deps.db_conn.execute(query)

result = agent.run_sync("Tell me about my orders", deps=MyDeps(user_name="Jules", db_conn=my_db))
```

### Structured Result Validation
You can force an agent to return a specific Pydantic model with automatic retry on validation failure.

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

### Agent Graph Iteration (June 2026)
Access and iterate over the internal agent graph nodes during execution for fine-grained monitoring or UI state management.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

with agent.capture_run() as run:
    result = agent.run_sync("Analyze this data...")
    for node in run.nodes:
        print(f"Executing node: {node.name}")
```

## Licensing and cost
- **Open Source**: Yes (MIT).
- **Cost**: Free (Framework) + LLM API costs.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Pydantic](https://docs.pydantic.dev/) — Core data validation library.
- [Logfire](https://pydantic.dev/logfire) — Native observability for Pydantic and PydanticAI.
- [FastAPI](https://fastapi.tiangolo.com/) — Often used together for building AI microservices.
- [LangGraph](langgraph.md) — Alternative graph-based orchestration framework.
- [CrewAI](crewai.md) — Focuses on role-playing and collaborative agents.
- [Agentic Design Patterns](../../knowledge_base/patterns/agentic-workflows.md) — Strategic patterns for reliable agent systems.
- [Documentation Writer](../agents/documentation-writer.md): For creating technical documentation for PydanticAI agents.
- [big-AGI](../ai_knowledge/big-agi.md): Professional workspace that can interface with PydanticAI backends.
- [Claude Code](../development_ops/claude-code.md): The primary CLI agent used for building PydanticAI apps.
- [Agentic Calendar Orchestration](../../knowledge_base/patterns/agentic-workflows.md): Patterns for building complex calendar agents.

## Sources / References
- [Official GitHub](https://github.com/pydantic/pydantic-ai)
- [Documentation](https://ai.pydantic.dev/)
- [Pydantic AI Skills](https://github.com/DougTrajano/pydantic-ai-skills)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
