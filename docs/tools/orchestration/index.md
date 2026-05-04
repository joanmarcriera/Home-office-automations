# Orchestration

Orchestration tools manage the execution flow of AI workloads, from simple linear pipelines to complex, autonomous multi-agent systems. This layer is responsible for routing, state management, error handling, and long-running process durability.

## Orchestration Patterns

- **Linear/DAG Orchestration**: Predetermined paths for data processing (e.g., standard n8n workflows). Best for predictable, high-volume tasks.
- **Agentic Orchestration**: Dynamic, loop-based execution where the LLM decides the next step (e.g., LangGraph or Agno). Best for open-ended problem solving.
- **Durable Orchestration**: Systems that ensure long-running workflows survive restarts and failures (e.g., Temporal).

## Tool Matrix

| Tool | Focus | UI | Self-hostable | Best for... |
| :--- | :--- | :---: | :---: | :--- |
| [n8n](../../services/n8n.md) | Visual Automation | 🟢 | 🟢 | Home/Office automation with local AI nodes. |
| [Temporal](temporal.md) | Durable Workflows | 🟢 | 🟢 | Mission-critical, stateful execution at scale. |
| [Zapier](../automation_orchestration/zapier.md) | SaaS Integration | 🟢 | 🔴 | Rapidly connecting cloud apps via AI actions. |
| [Goose](../automation_orchestration/goose.md) | Local Agentic | 🟢 | 🟢 | Terminal-friendly local agent orchestration. |
| [Vellum](../automation_orchestration/vellum.md) | Prompt/Workflow Ops | 🟢 | 🔴 | Collaborative prompt engineering and hosting. |

## Related Tools / Concepts

- [Agent Frameworks](../frameworks/index.md)
- [Agent Protocols (MCP & ACP)](../../knowledge_base/agent_protocols.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [LiteLLM](../../services/litellm.md)
