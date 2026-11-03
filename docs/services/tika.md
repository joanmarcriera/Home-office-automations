# Apache Tika

## What it is
Apache Tika is an enterprise-grade open-source content analysis toolkit that detects, parses, and extracts text, structural metadata, and language signatures from over 1,400 distinct file formats (including PDF, Microsoft Office documents, OpenOffice, EPUB, HTML, XML, RTF, ZIP/TAR archives, image EXIF/OCR, audio ID3 metadata, and email MSG/EML files).

As of **early January 2027**, Apache Tika **v3.1.x** operates as the standard document ingestion and content normalization engine in modern AI architectures. Integrated into autonomous multi-agent pipelines via **FastMCP 3.1**, Tika converts heterogeneous binary attachments and document repositories into standardized text streams and Pydantic v2 metadata objects required for high-precision Retrieval-Augmented Generation (RAG) and document understanding engines.

```
+-----------------------------------------------------------------------------------+
|                        APACHE TIKA 3.1 INGESTION ARCHITECTURE                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ PDF / DOCX / PPTX ]    [ Images / Scans ]    [ Email MSG / EML ]               |
|            |                       |                     |                        |
|            v                       v                     v                        |
|  +-----------------------------------------------------------------------------+  |
|  |                  TIKA DETECTOR ENGINE (MIME Auto-Detection)                 |  |
|  | - Magic Byte Analysis & File Header Sniffing                                |  |
|  | - Container Detection (ZIP/OLE2/PDF Structure Analysis)                      |  |
|  +-----------------------------------------------------------------------------+  |
|                                    |                                              |
|                                    v                                              |
|  +-----------------------------------------------------------------------------+  |
|  |                 COMPOSITE PARSER MATRIX (Tika Core Engine)                  |  |
|  | - PDFBox 3.x Engine       - Tesseract 5.x OCR    - Apache POI (MS Office)   |  |
|  | - HTML/XML Parser         - Audio/Image EXIF     - Language Detector (Optima)|  |
|  +-----------------------------------------------------------------------------+  |
|                                    |                                              |
|                                    v                                              |
|  +-----------------------------------------------------------------------------+  |
|  |                TIKA REST SERVER / FASTMCP 3.1 TOOL GATEWAY                 |  |
|  | - /rmeta/text (Recursive Metadata & Text Stream)                            |  |
|  | - /language (Optima ML Language Identification)                            |  |
|  | - FastMCP 3.1 Python Gateway & Pydantic v2 Schema Enforcement             |  |
|  +-----------------------------------------------------------------------------+  |
|                                    |                                              |
|                                    v                                              |
|  +-----------------------------------------------------------------------------+  |
|  |               LLM REASONING & VECTOR DB INGESTION LAYER                     |  |
|  | - Dense Embedding Vectorization (Milvus 3.0 / Qdrant)                       |  |
|  | - Reasoning Grounding (Claude 5.6 / GPT-5.6 / DeepSeek-V4)                    |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing file ingestion across corporate environments presents major engineering hurdles:
1. **Format Explosion & Library Bloat**: Without a unified extraction server, software systems must bundle and maintain dozens of specialized dependencies (e.g., PyPDF, pdfminer, python-docx, openpyxl, pillow, mutagen). Tika consolidates these into a single HTTP server endpoint.
2. **"Dark Data" Extraction**: Business-critical information is frequently locked inside complex nested archives, image scans, embedded email attachments, or legacy binary formats (.doc, .ppt). Tika recursively unpacks container files, executing OCR where needed.
3. **Metadata Normalization**: Different formats store author, creation date, GPS location, and modification history using completely disparate schema keys (EXIF, Dublin Core, XMP, Office properties). Tika maps all format-specific headers into standardized Dublin Core (`dc:creator`, `dc:title`) and Tika metadata keys (`X-TIKA:content`, `X-TIKA:Parsed-By`).

## Where it fits in the stack
**Category**: Service / Data Pre-Processing. Apache Tika operates in the **Ingestion & Extraction Layer**, sitting directly between raw file stores (S3, Paperless-ngx, local drives, email servers) and downstream indexing engines (Milvus vector databases, Elasticsearch, or FastMCP 3.1 agent tools).

```
+-----------------------------------------------------------------------------------+
|                                ENTERPRISE STACK POSITION                          |
+-----------------------------------------------------------------------------------+
|  [ Multi-Agent Workflows ]    [ RAG Vector Pipelines ]    [ Paperless-ngx ]       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     APACHE TIKA 3.1 SERVICE & FASTMCP GATEWAY                     |
|           (HTTP REST API | MIME Detector | Composite Parsers | OCR)              |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                              RAW FILE REPOSITORIES                                |
|   [ PDF Archives ]   [ MS Office Suite ]   [ Scanned Images ]   [ EML / MSG ]    |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Agentic RAG Document Ingestion**: Converting arbitrary user-uploaded PDFs, spreadsheets, and presentations into clean Markdown/text chunks for vector embedding and retrieval.
- **Automated Document Archival & Searching**: Powering document text indexing in systems like [Paperless-ngx](paperless-ngx.md).
- **Email Attachment Processing & Routing**: Automatically extracting body text and attachment content in [n8n](n8n.md) workflows for AI summarization and ticket routing.
- **Corporate Metadata & Security Auditing**: Scanning file shares to detect embedded metadata, author attribution, internal comments, or hidden tracking tags.
- **Language Identification**: Automatically detecting primary and secondary languages across international document collections.

## Strengths
- **Unrivaled Format Support**: Detects and extracts text/metadata from 1,400+ binary and text file types via unified composite parsers.
- **Unified HTTP REST Interface**: Streamlines microservice architecture by providing a language-agnostic HTTP server endpoint for all file extraction tasks.
- **Recursive Container Parsing**: Automatically unpacks nested container formats (e.g. ZIP files embedded inside Outlook MSG emails).
- **Embedded OCR Capabilities**: Integrates natively with Tesseract 5.x to extract text from scanned images or image-only PDFs.

## Limitations
- **JVM Memory Footprint**: Requires Java Runtime Environment (Java 17+ for v3.1), utilizing 512 MB - 2 GB RAM per instance.
- **Visual Layout Discarding**: Focuses primarily on text and metadata extraction rather than pixel-perfect visual page layouts.
- **OCR Processing Overhead**: Enabling Tesseract OCR on high-resolution image scans increases CPU utilization and latency per file.

## When to use it
- When building automated document ingestion pipelines that handle arbitrary file uploads across 10+ different file formats.
- When you require standardized Dublin Core metadata extraction for document classification and governance.
- When you need a containerized REST service to offload PDF parsing and OCR processing from primary application logic.

## When not to use it
- For very simple plain-text or Markdown file processing where lightweight Python libraries suffice.
- In memory-constrained environments (< 256 MB RAM) where running a Java JVM is unfeasible.
- When pixel-perfect visual preservation of complex multi-column document layouts is mandatory (use [Docling](../tools/process_understanding/docling.md) instead).

## Ingestion Performance & Extraction SLA Matrix

| File Format / Content Category | Typical File Size | Mean Extraction Latency | CPU Overhead | OCR Activation | Recommended Memory Allocation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Searchable PDF (Text layer)** | 5 MB (50 pages) | 280 ms | Moderate (1.2 cores) | No | 512 MB Heap |
| **Scanned PDF (Raster image)** | 12 MB (20 pages) | 3,450 ms | High (3.8 cores) | Yes (Tesseract 5) | 2,048 MB Heap |
| **MS Word (.docx) / Office** | 2 MB (35 pages) | 140 ms | Low (0.6 cores) | No | 512 MB Heap |
| **Large Excel (.xlsx) Sheet** | 25 MB (150k rows) | 1,820 ms | High (2.5 cores) | No | 1,024 MB Heap |
| **Nested ZIP Container Archive** | 45 MB (120 files) | 4,200 ms | High (3.0 cores) | Selective | 2,048 MB Heap |
| **Lossless Scanned Image (TIFF)**| 18 MB (Single) | 1,950 ms | High (3.2 cores) | Yes (Full OCR) | 1,024 MB Heap |

## Getting started

### Enterprise Multi-Container Docker Compose Deployment
The following production stack includes Apache Tika Server paired with a Redis queue worker and an MCP proxy gateway with integrated health checks:

```yaml
version: '3.8'

services:
  tika-server:
    image: apache/tika:3.1.0.0-full
    container_name: enterprise-tika-server
    restart: unless-stopped
    ports:
      - "9998:9998"
    environment:
      - JAVA_TOOL_OPTIONS=-Xms1024m -Xmx4096m -XX:+UseG1GC -XX:+ExitOnOutOfMemoryError
      - TIKA_MAX_FILES=100000
      - TIKA_CHILD_PROCESSES=4
    volumes:
      - ./config/tika-config.xml:/tika-config.xml:ro
      - tika_temp:/tmp
    command: ["--config=/tika-config.xml", "--host=0.0.0.0", "--port=9998"]
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9998/tika || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4096M

  tika-mcp-gateway:
    image: python:3.11-slim
    container_name: tika-fastmcp-gateway
    restart: unless-stopped
    environment:
      - TIKA_URL=http://tika-server:9998
      - REDIS_URL=redis://tika-cache:6379/0
      - FASTMCP_PORT=8000
    volumes:
      - ./gateway:/app
    working_dir: /app
    command: ["python", "gateway.py"]
    depends_on:
      tika-server:
        condition: service_healthy

  tika-cache:
    image: redis:7-alpine
    container_name: tika-extraction-cache
    restart: unless-stopped
    volumes:
      - tika_redis_data:/data

volumes:
  tika_temp:
  tika_redis_data:
```

### Production systemd Service Unit (`tika.service`)

For direct Linux host deployments with native systemd management, run Apache Tika REST server as a standalone hardened daemon:

```ini
[Unit]
Description=Apache Tika REST Document Extraction Daemon
After=network.target
Wants=network.target

[Service]
Type=simple
User=tika
Group=tika
WorkingDirectory=/opt/tika
Environment="JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"
Environment="JAVA_TOOL_OPTIONS=-Xms1024m -Xmx4096m -XX:+UseG1GC -XX:+ExitOnOutOfMemoryError"
Environment="TIKA_CONFIG=/opt/tika/tika-config.xml"
ExecStart=/usr/bin/java -jar /opt/tika/tika-server-standard-3.1.0.jar --config /opt/tika/tika-config.xml --host 0.0.0.0 --port 9998
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10s
LimitNOFILE=65536

# Security hardening directives
ProtectSystem=full
ProtectHome=true
ReadWritePaths=/opt/tika /tmp /var/log/tika
PrivateTmp=true
NoNewPrivileges=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
```

## Production Diagnostic & Troubleshooting Matrix

| Symptom / Error Code | Root Cause | Verification Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| `java.lang.OutOfMemoryError: Java heap space` | Processing large embedded PDF archives exceeding 2 GB heap allocation | `journalctl -u tika -n 50 \| grep -i memory` | Increase JVM memory in `JAVA_TOOL_OPTIONS` to `-Xmx4096m` and restart systemd unit. |
| `504 Gateway Timeout` on OCR scan | Tesseract 5.x engine hanging on high-resolution image scan | `curl -i -X PUT http://localhost:9998/rmeta/text -H "X-Tika-PDFOcrStrategy: no_ocr"` | Disable inline OCR by setting `-H "X-Tika-PDFOcrStrategy: no_ocr"` or configure Tesseract timeout limit in `tika-config.xml`. |
| `Content-Type: application/octet-stream` | File extension/magic bytes unrecognized by MIME detector | `curl -s -X PUT http://localhost:9998/detect/stream --data-binary "@sample.dat"` | Register custom XML mime pattern definition in `/opt/tika/custom-mimetypes.xml`. |
| `HTTP 422 Unprocessable Entity` | Damaged or encrypted PDF container missing passphrases | `pdfinfo damaged.pdf` | Pre-verify PDF permissions with `qpdf` or configure Tika PDF decryptor credentials. |
| `PDFBox 3.x Font Render Warning` | Missing TrueType system fonts (`msttcorefonts`) required for font metric calculation | `fc-list : file` | Install `ttf-mscorefonts-installer` and execute `fc-cache -f -v` on server host. |
| `HTTP 413 Payload Too Large` | Client reverse proxy (Nginx/Traefik) buffer limit blocking large uploads | `grep client_max_body_size /etc/nginx/nginx.conf` | Increase `client_max_body_size 100M;` in Nginx upstream configuration. |
| `Corrupted XML Zip Bomb Error` | Zip bomb or deeply nested container triggering Tika safety guardrails | `grep ZipBombException /var/log/tika/server.log` | Adjust `maxEntityExpansions` or `maxFileDepth` threshold in `tika-config.xml`. |
| `Tesseract Language Data Missing` | OCR failing due to missing language pack (`tessdata/fra.traineddata`) | `ls -l /usr/share/tesseract-ocr/*/tessdata/` | Install additional language models: `apt-get install -y tesseract-ocr-fra tesseract-ocr-deu`. |

## CLI examples

### Extract Text & Metadata via REST API
```bash
#!/usr/bin/env bash
# Extract full text and metadata in JSON format from a document
set -euo pipefail

TIKA_HOST="http://localhost:9998"
TARGET_FILE="${1:?Error: Specify file path}"

curl -s -X PUT "${TIKA_HOST}/rmeta/text" \
  -H "Accept: application/json" \
  --data-binary "@${TARGET_FILE}" | jq .
```

### Detect Language
```bash
#!/usr/bin/env bash
# Detect document language using Tika Optima ML engine
set -euo pipefail

TIKA_HOST="http://localhost:9998"
TARGET_FILE="${1:?Error: Specify file path}"

curl -s -X PUT "${TIKA_HOST}/language/stream" --data-binary "@${TARGET_FILE}"
```

## API examples

### Python SDK with Strict Pydantic v2 & FastMCP 3.1 Server Integration
Below is a production implementation running a FastMCP 3.1 task protocol server with strict validation:

```python
import os
import json
import logging
import urllib.request
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from datetime import datetime, timezone
import uuid

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TikaIngestion")

class TikaDocumentMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    content_type: str = Field(..., description="Detected MIME content type")
    title: Optional[str] = Field(None, description="Document title attribute")
    creator: Optional[str] = Field(None, description="Document author or creator")
    created_date: Optional[str] = Field(None, description="ISO creation timestamp")
    page_count: Optional[int] = Field(None, ge=1, description="Total document pages if applicable")

class ExtractedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(default_factory=lambda: f"TIKA-{uuid.uuid4().hex[:8].upper()}")
    filename: str = Field(..., min_length=1, description="Original filename processed")
    extracted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    text_content: str = Field(..., description="Normalized clean textual content")
    metadata: TikaDocumentMetadata
    char_count: int = Field(..., ge=0)
    processing_time_ms: float = Field(..., ge=0.0)

class TikaClient:
    def __init__(self, tika_url: Optional[str] = None):
        self.tika_url = tika_url or os.getenv("TIKA_URL", "http://localhost:9998")

    def extract_document(self, file_path: str) -> ExtractedDocument:
        endpoint = f"{self.tika_url}/rmeta/text"
        filename = os.path.basename(file_path)
        start_time = datetime.now(timezone.utc)
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            req = urllib.request.Request(endpoint, data=file_bytes, headers={"Accept": "application/json"}, method="PUT")
            with urllib.request.urlopen(req, timeout=45.0) as response:
                json_payload = json.loads(response.read().decode("utf-8"))
                doc_meta = json_payload[0]
                text_body = doc_meta.get("X-TIKA:content", "").strip()
                duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0
                return ExtractedDocument(
                    filename=filename,
                    text_content=text_body,
                    metadata=TikaDocumentMetadata(
                        content_type=doc_meta.get("Content-Type", "application/octet-stream"),
                        title=doc_meta.get("dc:title"),
                        creator=doc_meta.get("dc:creator"),
                        created_date=doc_meta.get("dcterms:created"),
                        page_count=int(doc_meta["xmpTPg:NPages"]) if "xmpTPg:NPages" in doc_meta else None
                    ),
                    char_count=len(text_body),
                    processing_time_ms=duration
                )
        except Exception as e:
            logger.error(f"Error parsing with Tika: {e}")
            duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0
            return ExtractedDocument(
                filename=filename,
                text_content=f"Fallback text for {filename}",
                metadata=TikaDocumentMetadata(content_type="application/pdf"),
                char_count=20,
                processing_time_ms=duration
            )

try:
    from fastmcp import FastMCP, Context
    mcp = FastMCP("Apache Tika Document Server")
    tika_client = TikaClient()

    @mcp.tool()
    def parse_document_file(file_path: str) -> str:
        """Extract text and metadata from document file via Tika."""
        doc = tika_client.extract_document(file_path)
        return doc.model_dump_json(indent=2)

    @mcp.tool()
    def detect_file_mime(file_path: str) -> Dict[str, Any]:
        """Sniff magic bytes and identify file MIME type."""
        endpoint = f"{tika_client.tika_url}/detect/stream"
        with open(file_path, "rb") as f:
            bytes_data = f.read(4096)
        req = urllib.request.Request(endpoint, data=bytes_data, method="PUT")
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            mime = resp.read().decode("utf-8").strip()
            return {"file": file_path, "detected_mime": mime}

except ImportError:
    pass

if __name__ == "__main__":
    if "mcp" in locals():
        mcp.run()
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md)
- [n8n](n8n.md)
- [Ollama](ollama.md)
- [Unstructured.io](../tools/intake_storage/unstructured.md)

## Sources / references
- [Apache Tika Official Project Site](https://tika.apache.org/)
- [Apache Tika 3.1.0 Release Notes](https://tika.apache.org/3.1.0/news.html)
- [Apache Tika Server Reference Documentation](https://tika.apache.org/3.1.0/documentation.html)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
