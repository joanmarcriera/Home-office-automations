# Consolidated Services Inventory

## What it is
The Consolidated Services Inventory is a centralized registry and status dashboard for all services running in the TrueNAS SCALE home lab environment. It provides a high-level overview of the service purpose, container images, data persistence paths, and network exposure.

## What problem it solves
In a complex home lab with dozens of interconnected services (Nextcloud, Home Assistant, Ollama, etc.), it becomes difficult to track where data is stored, which images are in use, and how each service is exposed. This inventory serves as the single source of truth for administrative oversight and disaster recovery planning.

## Where it fits in the stack
**Infrastructure Management / Documentation**. It sits above the individual service configurations, providing a map of the entire self-hosted ecosystem.

| Service Name | Purpose | Image | Data Path | Exposure |
| :--- | :--- | :--- | :--- | :--- |
| **Nextcloud** | File Storage & Sync | `nextcloud:latest` | `/mnt/<pool>/applications/nextcloud/` | Reverse Proxy / LAN |
| **Paperless-ngx** | Document Management | `ghcr.io/paperless-ngx/paperless-ngx` | `/mnt/<pool>/applications/paperless-ngx/` | Reverse Proxy / LAN |
| **n8n** | Workflow Automation | `docker.n8n.io/n8nio/n8n` | `/mnt/<pool>/applications/n8n/` | Reverse Proxy / LAN |
| **Home Assistant** | Smart Home Control | `homeassistant/home-assistant` | `/mnt/<pool>/applications/home-assistant/` | Reverse Proxy / LAN |
| **Ollama** | Local LLM Runner | `ollama/ollama` | `/mnt/<pool>/applications/ollama/` | LAN / Tailscale |
| **Jellyfin** | Media Streaming | `jellyfin/jellyfin` | `/mnt/<pool>/applications/jellyfin/` | Reverse Proxy / LAN |
| **Vikunja** | Task Management | `vikunja/vikunja` | Private dataset path | Private network / reverse proxy |
| **Linkwarden** | Bookmark Manager | `ghcr.io/linkwarden/linkwarden` | `/mnt/<pool>/applications/linkwarden/` | Reverse Proxy / LAN |
| **Habitica** | Gamified Tasks | `habitica/habitica` | `/mnt/<pool>/applications/habitica/` | LAN / Tailscale |
| **Focalboard** | Project Management | `mattermost/focalboard` | `/mnt/<pool>/applications/focalboard/` | LAN / Tailscale |
| **qBittorrent** | Torrent Client | `linuxserver/qbittorrent` | `/mnt/<pool>/applications/qbittorrent/` | LAN (VPN) |
| **Jackett** | Tracker Proxy | `linuxserver/jackett` | `/mnt/<pool>/applications/jackett/` | LAN |
| **Diskover** | Disk Analysis | `diskover/diskover` | `/mnt/<pool>/applications/diskover/` | LAN |
| **Storj Node** | Decentralized Storage | `storjlabs/storagenode` | `/mnt/<pool>/applications/storj/` | WAN (Port Forward) |
| **Radicale** | CalDAV Server | `tomschroeder/radicale` | `/mnt/<pool>/applications/radicale/` | Reverse Proxy / LAN |
| **LiteLLM** | LLM Proxy | `ghcr.io/berriai/litellm` | `/mnt/<pool>/applications/litellm/` | LAN / Tailscale |
| **rclone** | Cloud Sync | `rclone/rclone` | `/mnt/<pool>/applications/rclone/` | N/A (CLI/Cron) |
| **Authentik** | IDP / SSO | `ghcr.io/goauthentik/server` | `/mnt/<pool>/applications/authentik/` | Reverse Proxy / LAN |
| **Synapse** | Matrix Server | `matrixdotorg/synapse:latest` | `/mnt/<pool>/applications/synapse/` | Reverse Proxy / LAN |

## Typical use cases
- Auditing container image versions for security updates across the stack.
- Verifying ZFS dataset paths during storage migration or backup configuration.
- Checking network exposure (Reverse Proxy vs. LAN-only) to ensure security compliance.
- Assisting AI agents (Claude 4.8 Opus, GPT-5.5) in mapping the environment for autonomous troubleshooting.

## Strengths
- **Centralized Visibility**: Consolidated view of disparate services.
- **Data Path Tracking**: Critical for ensuring all stateful data is backed up.
- **Exposure Mapping**: Helps prevent accidental exposure of private services to the WAN.
- **Consistency**: Matches standard KnowledgeOps formatting for easy parsing by automated agents.

## Limitations
- **Manual Updates**: Requires manual updates or specific automation triggers when services are added.
- **Static Content**: Does not show real-time health or performance metrics.
- **Abstraction**: Does not replace detailed individual service documentation files.

## When to use it
- When planning infrastructure changes (e.g., ZFS pool migrations or hardware upgrades).
- When performing security audits of exposed services and reverse proxy configurations.
- During disaster recovery to quickly find the data path or image of a specific service.

## When not to use it
- For real-time monitoring (use Prometheus/Grafana or Dashworks for that).
- For detailed configuration parameters or environment variable lists (refer to individual service `.md` files).
- For sensitive secret management (refer to Vault or TrueNAS Secrets).

## Getting started

### Registering a New Service
To maintain the integrity of the inventory, new services should be registered using the following YAML template, which is then parsed by the inventory audit script.

```yaml
service_name: "Ghost"
purpose: "Personal Blog"
image: "ghost:latest"
data_path: "/mnt/tank/applications/ghost"
exposure: "Reverse Proxy"
owner: "Admin"
tags: ["web", "content"]
```

## CLI examples

### Inventory Audit Script (Python)
The following script audits the versions of all services defined in the inventory table against the currently running Docker containers.

```python
import subprocess
import re

def get_running_containers():
    result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}|{{.Image}}'], capture_output=True, text=True)
    return dict(line.split('|') for line in result.stdout.strip().split('\n') if '|' in line)

def audit_inventory(inventory_file):
    running = get_running_containers()
    with open(inventory_file, 'r') as f:
        content = f.read()

    matches = re.findall(r'\| \*\*([^*]+)\*\* \| [^|]+ \| `([^`]+)` \|', content)

    for name, expected in matches:
        container_name = name.lower().replace(' ', '-')
        actual = running.get(container_name, "NOT RUNNING")
        print(f"{name}: {actual} (Expected: {expected})")

if __name__ == "__main__":
    audit_inventory('docs/services/inventory.md')
```

### Service Health Check
Quick CLI check to verify service reachability.

```bash
# Check if n8n is reachable via local DNS
curl -s -I http://n8n.local:5678 | grep "HTTP/1.1 200 OK" || echo "n8n Down"
```

## API examples

### Fetching Inventory Data (Python)
Programmatically accessing the inventory for use in custom dashboards or agentic reasoning.

```python
import requests

def get_service_path(service_name):
    # Mocking a call to a hypothetical Documentation API or parsing the MD
    inventory = {
        "Nextcloud": {"data_path": "/mnt/pool/apps/nextcloud"},
        "Ollama": {"data_path": "/mnt/pool/apps/ollama"}
    }
    return inventory.get(service_name, {}).get("data_path", "Path not found")

print(get_service_path('Nextcloud'))
```

## Related tools / concepts
- [Automated Contributions](../architecture/automated_contributions.md) — How new services are registered.
- [Infrastructure Overview](../architecture/infrastructure.md) — Base hardware and OS details.
- [Nextcloud](nextcloud.md) — Core storage service.
- [Paperless-ngx](paperless-ngx.md) — Document management.
- [n8n](n8n.md) — Workflow automation orchestrator.
- [Ollama](ollama.md) — Local AI inference runner.
- [Authentik](authentik.md) — Identity and access management.
- [Syncthing](syncthing.md) — P2P file synchronization.

## Sources / references
- [TrueNAS SCALE Documentation](https://www.truenas.com/docs/scale/)
- [Home Lab Services Guide](https://github.com/joanmarcriera/Home-office-automations)
- [Docker Documentation](https://docs.docker.com/)

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
