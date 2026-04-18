# n8n Error Handling Pattern

Standardized error management ensures that failed workflows are visible, logged, and actionable.

## What problem it solves
In complex automation stacks, workflows can fail due to API rate limits, network issues, or malformed data. Without standardized error handling, these failures often go unnoticed (silent failures).

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

## Implementation Guide

1. Create a global `Error Handler` workflow.
2. In your primary workflow, add the `Error Trigger` node.
3. Connect the `Error Trigger` to an `Execute Workflow` node that calls the `Error Handler`.

## Sources / References
- [n8n Error Handling Docs](https://docs.n8n.io/hosting/monitoring-n8n/error-handling/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high

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
