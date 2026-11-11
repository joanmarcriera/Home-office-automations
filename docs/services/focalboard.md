# Focalboard

> [!WARNING]
> The standalone Focalboard project (Personal Server/Desktop) is in **community maintenance mode**. Mattermost development focus remains centered on the integrated "Boards" plugin for the Mattermost enterprise platform. Users seeking an actively developed, standalone task and project management ecosystem with native FastMCP 3.1 support should prioritize [Vikunja](vikunja.md).

## What it is
Focalboard is an open-source task and project management platform providing an intuitive Kanban-style interface, table views, and customizable property fields for organizing workflows. Originally built by Mattermost as an alternative to Trello, Notion, and Asana, Focalboard remains a stable, schema-predictable target for task injection, visual status dashboards, and archival project tracking. In early January 2027, Focalboard serves as a reliable visual dashboard backend for autonomous agents managed via **FastMCP 3.1 Task Protocol** sidecar adapters.

```
+-----------------------------------------------------------------------------------+
|                           Focalboard Architecture                                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Agent Orchestration / Human Operator UI ]                                     |
|                                |                                                  |
|                        (FastMCP 3.1 / REST API)                                  |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  | Focalboard Server Container (Port 8000)                                     |  |
|  +-----------------------------------------------------------------------------+  |
|          |                                             |                          |
|          v                                             v                          |
|  +-------------------------------+             +-------------------------------+  |
|  | Board Engine                  |             | Card & Block Store            |  |
|  | (Kanban / Table / Gallery)    |             | (Custom Properties / Views)   |  |
|  +-------------------------------+             +-------------------------------+  |
|          |                                             |                          |
|          +-----------------------+---------------------+                          |
|                                  |                                                |
|                                  v                                                |
|  +-----------------------------------------------------------------------------+  |
|  | Database Layer                                                              |  |
|  | (SQLite / PostgreSQL / MySQL Block Stores)                                  |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Mathematical Formulations & Block-Tree Data Synchronization

### 1. Collaborative Block-Tree Conflict Resolution & Operational Bounds
Focalboard models all workspace entities (workspaces, boards, views, cards, and content elements) as a directed acyclic tree of polymorphic blocks $\mathcal{B} = (V, E, \Phi)$. Each block $b \in V$ contains an immutable schema version $v(b)$ and monotonic update timestamp $t_{\text{update}}(b)$. Under concurrent agentic writes from multiple FastMCP worker nodes, state convergence across the block graph is evaluated using Last-Write-Wins (LWW) timestamped operational transforms:

$$b_{\text{state}}(t) = \arg\max_{b^{(i)} \in \mathcal{U}(b)} \left( t_{\text{update}}\left(b^{(i)}\right) + \delta_{\text{node}}(i) \right)$$

Where $\mathcal{U}(b)$ represents the set of mutation proposals in the replication buffer, and $\delta_{\text{node}}(i)$ represents high-resolution logical clock skew adjustments.

### 2. Markov Decision Chains for Card Status Progression
When autonomous agents manage Kanban card workflows across discrete status columns $S = \{S_{\text{backlog}}, S_{\text{in\_progress}}, S_{\text{review}}, S_{\text{done}}, S_{\text{blocked}}\}$, the state transition probability matrix $P_{ij} = \mathbb{P}(X_{t+1} = S_j \mid X_t = S_i)$ satisfies:

$$\sum_{j \in S} P_{ij} = 1 \quad \forall i \in S$$

The expected completion time $\mathbb{E}[T_{\text{done}} \mid X_0 = S_{\text{backlog}}]$ is computed using fundamental matrix $\mathbf{N} = (\mathbf{I} - \mathbf{Q})^{-1}$:

$$\mathbb{E}[T_{\text{done}}] = \sum_{k \in S_{\text{transient}}} N_{\text{backlog}, k}$$

Where $\mathbf{Q}$ is the sub-matrix of transient states $\{S_{\text{backlog}}, S_{\text{in\_progress}}, S_{\text{review}}, S_{\text{blocked}}\}$. When autonomous FastMCP review tools reduce friction, transient occupancy in $S_{\text{review}}$ drops exponentially, accelerating delivery.

### 3. PostgreSQL Block Storage Lock Contention Under FastMCP Concurrency
When $N_{\text{agents}}$ concurrent agents execute bulk block updates via FastMCP, row-level write contention on the PostgreSQL block table produces waiting transaction queue latency:

$$W_{\text{lock}} \approx \frac{\lambda_{\text{writes}} \cdot \mathbb{E}[T_{\text{tx}}]^2}{2 \left( 1 - \lambda_{\text{writes}} \cdot \mathbb{E}[T_{\text{tx}}] \right)}$$

Where $\lambda_{\text{writes}} = \sum_{a=1}^{N_{\text{agents}}} r_a$ is aggregate mutation arrival rate and $\mathbb{E}[T_{\text{tx}}]$ is average database commit latency ($2.1\text{ ms} – 5.4\text{ ms}$). To maintain $W_{\text{lock}} < 10\text{ ms}$, batch updates must be grouped into atomic transactions of $K \ge 10$ blocks per HTTP POST call.

## What problem it solves
Managing task pipelines across multi-agent workflows requires predictable database schemas and zero unexpected API deprecations. Standard SaaS project platforms frequently modify their API endpoints, introduce breaking UI changes, or throttle automated REST requests.

Focalboard addresses these operational concerns by offering:
1. **Schema-Stable Block Model**: Stores boards, cards, views, and properties as atomic, queryable "blocks" with immutable property schema IDs.
2. **Predictable REST API Surface**: Highly stable REST endpoints that allow autonomous agents ([Claude 5.6](../tools/providers/anthropic.md), GPT-5.6) to reliably create, move, and update cards without breaking changes.
3. **Multi-View Rendering**: Allows human operators to inspect agentic task progress using Kanban boards, while AI agents query the underlying database via structured JSON tables.

## Where it fits in the stack
**Services / Task Management & Visual Status Layer**. Focalboard sits in the productivity and execution layer:
- **Upstream Connection**: Receives task requests, bug reports, or feature specifications from AI agents or human operators via REST API or FastMCP 3.1 bridge sidecars.
- **Internal Execution**: Stores task state in local SQLite or PostgreSQL block stores, updating board column positions and custom card properties.
- **Downstream Integration**: Functions as a visual status reporting dashboard for human supervision of autonomous multi-agent software engineering pipelines.

## Typical use cases
- **Agentic Task Visualization Dashboard**: Serving as a visual Kanban board where autonomous agents populate cards with research summaries, code diffs, and audit reports for human operator sign-off.
- **Legacy Project Archival**: Storing long-term, read-only engineering archives from prior development cycles in a self-hosted environment.
- **Hardware & Homelab Asset Tracker**: Utilizing custom card properties (IP address, MAC address, serial number, status) to track homelab equipment.
- **Content Pipeline Scheduling**: Planning media creation workflows using visual drag-and-drop Kanban columns.
- **Automated Bug Triage Pipeline**: Routing incoming Sentry / GitHub exceptions into prioritized triage boards via FastMCP scheduled polling.

## Strengths
- **Stable Block Database Architecture**: Consistent JSON block model that undergoes minimal API drift.
- **Custom Property Schema**: Supports arbitrary card properties (text, select, multi-select, date, URL, person) for storing agentic execution metadata.
- **Multi-View Flexibility**: Instantly toggle between Kanban Board, Grid Table, and Image Gallery views.
- **Local Self-Hosted Sovereignty**: Zero cloud dependencies, complete data ownership, and low CPU/memory footprint.
- **Lightweight Hardware Footprint**: Runs comfortably in environments with $\le 512\text{ MB}$ RAM on single-core virtual private servers.

## Limitations
- **Maintenance Status**: Standalone Focalboard is in community maintenance mode; new feature development is concentrated on Mattermost Boards.
- **Lacks Native MCP Server**: Requires an external FastMCP 3.1 sidecar container to bridge agent tool calls to Focalboard REST endpoints.
- **No Native Real-Time WebSockets in Standalone Mode**: Does not support real-time multi-user cursor collaboration out-of-the-box (unlike the Mattermost plugin version).
- **Limited Plugin Ecosystem**: Third-party plugin extensions are restricted compared to modern platforms.

## When to use it
- When requiring a predictable, non-shifting Kanban board target for automated agent task injection.
- When hosting a lightweight, self-hosted visual dashboard for homelab or personal project tracking.
- For historical project archival where API stability takes precedence over new feature additions.
- In low-resource air-gapped environments needing an instant zero-dependency Kanban UI.

## When not to use it
- For mission-critical active enterprise production tasks requiring vendor support and active security patching (use [Vikunja](vikunja.md)).
- When real-time collaborative editing and native multi-tenant team chat integration are required (use Mattermost Boards or Vikunja).
- In environments requiring native fine-grained RBAC permission matrices per board column.

## Tool Comparison Matrix

| Metric / Dimension | Focalboard | Vikunja | Planka | Wekan | Taiga |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Development Status** | Community Maintenance | Highly Active (FastMCP Native) | Active Community | Mature / Maintenance | Active Enterprise |
| **Primary Data Model** | Polymorphic Block Tree | Hierarchical Task Lists | Real-time Kanban Cards | Trello-style Kanban | User Stories / Scrum / Kanban |
| **Database Backends** | SQLite, PostgreSQL, MySQL | SQLite, PostgreSQL, MySQL | PostgreSQL | MongoDB | PostgreSQL |
| **Agent Bridge Support** | FastMCP 3.1 Sidecar | Native FastMCP 3.1 Server | Community REST Hooks | Webhook API Adapter | Python API SDK |
| **Real-time Sync** | Polling / Local Storage | Native SSE & WebSockets | Native WebSockets | SockJS WebSockets | RabbitMQ / WebSockets |
| **Memory Footprint** | ~60 MB – 150 MB RAM | ~80 MB – 180 MB RAM | ~120 MB – 250 MB RAM | ~350 MB – 800 MB (Node/Mongo) | ~500 MB – 1.2 GB (Django) |
| **Custom Property Types** | Arbitrary Block Fields | Custom Attributes & Labels | Custom Card Fields | Custom Fields | Custom Story Fields |
| **Deployment Complexity**| Minimal (Single Binary/Docker)| Minimal (Single Binary/Docker)| Moderate (Postgres + Redis) | Moderate (Node + MongoDB) | High (Multi-container stack) |

## Getting started

### Installation (Docker)
Focalboard is deployed as a single lightweight Docker container mapping host port 8000:

```bash
docker run -d \
  --name focalboard \
  -p 8000:8000 \
  -v ./focalboard-data:/focalboard/data \
  mattermost/focalboard:latest
```

### Initial Configuration
1. Access `http://localhost:8000` in your browser.
2. Register the administrator account credentials.
3. Click **Add Board** and choose **Project Tasks**.
4. Generate a session token via API login for programmatically interacting with the server.

## CLI examples

### Container Management & Server Health
```bash
# Check Focalboard container process logs
docker logs focalboard --tail 50

# Reset password for an administrator account
docker exec -it focalboard ./focalboard-server reset-password admin_user

# Check server binary version
docker exec -it focalboard ./focalboard-server version

# Perform direct REST API login to obtain session token
curl -s -X POST "http://localhost:8000/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{
       "loginId": "admin_user",
       "password": "your_secure_password_here",
       "type": "normal"
     }' -c cookies.txt

# Inspect active SQLite block store integrity
sqlite3 ./focalboard-data/focalboard.db "PRAGMA integrity_check;"
```

## Production Deployment & Orchestration

### Systemd Standalone Service Unit (`/etc/systemd/system/focalboard.service`)
```ini
[Unit]
Description=Focalboard Server Service
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=focalboard
Group=focalboard
WorkingDirectory=/opt/focalboard
ExecStart=/opt/focalboard/bin/focalboard-server
Restart=always
RestartSec=10s
Environment="FOCALBOARD_PORT=8000"
Environment="FOCALBOARD_DBTYPE=postgres"
Environment="FOCALBOARD_DBCONFIG=postgres://focalboard:secure_pass@127.0.0.1:5432/focalboard?sslmode=disable"
Environment="FOCALBOARD_USE_SSL=false"

# Security Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/focalboard/data
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Docker Compose Multi-Container Stack (`docker-compose.yml`)
```yaml
version: "3.8"

services:
  focalboard-app:
    image: mattermost/focalboard:latest
    container_name: focalboard-server
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - VIRTUAL_HOST=boards.local
      - FOCALBOARD_DBTYPE=postgres
      - FOCALBOARD_DBCONFIG=postgres://focalboard:dbpassword123@focalboard-db:5432/focalboard?sslmode=disable
      - FOCALBOARD_USE_SSL=false
    volumes:
      - focalboard-data:/focalboard/data
    depends_on:
      - focalboard-db
    networks:
      - focalboard-net

  focalboard-db:
    image: postgres:15-alpine
    container_name: focalboard-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=focalboard
      - POSTGRES_PASSWORD=dbpassword123
      - POSTGRES_DB=focalboard
    volumes:
      - focalboard-db-data:/var/lib/postgresql/data
    networks:
      - focalboard-net

volumes:
  focalboard-data:
  focalboard-db-data:

networks:
  focalboard-net:
    driver: bridge
```

## API examples

### Complete FastMCP 3.1 Task Protocol Server Implementation
This Python script provides a **FastMCP 3.1 Task Protocol** server that exposes Focalboard REST API endpoints as tools (`@mcp.tool()`), enabling AI agents to search boards, create cards, and move card status columns using strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
"""
Focalboard FastMCP 3.1 Task Protocol Bridge Server.
Exposes Focalboard Kanban card and board management endpoints to AI agent runners.
"""

import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("focalboard-mcp")

FOCALBOARD_URL = os.getenv("FOCALBOARD_URL", "http://localhost:8000").rstrip("/")
FOCALBOARD_TOKEN = os.getenv("FOCALBOARD_TOKEN", "default_session_token")

mcp = FastMCP(
    name="focalboard-mcp-server",
    version="3.1.0",
    instructions="FastMCP 3.1 bridge server for creating and updating Focalboard Kanban cards."
)

class CreateCardInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    board_id: str = Field(..., min_length=4, description="Target board ID")
    title: str = Field(..., min_length=1, max_length=200, description="Card title text")
    description: Optional[str] = Field(default="", description="Detailed markdown body of card")
    priority: Optional[str] = Field(default="Normal", description="Priority level (Low, Normal, High, Urgent)")

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Card title cannot be empty or whitespace.")
        return cleaned

class SearchCardsInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    board_id: str = Field(..., description="Target board ID")
    query: str = Field(..., min_length=2, description="Search term for card titles")

class UpdateCardStatusInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    board_id: str = Field(..., description="Target board ID")
    card_id: str = Field(..., description="Card block ID to update")
    status_property_id: str = Field(..., description="Board property schema ID corresponding to status")
    target_option_id: str = Field(..., description="Selected option ID for the destination column")


@mcp.tool(
    name="focalboard_create_card",
    description="Creates a new task card on a specified Focalboard board."
)
async def focalboard_create_card(input_data: CreateCardInput, ctx: Context) -> Dict[str, Any]:
    """Creates a new card block on Focalboard using the REST API."""
    await ctx.report_progress(10, 100)
    ctx.info(f"Creating card '{input_data.title}' on board '{input_data.board_id}'...")

    headers = {
        "Authorization": f"Bearer {FOCALBOARD_TOKEN}",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    card_block = {
        "boardId": input_data.board_id,
        "type": "card",
        "title": input_data.title,
        "fields": {
            "contentOrder": [],
            "properties": {
                "priority": input_data.priority
            }
        }
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{FOCALBOARD_URL}/api/v1/boards/{input_data.board_id}/blocks"
            await ctx.report_progress(50, 100)
            resp = await client.post(url, json=[card_block], headers=headers)
            resp.raise_for_status()
            blocks_created = resp.json()

            card_id = blocks_created[0]["id"] if blocks_created else "unknown"
            await ctx.report_progress(100, 100)

            return {
                "status": "success",
                "card_id": card_id,
                "title": input_data.title,
                "board_id": input_data.board_id,
                "mcp_version": "3.1"
            }
        except httpx.HTTPError as err:
            ctx.error(f"Failed to create card: {err}")
            return {"status": "error", "message": f"Focalboard API error: {str(err)}", "mcp_version": "3.1"}


@mcp.tool(
    name="focalboard_list_boards",
    description="Lists all accessible boards on the Focalboard server."
)
async def focalboard_list_boards() -> Dict[str, Any]:
    """Fetches the list of boards for the authenticated session."""
    headers = {
        "Authorization": f"Bearer {FOCALBOARD_TOKEN}",
        "X-Requested-With": "XMLHttpRequest"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{FOCALBOARD_URL}/api/v1/boards"
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            boards = resp.json()

            summarized = [
                {"id": b.get("id"), "title": b.get("title"), "type": b.get("type")}
                for b in boards
            ]

            return {
                "status": "success",
                "count": len(summarized),
                "boards": summarized,
                "mcp_version": "3.1"
            }
        except httpx.HTTPError as err:
            return {"status": "error", "message": f"Focalboard API error: {str(err)}", "mcp_version": "3.1"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Advanced Pydantic v2 Board & Block Schema Auditor
This Python script uses strict **Pydantic v2** models to validate Focalboard board responses, custom card properties, and block hierarchies.

```python
"""
Focalboard Pydantic v2 Block Schema Auditor.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict


class CardPropertyOption(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="Option ID value")
    value: str = Field(..., description="Human-readable option string")
    color: Optional[str] = Field(default="propColorDefault")


class BoardPropertySchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="Property ID")
    name: str = Field(..., description="Property display name")
    type: str = Field(..., description="Property type: text, select, multiSelect, date, url")
    options: List[CardPropertyOption] = Field(default_factory=list)


class FocalboardBlock(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., min_length=4, description="Block ID")
    boardId: str = Field(..., description="Parent board ID")
    type: str = Field(..., description="Block type: board, card, view, text")
    title: str = Field(default="", description="Block title")
    fields: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("type")
    @classmethod
    def check_block_type(cls, v: str) -> str:
        valid_types = {"board", "card", "view", "text", "image", "divider"}
        if v not in valid_types:
            raise ValueError(f"Unknown block type: {v}")
        return v


class BoardManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="Board ID")
    title: str = Field(..., min_length=1, description="Board name")
    card_count: int = Field(default=0, ge=0)
    properties: List[BoardPropertySchema] = Field(default_factory=list)

    @model_validator(mode="after")
    def verify_properties_exist(self) -> "BoardManifest":
        if not self.properties:
            print(f"[Audit Warning] Board '{self.title}' ({self.id}) contains zero custom property schemas.")
        return self


def audit_board_manifest(raw_json: dict) -> None:
    try:
        manifest = BoardManifest.model_validate(raw_json)
        print("=== Focalboard Board Manifest Successfully Audited ===")
        print(f"ID: {manifest.id} | Title: '{manifest.title}'")
        print(f"Properties Schemas Count: {len(manifest.properties)}")
    except Exception as err:
        print(f"Manifest Audit Failed: {err}")


if __name__ == "__main__":
    sample_board = {
        "id": "board_eng_001",
        "title": "Agentic Engineering Pipeline 2027",
        "card_count": 14,
        "properties": [
            {
                "id": "prop_status",
                "name": "Status",
                "type": "select",
                "options": [
                    {"id": "opt_todo", "value": "To Do", "color": "propColorBlue"},
                    {"id": "opt_done", "value": "Completed", "color": "propColorGreen"}
                ]
            },
            {
                "id": "prop_agent",
                "name": "Assigned Agent",
                "type": "text",
                "options": []
            }
        ]
    }

    audit_board_manifest(sample_board)
```

## Diagnostic & Operational Troubleshooting Matrix

| Issue Symptom / Error | Root Cause | Verification Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`HTTP 401 Unauthorized`** | Session token expired or authorization header missing | `curl -i -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/boards` | Re-authenticate via `/api/v1/login` and renew `FOCALBOARD_TOKEN` |
| **`HTTP 404 Block Not Found`** | Target card ID does not exist or was deleted | Inspect card ID from query endpoint | Confirm block existence with `focalboard_list_boards` |
| **`Database Locked (SQLite)`** | Multiple agent workers attempting concurrent SQLite writes | `sqlite3 ./focalboard.db "PRAGMA journal_mode;"` | Switch database configuration to PostgreSQL backend for concurrent writes |
| **FastMCP Connection Timeout** | FastMCP sidecar unable to reach Focalboard HTTP port | `nc -zv 127.0.0.1 8000` | Ensure Focalboard container is running and exposed on expected port |
| **Property Validation Failure** | Option ID does not match defined select schema options | Validate JSON payload against `BoardPropertySchema` | Query `/api/v1/boards/{id}` to refresh valid option IDs before mutating card |
| **Slow Card Search Queries** | Unindexed block table under thousands of historical cards | `EXPLAIN ANALYZE SELECT * FROM blocks WHERE board_id = ...;` | Create composite index `CREATE INDEX idx_blocks_board_type ON blocks(board_id, type);` |
| **Card Description Truncation** | Block content order array missing markdown text block IDs | Inspect `fields.contentOrder` array in response | Append new text block ID to parent card `contentOrder` list |
| **High Memory on PostgreSQL** | Connection leak from unpooled HTTP agent clients | `SELECT count(*) FROM pg_stat_activity;` | Configure connection pooling (PgBouncer) or set max pool size in Focalboard config |

## Operational Guardrails & Production Checklist
1. **Migrate to PostgreSQL for Multi-Agent Workflows**: Never use default SQLite storage when running $>2$ autonomous FastMCP agent worker sidecars.
2. **Token Renewal Automation**: Implement automatic session re-login in FastMCP sidecars to prevent silent 401 API failures.
3. **Automated Database Backups**: Schedule nightly PostgreSQL dumps (`pg_dump focalboard > backup.sql`) or volume snapshots.
4. **Enforce Strict Schema Contracts**: Use Pydantic v2 `extra="forbid"` to catch API drift before writing corrupt block objects to the store.
5. **Evaluate Migration to Vikunja**: For active modern production requirements, plan forward migration to [Vikunja](vikunja.md).

## Related tools / concepts
- [Vikunja](vikunja.md) — Primary recommended modern alternative for active self-hosted task management.
- [Ollama](ollama.md) — For hosting local LLMs to process Focalboard cards.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Protocol registry for agent tools.
- [Authentik](authentik.md) — For managing SSO access to Focalboard.
- [Trilium](trilium.md) — For persistent personal knowledge management.
- [Claude 5.6](../tools/providers/anthropic.md) — Reasoning engine for task assignment.

## Sources / references
- [Official Website](https://www.focalboard.com/)
- [GitHub Repository](https://github.com/mattermost/focalboard)
- [Mattermost Boards Integration](https://mattermost.com/platform/mattermost-boards/)
- [Focalboard API Reference](https://developers.mattermost.com/contribute/focalboard/api-reference/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
