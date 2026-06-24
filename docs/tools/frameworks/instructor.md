# Instructor

## What it is
Instructor is a multi-language library (Python, TypeScript, Go, Ruby, etc.) designed specifically for extracting structured data from Large Language Models (LLMs). It uses Pydantic (in Python) and similar schema-validation tools to ensure LLM outputs follow a strict, typed structure. As of June 2026, **Instructor v2** is the industry standard for type-safe LLM integration and semantic validation.

## What problem it solves
It solves the "hallucination" and unpredictability problem of LLM outputs. Instead of receiving raw text that might be hard to parse or non-deterministic, Instructor ensures you get validated, type-safe objects. It automatically handles retries, re-asking the model if the initial output fails validation, and supports complex semantic rules that go beyond simple data types.

## Where it fits in the stack
**Category**: Frameworks / Data Extraction. It acts as the "Validation & Schema" layer between the LLM provider ([OpenAI](../ai_knowledge/openai.md), [Anthropic](../providers/anthropic.md), etc.) and the application logic, often used in conjunction with [PydanticAI](pydantic-ai.md).

## Typical use cases
- **Reliable Data Extraction**: Converting messy natural language (e.g., medical records, customer emails) into structured database records.
- **Agentic Output Shaping**: Ensuring autonomous agents return results in a format that other tools or agents can consume programmatically.
- **Quality Gates**: Implementing subjective validation rules (e.g., "The answer must be polite") that are enforced via LLM-based evaluators and automatic retries.
- **Streaming Structured Data**: Processing partial LLM responses in real-time while maintaining schema validity.

## Strengths
- **Schema-First Design**: Define what you want using standard types (Pydantic models, Zod schemas, etc.) and let Instructor handle the prompting.
- **Universal Provider Support**: Works seamlessly with OpenAI, Anthropic, Gemini, DeepSeek, Ollama, and many others via a unified interface.
- **Semantic Validation**: Built-in support for validating LLM outputs against subjective criteria using LLM-based validators.
- **High Performance**: Optimized for low-latency extraction with enhanced support for parallel tool calling.

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
pip install instructor
```

### Basic Extraction Example
```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

class User(BaseModel):
    name: str
    age: int

# Patch the client to add Instructor functionality
client = instructor.from_provider(OpenAI())

user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    messages=[{"role": "user", "content": "Jason is 25 years old."}],
)

print(user.name) # "Jason"
```

## CLI examples

### Instructor CLI
Instructor provides a CLI for testing schemas and inspecting provider capabilities.
```bash
# Check provider capabilities for structured output
instructor hub check openai

# Test a schema against a prompt from the CLI
instructor jobs run --model gpt-4o --schema UserSchema.py --prompt "Extract user info from: Alice is 30"
```

## API examples

### 1. Semantic Validation with Instructor v2
```python
from instructor import SemanticValidator
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated

class Response(BaseModel):
    answer: Annotated[
        str,
        BeforeValidator(SemanticValidator(openai_client=client, statement="The answer must be polite and helpful"))
    ]

# Instructor will automatically retry if the LLM generates an impolite response
```

### 2. Streaming Lists of Objects
```python
users = client.chat.completions.create_iterable(
    model="gpt-4o",
    response_model=User,
    messages=[{"role": "user", "content": "Generate a list of 3 users."}],
)

for user in users:
    print(user.name)
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
- [GitHub Repository](https://github.com/jxnl/instructor)
- [Instructor Cookbook](https://python.useinstructor.com/examples/)
- [What's new in Instructor v2?](https://python.useinstructor.com/blog/2026/05/11/whats-new-in-instructor-v2/)
- [Semantic Validation Guide](https://python.useinstructor.com/concepts/validation/)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
