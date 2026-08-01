# Linkwarden

## What it is
Linkwarden is an open-source collaborative bookmark manager designed to archive, organize, and collaborate on webpages. It captures a permanent snapshot (screenshot and PDF) of each bookmarked page, ensuring the information remains accessible even if the original website goes offline or changes. In the late October / November 2026 ecosystem, it serves as a critical archival layer for multimodal AI agents.

## What problem it solves
Web content is highly ephemeral; "link rot" renders traditional bookmarking ineffective for long-term research. Linkwarden solves this by creating a self-hosted, searchable archive. By late 2026, it also addresses the "AI context rot" problem, providing stable, versioned snapshots that frontier models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0** agents can use for consistent retrieval without worrying about live site changes, paywalls, or anti-bot measures.

## Where it fits in the stack
**Category**: Service / Knowledge Management. It sits in the **information capture and archival** layer. It acts as the "Cold Storage" for web knowledge, feeding into RAG pipelines via the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** servers.

## Typical use cases
- **Multimodal Research Archival**: Using **Gemma 3** or **Claude 5.1**'s vision capabilities to analyze and summarize archived screenshots directly within Linkwarden.
- **Agentic Knowledge Intake**: Autonomous agents saving relevant documentation during a task to ensure a persistent trail of sources.
- **Team Collaboration**: Sharing curated, archived collections of technical papers or market research in a private environment.
- **Automated Archival Triggers**: Using **MCP 3.1 Task Protocol** to automatically trigger Linkwarden archival when a new high-signal URL is detected in a chat or RSS feed.

## Strengths
- **Automatic Multi-Format Snapshots**: Generates PNG, PDF, and simplified Markdown (via **FastMCP 3.1** integration) for every link.
- **Gemma 3 / Qwen 3.6 Integration**: Native support for running local vision models against archived snapshots for automated tagging.
- **v2.18+ Performance**: Utilizes Next.js 16 and React 20 for near-instant rendering and optimistic state updates.
- **Self-Hosted Privacy**: Ensures that sensitive research data never leaves your infrastructure.

## Limitations
- **Storage Growth**: High-fidelity snapshots can consume significant disk space over time; requires active volume management.
- **Processing Overhead**: Generating snapshots and running local vision models for tagging requires robust CPU/GPU resources.
- **Dynamic Content**: Highly complex SPAs with heavy animation may still present challenges for static PDF/PNG snapshots.

## When to use it
- When you need a permanent, privacy-first archive of web content for research or legal compliance.
- For managing shared knowledge bases where source integrity is paramount.
- When building AI agents that require "frozen" snapshots of the web to prevent hallucinations caused by content drift.

## When not to use it
- For ephemeral links that do not require long-term archival.
- If server resources (CPU/Disk) are extremely constrained.
- For managing structured relational data (use [Actual Budget](actual-budget.md) or [Homebox](homebox.md) instead).

## Getting started

### Installation (Docker Compose)
Recommended deployment using the latest late 2026 stable images.

```yaml
services:
  linkwarden:
    image: ghcr.io/linkwarden/linkwarden:latest
    container_name: linkwarden
    restart: always
    ports:
      - 3000:3000
    environment:
      - DATABASE_URL=postgresql://linkwarden:password@postgres:5432/linkwarden
      - NEXTAUTH_SECRET=use-a-secure-random-string
      - NEXTAUTH_URL=http://localhost:3000
      - STORAGE_FOLDER=/data/data
      - MCP_ENABLED=true # Enable MCP 3.1 endpoint
    volumes:
      - ./data:/data/data
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_USER=linkwarden
      - POSTGRES_DB=linkwarden
    volumes:
      - ./pgdata:/var/lib/postgresql/data
```

## CLI examples

### Asset Maintenance
Managing the archival storage volume.

```bash
# Check storage consumption by collection
docker exec linkwarden du -sh /data/data/*

# Force a snapshot regeneration for a specific ID
docker exec linkwarden npm run archive:retry --id=123
```

### Database Operations
```bash
# Export the database for migration or backup
docker exec -t postgres pg_dump -U linkwarden linkwarden > linkwarden_nov_2026.sql
```

## API examples

### FastMCP 3.1 Tool Definition (TypeScript)
Exposing Linkwarden archival as a tool for AI agents.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("linkwarden-archiver");

mcp.addTool({
  name: "archive_url",
  description: "Save a URL to Linkwarden and generate a snapshot",
  parameters: {
    url: { type: "string", description: "The URL to archive" },
    collectionId: { type: "number", description: "Target collection ID" }
  },
  execute: async ({ url, collectionId }) => {
    const res = await fetch("http://linkwarden:3000/api/v1/links", {
      method: "POST",
      headers: { "Authorization": `Bearer ${process.env.LW_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ url, collectionId })
    });
    return res.json();
  }
});

mcp.serve();
```

### Fetching Snapshots (Python)
Programmatic Python script for retrieving and validating Linkwarden archived snapshot metadata using **Pydantic v2** validation.

```python
import os
from typing import Optional
import requests
from pydantic import BaseModel, Field, HttpUrl

# Pydantic v2 schemas for validating Linkwarden API payloads
class SnapshotDetails(BaseModel):
    pdf_path: Optional[str] = Field(None, alias="pdfPath")
    screenshot_path: Optional[str] = Field(None, alias="screenshotPath")
    readable_markdown_path: Optional[str] = Field(None, alias="readableMarkdownPath")

class LinkwardenLinkResponse(BaseModel):
    id: int
    url: HttpUrl
    title: str
    collection_id: int = Field(..., alias="collectionId")
    preserve_details: SnapshotDetails = Field(..., alias="preserveDetails")

def get_snapshot_metadata(link_id: int) -> LinkwardenLinkResponse:
    api_key = os.getenv("LW_API_KEY", "your_api_key_here")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"http://linkwarden:3000/api/v1/links/{link_id}", headers=headers)
    response.raise_for_status()

    # Parse and validate response directly using Pydantic v2 model_validate
    data = response.json().get("response", {})
    return LinkwardenLinkResponse.model_validate(data)

if __name__ == "__main__":
    try:
        link_info = get_snapshot_metadata(456)
        print(f"Validated Document Title: {link_info.title}")
        print(f"Archived PDF Path: {link_info.preserve_details.pdf_path}")
    except Exception as e:
        print(f"Validation failed: {e}")
```

## Related tools / concepts
- [SearXNG](searXNG.md) — Primary discovery engine for content to be archived in Linkwarden.
- [Changedetection.io](changedetection.md) — For monitoring the live versions of archived pages.
- [Paperless-ngx](paperless-ngx.md) — For advanced OCR and management of exported Linkwarden PDFs.
- [Ollama](ollama.md) — Local model engine hosting Gemma 3 and Qwen 3.6 for analyzing Linkwarden snapshots.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Registry of servers connecting Linkwarden to agentic workflows.
- [Nextcloud](nextcloud.md) — For redundant backup of Linkwarden's storage volume.
- [Authentik](authentik.md) — SSO provider for secure collaborative access.
- [Home Assistant](home-assistant.md) — For dashboard notifications when new research is archived.

## Sources / references
- [Official Website](https://linkwarden.app/)
- [GitHub Repository](https://github.com/linkwarden/linkwarden)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/3.1)

## Contribution Metadata
- Last reviewed: 2026-11-07
- Confidence: high
