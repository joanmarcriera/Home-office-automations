# Self-Healing Homelab Agent Research

## What it is
A specialized monitoring and remediation agent (implemented via n8n or a custom Python script) designed to detect failures in the homelab stack and take autonomous corrective actions.

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

### K3s (Kubernetes) Pods
- **Command**: `kubectl rollout restart deployment/<deployment_name>`
- **n8n Implementation**: Use the "SSH" node or a dedicated K8s operator.
- **Advantage**: Kubernetes handles the rolling restart, ensuring no downtime if multiple replicas exist.

## Automated Alerts
- **High Priority**: (Hardware failure, ZFS pool issues) -> Push notification (Pushover/Telegram) + Persistent Home Assistant Dashboard Notification.
- **Medium Priority**: (Service restart successful) -> Silent log entry + Daily Briefing mention.

## Implementation Roadmap
1. **Phase 1**: Set up n8n "Health Check" workflow running every 5 minutes.
2. **Phase 2**: Configure TrueNAS Syslog to forward critical alerts via Webhook.
3. **Phase 3**: Implement SSH-based "Service Restarter" in n8n.
4. **Phase 4**: Add "Cooldown" logic to prevent restart loops.

- Last reviewed: 2026-04-09
- Confidence: high

## Sources / References
- [TrueNAS Documentation](https://www.truenas.com/docs/scale/systemsettings/advanced/managesyslogs/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
