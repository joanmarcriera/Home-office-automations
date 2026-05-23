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

## Typical use cases
- Auditing container image versions for security updates.
- Verifying ZFS dataset paths during storage migration or backup configuration.
- Checking network exposure (Reverse Proxy vs. LAN-only) to ensure security compliance.
- Providing a "quick start" list for new developers onboarding to the lab environment.

## Strengths
- **Centralized Visibility**: Consolidated view of disparate services.
- **Data Path Tracking**: Critical for ensuring all stateful data is backed up.
- **Exposure Mapping**: Helps prevent accidental exposure of private services to the WAN.
- **Consistency**: Uses standard formatting that matches the rest of the KnowledgeOps documentation.

## Limitations
- **Manual Updates**: Currently requires manual updates when new services are added or configurations changed.
- **Static Content**: Does not show real-time health or performance metrics.
- **Abstraction**: High-level overview only; does not replace detailed individual service documentation.

## When to use it
- When planning infrastructure changes (e.g., pool migrations).
- When performing security audits of exposed services.
- During troubleshooting to quickly find the data path or image of a specific service.

## When not to use it
- For real-time monitoring (use Prometheus/Grafana instead).
- For detailed configuration parameters (refer to individual service `.md` files).
- For secret management (refer to Vault or TrueNAS Secrets).

## Getting started

### Registering a New Service
To maintain the integrity of the inventory, new services should be registered using the following YAML template, which is then parsed by the inventory audit script.

```yaml
# service_metadata.yaml example
service_name: "Ghost"
purpose: "Personal Blog"
image: "ghost:latest"
data_path: "/mnt/tank/applications/ghost"
exposure: "Reverse Proxy"
owner: "Admin"
tags: ["web", "content"]
```

## CLI examples

### Inventory Audit Script
The following Python script can be used to audit the versions of all services defined in the inventory table against the currently running Docker containers.

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

    # Extract service name and image from the markdown table
    matches = re.findall(r'\| \*\*([^*]+)\*\* \| [^|]+ \| `([^`]+)` \|', content)

    print(f"{'Service':<20} | {'Expected Image':<40} | {'Status'}")
    print("-" * 80)
    for name, expected in matches:
        container_name = name.lower().replace(' ', '-')
        actual = running.get(container_name, "NOT RUNNING")
        status = "OK" if actual == expected else "VERSION MISMATCH" if actual != "NOT RUNNING" else "MISSING"
        print(f"{name:<20} | {expected:<40} | {status}")

if __name__ == "__main__":
    # audit_inventory('docs/services/inventory.md')
    print("Example output for Nextcloud: OK")
```

### Service Health Check
A quick CLI check to verify if critical services are responding on their expected ports.

```bash
# Check if Nextcloud is reachable
curl -s -I http://nextcloud.local | grep "HTTP/1.1 200 OK" || echo "Nextcloud Down"

# Check if Ollama API is active
curl -s http://ollama.local:11434/api/tags | grep -q "models" && echo "Ollama Up" || echo "Ollama Down"
```

## API examples

### Fetching Inventory via REST
If the inventory is served via a documentation server (like MkDocs), it can be queried programmatically to assist automated maintenance agents.

```python
import requests

def get_service_path(service_name):
    # Mocking a call to the documentation API
    doc_url = "https://docs.homelab.local/services/inventory/data.json"
    # response = requests.get(doc_url)
    # inventory = response.json()

    inventory = {
        "Nextcloud": {"data_path": "/mnt/pool/apps/nextcloud"},
        "Ollama": {"data_path": "/mnt/pool/apps/ollama"}
    }

    return inventory.get(service_name, {}).get("data_path", "Path not found")

print(f"Data Path for Nextcloud: {get_service_path('Nextcloud')}")
```

## Related tools / concepts
- [Automated Contributions](../architecture/automated_contributions.md) — How new services are added to the documentation.
- [Infrastructure Overview](../architecture/infrastructure.md) — The hardware and base OS (TrueNAS SCALE).
- [Nextcloud](nextcloud.md) — Core storage service.
- [Home Assistant](home-assistant.md) — Core automation service.
- [Ollama](ollama.md) — Local AI inference.
- [LiteLLM](litellm.md) — AI proxy layer.
- [Paperless-ngx](paperless-ngx.md) — Document management.
- [Vikunja](vikunja.md) — Task management.
- [n8n](n8n.md) — Workflow automation orchestrator.
- [Authentik](authentik.md) — Identity and access management.

## Sources / references
- [TrueNAS SCALE Documentation](https://www.truenas.com/docs/scale/)
- [Home Lab Services Guide](https://github.com/joanmarcriera/Home-office-automations)

## Infrastructure Gaps & Risks
- **Direct Discovery**: Automated service discovery was restricted due to lack of direct `k3s`/`midclt` access from the development environment. Documentation is based on "Known Services" requirements and expected TrueNAS patterns.
- **Secret Management**: Need to ensure all `.env` files are properly excluded from version control and secrets are managed via a dedicated manager (e.g., Vault or TrueNAS Secrets).
- **ZFS Dataset Alignment**: Verified dataset paths should be updated in the individual service files once the final pool structure is confirmed.
- **Monitoring**: Integration of a centralized monitoring stack (Prometheus/Grafana) is identified as a short-term roadmap item.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-23
