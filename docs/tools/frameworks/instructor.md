# Instructor

## What it is
Instructor is a multi-language library (Python, TypeScript, Go, Ruby, PHP, etc.) designed specifically for extracting structured data from Large Language Models (LLMs). Following its v2 rewrite, it focuses on a simplified `from_provider` integration pattern and enhanced semantic validation using Pydantic (in Python) and similar schema-validation tools to ensure LLM outputs follow a strict, typed structure.

## What problem it solves
It solves the "hallucination" and unpredictability problem of LLM outputs. Instead of receiving raw text that might be hard to parse, Instructor ensures you get validated, type-safe objects, automatically handling retries and re-asking the model if the initial output fails validation.

## Where it fits in the stack
**Category**: Frameworks / Data Extraction

## Typical use cases
- **Reliable Data Extraction**: Converting messy natural language (e.g., customer support emails) into structured database records.
- **Type-Safe LLM Integration**: Ensuring LLM outputs can be directly used in application logic without complex parsing or regex.
- **Quality Gates**: Implementing validation rules (e.g., "age must be positive", "response must not contain profanity") that are enforced via LLM retries.
- **Semantic Validation**: Using LLMs to validate the content of extracted fields (e.g., "is this summary actually concise?").

## Strengths
- **Schema-First**: Define what you want using standard types (Pydantic, Zod, etc.).
- **Automatic Retries**: Built-in logic to re-prompt the LLM when validation fails.
- **Multi-Provider**: Works with OpenAI, Anthropic, Gemini, DeepSeek, Ollama, and many others.
- **Lightweight**: Focuses on structured output rather than being a full agent orchestration framework.
- **Type Inference**: Excellent IDE support and autocompletion for extracted data.

## Limitations
- **Narrow Focus**: It is not a general-purpose agent framework (like CrewAI or AutoGen); it does structured extraction exceptionally well.
- **Schema Dependency**: Requires defining formal schemas upfront, which might be overkill for simple text-to-text tasks.

## When to use it
- When you need reliable, type-safe data extraction from LLMs for use in programmatic workflows.
- If you want a lightweight solution that integrates easily with your existing OpenAI/Anthropic/Gemini client code.
- To enforce complex validation rules and automatic retries on LLM outputs using schema-based validation.

## When not to use it
- For open-ended creative writing or chat where a strict schema is not necessary or possible.
- If you need a comprehensive framework for managing complex multi-agent conversations and memory (consider LangGraph or CrewAI).

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

# Patch the client to add Instructor functionality (v2 syntax)
client = instructor.from_provider(OpenAI())

user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    messages=[{"role": "user", "content": "Jason is 25 years old."}],
)

print(user.name) # "Jason"
print(user.age)  # 25
```

### Semantic Validation Example
Instructor allows you to use an LLM to validate the output of another (or the same) LLM call.

```python
from typing_extensions import Annotated
from pydantic import AfterValidator
from instructor import llm_validator

def is_concise(v: str):
    # This uses an LLM to check if the text is concise
    return llm_validator("is this concise?", model="gpt-4o-mini")(v)

class Summary(BaseModel):
    content: Annotated[str, AfterValidator(is_concise)]

# Instructor will automatically retry if the LLM-based validator fails
```

## Related tools / concepts
- [PydanticAI](pydantic-ai.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) (uses Zod for similar patterns in TS)
- [DSPy](dspy.md)
- [Structured Output Pattern](../../knowledge_base/patterns/index.md)
- [LiteLLM](../../services/litellm.md)
- [Firebase Genkit](firebase-genkit.md)
- [Extraction and Classification](../../knowledge_base/patterns/extraction-and-classification.md)
- [Date Extraction](../../knowledge_base/patterns/date-extraction.md)

## Sources / references
- [Official Website](https://python.useinstructor.com/)
- [GitHub Repository](https://github.com/jxnl/instructor)
- [Instructor Cookbook](https://python.useinstructor.com/examples/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
