# Pydantic

## What it is
Pydantic is the standard data validation and settings management library for Python. Powered by a high-performance Rust core (`pydantic-core`), Pydantic enforces type hints at runtime, providing user-friendly errors when data is invalid, and serializes Python data structures to and from JSON smoothly.

In AI engineering, LLM agent development, and Model Context Protocol (MCP) tool building, Pydantic is the foundational library used to define structured outputs, function calling signatures, prompt input schemas, and application settings.

## What problem it solves
LLMs naturally output unconstrained unstructured text. Extracting reliable, typed data structures (e.g., JSON, Pydantic models) from LLMs without runtime validation often results in parsing failures, schema mismatches, and fragile downstream logic. Pydantic solves this by validating LLM outputs against declarative schema definitions, auto-generating JSON Schemas for tool calling, and parsing complex nested responses safely.

## Where it fits in the stack
**Agent & LLM Frameworks / Data Validation & Schemas** — acts as the universal schema layer across AI frameworks, FastAPI microservices, instructor pipelines, and agent workbenches (e.g., Pydantic AI, LangChain, Instructor).

## Typical use cases
- **Structured Outputs from LLMs**: Defining response models for LLM output parsing via OpenAI Structured Outputs, Instructor, or Pydantic AI.
- **Agent Tool Parameter Schemas**: Generating JSON Schemas for tool definitions and function signatures passed to model tool-calling APIs.
- **Environment & App Configuration**: Managing application settings and secret keys safely using `pydantic-settings`.
- **FastAPI Request/Response Validation**: Validating REST and WebSocket request payloads in Python AI microservices.

## Strengths
- **Rust-powered Performance**: Core validation engine (`pydantic-core`) is written in Rust, offering up to 20x faster data validation than pure Python.
- **Native Python Type Hint Integration**: Seamlessly works with standard Python type annotations (`str`, `int`, `List`, `Optional`, Dataclasses).
- **Automatic JSON Schema Generation**: Generates compliant JSON Schema definitions (`Model.model_json_schema()`) required by LLM function calling APIs.
- **Extensible Field Validation**: Provides `@field_validator` and `@model_validator` decorators for custom domain-specific constraints.

## Limitations
- **Runtime Validation Overhead**: While fast, runtime validation adds minor computational overhead compared to raw unchecked Python dictionaries.
- **Migration Effort (V1 to V2)**: Upgrading legacy Pydantic v1 code bases to Pydantic v2 requires syntax updates (e.g., `.dict()` to `.model_dump()`).

## When to use it
- When defining structured outputs, agent tool arguments, or API request schemas in Python LLM applications.
- When validating data extracted from unstructured documents or web scrapers.
- When configuring complex application settings with environment variable fallbacks via `pydantic-settings`.

## When not to use it
- For ultra-low latency, inner-loop array computations where raw NumPy arrays or PyTorch tensors without schema validation are required.

## Getting started
### Installing Pydantic v2
Install Pydantic via pip:

```bash
pip install pydantic
```

### Basic Model Definition and Validation
Define a declarative Pydantic model:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class UserProfile(BaseModel):
    id: int
    name: str = Field(description="Full user display name")
    email: EmailStr
    roles: List[str] = Field(default_factory=list)
    is_active: bool = True

# Validate incoming payload
user = UserProfile(
    id=101,
    name="Jane Doe",
    email="jane.doe@example.com",
    roles=["admin", "developer"]
)

print(user.model_dump_json(indent=2))
```

## CLI examples
Inspecting Pydantic models or generating JSON schemas via Python CLI execution:

```bash
# Print generated JSON Schema for tool calling definition
python3 -c "from pydantic import BaseModel; class ToolArgs(BaseModel): query: str; count: int = 5; print(ToolArgs.model_json_schema())"
```

## API examples
The following Python script demonstrates using Pydantic v2 models for LLM structured output parsing and tool call schema extraction:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any
import json

class AgentAction(BaseModel):
    tool_name: str = Field(description="Name of the tool to execute")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments to pass to the tool")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Model confidence score between 0 and 1")

    @field_validator('tool_name')
    @classmethod
    def validate_tool_name(cls, v: str) -> str:
        valid_tools = {'search_web', 'query_database', 'send_email', 'final_answer'}
        if v not in valid_tools:
            raise ValueError(f"Tool '{v}' is not in the allowed toolset: {valid_tools}")
        return v

class StructuredAgentResponse(BaseModel):
    thought_process: str = Field(description="Chain-of-thought reasoning steps")
    actions: List[AgentAction] = Field(description="List of agent tool executions to run")

# Example validation usage
if __name__ == "__main__":
    raw_llm_json = """
    {
      "thought_process": "The user requested database search and web search.",
      "actions": [
        {
          "tool_name": "search_web",
          "arguments": {"query": "Pydantic v2 features"},
          "confidence_score": 0.95
        }
      ]
    }
    """
    parsed_response = StructuredAgentResponse.model_validate_json(raw_llm_json)
    print("Parsed Reasoning:", parsed_response.thought_process)
    print("Action Tool:", parsed_response.actions[0].tool_name)
    print("JSON Schema for Tool Calling:\n", json.dumps(StructuredAgentResponse.model_json_schema(), indent=2))
```

## Related tools / concepts
- [Pydantic AI](pydantic-ai.md)
- [Instructor](instructor.md)
- [FastAPI](fastapi.md)
- [LangChain](langchain.md)

## Sources / references
- [Pydantic Official Documentation](https://docs.pydantic.dev/?ref=2026-09-21-audit)
- [Pydantic GitHub Repository](https://github.com/pydantic/pydantic)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
