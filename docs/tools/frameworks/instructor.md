# Instructor

## What it is
Instructor is a multi-language library (Python, TypeScript, Go, Ruby, Rust) designed specifically for extracting structured data from Large Language Models (LLMs). It uses Pydantic (in Python) and similar schema-validation tools to ensure LLM outputs follow a strict, typed structure. As of early January 2027, **Instructor v2.x** remains the industry standard for type-safe LLM integration, natively supporting strict structured schema modes for frontier models like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra**.

## Architecture & Validation Flow

```
                                +------------------------------------+
                                |    Application Code / FastMCP 3.1  |
                                +-----------------+------------------+
                                                  | Define Pydantic v2 Schema
                                                  v
                                +-----------------+------------------+
                                |    Instructor v2.x Client Engine   |
                                |  - Schema -> JSON Schema Mode     |
                                |  - System Prompt Injection         |
                                +-----------------+------------------+
                                                  | Call LLM API (Structured Outputs)
                                                  v
                                +-----------------+------------------+
                                |    Frontier LLM Provider           |
                                |  (Claude 5.6 / GPT-5.6 / Gemini)  |
                                +-----------------+------------------+
                                                  | Raw JSON Response
                                                  v
                                +-----------------+------------------+
                                |   Pydantic v2 Validation Engine    |
                                |  - Type Validation                 |
                                |  - AfterValidator / Field Rules   |
                                +--------+-------------------+-------+
                                         |                   |
                           Validation OK |                   | Validation Error
                                         v                   v
                        +----------------+---+      +--------+-------------------+
                        | Validated Typed    |      | Re-prompt Loop (Retries)   |
                        | Object Instantiation|      | Error Traceback back to LLM|
                        +--------------------+      +----------------------------+
```

## What problem it solves
It solves the "hallucination" and unpredictability problem of LLM outputs. Instead of receiving raw text that might be hard to parse or non-deterministic, Instructor ensures you get validated, type-safe objects. It automatically handles retries, re-asking the model if the initial output fails validation, and supports complex semantic rules that go beyond simple data types.

## Feature Comparison Matrix

| Dimension / Feature | Instructor v2.x | PydanticAI | Vercel AI SDK (`generateObject`) | Raw LLM JSON Mode |
| :--- | :--- | :--- | :--- | :--- |
| **Language Support** | Python, TS, Go, Ruby, Rust | Python | TypeScript / JavaScript | All (REST API) |
| **Validation Mechanism** | Native Pydantic v2 / Zod | Native Pydantic v2 | Zod | Manual Post-Parsing |
| **Self-Correction Retries** | Automatic with trace | Automatic with trace | Manual Retry Logic | Custom Error Handling |
| **Semantic Rules** | `AfterValidator` + LLM Grading | System Prompts | Custom Transformers | None |
| **FastMCP 3.1 Native** | First-Class Tool Schema | First-Class Agent Frame | First-Class Server Route | Manual Parsing |

## Where it fits in the stack
**Category**: Frameworks / Data Extraction. It acts as the "Validation & Schema" layer between the LLM provider ([OpenAI](../ai_knowledge/openai.md), [Anthropic](../providers/anthropic.md), etc.) and the application logic, often used in conjunction with [PydanticAI](pydantic-ai.md).

## Typical use cases
- **Reliable Data Extraction**: Converting messy natural language (e.g., medical records, customer emails) into structured database records.
- **Agentic Output Shaping**: Ensuring autonomous agents return results in a format that other tools or agents can consume programmatically under **FastMCP 3.1** Task Protocol definitions.
- **Quality Gates**: Implementing subjective validation rules (e.g., "The answer must be polite and accurate") that are enforced via LLM-based evaluators and automatic retries.
- **Streaming Structured Data**: Processing partial LLM responses in real-time while maintaining schema validity.

## Strengths
- **Schema-First Design**: Define what you want using standard types (Pydantic models, Zod schemas, etc.) and let Instructor handle the prompting.
- **Universal Provider Support**: Works seamlessly with OpenAI, Anthropic, Gemini, DeepSeek, Ollama, and many others via a unified interface.
- **Semantic Validation**: Built-in support for validating LLM outputs against subjective criteria using LLM-based validators.
- **High Performance**: Optimized for low-latency extraction with enhanced support for parallel tool calling and strict JSON schema modes.

## Limitations
- **Narrow Focus**: It is not a general-purpose agent orchestration framework (like [LangGraph](langgraph.md) or [CrewAI](crewai.md)); it focuses exclusively on structured output.
- **Schema Overhead**: Requires defining formal schemas upfront, which might be unnecessary for simple, free-form chat applications.
- **Retry Cost**: Multiple retries on complex validation failures can increase token usage and latency.

## When to use it
- When you need reliable, type-safe data extraction from LLMs for use in programmatic workflows.
- If you want a lightweight solution that integrates easily with your existing LLM client code without adopting a heavy framework.
- To enforce complex validation rules and automatic retries on LLM outputs using schema-based validation.

## When not to use it
- For open-ended creative writing or simple chat where a strict schema is not required.
- If you need a comprehensive framework for managing complex multi-agent state machines (consider [LangGraph](langgraph.md)).

## Getting started

### Installation (Python)
```bash
pip install instructor pydantic
```

### Basic Extraction Example
```python
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

class User(BaseModel):
    name: str = Field(..., description="The user's full name")
    age: int = Field(..., description="The user's age in years")

# Patch the client to add Instructor functionality
client = instructor.from_provider(OpenAI())

user = client.chat.completions.create(
    model="gpt-5.6",
    response_model=User,
    messages=[{"role": "user", "content": "Jason is 25 years old."}],
)

print(user.name) # "Jason"
print(user.age)  # 25
```

## FastMCP 3.1 Task Protocol Integration

In early 2027, Instructor integrates directly with FastMCP 3.1 Task Protocol servers to provide schema-validated tool calling:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

mcp = FastMCP("InstructorTaskServer", version="3.1.0")
client = instructor.from_provider(OpenAI())

class IncidentReport(BaseModel):
    service_name: str = Field(..., description="Affected system or service name")
    severity: str = Field(..., description="Incident severity level: LOW, MED, HIGH, CRITICAL")
    remediation_steps: list[str] = Field(..., description="Ordered resolution action items")

@mcp.tool()
async def extract_incident_summary(raw_log_text: str) -> IncidentReport:
    """Uses Instructor v2.x to extract structured incident reports from unstructured logs."""
    report = client.chat.completions.create(
        model="gpt-5.6",
        response_model=IncidentReport,
        messages=[
            {"role": "system", "content": "Extract incident data accurately."},
            {"role": "user", "content": raw_log_text}
        ]
    )
    return report

if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### Instructor CLI
Instructor provides a CLI for testing schemas and inspecting provider capabilities.
```bash
# Check provider capabilities for structured output
instructor hub check openai

# Test a schema against a prompt from the CLI
instructor jobs run --model gpt-5.6 --schema UserSchema.py --prompt "Extract user info from: Alice is 30"
```

## API examples

### 1. Semantic Validation with Instructor v2.x and Strict Pydantic v2
Instructor automatically retries if the LLM generates a response that violates the semantic validation rules. This example utilizes `AfterValidator` and a strict schema validation setup to enforce professional tone guidelines with an auto-retry loop.
```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, AfterValidator, ConfigDict
from typing_extensions import Annotated

# Patch the OpenAI client to support Instructor structured execution
client = instructor.from_provider(OpenAI())

def validate_professional_tone(v: str) -> str:
    # LLM-based grading step for semantic validation
    response = client.chat.completions.create(
        model="gpt-5.6",
        response_model=bool,
        messages=[
            {
                "role": "system",
                "content": (
                    "Evaluate if the given text is highly professional, polite, and matches "
                    "corporate support standards. Reply with True or False only."
                )
            },
            {"role": "user", "content": v}
        ]
    )
    if not response:
        raise ValueError("Text failed semantic validation: Content is impolite or unprofessional.")
    return v

class ProfessionalResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True
    )

    # Attach the validator as an Annotated Metadata using Pydantic v2 AfterValidator
    support_message: Annotated[str, AfterValidator(validate_professional_tone)] = Field(
        ...,
        description="The customer-facing support message containing helpful guidelines."
    )

# When creating completions, Instructor catches the validation error and automatically
# self-corrects by sending the error traceback back to the model (up to max_retries).
try:
    response = client.chat.completions.create(
        model="gpt-5.6",
        response_model=ProfessionalResponse,
        max_retries=3,
        messages=[
            {
                "role": "user",
                "content": "Draft a message telling a customer their subscription payment was rejected. Be blunt."
            }
        ]
    )
    print("Validated Message:", response.support_message)
except Exception as e:
    print("Failed to produce validated response after retries:", e)
```

### 2. Streaming Lists of Objects (FastMCP 3.1 Conforming)
```python
from pydantic import BaseModel, Field, ConfigDict
from typing import List

class TaskItem(BaseModel):
    model_config = ConfigDict(extra="forbid", freeze=True)

    task_id: str = Field(..., description="Unique alphanumeric identifier for the task")
    command: str = Field(..., description="Shell command or function to execute")
    priority: int = Field(default=1, description="Priority level 1-5")

# Stream a list of task models from a single LLM response
tasks = client.chat.completions.create_iterable(
    model="gpt-5.6",
    response_model=TaskItem,
    messages=[{"role": "user", "content": "Decompose the project build setup into 3 priority tasks."}],
)

for task in tasks:
    print(f"[{task.priority}] {task.task_id}: {task.command}")
```

## Related tools / concepts
- [PydanticAI](pydantic-ai.md) — higher-level agentic framework built on Pydantic.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — TypeScript alternative for structured output.
- [DSPy](dspy.md) — for programmatic prompt optimization.
- [Extraction and Classification](../../knowledge_base/patterns/extraction-and-classification.md) — general design pattern.
- [Date Extraction](../../knowledge_base/patterns/date-extraction.md) — specialized extraction pattern.
- [LiteLLM](../../services/litellm.md) — often used as a provider backend for Instructor.
- [Firebase Genkit](firebase-genkit.md) — Google's framework with similar schema-based typing.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — the architectural context for structured data exchange.

## Sources / references
- [Official Website](https://python.useinstructor.com/)
- [Instructor GitHub Repository](https://github.com/jxnl/instructor)
- [Instructor Cookbook](https://python.useinstructor.com/examples/)
- [What's new in Instructor v2?](https://python.useinstructor.com/blog/2026/05/11/whats-new-in-instructor-v2/)
- [Semantic Validation Guide](https://python.useinstructor.com/concepts/validation/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
