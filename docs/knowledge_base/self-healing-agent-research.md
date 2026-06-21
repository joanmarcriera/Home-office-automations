# Self-Healing Homelab Agent Research

## What it is
A specialized monitoring and remediation agent (implemented via n8n, custom Python scripts, or **Agent Platform** managed agents) designed to detect failures in the homelab stack and take autonomous corrective actions using log-based reasoning.

## What problem it solves
- **Manual Monitoring Overhead**: Reduces the need for humans to constantly check dashboards.
- **Extended Downtime**: Shortens the "Mean Time To Recovery" (MTTR) by acting immediately.
- **Alert Fatigue**: Filters noise by only alerting humans when automated remediation (like a service restart or config rollback) fails.
- **Root Cause Analysis (RCA)**: Using LLMs to reason about log patterns rather than just reacting to status codes.

## Where it fits in the stack
**Observability / Automation Layer**. It sits "above" the services (Home Assistant, Paperless, etc.) and "beside" the infrastructure (TrueNAS, K3s), using webhooks, SSH, and the Kubernetes API to bridge the gap between detection and action.

## Typical use cases
- **Hung Web Services**: Restarting a Docker container that is technically "running" but not responding to HTTP requests.
- **Stale Sync Jobs**: Re-triggering a cloud sync or backup if the last run failed or was interrupted.
- **Hardware Warnings**: Proactively notifying the operator if a ZFS pool is degraded.
- **Log-Based Remediation**: Detecting a specific database lock pattern in logs and running a cleanup script.

## Strengths
- **Low Latency**: Responses happen in seconds, not minutes.
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

## Monitoring & Reasoning Strategy (June 2026)

### 1. Log-Based Reasoning (The "Observer" Pattern)
Instead of simple regex, the agent uses an LLM (e.g., Claude 4.8 Opus or Gemini 3.5 Flash) to analyze log chunks.
- **Method**: Forward logs via **OpenTelemetry** or specialized **Managed Agents API (MCP 3.0)**.
- **Reasoning**: "Is this 'Connection Refused' error caused by the DB being down or a bad API key?"

### 2. Service Health Checks
| Service | Endpoint / Method | Success Indicator |
| :--- | :--- | :--- |
| **Home Assistant** | `GET /api/` | `{"message": "API running."}` (Requires Token) |
| **Paperless-ngx** | `GET /` | HTTP 200 (Login page or Dashboard) |
| **n8n** | `GET /healthz` | HTTP 200 |
| **Vikunja** | `GET /api/v1/info` | HTTP 200 |

## Remediation Logic (Restart Strategies)

### Kubernetes (K3s) Rollout
Using the native K8s API for safer, zero-downtime restarts.
```bash
# Force a rollout restart of a deployment
kubectl rollout restart deployment/paperless-ngx -n apps
```

### Agentic Config Rollback
If the agent detects a failure immediately following a config change (detected via Git/Gitea webhooks), it can revert the change.
1. Detect health failure.
2. Check recent Git commits in the `homelab-ops` repo.
3. If commit < 5 mins ago, `git revert HEAD` and push.
4. Trigger redeploy.

## Technical Examples

### Agentic Recovery Loop (Python + Ollama)
This script uses a local LLM to decide whether to restart or escalate.

```python
import subprocess
import requests
import json

def get_ai_decision(error_logs):
    # Ask local LLM to reason about the log
    prompt = f"Analyze these logs and choose [RESTART, RECONFIG, ESCALATE]. Logs: {error_logs}"
    # Implementation using Ollama or LiteLLM
    # response = ...
    return "RESTART" # Simplified for example

def remediate(service_name, action):
    if action == "RESTART":
        subprocess.run(["kubectl", "rollout", "restart", f"deployment/{service_name}"])
    elif action == "ESCALATE":
        send_telegram_alert(f"Critical failure in {service_name}. Manual intervention required.")

def main():
    # Monitor loop
    # ...
    pass
```

### n8n Remediation Workflow
1. **Trigger**: Uptime Kuma Webhook (Down).
2. **Action**: Fetch last 100 lines of logs from the service.
3. **Reasoning**: AI Node (Claude 4.8 or Gemini 3.5 Flash) - "What is the likely fix?"
4. **Execution**: Execute SSH or K8s command via **MCP 3.0** based on AI output.
5. **Verification**: Wait 60s, check health again.
6. **Notification**: Send result to Telegram.

## Automated Alerts
- **High Priority**: (Hardware failure, ZFS pool issues, AI Remediation failed) -> Telegram/Pushover.
- **Medium Priority**: (Self-healing successful) -> Slack/Log entry only.

## Related tools / concepts
- [n8n Error Handling](patterns/n8n-error-handling.md) — specific patterns for building resilient workflows.
- [Agentic Workflows](patterns/agentic-workflows.md) — broader context for autonomous agent logic.
- [Invisible Kubernetes](invisible_kubernetes.md) — the infrastructure layer these agents often manage.
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — integration with the primary family assistant.
- [Gitea](../services/gitea.md) — for config rollback patterns.
- [n8n](../services/n8n.md) — automation platform for recovery workflows.
- [Uptime Kuma](../services/uptime-kuma.md) — for service monitoring and triggers.

## Implementation Roadmap (June 2026)
1. **Phase 1 (Baseline)**: Set up n8n "Health Check" loop and Telegram alerts.
2. **Phase 2 (Reactive)**: Implement SSH-based `docker restart` commands.
3. **Phase 3 (Agentic)**: Integrate Claude 4.8 or Gemini 3.5 Flash for log analysis before acting.
4. **Phase 4 (Infrastructure)**: Move to K8s `rollout restart` and Git-based config rollback with MCP 3.0 verification.

## Sources / References
- [Kubernetes Self-Healing Patterns (CNCF)](https://www.cncf.io/blog/2026/02/10/self-healing-kubernetes-agentic-patterns/)
- [Gemini 3.5 Flash for Ops (Google Cloud Blog)](https://cloud.google.com/blog/products/ai-machine-learning/gemini-flash-ops)
- [n8n AI Node Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.ai-agent/)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
