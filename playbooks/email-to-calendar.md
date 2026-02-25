# Playbook: Email to Calendar

## Objective
Automatically extract dates and events from incoming emails and sync them to the primary family calendar.

## Pre-requisites
- [n8n](../docs/services/n8n.md)
- [Paperless-ngx](../docs/services/paperless-ngx.md)
- [LLM (Ollama or OpenAI)](../docs/services/ollama.md)
- [Google Calendar](../docs/tools/calendar_tasks/google_calendar.md)

## Step-by-Step Flow
1.  **Ingestion**: n8n workflow triggers via IMAP on a new email in the `Automate/Intake` folder.
2.  **Storage**: n8n uploads the email body (as PDF) or any existing PDF attachments to Paperless-ngx with the tag `needs-processing`.
3.  **Extraction**: n8n calls the LLM with the [Date Extraction Prompt](../reference-implementations/llm-prompts/date-extraction.md), passing the OCR text from Paperless.
4.  **Verification**: LLM returns a structured JSON object containing `event_name`, `start_date`, `end_date`, and `location`.
5.  **Action**: n8n creates an event in Google Calendar using the data returned by the LLM.
6.  **Cleanup**: n8n updates the Paperless document tag from `needs-processing` to `synced-to-calendar`.

## Data Contract
| Field | Type | Format | Source |
| :--- | :--- | :--- | :--- |
| `event_name` | String | Plain Text | Email Subject/Body |
| `start_date` | DateTime | ISO8601 | Email Body |
| `end_date` | DateTime | ISO8601 | Email Body |
| `location` | String | Plain Text | Email Body |

## Failure Modes & Recovery
- **Extraction Failed**: LLM returns "No event found".
    - *Detection*: n8n check for null fields.
    - *Recovery*: Tag document in Paperless as `automation-failed` and send a notification to Matrix.
- **IMAP Timeout**:
    - *Detection*: n8n workflow execution error.
    - *Recovery*: Retry policy in n8n (3 retries).

## Variants
- **SaaS Only**: Replace n8n/Ollama with Zapier and ChatGPT.
- **Local Only**: Replace Google Calendar with [Radicale](../docs/services/radicale.md) via CalDAV.
