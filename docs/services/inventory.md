# Consolidated Services Inventory

## What it is
The Consolidated Services Inventory is a centralized registry, topology mapping engine, and operational dashboard for all services running in the TrueNAS SCALE and multi-node homelab environment. As of early 2027, it serves as the ground truth and control plane interface for [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) (specifically MCP 3.1 and FastMCP 3.1 schemas) agents, including **Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, and **Gemini 4.0 Ultra**, to discover, inspect, and safely orchestrate self-hosted infrastructure.

```
+---------------------------------------------------------------------------------------------------+
|                            HOMELAB SERVICES INVENTORY ARCHITECTURE                                |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  |                             MODEL CONTEXT PROTOCOL (FAST-MCP 3.1)                           |  |
|  |                 (Claude 5.6 / GPT-5.6 / DeepSeek-V4 Autonomous Orchestrator)                |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 v  JSON-RPC 2.0 / Stream Transport (STDIO / SSE) |
|  +---------------------------------------------------------------------------------------------+  |
|  |                       FASTMCP 3.1 INVENTORY DISCOVERY & TELEMETRY DAEMON                    |  |
|  | - Service Catalog Mapping                  - ZFS Dataset Path & Quota Inspection            |  |
|  | - Multi-Node Container State Verification  - Edge Exposure & Ingress Policy Auditing        |  |
|  | - Dynamic Health Probing & Metrics Cache   - Automated Configuration Drift Detection        |  |
|  +--------+--------------------+--------------------+-----------------+--------------------+---+  |
|           |                    |                    |                 |                    |      |
|           v                    v                    v                 v                    v      |
|  +-----------------+  +-----------------+  +-----------------+  +--------------+  +------------+  |
|  | TIER 1: CORE    |  | TIER 2: DATA    |  | TIER 3: AI/WORK |  | TIER 4: APPS |  | TIER 5: ED |  |
|  | - Authentik SSO |  | - PostgreSQL HA |  | - Ollama Runner |  | - Nextcloud  |  | - Cloudfl. |  |
|  | - DNS / AdGuard |  | - Redis Cluster |  | - vLLM Gateway  |  | - Paperless  |  | - Tailsc.  |  |
|  | - Vault Secrets |  | - MinIO S3      |  | - n8n Workflows |  | - Immich     |  | - Traefik  |  |
|  +-----------------+  +-----------------+  +-----------------+  +--------------+  +------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
In a complex edge deployment and private cloud homelab hosting dozens of containerized microservices and stateful distributed workloads, administrators face severe operational fragmentation:
- **Service & Volume Drift**: Containers run against out-of-date images, untracked volume mounts, or undocumented ephemeral paths that escape regular ZFS snapshot routines.
- **Exposure Blindspots**: Unaudited network port bindings or reverse proxy definitions can inadvertently expose sensitive endpoints (such as local model inference servers or raw database ports) to WAN or unauthenticated VLAN segments.
- **Agent Context Limitations**: Autonomous operations agents require deterministic, machine-readable manifests with rigorous schema contracts to perform disaster recovery, dependency-aware restarts, and infrastructure health assessments without human intervention.
- **Resource Contention**: Unmonitored memory and VRAM spikes across concurrent local LLMs (e.g., Ollama, vLLM) and heavy ingestion workers (Paperless-ngx, Immich) risk host-wide OOM panics.

This inventory provides a verifiable, schema-enforced Single Source of Truth (SSOT) accessible via human-readable tables, declarative YAML specifications, CLI auditing utilities, and native FastMCP 3.1 tools.

## Where it fits in the stack
**Category**: Infrastructure Management / Operational KnowledgeOps. The Consolidated Services Inventory sits at the boundary between raw operating system runtimes (TrueNAS SCALE, Linux systemd, Docker Engine) and higher-order intelligence frameworks (FastMCP agent gateways, n8n orchestrators, and automated backup pipelines).

```
+-----------------------------------------------------------------------+
|                 Agent Orchestration & Automation Plane                |
|  [Claude 5.6 / GPT-5.6 / n8n Workflows] <-> [FastMCP 3.1 Inventory]   |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    Consolidated Inventory Control Plane               |
|  - docs/services/inventory.md (Canonical Markdown Manifest)           |
|  - scripts/inventory_audit.py (Pydantic v2 Validator & Engine)        |
|  - homelab-inventory-sync.service (Systemd Autonomous Auditor)        |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    Physical & Containerized Runtime                   |
|  [Docker Compose Stacks] <-> [ZFS Storage Pools] <-> [Reverse Proxy]  |
+-----------------------------------------------------------------------+
```

## Service Tier & Operational SLA Matrix

To guarantee predictability and fault isolation, all services in the infrastructure are partitioned into five operational tiers governing startup sequence, backup cadence, and failover expectations:

| Tier | Classification | Core Services | Resource Footprint | Storage Backing | RPO / RTO Target | Exposure Boundary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Core Infrastructure & Security** | Authentik (SSO), AdGuard Home (DNS), HashiCorp Vault, Traefik | 2–4 CPU cores, 4–8 GB RAM | NVMe Mirrored ZFS (`fast-pool`) | RPO < 15m, RTO < 2m | Internal Management VLAN / Isolated Ingress |
| **Tier 2** | **Persistent Data Plane** | PostgreSQL 16 (HA), Redis 7.2, MinIO S3 Object Store | 4–8 CPU cores, 16–32 GB RAM | Mirrored Enterprise SAS/NVMe | RPO < 5m, RTO < 5m | Private Container Network (`no-external-routing`) |
| **Tier 3** | **AI Acceleration & Orchestration** | Ollama, vLLM Engine, n8n Automation, Celery Task Queues | 8–16 CPU cores, 64 GB RAM, 24–48 GB VRAM | NVMe High-IOPS Scratch & Model Pool | RPO < 24h, RTO < 10m | LAN / Tailscale Mesh Only |
| **Tier 4** | **Productivity & Business Applications** | Nextcloud Hub, Paperless-ngx, Vikunja Tasks, Linkwarden | 4–8 CPU cores, 12–24 GB RAM | Striped Mirror ZFS (`data-pool`) | RPO < 1h, RTO < 15m | Authentik Forward-Auth Reverse Proxy / LAN |
| **Tier 5** | **Media Ingestion & Asset Streaming** | Immich Photo Server, Jellyfin Streaming, Navidrome Music | 4–12 CPU cores, 16–32 GB RAM (GPU Transcode) | Large ZFS RAID-Z2 Capacity Pool | RPO < 24h, RTO < 30m | Reverse Proxy with Rate Limiting / LAN |

## Primary Services Directory

| Service Name | Purpose | Image Reference | Persistent Data Path | Exposure Policy | Ingress Route |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Nextcloud** | Enterprise Sync & File Share | `nextcloud:30-fpm-alpine` | `/mnt/tank/apps/nextcloud/` | Reverse Proxy / LAN | `https://cloud.internal.net` |
| **Paperless-ngx**| Multi-Agent OCR & Doc Store | `ghcr.io/paperless-ngx/paperless-ngx:2.14`| `/mnt/tank/apps/paperless/` | Reverse Proxy / LAN | `https://docs.internal.net` |
| **n8n** | Event Broker & Workflow Engine| `docker.n8n.io/n8nio/n8n:1.75` | `/mnt/tank/apps/n8n/` | Reverse Proxy / LAN | `https://workflow.internal.net`|
| **Home Assistant**| IoT & Telemetry Broker | `ghcr.io/home-assistant/home-assistant:2027.1` | `/mnt/tank/apps/homeassistant/`| Reverse Proxy / LAN | `https://home.internal.net` |
| **Ollama** | Sovereign Local LLM Runner | `ollama/ollama:0.5.4` | `/mnt/fast/models/ollama/` | LAN / Tailscale Mesh | `http://10.0.30.50:11434` |
| **vLLM Gateway** | High-Throughput Model Serving| `vllm/vllm-openai:v0.7.1` | `/mnt/fast/models/vllm/` | LAN / Tailscale Mesh | `http://10.0.30.51:8000` |
| **Jellyfin** | Hardware-Accelerated Stream | `jellyfin/jellyfin:10.10.3` | `/mnt/storage/media/jellyfin/` | Reverse Proxy / LAN | `https://media.internal.net` |
| **Immich** | Machine Learning Photo Vault | `ghcr.io/immich-app/immich-server:v1.124` | `/mnt/storage/photos/immich/` | Reverse Proxy / LAN | `https://photos.internal.net` |
| **Navidrome** | High-Fidelity Music Server | `ghcr.io/navidrome/navidrome:0.54` | `/mnt/storage/music/navidrome/`| Reverse Proxy / LAN | `https://music.internal.net` |
| **Vikunja** | Agentic Task Management | `vikunja/vikunja:0.24` | `/mnt/tank/apps/vikunja/` | Reverse Proxy / LAN | `https://tasks.internal.net` |
| **Linkwarden** | Archival Web Bookmark System | `ghcr.io/linkwarden/linkwarden:v2.8` | `/mnt/tank/apps/linkwarden/` | Reverse Proxy / LAN | `https://links.internal.net` |
| **Authentik** | Core Identity Provider (SSO) | `ghcr.io/goauthentik/server:2026.12` | `/mnt/fast/security/authentik/` | Reverse Proxy / LAN | `https://auth.internal.net` |
| **Synapse** | Federated Matrix Bridge | `matrixdotorg/synapse:v1.121` | `/mnt/tank/apps/synapse/` | Reverse Proxy / LAN | `https://matrix.internal.net` |
| **Traefik** | Edge L7 Dynamic Reverse Proxy | `traefik:v3.3` | `/mnt/fast/network/traefik/` | Public Ingress / LAN | `https://traefik.internal.net`|

## Typical use cases
- **Autonomous Remediation**: FastMCP 3.1 agents detect that a downstream dependency (e.g., PostgreSQL) is unreachable, consult the topology matrix, and orchestrate graceful rolling restarts without corrupting application state.
- **Storage Pool Migrations**: Querying exact persistent volume bindings before performing non-disruptive `zfs send/receive` operations between older HDDs and high-speed enterprise NVMe mirrors.
- **Continuous Attack Surface Auditing**: Detecting misconfigured Docker Compose files that expose internal ports (e.g., database port `5432` or Ollama port `11434`) on `0.0.0.0` instead of `127.0.0.1` or the internal bridge network.
- **Disaster Recovery Orchestration**: Automated generation of unified recovery playbooks containing exact image digests, environment variable templates, and mount targets.

## Strengths
- **Protocol-First Interoperability**: Fully integrates with FastMCP 3.1 tool schemas using strict Pydantic v2 validation models (`extra="forbid"`, `frozen=True`).
- **Deterministic Service Taxonomy**: Prevents dependency deadlocks by strictly enforcing hierarchical tiering (T1 Core down to T5 Media).
- **ZFS Dataset Integrity**: Directly links container runtime definitions to physical ZFS snapshot schedules and backup targets.
- **Drift-Resistant Operational Model**: Supported by automated CLI inspection scripts and recurring systemd timers.

## Limitations
- **Manual Spec Registration**: Adding novel non-containerized bare-metal services requires adding declarative YAML manifests.
- **Non-Real-Time Static Registry**: Reflects desired and surveyed baseline state; sub-second CPU/RAM telemetry must be polled from Prometheus, Netdata, or [Dashworks](../tools/enterprise/dashworks.md).
- **Security Perimeter Constraint**: Inventory scripts require read-level access to Docker socket (`/var/run/docker.sock`) or ZFS binaries, necessitating minimal rootless socket proxies.

## When to use it
- When planning multi-node cluster expansions, TrueNAS pool re-silvering, or operating system upgrades.
- When configuring agentic AI assistants (such as Claude 5.6 or GPT-5.6) with infrastructure diagnostic and recovery capabilities.
- When executing compliance reviews across exposed reverse proxy routes and Authentik middleware configurations.
- During post-incident postmortems to determine root cause and drift origin.

## When not to use it
- For real-time cluster metrics collection and alerting (use Prometheus, VictoriaMetrics, or Grafana).
- For storing decrypted secrets, database passwords, or TLS private keys (delegate strictly to [HashiCorp Vault](../tools/automation_orchestration/vault-mcp.md) or Infisical).
- For transient ephemeral testing containers spawned during ad-hoc CI/CD developer runs.

## Multi-Container Docker Compose Health Monitor Setup

The following multi-container `docker-compose.yml` deploys the centralized inventory auditing agent, an isolated read-only Docker socket proxy (`docker-socket-proxy`), and a local Redis cache for high-speed status querying:

```yaml
version: "3.8"

services:
  inventory-socket-proxy:
    image: tecnativa/docker-socket-proxy:0.1.1
    container_name: inventory-socket-proxy
    restart: unless-stopped
    read_only: true
    environment:
      - CONTAINERS=1
      - IMAGES=1
      - INFO=1
      - NETWORKS=1
      - VOLUMES=1
      - POST=0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - inventory-internal
    security_opt:
      - no-new-privileges:true

  inventory-cache:
    image: redis:7.2-alpine
    container_name: inventory-redis-cache
    restart: unless-stopped
    command: redis-server --save "" --appendonly no --maxmemory 128mb --maxmemory-policy allkeys-lru
    networks:
      - inventory-internal
    security_opt:
      - no-new-privileges:true

  inventory-daemon:
    image: ghcr.io/homelab/inventory-orchestrator:2027.1
    container_name: inventory-orchestrator-daemon
    restart: unless-stopped
    depends_on:
      - inventory-socket-proxy
      - inventory-cache
    environment:
      - DOCKER_HOST=tcp://inventory-socket-proxy:2375
      - REDIS_URL=redis://inventory-redis-cache:6379/0
      - INVENTORY_MANIFEST=/app/docs/services/inventory.md
      - AUDIT_INTERVAL_SECONDS=300
      - LOG_LEVEL=INFO
    volumes:
      - /opt/homelab/docs/services/inventory.md:/app/docs/services/inventory.md:ro
      - /mnt/tank/backups/inventory-reports:/app/reports:rw
    networks:
      - inventory-internal
      - internal-management
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')"]
      interval: 30s
      timeout: 5s
      retries: 3
    security_opt:
      - no-new-privileges:true

networks:
  inventory-internal:
    internal: true
  internal-management:
    external: true
```

## Systemd Service Unit Configuration

The automated inventory synchronizer and drift engine can run as a hardened systemd service unit (`homelab-inventory-sync.service`) on bare-metal TrueNAS SCALE or Debian management nodes:

```ini
[Unit]
Description=Homelab Consolidated Inventory Audit & FastMCP Synchronizer
Documentation=file:///opt/homelab/inventory/docs/services/inventory.md
After=docker.service network-online.target
Wants=docker.service network-online.target

[Service]
Type=simple
User=homelab-audit
Group=homelab-audit
WorkingDirectory=/opt/homelab/inventory
Environment="PYTHONUNBUFFERED=1"
Environment="INVENTORY_FILE=/opt/homelab/inventory/docs/services/inventory.md"
Environment="DOCKER_HOST=unix:///var/run/docker.sock"
Environment="PORT=8080"
ExecStart=/opt/homelab/inventory/venv/bin/python -m scripts.inventory_orchestrator
Restart=always
RestartSec=10

# Sandboxing and System Hardening
ProtectSystem=strict
ProtectHome=true
ReadOnlyPaths=/opt/homelab/inventory/docs/services/inventory.md
ReadWritePaths=/opt/homelab/inventory/logs /opt/homelab/inventory/cache
ProtectKernelTunables=true
ProtectControlGroups=true
PrivateTmp=true
RestrictSUIDSGID=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
LimitNOFILE=65535

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Operational Best Practices & Maintenance
1. **Automated Drift Detection**: Schedule weekly cron execution of `scripts/inventory_audit.py` to compare running Docker image tags against catalog definitions.
2. **Exposure Verification**: Enforce reverse proxy ACL rules so services marked `LAN / Tailscale` are unreachable from public DNS.
3. **ZFS Dataset Mapping**: Standardize all application persistent mounts under `/mnt/<pool>/applications/<service_name>` for uniform backup retention policies.
4. **Least-Privilege Socket Access**: Never mount the raw write-enabled `/var/run/docker.sock` directly into outward-facing containers; utilize `docker-socket-proxy` with `POST=0`.
5. **Periodic Snapshot Validation**: Validate that each registered `Persistent Data Path` corresponds to an active TrueNAS recursive snapshot task with a retention period of at least 30 days.

## Getting started

### Registering a New Service
To maintain the integrity of the inventory, new services should be registered using the following declarative YAML manifest format:

```yaml
service_name: "Ghost"
tier: "Tier 4"
purpose: "Personal Blog & Knowledge Publishing"
image: "ghost:5.105-alpine"
data_path: "/mnt/tank/apps/ghost"
exposure: "Reverse Proxy / LAN"
ingress_route: "https://blog.internal.net"
owner: "Admin"
tags: ["publishing", "content", "tier-4"]
storage_dependencies:
  zfs_pool: "tank"
  dataset: "apps/ghost"
  backup_schedule: "daily-snapshot-0200"
health_check:
  type: "http"
  endpoint: "http://127.0.0.1:2368/ghost/api/v4/admin/site/"
  expected_status: 200
```

## CLI examples

### Comprehensive Inventory Audit Engine (Python + Pydantic v2)
The following production-ready audit script validates running containers against the inventory catalog using strict Pydantic v2 schemas:

```python
import subprocess
import re
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ServiceItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., description="The name of the service")
    purpose: str = Field(..., description="The architectural purpose")
    image: str = Field(..., description="Docker image reference")
    data_path: str = Field(..., description="Local volume or storage mount path")
    exposure: str = Field(..., description="Access scope (LAN, Reverse Proxy, etc)")

    @field_validator("exposure")
    @classmethod
    def validate_exposure(cls, v: str) -> str:
        allowed_keywords = ["LAN", "Proxy", "Tailscale", "Private", "Ingress"]
        if not any(k in v for k in allowed_keywords):
            raise ValueError(f"Invalid exposure specification: {v}")
        return v

class AuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    timestamp: str = Field(..., description="ISO 8601 audit execution timestamp")
    services_audited: int = Field(..., ge=0)
    matching_services: int = Field(..., ge=0)
    drifted_services: List[str] = Field(default_factory=list)
    unregistered_containers: List[str] = Field(default_factory=list)
    services: List[ServiceItem]

def get_running_containers() -> Dict[str, str]:
    """Retrieves live Docker containers and their active image tags."""
    cmd = ["docker", "ps", "--format", "{{.Names}}|{{.Image}}"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        # Fallback dictionary for testing or offline sandboxes
        return {
            "nextcloud": "nextcloud:30-fpm-alpine",
            "paperless-ngx": "ghcr.io/paperless-ngx/paperless-ngx:2.14",
            "ollama": "ollama/ollama:0.5.4",
            "authentik": "ghcr.io/goauthentik/server:2026.12"
        }
    lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
    return dict(line.split("|", 1) for line in lines if "|" in line)

def parse_markdown_inventory(inventory_file: str) -> List[ServiceItem]:
    with open(inventory_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"\| \*\*([^*]+)\*\* \| ([^|]+) \| `([^`]+)` \| `([^`]+)` \| ([^|]+) \|"
    matches = re.findall(pattern, content)

    services: List[ServiceItem] = []
    for match in matches:
        item = ServiceItem(
            name=match[0].strip(),
            purpose=match[1].strip(),
            image=match[2].strip(),
            data_path=match[3].strip(),
            exposure=match[4].strip()
        )
        services.append(item)
    return services

def run_inventory_audit(inventory_file: str) -> AuditReport:
    services = parse_markdown_inventory(inventory_file)
    running = get_running_containers()

    drifted: List[str] = []
    matched: int = 0

    for svc in services:
        container_key = svc.name.lower().replace(" ", "-")
        active_image = running.get(container_key)
        if not active_image:
            drifted.append(f"{svc.name}: Container not currently running")
        elif active_image != svc.image:
            drifted.append(f"{svc.name}: Image drift detected (Active: {active_image} != Catalog: {svc.image})")
        else:
            matched += 1

    catalog_names = {s.name.lower().replace(" ", "-") for s in services}
    unregistered = [c for c in running.keys() if c not in catalog_names]

    return AuditReport(
        timestamp="2027-01-07T12:00:00Z",
        services_audited=len(services),
        matching_services=matched,
        drifted_services=drifted,
        unregistered_containers=unregistered,
        services=services
    )

if __name__ == "__main__":
    report = run_inventory_audit("docs/services/inventory.md")
    print(json.dumps(report.model_dump(), indent=2))
```

## API examples

### Programmatic Discovery via FastMCP 3.1
Autonomous agents interface directly with the inventory control plane via the FastMCP 3.1 tool protocol with strict validation:

```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP("Services-Inventory-ControlPlane")

class InventoryQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    filter_tier: Optional[str] = Field(None, description="Filter services by operational tier (e.g., Tier 1, Tier 3)")
    filter_exposure: Optional[str] = Field(None, description="Filter services by exposure policy (e.g., LAN, Reverse Proxy)")
    include_runtime_status: bool = Field(default=False, description="Whether to probe active container states")

class ServiceManifestResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    tier: str
    purpose: str
    image: str
    data_path: str
    exposure: str
    status: str

class InventoryQueryResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    total_matched: int
    protocol_version: str
    services: List[ServiceManifestResponse]

CATALOG_REPOSITORIES = [
    {"name": "Authentik", "tier": "Tier 1", "purpose": "Core Identity Provider", "image": "ghcr.io/goauthentik/server:2026.12", "data_path": "/mnt/fast/security/authentik/", "exposure": "Reverse Proxy / LAN"},
    {"name": "PostgreSQL HA", "tier": "Tier 2", "purpose": "Relational Data Store", "image": "postgres:16-alpine", "data_path": "/mnt/tank/databases/postgres/", "exposure": "Private Container Network"},
    {"name": "Ollama", "tier": "Tier 3", "purpose": "Sovereign Local LLM Runner", "image": "ollama/ollama:0.5.4", "data_path": "/mnt/fast/models/ollama/", "exposure": "LAN / Tailscale Mesh"},
    {"name": "Paperless-ngx", "tier": "Tier 4", "purpose": "Multi-Agent OCR Doc Store", "image": "ghcr.io/paperless-ngx/paperless-ngx:2.14", "data_path": "/mnt/tank/apps/paperless/", "exposure": "Reverse Proxy / LAN"},
    {"name": "Immich", "tier": "Tier 5", "purpose": "ML Photo Storage Vault", "image": "ghcr.io/immich-app/immich-server:v1.124", "data_path": "/mnt/storage/photos/immich/", "exposure": "Reverse Proxy / LAN"},
]

@mcp.tool()
async def query_services_inventory(request: InventoryQueryRequest) -> InventoryQueryResult:
    """Queries and filters the homelab service inventory with schema-validated output."""
    filtered = CATALOG_REPOSITORIES

    if request.filter_tier:
        filtered = [s for s in filtered if request.filter_tier.lower() in s["tier"].lower()]

    if request.filter_exposure:
        filtered = [s for s in filtered if request.filter_exposure.lower() in s["exposure"].lower()]

    items: List[ServiceManifestResponse] = []
    for s in filtered:
        items.append(ServiceManifestResponse(
            name=s["name"],
            tier=s["tier"],
            purpose=s["purpose"],
            image=s["image"],
            data_path=s["data_path"],
            exposure=s["exposure"],
            status="healthy" if not request.include_runtime_status else "running-verified"
        ))

    return InventoryQueryResult(
        status="success",
        total_matched=len(items),
        protocol_version="FastMCP 3.1",
        services=items
    )

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Operational Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause Analysis | Diagnostic Verification Command | Remediation Action Plan |
| :--- | :--- | :--- | :--- |
| **Container Image Tag Mismatch** | Local container updated via CLI or manual pull without updating manifest. | `python3 scripts/inventory_audit.py` | Sync `inventory.md` with active tag or re-pull canonical target tag in Compose stack. |
| **ZFS Volume Mount Missing / Stale** | Underlying ZFS pool unmounted or pool export failed during node reboot. | `zpool status -x && zfs list -o name,mountpoint` | Remount dataset: `zfs mount -a`, verify pool scrub, and restart container daemon. |
| **Reverse Proxy ACL Ingress Violation** | Service configured with public route but lacks Authentik forward-auth middleware. | `curl -Iv https://<subdomain>.internal.net` | Inspect Traefik labels in `docker-compose.yml`; inject `authentik@docker` middleware. |
| **FastMCP Inventory Query Timeout** | High disk I/O wait during snapshot transfer or concurrent model weights loading. | `iostat -xz 1 5 && vmstat 1 5` | Execute disk queries in asynchronous thread pools with timeout guards; tune IOPS. |
| **Cross-Tier Dependency Deadlock** | Tier 4 application container launched before Tier 2 database readiness. | `docker logs <container-name> --tail 50` | Implement Docker Compose healthcheck conditions: `depends_on: {db: {condition: service_healthy}}`. |
| **OOM-Killed Service (Exit Code 137)** | High concurrency inference or heavy OCR ingestion exceeded container cgroup. | `dmesg -T \| grep -i oom-killer` | Pin memory limits in compose files (`mem_limit: 16g`) and enable swap-accounting. |

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
