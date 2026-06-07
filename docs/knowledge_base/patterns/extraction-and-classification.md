# Extraction and Classification

## What it is
Extraction and Classification are fundamental patterns in LLM-powered applications where unstructured text (emails, logs, transcripts) is converted into a structured, typed format (JSON, Pydantic objects) or assigned to specific categories (labels). These patterns rely on **Schema-First Design** to enforce data integrity.

## What problem it solves
LLMs are naturally probabilistic and return text. In software engineering, we need deterministic data to drive application logic, update databases, or trigger specific workflows. This pattern solves:
- **Data Hallucination**: Ensuring the LLM only returns fields defined in a schema.
- **Malformed JSON**: Automatically retrying or correcting responses that fail to parse.
- **Logic Branching**: Mapping open-ended user intent to a fixed set of enums or categories that a system can act upon.

## Where it fits in the stack
This pattern is used at the **Input/Intake layer** of an application or as a **Preprocessing step** in an agentic workflow.

## Core Concepts

### 1. Schema-First Extraction
Defining the desired output shape before the model is called. Libraries like [Instructor](../../tools/frameworks/instructor.md) use Pydantic models to describe the target object, which is then used to generate system instructions and validate the LLM response.

### 2. Multi-Label Classification
Assigning a text input to one or more predefined categories. This is often more reliable than open-ended "intent detection" because the model is constrained to a known list of valid labels.

### 3. Entity Recognition (NER)
Extracting specific "entities" (names, organizations, product IDs) from text and mapping them to structured objects, often with associated metadata or confidence scores.

## Key Implementation Tools
- **[Instructor](../../tools/frameworks/instructor.md)**: The standard-bearer for structured extraction across Python, TS, and Go.
- **[PydanticAI](../../tools/frameworks/pydantic-ai.md)**: A Python-native framework that uses Pydantic for both input and output validation.
- **[Vercel AI SDK](../../tools/development_ops/vercel-ai-sdk.md)**: Uses Zod in the TypeScript ecosystem for enforcing structured outputs.
- **[DSPy](../../tools/frameworks/dspy.md)**: Allows for optimizing extraction prompts and signatures programmatically.

## Typical Use Cases
- **Customer Support**: Classifying tickets (Billing, Technical, Sales) and extracting order IDs.
- **Medical Records**: Extracting symptoms and diagnoses into standardized medical codes.
- **Financial Logs**: Parsing bank statements into transaction objects with dates, amounts, and merchants.
- **Content Moderation**: Classifying user-generated content against safety guidelines.

## Technical Example: Extraction with Instructor
Below is a Python example using [Instructor](../../tools/frameworks/instructor.md) and Pydantic:

```python
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import instructor
from openai import OpenAI

class Label(str, Enum):
    BILLING = "billing"
    TECH_SUPPORT = "tech_support"
    GENERAL = "general"

class TicketInfo(BaseModel):
    category: Label
    urgency: int = Field(..., ge=1, le=5)
    entities: List[str] = Field(description="Order IDs, account numbers, etc.")

client = instructor.from_provider(OpenAI())

ticket = client.chat.completions.create(
    model="gpt-4o",
    response_model=TicketInfo,
    messages=[{"role": "user", "content": "My order #12345 hasn't arrived and I want a refund."}]
)
# Result: TicketInfo(category='billing', urgency=4, entities=['#12345'])
```

## Strengths
- **Deterministic Output**: Guarantees that the application receives data it knows how to handle.
- **Automatic Validation**: Validation logic (e.g., regex, range checks) can be baked into the schema.
- **Improved Accuracy**: Constraining the model's output space reduces the likelihood of creative "wandering."

## Limitations
- **Token Overhead**: Defining complex schemas in the prompt consumes input tokens.
- **Model Capability**: Smaller or older models may struggle to strictly adhere to complex JSON schemas.
- **Latency**: Validation failures may trigger internal retries, increasing the overall response time.

## When to use it
- When you need to bridge the gap between unstructured human input and structured database/API operations.
- To implement "guardrails" for your model's output format.
- For high-volume data processing where manual classification is impossible.

## When not to use it
- For general-purpose chatbots where the user expects a conversational response.
- When the output structure is highly dynamic and cannot be defined upfront.

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md)
- [PydanticAI](../../tools/frameworks/pydantic-ai.md)
- [Vercel AI SDK](../../tools/development_ops/vercel-ai-sdk.md)
- [DSPy](../../tools/frameworks/dspy.md)

## Related Patterns
- [RAG](../../knowledge_base/patterns/rag.md)
- [Tool Calling](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Date Extraction](../../knowledge_base/patterns/date-extraction.md)

## Sources / References
- [Instructor: Philosophy of Extraction](https://python.useinstructor.com/concepts/philosophy/)
- [OpenAI: Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [PydanticAI: Results and Validation](https://ai.pydantic.dev/results/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
