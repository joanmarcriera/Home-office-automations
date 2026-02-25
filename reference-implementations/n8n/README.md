# Reference Implementation: n8n Workflows

This directory contains reference workflow exports for common automations.

## 1. Email Intake to Paperless
**File**: `email-to-paperless.json` (Mocked)
**Triggers**: IMAP node.
**Actions**: Filter by attachment, POST to Paperless API.

## 2. Paperless Tag to Google Calendar
**File**: `tag-to-calendar.json` (Mocked)
**Triggers**: Webhook from Paperless.
**Actions**: Get OCR text, Send to LLM node, Create GCal event.

## How to use
1. Import the JSON into your [n8n](../../docs/services/n8n.md) instance.
2. Configure credentials for IMAP, Paperless, and Google.
3. Update the LLM model ID to your local [Ollama](../../docs/services/ollama.md) or OpenAI instance.
