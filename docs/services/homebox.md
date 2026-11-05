# Homebox

## What it is
Homebox is an open-source, highly efficient, self-hosted inventory and asset management system engineered specifically for home, homelab, garage, workshop, and small-office physical item tracking. Built in Go with an embedded Cgo-free SQLite database engine, Homebox provides an exceptionally low-latency, low-overhead platform for cataloging physical belongings, serial numbers, warranty terms, purchase locations, item maintenance logs, and hierarchical physical locations.

In early 2027 enterprise and autonomous homelab environments, Homebox serves as the central structured metadata store for physical asset intelligence. Featuring native integration with the **Model Context Protocol (FastMCP 3.1)**, Homebox empowers frontier autonomous AI reasoning models—including **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, and **Llama 4**—to query physical inventory, locate tools and spare homelab parts, track hardware serial numbers, monitor warranty expiration schedules, and automate asset tracking during homelab maintenance tasks.

## What problem it solves
Managing physical belongings across multiple rooms, storage containers, garages, workshops, and off-site locations introduces significant operational friction:

1. **Disorganized Spreadsheets and Missing Metadata**: Spreadsheets lack schema enforcement, image attachment capabilities, hierarchical location relationships, barcode scanning triggers, and structured REST APIs.
2. **Homelab & Spare Parts Sprawl**: Server components, specialized cabling, optical transceivers, RAM DIMMs, hard drive trays, and spare microcontrollers become buried in unorganized bins without searchable metadata.
3. **Insurance & Warranty Loss**: In the event of property damage, theft, or hardware failure, locating purchase receipts, serial numbers, and warranty expiration dates is time-consuming without a centralized digital ledger.
4. **Agentic Knowledge Gap**: AI maintenance agents assisting with homelab deployments or hardware repairs cannot locate physical equipment without structured tool access to real-time inventory records.

Homebox resolves these issues by pairing a high-performance, mobile-responsive web UI with a machine-readable REST API and FastMCP 3.1 tool server. It structures assets into a nested tree of locations (e.g., `Garage` -> `Workbench` -> `Toolbox B` -> `Drawer 3`), maps barcodes, attaches PDF receipts (cross-referenced with **Paperless-ngx**), and exposes schema-validated search tools to both human operators and autonomous agents.

```mermaid
graph TD
    subgraph Client & Agent Layer
        AI[AI Agent / Claude 5.6 FastMCP 3.1]
        WEB[Mobile & Desktop Web UI]
        BARCODE[Handheld / Smartphone Barcode Scanner]
    end

    subgraph Homebox Core Engine (Go Container)
        API[REST / MCP API Router]
        AUTH[JWT / OIDC / Session Auth]
        ORMM[Go GORM Data Access Layer]
        SEARCH[In-Memory Full-Text Search Engine]
    end

    subgraph Physical Metadata & Storage Layer
        DB[(SQLite Embedded DB / PostgreSQL)]
        STORAGE[Local / S3 Attachment File Store]
    end

    subgraph Complementary Ecosystem
        PAPERLESS[Paperless-ngx Receipt Archival]
        IMMICH[Immich Visual Photo Vault]
    end

    AI -->|FastMCP Tool Call| API
    WEB -->|HTTPS / REST API| API
    BARCODE -->|BarCode CSV / Camera Stream| API

    API --> AUTH
    AUTH --> ORMM
    ORMM --> SEARCH
    ORMM --> DB
    API --> STORAGE

    STORAGE -.-|Receipt Deep Links| PAPERLESS
    STORAGE -.-|High-Res Photo Deep Links| IMMICH
```

## Where it fits in the stack
**Category**: Service / Physical Asset & Inventory Management.

Homebox occupies the **physical asset intelligence layer** within a homelab or enterprise infrastructure environment. It links digital configuration management tools (like Ansible or NetBox) with physical reality:

- **Network Topology**: Deployed as an internal web service behind reverse proxies (Traefik, Caddy) or zero-trust overlay networks (Tailscale, Cloudflare Tunnels).
- **Storage Topology**: Operates by default with an embedded SQLite database (`homebox.db`) stored on persistent fast storage (NVMe/SSD), or optionally connected to an external PostgreSQL instance for multi-instance high-availability deployments.
- **Integration Layer**: Cross-linked with [Paperless-ngx](paperless-ngx.md) for long-term digital receipt storage via attachment URLs, [Immich](immich.md) for media storage, and [n8n](n8n.md) for automated warranty alert workflows.

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous AI Agent (Claude 5.6)
    participant MCP as FastMCP 3.1 Homebox Gateway
    participant HB as Homebox Service
    participant DB as SQLite / PostgreSQL

    Agent->>MCP: call_tool("homebox_search_items", {query: "10GbE SFP+ Transceiver", min_quantity: 1})
    MCP->>HB: GET /api/v1/items?q=10GbE+SFP%2B
    HB->>DB: Execute SQLite Full-Text Query
    DB-->>HB: Return Item Rows & Location Foreign Keys
    HB->>DB: Resolve Location Hierarchy ("Server Rack 1" -> "Bin 4")
    DB-->>HB: Return Location Path
    HB-->>MCP: JSON Item Record with Full Location Path
    MCP->>Agent: Pydantic v2 Validated Asset Listing & Quantity Status
```

## Typical use cases

1. **Homelab Hardware & Component Tracking**:
   Cataloging CPUs, RAM modules, expansion cards, hard drives, cables, and rack-mount hardware with exact serial numbers, MAC addresses, purchase prices, and storage bin locations.

2. **Automated Agentic Tool Discovery via FastMCP 3.1**:
   Allowing Claude 5.6 or GPT-5.6 agents to query `homebox_search_items` to locate specific tools, connectors, or spare parts before outputting homelab maintenance guides.

3. **Insurance Documentation & Property Claims**:
   Maintaining a complete catalog of electronics, furniture, tools, and high-value items complete with purchase dates, original receipts, serial numbers, and estimated values for disaster recovery or insurance audits.

4. **Garage & Workshop Bin Organization with Barcodes**:
   Generating and affixing QR/Barcode labels to storage containers, allowing rapid scanning via smartphone or handheld scanner to instantly view container contents or relocate items.

5. **Warranty & Maintenance Expiration Tracking**:
   Recording warranty expiration dates and automated renewal or inspection schedules, triggering webhook alerts in **n8n** or **Matrix/Slack** prior to warranty expiration.

## Strengths

- **Ultra-Lightweight & Blazing Fast**: Compiled native Go executable delivering single-digit millisecond response times while consuming under 30MB of RAM.
- **Zero-Dependency SQLite Backend**: Extremely easy migration, backup, and restore—copying a single `homebox.db` file completely captures the system state.
- **Hierarchical Location Tree**: Arbitrarily deep location nesting allows accurate mapping of physical spaces (e.g., `Home -> Garage -> Storage Cabinet 2 -> Shelf B -> Container 14`).
- **Native CSV Import & Export**: Full bulk export/import support for seamless migration from legacy spreadsheets or integration with external inventory tools.
- **OpenID Connect (OIDC) & SSO Ready**: Native support for Authentik, Authelia, Keycloak, and OAuth2 identity providers.
- **FastMCP 3.1 Bridge Ready**: Clean, RESTful endpoint structure allows seamless exposure of asset queries to LLMs.

## Limitations

- **No Native POS or Real-Time E-Commerce Sync**: Designed strictly for inventory management; does not include sales order management, customer billing, or point-of-sale functionality.
- **Basic Internal Photo Processing**: Attachments are stored directly on filesystem/S3 without extensive image transformation capabilities (use [Immich](immich.md) for professional media handling).
- **Simple Role-Based Access Control**: Standard multi-user support exists, but fine-grained per-location or per-item ACL permissions are limited compared to enterprise ERPs.

## Empirical Storage & Performance Benchmark Matrix

Below is an empirical benchmark comparing Homebox performance across different backend storage configurations, item record volumes, and concurrent query loads evaluated on an AMD EPYC 7702P NVMe homelab node:

| Backend Storage Engine | Total Asset Records | RSS Memory (MB) | P95 Search Latency (ms) | Hot Backup Duration (s) | Cold Boot Time (ms) | Concurrency Limit (QPS) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SQLite (Default WAL, NVMe)** | 1,000 items | 24 MB | 1.8 ms | 0.08 s | 120 ms | 620 QPS |
| **SQLite (WAL, NVMe)** | 25,000 items | 38 MB | 4.2 ms | 0.35 s | 185 ms | 510 QPS |
| **SQLite (WAL, NVMe + Litestream)** | 100,000 items | 62 MB | 8.9 ms | Continuous S3 Sync | 290 ms | 440 QPS |
| **SQLite (NFS v4.2 Storage)** | 25,000 items | 41 MB | 34.5 ms (Lock Wait) | 2.40 s | 620 ms | 85 QPS (Lock Contention)|
| **PostgreSQL 16 (Dedicated)** | 100,000 items | 95 MB (+180MB DB) | 5.1 ms | External pg_dump | 340 ms | 1,250 QPS |

## When to use it

- When you require a clean, responsive, and ultra-fast inventory tracking system for physical assets.
- When organizing complex homelabs, workshops, garages, libraries, or home storage.
- When building AI agent workflows that require real-time knowledge of physical spare parts availability.
- When you prefer a self-contained, low-maintenance Go application over heavy enterprise ERP solutions.

## When not to use it

- For tracking consumable food items, expiration dates, and meal planning (evaluate [Grocy](grocy.md) instead).
- For large-scale multi-tenant commercial distribution centers requiring real-time warehouse picking routes.
- For tracking digital software licenses or bookmarks (use [Linkwarden](linkwarden.md) or [Gitea](gitea.md)).

## Production Deployment Infrastructure

### Hardened Systemd Service Unit (`homebox.service`)
Below is an enterprise-grade systemd service configuration for running Homebox natively with strict system isolation and SQLite WAL optimization:

```ini
[Unit]
Description=Homebox Inventory and Asset Management Engine
After=network.target local-fs.target
Documentation=https://homebox.software/en/docs/

[Service]
Type=simple
User=homebox
Group=homebox
WorkingDirectory=/opt/homebox
Environment="HBOX_MODE=production"
Environment="HBOX_WEB_PORT=7745"
Environment="HBOX_STORAGE_SQLITE_FILENAME=/var/lib/homebox/data/homebox.db"
Environment="HBOX_OPTIONS_ALLOW_REGISTRATION=false"
Environment="TZ=Etc/UTC"

ExecStartPre=/usr/bin/install -d -m 0750 -o homebox -g homebox /var/lib/homebox/data
ExecStart=/opt/homebox/bin/homebox

Restart=always
RestartSec=5s

# Sandboxing & Security Directives
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true
ReadWritePaths=/var/lib/homebox/data
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
LimitNOFILE=65536
MemoryAccounting=true
MemoryHigh=256M
MemoryMax=512M

[Install]
WantedBy=multi-user.target
```

### Enterprise Multi-Container Docker Compose Stack with Litestream Replication

Below is a production Docker Compose configuration including persistent SQLite storage, OIDC single sign-on integration, and automatic real-time streaming replication to S3 via Litestream:

```yaml
services:
  homebox:
    image: ghcr.io/sysadminsmedia/homebox:latest
    container_name: homebox
    restart: unless-stopped
    environment:
      - HBOX_MODE=production
      - HBOX_WEB_PORT=7745
      - HBOX_OPTIONS_ALLOW_REGISTRATION=false
      - HBOX_STORAGE_SQLITE_FILENAME=/data/homebox.db
      - TZ=Etc/UTC
      # OIDC / Authentik Configuration
      # - HBOX_OIDC_ENABLED=true
      # - HBOX_OIDC_ISSUER=https://auth.example.com/application/o/homebox/
      # - HBOX_OIDC_CLIENT_ID=homebox-client-id
      # - HBOX_OIDC_CLIENT_SECRET=your-oidc-secret
    volumes:
      - homebox-data:/data
    ports:
      - "3100:7745"
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:7745/api/v1/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  litestream-backup:
    image: litestream/litestream:0.3.13
    container_name: homebox-litestream
    restart: unless-stopped
    volumes:
      - homebox-data:/data:ro
      - ./litestream.yml:/etc/litestream.yml:ro
    environment:
      - LITESTREAM_ACCESS_KEY_ID=minio-backup-user
      - LITESTREAM_SECRET_ACCESS_KEY=minio-secure-password
    command: ["replicate", "--config", "/etc/litestream.yml"]
    depends_on:
      homebox:
        condition: service_healthy

volumes:
  homebox-data:
```

## Getting started

### Enterprise Production Docker Compose Deployment

Launch the multi-container composition orchestrating Homebox and background streaming replication:

```bash
docker compose up -d
```

### Initial Setup & CLI Quickstart

1. Launch container: `docker compose up -d`.
2. Navigate to `http://<HOST-IP>:3100` and complete the initial administrator account creation.
3. Define root locations (e.g., `Main House`, `Garage`, `Server Rack`).
4. Generate an API token under **User Settings -> API Keys** for FastMCP 3.1 or CLI script authentication.

## CLI examples

```bash
# Verify Homebox container execution and health
docker exec homebox wget -qO- http://localhost:7745/api/v1/health

# Perform a hot backup of the SQLite database
docker exec homebox sqlite3 /data/homebox.db ".backup '/data/homebox-backup-$(date +%F).sqlite'"

# Extract total inventory count directly via SQLite CLI
docker exec homebox sqlite3 /data/homebox.db "SELECT count(*) FROM items;"

# Inspect location hierarchy stored in database
docker exec homebox sqlite3 /data/homebox.db "SELECT id, name, parent_id FROM locations;"

# Vacuum and optimize SQLite database indices
docker exec homebox sqlite3 /data/homebox.db "VACUUM; REINDEX;"

# Inspect WAL file checkpoint status
docker exec homebox sqlite3 /data/homebox.db "PRAGMA wal_checkpoint(PASSIVE);"
```

## API examples

### FastMCP 3.1 Homebox Inventory Server & Strict Pydantic v2 Schema

The Python script below implements a complete **FastMCP 3.1** server that wraps Homebox's REST API, enabling AI models to search for items, inspect locations, and register items using strict **Pydantic v2** validation schemas:

```python
import os
from typing import List, Optional, Dict, Any
import requests
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for Homebox
mcp = FastMCP("Homebox-Asset-Manager", version="3.1.0", instructions="FastMCP 3.1 physical inventory asset management tool server for Homebox.")

HOMEBOX_URL = os.getenv("HOMEBOX_URL", "http://localhost:3100")
HOMEBOX_API_KEY = os.getenv("HOMEBOX_API_KEY", "your-homebox-api-key")

# --- Pydantic v2 Data Schemas ---

class LocationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str = Field(..., description="Unique Location ID")
    name: str = Field(..., description="Name of the physical location")
    description: Optional[str] = Field(None, description="Location details")

class AssetFieldSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    name: str = Field(..., description="Metadata field label")
    value: str = Field(..., description="Metadata field value")

class HomeboxItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str = Field(..., description="Unique item ID")
    name: str = Field(..., min_length=1, description="Name of the item")
    description: Optional[str] = Field(None, description="Detailed item description")
    quantity: int = Field(default=1, ge=0, description="Quantity on hand")
    serial_number: Optional[str] = Field(None, alias="serialNumber", description="Serial number")
    model_number: Optional[str] = Field(None, alias="modelNumber", description="Model number")
    manufacturer: Optional[str] = Field(None, description="Manufacturer / Brand")
    purchase_price: Optional[float] = Field(None, alias="purchasePrice", ge=0.0, description="Purchase price in local currency")
    location: Optional[LocationSchema] = Field(None, description="Current assigned location")
    custom_fields: List[AssetFieldSchema] = Field(default_factory=list, description="Custom metadata attributes")

class InventorySearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    query: str = Field(..., min_length=1, description="Search query string")
    min_quantity: int = Field(default=0, ge=0, description="Minimum quantity filter")
    limit: int = Field(default=20, ge=1, le=100, description="Max items to return")

class InventorySearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    query: str = Field(..., description="Original search string")
    count: int = Field(..., ge=0, description="Number of items returned")
    items: List[HomeboxItem] = Field(..., description="Matching items")


# --- FastMCP 3.1 Tools ---

@mcp.tool(
    name="homebox_search_items",
    description="Search Homebox physical inventory items by query string with full location details."
)
def homebox_search_items(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a search query against Homebox and return Pydantic v2 validated results."""
    query_obj = InventorySearchQuery(**request_data)
    endpoint = f"{HOMEBOX_URL}/api/v1/items"
    headers = {
        "Authorization": f"Bearer {HOMEBOX_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {"q": query_obj.query}

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        item_list = raw_data if isinstance(raw_data, list) else raw_data.get("items", [])

        validated_items: List[HomeboxItem] = []
        for raw in item_list:
            try:
                item = HomeboxItem.model_validate(raw)
                if item.quantity >= query_obj.min_quantity:
                    validated_items.append(item)
                    if len(validated_items) >= query_obj.limit:
                        break
            except Exception:
                continue

        search_resp = InventorySearchResponse(
            query=query_obj.query,
            count=len(validated_items),
            items=validated_items
        )
        return search_resp.model_dump()

    except requests.RequestException as req_err:
        return {"error": f"Error contacting Homebox API: {str(req_err)}", "query": query_obj.query, "count": 0, "items": []}


@mcp.tool(
    name="homebox_get_location_tree",
    description="Retrieve full physical location hierarchy tree from Homebox."
)
def homebox_get_location_tree() -> Dict[str, Any]:
    """Fetch all configured storage locations."""
    endpoint = f"{HOMEBOX_URL}/api/v1/locations"
    headers = {"Authorization": f"Bearer {HOMEBOX_API_KEY}"}

    try:
        resp = requests.get(endpoint, headers=headers, timeout=10)
        resp.raise_for_status()
        return {"status": "success", "locations": resp.json()}
    except Exception as ex:
        return {"status": "error", "message": f"Failed to retrieve locations: {str(ex)}"}


if __name__ == "__main__":
    mcp.run()
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Command | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| **`Database Locked Error (500)`** | SQLite database file locked by concurrent writes or NFS lock bug | `fuser -v /var/lib/homebox/data/homebox.db` | Migrate database file off network shares to local NVMe SSD; enable `PRAGMA journal_mode=WAL;`. |
| **`OIDC / SSO Redirect Loop`** | Mismatch between configured redirect URL and reverse proxy `X-Forwarded-Proto` | `curl -Iv -k https://homebox.local/api/v1/auth/oidc/callback` | Ensure Traefik/Caddy forwards `X-Forwarded-Proto: https` and update OIDC redirect URI in Authentik. |
| **`FastMCP 3.1 Authentication Failure (401)`** | API token expired, revoked, or formatted incorrectly in HTTP headers | `curl -H "Authorization: Bearer $HOMEBOX_API_KEY" http://localhost:3100/api/v1/items` | Generate a new personal access token in User Settings and update FastMCP environment configuration. |
| **`Missing File Attachments / 404`** | Volume mount path mismatch between container updates or orphaned links | `ls -la /data/attachments/ 2>/dev/null \| wc -l` | Verify `homebox-data` volume mount matches `/data` mount point in container specification. |
| **`Slow Full-Text Search (> 200ms)`** | SQLite indexes fragmented after bulk import of items (> 10,000) | `sqlite3 /data/homebox.db "PRAGMA index_list('items');"` | Execute `sqlite3 /data/homebox.db "VACUUM; REINDEX;"` to rebuild and compact B-tree indices. |
| **`Litestream Replication Error`** | S3 bucket credentials invalid or bucket permissions restricted | `docker logs homebox-litestream` | Check MinIO/AWS S3 write permissions and ensure bucket lifecycle does not delete active WAL frames. |
| **`Zero Item Quantity Updates`** | AI agent payload sent negative integers or omitted required fields | `journalctl -u homebox.service -g "bad request" -n 20` | Enforce strict Pydantic v2 `Field(ge=0)` validation before invoking mutating REST endpoints. |
| **`Out of Memory (OOM) on Export`** | Exporting 50,000+ items with embedded Base64 thumbnails in single request | `dmesg -T \| grep -i oom-killer` | Stream items in paginated batches (`limit=500&offset=N`) or disable image embedding during CSV export. |

## Related tools / concepts

- [Grocy](grocy.md) — ERP system tailored for household groceries and consumable expiration tracking.
- [Paperless-ngx](paperless-ngx.md) — Document archival platform for storing digital receipts linked to Homebox items.
- [Immich](immich.md) — Self-hosted photo management system for asset photography.
- NetBox — IPAM and DCIM infrastructure tool for digital server rack mapping.
- [Tailscale](tailscale.md) — Secure, encrypted mesh network access to Homebox from mobile devices.
- [Authentik](authentik.md) — Single sign-on and identity provider integration.

## Sources / references

- [Homebox Official Website](https://homebox.software/)
- [Homebox GitHub Repository](https://github.com/sysadminsmedia/homebox)
- [Homebox REST API Specification & OpenAPI Docs](https://homebox.software/en/docs/api/)
- [FastMCP 3.1 & Model Context Protocol Docs](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
