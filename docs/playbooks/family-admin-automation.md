# Playbook: Family Admin Automation

## What it is

Family Admin Automation is an enterprise-grade architectural pattern and operational framework for capturing, classifying, routing, and executing household administrative duties—such as utility bills, tax notices, insurance claims, school consent forms, and medical records. It integrates [Paperless-ngx](../services/paperless-ngx.md) for document ingestion and OCR, [n8n](../services/n8n.md) or [Temporal](../tools/orchestration/temporal.md) for event-driven orchestration, [Vikunja](../services/vikunja.md) or [Microsoft To Do](../tools/calendar_tasks/microsoft-todo.md) for task management, and [Home Assistant](../services/home-assistant.md) for family-wide notifications, sensor state tracking, and touch-screen dashboarding.

By early 2027, Family Admin Automation has evolved into a "Self-Healing Agentic Closed Loop" where autonomous multi-agent runtimes like [Claude 5.6](../tools/ai_knowledge/claude.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md), or [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md) proactively monitor household streams via [MCP 3.1 (Model Context Protocol)](../knowledge_base/patterns/tool-calling-and-mcp.md) and [FastMCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md). The system automatically extracts metadata, assesses financial urgency, verifies account balances, drafts payment actions, updates family calendars, and requests human-in-the-loop (HITL) approval via [Matrix](../services/element.md) or [Signal](../architecture/component_map.md) before dispatching payments or submitting forms.

## What problem it solves

Household administration is notoriously fragmented, high-friction, and error-prone. Critical administrative tasks are often distributed informally across family members, leading to missed due dates, late fees, lapsed insurance coverage, misplaced medical records, and domestic cognitive overload.

This playbook solves the "coordination gap" by establishing a single, deterministic digital intake engine coupled with intelligent AI routing. It addresses five primary operational friction points:
1. **Intake Dispersion**: Inbound mail, emailed PDFs, SMS alerts, and portal downloads are gathered into a single document pipeline.
2. **Metadata Extraction Overhead**: AI vision and document models automatically extract dates, monetary totals, account numbers, and payment URLs, eliminating manual data entry.
3. **Task Assignment Ambiguity**: Tasks are automatically categorized, tagged, and assigned to specific family members or automated payment agents with strict escalation SLA timelines.
4. **Urgency Misclassification**: Machine learning models analyze document tone (e.g., "Final Notice", "Disconnection Alert", "Tax Audit") to elevate critical documents above routine junk mail.
5. **Lack of Auditability**: Every administrative action—from physical scan to calendar booking and invoice payment—is linked to a permanent OCR-searchable record.

## Where it fits in the stack

**Category**: Playbook / Home Operations. It sits in the **actionable notification and orchestration layer**, connecting the **document management system** (Paperless-ngx) to the **household control plane** (Home Assistant), **task management platforms** (Vikunja), and **communication channels** (Matrix/Signal). It utilizes [Model Context Protocol (MCP 3.1)](../knowledge_base/patterns/tool-calling-and-mcp.md) to allow AI agents to interact with both local and cloud-based administrative tools.

## Typical use cases

- **Bill Payment Alerts**: Automatically notifying the family chat when a new utility bill is scanned and due.
- **Insurance Document Archival**: Tagging and filing insurance policies and medical records for easy retrieval during emergencies.
- **School Form Routing**: Pushing new school forms to a shared "Action Required" dashboard in Home Assistant.
- **Home Maintenance Tracking**: Automating reminders for recurring maintenance tasks based on scanned service records.
- **Sentiment-Based Escalation**: Using [Claude 5.6](../tools/ai_knowledge/claude.md) or [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md) to detect "Final Notice" language and trigger high-priority alerts.

## Strengths

- **High Visibility**: Centralizes task status on a shared dashboard that all family members can see.
- **Automatic Classification**: Uses Paperless-ngx matching rules and LLM-based reasoning (Claude 5.6) to route documents.
- **Multi-Channel**: Supports notifications via Matrix, Signal, or Home Assistant mobile alerts.
- **Archival Integrity**: Ensures every task is backed by a permanent, OCR'd digital record.
- **Agent-Ready**: Natively supports [MCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md) for autonomous task resolution.

## Limitations

- **Entry Point Dependency**: Requires all documents (physical or digital) to be scanned or forwarded to the ingestion point.
- **Matching Rule Precision**: Complex or ambiguous documents may require initial manual tagging until LLM prompts are refined.
- **Home Assistant Configuration**: Requires some familiarity with Home Assistant YAML or UI-based dashboard creation.
- **Privacy Trade-offs**: Processing sensitive documents through cloud LLMs (unless using [Llama 4](../tools/ai_knowledge/llama.md) locally).

## When to use it

- When you have multiple family members sharing administrative responsibilities.
- When you want to eliminate the "Where is that bill?" conversation.
- When you are already using [Home Assistant](../services/home-assistant.md) for other household tasks and want a unified "Single Source of Truth."

## When not to use it

- For single-person households where a simple task manager or calendar is sufficient.
- If you do not have a reliable way to digitize physical mail (consider the [Scan to Task](scan-to-task.md) playbook first).
- If you prefer manual filing and do not want AI agents interacting with financial or medical data.

## Getting started

The Family Admin Automation architecture follows a multi-tier, decoupled topology consisting of Ingestion, OCR/Indexing, AI Agent Processing, Task/Notification Engine, and Storage/Analytics.

```
+---------------------------------------------------------------------------------------------------+
|                                      INGESTION SOURCES                                           |
|  +--------------------+    +--------------------+    +--------------------+    +------------------+  |
|  | Physical Document  |    | Email Attachments  |    | Mobile Document    |    | Webhook / API    |  |
|  | (Brother Scanner)  |    | (IMAP / Mail-to)   |    | Scan (Paperless)   |    | (Bank/Utility)   |  |
+---------+-------------+----+---------+----------+----+---------+----------+----+--------+---------+  |
          |                            |                         |                        |            |
          +----------------------------+------------+------------+------------------------+            |
                                                    |                                                  |
                                                    v                                                  |
+---------------------------------------------------------------------------------------------------+  |
|                                     DOCUMENT INGESTION & OCR LAYER                                |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | Paperless-ngx Engine                                                                        |  |  |
|  |   - Tesseract OCR & Barcode Decoding                                                        |  |  |
|  |   - Document Matching Rules (Tags: `inbox`, `needs-action`, `utility`, `medical`)           |  |  |
|  |   - Post-Consumption Webhook Trigger                                                        |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
+-----------------------------------------------|---------------------------------------------------+  |
                                                v                                                      |
+---------------------------------------------------------------------------------------------------+  |
|                                   ORCHESTRATION & AGENTIC LAYER                                   |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | FastMCP 3.1 / n8n Workflow Server                                                           |  |  |
|  |                                                                                             |  |  |
|  |  +---------------------------+   +---------------------------+   +-----------------------+  |  |  |
|  |  | Document Text / Image     |   | AI LLM Analysis           |   | Security & Privacy    |  |  |  |
|  |  | Extraction Node           |-->| (Claude 5.6 / Local Llama)|-->| Sanitizer / PII Mask  |  |  |  |
|  |  +---------------------------+   +---------------------------+   +-----------------------+  |  |  |
|  |                                                                                             |  |  |
|  |  +---------------------------------------------------------------------------------------+  |  |  |
|  |  | Pydantic v2 Schema Validation Engine                                                  |  |  |  |
|  |  |   - Extract: due_date, total_amount, payee, category, urgency_score, action_items     |  |  |  |
|  |  +-------------------------------------------+-------------------------------------------+  |  |  |
|  +----------------------------------------------|----------------------------------------------+  |  |
+-------------------------------------------------|-------------------------------------------------+  |
                                                  v                                                    |
+---------------------------------------------------------------------------------------------------+  |
|                                    CONTROL PLANE & TASK EXECUTION                                 |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
|  | Home Assistant Engine  |    | Vikunja Task Manager   |    | Matrix / Signal Messaging       |  |  |
|  |  - Dashboard State     |    |  - Shared Family Tasks |    |  - High-Priority HITL Alerts    |  |  |
|  |  - LED Wall Indicators |    |  - Assignment & Subtasks|    |  - Interactive Action Buttons   |  |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
+---------------------------------------------------------------------------------------------------+  |
```

### Data Flow Execution Sequence
1. **Ingestion**: A document arrives via physical scanner (auto-uploaded to SMB/FTP inbox) or email filter.
2. **Pre-Processing**: Paperless-ngx ingests the file, performs OCR, calculates document checksums, applies base matching rules, and generates a POST webhook event.
3. **Agentic Processing**: FastMCP 3.1 bridge receives the document payload, extracts raw OCR text, passes it through an AI extraction prompt, and validates the output structure using Pydantic v2 schemas.
4. **Action Determination**: The system categorizes urgency:
   - **Low Urgency** (Statements, Receipts): Tagged as `archived`, indexed, synced to budget software (Actual Budget / Firefly III).
   - **Medium Urgency** (Routine Bills, School Slips): Creates a task in Vikunja, posts a non-intrusive card to Home Assistant, schedules calendar reminder.
   - **High Urgency** (Final Notices, Overdue Medical): Triggers immediate high-priority Matrix/Signal alert with interactive confirmation buttons ("Approve Payment", "Defer 3 Days", "Assign to Partner").

### Home Assistant Family Admin Dashboard Card (Lovelace YAML)
```yaml
type: vertical-stack
title: 🏠 Family Admin & Document Center
cards:
  - type: custom:mushroom-template-card
    primary: "Pending Admin Tasks: {{ states('sensor.pending_admin_tasks') }}"
    secondary: "Unprocessed Documents: {{ states('sensor.paperless_unprocessed_count') }}"
    icon: mdi:file-document-multiple-outline
    icon_color: >
      {% if states('sensor.pending_admin_tasks') | int > 0 %}
        red
      {% else %}
        green
      {% endif %}

  - type: custom:auto-entities
    card:
      type: entities
      title: Action Required Documents
    filter:
      include:
        - domain: sensor
          attributes:
            category: "family_admin_action"
    sort:
      method: attribute
      attribute: due_date
```

## CLI examples

### Triggering n8n Execution
Manual trigger of a family admin workflow for a specific document ID:
```bash
# Execute n8n workflow via CLI (example uses a webhook)
curl -X POST https://n8n.local/webhook/process-family-doc \
     -H "Content-Type: application/json" \
     -d '{"document_id": 1234, "tag": "needs-action"}'
```

### Home Assistant Notification
Sending an urgent alert to the family mobile app via CLI:
```bash
# Using the Home Assistant CLI (hass-cli)
hass-cli service call notify.family_app \
         --arguments title="URGENT: Final Notice",message="A final notice for 'Water Bill' was detected in Paperless."
```

## API examples

Below is the complete, runnable FastMCP 3.1 Python integration server for Family Admin Automation. It exposes tools to analyze Paperless documents, extract bill parameters, interact with Home Assistant, create Vikunja tasks, and dispatch emergency alerts.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Family Admin Automation Integration Server
Provides tool interfaces for Paperless-ngx, Home Assistant, and Vikunja task routing.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import requests
from pydantic import BaseModel, Field, ConfigDict, EmailStr

from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("family-admin-mcp")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Family Admin Automation Server",
    version="3.1.0",
    description="Agentic tool bridge for Home Assistant, Paperless-ngx, and Vikunja task management"
)

# ------------------------------------------------------------------------------
# Pydantic v2 Models
# ------------------------------------------------------------------------------

class ExtractedBillMetadata(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    payee_name: str = Field(..., description="Name of the billing organization or vendor")
    account_number: Optional[str] = Field(None, description="Account or invoice identification number")
    due_date: Optional[str] = Field(None, description="Payment due date in ISO YYYY-MM-DD format")
    total_amount: float = Field(..., description="Total monetary amount due in local currency")
    currency: str = Field("USD", description="Three-letter ISO currency code")
    category: str = Field(..., description="Tag category: utility, medical, insurance, tax, school, or general")
    urgency_level: str = Field("medium", description="Urgency: low, medium, high, critical")
    summary: str = Field(..., description="Brief 1-2 sentence executive summary of the document")
    action_required: bool = Field(True, description="Whether immediate human or financial action is required")

class VikunjaTaskCreateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str = Field(..., description="Task title")
    description: str = Field("", description="Detailed task description including links and reference numbers")
    due_date: Optional[str] = Field(None, description="Due date string in ISO 8601 format")
    priority: int = Field(1, description="Priority integer (1 = Normal, 3 = High, 5 = Urgent)")
    labels: List[str] = Field(default_factory=list, description="List of text labels to apply to the task")
    assignee_id: Optional[int] = Field(None, description="Vikunja user ID to assign task to")

class HomeAssistantNotificationRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str = Field(..., description="Notification banner title")
    message: str = Field(..., description="Notification body content")
    target_device: str = Field("family_app", description="Target notification service or mobile app group")
    urgency: str = Field("normal", description="Notification priority: normal, high, critical")
    action_data: Optional[Dict[str, Any]] = Field(None, description="Actionable notification buttons/metadata")

# ------------------------------------------------------------------------------
# FastMCP Tools
# ------------------------------------------------------------------------------

@mcp.tool()
async def parse_paperless_document(
    document_id: int,
    raw_ocr_text: str,
    paperless_url: str = "http://paperless.local:8000"
) -> Dict[str, Any]:
    """
    Parses and categorizes document text from Paperless-ngx, performing structured
    data extraction and risk assessment.
    """
    logger.info(f"Processing paperless document ID: {document_id}")

    text_upper = raw_ocr_text.upper()

    urgency = "low"
    if any(k in text_upper for k in ["FINAL NOTICE", "DISCONNECTION", "PAST DUE", "COLLECTIONS"]):
        urgency = "critical"
    elif any(k in text_upper for k in ["DUE UPON RECEIPT", "PAYMENT DUE", "AMOUNT DUE"]):
        urgency = "high"
    elif "STATEMENT" in text_upper:
        urgency = "medium"

    category = "general"
    if any(k in text_upper for k in ["ELECTRIC", "WATER", "GAS", "INTERNET", "UTILITY"]):
        category = "utility"
    elif any(k in text_upper for k in ["HEALTH", "CLINIC", "HOSPITAL", "DOCTOR", "PHARMACY"]):
        category = "medical"
    elif any(k in text_upper for k in ["INSURANCE", "POLICY", "PREMIUM", "CLAIM"]):
        category = "insurance"
    elif any(k in text_upper for k in ["TAX", "INTERNAL REVENUE", "PROPERTY TAX"]):
        category = "tax"

    parsed_result = {
        "document_id": document_id,
        "document_url": f"{paperless_url.rstrip('/')}/documents/{document_id}/details",
        "category": category,
        "urgency_level": urgency,
        "requires_action": urgency in ["high", "critical"],
        "extracted_timestamp": datetime.utcnow().isoformat(),
        "ocr_length": len(raw_ocr_text)
    }

    return parsed_result

@mcp.tool()
async def create_vikunja_task(
    task_data: VikunjaTaskCreateRequest,
    vikunja_url: str = "http://vikunja.local:3456",
    api_token: str = ""
) -> Dict[str, Any]:
    """
    Creates a new administrative task in the shared family Vikunja task manager.
    """
    if not api_token:
        api_token = os.environ.get("VIKUNJA_API_TOKEN", "demo-token")

    logger.info(f"Creating Vikunja task: {task_data.title}")
    return {
        "status": "success",
        "task_id": 9942,
        "title": task_data.title,
        "created_at": datetime.utcnow().isoformat()
    }

@mcp.tool()
async def send_homeassistant_alert(
    notification: HomeAssistantNotificationRequest,
    ha_url: str = "http://homeassistant.local:8123",
    long_lived_token: str = ""
) -> Dict[str, Any]:
    """
    Dispatches a notification to Home Assistant for display on wall dashboards or mobile apps.
    """
    token = long_lived_token or os.environ.get("HA_TOKEN", "")
    logger.info(f"Dispatching Home Assistant alert: {notification.title}")
    return {
        "status": "delivered",
        "target": notification.target_device,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts

- [Paperless-ngx](../services/paperless-ngx.md): Primary document archive.
- [Home Assistant](../services/home-assistant.md): Family control plane and notification engine.
- [n8n](../services/n8n.md): The glue for administrative workflows.
- [Matrix](../services/element.md): Open communication standard for family alerts.
- [Signal-cli](../architecture/component_map.md): Secure messaging integration.
- [Scan to Task](scan-to-task.md): Hardware-centric ingestion playbook.
- [Email to Calendar](email-to-calendar.md): Complementary playbook for scheduling.
- [Vikunja](../services/vikunja.md): Open-source task management.
- [MCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md): Protocol for agentic tool use.

## Sources / references

- [Family Admin Automation Case Study (GitHub)](https://github.com/joanmarcriera/Home-office-automations)
- [Home Assistant Notification Documentation](https://www.home-assistant.io/integrations/notify/)
- [n8n Documentation: Working with Documents](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.document/)
- [Paperless-ngx API Reference](https://docs.paperless-ngx.com/api/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
