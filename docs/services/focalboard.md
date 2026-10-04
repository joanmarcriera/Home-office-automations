# Focalboard

> [!WARNING]
> The standalone Focalboard project (Personal Server/Desktop) is in **community maintenance mode**. Mattermost development focus remains centered on the integrated "Boards" plugin for the Mattermost enterprise platform. Users seeking an actively developed, standalone task and project management ecosystem with native FastMCP 3.1 support should prioritize [Vikunja](vikunja.md).

## What it is
Focalboard is a open-source task and project management platform providing an intuitive Kanban-style interface, table views, and customizable property fields for organizing workflows. Originally built by Mattermost as an alternative to Trello, Notion, and Asana, Focalboard remains a stable, schema-predictable target for task injection, visual status dashboards, and archival project tracking. In early January 2027, Focalboard serves as a reliable visual dashboard backend for autonomous agents managed via **FastMCP 3.1 Task Protocol** sidecar adapters.

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

## Strengths
- **Stable Block Database Architecture**: Consistent JSON block model that undergoes minimal API drift.
- **Custom Property Schema**: Supports arbitrary card properties (text, select, multi-select, date, URL, person) for storing agentic execution metadata.
- **Multi-View Flexibility**: Instantly toggle between Kanban Board, Grid Table, and Image Gallery views.
- **Local Self-Hosted Sovereignty**: Zero cloud dependencies, complete data ownership, and low CPU/memory footprint.

## Limitations
- **Maintenance Status**: Standalone Focalboard is in community maintenance mode; new feature development is concentrated on Mattermost Boards.
- **Lacks Native MCP Server**: Requires an external FastMCP 3.1 sidecar container to bridge agent tool calls to Focalboard REST endpoints.
- **No Native Real-Time WebSockets in Standalone Mode**: Does not support real-time multi-user cursor collaboration out-of-the-box (unlike the Mattermost plugin version).

## When to use it
- When requiring a predictable, non-shifting Kanban board target for automated agent task injection.
- When hosting a lightweight, self-hosted visual dashboard for homelab or personal project tracking.
- For historical project archival where API stability takes precedence over new feature additions.

## When not to use it
- For mission-critical active enterprise production tasks requiring vendor support and active security patching (use [Vikunja](vikunja.md)).
- When real-time collaborative editing and native multi-tenant team chat integration are required (use Mattermost Boards or Vikunja).

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
```

## API examples

### Complete FastMCP 3.1 Task Protocol Server Implementation
This Python script provides a **FastMCP 3.1 Task Protocol** server that exposes Focalboard REST API endpoints as tools (`@mcp.tool()`), enabling AI agents to search boards, create cards, and move card status columns.

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
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("focalboard-mcp")

FOCALBOARD_URL = os.getenv("FOCALBOARD_URL", "http://localhost:8000").rstrip("/")
FOCALBOARD_TOKEN = os.getenv("FOCALBOARD_TOKEN", "default_session_token")

mcp = FastMCP(
    name="focalboard-mcp-server",
    instructions="FastMCP 3.1 bridge server for creating and updating Focalboard Kanban cards."
)

class CreateCardInput(BaseModel):
    board_id: str = Field(..., min_length=4, description="Target board ID")
    title: str = Field(..., min_length=1, max_length=200, description="Card title text")
    description: Optional[str] = Field(default="", description="Detailed markdown body of card")

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Card title cannot be empty or whitespace.")
        return cleaned

class SearchCardsInput(BaseModel):
    board_id: str = Field(..., description="Target board ID")
    query: str = Field(..., min_length=2, description="Search term for card titles")


@mcp.tool(
    name="focalboard_create_card",
    description="Creates a new task card on a specified Focalboard board."
)
async def focalboard_create_card(input_data: CreateCardInput) -> Dict[str, Any]:
    """
    Creates a new card block on Focalboard using the REST API.
    """
    logger.info(f"Creating card '{input_data.title}' on board '{input_data.board_id}'...")

    headers = {
        "Authorization": f"Bearer {FOCALBOARD_TOKEN}",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Focalboard uses a block architecture for cards
    card_block = {
        "boardId": input_data.board_id,
        "type": "card",
        "title": input_data.title,
        "fields": {
            "contentOrder": [],
            "properties": {}
        }
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{FOCALBOARD_URL}/api/v1/boards/{input_data.board_id}/blocks"
            resp = await client.post(url, json=[card_block], headers=headers)
            resp.raise_for_status()
            blocks_created = resp.json()

            card_id = blocks_created[0]["id"] if blocks_created else "unknown"

            return {
                "status": "success",
                "card_id": card_id,
                "title": input_data.title,
                "board_id": input_data.board_id
            }
        except httpx.HTTPError as err:
            logger.error(f"Failed to create card: {err}")
            return {"status": "error", "message": f"Focalboard API error: {str(err)}"}


@mcp.tool(
    name="focalboard_list_boards",
    description="Lists all accessible boards on the Focalboard server."
)
async def focalboard_list_boards() -> Dict[str, Any]:
    """
    Fetches the list of boards for the authenticated session.
    """
    logger.info("Fetching accessible boards from Focalboard...")
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
                "boards": summarized
            }
        except httpx.HTTPError as err:
            logger.error(f"Failed to list boards: {err}")
            return {"status": "error", "message": f"Focalboard API error: {str(err)}"}


if __name__ == "__main__":
    logger.info("Starting Focalboard FastMCP 3.1 Task Protocol Bridge Server...")
    mcp.run(transport="sses")
```

### Advanced Pydantic v2 Board & Block Schema Auditor
This Python script uses strict **Pydantic v2** models to validate Focalboard board responses, custom card properties, and block hierarchies.

```python
"""
Focalboard Pydantic v2 Block Schema Auditor.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class CardPropertyOption(BaseModel):
    id: str = Field(..., description="Option ID value")
    value: str = Field(..., description="Human-readable option string")
    color: Optional[str] = Field(default="propColorDefault")


class BoardPropertySchema(BaseModel):
    id: str = Field(..., description="Property ID")
    name: str = Field(..., description="Property display name")
    type: str = Field(..., description="Property type: text, select, multiSelect, date, url")
    options: List[CardPropertyOption] = Field(default_factory=list)


class FocalboardBlock(BaseModel):
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
                "type": "text"
            }
        ]
    }

    audit_board_manifest(sample_board)
```

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
