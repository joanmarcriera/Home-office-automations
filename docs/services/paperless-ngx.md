# Paperless-ngx

## What it is
Paperless-ngx is a community-supported document management system (DMS) that transforms your physical documents into a searchable online archive.

## What problem it solves
It eliminates paper clutter by providing a central, digital repository for all your documents. It handles OCR (Optical Character Recognition) automatically, making scanned PDFs and images full-text searchable, and uses machine learning to suggest tags, correspondents, and document types.

## Where it fits in the stack
**Category**: Services / Document Management. It serves as the primary "Intake & Storage" layer for scanned and digital documents in a homelab or small office.

## Typical use cases
- Digitizing household bills, receipts, and medical records.
- Storing and indexing technical manuals and whitepapers.
- Managing a paperless office with automated tagging and classification.
- Providing a searchable backend for AI agents to query household data.

## Strengths
- **Automated OCR**: High-quality text extraction from images and PDFs.
- **Machine Learning**: Learns your tagging patterns over time.
- **Searchable Archive**: Fast full-text search with support for complex queries.
- **Flexible Ingestion**: Supports consumption folders, email polling, and a REST API.

## Limitations
- **Hardware Intensive**: OCR can be CPU intensive, especially for large backlogs.
- **Complexity**: Setting up reliable email ingestion or custom workflows requires some configuration.

## When to use it
- When you want to go paperless and need a robust way to organize scanned documents.
- When you want to host your own document archive privately.

## When not to use it
- For managing highly collaborative real-time documents (use [Nextcloud](../services/nextcloud.md) or Google Docs).
- If you only have a handful of documents and don't need OCR or advanced searching.

## Getting started

### Installation (Docker Compose)
```yaml
services:
  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/usr/src/paperless/data
      - ./media:/usr/src/paperless/media
      - ./export:/usr/src/paperless/export
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

### Hello World (API)
You can ingest a document via the API using `curl`:
```bash
curl -X POST http://localhost:8000/api/documents/post_document/ \
  -H "Authorization: Token your_api_token" \
  -F "document=@/path/to/my_document.pdf" \
  -F "title=My First Document"
```

## CLI examples

### paperless-ngx manage document_exporter
Exports all documents and metadata to a directory:
```bash
docker exec -it paperless-webserver python3 manage.py document_exporter /usr/src/paperless/export
```

### paperless-ngx manage document_renamer
Renames files based on their current metadata and your storage path template:
```bash
docker exec -it paperless-webserver python3 manage.py document_renamer
```

### paperless-ngx manage document_index reindex
Rebuilds the search index, useful after bulk updates or if search seems inconsistent:
```bash
docker exec -it paperless-webserver python3 manage.py document_index reindex
```

## API examples

### Python (Listing Documents)
```python
import requests

url = "http://localhost:8000/api/documents/"
headers = {"Authorization": "Token your_api_token"}

response = requests.get(url, headers=headers)
documents = response.json()

for doc in documents['results']:
    print(f"ID: {doc['id']}, Title: {doc['title']}, Created: {doc['created']}")
```

### Python (Fetching Document Metadata)
```python
import requests

doc_id = 123
url = f"http://localhost:8000/api/documents/{doc_id}/"
headers = {"Authorization": "Token your_api_token"}

response = requests.get(url, headers=headers)
print(response.json()['content']) # Prints the OCR'd text content
```

## Licensing and cost
- **Open Source**: Yes (GPL-3.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [n8n](../services/n8n.md) (For automation workflows)
- [Vikunja](../services/vikunja.md) (For task management linked to docs)
- [Tika](../services/tika.md) (Underlying content extraction)
- [Nextcloud](../services/nextcloud.md) (Alternative storage)
- [Docspell](https://docspell.org/) (Alternative DMS)

## Sources / References
- [Official Website](https://docs.paperless-ngx.com/)
- [GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
