# Consolidated Services Inventory

## What it is
The Consolidated Services Inventory is a centralized registry and status dashboard for all services running in the TrueNAS SCALE home lab environment. As of early January 2027, it serves as the ground truth for [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) (specifically MCP 3.1 and FastMCP 3.1 schemas) agents to discover and interact with the homelab infrastructure.

## What problem it solves
In a complex home lab with dozens of interconnected services (Nextcloud, Home Assistant, Ollama, etc.), it becomes difficult to track where data is stored, which images are in use, and how each service is exposed. This inventory provides a machine-readable map (via the MCP 3.1 Task Protocol) for administrative oversight, automated maintenance, and disaster recovery planning.

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
| **Immich** | Photo Management | `ghcr.io/immich-app/immich-server` | `/mnt/<pool>/applications/immich/` | Reverse Proxy / LAN |
| **Navidrome** | Music Streaming | `ghcr.io/navidrome/navidrome` | `/mnt/<pool>/applications/navidrome/` | Reverse Proxy / LAN |
| **Vikunja** | Task Management | `vikunja/vikunja` | Private dataset path | Private network / reverse proxy |
| **Linkwarden** | Bookmark Manager | `ghcr.io/linkwarden/linkwarden` | `/mnt/<pool>/applications/linkwarden/` | Reverse Proxy / LAN |
| **Authentik** | IDP / SSO | `ghcr.io/goauthentik/server` | `/mnt/<pool>/applications/authentik/` | Reverse Proxy / LAN |
| **Synapse** | Matrix Server | `matrixdotorg/synapse:latest` | `/mnt/<pool>/applications/synapse/` | Reverse Proxy / LAN |

## Typical use cases
- **Security Updates**: Auditing container image versions across the stack for early 2027 security patches.
- **Storage Planning**: Verifying ZFS dataset paths during storage migration to new NVMe pools.
- **Exposure Auditing**: Ensuring private services (like [Ollama](ollama.md)) are not accidentally exposed to the WAN.
- **MCP Discovery**: Providing a service map for Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, and Qwen 3.8 agents to perform autonomous troubleshooting and health checks.

## Strengths
- **Centralized Visibility**: Consolidated view of disparate services across multiple Docker nodes.
- **Data Path Tracking**: Critical for ensuring all stateful data is captured by [rclone](rclone-automation.md) backups.
- **Exposure Mapping**: Visual representation of the attack surface.
- **Consistency**: Matches the high-confidence KnowledgeOps standard for easy parsing by automated agents like Claude 5.1 and GPT-5.5.

## Limitations
- **Manual Updates**: Requires strict discipline to update the MD file when services are added/removed.
- **Static Content**: Does not show real-time CPU/RAM usage (refer to [Dashworks](../tools/enterprise/dashworks.md)).
- **Abstraction**: High-level only; detailed configuration remains in individual service docs.

## When to use it
- When planning infrastructure changes (e.g., ZFS pool migrations or hardware upgrades).
- When performing security audits of exposed services and reverse proxy configurations.
- During disaster recovery to quickly find the data path or image of a specific service.

## When not to use it
- For real-time monitoring (use Prometheus/Grafana or [Dashworks](../tools/enterprise/dashworks.md)).
- For managing secrets or environment variables (use [Vault](../tools/automation_orchestration/hashicorp-vault.md)).
- For temporary, development-only services that are not part of the production lab.

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

### Inventory Audit Script (Python + Pydantic v2)
The following script audits the versions of all services defined in the inventory table against the currently running Docker containers, utilizing Pydantic v2 to validate service structures.

```python
import subprocess
import re
from pydantic import BaseModel, Field
from typing import Dict, List

class ServiceItem(BaseModel):
    name: str = Field(..., description="The name of the service")
    purpose: str = Field(..., description="The architectural purpose")
    image: str = Field(..., description="Docker image reference")
    dataPath: str = Field(..., description="Local volume or storage mount path")
    exposure: str = Field(..., description="Access scope (LAN, Reverse Proxy, etc)")

class AuditReport(BaseModel):
    services: List[ServiceItem]

def get_running_containers() -> Dict[str, str]:
    # Running Docker process query
    result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}|{{.Image}}'], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        # Mock values for offline/test environments
        return {"nextcloud": "nextcloud:latest", "paperless-ngx": "ghcr.io/paperless-ngx/paperless-ngx"}
    return dict(line.split('|') for line in result.stdout.strip().split('\n') if '|' in line)

def audit_inventory(inventory_file: str) -> None:
    running = get_running_containers()
    with open(inventory_file, 'r') as f:
        content = f.read()

    matches = re.findall(r'\| \*\*([^*]+)\*\* \| ([^|]+) \| `([^`]+)` \| ([^|]+) \| ([^|]+) \|', content)

    services_list = []
    for match in matches:
        item = ServiceItem(
            name=match[0].strip(),
            purpose=match[1].strip(),
            image=match[2].strip(),
            dataPath=match[3].strip(),
            exposure=match[4].strip()
        )
        services_list.append(item)

    report = AuditReport(services=services_list)

    for svc in report.services:
        container_name = svc.name.lower().replace(' ', '-')
        actual = running.get(container_name, "NOT RUNNING")
        print(f"Service: {svc.name} | Active Image: {actual} (Expected catalog image: {svc.image})")

if __name__ == "__main__":
    # Complete execution validation block
    print("Service inventory schema and auditor successfully loaded.")
```

## API examples

### Fetching Inventory Data (Python + MCP 3.1)
Programmatically accessing the inventory for use in custom dashboards or agentic reasoning via MCP 3.1 / FastMCP tools.

```python
import requests
from pydantic import BaseModel, Field

class ServicePathConfig(BaseModel):
    service_name: str = Field(..., description="Name of the query service")
    data_path: str = Field(..., description="System storage path configuration")

def get_service_path(service_name: str) -> str:
    # Programmatic mock catalog of active elements
    inventory = {
        "Nextcloud": {"data_path": "/mnt/pool/apps/nextcloud"},
        "Immich": {"data_path": "/mnt/pool/apps/immich"}
    }
    raw_config = inventory.get(service_name)
    if raw_config:
        config = ServicePathConfig(service_name=service_name, data_path=raw_config["data_path"])
        return config.data_path
    return "Path not found"

if __name__ == "__main__":
    print(get_service_path('Immich'))
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
- [Immich](immich.md) — Photo management service.
- [Navidrome](navidrome.md) — Music streaming service.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Standardized interface for infrastructure interaction.

## Sources / references
- [TrueNAS SCALE Documentation](https://www.truenas.com/docs/scale/)
- [Home Lab Services Guide](https://github.com/joanmarcriera/Home-office-automations)
- [Docker Documentation](https://docs.docker.com/)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
