# Self-Healing Homelab Agent Research

## What it is
A specialized monitoring and remediation architecture (implemented via n8n, custom Python scripts, or **Agent Platform** managed agents) designed to detect failures in the homelab stack and take autonomous corrective actions using log-based reasoning and frontier model orchestration (Claude 4.8, GPT-5.5).

## What problem it solves
- **Manual Monitoring Overhead**: Reduces the need for humans to constantly check dashboards.
- **Extended Downtime**: Shortens the "Mean Time To Recovery" (MTTR) by acting immediately upon failure detection.
- **Alert Fatigue**: Filters noise by only alerting humans when automated remediation (like a service restart or config rollback) fails.
- **Root Cause Analysis (RCA)**: Using LLMs to reason about log patterns rather than just reacting to status codes.

## Where it fits in the stack
**Observability / Automation Layer**. It sits "above" the services (Home Assistant, Paperless-ngx, etc.) and "beside" the infrastructure (TrueNAS, K3s), using webhooks, SSH, and the Kubernetes API to bridge the gap between detection and action.

## Typical use cases
- **Hung Web Services**: Restarting a Docker container that is technically "running" but not responding to HTTP requests.
- **Stale Sync Jobs**: Re-triggering a cloud sync or backup if the last run failed or was interrupted.
- **Hardware Warnings**: Proactively notifying the operator if a ZFS pool is degraded.
- **Log-Based Remediation**: Detecting a specific database lock pattern in logs and running a cleanup script via MCP 3.0.
- **Config Rollback**: Automatically reverting a Git-managed configuration if a service fails immediately after a push.

## Strengths
- **Low Latency**: Responses happen in seconds, not minutes.
- **Intelligent Recovery**: LLM-based reasoning (Gemini 3.5 Flash / Claude 4.8) can distinguish between a transient network blip and a persistent config error.
- **Traceability**: Every action is logged, providing a clear history of system stability.
- **Self-Healing Infrastructure**: Integrates with K3s and Docker for native service management.

## Limitations
- **Risk of Infinite Loops**: A service failing due to a configuration error will continue to restart unless "cooldown" or "max attempt" logic is implemented.
- **Complexity**: Designing safe remediation for stateful services (like databases) requires significant care to avoid corruption.
- **Security**: SSH/Kubectl access for the agent must be tightly scoped using RBAC to prevent unauthorized tool-use.

## When to use it
- For **non-critical stateful services** where a restart is the common and safe fix.
- When you have a **stable set of health checks** and log patterns that accurately reflect service usability.
- In **distributed homelabs** where the operator is not always available for manual intervention.

## When not to use it
- **Critical Data Integrity**: Do not automate remediation for services where a restart during a write operation could cause corruption.
- **Infrastructure Core**: Do not automate self-healing for the networking layer (Tailscale/BGP) unless you have an out-of-band management channel.

## Getting started (Docker/Local Setup)
To implement a self-healing loop, you typically deploy an automation platform like n8n or a custom Python agent with access to your infrastructure.

### Local Agent Setup (Python)
1. Install dependencies: `pip install requests kubernetes litellm`
2. Configure your `KUBECONFIG` and provider API keys (e.g., `ANTHROPIC_API_KEY`).
3. Deploy the monitor script to a persistent node (e.g., a management LXC or VM).

### n8n Implementation
1. Deploy n8n via Docker Compose.
2. Create a workflow triggered by an **Uptime Kuma** webhook.
3. Use the **AI Agent Node** with Claude 4.8 to analyze logs fetched via SSH or HTTP.
4. Execute remediation via the **Execute Command** node.

## CLI examples

### Kubernetes Rollout Restart
The most common remediation for K3s-managed services:
```bash
# Force a rollout restart of a deployment
kubectl rollout restart deployment/paperless-ngx -n apps
```

### Log Extraction for AI Analysis
Extracting the last 100 lines of logs to feed into an LLM for reasoning:
```bash
# Get logs from a specific container
docker logs --tail 100 paperless-webserver > /tmp/service_logs.txt
```

### Git Config Rollback
If the agent detects a failure after a deployment, it can revert the last commit:
```bash
git revert HEAD --no-edit && git push origin main
```

## API examples

### Log Analysis via LiteLLM (Python)
Using a frontier model to decide on a remediation action based on error logs.

```python
from litellm import completion

def get_remediation_action(service_logs):
    prompt = f"Analyze these logs and choose [RESTART, ROLLBACK, ESCALATE]. Logs: {service_logs}"
    response = completion(
        model="claude-3-5-sonnet", # Or gpt-4o / gemini-1.5-pro
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Example usage
action = get_remediation_action("ERROR: Database connection timed out after 30s")
print(f"Action: {action}")
```

### MCP 3.0 Tool Execution
Self-healing agents use MCP 3.0 to safely execute tools across the infrastructure.

```json
{
  "method": "tools/call",
  "params": {
    "name": "docker_restart_container",
    "arguments": {
      "container_id": "paperless-ngx"
    }
  }
}
```

## Related tools / concepts
- [n8n Error Handling](patterns/n8n-error-handling.md) — specific patterns for building resilient workflows.
- [Agentic Workflows](patterns/agentic-workflows.md) — broader context for autonomous agent logic.
- [Invisible Kubernetes](invisible_kubernetes.md) — the infrastructure layer these agents often manage.
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — integration with the primary family assistant.
- [Gitea](../services/gitea.md) — for config rollback patterns.
- [n8n](../services/n8n.md) — automation platform for recovery workflows.
- [Uptime Kuma](../services/uptime-kuma.md) — for service monitoring and triggers.
- [LiteLLM](../services/litellm.md) — for unified LLM reasoning across providers.

## Sources / references
- [Kubernetes Self-Healing Patterns (CNCF)](https://www.cncf.io/blog/2026/02/10/self-healing-kubernetes-agentic-patterns/)
- [Gemini 3.5 Flash for Ops (Google Cloud Blog)](https://cloud.google.com/blog/products/ai-machine-learning/gemini-flash-ops)
- [n8n AI Node Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.ai-agent/)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
