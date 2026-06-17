# Paperless-ngx

## What it is
Paperless-ngx is a community-supported document management system (DMS) that transforms your physical documents into a searchable digital archive. It provides a web-based interface for managing scanned PDFs and images, utilizing advanced OCR and machine learning for automated organization.

## What problem it solves
It eliminates paper clutter and "digital fragmentation" by providing a central, private repository for all household and office documents. It solves the problem of unsearchable scanned files by performing automatic Optical Character Recognition (OCR) and uses machine learning to suggest tags, correspondents, and document types based on content.

## Where it fits in the stack
**Ingestion & Storage Layer**. It serves as the primary archival system for documents in the homelab, sitting between capture tools (scanners, emails) and consumption tools (AI agents, mobile apps). It integrates with [Authentik](authentik.md) for SSO and [n8n](n8n.md) for automated workflows.

## Typical use cases
- **Household Digitization**: Storing and indexing medical records, utility bills, and tax documents.
- **Technical Library Management**: Archiving whitepapers, manuals, and schematics for quick reference.
- **AI Knowledge Grounding**: Providing a structured, searchable data source for local RAG (Retrieval-Augmented Generation) pipelines.
- **Automated Expense Tracking**: Ingesting receipts via email and automatically tagging them for financial audits.

## Strengths
- **Automated OCR**: High-quality text extraction from images and PDFs using Tesseract.
- **Machine Learning Integration**: Learns your tagging patterns over time, reducing manual effort for new documents.
- **Full-Text Search**: Fast and precise search capabilities with support for complex filters and saved views.
- **Multi-Channel Ingestion**: Supports consumption folders, email polling (IMAP), and a comprehensive REST API.

## Limitations
- **Resource Intensive**: OCR processing can be CPU-heavy, especially during bulk ingestion of large document backlogs.
- **Dependency Management**: Requires a stack including Redis and a database (PostgreSQL/MariaDB) for optimal performance.
- **OCR Limitations**: Handwritten notes or extremely low-resolution scans may have lower extraction accuracy.

## When to use it
- When you want to transition to a paperless office and need a robust, self-hosted management system.
- To maintain a private, searchable archive of sensitive personal or business documents.
- When you need a structured document source to feed into AI agent workflows.

## When not to use it
- For managing real-time collaborative documents (use [Nextcloud](nextcloud.md) or Google Docs instead).
- If you only have a few dozen documents and don't require OCR or advanced tagging capabilities.

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
Navigate to the settings to configure OpenID Connect via [Authentik](authentik.md) for centralized authentication.

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
Rebuilds the search index, useful after bulk metadata updates:
```bash
docker exec -it paperless-webserver python3 manage.py document_index reindex
```

## API examples

### Uploading a Document (curl)
```bash
curl -X POST http://localhost:8000/api/documents/post_document/ \
  -H "Authorization: Token your_api_token" \
  -F "document=@/path/to/invoice.pdf" \
  -F "title=June 2026 Utility Bill"
```

### n8n (Document Ingestion Workflow)
Import this snippet into n8n to automate uploads:
```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "http://paperless:8000/api/documents/post_document/",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBinaryData": true,
        "binaryPropertyName": "data",
        "bodyParametersUi": {
          "parameter": [
            {
              "name": "title",
              "value": "={{$node[\"Read File\"].binary.data.fileName}}"
            }
          ]
        }
      },
      "name": "Upload to Paperless",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

## Related tools / concepts
- [n8n](n8n.md) — For automating document processing and multi-service synchronization.
- [Authentik](authentik.md) — For securing the DMS with enterprise-grade SSO and MFA.
- [Nextcloud](nextcloud.md) — For syncing the consumption folder across mobile devices and desktops.
- [Vikunja](vikunja.md) — For linking tasks to specific archived documents.
- [Changedetection.io](changedetection.md) — For capturing and ingesting web snapshots as PDFs.
- [Gitea](gitea.md) — For version-controlling scripts that interact with the Paperless API.
- [Tika](tika.md) — For extracting text from complex binary formats before ingestion.
- [Ollama](ollama.md) — For local AI analysis of OCR'd text content.

## Sources / references
- [Official Website](https://docs.paperless-ngx.com/)
- [GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
