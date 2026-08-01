# Apache Tika

## What it is
Apache Tika is a versatile, open-source content analysis toolkit that detects and extracts metadata and text from over a thousand different file types (e.g., PDF, PPT, XLS, DOCX). In late October / November 2026, version **3.1.x** is the industry standard for "Agentic Ingestion," providing the structured text extraction layer required for high-fidelity RAG (Retrieval-Augmented Generation) pipelines and autonomous document understanding.

## What problem it solves
Diverse file formats require specialized libraries for text extraction, leading to fragmented and complex ingestion pipelines. Tika simplifies this by providing a unified "parser of parsers." It solves the "dark data" problem by allowing autonomous agents (Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, Qwen 3.6) to "read" inside binary files, extract deeply embedded metadata, and identify the language of the content automatically without requiring specific format expertise.

## Where it fits in the stack
**Category**: Service / Data Processing. It sits in the **data ingestion and extraction layer**, acting as a critical pre-processor that converts unstructured binary documents into the clean text and metadata required by search engines, vector databases, and LLMs like **Gemma 3** or **Claude 5.1**.

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
- **Open Source (Apache 2.0)**: Fully free for personal and commercial use without licensing costs.

## Limitations
- **JVM Dependency**: Requires a Java runtime environment (Java 17+ for v3.1), which can be memory-intensive in small containers.
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

## Getting started

### Docker: Tika Server 3.1 Baseline
The easiest way to deploy Tika for homelab use is via Docker:

```bash
docker run -d -p 9998:9998 --name tika apache/tika:3.1.0.0
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
curl -O https://archive.apache.org/dist/tika/3.1.0/tika-app-3.1.0.jar

# Extract text from a local PDF
java -jar tika-app-3.1.0.jar --text my-document.pdf

# List all available parsers and their supported types
java -jar tika-app-3.1.0.jar --list-parsers

# Detect the language of a document
java -jar tika-app-3.1.0.jar --language my-document.pdf
```

## API examples
Interact with Tika Server via any HTTP-capable client. Below is a Python API validator utilizing Pydantic v2 to structure extracted document text and metadata.

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any

# Define document metadata schemas using Pydantic v2
class DocumentPayload(BaseModel):
    text_content: str = Field(..., alias="X-TIKA:content", description="The main textual body extracted from the document")
    author: Optional[str] = Field(None, alias="dc:creator", description="The author metadata tag if available")
    content_type: str = Field(..., alias="Content-Type", description="The mime content type detected by Tika")
    language: Optional[str] = Field(None, alias="language", description="The primary language detected")

    # Coerce fields and handle fallback fields gracefully in Pydantic v2
    @classmethod
    def from_tika_response(cls, raw_data: List[Dict[str, Any]]) -> "DocumentPayload":
        if not raw_data:
            raise ValueError("Empty response metadata received from Tika server")
        main_doc = raw_data[0]
        return cls(
            **{
                "X-TIKA:content": main_doc.get("X-TIKA:content", "").strip(),
                "dc:creator": main_doc.get("dc:creator") or main_doc.get("Author"),
                "Content-Type": main_doc.get("Content-Type", "application/octet-stream"),
                "language": main_doc.get("language")
            }
        )

def extract_document_features(file_path: str, tika_url: str = "http://localhost:9998/rmeta/text") -> DocumentPayload:
    with open(file_path, "rb") as f:
        headers = {"Accept": "application/json"}
        response = requests.put(tika_url, data=f, headers=headers)

    response.raise_for_status()
    payload = response.json()
    return DocumentPayload.from_tika_response(payload)

# Example usage
if __name__ == "__main__":
    doc_file = "sample.pdf"
    # validated_metadata = extract_document_features(doc_file)
    # print(f"Type: {validated_metadata.content_type}, Language: {validated_metadata.language}")
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — Uses Tika for document indexing and search.
- [n8n](n8n.md) — For orchestrating file ingestion workflows that utilize Tika.
- [Ollama](ollama.md) — For processing Tika-extracted text with local LLMs.
- Nextcloud — For managing the files being processed by Tika.
- [Whisper](whisper.md) — For complementary audio/video transcription.
- [Unstructured.io](../tools/intake_storage/unstructured.md) — A modern alternative for document extraction in AI pipelines.
- [Authentik](authentik.md) — For securing access to Tika endpoints.
- [Tailscale](tailscale.md) — For secure remote access to Tika servers.

## Sources / References
- [Apache Tika Official Project Site](https://tika.apache.org/)
- [Apache Tika Server Reference Documentation](https://tika.apache.org/3.1.0/documentation.html)
- [Apache Tika Git Repository](https://github.com/apache/tika)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2026-11-08
- Confidence: high
