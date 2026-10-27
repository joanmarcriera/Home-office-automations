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

## 3. Centralized Error Handler
**File**: `error-handler.json`
**Purpose**: A global sub-workflow to catch and route errors from other workflows to a centralized dashboard.
**Triggers**: Webhook (called by Error Trigger nodes in other workflows).
**Actions**: Pushes error metadata to Home Assistant via REST API.

## 4. Multi-Calendar Conflict Checker
**File**: `multi-calendar-conflict-checker.json`
**Purpose**: Aggregates availability from multiple Google Calendars and identifies overlapping busy slots (conflicts).
**Triggers**: Scheduled (Cron) or manual trigger.
**Actions**: Queries Free/Busy API, Identifies overlaps via Code node, Sends Telegram alert.

## 5. Voice to Vikunja
**File**: `voice-to-vikunja.json`
**Purpose**: Receives voice-to-text transcriptions via webhook (e.g., from Home Assistant Assist) and uses a local LLM to extract tasks into Vikunja.
**Triggers**: Webhook (from Home Assistant Assist).
**Actions**: LLM extraction (Ollama), Create task in Vikunja.

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

## When not to use it
- When simple cron scripts or native webhooks suffice without full visual workflow orchestration.
- When hard real-time latency (< 5ms) is strictly required between low-level message brokers.

## Getting started
Import workflow templates into n8n or run n8n CLI commands to activate references:

```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n:latest
```

## CLI examples
Manage n8n workflows and active instances directly from the terminal:

```bash
n8n export:workflow --backup --output=./workflows/
n8n import:workflow --input=./email-to-paperless.json
n8n update:workflow --id=1 --active=true
```

## API examples
Trigger n8n workflow webhooks and retrieve execution statistics programmatically:

```python
import json
import urllib.request

def trigger_n8n_webhook(webhook_url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

if __name__ == "__main__":
    res = trigger_n8n_webhook("http://localhost:5678/webhook/voice-to-vikunja", {"transcription": "Schedule dentist appointment for tomorrow at 10am"})
    print(res)
```
