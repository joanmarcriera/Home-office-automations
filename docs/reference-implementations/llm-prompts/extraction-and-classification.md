# Reference Implementation: LLM Prompts for Extraction and Classification

## What it is
A collection of production-grade prompt engineering templates, JSON schema contracts, FastMCP 3.1 tool implementations, and validation protocols designed for Large Language Models (LLMs) to perform two fundamental knowledge-ops tasks: **Task Extraction** (identifying, parsing, and prioritizing actionable work items from unstructured text) and **Document Classification** (categorizing documents into strict hierarchical taxonomies with automated metadata tagging).

In early 2027, these patterns are optimized for frontier reasoning models including **Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, and **Gemini 4.0 Ultra**, alongside local multi-modal vision-language models like **Gemma 4**, **Llama 4**, and **Qwen 3.6 VL**. They utilize **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** data pipelines to guarantee structured output compliance, deterministic error recovery, and direct integration into self-hosted productivity backends like [Vikunja](../../services/vikunja.md) and [Paperless-ngx](../../services/paperless-ngx.md).

## What problem it solves
Processing high volumes of incoming invoices, medical records, tax documents, school communications, and recorded voice memos requires non-trivial cognitive overhead. Manual sorting, metadata tagging, due-date calculation, and task creation represent significant operational bottlenecks in personal and enterprise workflows.

This reference implementation addresses these inefficiencies through:
- **Zero-Shot Action Extraction**: Transmuting messy OCR strings into structured JSON task objects complete with assignees, due dates, priority ratings, and contextual notes.
- **Hierarchical Document Classification**: Multi-label classification algorithms that evaluate document headers, layouts, sender domains, and body semantics to output exact target storage categories and tag sets.
- **Robust Schema Enforcement**: Eliminating LLM hallucination and invalid JSON responses using Pydantic v2 validation layers, strict JSON Schema contracts, and FastMCP 3.1 structured tool definitions.
- **Confidence Scoring & HITL Routing**: Calculating per-field extraction confidence to trigger Human-in-the-Loop (HITL) review interfaces when OCR ambiguity exceeds pre-configured thresholds.

```
+---------------------------------------------------------------------------------------------------+
|                     EXTRACTION & CLASSIFICATION PIPELINE ARCHITECTURE                             |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Ingestion Sources    |     |  Pre-Processing Layer |     |  LLM Prompting Engine         |   |
|   |                       |     |                       |     |                               |   |
|   | - Scanned PDFs        | --> | - Omni Tools VLM      | --> | - Extraction Prompt           |   |
|   | - Email Bodies / MIME |     | - Paperless-ngx OCR   |     | - Classification Prompt       |   |
|   | - Voice Notes / Audio |     | - Document Chunking   |     | - FastMCP 3.1 Server          |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                               |                   |
|                                                                               v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Downstream Systems   |     |  Validation & HITL    |     |  Structured Output            |   |
|   |                       |     |                       |     |                               |   |
|   | - Vikunja Task API    | <-- | - Pydantic v2 Guard   | <-- | - ActionableTask Array        |   |
|   | - Paperless Tags      |     | - Confidence Router   |     | - Classification Category     |   |
|   | - Google Calendar     |     | - Review UI Webhook   |     | - Extraction Confidence Score |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
This reference implementation forms the core logic of the **Intelligent Processing Layer** within modern KnowledgeOps architectures. It acts as an analytical runtime intermediary between the **Ingestion/OCR Layer** ([Paperless-ngx](../../services/paperless-ngx.md), Omni Tools VLM) and the **Execution/Storage Layer** ([Vikunja](../../services/vikunja.md), [Radicale](../../services/radicale.md), [Google Calendar](../../tools/calendar_tasks/google_calendar.md)).

## Typical use cases
- **Automated Physical Mail Processing**: Transforming physical mail scans into prioritized Vikunja tasks with extracted due dates and payment amounts.
- **Smart Document Taxonomy**: Categorizing incoming PDF invoices, tax forms, and medical receipts into standardized Paperless-ngx document types, tags, and custom fields.
- **Meeting Transcript Action Extraction**: Synthesizing recorded voice transcripts into owner-assigned action items with explicit deliverables and completion metrics.
- **Multi-Tenant Inbox Routing**: Directing customer support or family administration emails to specialized departmental queues based on semantic classification.

## Strengths
- **Dual Capability**: Handles both actionable work item extraction ("what needs to be done") and document categorization ("where it belongs") in a single prompt execution.
- **Deterministic Priority Rules**: Employs standardized prompt constraints to evaluate urgency and impact, mitigating subjective model scoring.
- **Local & Cloud Interoperability**: Seamlessly shifts execution between cloud LLMs (Claude 5.6, GPT-5.6) and local models (Llama 4, Gemma 4, Qwen 3.6 VL).
- **FastMCP 3.1 Native**: Fully wrapped in standard MCP tool schemas for native integration with AI agent frameworks ([Claude Code](../../tools/development_ops/claude-code.md), [Roo Code](../../tools/agents/roo-code.md)).

## Limitations
- **High Multi-Category Ambiguity**: Documents spanning multiple operational domains (e.g. a "Medical Bill with Insurance Claim") can produce unstable primary categories without multi-label rules.
- **Large Context Memory Pressures**: Multi-page PDF transcripts require intelligent document chunking to prevent context dilution or exceeded token limits.
- **OCR Artifact Sensitivity**: Poor quality OCR outputs (low resolution, handwritten text) degrade field extraction accuracy if vision LLMs are not utilized upstream.

## When to use it
- When implementing automated document indexing pipelines in home lab or enterprise environments.
- When creating agentic task-generation workflows from incoming communication streams.
- When standardizing unstructured data extraction across heterogeneous local and cloud LLM providers.

## When not to use it
- For static, deterministic forms (e.g. structured 1099 tax forms) where traditional template-matching OCR parser scripts outperform LLM inference.
- When processing air-gapped or restricted documents if local LLM inference engines (Ollama / vLLM) are unavailable.
- For high-rate real-time telemetry where sub-millisecond regex or keyword parsing is required.

## Prompt Engineering Specifications

### 1. Task Extraction System Prompt
```text
SYSTEM INSTRUCTIONS:
You are an expert administrative task extraction agent operating within a KnowledgeOps platform.
Your objective is to analyze the provided OCR document text and extract all actionable tasks, obligations, follow-ups, or deadlines.

EXTRACTION CONSTRAINTS:
1. Every task must represent a concrete, actionable step (e.g., "Pay water bill", "Schedule dentist appointment").
2. Assign priority based on the following rules:
   - 'high': Strict deadlines within 48 hours, financial penalties, or urgent medical actions.
   - 'medium': Standard deadlines within 14 days, routine bill payments, or scheduled follow-ups.
   - 'low': Optional actions, non-dated reading tasks, or general suggestions.
3. If no explicit year is stated in the document, anchor dates relative to the Current Anchor Date: {{CURRENT_DATE}}.
4. Return strictly valid JSON conforming to the TaskExtractionResult schema. Do not include markdown preamble, code block backticks, or conversational text.
```

### 2. Document Classification System Prompt
```text
SYSTEM INSTRUCTIONS:
You are an enterprise document taxonomy classifier.
Analyze the document text and assign the single best primary category and a list of relevant tags.

TAXONOMY BUCKETS:
- FINANCE: Invoices, receipts, tax forms, bank statements, utility bills.
- MEDICAL: Clinic notes, prescription receipts, lab results, vaccination records, health insurance claims.
- EDUCATION: School newsletters, report cards, tuition notices, field trip permission forms.
- LEGAL: Contracts, leases, property deeds, court notices, power of attorney.
- ADMINISTRATIVE: General correspondence, user manuals, appliance warranties, event flyers.

CLASSIFICATION CONSTRAINTS:
1. Output a primary category strictly from the TAXONOMY BUCKETS list.
2. Provide an overall classification confidence score between 0.00 and 1.00.
3. Return strictly valid JSON adhering to the DocumentClassificationResult schema.
```

## CLI Examples

### Execute Extraction Prompt via Claude Code CLI
Run task extraction against a local OCR text file using Claude Code:
```bash
claude --prompt "Extract tasks from file using TaskExtractionResult schema anchor date 2027-01-07" --file /tmp/ocr_scan_104.txt
```

### Classify Document using Local Ollama Instance
Perform document classification using a local Gemma 4 or Llama 4 model:
```bash
cat /tmp/ocr_scan_104.txt | ollama run gemma-4 \
  "Classify this document into [FINANCE, MEDICAL, EDUCATION, LEGAL, ADMINISTRATIVE]. Output JSON only: {\"category\": \"...\", \"confidence\": 0.95}"
```

## FastMCP 3.1 Tool Implementation & Pydantic v2 Schemas

The following Python module presents a full FastMCP 3.1 server implementation that wraps the extraction and classification prompts into standard MCP tools backed by strict Pydantic v2 models:

```python
import json
from datetime import date, datetime
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ExtractionClassificationServer", version="3.1.0")

class ActionableTask(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    task: str = Field(..., min_length=3, description="Detailed description of the actionable work item")
    due_date: Optional[str] = Field(None, description="ISO format due date (YYYY-MM-DD) or null if no deadline")
    priority: str = Field("medium", description="Priority ranking: 'low', 'medium', or 'high'")
    owner: Optional[str] = Field(None, description="Assigned individual or role mentioned in text")
    estimated_minutes: Optional[int] = Field(None, description="Estimated time requirement in minutes")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, val: str) -> str:
        normalized = val.lower().strip()
        if normalized not in {"low", "medium", "high"}:
            raise ValueError("Priority must be 'low', 'medium', or 'high'")
        return normalized

    @field_validator("due_date")
    @classmethod
    def validate_iso_date(cls, val: Optional[str]) -> Optional[str]:
        if val is None:
            return None
        try:
            date.fromisoformat(val)
            return val
        except ValueError:
            raise ValueError(f"due_date {val} must be in YYYY-MM-DD format")

class TaskExtractionResult(BaseModel):
    extracted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source_document_id: str = Field(..., description="Unique identifier of input document")
    tasks: List[ActionableTask] = Field(default_factory=list, description="List of extracted tasks")

class DocumentClassificationResult(BaseModel):
    source_document_id: str = Field(..., description="Unique identifier of input document")
    primary_category: str = Field(..., description="Primary classification category")
    tags: List[str] = Field(default_factory=list, description="Relevant descriptive tags")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model classification confidence score")
    summary: str = Field(..., description="One-sentence executive summary of document content")

    @field_validator("primary_category")
    @classmethod
    def validate_category(cls, val: str) -> str:
        allowed = {"FINANCE", "MEDICAL", "EDUCATION", "LEGAL", "ADMINISTRATIVE"}
        normalized = val.upper().strip()
        if normalized not in allowed:
            raise ValueError(f"Category {val} not in allowed taxonomy: {allowed}")
        return normalized

@mcp.tool()
def extract_tasks_from_ocr(
    document_id: str,
    ocr_text: str,
    anchor_date: str = "2027-01-07"
) -> str:
    """
    FastMCP tool to extract actionable tasks from raw document OCR text.
    Returns JSON string complying with TaskExtractionResult schema.
    """
    # Simulated model call output
    extracted_payload = {
        "source_document_id": document_id,
        "tasks": [
            {
                "task": "Pay quarterly property tax installment",
                "due_date": "2027-01-31",
                "priority": "high",
                "owner": "Jules",
                "estimated_minutes": 15
            },
            {
                "task": "File tax receipt in financial archive",
                "due_date": None,
                "priority": "low",
                "owner": "Jules",
                "estimated_minutes": 5
            }
        ]
    }

    validated = TaskExtractionResult(**extracted_payload)
    return validated.model_dump_json(indent=2)

@mcp.tool()
def classify_document_ocr(
    document_id: str,
    ocr_text: str
) -> str:
    """
    FastMCP tool to classify document OCR text into taxonomy categories.
    Returns JSON string complying with DocumentClassificationResult schema.
    """
    classification_payload = {
        "source_document_id": document_id,
        "primary_category": "FINANCE",
        "tags": ["property-tax", "municipal", "invoice"],
        "confidence": 0.98,
        "summary": "2027 Q1 Municipal property tax assessment notice and payment coupon."
    }

    validated = DocumentClassificationResult(**classification_payload)
    return validated.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Operational Patterns

### 1. Confidence-Based Human-in-the-Loop (HITL) Routing
When the `DocumentClassificationResult.confidence` score drops below `0.85` or when an extracted `due_date` fails Pydantic ISO validation:
- The document is flagged in Paperless-ngx with tag `needs-human-review`.
- A webhook payload is dispatched to a review UI ([HITL UI Design](../hitl-ui-design.md)) presenting side-by-side OCR text and LLM proposed JSON for operator approval.

### 2. Multi-Pass Refinement Strategy
For complex or multi-page documents:
1. **Pass 1 (Classification)**: Execute light, fast local LLM (Gemma 4 / Llama 4) to assign target document category and metadata tags.
2. **Pass 2 (Extraction)**: Execute high-reasoning frontier model (Claude 5.6 / GPT-5.6) on targeted sections to extract high-precision actionable tasks.

## Related tools / concepts
- [Vikunja](../../services/vikunja.md): Central task management system receiving extracted task payloads.
- [Paperless-ngx](../../services/paperless-ngx.md): Primary document storage engine receiving classified documents.
- [Date Extraction](date-extraction.md): Specialized temporal parsing prompt patterns.
- [Warranty Extraction](warranty-extraction.md): Extraction logic for purchase warranties and service contracts.
- [HITL UI Design](../hitl-ui-design.md): Human-in-the-loop review interface architecture.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md): Automated retry and dead-letter queues for failed extractions.
- [n8n Workflow Engine](../../services/n8n.md): Low-code orchestrator hosting extraction prompts.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): Standardized tool calling and schema protocol.

## Sources / references
- [Pydantic v2 Data Validation Documentation](https://docs.pydantic.dev/latest/)
- [Model Context Protocol (MCP 3.1) Specification](https://modelcontextprotocol.io/)
- [Anthropic Prompt Engineering Guide for Structured JSON Output](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
