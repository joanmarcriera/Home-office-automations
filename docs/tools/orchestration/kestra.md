# Kestra

## What it is
Kestra is an open-source orchestration platform for declarative, scheduled, event-driven, and business-critical workflows. It uses YAML-defined flows, a web UI, and a powerful plugin architecture. As of May 2026, **v0.18.x** is the current stable release, featuring enhanced **Flow Loops**, first-class **Python Script** support, and advanced **State Management**.

## What problem it solves
Kestra bridges the gap between infrastructure automation and data orchestration. It allows engineering teams to define complex workflows as simple YAML files, providing a unified control plane for scripts (Python, Node.js, Shell), data tools (dbt, SQL), and cloud services. It eliminates the "hidden" logic often found in cron jobs or custom scripts by making every execution observable and retryable.

## Where it fits in the stack
**Orchestration / Declarative Automation Platform**. It serves as the coordination layer that sits above your infrastructure (Kubernetes, Docker, Cloud) and data/AI services.

## Typical use cases
- **AI Model Retraining**: Triggering a training pipeline when new data arrives in S3, followed by an evaluation and a Slack notification.
- **Infrastructure Provisioning**: Coordinating Terraform or Ansible runs with post-deployment health checks.
- **Enterprise ETL/ELT**: Moving data between internal systems and warehouses with built-in error handling and retries.
- **Human-in-the-Loop**: Workflows that pause for manual approval before proceeding to sensitive steps like production deployments.

## Strengths
- **Declarative YAML**: Everything is defined in code, making it version-controllable and easy to review.
- **Embedded Scripts**: Run Python, Node.js, or Shell scripts directly within a flow without managing external workers.
- **Event-Driven**: Native support for triggers like file arrivals, webhooks, and message queue events.
- **High Observability**: A rich UI provides real-time logs, flow visualization, and performance metrics.
- **v0.18 Features**: Simplified Flow Loops, enhanced Secrets management, and improved Git integration.

## Limitations
- **YAML Learning Curve**: While simpler than complex Python DAGs, the YAML schema for advanced plugins requires study.
- **Not for Micro-Services**: Not intended to replace low-latency service-to-service communication.
- **Plugin Dependency**: Complex logic depends on the availability and maturity of specific Kestra plugins.

## When to use it
- You want to manage your workflows as code using a declarative YAML format.
- You need a unified platform that handles both data pipelines and infrastructure tasks.
- You require high visibility and a user-friendly UI for operations and monitoring.

## When not to use it
- For ultra-low latency request/response handling (use a dedicated API framework).
- If your team strictly requires a code-only (e.g., pure Python) orchestration library without a central server.
- For simple, isolated scripts where the overhead of a platform isn't justified.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free community edition; paid Enterprise Edition for advanced security and multi-tenancy.
- **Self-hostable**: Yes

## Getting started

### Docker Compose
Run Kestra locally with a single command:

```bash
docker run --pull always -p 8080:8080 kestra/kestra:latest-full
```
Access the UI at `http://localhost:8080`.

### Hello World Flow
Create a new flow in the UI:
```yaml
id: hello_world
namespace: dev

tasks:
  - id: log
    type: io.kestra.plugin.core.log.Log
    message: Hello from Kestra 2026!

  - id: python_script
    type: io.kestra.plugin.scripts.python.Script
    script: |
      import sys
      print(f"Python version: {sys.version}")
```

## CLI examples
The `kestra` CLI allows for flow validation and deployment.

```bash
# Validate a flow locally
kestra flow validate my_flow.yaml

# Create or update a flow from the CLI
kestra flow create dev my_flow.yaml

# Execute a flow and follow the logs
kestra flow execute dev hello_world --follow

# List all flows in a namespace
kestra flow list dev
```

## API examples
Kestra provides a REST API for programmatic interaction.

```bash
# Trigger a flow via curl
curl -X POST "http://localhost:8080/api/v1/executions/dev/hello_world" \
     -H "Content-Type: application/json" \
     -d '{"parameters": {"env": "prod"}}'

# Fetch logs for a specific execution
curl -X GET "http://localhost:8080/api/v1/logs/EXECUTION_ID"
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — The Python-based alternative.
- [Dagster](dagster.md) — Asset-centric data orchestration.
- [Prefect](prefect.md) — Dynamic Python workflows.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native orchestration.
- [n8n](../../services/n8n.md) — Low-code visual automation.
- [LiteLLM](../../services/litellm.md) — For AI task integration within flows.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — For extending Kestra with agentic tools.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high

## Sources / References
- [Kestra Official Documentation](https://kestra.io/docs)
- [Kestra v0.18 Release Notes](https://kestra.io/blog/release-0-18)
- [GitHub: Kestra Core](https://github.com/kestra-io/kestra)
