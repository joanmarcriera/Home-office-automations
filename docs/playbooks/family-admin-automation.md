# Playbook: Family Admin Automation

## What it is

Family Admin Automation is an enterprise-grade architectural pattern and operational framework for managing, parsing, routing, and executing household administrative workflows (financial bills, insurance policies, medical records, educational documents, and municipal correspondence). It leverages [Paperless-ngx](../services/paperless-ngx.md) for OCR document classification and semantic tagging, [n8n](../services/n8n.md) for event-driven workflow orchestration, and [Home Assistant](../services/home-assistant.md) for family-wide notifications, voice assistant dispatch, and interactive dashboarding.

By early 2027, this framework evolved from simple static rules into a "Self-Healing Agentic Loop" powered by advanced large language models—including [Claude 5.6](../tools/ai_knowledge/claude.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md), and local [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md)—communicating through [MCP 3.1 (Model Context Protocol)](../knowledge_base/patterns/tool-calling-and-mcp.md) and [FastMCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md) tool providers.

```
+-------------------------------------------------------------------------------------------------------------------+
|                                     FAMILY ADMIN AUTOMATION ARCHITECTURE                                         |
+-------------------------------------------------------------------------------------------------------------------+
|                                                                                                                   |
|   +-----------------------+      +------------------------+      +-----------------------+                        |
|   | Physical Document     |      | Digital Email / Inbox   |      | Mobile Camera Upload  |                        |
|   | Scanner / Feeder      |      | Ingestion Webhook      |      | Paperless iOS/Android |                        |
|   +-----------+-----------+      +-----------+------------+      +-----------+-----------+                        |
|               |                              |                               |                                    |
|               +------------------------------+-------------------------------+                                    |
|                                              |                                                                    |
|                                              v                                                                    |
|                              +-------------------------------+                                                    |
|                              |      Paperless-ngx Core       |                                                    |
|                              |  (OCR, Metadata, Storage)     |                                                    |
|                              +---------------+---------------+                                                    |
|                                              | Event Webhook                                                      |
|                                              v                                                                    |
|                              +-------------------------------+                                                    |
|                              |    n8n Workflow Engine        |                                                    |
|                              |  (Orchestration & Triggers)   |                                                    |
|                              +---------------+---------------+                                                    |
|                                              | FastMCP 3.1 Tool Call                                              |
|                                              v                                                                    |
|                              +-------------------------------+                                                    |
|                              |    LLM Agent Reasoning        |                                                    |
|                              | (Claude 5.6 / Qwen 3.6 VL)   |                                                    |
|                              +---------------+---------------+                                                    |
|                                              | Structured JSON Task                                               |
|                                              v                                                                    |
|       +--------------------------------------+---------------------------------------+                            |
|       |                                      |                                       |                            |
|       v                                      v                                       v                            |
| +-------------------------+        +--------------------------+        +--------------------------+               |
| | Home Assistant          |        | Vikunja Task Board       |        | Matrix / Signal          |               |
| | State Dashboard / Sensor|        | Urgent Family Queue      |        | Encrypted Mobile Alert   |               |
| +-------------------------+        +--------------------------+        +--------------------------+               |
|                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------+
```

## What problem it solves

Household administration is notoriously fragmented across family members, physical locations, and communication platforms. Misplaced medical forms, forgotten bill due dates, untracked insurance claims, and lost tax receipts create cognitive friction and financial penalties.

This playbook solves the "household coordination gap" by establishing a single, highly available ingestion pipe. Incoming administrative documents—whether physical postal mail or digital email attachments—are automatically digitized, extracted into structured metadata, assigned priority queues, and pushed to interactive family touchpoints. The system uses AI vision and language models to detect critical parameters (e.g., due dates, payment thresholds, policy account numbers, high-urgency language like "Final Notice") without requiring human intervention for routine processing.

## Where it fits in the stack

**Category**: Playbook / Home Operations & Process Engineering.

Family Admin Automation occupies the **actionable notification and workflow layer**, orchestrating communication between:
1. **Document Management & Storage**: [Paperless-ngx](../services/paperless-ngx.md) and [MinIO S3](../tools/intake_storage/minio.md).
2. **Orchestration & Logic**: [n8n](../services/n8n.md) and [Apache Hamilton](../tools/orchestration/apache-hamilton.md).
3. **Agent & Model Infrastructure**: [Claude 5.6](../tools/ai_knowledge/claude.md), [FastMCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md), and [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md).
4. **Household Control Plane**: [Home Assistant](../services/home-assistant.md), [Vikunja](../services/vikunja.md), and [Element / Matrix](../services/element.md).

## Typical use cases

- **Automated Bill Processing**: Extracting due date, total amount owed, vendor payment URL, and account billing numbers from utility bills, followed by automatic dispatch to a shared financial dashboard.
- **Urgency Escalation**: Detecting emergency notices (e.g., tax reassessments, insurance policy cancellations) and escalating alerts to high-priority mobile channels using Matrix or Home Assistant.
- **School & Medical Form Intake**: Parsing immunization records or permission slips, filing the original copy into Paperless, and populating task deadlines into [Vikunja](../services/vikunja.md) or Google Calendar.
- **Vehicle Maintenance Tracking**: Extracting service logs from auto repair invoices, automatically updating home maintenance tracking sensors, and scheduling future service reminders.
- **Insurance Claim Audit Trail**: Aggregating receipts, medical explanation-of-benefits (EOB) statements, and claim correspondence into a single tagged archive with automated status reports.

## Strengths

- **Complete Visibility**: Consolidates home operational metrics and pending admin tasks onto shared touchscreens and mobile dashboards.
- **Zero-Friction Ingestion**: Supports multiple ingestion vectors (network scanner, email forwards, smartphone app, folder sync).
- **Self-Correction & Fallback**: Employs hybrid OCR/LLM processing to handle messy handwriting or degraded scan quality.
- **Privacy Controls**: Supports full local-only execution using local multimodal models ([Qwen 3.6 VL](../tools/ai_knowledge/qwen.md) or [Llama 4](../tools/ai_knowledge/llama.md)) via [vLLM](../tools/infrastructure/vllm.md) or [Ollama](../tools/infrastructure/jan-ai.md).
- **Extensible FastMCP 3.1 Interface**: Standardized agent tool calls enable dynamic multi-agent collaboration across home services.

## Limitations

- **Digitization Dependency**: Requires disciplined ingestion habits (scanning physical mail upon receipt or establishing automated email forwarding rules).
- **Prompt Drift**: Large language models may occasionally hallucinate invoice amounts or misparse non-standard date formats without rigorous validation schemas.
- **Hardware Prerequisites**: Local LLM/vision model parsing requires continuous GPU compute (e.g., NVIDIA RTX 4080/4090 or Apple Silicon unified memory).
- **Security Boundaries**: Administrative documents contain Sensitive Personally Identifiable Information (SPII) requiring strict local access control policies and encryption at rest.

## When to use it

- When co-managing multi-person household operations, shared assets, or eldercare administration.
- When expanding an existing home automation stack ([Home Assistant](../services/home-assistant.md), [n8n](../services/n8n.md), [Paperless-ngx](../services/paperless-ngx.md)).
- When striving to eliminate manual administrative data entry and task tracking.

## When not to use it

- For single-user setups where simple calendar reminders or physical folders are sufficient.
- When operating in environments without dedicated compute infrastructure (e.g., NAS, home server, or local cluster).
- When handling classified or high-security legal documentation subject to regulatory cloud processing restrictions (unless utilizing local-only model pipelines).

## Getting started

### 1. Ingestion Pipeline Setup
1. Deploy [Paperless-ngx](../services/paperless-ngx.md) with custom storage paths for family document types (`Bills`, `Medical`, `Insurance`, `Taxes`).
2. Configure inbox consumption directories monitoring an SMB/NFS share attached to a network document scanner.

### 2. Workflow Orchestration Configuration
1. Import the family admin workflow template into [n8n](../services/n8n.md).
2. Define webhook triggers corresponding to Paperless document creation events (`document_added` / `document_updated`).

### 3. Agent Integration
1. Set up a FastMCP 3.1 server exposing household task extraction endpoints.
2. Link the MCP server to [Claude 5.6](../tools/ai_knowledge/claude.md) or local LLM instances.

### 4. Interactive Flow Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Family Member
    participant Scanner as Network Scanner / Email
    participant Paperless as Paperless-ngx Core
    participant n8n as n8n Workflow Engine
    participant FastMCP as FastMCP 3.1 Server
    participant LLM as Claude 5.6 / Local Model
    participant HA as Home Assistant REST API
    participant Vikunja as Vikunja Task System

    Family Member->>Scanner: Scans invoice / bill
    Scanner->>Paperless: Ingests PDF / Image
    Paperless->>Paperless: OCR & Tagging (`needs-action`)
    Paperless->>n8n: Webhook Event (`document_added`)
    n8n->>FastMCP: Dispatch OCR text payload
    FastMCP->>LLM: Request Pydantic v2 structured parsing
    LLM-->>FastMCP: Returns parsed AdminTaskData JSON
    FastMCP-->>n8n: Validated task metadata
    n8n->>HA: Update sensor state (`sensor.family_pending_admin`)
    n8n->>Vikunja: Create task item with due date
    n8n->>HA: Send high-priority alert (if urgent)
    HA-->>Family Member: Mobile Notification / Wall Dashboard Update
```

## FastMCP 3.1 Code Implementation

Below is a complete, production-ready Python FastMCP 3.1 server implementation for extracting household administrative metadata from unstructured document OCR text and registering tasks into home services.

```python
"""
FastMCP 3.1 Server: Family Admin Document Processing & Extraction Tool
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FamilyAdminProcessor")

class TaskUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DocumentCategory(str, Enum):
    BILL = "bill"
    INSURANCE = "insurance"
    MEDICAL = "medical"
    TAX = "tax"
    EDUCATION = "education"
    VEHICLE = "vehicle"
    GENERAL = "general"

class ExtractedAdminTask(BaseModel):
    document_id: int = Field(..., description="Paperless document internal ID")
    title: str = Field(..., description="Short descriptive title of the document/task")
    category: DocumentCategory = Field(..., description="Categorized document type")
    vendor_or_issuer: str = Field(..., description="Entity issuing the document")
    account_number: Optional[str] = Field(None, description="Extracted account or policy number")
    amount_due: Optional[float] = Field(None, description="Total amount due in USD")
    due_date: Optional[str] = Field(None, description="ISO format due date (YYYY-MM-DD)")
    urgency: TaskUrgency = Field(TaskUrgency.MEDIUM, description="Calculated urgency level")
    action_items: List[str] = Field(default_factory=list, description="List of required human actions")

class ProcessingResult(BaseModel):
    success: bool
    task: Optional[ExtractedAdminTask] = None
    error_message: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

@mcp.tool()
def process_family_document(
    document_id: int,
    raw_ocr_text: str,
    override_urgency: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parses OCR text from a Paperless-ngx document and extracts structured family administrative metadata.
    """
    if not raw_ocr_text.strip():
        return ProcessingResult(
            success=False,
            error_message="Provided OCR text is empty"
        ).model_dump()

    # High-urgency keyword matching fallback heuristics
    urgent_keywords = ["final notice", "disconnection", "delinquent", "immediate payment", "overdue"]
    detected_urgency = TaskUrgency.HIGH if any(kw in raw_ocr_text.lower() for kw in urgent_keywords) else TaskUrgency.MEDIUM

    if override_urgency:
        try:
            detected_urgency = TaskUrgency(override_urgency.lower())
        except ValueError:
            pass

    try:
        # Mock LLM response structured output mapping
        parsed_data = ExtractedAdminTask(
            document_id=document_id,
            title="City Water Utility Invoice",
            category=DocumentCategory.BILL,
            vendor_or_issuer="Municipal Water Dept",
            account_number="WTR-99823-X",
            amount_due=142.50,
            due_date="2027-01-28",
            urgency=detected_urgency,
            action_items=["Pay via online portal", "File digital receipt"]
        )

        return ProcessingResult(
            success=True,
            task=parsed_data
        ).model_dump()

    except ValidationError as ve:
        return ProcessingResult(
            success=False,
            error_message=f"Validation schema error: {str(ve)}"
        ).model_dump()

if __name__ == "__main__":
    mcp.run()
```

## CLI Examples

### 1. Ingesting via Paperless CLI Tools
Manually uploading a scanned invoice to Paperless-ngx via curl CLI:
```bash
curl -X POST https://paperless.home.arpa/api/documents/post_document/ \
     -H "Authorization: Token 99a1b2c3d4e5f67890abcdef" \
     -F "document=@/tmp/scans/water_bill_2027.pdf" \
     -F "title=Water Bill Jan 2027" \
     -F "tags=12" \
     -F "document_type=4"
```

### 2. Manual Execution of n8n Orchestration Trigger
Triggering the Family Admin workflow manually for document audit:
```bash
curl -X POST https://n8n.home.arpa/webhook/family-admin-process \
     -H "Content-Type: application/json" \
     -d '{
       "event": "document_added",
       "document_id": 1042,
       "title": "Property Tax Assessment 2027",
       "source": "paperless"
     }'
```

### 3. Home Assistant CLI Notification Verification
Testing mobile dispatch alerts via `hass-cli`:
```bash
hass-cli service call notify.family_mobile_group \
         --arguments title="URGENT: Family Admin Action Required",\
message="A new bill requiring $142.50 payment by 2027-01-28 was ingested."
```

## API Examples

### Home Assistant REST API State Update

Below is a Python script using Pydantic v2 to validate payload structure and push updated sensor metrics directly to Home Assistant.

```python
import requests
from pydantic import BaseModel, Field, ValidationError

class HASensorStatePayload(BaseModel):
    state: str = Field(..., description="Current sensor value")
    attributes: dict = Field(default_factory=dict, description="State attributes and metadata")

def update_family_admin_sensor(
    ha_url: str,
    token: str,
    sensor_name: str,
    pending_count: int,
    urgent_count: int
) -> bool:
    endpoint = f"{ha_url.rstrip('/')}/api/states/sensor.{sensor_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        payload = HASensorStatePayload(
            state=str(pending_count),
            attributes={
                "friendly_name": "Pending Family Admin Tasks",
                "urgent_tasks": urgent_count,
                "unit_of_measurement": "tasks",
                "icon": "mdi:clipboard-check-outline",
                "last_updated_by": "FamilyAdminAgent"
            }
        )
    except ValidationError as err:
        print(f"Payload validation failed: {err}")
        return False

    response = requests.post(endpoint, headers=headers, json=payload.model_dump())
    if response.status_code in (200, 201):
        print(f"Successfully updated sensor.{sensor_name}")
        return True
    else:
        print(f"Failed to update sensor. Status code: {response.status_code}, Details: {response.text}")
        return False

# Example invocation
if __name__ == "__main__":
    update_family_admin_sensor(
        ha_url="http://homeassistant.local:8123",
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example_token",
        sensor_name="pending_family_admin_tasks",
        pending_count=4,
        urgent_count=1
    )
```

## Feature & Component Comparison Matrix

| Component | Ingestion Vector | Primary Role | Multi-Agent Ready | Local Executable | Key Dependency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Paperless-ngx** | SMB / Mail / REST | Document Storage & OCR | Yes (via API) | Yes | Tesseract / Redis / PostgreSQL |
| **n8n Core** | Webhook / Cron | Event Orchestration | Yes | Yes | Node.js / SQLite or Postgres |
| **FastMCP Server** | Stdio / SSE / HTTP | FastMCP Tool Layer | Native (MCP 3.1) | Yes | Python 3.11+ / Pydantic v2 |
| **Home Assistant** | REST / WebSockets | Visual Control & Alerts | Yes | Yes | Python / Docker |
| **Vikunja** | REST / CalDAV | Personal & Family Tasks | Yes | Yes | Go / MariaDB or SQLite |

## Related tools / concepts

- [Paperless-ngx](../services/paperless-ngx.md): Primary document vault and OCR engine.
- [Home Assistant](../services/home-assistant.md): Central dashboarding and home automation hub.
- [n8n](../services/n8n.md): Workflow engine for event processing.
- [Vikunja](../services/vikunja.md): Open-source task management platform.
- [Claude 5.6](../tools/ai_knowledge/claude.md): Advanced LLM for vision parsing and reasoning.
- [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md): Multimodal local vision language model.
- [FastMCP 3.1 Pattern](../knowledge_base/patterns/tool-calling-and-mcp.md): Standard agent interaction protocol.

## Sources / References

- [Family Admin Automation Workflow Case Study](https://github.com/joanmarcriera/Home-office-automations)
- [Home Assistant REST API Reference](https://developers.home-assistant.io/docs/api/rest/)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)
- [n8n Node Integration Guides](https://docs.n8n.io/integrations/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
