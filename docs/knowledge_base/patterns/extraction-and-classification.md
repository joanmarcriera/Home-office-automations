# Extraction and Classification

## What it is
Extraction and Classification are fundamental patterns in LLM-powered applications where unstructured text (emails, logs, transcripts) is converted into a structured, typed format (JSON, Pydantic objects) or assigned to specific categories (labels). In June 2026, these patterns rely on **Schema-First Design** and the [Model Context Protocol (MCP 3.0)](../../tools/automation_orchestration/mcp.md) to enforce data integrity across agentic tool calls.

## What problem it solves
LLMs are naturally probabilistic and return text. In software engineering, we need deterministic data to drive application logic, update databases, or trigger specific workflows. This pattern solves:
- **Data Hallucination**: Ensuring the LLM only returns fields defined in a schema.
- **Malformed JSON**: Automatically retrying or correcting responses that fail to parse using frameworks like [Instructor](../../tools/frameworks/instructor.md).
- **Logic Branching**: Mapping open-ended user intent to a fixed set of enums or categories that a system can act upon.
- **Interoperability**: Enabling different agents to exchange structured state objects using standard schemas.

## Where it fits in the stack
This pattern is used at the **Input/Intake layer** of an application or as a **Preprocessing step** in an agentic workflow. It serves as the bridge between [Intake & Storage](../../tools/intake_storage/index.md) and the [Orchestration Layer](../../tools/orchestration/index.md).

## Typical use cases
- **Autonomous Support Triage**: Classifying support tickets (Billing, Technical, Sales) and extracting order IDs into a [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md).
- **Medical Records Synthesis**: Extracting symptoms and diagnoses from transcripts into standardized medical codes.
- **Financial Log Parsing**: Converting bank statements into transaction objects with dates, amounts, and merchants.
- **Agentic Skill Discovery**: Identifying which tool or "skill" an agent should use based on user intent classification.

## Strengths
- **Deterministic Output**: Guarantees that the application receives data it knows how to handle.
- **Automatic Validation**: Validation logic (e.g., regex, range checks) can be baked into Pydantic or Zod schemas.
- **Improved Accuracy**: Constraining the model's output space reduces the likelihood of creative "wandering."
- **Standardization**: Use of [Task Schemas](../../reference-implementations/metadata-schemas/task-schema.md) allows for cross-platform task management.

## Limitations
- **Token Overhead**: Defining complex schemas in the prompt consumes input tokens.
- **Model Capability**: Smaller models (e.g., 8B-70B) may struggle to strictly adhere to complex, nested JSON schemas.
- **Latency**: Validation failures may trigger internal retries (Self-Correction), increasing the overall response time.
- **Schema Rigidity**: Unexpected data formats in the source text might be dropped if they don't fit the predefined schema.

## When to use it
- When you need to bridge the gap between unstructured human input and structured database/API operations.
- To implement "guardrails" for your model's output format.
- For high-volume data processing where manual classification is impossible.
- When building [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) that require reliable tool inputs.

## When not to use it
- For general-purpose chatbots where the user expects a conversational response without downstream side effects.
- When the output structure is highly dynamic and cannot be defined upfront.
- For simple keyword extraction that can be handled by regex or traditional NLP (e.g., [ripgrep](../../tools/development_ops/ripgrep.md)).

## Getting started
1. **Define the Schema**: Use [Pydantic](https://docs.pydantic.dev/) (Python) or [Zod](https://zod.dev/) (TypeScript) to describe the desired output.
2. **Select a Framework**: Choose [Instructor](../../tools/frameworks/instructor.md) for multi-provider support or [PydanticAI](../../tools/frameworks/pydantic-ai.md) for Python-native workflows.
3. **Configure the Model**: Ensure the model supports "JSON Mode" or "Tool Calling" (e.g., GPT-5.5, Claude 4.8).
4. **Implement Retry Logic**: Set up a loop to handle validation errors by feeding them back into the model for correction.
5. **Verify Output**: Pass the structured object to your downstream service (e.g., [ServiceNow](../../tools/automation_orchestration/servicenow-mcp.md)).

## CLI examples
Using the [Instructor](../../tools/frameworks/instructor.md) CLI to extract data from a text file:

```bash
# Extract entities from a text file using a predefined Pydantic schema (conceptual)
instructor extract --model gpt-4o --schema schemas.TicketInfo --file input.txt
```

Using [ripgrep](../../tools/development_ops/ripgrep.md) for simple, deterministic extraction:
```bash
# Find all occurrences of Order IDs in logs
rg -o "ORD-[0-9]{5}" logs/production.log
```

## API examples
Extraction using [Instructor](../../tools/frameworks/instructor.md) and Pydantic in Python:

```python
from pydantic import BaseModel, Field
from enum import Enum
import instructor
from openai import OpenAI

class Label(str, Enum):
    BILLING = "billing"
    TECH_SUPPORT = "tech_support"

class Ticket(BaseModel):
    category: Label
    urgency: int = Field(ge=1, le=5)
    order_id: str | None

client = instructor.from_provider(OpenAI())

ticket = client.chat.completions.create(
    model="gpt-5-5-preview",
    response_model=Ticket,
    messages=[{"role": "user", "content": "I need a refund for ORD-99821"}]
)
# Result: Ticket(category='billing', urgency=4, order_id='ORD-99821')
```

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md) — The standard for structured LLM extraction.
- [PydanticAI](../../tools/frameworks/pydantic-ai.md) — Agentic framework using Pydantic for validation.
- [Vercel AI SDK](../../tools/development_ops/vercel-ai-sdk.md) — TypeScript toolkit for structured outputs.
- [DSPy](../../tools/frameworks/dspy.md) — Optimizing extraction signatures programmatically.
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) — Standardized metadata for tasks.
- [Date Extraction](date-extraction.md) — Specialized pattern for temporal data.
- [ServiceNow MCP](../../tools/automation_orchestration/servicenow-mcp.md) — Target for extracted ticket data.
- [ripgrep](../../tools/development_ops/ripgrep.md) — Deterministic keyword extraction.

## Sources / References
- [Instructor Documentation: Philosophy of Extraction](https://python.useinstructor.com/concepts/philosophy/)
- [OpenAI: Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [PydanticAI: Results and Validation](https://ai.pydantic.dev/results/)
- [Zod: TypeScript-first Schema Validation](https://zod.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
