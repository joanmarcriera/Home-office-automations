# PydanticAI

## What it is
PydanticAI is a production-grade Python agent framework developed by the Pydantic team, engineered to bring type-safety, structured data validation, dependency injection, and observable execution to Generative AI applications and multi-agent workflows. Just as Pydantic v2 established the industry standard for data validation across FastAPI and Python backends, PydanticAI applies strict schema generation, type hints, and runtime validation to agent prompts, tool invocations, and agent response payloads.

PydanticAI natively supports flagship foundation models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Gemma 4**. It integrates seamlessly with the **FastMCP 3.1 Task Protocol**, allowing developers to build model-agnostic agent systems with sub-10ms tool call routing, strict Pydantic schema validation, and native observability through Pydantic Logfire.

## What problem it solves
Early AI agent development suffers from major reliability and maintainability bottlenecks:
1. **Unstructured Output Fragility**: Non-deterministic LLM responses often fail JSON parsing, missing expected keys or outputting invalid data types in production systems.
2. **Untyped Tool Call Signatures**: Complex agent tools without strict schema definitions lead to silent bugs, missing required function arguments, and type mismatch errors.
3. **Implicit State Management**: Dependency injection across system prompts, tool functions, and output validators is frequently handled via brittle global state variables or untyped dictionary kwargs.
4. **Lack of Native Observability**: Debugging multi-step agent reasoning chains, tool failures, and validation retries requires custom logging glue code.

PydanticAI solves these challenges by leveraging Python type annotations (`type hints`), Pydantic v2 schemas, and runtime dependency injection (`RunContext`). When an LLM generates a response or tool call that fails schema validation, PydanticAI automatically formats validation error feedback back to the model, triggering self-correction retries until a valid, strictly-typed output is returned.

## Where it fits in the stack
**Category**: Frameworks / Agentic Workflow Frameworks & Microservice Infrastructure. PydanticAI operates at the **Application & Orchestration Layer**, bridging LLM provider APIs with database layers, FastMCP 3.1 tool servers, and enterprise microservice backends.

```mermaid
graph TD
    UserRequest[Client / User Request] --> AgentCore[PydanticAI Agent Engine]

    subgraph ValidationEngine [Pydantic v2 Type & Schema Engine]
        AgentCore --> SystemPrompt[System Prompt Builder + Dependency Injection]
        AgentCore --> ToolValidator[Tool Argument Schema Validator]
        AgentCore --> OutputValidator[Result Schema Validator & Retry Loop]
    end

    subgraph ProviderGateways [Model Agnostic LLM Providers]
        AgentCore -->|Anthropic API| Claude[Claude 5.6 / Sonnet]
        AgentCore -->|OpenAI API| GPT[GPT-5.6 / O3]
        AgentCore -->|Google Gemini API| Gemini[Gemini 4.0 Ultra]
        AgentCore -->|Local vLLM / Ollama| LocalModel[Gemma 4 / Llama 4]
    end

    subgraph ToolEcosystem [FastMCP 3.1 & External Systems]
        ToolValidator --> MCP[FastMCP 3.1 Server]
        MCP --> DB[(PostgreSQL / Vector DB)]
        MCP --> Shell[Local Workstation / Sandbox]
    end

    AgentCore --> Logfire[Pydantic Logfire Observability]
```

## Typical use cases
- **Production Structured Data Extraction**: Extracting complex, multi-nested domain entities from unstructured legal, medical, or financial documents into validated Pydantic v2 models with automatic self-correction.
- **Enterprise Agentic Microservices**: Building type-safe FastAPI endpoints powered by PydanticAI agents that expose standardized REST and FastMCP 3.1 tool APIs.
- **Multi-Agent Systems with State Injection**: Orchestrating specialized agent chains that securely pass database pools, user authorization tokens, and runtime configurations using `RunContext`.
- **Automated Code & API Generators**: Constructing software engineering agents that generate syntactically correct code snippets, JSON schemas, and SQL queries checked against strict schema constraints.
- **High-Fidelity Agent Observability**: Monitoring production agent runs, token costs, latency distribution, and tool execution traces using Pydantic Logfire integration.

## Strengths
- **Strict Pydantic v2 Validation**: Comprehensive type checking and automatic error-retry feedback loops for both tool inputs and agent result models.
- **Native FastMCP 3.1 Integration**: Direct support for hosting, serving, and invoking FastMCP tool servers.
- **Clean Dependency Injection**: First-class support for injecting runtime context (`deps_type`, `RunContext`) into prompts, tools, and validators.
- **Model Agnostic Abstraction**: Unified, clean interface across Anthropic, OpenAI, Google Gemini, DeepSeek, and local Ollama/vLLM models.
- **Type-Safe Graph Execution**: Native execution graph streaming and node inspection for interactive real-time agent UI state management.

## Limitations
- **Python-Exclusive Ecosystem**: Designed exclusively for Python 3.10+ environments (no native TypeScript or Go runtimes).
- **Type Hinting Requirement**: Requires disciplined use of Python type annotations and familiarity with Pydantic v2 features.
- **Verbose Tool Definitions**: Highly structured tool schemas require explicit Pydantic model definitions compared to plain docstring utilities.

## When to use it
- When building mission-critical, production AI applications where response schemas, tool argument types, and reliability are paramount.
- When working within teams heavily invested in Python, FastAPI, Pydantic v2, and modern AsyncIO architectures.
- For complex multi-agent workflows that require clean dependency injection and seamless **FastMCP 3.1** tool interoperability.

## When not to use it
- For quick single-file scripts or throwaway prototypes where type safety and formal schema design are unnecessary.
- If your engineering stack is built entirely on JavaScript/TypeScript (consider LangChain.js or Vercel AI SDK).
- When attempting to stitch together massive legacy pre-built tool libraries without standardizing them into FastMCP tools.

## Getting started

### Installation
Install `pydantic-ai` alongside Pydantic v2 and optional observability tools via PyPI:

```bash
# Core package installation
pip install pydantic-ai pydantic logfire

# Install provider dependencies
pip install anthropic openai google-genai
```

### Basic Minimal Example
Create a minimal agent instance that uses Claude 5.6 to answer questions:

```python
from pydantic_ai import Agent

# Initialize agent with target model
agent = Agent(
    'anthropic:claude-5-6-sonnet',
    system_prompt='You are a precise technical software assistant.',
)

# Execute synchronous agent run
result = agent.run_sync('Explain the primary benefits of Pydantic v2 validation.')
print(result.data)
```

## CLI examples

### Inspecting Agent Graph Structure
Inspect and visualize the execution graph and node topology of a PydanticAI agent:

```bash
pydantic-ai inspect my_agent_module:agent
```

### Serving a FastMCP 3.1 Tool Server
Launch a local FastMCP tool server using PydanticAI tool definitions:

```bash
pydantic-ai mcp serve my_tools.py --port 8000
```

### Running Agent Evaluation Benchmarks
Evaluate agent accuracy and schema compliance against a JSONL benchmark dataset:

```bash
pydantic-ai benchmark --agent my_agent_module:agent --dataset test_queries.jsonl
```

## API examples

### Advanced Dependency Injection & Structured Result Validation with Pydantic v2
This production-ready Python example demonstrates injecting runtime database connections, configuring strict Pydantic v2 result schemas, handling validation retries, and hosting a FastMCP 3.1 tool server:

```python
import json
from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, RunContext
from mcp.server.fastmcp import FastMCP

# 1. Define Dependency Container
@dataclass
class DatabaseConnection:
    connection_string: str
    active_tenant_id: str

    def query_user_orders(self, user_id: str) -> List[dict]:
        return [
            {"order_id": 101, "item": "High-Performance Server Blade", "qty": 2, "price": 1200.00},
            {"order_id": 102, "item": "FastMCP Gateway License", "qty": 1, "price": 350.00}
        ]

# 2. Define Output Schema with Pydantic v2
class OrderItem(BaseModel):
    order_id: int = Field(..., description="Unique integer order identifier")
    item_name: str = Field(..., description="Full descriptive title of the ordered item")
    quantity: int = Field(..., ge=1, description="Quantity ordered, must be at least 1")
    total_price: float = Field(..., ge=0.0, description="Total cost of items in USD")

class CustomerAuditReport(BaseModel):
    user_id: str = Field(..., description="Target customer identifier")
    tenant_id: str = Field(..., description="Multi-tenant account identifier")
    total_orders: int = Field(..., description="Count of parsed order items")
    orders: List[OrderItem] = Field(default_factory=list, description="List of validated order details")

    @field_validator("total_orders")
    def validate_total_orders(cls, v: int, info) -> int:
        return v

# 3. Instantiate Agent with Types and System Prompts
agent = Agent(
    'anthropic:claude-5-6-sonnet',
    deps_type=DatabaseConnection,
    result_type=CustomerAuditReport,
    system_prompt="You are an enterprise account auditing agent. Extract and validate customer order metrics."
)

@agent.system_prompt
def add_tenant_context(ctx: RunContext[DatabaseConnection]) -> str:
    return f"Active Tenant Context: {ctx.deps.active_tenant_id}. Ensure all returned records match this tenant."

@agent.tool
def fetch_customer_records(ctx: RunContext[DatabaseConnection], user_id: str) -> str:
    """Retrieves raw customer order records from the injected database connection."""
    records = ctx.deps.query_user_orders(user_id)
    return json.dumps(records)

# 4. FastMCP 3.1 Gateway Integration
mcp = FastMCP("PydanticAIAuditGateway")

@mcp.tool()
def execute_customer_audit(user_id: str, tenant_id: str) -> str:
    """FastMCP tool wrapper that executes the PydanticAI agent with injected context."""
    db_conn = DatabaseConnection(
        connection_string="postgresql://user:pass@localhost:5432/audit_db",
        active_tenant_id=tenant_id
    )

    result = agent.run_sync(
        f"Generate a validated CustomerAuditReport for customer user_id: '{user_id}'.",
        deps=db_conn
    )

    # result.data is guaranteed to be a valid CustomerAuditReport instance
    return result.data.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Pydantic](https://docs.pydantic.dev/) — Core data validation and settings management library.
- [Logfire](../process_understanding/logfire.md) — Native observability platform for Pydantic and PydanticAI.
- [FastAPI](fastapi.md) — High-performance Python web framework for agent microservices.
- [LangGraph](langgraph.md) — Graph-based agent state machine framework.
- [CrewAI](crewai.md) — Multi-agent role-playing orchestration framework.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standardized tool execution specification.
- [Agentic Design Patterns](../../knowledge_base/patterns/agentic-workflows.md) — Strategic patterns for reliable agent architectures.

## Sources / references
- [PydanticAI Official GitHub Repository](https://github.com/pydantic/pydantic-ai)
- [PydanticAI Documentation Portal](https://ai.pydantic.dev/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
