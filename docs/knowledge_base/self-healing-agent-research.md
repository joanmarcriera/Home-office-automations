# Self-Healing Homelab Agent Research

## What it is
A specialized monitoring and remediation agent (implemented via n8n or a custom Python script) designed to detect failures in the homelab stack and take autonomous corrective actions.

## What problem it solves

- **Manual Monitoring Overhead**: Reduces the need for humans to constantly check dashboards for service health.
- **Extended Downtime**: Shortens the "Mean Time To Recovery" (MTTR) by acting immediately when a failure is detected.
- **Alert Fatigue**: Filters noise by only alerting humans when automated remediation (like a service restart) fails.

## Where it fits in the stack

**Observability / Automation Layer**. It sits "above" the services (Home Assistant, Paperless, etc.) and "beside" the infrastructure (TrueNAS, K3s), using webhooks and SSH to bridge the gap between detection and action.

## Typical use cases

- **Hung Web Services**: Restarting a Docker container that is technically "running" but not responding to HTTP requests.
- **Stale Sync Jobs**: Re-triggering a cloud sync or backup if the last run failed or was interrupted.
- **Hardware Warnings**: Proactively notifying the operator if a ZFS pool is degraded before it leads to data loss.

## Strengths

- **Low Latency**: Responses happen in seconds, not minutes or hours.
- **Customizable**: Logic can be as simple as a restart or as complex as a multi-step failover.
- **Traceability**: Every action is logged, providing a clear history of system stability.

## Limitations

- **Risk of Infinite Loops**: A service failing due to a configuration error will continue to restart unless "cooldown" or "max attempt" logic is implemented.
- **Complexity**: Designing safe remediation for stateful services (like databases) requires significant care.
- **Dependency**: The self-healing agent itself becomes a single point of failure.

## When to use it

- For **non-critical stateful services** where a restart is the common fix.
- When you have a **stable set of health checks** that accurately reflect service usability.
- In **distributed homelabs** where the operator is not always available.

## When not to use it

- **Critical Data Integrity**: Do not automate remediation for services where a restart during a write operation could cause corruption.
- **Configuration Loops**: If the root cause is a bad update or config file, a restart won't help and may mask the issue.

## Monitoring Strategy

### 1. Log Streaming (TrueNAS SCALE)
- **Method**: Remote Syslog.
- **Implementation**: Configure TrueNAS SCALE under **System Settings > Advanced > Syslog** to send logs to a centralized collector (e.g., Vector, Fluentbit, or directly to an n8n webhook listener if using UDP/TCP to HTTP gateway).
- **Triggers**: Scan for "Hardware Error", "ZFS Pool Degraded", "OOM Kill", or "Service Failed" strings.

### 2. Service Health Checks
| Service | Endpoint / Method | Success Indicator |
| :--- | :--- | :--- |
| **Home Assistant** | `GET /api/` | `{"message": "API running."}` (Requires Token) |
| **Paperless-ngx** | `GET /` | HTTP 200 (Login page or Dashboard) |
| **n8n** | `GET /healthz` | HTTP 200 |
| **Vikunja** | `GET /api/v1/info` | HTTP 200 |

## Remediation Logic (Restart Strategies)

### Docker-based Services
- **Command**: `docker restart <container_name>`
- **n8n Implementation**: Use the "SSH" node to execute the command on the target host.
- **Safety**: Maximum 3 restart attempts within 1 hour. If it continues failing, escalate to "Alert".

```bash
# Manual remediation via SSH
ssh user@homelab-host "docker restart paperless-ngx"
```

### K3s (Kubernetes) Pods
- **Command**: `kubectl rollout restart deployment/<deployment_name>`
- **n8n Implementation**: Use the "SSH" node or a dedicated K8s operator.
- **Advantage**: Kubernetes handles the rolling restart, ensuring no downtime if multiple replicas exist.

```bash
# Kubernetes rollout restart
kubectl rollout restart deployment/home-assistant -n default
```

## Technical Examples

### Python Remediation Script (Self-Healing)
This script can be run as a cron job or a background service to monitor a local Docker container and restart it if the health check fails.

```python
import subprocess
import requests
import time

SERVICE_URL = "http://localhost:8000/healthz"
CONTAINER_NAME = "paperless-ngx"
MAX_RETRIES = 3

def check_health():
    try:
        response = requests.get(SERVICE_URL, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def restart_container():
    print(f"Restarting {CONTAINER_NAME}...")
    subprocess.run(["docker", "restart", CONTAINER_NAME], check=True)

def main():
    retries = 0
    while retries < MAX_RETRIES:
        if check_health():
            print(f"{CONTAINER_NAME} is healthy.")
            break
        else:
            print(f"{CONTAINER_NAME} health check failed.")
            restart_container()
            retries += 1
            time.sleep(30)  # Wait for service to come up

    if retries == MAX_RETRIES:
        print(f"Failed to heal {CONTAINER_NAME} after {MAX_RETRIES} attempts. Escalating...")
        # Add notification logic here (e.g., via Telegram API)

if __name__ == "__main__":
    main()
```

### n8n Remediation Webhook (cURL)
Triggering a remediation workflow in n8n from an external monitoring system (like Uptime Kuma).

```bash
curl -X POST https://n8n.example.com/webhook/remediate \
     -H "Content-Type: application/json" \
     -d '{
       "service": "home-assistant",
       "error": "HTTP 500",
       "host": "proxmox-01"
     }'
```

## Automated Alerts
- **High Priority**: (Hardware failure, ZFS pool issues) -> Push notification (Pushover/Telegram) + Persistent Home Assistant Dashboard Notification.
- **Medium Priority**: (Service restart successful) -> Silent log entry + Daily Briefing mention.

## Related tools / concepts

- [n8n Error Handling](patterns/n8n-error-handling.md) — specific patterns for building resilient workflows.
- [Agentic Workflows](patterns/agentic-workflows.md) — broader context for autonomous agent logic.
- [Prompt Requests](patterns/prompt_requests.md) — triggering remediation via agent specifications.
- [Invisible Kubernetes](invisible_kubernetes.md) — the infrastructure layer these agents often manage.
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — how Ralph integrates with self-healing.
- [Webhook Ingestion](../reference-implementations/paperless/webhook-ingestion.md) — trigger pattern for remediation.
- [Patterns Index](patterns/index.md) — other patterns in this knowledge base.

## Implementation Roadmap
1. **Phase 1**: Set up n8n "Health Check" workflow running every 5 minutes.
2. **Phase 2**: Configure TrueNAS Syslog to forward critical alerts via Webhook.
3. **Phase 3**: Implement SSH-based "Service Restarter" in n8n.
4. **Phase 4**: Add "Cooldown" logic to prevent restart loops.

- Last reviewed: 2026-05-24
- Confidence: high

## Sources / References
- [TrueNAS Documentation](https://www.truenas.com/docs/scale/systemsettings/advanced/managesyslogs/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
