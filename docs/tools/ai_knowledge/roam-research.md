# Roam Research

## What it is
Roam Research is a web-based "note-taking tool for networked thought" that pioneered block-level bi-directional linking and non-hierarchical knowledge graph management. Unlike traditional document-centric note applications that organize text into static nested folders, Roam treats every paragraph or list item as an independent, uniquely identified data node (a "block"). These blocks can be referenced, transcluded, and queried across arbitrary pages and graphs using Datomic Datalog query semantics.

As of **early January 2027**, Roam Research graph databases serve as personal and organizational knowledge graphs that connect directly to frontier AI models (**Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**) via **FastMCP 3.1 Task Protocol** server endpoints. This enables autonomous reasoning agents to traverse multi-layered thought graphs, perform multi-hop semantic retrieval, and write back structured research summaries.

```
+-----------------------------------------------------------------------------------+
|                        ROAM RESEARCH BI-DIRECTIONAL GRAPH ARCHITECTURE            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Daily Notes Entry ]            [ Project Page ]           [ Concept Node ]     |
|  - [[Project Alpha]] update       - #Research-Topic          - [[Machine Learning]]
|  - Block ((uid-101))              - Block ((uid-102))        - Block ((uid-103))  |
|            |                              |                          |            |
|            +------------------------------+--------------------------+            |
|                                           |                                       |
|                                           v                                       |
|  +-----------------------------------------------------------------------------+  |
|  |                 DATOMIC IN-MEMORY ATOM & BLOCK GRAPH STORE                  |  |
|  | - Datalog Query Engine (EDN Graph Queries)                                 |  |
|  | - Unique 9-Character Block UIDs & Transclusion Mapping                      |  |
|  | - Bi-Directional Reference Matrix & Unlinked Reference Discovery          |  |
|  +-----------------------------------------------------------------------------+  |
|                                           |                                       |
|                                           v                                       |
|  +-----------------------------------------------------------------------------+  |
|  |                 ROAM ALPHA REST API / WEBSOCKET PROTOCOL                    |  |
|  | - /v1/alpha/graph/{graph_name}/q (Datalog Query Execution)                 |  |
|  | - /v1/alpha/graph/{graph_name}/write (Batch Mutation Protocol)             |  |
|  +-----------------------------------------------------------------------------+  |
|                                           |                                       |
|                                           v                                       |
|  +-----------------------------------------------------------------------------+  |
|  |                   FASTMCP 3.1 GRAPH TOOL SERVER GATEWAY                    |  |
|  | - FastMCP 3.1 Task Protocol Tool Registration                               |  |
|  | - Grounded RAG Extraction & Agentic Multi-Hop Graph Traversal               |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional folder-based knowledge management forces information into rigid, artificial hierarchies. Users must decide "where a note belongs" before knowing how it will relate to future ideas. This leads to context fragmentation and hidden information silos.

Roam Research solves these structural issues:
1. **Frictionless Ingestion**: Information is captured in "Daily Notes" without requiring folder decisions. Connections emerge naturally through `[[links]]` and `#tags`.
2. **Context Preservation (Bi-Directional References)**: Linking Page A to Page B automatically registers a backlink on Page B showing the exact block context where Page A was mentioned.
3. **Block Transclusion & Zero-Duplication**: Any block can be embedded in multiple pages using its 9-character UID `((block-uid))`. Edits made to the source block update across all embedded locations instantly.
4. **Agentic Knowledge Interoperability**: Exposing graph structures via Datalog allows AI agents to execute relational and graph queries across years of structured notes.

## Where it fits in the stack
**Personal & Team Knowledge Graph Layer**. Roam operates as an unstructured/semi-structured personal knowledge management (PKM) engine that connects user notes with AI reasoning workflows via FastMCP 3.1 tool gateways.

```
+-----------------------------------------------------------------------------------+
|                                ENTERPRISE STACK POSITION                          |
+-----------------------------------------------------------------------------------+
|  [ AI Coding Agents (Cursor) ]     [ Roam Web UI ]     [ Multi-Agent Systems ]    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        ROAM FASTMCP 3.1 GATEWAY & API                             |
|          (Datalog Query Engine | REST Write API | Block Transclusions)            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                      DATOMIC GRAPH STORAGE & GRAPH BACKUPS                        |
|   [ Encrypted Graph Cloud ]   [ Local EDN / JSON Exports ]   [ Git Mirroring ]   |
+-----------------------------------------------------------------------------------+
```

## Feature Matrix & Knowledge Management Comparison

| Feature / Metric | Roam Research | Obsidian | Logseq | Notion AI |
| :--- | :--- | :--- | :--- | :--- |
| **Data Storage Engine** | Datomic Graph (Cloud/EDN)| Local Plain Markdown | Local Plain Markdown / EDN| Proprietary Cloud Relational|
| **Granularity** | First-Class Block (UIDs) | Page-Level (Block ID Anchor)| First-Class Block (UIDs)| Page / Block Mixed |
| **Query Engine** | Datalog / EDN Engine | Dataview Plugin (JS/SQL) | Datalog / Advanced Queries| Natural Language AI Search |
| **Bi-Directional Linking** | Native & Automatic | Native | Native | Inline Mention Links |
| **FastMCP 3.1 Tools** | Supported via API Server | Local MCP Gateway Plugin | Community Plugin Gateway | Notion API Gateway |
| **Offline First** | Offline Caching (Sync) | Native Local Files | Native Local Files | Cloud Dependent |

## Typical use cases
- **Multi-Hop Research Synthesis**: Connecting quotes, papers, and ideas across years of research to surface non-obvious thesis insights.
- **Agentic Knowledge Base Traversal**: Exposing graph blocks via FastMCP 3.1 so LLM agents can query project history, open tasks, and technical specifications.
- **Interactive Daily Logging & Task Tracking**: Using Daily Notes as a catch-all stream with embedded `{{[[TODO]]}}` checkboxes and dynamic Datalog queries.
- **Architectural Decision Tracking (ADRs)**: Tagging system design patterns and component dependencies with bi-directional references to pull requests and Jira IDs.

## Strengths
- **First-Class Block Granularity**: Uniquely identifies every paragraph/list item with a 9-character UID, allowing block-level referencing and transclusion.
- **Datalog Query Engine**: Provides expressive Datalog/EDN query capabilities to filter graph relationships and nested block properties dynamically.
- **Frictionless Daily Notes Workflow**: Eliminates manual organizational friction by centering input around Daily Notes pages.
- **Extensible Roam/js Ecosystem**: Supports rich client-side JavaScript extensions, custom UI controls, and API sync plugins.

## Limitations
- **Proprietary Cloud Backing**: Graph data resides on Roam's cloud servers (though client-side encrypted graphs and backups are supported).
- **Scale Lag on Large Graphs**: Graphs exceeding 50,000+ blocks can experience client-side rendering lag during graph-wide searches.
- **Proprietary SaaS Cost**: Requires a paid subscription ($15/month or $180/year) for ongoing graph access.

## When to use it
- When you prioritize discovering non-obvious connections between research ideas over rigid folder taxonomies.
- When you need block-level transclusion and bi-directional linking across complex multi-project research.
- When exposing a personal knowledge graph to autonomous FastMCP 3.1 agents for contextual querying.

## When not to use it
- When you require a strictly local-first, plain-markdown file-based workflow (use [Obsidian](./obsidian.md) or [Logseq](./logseq.md) instead).
- When looking for a completely free, open-source personal note-taking application.
- When building a structured relational database application with complex field types (use [Notion AI](./notion-ai.md) instead).

## Systemd Automated Graph Backup Configuration

To ensure continuous local data ownership and prevent data loss, a systemd timer can execute `roam-to-git` automated backups every 6 hours.

### Service Unit (`roam-backup.service`)
```ini
[Unit]
Description=Roam Research Graph Mirror Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=roam-backup
Group=roam-backup
WorkingDirectory=/var/backups/roam
EnvironmentFile=/etc/roam/roam.env
ExecStart=/usr/bin/npx roam-to-git /var/backups/roam/graph_data --graph ${ROAM_GRAPH_NAME} --developer-token ${ROAM_API_TOKEN}
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Timer Unit (`roam-backup.timer`)
```ini
[Unit]
Description=Timer for Roam Research Graph Automated Backups

[Timer]
OnCalendar=*-*-* 00/6:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## Getting started

### Account & Graph Setup
Access Roam Research via web browser or Desktop application at `https://roamresearch.com`.

### Core Syntax Overview
- `[[Page Name]]`: Creates or links to a page.
- `#Tag`: Creates or links to a page (shorthand for `[[Tag]]`).
- `((Block ID))`: References a specific block by its 9-character UID.
- `{{[[TODO]]}}`: Inserts an interactive checkbox.

## Advanced Datalog Querying

Roam allows executing raw Datalog EDN queries against its Datomic graph backend. The following query finds all unresolved TODO blocks tagged with `#Project-Alpha`:

```clojure
[:find (pull ?b [:block/uid :block/string :create/time])
 :where
 [?p :node/title "Project-Alpha"]
 [?b :block/refs ?p]
 [?b :block/string ?str]
 [(clojure.string/includes? ?str "{{[[TODO]]}}")]]
```

## CLI examples

### Automated Graph Mirroring with `roam-to-git`
```bash
#!/usr/bin/env bash
# Export Roam Research graph to local Markdown and JSON Git repository
set -euo pipefail

GRAPH_NAME="${ROAM_GRAPH_NAME:?Error: ROAM_GRAPH_NAME environment variable required}"
ROAM_API_TOKEN="${ROAM_API_TOKEN:?Error: ROAM_API_TOKEN environment variable required}"
BACKUP_DIR="./roam_graph_backups"

mkdir -p "${BACKUP_DIR}"

npx roam-to-git "${BACKUP_DIR}" \
  --graph "${GRAPH_NAME}" \
  --developer-token "${ROAM_API_TOKEN}"
```

### Querying Roam REST API via Curl
```bash
# Execute Datalog query via HTTP API
curl -X POST "https://api.roamresearch.com/v1/alpha/graph/${ROAM_GRAPH_NAME}/q" \
  -H "Authorization: Bearer ${ROAM_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "[:find ?title :where [?e :node/title ?title]]"
  }'
```

## API examples

### Python SDK with Pydantic v2 & FastMCP 3.1 Server Integration
The following code snippet demonstrates implementing a FastMCP 3.1 server with Pydantic v2 schemas for querying and writing blocks to Roam Research.

```python
import os
import json
import logging
import urllib.request
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RoamMCP")

# FastMCP 3.1 Server Initialization
mcp = FastMCP("Roam Research Knowledge Server")

class RoamBlockLocation(BaseModel):
    parent_uid: str = Field(..., description="UID of parent page or block (e.g., '01-07-2027' or 9-char UID)")
    order: int = Field(0, ge=0, description="Index position where the block should be inserted")

class RoamBlockContent(BaseModel):
    string: str = Field(..., min_length=1, description="Textual content of the block")

class RoamWriteRequest(BaseModel):
    action: str = Field("create-block", description="Roam API action type")
    location: RoamBlockLocation
    block: RoamBlockContent

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        allowed = ["create-block", "update-block", "delete-block"]
        if v not in allowed:
            raise ValueError(f"Action must be one of {allowed}")
        return v

class RoamClient:
    def __init__(self, graph_name: Optional[str] = None, api_token: Optional[str] = None):
        self.graph_name = graph_name or os.getenv("ROAM_GRAPH_NAME", "my-research-graph")
        self.api_token = api_token or os.getenv("ROAM_API_TOKEN", "")

    def write_block(self, parent_uid: str, text: str) -> bool:
        if not self.api_token or self.api_token == "mock_token":
            logger.info(f"[MOCK] Writing block to parent '{parent_uid}': {text[:30]}...")
            return True

        url = f"https://api.roamresearch.com/v1/alpha/graph/{self.graph_name}/write"
        headers = {"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/json"}
        payload = {
            "action": "create-block",
            "location": {"parent-uid": parent_uid, "order": 0},
            "block": {"string": text}
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15.0) as response:
                return response.status in (200, 204)
        except Exception as e:
            logger.error(f"Error writing to Roam: {e}")
            return False

client = RoamClient()

@mcp.tool()
async def append_roam_note(parent_page_uid: str, content: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Append a new block to a page or block UID in Roam Research via validated parameters."""
    if ctx:
        await ctx.info(f"Appending note to parent UID '{parent_page_uid}'...")

    try:
        req = RoamWriteRequest(
            location=RoamBlockLocation(parent_uid=parent_page_uid, order=0),
            block=RoamBlockContent(string=content)
        )
        success = client.write_block(parent_uid=req.location.parent_uid, text=req.block.string)
        return {
            "status": "success" if success else "failed",
            "parent_uid": req.location.parent_uid,
            "characters_written": len(req.block.string)
        }
    except ValidationError as ve:
        return {"status": "error", "message": str(ve)}

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Diagnostic Method | Remediation Action |
| :--- | :--- | :--- | :--- |
| **HTTP 429 Rate Limit Exceeded** | Batch script exceeding Roam API mutation velocity limits | Inspect response header `Retry-After` | Implement exponential backoff in python `RoamClient` wrapper |
| **HTTP 400 Invalid Block UID** | Targeted parent block UID does not exist in target graph | Check block UID length (must be 9 characters or valid page title) | Query page title via `/q` endpoint to retrieve actual UID before write |
| **Datalog Query Parse Error** | Invalid EDN syntax in `/q` endpoint payload | Validate EDN query structure using Clojure parser | Ensure vectors `[]` and symbols `?variable` are correctly formatted |
| **Sync Conflict in Daily Notes** | Concurrent write by human user and FastMCP agent to same index | Inspect client revision logs in Roam Web UI | Append blocks with `order: -1` (end of list) rather than fixed order 0 |
| **Client Render Lag** | Graph size over 50k blocks causing browser heap exhaustion | Open Chrome DevTools Performance Profiler | Re-index graph and filter out stale transclusion links |

## Related tools / concepts
- [Logseq](./logseq.md)
- [Obsidian](./obsidian.md)
- [Joplin](./joplin.md)
- [Notion AI](./notion-ai.md)
- [SilverBullet](../intake_storage/silverbullet.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Roam Research Official Site](https://roamresearch.com/)
- [Roam Research Developer API Documentation](https://developer.roamresearch.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
