# Instructor

## What it is
Instructor is a multi-language library (Python, TypeScript, Go, Ruby, etc.) designed specifically for extracting structured data from Large Language Models (LLMs). It uses Pydantic (in Python) and similar schema-validation tools to ensure LLM outputs follow a strict, typed structure. As of late August 2026, **Instructor v2.x** is the industry standard for type-safe LLM integration, natively supporting strict structured schema modes for frontier models like **Claude 5.1** and **GPT-5.5**.

## What problem it solves
It solves the "hallucination" and unpredictability problem of LLM outputs. Instead of receiving raw text that might be hard to parse or non-deterministic, Instructor ensures you get validated, type-safe objects. It automatically handles retries, re-asking the model if the initial output fails validation, and supports complex semantic rules that go beyond simple data types.

## Where it fits in the stack
**Category**: Frameworks / Data Extraction. It acts as the "Validation & Schema" layer between the LLM provider ([OpenAI](../ai_knowledge/openai.md), [Anthropic](../providers/anthropic.md), etc.) and the application logic, often used in conjunction with [PydanticAI](pydantic-ai.md).

## Typical use cases
- **Reliable Data Extraction**: Converting messy natural language (e.g., medical records, customer emails) into structured database records.
- **Agentic Output Shaping**: Ensuring autonomous agents return results in a format that other tools or agents can consume programmatically under **MCP 3.1** Task definitions.
- **Quality Gates**: Implementing subjective validation rules (e.g., "The answer must be polite") that are enforced via LLM-based evaluators and automatic retries.
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
    model="gpt-5.5-preview",
    response_model=User,
    messages=[{"role": "user", "content": "Jason is 25 years old."}],
)

print(user.name) # "Jason"
print(user.age)  # 25
```

## CLI examples

### Instructor CLI
Instructor provides a CLI for testing schemas and inspecting provider capabilities.
```bash
# Check provider capabilities for structured output
instructor hub check openai

# Test a schema against a prompt from the CLI
instructor jobs run --model gpt-5.5-preview --schema UserSchema.py --prompt "Extract user info from: Alice is 30"
```

## API examples

### 1. Semantic Validation with Instructor v2.x
Instructor automatically retries if the LLM generates a response that violates the semantic validation rules.
```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated

client = instructor.from_provider(OpenAI())

def create_semantic_validator(statement: str):
    def validate(v: str) -> str:
        # LLM-based grading step
        grading = client.chat.completions.create(
            model="gpt-5.5-preview",
            response_model=bool,
            messages=[
                {"role": "system", "content": f"Does the following text comply with: '{statement}'? Respond with True or False only."},
                {"role": "user", "content": v}
            ]
        )
        if not grading:
            raise ValueError(f"Content failed semantic policy: {statement}")
        return v
    return validate

class PoliteResponse(BaseModel):
    answer: Annotated[
        str,
        BeforeValidator(create_semantic_validator("The response must be polite, professional, and contain no offensive content."))
    ]

# The client will perform automatic retries on validation failure
```

### 2. Streaming Lists of Objects (MCP 3.1 Conforming)
```python
from pydantic import BaseModel, Field
from typing import List

class TaskItem(BaseModel):
    task_id: str = Field(..., description="Unique alphanumeric identifier for the task")
    command: str = Field(..., description="Shell command or function to execute")
    priority: int = Field(default=1, description="Priority level 1-5")

# Stream a list of task models from a single LLM response
tasks = client.chat.completions.create_iterable(
    model="gpt-5.5-preview",
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
- Last reviewed: 2026-08-03
- Confidence: high
