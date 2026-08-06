# PydanticAI

## What it is
PydanticAI is a Python agent framework from the Pydantic team, designed for building production-grade Generative AI applications and workflows. It brings the same rigor, type-safety, and validation to AI agents that Pydantic brought to data modeling. As of late November/December 2026, it natively supports **Gemma 3**, **Qwen 3.6**, and **Claude 5.1** models, the **MCP 3.1 Task Protocol**, and high-performance **FastMCP 3.1** tool servers.

## What problem it solves
It addresses the fragility and lack of structure often found in early AI agent frameworks. By leveraging Python type hints and Pydantic validation, it ensures that tool calls, agent responses, and complex multi-agent workflows are type-safe and reliable. Integration with the **MCP 3.1 Task Protocol** allows for standardized, cross-platform tool execution.

## Where it fits in the stack
**Framework / Agentic Workflow / Development & Ops**.

## Typical use cases
- **Structured Data Extraction**: Using **Gemma 3** or **Claude 5.1** agents to parse unstructured text into validated Pydantic models.
- **Production Agents**: Building agents that require strict adherence to schemas for tool usage and response formatting.
- **Multi-Agent Orchestration**: Coordinating multiple specialized agents with clear handoffs and state management using the **Task Protocol**.
- **Observability Integration**: Seamlessly integrating with tools like Pydantic Logfire for detailed tracing and monitoring of agentic runs.

## Strengths
- **Type Safety**: Full support for Python type hints throughout the agent lifecycle.
- **Validation**: Automatic validation of tool arguments and agent outputs using Pydantic V2.
- **MCP 3.1 Native**: Built-in support for calling and hosting MCP tool servers.
- **Model Agnostic**: Supports multiple LLM providers (OpenAI, Anthropic, Gemini, local Gemma 3) through a unified interface.
- **Integration with Pydantic Ecosystem**: Native support for Logfire and other Pydantic-related tools.

## Limitations
- **Python Centric**: Primarily designed for Python developers (no native JS/TS support).
- **Learning Curve**: Requires familiarity with Pydantic V2 and modern Python type hinting practices.
- **Maturity**: While growing rapidly, it is younger than frameworks like LangChain or AutoGen.

## When to use it
- When building production-ready AI applications where reliability and validation are paramount.
- If your team is already heavily invested in the Pydantic/FastAPI ecosystem.
- For complex workflows that benefit from strict type-safe interfaces and **MCP 3.1** interoperability.

## When not to use it
- For quick, throwaway scripts where type safety is an afterthought.
- If you require a framework with a massive library of legacy pre-built integrations and don't want to build your own MCP tools.

## Getting started

### Installation
```bash
pip install pydantic-ai pydantic logfire
```

### Minimal Example
```python
from pydantic_ai import Agent

agent = Agent(
    'google:gemma-3-27b',
    system_prompt='You are a helpful assistant.',
)

result = agent.run_sync('What is the capital of France?')
print(result.data)
```

## CLI examples

### Inspecting Agent Graph
```bash
pydantic-ai inspect my_agent:agent
```

### Running an MCP 3.1 Server
```bash
pydantic-ai mcp serve my_tools.py
```

### Benchmarking Agent Performance
```bash
pydantic-ai benchmark --agent my_agent:agent --dataset test_queries.jsonl
```

## API examples

### Dependency Injection (DI) with Strict Pydantic v2 Type-Safety
PydanticAI allows for runtime injection of external objects (database connections, user context, config) into system prompts, tools, and validators with strict type validation.

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    user_name: str
    db_conn: any

# Output schema using Pydantic v2
class OrderDetails(BaseModel):
    order_id: int = Field(..., description="Unique integer ID of the order")
    item_name: str = Field(..., description="The name of the item ordered")
    quantity: int = Field(..., ge=1, description="Quantity of items, must be 1 or more")

agent = Agent(
    'anthropic:claude-5-1-sonnet',
    deps_type=MyDeps,
    result_type=OrderDetails
)

@agent.system_prompt
def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"Hello {ctx.deps.user_name}, I am your assistant helping to extract order details."

@agent.tool
def get_user_data(ctx: RunContext[MyDeps], query: str) -> str:
    # Use injected database connection securely
    return f"DB query output for {query}"

# Execution with dependency injection and Pydantic v2 schema-checked output
class MockDb:
    def execute(self, query):
        return "Row data"

mock_db = MockDb()
deps = MyDeps(user_name="Jules", db_conn=mock_db)

result = agent.run_sync(
    "Extract this order: Coffee filters, quantity 5, order ID #12345.",
    deps=deps
)

# result.data is guaranteed to be a valid instance of OrderDetails
print(f"Validated Order ID: {result.data.order_id}")
print(f"Validated Item Name: {result.data.item_name}")
print(f"Validated Quantity: {result.data.quantity}")
```

### Structured Result Validation
You can force an agent to return a specific Pydantic model with automatic retry on validation failure.

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class ProductAnalysis(BaseModel):
    name: str
    rating: float
    pros: list[str]
    cons: list[str]

agent = Agent('openai:gpt-5.5', result_type=ProductAnalysis)

result = agent.run_sync("Analyze this product: SuperPhone 15. Rating: 4.8/5. It is fast but expensive.")
# result.data is an instance of ProductAnalysis
```

### Agent Graph Iteration
Access and iterate over the internal agent graph nodes during execution for fine-grained monitoring or UI state management.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.5')

with agent.capture_run() as run:
    result = agent.run_sync("Analyze this data...")
    for node in run.nodes:
        print(f"Executing node: {node.name}")
```

## Related tools / concepts
- [Pydantic](https://docs.pydantic.dev/) — Core data validation library.
- [Logfire](https://pydantic.dev/logfire) — Native observability for Pydantic and PydanticAI.
- [FastAPI](https://fastapi.tiangolo.com/) — Often used together for building AI microservices.
- [LangGraph](langgraph.md) — Alternative graph-based orchestration framework.
- [CrewAI](crewai.md) — Focuses on role-playing and collaborative agents.
- [Agentic Design Patterns](../../knowledge_base/patterns/agentic-workflows.md) — Strategic patterns for reliable agent systems.
- [Documentation Writer](../agents/documentation-writer.md): For creating technical documentation for PydanticAI agents.
- [Claude Code](../development_ops/claude-code.md): The primary CLI agent used for building PydanticAI apps.
- [Gemma 3](../ai_knowledge/local_llms.md): Canonical guide for the latest open models supported natively.

## Sources / References
- [Official GitHub](https://github.com/pydantic/pydantic-ai)
- [Documentation](https://ai.pydantic.dev/)
- [Pydantic AI Skills](https://github.com/DougTrajano/pydantic-ai-skills)

## Contribution Metadata
- Last reviewed: 2026-12-11
- Confidence: high
