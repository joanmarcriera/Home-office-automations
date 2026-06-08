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
- **Receipt Archival**: Scanning receipts for expense tracking, with the LLM (Claude 4.7 Vision) extracting the vendor and total.
- **Warranty Tracking**: Scanning product manuals or receipts to create a reminder for warranty expiration.

## Strengths
- **Automation**: Reduces the friction of moving from physical paper to a digital action list.
- **Searchability**: Documents are indexed and searchable in Paperless-ngx, linked directly from the task.
- **Accuracy**: LLMs can extract structured data from diverse document layouts better than traditional regex-based systems.
- **Vision Mastery**: Claude 4.7's improved vision capabilities allow for high-accuracy extraction from crumpled or low-contrast scans.

## Limitations
- **OCR Quality**: Success depends on the clarity of the original scan; handwritten or low-contrast text may fail (mitigated by using Claude 4.7 Vision).
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
- A local or remote LLM (e.g., [Ollama](../services/ollama.md) running `Llama 4 Maverick` or Claude 4.7 via API).

### Workflow Architecture (June 2026 Update)

```mermaid
flowchart TD
    A[Physical Document] -->|Scan| B(Nextcloud/Scans)
    B -->|Syncthing| C(Paperless-ngx Consumption)
    C -->|OCR & Classification| D{Action Required?}
    D -- Yes --> E[n8n Webhook Trigger]
    D -- No --> F[Archive]
    E -->|Extraction| G[LLM Processing: Claude 4.7 Vision]
    G -->|Create Task| H[Vikunja Task]
    H -->|Link Back| C
```

### Step-by-Step Flow
1.  **Ingestion**: Physical scan via mobile app or scanner reaches the `Nextcloud/Scans` folder.
2.  **Processing**: [Syncthing](../services/syncthing.md) moves the file to the Paperless consumption directory.
3.  **Understanding**: Paperless performs OCR and classifies the document. If it detects a keyword like "Invoice" or "Due", it adds the tag `action-required`.
4.  **Trigger**: n8n monitors Paperless via webhook for the `action-required` tag.
5.  **Reasoning**: n8n sends the OCR text and/or page images to Claude 4.7 Vision using the [Extraction and Classification Prompt](../reference-implementations/llm-prompts/extraction-and-classification.md).
6.  **Action**: n8n creates a task in Vikunja with a title, description, and due date.
7.  **Linking**: The Vikunja task description includes a direct link to the Paperless document.

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
- https://github.com/joanmarcriera/Home-office-automations
- [Paperless-ngx Documentation](https://docs.paperless-ngx.com/)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
