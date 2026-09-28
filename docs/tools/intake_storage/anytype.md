# AnyType

## What it is
AnyType is an open-source, decentralized, local-first personal knowledge management (PKM) workspace and sovereign data platform built on the Anysync protocol (an end-to-end encrypted peer-to-peer data synchronization network). Rather than storing documents as monolithic plain text or markdown files, AnyType represents information using an object-oriented graph model where every entity—whether a note, task, bookmark, physical asset, project, contact, or media item—is treated as a typed Object. Each Object possesses specific Relations, Views, and Schemas while remaining fully cryptographic, self-hosted, and offline-capable.

As of early 2027, AnyType serves as a cornerstone platform for **Agentic Knowledge Management** and local-first AI pipelines. Operating via a background daemon (`any-sync-node`) and exposing REST/gRPC endpoints alongside Model Context Protocol (FastMCP 3.1) integration, AnyType allows autonomous agent fleets (powered by models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL) to securely read, manipulate, index, and organize private knowledge graphs without exposing raw data to centralized cloud infrastructure or third-party aggregators.

## What problem it solves
Modern knowledge management and personal productivity tools present several major vulnerabilities and operational friction points for individuals and enterprise teams:

1. **Centralized Lock-In & Cloud Exposure**: Proprietary SaaS workspaces like Notion, Airtable, or Coda retain control over user data, expose databases to cloud outages, enforce per-seat subscription tiers, and process unencrypted sensitive content on corporate servers where it is vulnerable to sub-processors and automated training pipelines.
2. **Fragile File-Based Workspaces**: Traditional markdown file vaults (such as raw Obsidian or Logseq directories) struggle with complex relational queries, multi-property object indexing, structured database schemas, and atomic cross-device synchronization without risk of sync conflicts or external plugin fragility.
3. **Privacy Compromise in AI Workflows**: Integrating automated agentic workflows with private personal notes usually requires uploading sensitive documents to external cloud APIs, violating zero-trust organizational policies and personal privacy standards.
4. **Data Isolation & Vendor Silos**: Exporting structured databases from legacy SaaS tools often results in flattened CSVs or unlinked PDFs, destroying relational properties, bidirectional graph edges, and object history.

AnyType resolves these challenges by uniting the structured database capabilities of Notion with the privacy, cryptography, and offline speed of a sovereign local-first node. Through cryptographic key pairs, peer-to-peer Anysync protocols, and local FastMCP 3.1 agent bridges, AnyType enables local-first, agent-driven knowledge operations with zero cloud dependency.

## Where it fits in the stack
Within the KnowledgeOps and modern agentic engineering framework, AnyType functions as a **Local-First Sovereign Knowledge Engine & Agentic Vault** within the **Intake & Storage** layer.

```
+-----------------------------------------------------------------------------------+
|                            Autonomous Agent Layer                                 |
|            (Claude 5.6 / GPT-5.6 / Gemini 4.0 / Local DeepSeek-V4 / Qwen)          |
+-----------------------------------------------------------------------------------+
                                          |
                                    FastMCP 3.1 API
                                          |
+-----------------------------------------------------------------------------------+
|                        AnyType Local Node & FastMCP Server                        |
|                                (Port 31009 / REST API)                            |
+-----------------------------------------------------------------------------------+
       |                                  |                                 |
+--------------+                   +--------------+                  +--------------+
| Anysync P2P  |                   | Local SQLite |                  | Vector/Graph |
| Sync Engine  |                   | Engine & Blob|                  | Search Index |
+--------------+                   +--------------+                  +--------------+
       |                                  |                                 |
       +----------------------------------+---------------------------------+
                                          |
+-----------------------------------------------------------------------------------+
|                             Storage & Network Mesh                                |
|        (Self-Hosted any-sync-node / Docker / Local NVMe Storage / Tailscale)       |
+-----------------------------------------------------------------------------------+
```

- **Upstream Layer**: Connects to intake pipelines, web scrapers, email bridges (Fastmail/JMAP), document parsers (Docling, LlamaParse), and agent reasoning engines via the Model Context Protocol (FastMCP 3.1).
- **Internal Storage**: Maintains encrypted local storage on disk via SQLite and block-level cryptographic stores, managed locally on client hardware or headless Docker instances.
- **Downstream Sync**: Synchronizes bidirectionally across desktop (macOS, Windows, Linux) and mobile devices (iOS, Android) over direct local Wi-Fi, Tailscale mesh, or self-hosted `any-sync-node` relays.

## Typical use cases

### 1. Sovereign Knowledge Base & Agentic Second Brain
Users maintain an encrypted personal knowledge base of research papers, architectural diagrams, meeting transcripts, and code snippets. Autonomous agents use the AnyType FastMCP 3.1 server to perform semantic query retrieval, auto-tag new intake items, and assemble synthesized executive summaries directly inside AnyType Objects.

### 2. Multi-Device Relational Project Management
Teams build complex databases of projects, sprint tasks, feature requests, and system credentials. The object-oriented model allows a single "Developer" contact object to be linked simultaneously to multiple "Task" objects, "Code Commit" objects, and "Security Audit" notes across desktop and mobile devices.

### 3. Fully Offline & Air-Gapped Operations
Defense contractors, research laboratories, and privacy-conscious executives run AnyType on air-gapped laptops and isolated local networks. Sync occurs entirely over peer-to-peer local connections without requiring internet connectivity or DNS lookup.

### 4. Self-Hosted Infrastructure Knowledge Graph
DevOps engineers log server inventories, SSH key locations, container deployments, and incident post-mortems into AnyType. Automated monitoring scripts post structured alerts to AnyType local endpoints, creating an immutable history of infrastructure events.

## Strengths
- **Decentralized Cryptography & Zero-Knowledge**: Data is encrypted client-side using 128-bit symmetric keys derived from a 12-word recovery seed. Sync relays (`any-sync-node`) pass encrypted data blobs without ability to read object content.
- **Object-Oriented Flexible Schema**: Eliminates rigid folder hierarchies. Everything is an Object with custom Types, Relations (properties), and Views (Kanban, Table, Gallery, List).
- **Local-First Speed**: Zero latency when creating or searching large databases; reads and writes take place directly on local NVMe or SSD storage before background sync.
- **Native FastMCP 3.1 Agent Integration**: Provides direct tool definitions for AI agents to query spaces, inspect schemas, create objects, and manage graph linkages programmatically.
- **Cross-Platform Parity**: Identical feature sets and cryptographic security models across desktop (Linux, macOS, Windows) and mobile platforms.
- **Self-Hostable Network Relays**: Organizations can host their own `any-sync-node`, `any-sync-consensus`, and `any-sync-filenode` services in Docker or Kubernetes to maintain 100% network sovereignty.

## Limitations
- **Collaborative Editing Complexity**: Peer-to-peer conflict resolution (CRDTs over Anysync) is highly optimized for single-user multi-device sync, but real-time multi-user concurrent cursor collaboration is less fluid than cloud-native tools like Google Docs.
- **Object Model Learning Curve**: Users accustomed to flat markdown files or traditional file-and-folder trees must adapt to defining Types, Relations, and Sets.
- **Headless Node Resource Overhead**: Running self-hosted Anysync relays (`any-sync-node`, consensus, filenode) requires managing multiple Docker microservices and Go binaries.
- **API Rate Limits & Local Gateway Setup**: Automating AnyType requires maintaining an active local client session or running a headless AnyType daemon with API keys enabled.

## When to use it
- When local-first data ownership, zero-knowledge encryption, and privacy are strict requirements.
- When building structured relational databases (tasks, projects, research items) that require local offline execution.
- When exposing private notes to local AI agents via FastMCP 3.1 without risking cloud data exposure.
- When working in air-gapped or low-connectivity environments where cloud SaaS tools fail.

## When not to use it
- When requiring simple, human-readable plain text Markdown files saved directly on disk without database abstraction (use [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).
- When real-time multi-user document co-authoring with simultaneous visual cursors is required (use Nextcloud text or Google Docs).
- When light-weight headless web hosting of public wikis is needed without specialized web export builds.

## Getting started

### 1. Installation & Account Initialization
Download the desktop application for your platform from the [official AnyType portal](https://anytype.io/download).
During initial setup:
1. Generate your **12-word cryptographic seed phrase**. Store it in a secure offline password manager.
2. Create your primary Space (e.g., "Personal Knowledge" or "Engineering Vault").

### 2. Self-Hosting Anysync Network (Optional for Sovereign Teams)
To eliminate dependency on AnyType's default backup relays, deploy your own Anysync stack via Docker Compose:

```yaml
version: '3.8'
services:
  any-sync-node:
    image: anyproto/any-sync-node:latest
    container_name: any-sync-node
    environment:
      - ANY_SYNC_NODE_ACCOUNT_KEY=your_node_key
    ports:
      - "8080:8080"
      - "10010:10010"
    volumes:
      - ./config/node.yml:/etc/any-sync-node/config.yml
      - anytype_node_data:/var/lib/any-sync-node
    restart: unless-stopped

volumes:
  anytype_node_data:
```

### 3. Enabling Local REST API & MCP Server
1. Launch AnyType desktop application.
2. Navigate to **Settings** > **Integrations & API**.
3. Enable **Local API Server** (defaults to port `31009`).
4. Generate a new API Key with read/write permissions.

## CLI examples

### Interacting with Local AnyType MCP Gateway
Using the official Node.js MCP bridge package:

```bash
# Retrieve local credentials and connection status
npx -y @anyproto/anytype-mcp status --port 31009

# List all accessible Spaces in the local vault
npx -y @anyproto/anytype-mcp spaces list --api-key "YOUR_ANYTYPE_API_KEY"

# Search for specific objects across all spaces
npx -y @anyproto/anytype-mcp search --query "Architecture 2027" --space-id "space_01h9x..."
```

### Headless CLI Operations via Docker
```bash
# Query space objects via cURL against local API daemon
curl -s -X GET "http://127.0.0.1:31009/v1/spaces" \
  -H "Authorization: Bearer $ANYTYPE_API_KEY" \
  -H "Content-Type: application/json" | jq .

# Inspect object types configured in space
curl -s -X GET "http://127.0.0.1:31009/v1/spaces/$SPACE_ID/types" \
  -H "Authorization: Bearer $ANYTYPE_API_KEY" | jq '.types[] | {id, name}'
```

## API examples

### FastMCP 3.1 Python Integration Server
The following example demonstrates a production-grade FastMCP 3.1 server exposing AnyType vault tools to local LLM agents (Claude 5.6 / Local DeepSeek-V4):

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Server for AnyType Local Knowledge Base Integration.
Exposes secure tools for space queries, object creation, and relational tagging.
"""

import os
import requests
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize FastMCP 3.1 application
mcp = FastMCP(
    name="AnyType KnowledgeOps Server",
    version="3.1.0",
    description="Local-first agentic access gateway for AnyType vaults"
)

ANYTYPE_API_URL = os.getenv("ANYTYPE_API_URL", "http://127.0.0.1:31009/v1")
ANYTYPE_API_KEY = os.getenv("ANYTYPE_API_KEY", "default_secret_key")

def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {ANYTYPE_API_KEY}",
        "Content-Type": "application/json",
        "Anytype-Version": "2027-01-01"
    }

@mcp.tool()
def list_spaces() -> Dict[str, Any]:
    """Retrieves all available spaces in the connected AnyType vault."""
    response = requests.get(f"{ANYTYPE_API_URL}/spaces", headers=get_headers(), timeout=10)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def search_objects(space_id: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Searches AnyType objects within a specified space by title or content snippet.
    """
    payload = {"query": query, "limit": limit}
    url = f"{ANYTYPE_API_URL}/spaces/{space_id}/objects/search"
    response = requests.post(url, headers=get_headers(), json=payload, timeout=10)
    response.raise_for_status()
    return response.json().get("objects", [])

@mcp.tool()
def create_knowledge_object(
    space_id: str,
    object_type: str,
    title: str,
    body_markdown: str,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Creates a new typed Object (Note, Task, Research Paper) inside an AnyType space.
    """
    payload = {
        "type": object_type,
        "name": title,
        "body": body_markdown,
        "relations": {
            "tags": tags or [],
            "source": "Agentic Auto-Intake",
            "created_by": "FastMCP Agent 3.1"
        }
    }
    url = f"{ANYTYPE_API_URL}/spaces/{space_id}/objects"
    response = requests.post(url, headers=get_headers(), json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Schema Validation for AnyType Payload Contracts
```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class AnytypeRelation(BaseModel):
    relation_id: str = Field(..., description="ID or slug of the Relation property")
    value: Any = Field(..., description="Primitive or object link value assigned to relation")

class AnytypeObjectCreatePayload(BaseModel):
    space_id: str = Field(..., alias="spaceId", min_length=1, description="Target Space UUID")
    type_name: str = Field("Note", alias="type", description="Type of object (e.g. Note, Task, Bookmark)")
    title: str = Field(..., min_length=1, max_length=500, alias="name", description="Object title")
    body: str = Field("", description="Markdown or block payload")
    relations: List[AnytypeRelation] = Field(default_factory=list, description="Associated object relations")
    folder_id: Optional[str] = Field(None, alias="folderId", description="Target container folder ID")

    @field_validator("type_name")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = {"Note", "Task", "Bookmark", "Project", "Document", "Contact", "Asset"}
        if v not in allowed:
            raise ValueError(f"Invalid type_name '{v}'. Must be one of {allowed}")
        return v

def validate_and_format_object_request(space_id: str, title: str, body: str, object_type: str = "Note") -> str:
    """
    Validates object payload against Pydantic v2 schemas prior to dispatching to AnyType API.
    """
    try:
        payload = AnytypeObjectCreatePayload(
            spaceId=space_id,
            type=object_type,
            name=title,
            body=body,
            relations=[
                AnytypeRelation(relation_id="status", value="Active"),
                AnytypeRelation(relation_id="priority", value="High")
            ]
        )
        return payload.model_dump_json(by_alias=True, indent=2)
    except ValidationError as err:
        print(f"Validation failure for AnyType payload: {err.json()}")
        raise

if __name__ == "__main__":
    valid_json = validate_and_format_object_request(
        space_id="space_9901a_b2c3",
        title="2027 KnowledgeOps System Architecture",
        body="## Core Overview\nIntegrating FastMCP 3.1 with AnyType local node.",
        object_type="Document"
    )
    print("Successfully validated AnyType JSON payload:")
    print(valid_json)
```

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) (Markdown-file alternative)
- [Logseq](../ai_knowledge/logseq.md) (Outliner PKM)
- [SilverBullet](silverbullet.md) (Edge-hosted programmable Markdown wiki)
- [Model Context Protocol](../automation_orchestration/mcp.md) (Standard tool interface for LLM agents)
- [Nextcloud](../../services/nextcloud.md) (Self-hosted cloud platform)
- [Syncthing](../../services/syncthing.md) (Peer-to-peer file replication)
- [Docling](../process_understanding/docling-mcp.md) (Document processing pipeline for AI intake)
- [Component Map](../../architecture/component_map.md) (System architecture placement)

## Sources / references
- [Official AnyType Portal](https://anytype.io/)
- [Anyproto GitHub Organization](https://github.com/anyproto)
- [AnyType Documentation & Anysync Specification](https://doc.anytype.io/)
- [AnyType FastMCP Gateway Repository](https://github.com/anyproto/anytype-mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
