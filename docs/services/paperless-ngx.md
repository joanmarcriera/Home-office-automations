# Paperless-ngx

## What it is
Paperless-ngx is a community-supported document management system (DMS) that transforms your physical documents into a searchable digital archive. It provides a web-based interface for managing scanned PDFs and images, utilizing advanced OCR and machine learning for automated organization. In early January 2027, it serves as the cornerstone of private document intelligence, supporting the [FastMCP 3.1 / MCP](../tools/automation_orchestration/mcp.md) specifications for direct agentic access.

## What problem it solves
It eliminates paper clutter and "digital fragmentation" by providing a central, private repository for all household and office documents. It solves the problem of unsearchable scanned files by performing automatic Optical Character Recognition (OCR) and uses machine learning to suggest tags, correspondents, and document types based on content. It enables frontier models like [Gemma 3](../tools/ai_knowledge/local_llms.md), [Llama 4](../tools/ai_knowledge/local_llms.md), [GPT-5.5](../tools/providers/index.md), [Gemini 4.0 Pro](../tools/providers/index.md), and [Claude 5.1](../tools/providers/anthropic.md) to reason over physical mail, bills, and tax records securely.

## Where it fits in the stack
**Ingestion & Storage Layer**. It serves as the primary archival system for documents in the homelab, sitting between capture tools (scanners, emails) and consumption tools (AI agents, mobile apps). It integrates with [Authentik](authentik.md) for SSO, [n8n](n8n.md) for automated workflows, and the [FastMCP 3.1 Specification](../tools/automation_orchestration/mcp.md) for standardized agent discovery, tool definitions, and resource/prompt sharing.

## Typical use cases
- **Household Digitization**: Storing and indexing medical records, utility bills, and tax documents.
- **Technical Library Management**: Archiving whitepapers, manuals, and schematics for quick reference.
- **AI Knowledge Grounding**: Providing a structured, searchable data source for local RAG (Retrieval-Augmented Generation) pipelines using [Ollama](ollama.md).
- **Automated Expense Tracking**: Ingesting receipts via email and automatically tagging them for financial audits.
- **Agentic Document Processing**: Using an AI agent to extract specific data from invoices stored in Paperless-ngx.

## Strengths
- **Automated OCR**: High-quality text extraction from images and PDFs using Tesseract.
- **Machine Learning Integration**: Learns your tagging patterns over time, reducing manual effort for new documents.
- **Full-Text Search**: Fast and precise search capabilities with support for complex filters and saved views.
- **Multi-Channel Ingestion**: Supports consumption folders, email polling (IMAP), and a comprehensive REST API.
- **Native MCP Support**: Exposes documents to the AI ecosystem via standardized tools.

## Limitations
- **Resource Intensive**: OCR processing can be CPU-heavy, especially during bulk ingestion of large document backlogs.
- **Dependency Management**: Requires a stack including Redis and a database (PostgreSQL/MariaDB) for optimal performance.
- **OCR Accuracy**: Handwritten notes or extremely low-resolution scans may have lower extraction accuracy compared to digital-first PDFs.

## When to use it
- When you want to transition to a paperless office and need a robust, self-hosted management system.
- To maintain a private, searchable archive of sensitive personal or business documents.
- When you need a structured document source to feed into AI agent workflows.
- For local archival that doesn't rely on third-party cloud storage.

## When not to use it
- For managing real-time collaborative documents (use [Nextcloud](nextcloud.md) instead).
- If you only have a few dozen documents and don't require OCR or advanced tagging capabilities.
- For high-volume transactional logs that don't benefit from document-centric management.

## Getting started

### Installation (Docker Compose)
Paperless-ngx is best deployed using Docker Compose:

```yaml
services:
  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/usr/src/paperless/data
      - ./media:/usr/src/paperless/media
      - ./consume:/usr/src/paperless/consume
    environment:
      PAPERLESS_REDIS: redis://redis:6379
      PAPERLESS_DBHOST: db
  db:
    image: postgres:16
    volumes:
      - ./pgdata:/var/lib/postgresql/data
  redis:
    image: redis:7
```

### SSO Integration
Navigate to the settings to configure OpenID Connect via [Authentik](authentik.md) for centralized authentication and MFA.

## CLI examples

### Document Export
Exports all documents and metadata to a specified directory for backup:
```bash
docker exec -it paperless-webserver python3 manage.py document_exporter /usr/src/paperless/export
```

### Document Renaming
Renames files on disk based on their current metadata and your storage path template:
```bash
docker exec -it paperless-webserver python3 manage.py document_renamer
```

### Reindexing the Search Engine
Rebuilds the search index, useful after bulk metadata updates or manual database changes:
```bash
docker exec -it paperless-webserver python3 manage.py document_index reindex
```

## API examples

### Uploading a Document (curl)
```bash
curl -X POST http://localhost:8000/api/documents/post_document/ \
  -H "Authorization: Token your_api_token" \
  -F "document=@/path/to/invoice.pdf" \
  -F "title=Utility Bill"
```

### Programmatic Ingestion and Document Retrieval with Pydantic v2 (Python)
In early January 2027, parsing and querying files agentically requires strict validation layers. Below is an asynchronous Python snippet retrieving and validating document metadata from Paperless-ngx using **Pydantic v2**:

```python
import asyncio
import httpx
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class DocumentModel(BaseModel):
    id: int = Field(..., description="Unique document ID in Paperless-ngx")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Extracted OCR text content")
    added: str = Field(..., description="ISO 8601 timestamp representing addition date")
    tags: List[int] = Field(default=[], description="List of tag IDs assigned to this document")
    correspondent: Optional[int] = Field(None, description="ID of the assigned correspondent")

class DocumentListResponse(BaseModel):
    count: int
    next_url: Optional[HttpUrl] = Field(None, alias="next")
    previous_url: Optional[HttpUrl] = Field(None, alias="previous")
    results: List[DocumentModel]

async def get_recent_documents(base_url: str, token: str) -> DocumentListResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/documents/",
            headers={"Authorization": f"Token {token}", "Accept": "application/json"}
        )
        response.raise_for_status()
        raw_payload = response.json()

        # Validates and parses the JSON dictionary via Pydantic v2
        return DocumentListResponse.model_validate(raw_payload)

async def main():
    try:
        data = await get_recent_documents(
            base_url="http://localhost:8000",
            token="your_secret_api_token_here"
        )
        print(f"Total documents found: {data.count}")
        for doc in data.results:
            print(f"[{doc.id}] {doc.title} (Added: {doc.added}) - OCR length: {len(doc.content)} chars")
    except Exception as e:
        print(f"Structured validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [n8n](n8n.md) — For automating document processing and multi-service synchronization.
- [Authentik](authentik.md) — For securing the DMS with enterprise-grade SSO and MFA.
- [Nextcloud](nextcloud.md) — For syncing the consumption folder across mobile devices and desktops.
- [Vikunja](vikunja.md) — For linking tasks to specific archived documents.
- [Changedetection.io](changedetection.md) — For capturing and ingesting web snapshots as PDFs.
- [Gitea](gitea.md) — For version-controlling scripts that interact with the Paperless API.
- [Ollama](ollama.md) — For local AI analysis and summarization of extracted text content.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for integrating document intelligence into agent workflows.

## Sources / references
- [Official Website](https://docs.paperless-ngx.com/)
- [GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
