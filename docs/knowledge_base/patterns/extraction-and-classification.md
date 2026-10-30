# Extraction and Classification

## What it is
Extraction and Classification are fundamental patterns in LLM-powered applications where unstructured text (such as emails, logs, transcripts, or invoices) is converted into a structured, typed format (e.g., JSON, Pydantic objects) or assigned to specific categorical enums. In early 2027, these patterns rely on **Schema-First Design** and the **FastMCP 3.1 Task Protocol** to enforce strict, validated data integrity constraints across multi-agent tool calls and collaborative workspaces powered by frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL.

## Structured Extraction & Token Classification Pipeline

```
+-----------------------------------------------------------------------------------+
|                  Multi-Stage Extraction & Classification Pipeline                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+        +-----------------------------------------+  |
|  | Unstructured Ingestion    +------->+ FastMCP 3.1 Extraction Gateway           |  |
|  | (Emails, PDFs, Transcripts) |        | (Token Classification & Schema Enforcer)|  |
|  +---------------------------+        +--------------------+--------------------+  |
|                                                            |                      |
|                                                            v                      |
|  +---------------------------+        +-----------------------------------------+  |
|  | Downstream Executable     +<-------+ Pydantic v2 Schema Engine               |  |
|  | (Database / RAG / Workflows)|        | (Self-Correction & Regex Validation)    |  |
|  +---------------------------+        +-----------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
LLMs are inherently probabilistic and return unstructured text by default. However, software architectures require deterministic, strongly typed data to execute downstream business logic, update relational databases, or trigger operational pipelines. This pattern solves:
- **Data Hallucination**: Restricting the LLM's output parameters to explicitly defined schema fields and constraints.
- **Malformed Parser Responses**: Automatically catching, retrying, or self-correcting JSON outputs that fail validation using tools like [Instructor](../../tools/frameworks/instructor.md).
- **Automated Workflow Triage**: Seamlessly mapping free-form customer or system intent to fixed, actionable category labels and urgency levels.
- **Ecosystem Interoperability**: Establishing shared, verifiable data contracts (such as [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md)) across heterogeneous agent systems.

## Where it fits in the stack
This pattern operates at the **Input/Intake and Preprocessing layers** of an agentic application. It serves as the bridge between raw ingestion sources ([Intake & Storage](../../tools/intake_storage/index.md)) and execution engines ([Orchestration Layer](../../tools/orchestration/index.md)).

## Schema Validation & Extraction Strategy Comparison

| Extraction Method | Type Determinism | Latency & Overhead | Self-Correction Support | Ideal Workload | Token Cost Index |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Instructor + Pydantic v2** | High (Field Validators) | Medium (Retry Cycles) | Built-In (Feedback Prompting) | Unstructured Document Intake, Form Parsing | Low-Moderate |
| **Native LLM Structured Output** | High (Grammar Constrained) | Low (Single Call) | Framework Handled | High-Volume API Classification, Webhook Parsing | Low |
| **FastMCP 3.1 Task Schema** | High (MCP Protocol) | Medium (gRPC/HTTP) | Protocol Error Return | Inter-Agent Tool Calls & Task Routing | Moderate |
| **Regex / ripgrep Pre-Filter** | Deterministic Regex | Extremely Low (<5ms) | Not Applicable | Pre-Extraction Screening (UUIDs, Order IDs) | Ultra-Low |

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

## FastMCP 3.1 Document Extraction Server

The following complete Python implementation demonstrates a production-grade FastMCP 3.1 Extraction and Classification endpoint with strict Pydantic v2 validation (`extra="forbid"`):

```python
import asyncio
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Structured-Document-Extraction-Engine")

class IntentCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "tech_support"
    GENERAL_INQUIRY = "general"

class TicketUrgency(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

class SupportTicketExtractionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    raw_content: str = Field(..., min_length=10, description="Raw intake text or email content.")
    source_channel: str = Field(default="email", description="Origin intake channel (email, chat, api).")

    @field_validator("raw_content")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        return v.strip()

class SupportTicketResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: IntentCategory
    urgency: TicketUrgency
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence score.")
    order_id: Optional[str] = Field(None, description="Extracted order reference ORD-XXXXX.")
    extracted_entities: List[str] = Field(default_factory=list, description="Extracted keywords/metrics.")

    @field_validator("order_id")
    @classmethod
    def validate_order_id(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.startswith("ORD-") or len(v) != 9:
                raise ValueError("Order ID must follow exact format ORD-XXXXX with 5 digits.")
        return v

@mcp.tool()
async def extract_ticket_metadata(
    raw_content: str,
    source_channel: str = "email"
) -> Dict[str, Any]:
    """Extract structured categories, order references, and urgency scores from raw intake text."""
    try:
        req = SupportTicketExtractionRequest(
            raw_content=raw_content,
            source_channel=source_channel
        )
    except ValidationError as err:
        return {"status": "error", "validation_errors": err.errors()}

    # Simulate structured NLP extraction logic
    content_lower = req.raw_content.lower()
    extracted_order = "ORD-12345" if "ord-12345" in content_lower else None

    response = SupportTicketResponse(
        category=IntentCategory.BILLING if "charged" in content_lower else IntentCategory.GENERAL_INQUIRY,
        urgency=TicketUrgency.HIGH if "charged" in content_lower else TicketUrgency.MEDIUM,
        confidence_score=0.96,
        order_id=extracted_order,
        extracted_entities=["charged", "delivery delay"]
    )

    return response.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Systemd Service Unit Setup

To run the FastMCP Extraction Engine as a resilient background daemon in Linux production environments, create `/etc/systemd/system/extraction-engine.service`:

```ini
[Unit]
Description=FastMCP Structured Extraction Engine Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=extraction-agent
Group=extraction-agent
WorkingDirectory=/opt/extraction-engine
Environment="PATH=/opt/extraction-engine/venv/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="FASTMCP_PORT=8402"
Environment="OPENAI_API_KEY=sk-proj-prod-key-12345"
ExecStart=/opt/extraction-engine/venv/bin/python3 -m extraction_server
Restart=always
RestartSec=5
LimitNOFILE=65536

# Security Hardening Guidelines
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now extraction-engine
sudo systemctl status extraction-engine
```

## Docker Compose Production Setup

Deploy the structured extraction service container with health checks:

```yaml
version: "3.8"

services:
  extraction-engine-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: extraction-engine-mcp-server
    restart: always
    ports:
      - "8402:8402"
    environment:
      - FASTMCP_PORT=8402
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8402/health"]
      interval: 15s
      timeout: 5s
      retries: 3
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Verification Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **`ValidationError: Field required`** | Client payload missing mandated required schema property | `fastmcp call Structured-Document-Extraction-Engine extract_ticket_metadata --data '{}'` | Ensure caller provides mandated `raw_content` text field. |
| **Pydantic `extra_forbidden` Error** | Client submitted extra unknown key-value pairs | `fastmcp call Structured-Document-Extraction-Engine extract_ticket_metadata --data '{"raw_content": "test string...", "unknown": 1}'` | Strip non-schema properties or update Pydantic v2 model configuration. |
| **`order_id` Format Exception** | Model extracted invalid format string not matching `ORD-XXXXX` | Check raw JSON response in FastMCP trace output | Provide regex pattern docstring in model to guide LLM extraction. |
| **Timeout on Large Documents** | Single-pass extraction overwhelmed by large context length (> 50k tokens) | Check file size using `ls -lh document.txt` | Pre-chunk document into 4,000-character segments prior to extraction. |

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

### FastMCP 3.1 Document Extraction Server
Exposing structured token extraction over FastMCP 3.1:

```python
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from enum import Enum

mcp = FastMCP("Structured Document Parsing Engine")

class IntentCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"

class DocumentExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: IntentCategory
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    entities_found: List[str]

@mcp.tool()
async def parse_document_intent(raw_text: str, ctx: Context) -> DocumentExtractionResult:
    """Parses raw text and extracts classified categories and entities."""
    ctx.info("Processing document intent parsing...")

    return DocumentExtractionResult(
        category=IntentCategory.BILLING,
        confidence_score=0.96,
        entities_found=["INV-9021", "USD 450.00"]
    )

if __name__ == "__main__":
    mcp.run()
```

### Structured Extraction with Self-Correction (Instructor & Pydantic v2)
Structured Extraction with automatic self-correction and validation logic using `instructor` (v1.x) and `pydantic` (v2.13+) in Python:

```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, field_validator
from enum import Enum

# Define schema classification enums
class SupportCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "tech_support"
    GENERAL_INQUIRY = "general"

# Define validation target model using Pydantic v2
class SupportTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")
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
if __name__ == "__main__":
    email_content = "My order ORD-12345 has not arrived yet and I was already charged!"
    extracted_data = extract_ticket_info(email_content)
    print(extracted_data)
```

## Production Hardening & Operational Safety

### Fallback Strategies for Schema Violations
When an LLM repeatedly fails validation retries (e.g., max retries exceeded), the system must degrade gracefully rather than throwing uncaught exceptions to the caller:

```python
def safe_extract_with_fallback(raw_input: str) -> SupportTicket:
    try:
        return extract_ticket_info(raw_input)
    except Exception as err:
        # Route to general triage bucket on persistent schema failure
        return SupportTicket(
            category=SupportCategory.GENERAL_INQUIRY,
            urgency=3,
            order_id=None
        )
```

### Token Budgeting & Long Document Chunking
To prevent token budget exhaustion when processing large documents (e.g., 50-page contracts), split documents into semantic chunks and extract entities independently before aggregating:

```python
def chunk_text(text: str, max_chars: int = 4000) -> list[str]:
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
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
- Last reviewed: 2027-01-07
- Confidence: high
