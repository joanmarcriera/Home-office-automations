# Self-Healing Homelab Agent Research

## What it is
A specialized monitoring and remediation agent (implemented via n8n, custom Python scripts, or **Agent Platform** managed agents) designed to detect failures in the homelab stack and take autonomous corrective actions using log-based reasoning. As of July 2026, these agents leverage **MCP 3.0 Task Protocol** for direct infrastructure manipulation and [Gemma 3](../tools/ai_knowledge/local_llms.md) for low-latency edge reasoning.

## What problem it solves
- **Manual Monitoring Overhead**: Reduces the need for humans to constantly check dashboards.
- **Extended Downtime**: Shortens the "Mean Time To Recovery" (MTTR) by acting immediately.
- **Alert Fatigue**: Filters noise by only alerting humans when automated remediation (like a service restart or config rollback) fails.
- **Root Cause Analysis (RCA)**: Using LLMs to reason about log patterns rather than just reacting to status codes.

## Where it fits in the stack
**Observability / Automation Layer**. It sits "above" the services (Home Assistant, Paperless, etc.) and "beside" the infrastructure (TrueNAS, K3s), using webhooks, SSH, and the Kubernetes API to bridge the gap between detection and action. It utilizes **FastMCP 3.0** for real-time tool orchestration.

## Typical use cases
- **Hung Web Services**: Restarting a Docker container that is technically "running" but not responding to HTTP requests.
- **Stale Sync Jobs**: Re-triggering a cloud sync or backup if the last run failed or was interrupted.
- **Hardware Warnings**: Proactively notifying the operator if a ZFS pool is degraded.
- **Log-Based Remediation**: Detecting a specific database lock pattern in logs and running a cleanup script.

## Strengths
- **Low Latency**: Responses happen in seconds, not minutes, especially when using local models like [Gemma 3](../tools/ai_knowledge/local_llms.md).
- **Intelligent Recovery**: LLM-based reasoning can distinguish between a transient network blip and a persistent config error.
- **Traceability**: Every action is logged, providing a clear history of system stability.

## Limitations
- **Risk of Infinite Loops**: A service failing due to a configuration error will continue to restart unless "cooldown" or "max attempt" logic is implemented.
- **Complexity**: Designing safe remediation for stateful services (like databases) requires significant care.
- **Security**: SSH/Kubectl access for the agent must be tightly scoped using RBAC.

## When to use it
- For **non-critical stateful services** where a restart is the common fix.
- When you have a **stable set of health checks** and log patterns that accurately reflect service usability.
- In **distributed homelabs** where the operator is not always available.

## When not to use it
- **Critical Data Integrity**: Do not automate remediation for services where a restart during a write operation could cause corruption.
- **Infrastructure Core**: Do not automate self-healing for the networking layer (Tailscale/BGP) unless you have an out-of-band management channel.

## Getting started
Implementing a self-healing agent involves setting up monitoring triggers and connecting them to an AI-driven remediation loop.

### 1. Monitoring Setup
Configure **Uptime Kuma** or **Prometheus** to send webhooks to your agent (e.g., n8n or a custom Python script) when a service goes down.

### 2. Remediation Logic
Integrate an LLM (local [Gemma 3](../tools/ai_knowledge/local_llms.md) via [Ollama](../services/ollama.md) or cloud-based Claude 4.8) to analyze the failure and decide on an action.

## CLI examples
The agent can use CLI tools like `kubectl` or `docker` via MCP tools to execute remediation.

```bash
# Force a rollout restart of a deployment via K8s API
kubectl rollout restart deployment/paperless-ngx -n apps

# Check logs of a failing container for AI analysis
docker logs --tail 100 paperless-ngx

# Revert a configuration change in a Git-ops repo
git revert HEAD && git push origin main
```

## API examples
Remediation can be orchestrated using the MCP Python SDK to call system tools safely.

```python
# Example MCP tool call for service restart
async with McpClient(server_config) as client:
    await client.call_tool(
        "restart_service",
        {"service_name": "home-assistant", "namespace": "default"}
    )
```

## Related tools / concepts
- [n8n Error Handling](patterns/n8n-error-handling.md) — Specific patterns for building resilient workflows.
- [Agentic Workflows](patterns/agentic-workflows.md) — Broader context for autonomous agent logic.
- [Invisible Kubernetes](invisible_kubernetes.md) — The infrastructure layer these agents often manage.
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — Integration with the primary family assistant.
- [Gitea](../services/gitea.md) — For config rollback patterns.
- [n8n](../services/n8n.md) — Automation platform for recovery workflows.
- [Uptime Kuma](../services/uptime-kuma.md) — For service monitoring and triggers.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Preferred local reasoning engine for edge remediation.
- [MCP (Model Context Protocol)](../tools/automation_orchestration/mcp.md) — The protocol enabling secure tool access for agents.

## Sources / references
- [Kubernetes Self-Healing Patterns (CNCF)](https://www.cncf.io/blog/2026/02/10/self-healing-kubernetes-agentic-patterns/)
- [Gemma 3 for Ops (Google AI Blog)](https://ai.google.dev/gemma)
- [n8n AI Node Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.ai-agent/)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
