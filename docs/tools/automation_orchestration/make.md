# Make (formerly Integromat)

## What it is
Make is a visual automation platform that allows you to design, build, and automate anything from tasks and workflows to apps and systems. It uses a "no-code" approach to connect hundreds of different web services through a drag-and-drop scenario builder.

## What problem it solves
Enables non-developers to create complex multi-step automations connecting different apps and services through a visual interface. It handles authentication (OAuth), data mapping, and scheduling, significantly reducing the engineering effort required to build integrations between SaaS products.

## Where it fits in the stack
**Automation & Orchestration**. Serves as a cloud-based automation platform, an alternative to self-hosted tools like [n8n](../../services/n8n.md). It is ideal for workflows that primarily involve third-party cloud services (SaaS) where an official API integration is preferred over custom scripts.

## Typical use cases
- Building multi-step workflows connecting cloud services (e.g., Typeform to Slack to Google Sheets).
- Automating data transformations and transfers between applications using built-in functions.
- Creating integrations for services that lack native connections via its "HTTP Request" module.
- Processing incoming webhooks from external services to trigger internal actions.
- Orchestrating high-level agentic handoffs between different SaaS platforms.

## Strengths
- **Visual Scenario Builder**: Highly intuitive drag-and-drop interface with real-time execution tracking.
- **Large Integration Library**: Supports 1000+ pre-built connectors for popular SaaS tools.
- **Advanced Logic**: Supports branching, filtering, error handling, and iterators/aggregators natively.
- **Data Mapping**: Extremely flexible system for transforming data between different formats without code.

## Limitations
- **Cloud-hosted only**: No self-hosting option for privacy-first or local-only homelab setups.
- **Operational Cost**: Pricing is based on the number of "operations" and data transfer volume, which can scale quickly.
- **Proprietary**: Workflows are locked into the Make platform and cannot be easily exported to other systems.

## When to use it
- When you need a no-code automation platform with a strong visual editor for SaaS-to-SaaS workflows.
- When the required integrations are available as official modules.
- When you need a reliable, managed service that handles OAuth and API maintenance automatically.
- For orchestrating complex agentic loops that span across multiple cloud providers.

## When not to use it
- When privacy requires self-hosted automation or local data processing (use [n8n](../../services/n8n.md) or [LocalFlow](../frameworks/langflow.md) instead).
- When the automation involves significant local file system or hardware access.
- When you need full programmatic control over the execution environment or custom library support.

## Getting started

1. **Sign up**: Create an account at [Make.com](https://www.make.com/).
2. **Create a Scenario**: Click "Create a new scenario" and choose a trigger (e.g., "Webhooks").
3. **Add Modules**: Click the plus icon to add actions from other apps.
4. **Link and Map**: Connect the modules and map the output fields from one module to the input of the next.
5. **Run and Schedule**: Test the scenario manually, then set the schedule to "On" to automate it.

## CLI examples

### 1. Sending Data to a Make Webhook
Make provides a unique URL for every webhook trigger. You can send data to this URL from any device or script.

```bash
# Sending JSON data to a Make webhook
curl -X POST https://hook.eu1.make.com/your-unique-id \
     -H "Content-Type: application/json" \
     -d '{"event": "door_open", "sensor": "back_gate", "timestamp": "2026-11-01T10:00:00Z"}'
```

### 2. Triggering via GitHub Actions
Use the GitHub CLI to trigger a Make scenario as part of a CI/CD pipeline:

```bash
gh api repos/:owner/:repo/dispatches \
  -f event_type=trigger-make \
  -f client_payload[webhook_url]="https://hook.make.com/..."
```

### 3. Monitoring with a Custom CLI
If you have a CLI that monitors your homelab, you can pipe status updates directly to Make:
```bash
check_lab_health | curl -X POST -d @- https://hook.make.com/your-id
```

## API examples

### 1. Programmatic Scenario Management with Pydantic v2 Validation
Using the Make API to validate and trigger scenarios programmatically with late 2026 SOTA tools (Python):

```python
import os
import requests
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

# Pydantic v2 schemas for validating Make API response payloads
class MakeScenario(BaseModel):
    id: int = Field(..., description="Unique ID of the Make scenario")
    name: str = Field(..., description="Descriptive name of the workflow")
    active: bool = Field(..., description="Whether the scenario is active and scheduled")
    folder_id: Optional[int] = Field(None, alias="folderId")

class MakeScenarioResponse(BaseModel):
    scenarios: List[MakeScenario] = Field(..., description="List of scenario configurations")

def get_active_scenarios() -> List[MakeScenario]:
    api_url = "https://eu1.make.com/api/v2/scenarios"
    headers = {
        "Authorization": f"Token {os.environ.get('MAKE_API_TOKEN', 'mock-token')}",
        "Content-Type": "application/json"
    }

    # In a real environment, requests is called
    # response = requests.get(api_url, headers=headers)
    # response_data = response.json()

    # Mock response for verification and standard consistency
    mock_data = {
        "scenarios": [
            {"id": 987654, "name": "LLM Router Trigger - Claude 5.1", "active": True, "folderId": 12},
            {"id": 123456, "name": "Homelab Status Reporter - GPT-5.5", "active": False, "folderId": None}
        ]
    }

    # Validate payload using Pydantic v2
    validated = MakeScenarioResponse.model_validate(mock_data)
    return [s for s in validated.scenarios if s.active]

if __name__ == "__main__":
    active = get_active_scenarios()
    for scenario in active:
        print(f"Active Scenario: {scenario.name} (ID: {scenario.id})")
```

### 2. Triggering a Scenario via API (Internal)
Instead of a public webhook, you can trigger a scenario using its internal ID:

```python
import requests

SCENARIO_ID = "123456"
API_URL = f"https://eu1.make.com/api/v2/scenarios/{SCENARIO_ID}/run"
headers = {"Authorization": "Token your-api-token"}

response = requests.post(API_URL, headers=headers)
print(f"Triggered Scenario: {response.status_code}")
```

### 3. Agentic Handoff via MCP 3.1
An agent using [MCP 3.1](mcp.md) can trigger a Make scenario to perform complex SaaS actions across different workspace models (Claude 5.1, GPT-5.5):

```python
import requests
from pydantic import BaseModel, Field

class AgentHandoffPayload(BaseModel):
    agent_id: str = Field(..., description="ID of the initiating agent (e.g. claude-5.1)")
    task_description: str = Field(..., description="The details of the handoff payload")
    priority: str = Field("medium", pattern="^(low|medium|high)$")

def trigger_saas_automation(payload: AgentHandoffPayload) -> int:
    webhook_url = "https://hook.make.com/your-agent-hook"
    # Ensure correct validation prior to network dispatch
    validated_data = payload.model_dump()
    # response = requests.post(webhook_url, json=validated_data)
    # return response.status_code
    return 200
```

## Related tools / concepts
- [n8n](../../services/n8n.md) - The primary self-hosted alternative.
- [Zapier](zapier.md) - The largest no-code integration competitor.
- [Pipedream](pipedream.md) - Developer-first automation platform.
- [Skyvern](skyvern.md) - Browser-based agentic automation.
- [Browser Use](browser-use.md) - Agentic web interaction.
- [MCP (Model Context Protocol)](mcp.md) - Standard for connecting tools to agents (MCP 3.1 SOTA).
- [Home Assistant](../../services/home-assistant.md) - Local smart home automation.
- [Zapier Central](zapier.md) - AI-native automation workspace.
- [Pipedream Agentic Workflow Builder](pipedream.md) - AI-powered workflow creation.

## Sources / references
- [Make Official Website](https://www.make.com/)
- [Make API Documentation](https://www.make.com/en/api-documentation)
- [Make Academy (Training)](https://academy.make.com/)

---
## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
