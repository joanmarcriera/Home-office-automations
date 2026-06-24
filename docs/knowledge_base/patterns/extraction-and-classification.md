# Extraction and Classification

## What it is
Extraction and Classification are fundamental patterns in LLM-powered applications where unstructured text (emails, logs, transcripts, images) is converted into a structured, typed format (JSON, Pydantic objects) or assigned to specific categories (labels). In 2026, these patterns rely on **Schema-First Design** and native model capabilities for structured outputs to enforce data integrity and enable agentic workflows.

## What problem it solves
LLMs are naturally probabilistic and return text. In software engineering, we need deterministic data to drive application logic, update databases, or trigger specific workflows. This pattern solves:
- **Data Hallucination**: Ensuring the LLM only returns fields defined in a schema.
- **Malformed JSON**: Using native model constraints (like OpenAI Structured Outputs or Claude JSON Mode) to prevent parsing errors.
- **Logic Branching**: Mapping open-ended user intent to a fixed set of enums or categories that a system can act upon.
- **Data Transformation**: Converting messy, human-readable data into machine-readable "Golden Datasets" for downstream analytics or RAG.

## Where it fits in the stack
This pattern is used at the **Input/Intake layer** of an application or as a **Preprocessing step** in an agentic workflow. It acts as the bridge between the **Data Layer** (unstructured) and the **Business Logic Layer** (structured).

## Typical use cases
- **Customer Support**: Classifying tickets (Billing, Technical, Sales) and extracting order IDs or account numbers.
- **Medical Records**: Extracting symptoms, dosages, and diagnoses into standardized codes (ICD-10).
- **Financial Intelligence**: Parsing bank statements or invoices into transaction objects with dates, amounts, and merchants.
- **Content Moderation**: Classifying user-generated content against safety and community guidelines.
- **Document Processing**: Using [Docling](../../tools/process_understanding/docling.md) or [Crawl4AI](../../tools/process_understanding/crawl4ai.md) to extract structured facts from PDFs or web pages.

## Strengths
- **Deterministic Output**: Guarantees that the application receives data it knows how to handle.
- **Automatic Validation**: Validation logic (e.g., regex, range checks, custom logic) can be baked into the schema (e.g., via Pydantic).
- **Improved Accuracy**: Constraining the model's output space reduces the likelihood of creative "wandering."
- **Efficiency**: Allows for high-volume, automated processing of data that previously required manual human review.

## Limitations
- **Token Overhead**: Defining complex schemas (especially with descriptions for every field) consumes input tokens.
- **Model Capability**: Smaller or older models may struggle to strictly adhere to complex JSON schemas.
- **Latency**: Validation failures may trigger internal retries, increasing the overall response time.
- **Schema Rigidity**: If the schema is too narrow, it might miss nuance or "unexpected" but important information in the source text.

## When to use it
- When you need to bridge the gap between unstructured human input and structured database/API operations.
- To implement "guardrails" for your model's output format.
- For high-volume data processing where manual classification is impossible or too slow.
- When building agents that need to produce "Artifacts" (e.g., a formal report or a configuration file).

## When not to use it
- For general-purpose chatbots where the user expects a conversational, open-ended response.
- When the output structure is highly dynamic and cannot be defined upfront.
- When the overhead of a large model is too high for a task that could be solved with simple regex or a small BERT model.

## Getting started
To implement extraction and classification:
1. **Define your Schema**: Use Pydantic (Python) or Zod (TypeScript) to define the target structure.
2. **Select a Library**: Use [Instructor](../../tools/frameworks/instructor.md) for its simplicity and cross-provider support.
3. **Choose a Model**: Use a model with strong structured output support (e.g., GPT-5.5, Claude 4.8, or Gemini 3.5 Pro).
4. **Iterate on Field Descriptions**: Add clear instructions to each field in your schema to guide the model.
5. **Handle Failures**: Implement retry logic for validation errors.

## CLI examples
Using `curl` to test a classification endpoint:

```bash
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "messages": [
      {"role": "system", "content": "You are a classifier. Respond ONLY in JSON."},
      {"role": "user", "content": "Classify this: I love the new features!"}
    ],
    "response_format": { "type": "json_schema", "json_schema": {"name": "sentiment", "schema": {"type": "object", "properties": {"label": {"type": "string", "enum": ["positive", "negative", "neutral"]}}, "required": ["label"]}}}
  }'
```

## API examples
Example using [Instructor](../../tools/frameworks/instructor.md) and Pydantic:

```python
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import instructor
from openai import OpenAI

class Category(str, Enum):
    BILLING = "billing"
    TECH_SUPPORT = "tech_support"
    GENERAL = "general"

class TicketInfo(BaseModel):
    category: Category = Field(description="The primary department for the ticket")
    urgency: int = Field(..., ge=1, le=5, description="1 is low, 5 is critical")
    entities: List[str] = Field(description="List of order IDs, account numbers, or tracking codes found")

client = instructor.from_provider(OpenAI())

ticket = client.chat.completions.create(
    model="gpt-5.5-preview",
    response_model=TicketInfo,
    messages=[{"role": "user", "content": "My order #12345 hasn't arrived and I want a refund."}]
)
# Result: TicketInfo(category='billing', urgency=4, entities=['#12345'])
```

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md) — The industry standard for structured extraction.
- [PydanticAI](../../tools/frameworks/pydantic-ai.md) — Schema-first agent framework from the Pydantic team.
- [Vercel AI SDK](../../tools/development_ops/vercel-ai-sdk.md) — TypeScript-native extraction and routing.
- [DSPy](../../tools/frameworks/dspy.md) — Programmatic prompt optimization for extraction signatures.
- [Docling](../../tools/process_understanding/docling.md) — High-fidelity document parsing and extraction.
- [Crawl4AI](../../tools/process_understanding/crawl4ai.md) — Agent-ready web crawling and data extraction.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — For extracting data directly into tools.
- [OpenAI Structured Outputs](../../tools/ai_knowledge/openai.md) — Native model-level schema enforcement.

## Sources / References
- [Instructor: Philosophy of Extraction](https://python.useinstructor.com/concepts/philosophy/)
- [OpenAI: Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [PydanticAI: Results and Validation](https://ai.pydantic.dev/results/)
- [Anthropic: Tool Use (Extraction)](https://docs.anthropic.com/claude/docs/tool-use)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
