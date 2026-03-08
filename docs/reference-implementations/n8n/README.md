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
1. Import the JSON into your [n8n](../../services/n8n.md) instance.
2. Configure credentials for IMAP, Paperless, and Google.
3. Update the LLM model ID to your local [Ollama](../../services/ollama.md) or OpenAI instance.

## Local LLM Node Configuration
To use local models within n8n, use the **OpenAI Chat Model** node with a custom base URL.

### 1. Connection via Ollama
- **Resource**: Chat Model
- **Model**: `qwen3-coder-next:latest` (or your preferred model)
- **Base URL**: `http://<your-server-ip>:11434/v1`
- **Authentication**: None (unless configured with a proxy)

### 2. Connection via LiteLLM
[LiteLLM](../../services/litellm.md) can act as a unified gateway for multiple local models.
- **Base URL**: `http://<litellm-ip>:4000`
- **Model**: The model name as defined in your `config.yaml`

### Token-Efficiency Tip
Disable **Memory** (History) in the LLM node for one-off extraction tasks to keep the context window small and save local compute resources.
