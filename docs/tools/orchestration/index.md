# Orchestration

Orchestration tools manage the execution flow of AI workloads, from simple linear pipelines to complex, autonomous multi-agent systems. This layer is responsible for routing, state management, error handling, and long-running process durability.

## Orchestration Patterns

- **Linear/DAG Orchestration**: Predetermined paths for data processing (e.g., standard n8n workflows). Best for predictable, high-volume tasks.
- **Agentic Orchestration**: Dynamic, loop-based execution where the LLM decides the next step (e.g., LangGraph, Multi-Agent Systems, or Ag2). Best for open-ended problem solving.
- **Durable Orchestration**: Systems that ensure long-running workflows survive restarts and failures (e.g., Temporal).
- **Declarative Orchestration**: Defining the desired state or asset rather than the specific steps (e.g., Kestra or Dagster).

## Tool Matrix

| Tool | Focus | UI | Self-hostable | Best for... |
| :--- | :--- | :---: | :---: | :--- |
| [Apache Airflow](apache-airflow.md) | Batch DAG Scheduling | 🟢 | 🟢 | Mature scheduled data and operations workflows (Airflow 3.x). |
| [Apache Hamilton](apache-hamilton.md) | Python Dataflows | 🟢 | 🟢 | Function-derived transformation DAGs inside Python systems. |
| [Argo Workflows](argo-workflows.md) | Kubernetes Workflows | 🟢 | 🟢 | Highly parallel container jobs on Kubernetes. |
| [Dagster](dagster.md) | Data Asset Orchestration | 🟢 | 🟢 | Data and AI pipelines with lineage and freshness context (v1.10+). |
| [Flyte](flyte.md) | AI/ML Workflows | 🟢 | 🟢 | Reproducible ML and AI workflows at scale (Flyte 2.x). |
| [Kestra](kestra.md) | Declarative Automation | 🟢 | 🟢 | Event-driven workflows across data, infra, and approvals (v0.22+). |
| [n8n](../../services/n8n.md) | Visual Automation | 🟢 | 🟢 | Home/Office automation with local AI nodes and MCP support. |
| [Prefect](prefect.md) | Python Workflow Engine | 🟢 | 🟢 | Python scripts moving into observable production (Prefect 3.x). |
| [Temporal](temporal.md) | Durable Workflows | 🟢 | 🟢 | Mission-critical, stateful execution and durable functions. |
| [ZenML](zenml.md) | MLOps Pipelines | 🟢 | 🟢 | Portable ML and agent pipelines across infrastructure stacks. |
| [Zapier](../automation_orchestration/zapier.md) | SaaS Integration | 🟢 | 🔴 | Rapidly connecting cloud apps via AI actions. |
| [Goose](../agents/goose.md) | Local Agentic | 🟢 | 🟢 | Terminal-friendly local agent orchestration. |
| [Multi-Agent Systems](../agents/multi-agent-systems.md) | Agent Orchestration | 🟢 | 🟢 | Multi-agent collaboration frameworks (AutoGen, CrewAI, LangGraph). |
| [Vellum](../automation_orchestration/vellum.md) | Prompt/Workflow Ops | 🟢 | 🔴 | Collaborative prompt engineering and hosting. |

## Related Tools / Concepts

- [Agent Frameworks](../frameworks/index.md)
- [Agent Protocols (MCP & ACP)](../../knowledge_base/agent_protocols.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [LiteLLM](../../services/litellm.md)
- [Temporal Durable Execution](temporal.md)

## Sources / References

- [Apache Airflow documentation](https://airflow.apache.org/docs/)
- [Argo Workflows documentation](https://argoproj.github.io/workflows/)
- [Dagster documentation](https://docs.dagster.io/)
- [Flyte documentation](https://docs.flyte.org/)
- [Prefect documentation](https://docs.prefect.io/)
- [Kestra documentation](https://kestra.io/docs)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
