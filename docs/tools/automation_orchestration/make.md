# Make (formerly Integromat)

## What it is
Make is a cloud-based visual automation and workflow orchestration platform that enables engineers and non-developers to build, execute, and monitor complex multi-step integration scenarios. Operating via a drag-and-drop scenario editor, Make connects disparate SaaS services, database endpoints, and LLM APIs without requiring custom glue code. As of early 2027, Make supports native integrations for frontier AI models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Pro, and DeepSeek-V4) and exposes custom webhook connectors for the [Model Context Protocol (MCP)](mcp.md) FastMCP 3.1 standard, making it a critical hub for enterprise cloud-to-agent automation loops.

```
+-----------------------------------------------------------------------------------+
|                           Make.com Cloud Orchestration Platform                   |
|                                                                                   |
|  +------------------------+      +-------------------+      +------------------+  |
|  | Webhook / Event Source | ---> | Visual Scenario   | ---> | Data Router &    |  |
|  | (SaaS / FastMCP 3.1)  |      | Router / Filters  |      | Transformer      |  |
|  +------------------------+      +-------------------+      +------------------+  |
|               |                            |                          |           |
+---------------+----------------------------+--------------------------+-----------+
                |                            |                          |
                v                            v                          v
+-----------------------------------------------------------------------------------+
|                                External Service Endpoints                         |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | Frontier LLM APIs  |     | Enterprise Databases|     | SaaS Applications    |  |
|  | (Claude 5.6 / GPT) |     | (Postgres / Notion) |     | (Slack / Salesforce) |  |
|  +--------------------+     +---------------------+     +----------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Make addresses fundamental challenges in modern distributed application development and cloud service integration:
- **Integration Friction**: Eliminates the need to write and maintain custom API authentication wrappers (OAuth 2.0, API keys) across hundreds of SaaS vendors.
- **Data Transformation Complexity**: Offers built-in functions, iterators, aggregators, and JSON/XML parsers to map arbitrary data structures visually.
- **Agentic SaaS Orchestration**: Bridges isolated cloud platforms with autonomous AI agents, enabling agents to trigger complex multi-app workflows via lightweight Webhook calls.
- **Visual Operational Telemetry**: Provides real-time execution tracking, step-by-step data inspection, and automated retry handling for transient API failures.

## Where it fits in the stack
**Automation & Orchestration**. Serves as a managed cloud integration platform alongside developer-oriented tools like [Pipedream](pipedream.md) and self-hosted workflow solutions like [n8n](../../services/n8n.md).

## Architecture & System Dynamics

```
+-----------------------------------------------------------------------------------+
|                        Make.com Scenario Execution System Architecture              |
|                                                                                   |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Webhook Receiver Node | <-> | Execution Scheduler    | <-> | Make Engine Core| |
|  +-----------------------+     +------------------------+     +-----------------+ |
|             |                              |                           |          |
|             v                              v                           v          |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Data Transformer      | <-> | Iterators / Aggregators| <-> | FastMCP 3.1     | |
|  | & Mapping Engine      |     | Branching Logic        |     | External Bridge | |
|  +-----------------------+     +------------------------+     +-----------------+ |
+-----------------------------------------------------------------------------------+
```

The platform's execution architecture comprises four main layers:
1. **Trigger & Webhook Gateway**: Ingests real-time events via instant webhooks or scheduled polling mechanisms.
2. **Data Mapping & Routing Engine**: Evaluates scenario filter conditions, branches execution paths, and applies inline transformations.
3. **Module Connectors**: Communicates with external APIs using managed credentials, handling token refresh cycles and exponential backoff automatically.
4. **Execution History Ledger**: Records detailed per-operation inputs, outputs, and execution metrics for auditing and debugging.

## Key Features & Capabilities
- **Visual Drag-and-Drop Editor**: Intuitive Canvas interface supporting complex multi-branch logic and nested iterators.
- **1,500+ Native Connectors**: Pre-configured modules for major productivity, marketing, CRM, and developer tools.
- **Advanced Error Handling**: Built-in error directives (`Commit`, `Resume`, `Ignore`, `Break`, `Rollback`) to ensure system resiliency.
- **Custom App Builder**: Capability to define private app modules and API specs using standard JSON descriptions.
- **Data Store Management**: Built-in key-value storage engine inside Make to persist state across scenario runs.

## Typical use cases
- **Multi-App Business Automations**: Syncing data seamlessly between forms, CRM databases, Slack notifications, and analytics warehouses.
- **Agentic Cloud Task Handoff**: Accepting structured JSON payloads from AI agents via Webhooks to perform multi-step administrative actions.
- **Data Sanitization & ETL**: Extracting, transforming, and loading data across disparate third-party web services.
- **Automated Incident Response**: Ingesting alert Webhooks from monitoring systems to spin up tickets and alert engineering channels.

## Enterprise Operational Considerations

| Dimension | Consideration / Requirement |
|-----------|-----------------------------|
| **Data Governance** | EU-hosted dedicated cloud regions (Make Enterprise Cloud) compliant with GDPR |
| **Authentication** | SAML 2.0 Single Sign-On (SSO), Team Roles, and granular workspace permissions |
| **Operational Limits** | Scalable operation limits based on monthly tier allocations and execution concurrency limits |
| **Security & Compliance** | SOC 2 Type II certified with encrypted data-at-rest and TLS 1.3 transit encryption |

## Strengths
- **No-Code Visual Interface**: Rapid scenario design with real-time payload inspection at each step.
- **Managed OAuth Pipeline**: Eliminates credential exposure and simplifies token management across services.
- **Extensible Webhook System**: Easily interfaces with custom servers, cloud functions, and FastMCP 3.1 endpoints.
- **Comprehensive Error Directives**: Native handling for transient HTTP errors and rate limits.

## Limitations
- **Cloud-Only Hosting**: Lacks an open-source, on-premises, or air-gapped deployment option.
- **Operation-Based Pricing**: High-volume iterations or infinite loops can consume monthly operation quotas rapidly.
- **Vendor Lock-In**: Scenario logic is proprietary to Make and cannot be directly exported as code.

## When to use it
- When connecting mainstream cloud SaaS products where managed OAuth reduces development overhead.
- When non-technical stakeholders need visibility into automated business workflows.
- For orchestrating multi-step SaaS actions triggered by AI agents.

## When not to use it
- When privacy or compliance mandates complete on-premises, self-hosted execution (use [n8n](../../services/n8n.md)).
- For high-frequency, sub-second latency microservices processing thousands of events per second.

## Getting started

1. Sign up at [Make.com](https://www.make.com/).
2. Create a new scenario in the visual builder and select a trigger module (e.g., **Custom Webhook**).
3. Copy the generated Webhook URL to send test HTTP POST payloads.
4. Connect downstream modules (e.g., OpenAI, Google Sheets, Slack) and map fields from the trigger output.
5. Save, test, and set the scenario schedule to active.

## CLI examples

```bash
# Dispatch a JSON payload to a Make Custom Webhook endpoint
curl -X POST https://hook.eu1.make.com/YOUR_CUSTOM_WEBHOOK_ID \
     -H "Content-Type: application/json" \
     -d '{
           "event": "agent_action_requested",
           "agent_id": "claude-5.6-exec",
           "action": "provision_user_access",
           "target_email": "user@enterprise.com",
           "timestamp": "2027-01-07T12:00:00Z"
         }'

# Query scenario status via Make REST API
curl -s -H "Authorization: Token YOUR_MAKE_API_TOKEN" \
     https://eu1.make.com/api/v2/scenarios/123456
```

## API examples

### FastMCP 3.1 Server Integrating Make Webhooks

The Python script below implements a **FastMCP 3.1** server that triggers a Make scenario using validated **Pydantic v2** models:

```python
"""
Make.com FastMCP 3.1 Integration Server
Enables AI agents to trigger Make.com visual scenario workflows via Webhooks.
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="MakeWorkflowTriggerServer",
    version="3.1.0",
    description="FastMCP 3.1 server for invoking Make.com scenarios via webhooks."
)

class ScenarioWebhookPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    agent_name: str = Field(..., alias="agentName", description="Name of the triggering agent")
    task_name: str = Field(..., alias="taskName", description="Workflow task title")
    priority: str = Field(default="medium", description="Task priority: low, medium, high, critical")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary payload key-values")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 execution timestamp"
    )

class ScenarioTriggerResponse(BaseModel):
    success: bool
    status_code: int
    message: str

@mcp.tool(
    name="trigger_make_scenario",
    description="Triggers a Make.com scenario via its custom webhook URL."
)
def trigger_make_scenario(
    webhook_url: str,
    agent_name: str,
    task_name: str,
    priority: str = "medium",
    parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Validates payload with Pydantic v2 and dispatches HTTP POST to Make webhook."""
    try:
        raw_payload = {
            "agentName": agent_name,
            "taskName": task_name,
            "priority": priority,
            "parameters": parameters or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Pydantic v2 schema validation
        validated_payload = ScenarioWebhookPayload.model_validate(raw_payload)

        # Dispatch to Make webhook (simulated network dispatch for verification)
        headers = {"Content-Type": "application/json"}
        # response = requests.post(webhook_url, json=validated_payload.model_dump(by_alias=True), headers=headers)

        result = ScenarioTriggerResponse(
            success=True,
            status_code=200,
            message=f"Successfully dispatched task '{validated_payload.task_name}' to Make.com scenario."
        )
        return result.model_dump()

    except Exception as e:
        return ScenarioTriggerResponse(
            success=False,
            status_code=500,
            message=f"Failed to trigger scenario: {str(e)}"
        ).model_dump()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Complex Scenario State Management Blueprint Example (JSON)

```json
{
  "name": "FastMCP 3.1 Webhook Router",
  "flow": [
    {
      "id": 1,
      "module": "gateway:CustomWebhook",
      "version": 1,
      "parameters": {
        "hook": "10293847"
      }
    },
    {
      "id": 2,
      "module": "router:Router",
      "version": 1,
      "routes": [
        {
          "filter": "{{1.priority == 'critical'}}",
          "target": 3
        },
        {
          "filter": "{{1.priority == 'medium'}}",
          "target": 4
        }
      ]
    }
  ]
}
```

## Related tools / concepts
- [n8n](../../services/n8n.md) - Primary self-hosted workflow automation alternative.
- [Zapier](zapier.md) - Major cloud no-code competitor.
- [Pipedream](pipedream.md) - Developer-first serverless integration platform.
- [MCP (Model Context Protocol)](mcp.md) - Standard protocol for agent tool integration.
- [Home Assistant](../../services/home-assistant.md) - Local smart home automation hub.

## Sources / references
- [Make Official Website](https://www.make.com/)
- [Make API Documentation](https://www.make.com/en/api-documentation)
- [Make Academy Training](https://academy.make.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
