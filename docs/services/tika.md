# Apache Tika

## What it is
Apache Tika is a versatile, open-source content analysis toolkit that detects and extracts metadata and text from over a thousand different file types (e.g., PDF, PPT, XLS, DOCX). In June 2026, version **3.0** has become the industry standard for "Agentic Ingestion," providing the structured text extraction layer required for high-fidelity RAG (Retrieval-Augmented Generation) pipelines.

## What problem it solves
Diverse file formats require specialized libraries for text extraction, leading to fragmented and complex ingestion pipelines. Tika simplifies this by providing a unified "parser of parsers." It solves the "dark data" problem by allowing autonomous agents to "read" inside binary files, extract deeply embedded metadata, and identify the language of the content automatically.

## Where it fits in the stack
**Category**: Service / Data Processing. It sits in the **data ingestion and extraction layer**, acting as a critical pre-processor that converts unstructured binary documents into the clean text and metadata required by search engines and LLMs.

## Typical use cases
- **Agentic RAG Pipelines**: Converting local PDF archives into structured text for indexing in vector databases.
- **Automated Document Archival**: Using [Paperless-ngx](paperless-ngx.md) (which utilizes Tika) to organize and search physical document scans.
- **Email Attachment Processing**: Automatically extracting text from incoming email attachments in [n8n](n8n.md) for routing and summarization.
- **Metadata Auditing**: Analyzing large file stores to identify sensitive PII or document ownership for governance.
- **Language Identification**: Automatically tagging document collections by language for specialized translation workflows.

## Strengths
- **Unrivaled Format Support**: Extracts text and metadata from almost any file type in existence.
- **Unified REST API**: Simplifies integration with any language or automation tool via a single HTTP interface.
- **Deep Metadata Extraction**: Retrieves author, creation date, GPS coordinates, and more from embedded file headers.
- **Native OCR Integration**: Can automatically trigger Tesseract OCR for images or "image-only" PDFs during extraction.
- **High Performance (v3.0)**: Optimized JVM settings and modular parser configurations for high-throughput batch processing.

## Limitations
- **JVM Dependency**: Requires a Java runtime environment (Java 17+ for v3.0), which can be memory-intensive in small containers.
- **Formatting Loss**: Primarily focuses on text extraction; original visual layouts and styles are generally discarded.
- **OCR Overhead**: Enabling OCR significantly increases processing time and resource consumption.

## When to use it
- When you need to extract text from a wide variety of document formats for use in search engines or LLMs.
- For building automated document ingestion pipelines that must handle arbitrary file uploads.
- When you require deep metadata extraction for document classification and governance.
- To add OCR capabilities to your file processing workflow via a unified interface.

## When not to use it
- For very simple plain-text or Markdown processing where a lightweight library suffices.
- In extremely memory-constrained environments where a JVM-based service is not feasible.
- If you require pixel-perfect visual preservation of document layouts.

## Licensing and cost
- **Licensing**: Open Source (Apache 2.0).
- **Cost**: Free.
- **Self-hostable**: Yes, officially supported via Docker and binary JAR files.

## Getting started

### Docker: Tika Server 3.0 Baseline
The easiest way to deploy Tika for homelab use is via Docker:

```bash
docker run -d -p 9998:9998 --name tika apache/tika:3.0.0.0
```

### Hello World (REST API)
1. Ensure the Tika container is running.
2. Create a test text file: `echo "Hello Apache Tika" > test.txt`.
3. Send it to the Tika API: `curl -T test.txt http://localhost:9998/tika`.
4. Tika will return the extracted text: `Hello Apache Tika`.

## CLI examples
Use the `tika-app` JAR for local, non-server processing.

```bash
# Download the latest app JAR
curl -O https://archive.apache.org/dist/tika/3.0.0/tika-app-3.0.0.jar

# Extract text from a local PDF
java -jar tika-app-3.0.0.jar --text my-document.pdf

# List all available parsers and their supported types
java -jar tika-app-3.0.0.jar --list-parsers

# Detect the language of a document
java -jar tika-app-3.0.0.jar --language my-document.pdf
```

## API examples
Interact with Tika Server via any HTTP-capable client.

### Python: Extracting Text and Metadata
```python
import requests
import json

URL = "http://localhost:9998/rmeta/text"

with open("document.pdf", "rb") as f:
    headers = {"Accept": "application/json"}
    response = requests.put(URL, data=f, headers=headers)

data = response.json()
print(f"Extracted Text: {data[0]['X-TIKA:content']}")
print(f"Author: {data[0].get('dc:creator', 'Unknown')}")
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — Uses Tika for document indexing and search.
- [n8n](n8n.md) — For orchestrating file ingestion workflows that utilize Tika.
- [Ollama](ollama.md) — For processing Tika-extracted text with local LLMs.
- [Nextcloud](nextcloud.md) — For managing the files being processed by Tika.
- [Whisper](whisper.md) — For complementary audio/video transcription.
- [Unstructured.io](../tools/process_understanding/unstructured.md) — A modern alternative for document extraction in AI pipelines.
- [Supabase](../tools/infrastructure/supabase.md) — For storing vector embeddings of Tika-extracted text.
- [Authentik](authentik.md) — For securing access to Tika endpoints.
- [Tailscale](tailscale.md) — For secure remote access to Tika servers.
- [Claude](../tools/ai_knowledge/claude.md) — Agent used for processing extracted text.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — The underlying engine used by Tika for images.

## Sources / References
- [Official Website](https://tika.apache.org/)
- [Tika Documentation](https://tika.apache.org/3.0.0/documentation.html)
- [Tika GitHub](https://github.com/apache/tika)
- [Tika Server Wiki](https://cwiki.apache.org/confluence/display/TIKA/TikaServer)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
