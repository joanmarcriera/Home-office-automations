# Kestra

## What it is
Kestra is an open-source orchestration platform for declarative, scheduled, event-driven, and business-critical workflows. It uses YAML-defined flows, a web UI, plugins, and Git/Terraform-friendly operations.

## What problem it solves
Kestra gives engineering and operations teams a shared platform for running workflows that span data pipelines, infrastructure automation, approvals, scripts, APIs, and event triggers. In AI stacks, it can coordinate data refreshes, evaluation jobs, integration tasks, and human approval steps around model or agent workflows.

## Where it fits in the stack
**Orchestration / Declarative automation platform**.

## Typical use cases
- Scheduled and event-driven data pipelines.
- Infrastructure and platform automation.
- Human-in-the-loop approval workflows.
- Coordinating Python, dbt, API, and cloud-service tasks.

## Strengths
- Declarative workflow definitions are easy to version and review.
- UI support makes runs, logs, and operational status visible.
- Broad plugin approach can cover data, infrastructure, and business workflows.
- Open-source core with enterprise options.

## Limitations
- YAML authoring can be less expressive than Python for complex branching logic.
- Teams need to evaluate plugin maturity for their exact systems.
- Not a specialized AI agent framework.
- Operational model may be more platform-like than necessary for small scripts.

## When to use it
- You want a declarative orchestration layer for scheduled and event-driven operations.
- Workflows span data, infrastructure, and approval steps.
- GitOps and UI observability both matter.

## When not to use it
- You need a Python library embedded directly in application code.
- You primarily need durable long-running application workflows.
- Non-technical users need a consumer SaaS automation builder.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0 for the community edition)
- **Cost**: Free community edition; paid enterprise features available.
- **Self-hostable**: Yes

## Related tools / concepts
- [Apache Airflow](apache-airflow.md)
- [Prefect](prefect.md)
- [n8n](../../services/n8n.md)
- [Zapier](../automation_orchestration/zapier.md)

## Sources / References
- [Official website](https://kestra.io/)
- [Official documentation](https://kestra.io/docs/)
- [GitHub](https://github.com/kestra-io/kestra)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
