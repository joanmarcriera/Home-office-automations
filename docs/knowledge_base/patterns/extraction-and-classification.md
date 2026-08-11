# Extraction and Classification

## What it is
Extraction and Classification are fundamental patterns in LLM-powered applications where unstructured text (such as emails, logs, transcripts, or invoices) is converted into a structured, typed format (e.g., JSON, Pydantic objects) or assigned to specific categorical enums. In late December 2026, these patterns rely on **Schema-First Design** and the **Model Context Protocol (MCP 3.1)** / FastMCP 3.1 to enforce strict, validated data integrity constraints across multi-agent tool calls and collaborative workspaces.

## What problem it solves
LLMs are inherently probabilistic and return unstructured text by default. However, software architectures require deterministic, strongly typed data to execute downstream business logic, update relational databases, or trigger operational pipelines. This pattern solves:
- **Data Hallucination**: Restricting the LLM's output parameters to explicitly defined schema fields and constraints.
- **Malformed Parser Responses**: Automatically catching, retrying, or self-correcting JSON outputs that fail validation using tools like [Instructor](../../tools/frameworks/instructor.md).
- **Automated Workflow Triage**: Seamlessly mapping free-form customer or system intent to fixed, actionable category labels and urgency levels.
- **Ecosystem Interoperability**: Establishing shared, verifiable data contracts (such as [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md)) across heterogeneous agent systems.

## Where it fits in the stack
This pattern operates at the **Input/Intake and Preprocessing layers** of an agentic application. It serves as the bridge between raw ingestion sources ([Intake & Storage](../../tools/intake_storage/index.md)) and execution engines ([Orchestration Layer](../../tools/orchestration/index.md)).

## Typical use cases
- **Autonomous Support Triage**: Classifying incoming support tickets into specialized departments (e.g., Billing, Technical, Sales) and extracting specific identifiers like order IDs into a [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md).
- **Medical Diagnostics Parsing**: Normalizing clinical reports, patient notes, or voice transcripts into structured health enums and symptoms.
- **Financial Transaction Extraction**: Converting unstructured bank statements or receipts into absolute, normalized expense objects with timestamps, merchant details, and amounts for ingestion.
- **Intent-Based Skill Selection**: Classifying user queries in conversational assistants to select the most appropriate execution tool or sub-agent.

## Strengths
- **Type Safety and Determinism**: Guarantees that the orchestrator receives data in an expected format, reducing downstream failures.
- **Baked-In Validation Rules**: Leverages built-in validation logic (e.g., regex constraints, numerical ranges, custom field validators) directly inside Pydantic or Zod models.
- **Reduced Output Drift**: Forcing models to output schema-compliant formats drastically reduces creative "hallucinations."
- **Observability**: Clearly logs structured state transitions, making the reasoning steps of agents auditable.

## Limitations
- **Token Overhead**: Defining complex, nested schemas in system prompts or tool schemas consumes significant input tokens.
- **Small-Model Compliance**: Smaller open-weight models (e.g., 8B parameters) can struggle to strictly adhere to complex, deeply nested schemas.
- **Latency from Retries**: Undergoing self-correction loops when schema validation fails adds extra LLM rounds and latency.
- **Rigid Data Structure**: Real-world variability that does not map directly to the predefined schema fields may be truncated or lost.

## When to use it
- When bridging the gap between raw human input (text or speech) and structured backend systems (relational databases, REST APIs).
- When implementing automated data validation, cleaning, or normalization pipelines.
- For high-throughput classification tasks where manual taring is inefficient.
- When orchestrating [Agentic Workflows](agentic-workflows.md) that require reliable inputs.

## When not to use it
- For open-ended, creative conversation interfaces where structured constraints are unnecessary.
- When the expected target fields are highly dynamic and cannot be represented by a fixed, pre-defined schema.
- For simple string searches or keyword detections that are more efficiently solved by deterministic regex engines or search utilities like [ripgrep](../../tools/development_ops/ripgrep.md).

## Getting started
1. **Define the Target Schema**: Use [Pydantic](https://docs.pydantic.dev/) in Python or [Zod](https://zod.dev/) in TypeScript to define the expected structure, enums, and validations.
2. **Select an LLM Framework**: Utilize [Instructor](../../tools/frameworks/instructor.md) for lightweight, multi-provider structured extraction, or [PydanticAI](../../tools/frameworks/pydantic-ai.md) for specialized agentic workflows.
3. **Choose a Structured Inference Model**: Ensure the target model natively supports JSON Mode or tool calling (e.g., Claude 5.1, GPT-5.5, Llama 4).
4. **Configure Self-Correction Retries**: Set up validation handlers to capture schema violations and feed the errors back to the model for inline correction.
5. **Route Extracted Entities**: Pass the validated object to down-stream services (e.g., [ServiceNow](../../tools/automation_orchestration/servicenow-mcp.md) or database interfaces).

## CLI examples
Using the [Instructor](../../tools/frameworks/instructor.md) CLI to extract structured data from an unstructured text document:

```bash
# Extract entities from a log file using a predefined Pydantic model structure
instructor extract --model gpt-5-5-preview --schema schemas.TicketInfo --file intake_email.txt
```

Using [ripgrep](../../tools/development_ops/ripgrep.md) for simple, deterministic regular expression extraction:
```bash
# Extract all matched invoice numbers from local audit files
rg -o "INV-[0-9]{4}-[A-Z0-9]{3}" data/audit/
```

## API examples
Structured Extraction with automatic self-correction and validation logic using `instructor` (v1.x) and `pydantic` (v2.13+) in Python:

```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
from enum import Enum

# Define schema classification enums
class SupportCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "tech_support"
    GENERAL_INQUIRY = "general"

# Define validation target model using Pydantic v2
class SupportTicket(BaseModel):
    category: SupportCategory
    urgency: int = Field(
        ...,
        description="Priority of ticket from 1 (low) to 5 (critical)",
        ge=1,
        le=5
    )
    order_id: str | None = Field(
        None,
        description="The order ID if provided, matching standard format ORD-XXXXX"
    )

    # Implement custom Pydantic v2 field validator for strict format checks
    @field_validator("order_id")
    @classmethod
    def validate_order_id(cls, value: str | None) -> str | None:
        if value is not None:
            if not value.startswith("ORD-") or len(value) != 9:
                raise ValueError("Order ID must follow the pattern ORD-XXXXX with 5 digits.")
        return value

# Initialize Instructor Client with OpenAI
client = instructor.from_provider(OpenAI())

def extract_ticket_info(user_email: str) -> SupportTicket:
    # Instructor automatically handles self-correction/retries when ValueError is raised
    ticket: SupportTicket = client.chat.completions.create(
        model="gpt-5-5-preview",
        response_model=SupportTicket,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": "You are a customer service intake system. Extract ticket category, urgency and order ID."
            },
            {
                "role": "user",
                "content": user_email
            }
        ]
    )
    return ticket

# Example run
email_content = "My order ORD-12345 has not arrived yet and I was already charged!"
extracted_data = extract_ticket_info(email_content)
print(extracted_data)
# Output: category=<SupportCategory.BILLING: 'billing'> urgency=4 order_id='ORD-12345'
```

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md) — The lightweight industry standard for structured extraction.
- [PydanticAI](../../tools/frameworks/pydantic-ai.md) — Agentic framework incorporating native Pydantic validation.
- [Vercel AI SDK](../../tools/development_ops/vercel-ai-sdk.md) — Comprehensive TypeScript toolkit for streaming and structured JSON.
- [DSPy](../../tools/frameworks/dspy.md) — For optimizing and compiling extraction prompt signatures.
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) — Enterprise standard schema for task representation.
- [Date Extraction](date-extraction.md) — Specialized pattern for normalization of temporal values.
- [ServiceNow MCP](../../tools/automation_orchestration/servicenow-mcp.md) — Enterprise service integration target.
- [ripgrep](../../tools/development_ops/ripgrep.md) — High-performance regex tool for deterministic discovery.

## Sources / References
- [Instructor Documentation: Extraction and Validation](https://python.useinstructor.com/concepts/philosophy/)
- [OpenAI Guide: Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [PydanticAI Validation & Results](https://ai.pydantic.dev/results/)
- [Zod: TypeScript-First Schema Validation](https://zod.dev/)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
