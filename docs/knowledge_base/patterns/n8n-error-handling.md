# n8n Error Handling Pattern

## What it is
The n8n Error Handling Pattern is a standardized approach to managing failures within automated workflows. It utilizes dedicated "Error Trigger" nodes and centralized "Error Handler" sub-workflows to ensure that every failure is logged, visualized, and acted upon.

## What problem it solves
In complex automation stacks, workflows can fail due to API rate limits, network issues, or malformed data. Without standardized error handling, these failures often go unnoticed (silent failures). This pattern ensures visibility and provides a mechanism for automated or manual recovery.

## Where it fits in the stack
It belongs to the **Orchestration & Workflow Layer**, providing resilience for all n8n-based automation.

## Typical use cases
- **API Monitoring**: Catching and notifying when a third-party service (e.g., Google Calendar) is down.
- **Data Integrity**: Flagging when an AI extraction (e.g., via [Claude 4.8](../../tools/ai_knowledge/claude.md)) fails to meet the required schema.
- **Homelab Health**: Alerting on failed system backups or infrastructure syncs via [MCP](../../tools/automation_orchestration/mcp.md) notification servers.
- **Self-Healing**: Triggering an LLM-based reasoning loop to diagnose and fix transient errors.

## Strengths
- **Visibility**: Eliminates silent failures through centralized alerting.
- **Maintainability**: Centralizes error logic in a single sub-workflow instead of duplicating it in every workflow.
- **Extensibility**: Easily integrate new notification channels (Telegram, Gotify) without changing individual workflows.

## Limitations
- **Overhead**: Requires setting up an Error Trigger node in every production workflow.
- **Dependency**: If the Error Handler sub-workflow fails, it might create a blind spot (though n8n logs this in its execution history).

## When to use it
- In any production-grade n8n workflow where failure would disrupt business or home operations.
- When you need a centralized audit trail of all automation failures.

## When not to use it
- For temporary, experimental, or "scratchpad" workflows where failure doesn't matter.
- In extremely simple workflows that are triggered manually and monitored in real-time.

## Getting started
1.  **Create the Global Error Handler**: Create a workflow that receives error data and sends a notification.
2.  **Add Error Trigger**: In your primary workflow, add the `Error Trigger` node.
3.  **Link to Handler**: Connect the `Error Trigger` to an `Execute Workflow` node that calls your global `Error Handler`.

### Research: Error Visualization Tools
- **Home Assistant**: Best for immediate visibility and real-time alerts in the homelab.
- **Grafana**: Best for analyzing failure patterns over weeks or months.

### Standardized Error Schema
| Field | Type | Description |
| :--- | :--- | :--- |
| status | String | Always failed for errors. |
| workflow_id | String | The unique ID of the failing n8n workflow. |
| node_name | String | The specific node that triggered the error. |
| timestamp | ISO8601 | The exact time of the failure. |
| message | String | The human-readable error message. |

### Reference Implementation: Home Assistant Dashboard
```yaml
type: markdown
title: n8n Error Queue
content: >
  **Status**: {{ state_attr('sensor.n8n_error_queue', 'status') }}
  **Message**: {{ states('sensor.n8n_error_queue') }}
  **Workflow ID**: {{ state_attr('sensor.n8n_error_queue', 'workflow_id') }}
  **Failed Node**: {{ state_attr('sensor.n8n_error_queue', 'node_name') }}
  **Last Occurred**: {{ state_attr('sensor.n8n_error_queue', 'timestamp') }}
```

## CLI examples
```bash
# Export the Error Handler workflow to a JSON file
n8n export:workflow --id=5 --output=error-handler.json

# List recent failed executions for a specific workflow
n8n list:executions --workflowId=10 --status=failed
```

## API examples
```python
import requests

# Example: Fetching the last 5 failed executions from n8n API
def get_failed_executions(api_key, n8n_url):
    url = f"{n8n_url}/api/v1/executions"
    headers = {"X-N8N-API-KEY": api_key}
    params = {"status": "failed", "limit": 5}
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)
- [n8n Service](../../services/n8n.md)
- [Home Assistant](../../services/home-assistant.md)
- [Self-Healing Agent Research](../self-healing-agent-research.md)
- [Agentic Workflows](agentic-workflows.md)
- [Gotify](../../services/gotify.md)
- [Webhooks](../../tools/process_understanding/webhook.md)
- [LLM-based Log Reasoning](../../architecture/multi_agent_knowledgeops.md)

## Sources / References
- [n8n Error Handling Docs](https://docs.n8n.io/hosting/monitoring-n8n/error-handling/)
- [n8n v1.50 Release Notes](https://github.com/n8n-io/n8n/releases)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
