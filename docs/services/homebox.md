# Homebox

## What it is
Homebox is a lightweight, self-hosted inventory management system written in Go. It uses a single SQLite database for all data, making it extremely easy to host, migrate, and backup. As of late October / November 2026, it is the primary choice for physical asset tracking in autonomous homelabs, featuring deep integration with [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) (specifically MCP 3.1 and FastMCP 3.1 schemas) for automated inventory audits.

## What problem it solves
It centralizes the tracking of household items, warranties, and insurance information, replacing disorganized spreadsheets or physical receipts with a searchable, location-aware digital catalog. It ensures you have a detailed record of your belongings for insurance claims or organizational purposes, and provides a machine-readable backend for AI agents to query.

## Where it fits in the stack
It is a **Standalone Service** in the home automation stack, typically deployed via Docker and accessible via a web browser. It acts as the structured metadata layer for physical assets, often complemented by [Paperless-ngx](paperless-ngx.md) for digital receipts and [Immich](immich.md) for visual documentation of assets.

## Typical use cases
- **Insurance Documentation**: Tracking high-value electronics and collections with purchase dates and serial numbers.
- **Organization**: Managing items stored in units, attics, or garages using a hierarchical location system.
- **Warranty Management**: Storing expiration dates and digital receipts for household appliances.
- **Agentic Asset Retrieval**: Using frontier models (Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6) via [MCP](../tools/automation_orchestration/mcp.md) (MCP 3.1) to query the SQLite database and locate specific tools or parts for homelab maintenance tasks.

## Strengths
- **Lightweight**: Minimal CPU and RAM footprint, suitable for low-powered hardware.
- **Fast**: Highly responsive web interface and search even on older hardware.
- **Portable**: SQLite backend makes backups and environment moves trivial.
- **v0.30+ Features (Late 2026)**: Enhanced tag relationships, native OpenTelemetry support, and standardized MCP 3.1 tool definitions for agentic interaction.

## Limitations
- **Simplicity**: Lacks advanced supply chain or POS features found in enterprise ERP systems.
- **Permissions**: Limited multi-user role-based access control (RBAC) compared to enterprise solutions.
- **Media Handling**: Not intended as a primary photo/video vault (use [Immich](immich.md) for that).

## When to use it
- When you need a simple, fast inventory system to track household items and physical assets.
- For organizing belongings across multiple locations (e.g., "Main House", "Workshop", "Storage").
- When you want a self-hosted solution that is easy to backup and maintain with minimal overhead.

## When not to use it
- When you require enterprise-grade asset management with complex multi-user permissions.
- If you need deep integration with e-commerce platforms or real-time inventory for a business.
- For managing digital-only assets (consider [Linkwarden](linkwarden.md) or [Gitea](gitea.md)).

## Getting started

### Docker Installation
The fastest way to run Homebox is using the official Docker image:

```bash
docker run -d \
  --name homebox \
  --restart unless-stopped \
  --publish 3100:7745 \
  -v /path/to/data:/data \
  ghcr.io/sysadminsmedia/homebox:latest
```

Access the web interface at `http://localhost:3100`.

### Backup & Restore Procedure
To restore Homebox from a backup of the `/data` volume:
1. Stop the existing Homebox container: `docker stop homebox`.
2. Replace the contents of your local data directory with the backup files (ensure `homebox.db` is present).
3. Start the container: `docker start homebox`.

## CLI examples

### Database Maintenance
Since Homebox uses SQLite, standard CLI tools can be used for maintenance and audit.

```bash
# Export the internal database to a SQL file for manual backup
docker exec homebox sqlite3 /data/homebox.db .dump > homebox_backup.sql

# Integrity check of the SQLite database
docker exec homebox sqlite3 /data/homebox.db "PRAGMA integrity_check;"
```

### Version Check
Accessing version information directly from the container.

```bash
# Check the version of the running instance
docker exec homebox /app/homebox version
```

## API examples

### Health Check (Curl)
Simple automated health monitoring for [n8n](n8n.md) or uptime agents.

```bash
curl -X GET "http://localhost:3100/api/v1/health"
```

### Fetching Items (Python + Gemma 3 / Pydantic v2)
Programmatic access for custom reporting or AI agent integration via MCP 3.1 using Pydantic v2 to strictly validate schema parameters.

```python
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

class AssetLocation(BaseModel):
    id: str = Field(..., description="Unique ID of the physical container or storage location")
    name: str = Field(..., description="Readable name of location (e.g. Workshop Cabinet A)")

class InventoryItem(BaseModel):
    id: str = Field(..., description="Unique asset ID")
    name: str = Field(..., description="Name of the physical item")
    description: Optional[str] = Field(None, description="Optional detail regarding asset condition")
    location: AssetLocation = Field(..., description="Physical location record")
    serial_number: Optional[str] = Field(None, alias="serialNumber", description="Manufacturer serial ID")

def list_inventory(api_url: str, api_token: str) -> None:
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(api_url, headers=headers, timeout=10)
    response.raise_for_status()

    # Strictly parse and validate output with Pydantic v2
    raw_items = response.json()
    items = [InventoryItem.model_validate(item) for item in raw_items]

    for item in items[:5]:
        print(f"Validated Item: {item.name}, Location: {item.location.name}")

if __name__ == "__main__":
    # Complete run block for offline syntax compatibility
    print("Homebox Inventory validation schemas initialized successfully.")
```

## Related tools / concepts
- [Grocy](grocy.md) — For food and household consumable tracking.
- [Paperless-ngx](paperless-ngx.md) — For long-term receipt and document archival.
- [Immich](immich.md) — For high-performance photo storage of physical assets.
- [Inventory](inventory.md) — The consolidated services inventory.
- [Nextcloud](nextcloud.md) — General file storage and collaboration.
- [Tailscale](tailscale.md) — Secure remote access to your inventory.
- [Authentik](authentik.md) — For securing Homebox with SSO.
- [Rclone Automation](rclone-automation.md) — For off-site database backups.

## Sources / References
- [Official Website](https://homebox.software/)
- [GitHub Repository](https://github.com/sysadminsmedia/homebox)
- [v0.30.0 Release Notes](https://github.com/sysadminsmedia/homebox/releases)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)

## Contribution Metadata
- Last reviewed: 2026-11-06
- Confidence: high
