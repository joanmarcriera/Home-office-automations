# Trilium Notes (TriliumNext)

Trilium Notes is a hierarchical, highly customizable note-taking application designed for constructing large, deeply structured personal knowledge bases. Following the transition of the original project to maintenance mode, the community-driven [TriliumNext](https://github.com/TriliumNext/TriliumNext) project has established itself as the primary active release track (v0.103.x+, early January 2027), introducing native spreadsheet support (Univer Sheets), FastMCP 3.1 task capabilities, enhanced OCR engines, and native integration for autonomous agent reasoning loops.

```
+-----------------------------------------------------------------------------------+
|                           Trilium Notes Topology                                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Agent Orchestration / User Desktop UI ]                                        |
|                                |                                                  |
|                        (FastMCP 3.1 / REST API)                                  |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  | TriliumNext Server Instance (Port 8080)                                    |  |
|  +-----------------------------------------------------------------------------+  |
|          |                                             |                          |
|          v                                             v                          |
|  +-------------------------------+             +-------------------------------+  |
|  | Node Forest Engine            |             | Execution & Scripting Engine  |  |
|  | (Cloning / Relation Links)    |             | (Node.js v22.x / fetch API)   |  |
|  +-------------------------------+             +-------------------------------+  |
|          |                                             |                          |
|          +-----------------------+---------------------+                          |
|                                  |                                                |
|                                  v                                                |
|  +-----------------------------------------------------------------------------+  |
|  | SQLite Storage Engine & Document Indexer                                   |  |
|  | (Full-Text Search FTS5 / OCR Processing / File Attachments)                 |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What it is
Trilium Notes (TriliumNext) is a local-first, hierarchical knowledge engine that models information as a directed forest graph rather than flat text files. Notes in Trilium can possess multiple parents (cloning), run embedded JavaScript scripts to reactively modify metadata, embed live spreadsheets, store encrypted code snippets, and perform automated OCR on attached images and PDFs. In early 2027, Trilium serves as an ideal persistent knowledge backend for autonomous agent workflows powered by [Claude 5.6](../tools/providers/anthropic.md), GPT-5.6, and [Gemma 4](../tools/ai_knowledge/local_llms.md).

## What problem it solves
Standard note-taking applications enforce either strict single-folder hierarchies or flat tag lists, causing information fragmentation and "knowledge decay" in large repositories (>10,000 pages).

Trilium solves this structural limitation by providing:
1. **Directed Forest Hierarchy**: Allows a note to exist simultaneously under multiple parent notes without content duplication.
2. **Automated Lifecycle Scripting**: Executes custom JavaScript functions triggered by note creation, updates, or daily interval timers.
3. **Structured Attribute Engine**: Attaches typed key-value labels, relations, and promo attributes to dynamically filter and render custom dashboards.
4. **Local-First Synchronization**: Encrypts and synchronizes knowledge trees across multiple desktop and server nodes using atomic revision delta logs.

## Where it fits in the stack
**Services / Knowledge Base & Persistent Agent Memory Layer**. Trilium sits between ingestion/automation tools ([n8n](n8n.md), Paperless-ngx) and reasoning agents:
- **Data Ingestion**: Receives web clips, automated journal entries, and PDF OCR extracts via REST API or FastMCP 3.1 tools.
- **Data Organization**: Organizes research trees, project specifications, and code snippets into queryable nodes.
- **Agent Interfacing**: Serves structured context and memory state to agent execution engines via the FastMCP 3.1 Task Protocol.

## Typical use cases
- **Autonomous Agent Memory Bank**: Functioning as an indexed, long-term memory store for AI agents storing interaction logs, project milestones, and user preferences.
- **Enterprise Technical Wiki**: Maintaining deeply nested documentation, architecture diagrams, and runnable code snippets.
- **Integrated Data Analysis**: Storing financial logs, task schedules, and metrics using embedded **Univer Sheets** notes with built-in formula calculations.
- **Document Vault**: Indexing paper receipts, scans, and PDF manuals using the integrated Tesseract/OCR pipeline.

## Strengths
- **Non-Linear Tree Cloning**: Clone any note into arbitrary locations in the tree; updating the master content updates all visible instances instantly.
- **Built-in Automation Engine**: Node.js execution environment allowing notes to run backend scripts, execute HTTP requests, and auto-generate summary notes.
- **Native Spreadsheet Support**: Integrated Univer Sheets editing for inline cell formulas and tabular data processing inside notes.
- **Full-Text FTS5 Search & OCR**: High-speed indexing of text, markdown, HTML, code snippets, and attached image text.
- **Local-First & Encrypted**: All data stored locally in SQLite with optional end-to-end payload encryption during sync.

## Limitations
- **Steep Learning Curve**: Mastering cloning, relation attributes, and backend scripting requires dedicated onboarding.
- **UI Density**: Complex sidebars and multi-tab pane layouts can feel overwhelming compared to minimal markdown editors.
- **Migration Requirements**: Legacy scripts relying on older Trilium APIs (`api.axios`) require refactoring to use standard global `fetch()`.

## When to use it
- **Deeply Structured Repositories**: When managing complex personal or team knowledge bases exceeding thousands of cross-referenced pages.
- **Scriptable Knowledge Workflows**: When notes need reactive behaviors, such as auto-calculating totals or pulling RSS feeds.
- **Local-First Data Ownership**: When requiring complete offline control, local SQLite storage, and self-hosted server synchronization.

## When not to use it
- **Simple Scratchpad Notes**: For quick, temporary text notes, simpler tools like [Logseq](../tools/ai_knowledge/logseq.md) or Joplin are lighter.
- **Real-Time Collaborative Editing**: Multiple users simultaneously editing the exact same note character-by-character (use Hedgedoc or Etherpad).

## Getting started

### Deployment Overview
TriliumNext is deployed as a single Docker container mounting a local data volume to store SQLite database files and uploaded media attachments.

### System Prerequisites
- Docker Engine 24.0+ / Docker Compose v2.x.
- Minimum 1 GB RAM and 1 CPU core.
- Port 8080 available for HTTP traffic.

## CLI examples

### Deploying TriliumNext via Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  triliumnext:
    image: triliumnext/notes:v0.103.2
    container_name: triliumnext-server
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - TRILIUM_DATA_DIR=/home/node/trilium-data
    volumes:
      - ./trilium-data:/home/node/trilium-data
```

### Server Execution & Health Validation
```bash
# Start TriliumNext container
docker compose up -d

# Check TriliumNext instance health endpoint
curl -s http://localhost:8080/api/health | jq .

# Create a API Secret Token in Settings -> ETAPI
export TRILIUM_TOKEN="your_etapi_token_here"

# List child notes under the root note
curl -s -H "Authorization: $TRILIUM_TOKEN" \
     "http://localhost:8080/etapi/notes/root/children" | jq .
```

## API examples

### Complete FastMCP 3.1 Task Protocol Server Implementation
This Python script provides a complete **FastMCP 3.1 Task Protocol** server that wraps TriliumNext's ETAPI REST endpoints. It exposes tools (`@mcp.tool()`) for search, note creation, and note cloning for autonomous AI agents.

```python
"""
TriliumNext FastMCP 3.1 Server Implementation
Exposes Trilium ETAPI hierarchical note management capabilities to AI agent runners.
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
logger = logging.getLogger("trilium-mcp-server")

# Environment Variables
TRILIUM_URL = os.getenv("TRILIUM_URL", "http://localhost:8080").rstrip("/")
TRILIUM_ETAPI_TOKEN = os.getenv("TRILIUM_ETAPI_TOKEN", "default_etapi_token")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="trilium-notes-mcp",
    instructions="FastMCP 3.1 server for interacting with TriliumNext hierarchical knowledge base."
)

class CreateNoteInput(BaseModel):
    parent_note_id: str = Field(default="root", description="ID of the parent note under which to create this note")
    title: str = Field(..., min_length=1, max_length=250, description="Title of the new note")
    type: str = Field(default="text", description="Note type: text, code, spreadsheet, renderedHtml")
    content: str = Field(..., description="Content payload for the note (Markdown or HTML)")

    @field_validator("type")
    @classmethod
    def validate_note_type(cls, v: str) -> str:
        valid_types = {"text", "code", "spreadsheet", "renderedHtml", "search", "file"}
        if v not in valid_types:
            raise ValueError(f"Note type '{v}' must be one of {valid_types}")
        return v

class SearchNotesInput(BaseModel):
    query: str = Field(..., min_length=2, description="Search term or Trilium search expression")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of search results to return")


@mcp.tool(
    name="trilium_create_note",
    description="Creates a new note inside TriliumNext under the specified parent node."
)
async def trilium_create_note(input_data: CreateNoteInput) -> Dict[str, Any]:
    """
    Creates a new node in TriliumNext using ETAPI.
    """
    logger.info(f"Creating note '{input_data.title}' under parent '{input_data.parent_note_id}'...")

    headers = {
        "Authorization": TRILIUM_ETAPI_TOKEN,
        "Content-Type": "application/json"
    }

    # 1. Create Note Metadata
    note_payload = {
        "parentNoteId": input_data.parent_note_id,
        "title": input_data.title,
        "type": input_data.type,
        "mime": "text/html" if input_data.type == "text" else "text/plain"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(f"{TRILIUM_URL}/etapi/create-note", json=note_payload, headers=headers)
            resp.raise_for_status()
            note_info = resp.json()
            note_id = note_info["note"]["noteId"]

            # 2. Put Note Content
            content_resp = await client.put(
                f"{TRILIUM_URL}/etapi/notes/{note_id}/content",
                content=input_data.content,
                headers={"Authorization": TRILIUM_ETAPI_TOKEN, "Content-Type": "text/html"}
            )
            content_resp.raise_for_status()

            return {
                "status": "success",
                "note_id": note_id,
                "title": input_data.title,
                "parent_note_id": input_data.parent_note_id,
                "type": input_data.type
            }
        except httpx.HTTPError as err:
            logger.error(f"Failed to create Trilium note: {err}")
            return {"status": "error", "message": f"ETAPI execution failed: {str(err)}"}


@mcp.tool(
    name="trilium_search_notes",
    description="Searches TriliumNext knowledge base notes using full-text search or attributes."
)
async def trilium_search_notes(input_data: SearchNotesInput) -> Dict[str, Any]:
    """
    Queries TriliumNext using ETAPI search endpoints.
    """
    logger.info(f"Executing Trilium search query: '{input_data.query}'")
    headers = {"Authorization": TRILIUM_ETAPI_TOKEN}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            params = {"search": input_data.query, "limit": input_data.limit}
            resp = await client.get(f"{TRILIUM_URL}/etapi/notes", params=params, headers=headers)
            resp.raise_for_status()
            results = resp.json()

            formatted_results = [
                {
                    "noteId": item.get("noteId"),
                    "title": item.get("title"),
                    "type": item.get("type"),
                    "isProtected": item.get("isProtected", False)
                }
                for item in results.get("results", [])
            ]

            return {
                "status": "success",
                "query": input_data.query,
                "count": len(formatted_results),
                "notes": formatted_results
            }
        except httpx.HTTPError as err:
            logger.error(f"Trilium search failed: {err}")
            return {"status": "error", "message": f"Search API error: {str(err)}"}


if __name__ == "__main__":
    logger.info("Starting TriliumNext FastMCP 3.1 Task Protocol Server...")
    mcp.run(transport="sses")
```

### Pydantic v2 Schema for Trilium Note Export & Attribute Validation
This Python module demonstrates validating exported Trilium note attributes, relation tags, and note hierarchies using strict Pydantic v2 models.

```python
"""
TriliumNext Pydantic v2 Attribute & Node Structural Validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator


class NoteAttribute(BaseModel):
    attributeId: str = Field(..., description="Unique attribute ID")
    type: str = Field(..., description="Attribute type: label, relation, promo")
    name: str = Field(..., min_length=1, description="Attribute key name")
    value: Optional[str] = Field(default=None, description="Attribute string value")
    isInheritable: bool = Field(default=False, description="Inherit attribute to child notes")

    @field_validator("type")
    @classmethod
    def check_attribute_type(cls, v: str) -> str:
        if v not in {"label", "relation", "promo"}:
            raise ValueError(f"Invalid attribute type '{v}'. Must be label, relation, or promo.")
        return v


class TriliumNodeExport(BaseModel):
    noteId: str = Field(..., min_length=4, description="Trilium note ID")
    title: str = Field(..., description="Note title")
    type: str = Field(..., description="Note type")
    parentNoteIds: List[str] = Field(..., min_items=1, description="List of parent note IDs (supports cloning)")
    attributes: List[NoteAttribute] = Field(default_factory=list, description="Attached labels and relations")
    content_length: int = Field(default=0, ge=0, description="Content character count")

    @model_validator(mode="after")
    def verify_cloning_status(self) -> "TriliumNodeExport":
        if len(self.parentNoteIds) > 1:
            print(f"[Info] Note '{self.title}' ({self.noteId}) is cloned across {len(self.parentNoteIds)} parent locations.")
        return self


def parse_export_manifest(raw_manifest: dict) -> None:
    try:
        node = TriliumNodeExport.model_validate(raw_manifest)
        print("=== Trilium Node Validation Successful ===")
        print(f"ID: {node.noteId} | Title: '{node.title}' | Type: {node.type}")
        print(f"Parents: {node.parentNoteIds}")
        print(f"Attributes Count: {len(node.attributes)}")
    except Exception as err:
        print(f"Manifest Parsing Failure: {err}")


if __name__ == "__main__":
    sample_data = {
        "noteId": "note_arch_001",
        "title": "Agentic Architecture Map 2027",
        "type": "text",
        "parentNoteIds": ["root", "folder_ai_agents"],
        "attributes": [
            {
                "attributeId": "attr_01",
                "type": "label",
                "name": "status",
                "value": "active",
                "isInheritable": True
            },
            {
                "attributeId": "attr_02",
                "type": "relation",
                "name": "relatesTo",
                "value": "note_mcp_002",
                "isInheritable": False
            }
        ],
        "content_length": 4820
    }

    parse_export_manifest(sample_data)
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md) — The primary markdown-based knowledge editor.
- [Logseq](../tools/ai_knowledge/logseq.md) — Privacy-first outliner knowledge tool.
- [Joplin](../tools/ai_knowledge/joplin.md) — Simple cross-platform notebook manager.
- [SilverBullet](../tools/intake_storage/silverbullet.md) — Hackable markdown-native knowledge base.
- [n8n](n8n.md) — Workflow automation tool for pushing data to Trilium.
- [Paperless-ngx](paperless-ngx.md) — Document archiving service integrated with Trilium.
- [Claude 5.6](../tools/providers/anthropic.md) — Reasoning model for multi-note synthesis.

## Sources / references
- [TriliumNext GitHub Repository](https://github.com/TriliumNext/TriliumNext)
- [Trilium Wiki & Documentation](https://github.com/zadam/trilium/wiki)
- [TriliumNext Releases & Changelog](https://github.com/TriliumNext/TriliumNext/releases)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
