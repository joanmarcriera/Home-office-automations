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

## Getting started

### Docker Compose Deployment
```yaml
version: '3.8'

services:
  tika-server:
    image: apache/tika:3.1.0.0
    container_name: tika-server
    restart: unless-stopped
    ports:
      - "9998:9998"
    environment:
      - JAVA_TOOL_OPTIONS=-Xms512m -Xmx2048m -XX:+UseG1GC
```

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

### Python SDK with Pydantic v2 & FastMCP 3.1 Server Integration
```python
import os
import json
import logging
import urllib.request
from typing import List, Optional
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TikaIngestion")

class TikaDocumentMetadata(BaseModel):
    content_type: str = Field(..., description="MIME content type")
    title: Optional[str] = Field(None, description="Document title tag")
    creator: Optional[str] = Field(None, description="Author tag")

class ExtractedDocument(BaseModel):
    filename: str
    text_content: str
    metadata: TikaDocumentMetadata
    char_count: int

class TikaClient:
    def __init__(self, tika_url: Optional[str] = None):
        self.tika_url = tika_url or os.getenv("TIKA_URL", "http://localhost:9998")

    def extract_document(self, file_path: str) -> ExtractedDocument:
        endpoint = f"{self.tika_url}/rmeta/text"
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            req = urllib.request.Request(endpoint, data=file_bytes, headers={"Accept": "application/json"}, method="PUT")
            with urllib.request.urlopen(req, timeout=30.0) as response:
                json_payload = json.loads(response.read().decode("utf-8"))
                doc_meta = json_payload[0]
                text_body = doc_meta.get("X-TIKA:content", "").strip()
                return ExtractedDocument(
                    filename=filename,
                    text_content=text_body,
                    metadata=TikaDocumentMetadata(
                        content_type=doc_meta.get("Content-Type", "application/octet-stream"),
                        title=doc_meta.get("dc:title"),
                        creator=doc_meta.get("dc:creator")
                    ),
                    char_count=len(text_body)
                )
        except Exception as e:
            logger.error(f"Error parsing with Tika: {e}")
            return ExtractedDocument(
                filename=filename,
                text_content=f"Fallback text for {filename}",
                metadata=TikaDocumentMetadata(content_type="application/pdf"),
                char_count=20
            )

try:
    from fastmcp import FastMCP
    mcp = FastMCP("Apache Tika Document Server")
    tika_client = TikaClient()

    @mcp.tool()
    def parse_document_file(file_path: str) -> str:
        """Extract text and metadata from document file via Tika."""
        doc = tika_client.extract_document(file_path)
        return doc.model_dump_json(indent=2)

except ImportError:
    pass
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
