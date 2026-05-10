# n8n Error Handling Pattern

## What it is
The n8n Error Handling Pattern is a standardized approach to managing failures within automated workflows. It utilizes dedicated "Error Trigger" nodes and centralized "Error Handler" sub-workflows to ensure that every failure is logged, visualized, and acted upon.

## What problem it solves
In complex automation stacks, workflows can fail due to API rate limits, network issues, or malformed data. Without standardized error handling, these failures often go unnoticed (silent failures). This pattern ensures visibility and provides a mechanism for automated or manual recovery.

## Where it fits in the stack
It belongs to the **Orchestration & Workflow Layer**, providing resilience for all n8n-based automation.

## Typical use cases
- **API Monitoring**: Catching and notifying when a third-party service (e.g., Google Calendar) is down.
- **Data Integrity**: Flagging when an AI extraction fails to meet the required schema.
- **Homelab Health**: Alerting on failed system backups or infrastructure syncs.

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
1.  **Create the Global Error Handler**: Create a workflow that receives error data and sends a notification (e.g., via Telegram).
2.  **Add Error Trigger**: In your primary workflow, add the `Error Trigger` node.
3.  **Link to Handler**: Connect the `Error Trigger` to an `Execute Workflow` node that calls your global `Error Handler`.
4.  **Set Status**: Ensure the Error Handler updates the status in your centralized dashboard (e.g., Home Assistant).

## Core Components

### 1. Error Trigger Node
Every production workflow should include an **Error Trigger** node. This node catches any unhandled error within the workflow.

### 2. Standardized Error Sub-workflow
Instead of handling errors locally in every workflow, use an "Error Handler" sub-workflow.
- **Input**: Error details (Workflow Name, Error Message, Node Name, Timestamp).
- **Actions**:
    - Log to a centralized database or file.
    - Send a notification to a human review channel (e.g., Gotify, NTFY, or a dedicated "Failed Tasks" board).
    - Optionally, trigger a retry if the error is transient.

## Research: Error Visualization Tools

To close the visibility gap, two primary paths are recommended for visualizing n8n errors:

### 1. Home Assistant (Incident Response Focus)
- **Best for**: Immediate visibility and real-time alerts in the homelab.
- **Implementation**: n8n pushes error details to HA via the REST API or MQTT. A dedicated dashboard view (e.g., using a Markdown Card) displays the last few failed workflows.
- **Pros**: Low latency, integrated with home notifications, easy to set up.

### 2. Grafana (Analytics & Trends Focus)
- **Best for**: Analyzing failure patterns over weeks or months.
- **Implementation**: n8n logs error metadata to a database (InfluxDB or PostgreSQL). Grafana provides high-fidelity charts and heatmaps.
- **Pros**: Professional-grade analytics, handles high volume easily.


## Standardized Error Schema

To ensure consistency across the stack, the following schema must be used when passing error data to the centralized queue:

| Field | Type | Description |
| :--- | :--- | :--- |
| status | String | Always failed for errors. |
| model | String | (Optional) The LLM model being used when the failure occurred. |
| workflow_id | String | The unique ID of the failing n8n workflow. |
| node_name | String | The specific node that triggered the error. |
| timestamp | ISO8601 | The exact time of the failure. |
| message | String | The human-readable error message. |

## Reference Implementation: Home Assistant Dashboard

To visualize the error queue in Home Assistant, use a **Markdown Card** in your dashboard. This card parses the attributes of the `sensor.n8n_error_queue` created by the reference n8n workflow.

### Dashboard Card (Markdown)

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

### Manual Configuration (configuration.yaml)

If you prefer to define the sensor manually to ensure it exists before the first n8n push:

```yaml
template:
  - sensor:
      - name: "n8n Error Queue"
        unique_id: n8n_error_queue
        state: "No errors"
        attributes:
          status: "healthy"
          workflow_id: "none"
          node_name: "none"
          timestamp: "N/A"
```

## Related tools / concepts
- [n8n Service](../../services/n8n.md)
- [Home Assistant](../../services/home-assistant.md)
- [Self-Healing Agent Research](../self-healing-agent-research.md)
- [Agentic Workflows](agentic-workflows.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Gotify](../../services/gotify.md)
- [Webhooks](../../tools/process_understanding/webhook.md)

## Sources / References
- [n8n Error Handling Docs](https://docs.n8n.io/hosting/monitoring-n8n/error-handling/)

## Contribution Metadata
- Last reviewed: 2026-05-10
- Confidence: high
