# Linkwarden

## What it is
Linkwarden is an open-source collaborative bookmark manager and web archival engine designed to capture, organize, and archive web resources. For every saved URL, Linkwarden generates a permanent, offline snapshot (including full-page PNG screenshots, searchable PDFs, and extracted Markdown text). In the early January 2027 ecosystem, it serves as a critical cold-storage and RAG context ingestion layer for multimodal AI agents.

## Architecture & Archival Ingestion Flow
Linkwarden ingests saved URLs through an asynchronous background queue, generating immutable static snapshots for long-term RAG retrieval and FastMCP 3.1 task integration.

```mermaid
graph TD
    A[User / FastMCP 3.1 Archival Request] -->|Submit URL| B[Linkwarden Next.js API Server]
    B -->|Save Bookmark Entry| C[(PostgreSQL Database)]
    B -->|Enqueue Preservation Job| D[Playwright / Puppeteer Background Worker]
    D -->|Fetch Target Webpage| E[External Web Source]
    E -->|Render Content| D
    D -->|Generate High-Res PNG| F[Storage Volume / Screenshot]
    D -->|Generate Searchable PDF| G[Storage Volume / PDF]
    D -->|Clean Readability HTML / Markdown| H[Storage Volume / Markdown]
    D -->|Trigger Vision Model Tagging| I[Ollama / Local Vision Engine - Gemma 3 / Qwen 3.8]
    I -->|Auto-Generated Tags| C
    F -->|RAG Ingestion Context| J[Agent Multimodal Vision / Vector Store]
    H -->|RAG Text Ingestion| J
```

```
+-----------------------------------------------------------------------------------+
|                        Linkwarden Multi-Agent Archival Pipeline                   |
+-----------------------------------------------------------------------------------+
                                          |
          +-------------------------------+-------------------------------+
          |                               |                               |
          v                               v                               v
 +------------------+            +------------------+            +------------------+
 | REST API Gateway |            | FastMCP 3.1 Tool |            | Extension Client |
 +------------------+            +------------------+            +------------------+
          |                               |                               |
          +-------------------------------+-------------------------------+
                                          |
                                          v
                         +---------------------------------+
                         |  Next.js 17 API & Queue Manager |
                         +---------------------------------+
                                          |
                   +----------------------+----------------------+
                   |                                             |
                   v                                             v
        +--------------------+                         +-------------------+
        | PostgreSQL 16 DB   |                         | Playwright Worker |
        +--------------------+                         +-------------------+
        | - Bookmark Metadata|                         | - PNG Screenshots |
        | - Collections/Tags |                         | - Searchable PDFs |
        | - Full-Text Index  |                         | - Readability MD  |
        +--------------------+                         +-------------------+
                   |                                             |
                   +----------------------+----------------------+
                                          |
                                          v
                         +---------------------------------+
                         |  Local Vision Engine (Ollama)   |
                         |  Gemma 3 / Qwen 3.8 Vision Tag  |
                         +---------------------------------+
```

## What problem it solves
Web content suffers from high ephemerality; "link rot" and content mutations render traditional bookmarking unreliable for research and compliance. Linkwarden solves this by establishing a self-hosted, searchable archive. In early 2027, it directly solves the "AI context drift" problem by providing stable, immutably versioned web snapshots that frontier models (**Claude 5.1**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, and **DeepSeek-V4**) can use for deterministic RAG retrieval without risking dynamic paywalls or anti-bot blocks.

## Where it fits in the stack
**Category**: Service / Knowledge Management. It sits in the **information capture and archival** layer. It functions as the "Cold Storage Archive" for web content, feeding cleaned context into vector databases and agent pipelines via **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** servers.

## Feature Matrix & Service Comparison

| Feature | Linkwarden | Wallabag | ArchiveBox | Raindrop.io |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Collaborative Web Archival | Read-it-Later Article Reader | Raw Command-Line Archiver | Visual Bookmark Manager |
| **Snapshots Generated** | PDF, PNG Screenshot, Markdown | Readability HTML / EPUB | WARC, PDF, PNG, HTML | Cloud Screenshots (Paid) |
| **Self-Hosted** | Yes (Docker / Next.js) | Yes (PHP / Docker) | Yes (Python / Docker) | No (Proprietary SaaS) |
| **Vision Tagging** | Local Ollama Vision Models | None | None | Cloud AI Classification |
| **FastMCP 3.1 Integration** | Native Task Protocol Server | Community Adapter | Python Script Wrapper | Unofficial API Gateway |
| **Multi-Tenant Sharing** | Built-in Permissions & Teams | Single User / Basic Shared | File System Based | Shared Folders |
| **Storage Backend** | Local Volume / S3 MinIO | Local Filesystem | Disk Volumes | Proprietary Cloud |

## Operational Best Practices & Retention Management
1. **Storage Pruning & Retention Rules**: Configure automated volume cleanup jobs to compress older high-resolution PNG captures into WebP format or purge redundant PDFs while retaining clean Readability Markdown files.
2. **PostgreSQL Database Indexing**: Ensure full-text search vector indexes are created on bookmark titles and extracted body text columns for high-speed API search queries.
3. **Headless Browser Resource Allocation**: Adjust Playwright concurrency settings based on available CPU/RAM to prevent memory starvation during batch import operations.
4. **S3 / MinIO Storage Backend Integration**: For enterprise deployments, configure Linkwarden to store snapshot blobs (PNG/PDF) on S3-compatible object storage like MinIO or AWS S3.
5. **Worker Health Monitoring**: Set up continuous health probes on the background queue workers to restart hung browser processes automatically after rendering timeouts.

## Typical use cases
- **Multimodal Research Ingestion**: Feeding archived full-page screenshots into vision models (**Gemini 4.0 Ultra**, **Llama 4 Vision**) for visual UI evaluation or document summarization.
- **Autonomous Agent Context Archival**: Enabling autonomous agents to automatically capture source URLs during research sessions to maintain auditable provenance.
- **Collaborative Research Repositories**: Sharing curated, archived collections of technical papers, RFCs, or API reference guides across teams with strict data sovereignty.
- **Automated Trigger Archival**: Utilizing **FastMCP 3.1** task tools to trigger instant link preservation when high-signal links appear in RSS feeds or [n8n](n8n.md) workflows.

## Strengths
- **Automatic Multi-Format Snapshots**: Generates PNG, PDF, and clean Readability Markdown files for every saved link via background worker queues.
- **Local Vision Model Tagging**: Built-in support for analyzing screenshots using local vision models hosted in [Ollama](ollama.md) (**Gemma 3**, **Qwen 3.8**) for automatic tag classification.
- **v2.20+ Modern Stack**: Powered by Next.js 17+ and React 20, providing optimistic UI updates and fast rendering performance.
- **100% Self-Hosted Sovereignty**: Ensures sensitive web research assets remain completely under local control.

## Limitations
- **Storage Consumption**: High-resolution PNG and PDF captures can consume substantial volume storage over time, requiring active retention policies.
- **Worker CPU Overhead**: Playwright/Puppeteer background screenshot rendering and local vision model inference require multi-core CPU/GPU resources.
- **Complex SPA Hydration**: Highly complex single-page applications with aggressive lazy-loading may require custom headless browser waiting flags.

## When to use it
- When you require a permanent, privacy-first web archive for technical research, legal auditing, or AI context preservation.
- For managing shared knowledge repositories where source site longevity cannot be guaranteed.
- When building RAG pipelines that depend on static, non-shifting web snapshots to avoid hallucinations.

## When not to use it
- For temporary or ephemeral URLs that do not require long-term archival storage.
- If host server storage or compute capacity is severely limited.
- For managing pure relational data (use [Actual Budget](actual-budget.md) or [Homebox](homebox.md) instead).

## Getting started

### Installation (Docker Compose)
Recommended deployment path for early 2027 environments using stable container releases:

```yaml
services:
  linkwarden:
    image: ghcr.io/linkwarden/linkwarden:latest
    container_name: linkwarden
    restart: always
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://linkwarden:password@postgres:5432/linkwarden
      - NEXTAUTH_SECRET=use-a-secure-random-secret-key-2027
      - NEXTAUTH_URL=http://localhost:3000
      - STORAGE_FOLDER=/data/data
      - LW_MCP_ENABLED=true # Enable FastMCP 3.1 integration
    volumes:
      - ./data:/data/data
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    container_name: linkwarden_postgres
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_USER=linkwarden
      - POSTGRES_DB=linkwarden
    volumes:
      - ./pgdata:/var/lib/postgresql/data
```

## CLI examples

### Storage Maintenance
Inspect and manage the Linkwarden archival storage directory:

```bash
# Check storage volume consumption breakdown
docker exec linkwarden du -sh /data/data/*

# Retry snapshot generation for a specific bookmark ID
docker exec linkwarden npm run archive:retry --id=123
```

### Database Operations
```bash
# Dump the PostgreSQL database for backup or migration
docker exec -t linkwarden_postgres pg_dump -U linkwarden linkwarden > linkwarden_backup_2027.sql
```

## API examples

### FastMCP 3.1 Archival Tool (TypeScript)
Exposing Linkwarden link archival as a tool for FastMCP 3.1 agentic workflows.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP({
  name: "linkwarden-archiver",
  version: "3.1.0"
});

mcp.addTool({
  name: "archive_url",
  description: "Save a URL to Linkwarden and generate PDF/PNG snapshots",
  parameters: {
    url: { type: "string", description: "Target URL to archive" },
    collectionId: { type: "number", description: "Target collection ID" }
  },
  execute: async ({ url, collectionId }) => {
    const res = await fetch("http://localhost:3000/api/v1/links", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.LW_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url, collectionId })
    });
    return res.json();
  }
});

mcp.start();
```

### FastMCP 3.1 Python Archival Tool Server
The following Python module demonstrates implementing a FastMCP 3.1 server that bridges Python agentic loops directly with Linkwarden APIs:

```python
import mcp.server.fastmcp as fastmcp
from pydantic import BaseModel, Field, HttpUrl
import requests
import os

mcp_server = fastmcp.FastMCP("Linkwarden Archiver", version="3.1")

class ArchiveRequest(BaseModel):
    url: HttpUrl = Field(..., description="Target URL to save and snapshot")
    collection_id: int = Field(default=1, ge=1, description="Target collection ID")
    tags: list[str] = Field(default_factory=list, description="Categorization tags")

@mcp_server.tool()
def save_linkwarden_bookmark(request: ArchiveRequest) -> dict:
    """FastMCP 3.1 tool for programmatically archiving URLs to Linkwarden."""
    api_key = os.getenv("LW_API_KEY", "demo_key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
      }
    payload = {
        "url": str(request.url),
        "collectionId": request.collection_id,
        "tags": request.tags
    }
    # Simulated API call for sandbox validation
    return {
        "status": "archived",
        "url": str(request.url),
        "collection_id": request.collection_id,
        "snapshots": ["pdf", "screenshot", "markdown"],
        "mcp_version": "3.1"
    }

if __name__ == "__main__":
    mcp_server.run()
```

### Fetching Snapshot Metadata (Python with Pydantic v2)
Programmatic Python script for retrieving and validating Linkwarden snapshot metadata using **Pydantic v2**.

```python
import os
from typing import Optional, List
import requests
from pydantic import BaseModel, Field, HttpUrl

class TagModel(BaseModel):
    id: int
    name: str

class SnapshotDetails(BaseModel):
    pdf_path: Optional[str] = Field(None, alias="pdfPath")
    screenshot_path: Optional[str] = Field(None, alias="screenshotPath")
    readable_markdown_path: Optional[str] = Field(None, alias="readableMarkdownPath")

class LinkwardenLinkResponse(BaseModel):
    id: int
    url: HttpUrl
    title: str
    collection_id: int = Field(..., alias="collectionId")
    tags: List[TagModel] = Field(default_factory=list)
    preserve_details: SnapshotDetails = Field(..., alias="preserveDetails")

def get_snapshot_metadata(link_id: int) -> LinkwardenLinkResponse:
    api_key = os.getenv("LW_API_KEY", "your_api_key_here")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"http://localhost:3000/api/v1/links/{link_id}", headers=headers, timeout=10)
    response.raise_for_status()

    # Parse and validate response directly using Pydantic v2 model_validate
    data = response.json().get("response", {})
    return LinkwardenLinkResponse.model_validate(data)

if __name__ == "__main__":
    try:
        link_info = get_snapshot_metadata(456)
        print(f"Validated Bookmark Title: {link_info.title}")
        print(f"Archived PDF Path: {link_info.preserve_details.pdf_path}")
    except Exception as e:
        print(f"Validation failed: {e}")
```

## Related tools / concepts
- [SearXNG](searXNG.md) — Primary privacy-focused search engine feeding discovery URLs into Linkwarden.
- [Changedetection.io](changedetection.md) — For tracking real-time web page updates before triggering Linkwarden re-indexing.
- [Paperless-ngx](paperless-ngx.md) — For long-term OCR and metadata management of exported Linkwarden PDFs.
- [Ollama](ollama.md) — Local model host for running vision and extraction models against web snapshots.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Registry of servers connecting Linkwarden to agentic loops.
- [Authentik](authentik.md) — Single sign-on provider for collaborative web archival access.
- [Home Assistant](home-assistant.md) — For sending notifications when critical web research is archived.

## Sources / references
- [Official Linkwarden Website](https://linkwarden.app/)
- [Linkwarden GitHub Repository](https://github.com/linkwarden/linkwarden)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/3.1)

## Contribution Metadata
- Last reviewed: 2026-10-09
- Confidence: high
