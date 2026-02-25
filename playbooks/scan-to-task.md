# Playbook: Scan to Task

## Objective
Convert physical documents (mail, receipts) into actionable tasks in the task manager.

## Pre-requisites
- [OCRmyPDF](../docs/tools/process_understanding/ocrmypdf.md)
- [Paperless-ngx](../docs/services/paperless-ngx.md)
- [Vikunja](../docs/services/vikunja.md)
- [n8n](../docs/services/n8n.md)

## Step-by-Step Flow
1.  **Ingestion**: Physical scan via mobile app or scanner reaches the `Nextcloud/Scans` folder.
2.  **Processing**: [Syncthing](../docs/services/syncthing.md) moves the file to the Paperless consumption directory.
3.  **Understanding**: Paperless performs OCR and classifies the document. If it detects a keyword like "Invoice" or "Due", it adds the tag `action-required`.
4.  **Trigger**: n8n monitors Paperless via webhook for the `action-required` tag.
5.  **Reasoning**: n8n sends the OCR text to the LLM using the [Extraction and Classification Prompt](../reference-implementations/llm-prompts/extraction-and-classification.md).
6.  **Action**: n8n creates a task in Vikunja with a title, description, and due date.
7.  **Linking**: The Vikunja task description includes a direct link to the Paperless document.

## Data Contract
| Field | Type | Format | Notes |
| :--- | :--- | :--- | :--- |
| `task_title` | String | Plain Text | Max 100 chars |
| `due_date` | Date | YYYY-MM-DD | Optional |
| `paperless_link` | URL | String | Internal ID |

## Failure Modes & Recovery
- **OCR Failure**: Text is garbled or unreadable.
    - *Recovery*: Document is tagged `low-confidence` in Paperless; manual review required.
- **Task Duplicate**:
    - *Recovery*: n8n checks Vikunja for existing tasks with similar names/dates before creating.

## Variants
- **Manual Intake**: User manually uploads a PDF to Paperless and applies the tag.
- **Email Forward**: User forwards an email to the intake address.
