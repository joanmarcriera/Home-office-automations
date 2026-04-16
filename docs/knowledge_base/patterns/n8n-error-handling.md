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
- Last reviewed: 2026-04-06
- Confidence: high
