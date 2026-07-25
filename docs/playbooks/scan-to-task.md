# Playbook: Scan to Task

## What it is
Scan to Task is a paperless automation pattern that transforms physical documents (mail, receipts, invoices) into actionable digital tasks. It uses OCR, LLM-based extraction, and workflow orchestration to eliminate manual data entry.

## What problem it solves
Managing physical paperwork often leads to forgotten deadlines or lost information. Scan to Task digitizes the intake process, automatically identifying due dates, amounts, and required actions from scanned images or PDFs, and injecting them directly into a task management system.

## Where it fits in the stack
This playbook sits in the **Operations / Playbooks** layer. It orchestrates the flow of data between **Services** (Paperless-ngx, Nextcloud, Vikunja) and uses **Automation & Orchestration** (n8n) and **AI Models** (via Ollama or APIs) for reasoning.

## Typical use cases
- **Invoice Management**: Scanning a utility bill and automatically creating a task in Vikunja with the due date and amount.
- **Mail Triage**: Scanning incoming letters and creating tasks for items requiring a response.
- **Receipt Archival**: Scanning receipts for expense tracking, with the LLM (Claude 5.1 Vision) extracting the vendor and total.
- **Warranty Tracking**: Scanning product manuals or receipts to create a reminder for warranty expiration.

## Strengths
- **Automation**: Reduces the friction of moving from physical paper to a digital action list.
- **Searchability**: Documents are indexed and searchable in Paperless-ngx, linked directly from the task.
- **Accuracy**: LLMs can extract structured data from diverse document layouts better than traditional regex-based systems.
- **Vision Mastery**: Claude 5.1's improved vision capabilities allow for high-accuracy extraction from crumpled or low-contrast scans.

## Limitations
- **OCR Quality**: Success depends on the clarity of the original scan; handwritten or low-contrast text may fail (mitigated by using Claude 5.1 Vision).
- **Privacy**: If using cloud-based LLMs, sensitive document text is sent to an external provider (mitigated by using local models).
- **Setup Complexity**: Requires multiple services (Paperless, n8n, Vikunja) to be correctly configured and integrated.

## When to use it
- When you have a significant volume of physical documents that require action.
- When you want to maintain a centralized, searchable archive of all paperwork alongside your task list.
- When you want to leverage AI to automate the "understanding" phase of document management.

## When not to use it
- For very high-security documents that should never be digitized or processed by an LLM.
- If you only have one or two documents a month; manual entry is simpler in that case.

## Getting started

### Pre-requisites
- [Paperless-ngx](../services/paperless-ngx.md) for document storage and OCR.
- [Vikunja](../services/vikunja.md) or another task manager with an API.
- [n8n](../services/n8n.md) for workflow orchestration.
- A local or remote LLM (e.g., [Ollama](../services/ollama.md) running `Llama 4` or Claude 5.1 via API).

### Workflow Architecture (August 2026 Update)

```mermaid
flowchart TD
    A[Physical Document] -->|Scan| B(Nextcloud/Scans)
    B -->|Syncthing| C(Paperless-ngx Consumption)
    C -->|OCR & Classification| D{Action Required?}
    D -- Yes --> E[n8n Webhook Trigger]
    D -- No --> F[Archive]
    E -->|Extraction| G[LLM Processing: Claude 5.1 Vision]
    G -->|Create Task| H[Vikunja Task]
    H -->|Link Back| C
```

## CLI examples

### Triggering a Manual Scan Consumption
Force Paperless-ngx to check the consumption directory for new documents.
```bash
# Using the Paperless-ngx management command
docker exec paperless_app python3 manage.py document_consumer
```

### Checking n8n Execution Logs
Searching for failed document extraction workflows.
```bash
# Querying n8n's SQLite database for failed executions
sqlite3 ~/.n8n/database.sqlite "SELECT id, workflowId, finished, data FROM execution_entity WHERE finished = 0 AND workflowId = 'extract-task-v2' LIMIT 5;"
```

## API examples

### Fetching Document Metadata from Paperless-ngx
An agent using the Paperless API to retrieve OCR text for processing.
```python
import requests

def get_document_text(doc_id, api_token):
    url = f"http://paperless.local/api/documents/{doc_id}/"
    headers = {"Authorization": f"Token {api_token}"}
    response = requests.get(url, headers=headers)
    return response.json().get('content')

# Example usage
ocr_text = get_document_text(402, "your_api_token")
print(f"Extracted OCR Text: {ocr_text[:100]}...")
```

### Creating a Task in Vikunja via n8n and MCP 3.1 payload
Defining the JSON payload sent from n8n to Vikunja to create a linked task, incorporating MCP 3.1 Task Protocol fields.
```json
{
  "title": "Pay Utility Bill - $145.20",
  "description": "Extracted from Paperless Doc #402. Due: 2026-09-15. [View Document](http://paperless.local/documents/402)",
  "due_date": "2026-09-15T23:59:59Z",
  "priority": 3,
  "labels": ["finance", "automated"],
  "mcp_context": {
    "task_id": "mcp-scan-to-task-402",
    "mcp_version": "3.1",
    "schema": "https://modelcontextprotocol.org/schemas/3.1/task-protocol.json"
  }
}
```

## Related tools / concepts
- [Paperless-ngx](../services/paperless-ngx.md) — The core document management system.
- [Vikunja](../services/vikunja.md) — The target task management system.
- [n8n](../services/n8n.md) — The workflow engine connecting the components.
- [Ollama](../services/ollama.md) — For running local LLMs for private document extraction.
- [Syncthing](../services/syncthing.md) — For moving files between the scanner, cloud, and Paperless.
- [Nextcloud](../services/nextcloud.md) — Often used as the initial landing zone for mobile scans.
- [OCRmyPDF](../tools/process_understanding/ocrmypdf.md) — The underlying technology for document OCR.
- [Extraction and Classification Prompt](../reference-implementations/llm-prompts/extraction-and-classification.md) — The specific prompt used to guide the LLM.

## Sources / References
- [Paperless-ngx Documentation](https://docs.paperless-ngx.com/)
- [Model Context Protocol Task Protocol v3.1](https://modelcontextprotocol.org/spec)
- https://github.com/joanmarcriera/Home-office-automations

## Contribution Metadata
- Last reviewed: 2026-08-20
- Confidence: high
