# Paperless-ngx

## What it is
Paperless-ngx is an open-source, enterprise-grade document management system (DMS) that converts physical paper documents, emails, digital receipts, and scanned PDFs into a searchable, organized digital archive. Operating as a self-hosted web application backed by PostgreSQL, Redis, and a Python Django / Celery core, Paperless-ngx uses Tesseract OCR, machine learning classification, and automated ingestion pipelines to process incoming documents.

It provides automatic text extraction, auto-tagging, document type detection, custom metadata fields, correspondent assignment, full-text search indexing, and a REST/gRPC API. In modern homelab and enterprise AI architectures, Paperless-ngx functions as the primary document ingestion store, integrating directly with FastMCP 3.1 agents, local LLMs (Ollama, vLLM), and automation workflow platforms (n8n, Node-RED).

## What problem it solves
Managing household and organizational physical documents creates major technical and operational friction:
- **Physical Clutter & Lost Records**: Mail, utility bills, medical records, tax forms, and warranties accumulate physically and are difficult to locate when needed.
- **Unsearchable Scanned Files**: Raw PDF scans lack embedded text layers, rendering standard file search tools ineffective.
- **Manual Metadata Entry**: Manually tagging, naming, categorizing, and filing hundreds of incoming documents requires significant labor.
- **Data Privacy Risks in Cloud Services**: Uploading confidential financial, medical, and legal documents to third-party cloud storage exposes sensitive data to external breaches.

Paperless-ngx solves these issues by automating the end-to-end ingestion lifecycle. It monitors drop folders, IMAP email accounts, and mobile upload apps; applies OCR and spatial text extraction; uses machine learning (scikit-learn based classifiers) to automatically assign tags and correspondents; and exposes structured document content to local RAG pipelines and FastMCP 3.1 AI agents without data leaving your local network.

## Where it fits in the stack
**Ingestion & Storage Layer / Private Knowledge Base Architecture**.

Paperless-ngx sits between physical/digital capture points (document scanners, email inboxes, web scrapers) and downstream AI consumption frameworks (FastMCP 3.1 AI agents, local RAG vector stores, n8n automation workflows, and SSO identity providers like Authentik).

```
+-----------------------------------------------------------------------------------+
|                           Multi-Channel Ingestion                                 |
|      (Physical Scanner / Mobile App / IMAP Email Poller / Consumption Directory)  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  (File Drops & API Uploads)
+-----------------------------------------------------------------------------------+
|                             Paperless-ngx Core Server                             |
|                                                                                   |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  | Consumption Engine |  | Tesseract OCR      |  | Machine Learning Classifier |  |
|  | - File Watching    |  | - Text Extraction  |  | - Auto-Tagging              |  |
|  | - PDF Assembly     |  | - HOCR Spatial Map |  | - Correspondent Matching    |  |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | PostgreSQL Database (Metadata) + Redis / Celery Task Queue                   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                        REST API / FastMCP 3.1 Server Interface
                                          v
+-----------------------------------------------------------------------------------+
|                        Downstream AI & Automation Stack                           |
|       (FastMCP 3.1 Agents / Ollama Local RAG / n8n Pipelines / Authentik SSO)     |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Automated Household Document Archival**: Digitizing physical mail, property tax notices, utility bills, and medical receipts via a network scanner connected directly to the consumption directory.
- **Enterprise Expense & Receipt Processing**: Ingesting financial receipts from email attachments, running OCR, extracting vendor names, and auto-tagging tax categories.
- **Local RAG Grounding Source**: Serving as the structured document store for local vector databases (Qdrant, Chroma, Weaviate) queried by Ollama-hosted LLMs.
- **FastMCP 3.1 Agent Tool Execution**: Allowing Claude Code, Cursor, or custom FastMCP 3.1 agents to query, search, and extract document content via structured API endpoints.
- **Contract & Technical Library Management**: Storing equipment manuals, software licenses, and legal contracts with full-text searchability across technical terms.

## Architecture & Core Mechanics

### Architecture Diagram: Document Ingestion & Processing Lifecycle

```
[ Incoming File (PDF / PNG / Email) ]
                  |
                  v
+-----------------------------------+
|  Consumption Folder / Barcode Scan|
+-----------------------------------+
                  |
                  v
+-----------------------------------+
|  Celery Task Queue (Redis Backed) |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
|  Paperless Ingestion Pipeline     |
|  1. Pre-consumption Hooks         |
|  2. PDF / Image Normalization     |
|  3. Tesseract OCR Processing      |
|  4. ML Model Tag & Owner Predict  |
|  5. Metadata & Custom Field Parse |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
|  Storage & Indexing Engine        |
|  - Postgres Metadata Write        |
|  - Whoosh / Xapian Index Update   |
|  - Save Searchable PDF to Disk    |
|  6. Post-consumption Triggers     |
+-----------------------------------+
                  |
                  v
[ REST API / FastMCP Agent Endpoint Available ]
```

### Key Technical Features & Subsystems

1. **OCR Engine (Tesseract & pdf2image)**: Paperless-ngx converts raster images and vector PDFs into fully searchable archivable PDF/A files. Tesseract extracts plain text and spatial hOCR metadata, preserving multi-column layouts and text coordinates.
2. **Scikit-Learn Machine Learning Classifier**: The system includes a Naive Bayes classifier trained continuously on user tagging habits. When new documents arrive, the classifier analyzes the extracted text and assigns tags, document types, and correspondents with calculated probability confidence.
3. **IMAP Email Ingestion Module**: Monitors external IMAP email accounts, downloads attachments matching configurable subject/sender rules, and pushes them straight into the processing queue.
4. **Storage Path Templating Engine**: Dynamically renames and organizes physical disk storage folders using Django template logic (e.g., `{created_year}/{correspondent}/{document_type}_{title}.pdf`).
5. **REST API & FastMCP 3.1 Compatibility**: Exposes comprehensive OpenAPI-documented REST endpoints for searching documents, updating tags, extracting raw OCR text, downloading PDF streams, and triggering custom workflows.

## Strengths
- **Fully Self-Hosted & Private**: Zero external cloud dependency ensures complete privacy for financial, health, and legal documents.
- **Automated Machine Learning Tagging**: Learns tagging logic over time, eliminating manual data entry for recurring bills and statements.
- **Robust Multi-Channel Ingestion**: Supports direct file watch folders, IMAP email polling, web UI drops, and REST API uploads.
- **Full-Text & Spatial Search**: Fast, complex boolean search query support over OCR text content, tags, custom fields, and date ranges.
- **Standardized SSO Support**: OpenID Connect (OIDC) integration allows seamless authentication via Authentik, Keycloak, or Authelia.

## Limitations
- **High Resource Requirements during OCR**: Bulk ingesting thousands of multi-page PDFs can cause high CPU utilization during Tesseract processing.
- **Handwriting Recognition Constraints**: Standard Tesseract OCR struggles with handwritten notes or poor quality thermal paper receipts compared to advanced cloud vision APIs.
- **Database Dependency Stack**: Requires maintaining PostgreSQL and Redis alongside the main application container for optimal queue management.

## When to use it
- Setting up a private, self-hosted document management center for home-office or enterprise use.
- Feeding structured document text into local AI agent workflows and RAG knowledge bases.
- Automating invoice and expense receipt organization directly from email accounts.
- Ensuring strict compliance where sensitive documents cannot be uploaded to third-party SaaS cloud platforms.

## When not to use it
- Real-time multi-user collaborative document editing (use Nextcloud or Google Docs instead).
- Storing unformatted raw binary backups or media assets (use MinIO or Syncthing instead).
- Lightweight deployments without Docker/PostgreSQL capability where simple file folder structures suffice.

## Getting started

### Installation via Docker Compose
Deploy Paperless-ngx with PostgreSQL, Redis, and Tesseract OCR language packs:

```yaml
version: "3.8"
services:
  broker:
    image: docker.io/library/redis:7-alpine
    container_name: paperless-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data

  db:
    image: docker.io/library/postgres:16-alpine
    container_name: paperless-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: paperless_secure_password
    volumes:
      - pgdata:/var/lib/postgresql/data

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperless-webserver
    restart: unless-stopped
    depends_on:
      - db
      - broker
    ports:
      - "8000:8000"
    volumes:
      - ./data:/usr/src/paperless/data
      - ./media:/usr/src/paperless/media
      - ./export:/usr/src/paperless/export
      - ./consume:/usr/src/paperless/consume
    environment:
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_DBHOST: db
      PAPERLESS_DBNAME: paperless
      PAPERLESS_DBUSER: paperless
      PAPERLESS_DBPASS: paperless_secure_password
      PAPERLESS_OCR_LANGUAGE: eng
      PAPERLESS_TIME_ZONE: America/New_York
      PAPERLESS_TASK_WORKERS: 2
      PAPERLESS_SECRET_KEY: "change-this-to-a-random-secret-key"

volumes:
  redis_data:
  pgdata:
```

Launch the stack and create an administrative account:

```bash
docker compose up -d
docker exec -it paperless-webserver python3 manage.py createsuperuser
```

## CLI examples

```bash
# Export all documents and metadata for backup
docker exec -it paperless-webserver python3 manage.py document_exporter /usr/src/paperless/export

# Rebuild full-text search index after bulk updates
docker exec -it paperless-webserver python3 manage.py document_index reindex

# Rename disk files according to active storage path templates
docker exec -it paperless-webserver python3 manage.py document_renamer

# Retrain machine learning classifier manually
docker exec -it paperless-webserver python3 manage.py document_train_classifier
```

## API examples

### 1. FastMCP 3.1 Document Search & Content Tool Server

This executable Python script builds a FastMCP 3.1 tool server exposing Paperless-ngx document search and full-text content extraction to AI agents, enforced via strict Pydantic v2 data models.

```python
import os
import httpx
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from fastmcp import FastMCP

# Instantiate FastMCP 3.1 Server
mcp = FastMCP(
    name="Paperless-ngx Agent Bridge",
    version="3.1.0",
    description="FastMCP server providing structured document search and OCR content extraction from Paperless-ngx."
)

# ------------------------------------------------------------------
# Pydantic v2 Schemas
# ------------------------------------------------------------------

class DocumentSearchRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(..., min_length=1, description="Search query string (supports boolean operators).")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of documents to return.")
    tag_id: Optional[int] = Field(default=None, description="Optional tag ID filter.")


class PaperlessDocumentSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    document_id: int = Field(..., description="Unique document ID in Paperless-ngx.")
    title: str = Field(..., description="Document title.")
    created_date: str = Field(..., description="ISO 8601 creation timestamp.")
    ocr_content_snippet: str = Field(..., description="First 300 characters of extracted OCR text.")
    document_url: str = Field(..., description="Direct web UI URL for the document.")


class DocumentSearchResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    total_found: int = Field(..., ge=0)
    results: List[PaperlessDocumentSummary]


# ------------------------------------------------------------------
# FastMCP Tool Implementation
# ------------------------------------------------------------------

@mcp.tool(
    name="search_paperless_documents",
    description="Queries the Paperless-ngx document archive and returns matching document metadata and OCR snippets."
)
async def search_paperless_documents(request: DocumentSearchRequest) -> DocumentSearchResponse:
    base_url = os.getenv("PAPERLESS_URL", "http://localhost:8000")
    api_token = os.getenv("PAPERLESS_API_TOKEN", "sample_token")

    headers = {
        "Authorization": f"Token {api_token}",
        "Accept": "application/json"
    }

    params = {
        "query": request.query,
        "page_size": request.limit
    }
    if request.tag_id:
        params["tags__id__all"] = request.tag_id

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(f"{base_url}/api/documents/", headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            raise RuntimeError(f"Error connecting to Paperless API: {str(exc)}") from exc

    results_list: List[PaperlessDocumentSummary] = []
    for item in data.get("results", []):
        snippet = (item.get("content") or "")[:300].replace("\n", " ") + "..."
        doc_summary = PaperlessDocumentSummary(
            document_id=item["id"],
            title=item["title"],
            created_date=item.get("created", "1970-01-01"),
            ocr_content_snippet=snippet,
            document_url=f"{base_url}/documents/{item['id']}"
        )
        results_list.append(doc_summary)

    return DocumentSearchResponse(
        total_found=data.get("count", len(results_list)),
        results=results_list
    )


if __name__ == "__main__":
    mcp.run()
```

### 2. Async Python Document Ingestion Client with Pydantic v2

```python
import asyncio
import httpx
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class IngestDocumentRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    title: str = Field(..., min_length=1)
    file_path: str = Field(..., min_length=1)
    tags: List[int] = Field(default_factory=list)

class IngestDocumentResponse(BaseModel):
    task_id: str = Field(..., description="Celery task UUID for background consumption.")
    status: str = Field(default="queued")

async def upload_document_to_paperless(req: IngestDocumentRequest, url: str, token: str) -> IngestDocumentResponse:
    headers = {"Authorization": f"Token {token}"}

    # In a real environment:
    # with open(req.file_path, "rb") as f:
    #     files = {"document": f}
    #     data = {"title": req.title}
    #     res = httpx.post(f"{url}/api/documents/post_document/", headers=headers, files=files, data=data)
    #     return IngestDocumentResponse(task_id=res.text)

    # Simulated return for documentation verification
    return IngestDocumentResponse(task_id="cb7e8912-3490-4811-9a99-01828f21bc99", status="queued")

if __name__ == "__main__":
    request_data = IngestDocumentRequest(
        title="2026_Electric_Utility_Statement.pdf",
        file_path="/tmp/utility_2026.pdf",
        tags=[12, 45]
    )
    res = asyncio.run(upload_document_to_paperless(request_data, "http://localhost:8000", "dummy"))
    print(f"Document upload initiated successfully. Task UUID: {res.task_id}")
```

## Related tools / concepts
- [n8n](n8n.md) — Workflow engine for automating multi-service document flows.
- [Authentik](authentik.md) — Enterprise identity provider for SSO security.
- [Nextcloud](nextcloud.md) — Cloud file storage for syncing scan folders across devices.
- [Ollama](ollama.md) — Local model server for running LLM analysis over OCR text.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Tool integration protocol for AI agents.

## Sources / references
- [Paperless-ngx Official Documentation](https://docs.paperless-ngx.com/)
- [Paperless-ngx Official GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)
- [Paperless-ngx REST API Reference](https://docs.paperless-ngx.com/api/)
- [FastMCP 3.1 Task Protocol Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
