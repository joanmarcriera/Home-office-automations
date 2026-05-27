# Apache Tika

## What it is

The Apache Tika toolkit is an open-source library that detects and extracts metadata and text from over a thousand different file types (such as PPT, XLS, and PDF). It provides a single, unified interface for parsing complex document formats, making it a foundational tool for search engines and content analysis systems.

## What problem it solves

Processing diverse file formats requires specialized libraries for each type (e.g., PDFBox for PDFs, POI for Office docs). Tika simplifies this by abstracting the complexity behind a single API. It solves the problem of "dark data" by allowing automated systems to "see" inside binary files to extract searchable text and structured metadata.

## Where it fits in the stack

**Category**: Service / Data Processing. It sits in the **data ingestion and extraction** layer, acting as a pre-processor that converts unstructured binary documents into structured text that can be indexed by search engines (like Solr or Elasticsearch) or processed by LLMs.

## Typical use cases

- **Search Indexing**: Extracting text from uploaded PDFs and Word docs for a searchable knowledge base.
- **Content Analysis**: Identifying the language and metadata (author, creation date) of large file archives.
- **RAG Pre-processing**: Converting diverse document formats into plain text for use in Retrieval-Augmented Generation pipelines (often feeding into [Ollama](ollama.md) or [LiteLLM](litellm.md)).
- **Attachment Processing**: Automatically extracting text from email attachments for automated routing or classification in [n8n](n8n.md).

## Strengths

- **Universal Parser**: Supports an incredible range of formats out of the box.
- **Metadata Rich**: Extracts not just text, but deeply embedded metadata.
- **Language Detection**: Built-in ability to identify the language of the extracted text.
- **OCR Integration**: Can automatically trigger Tesseract OCR for images or "image-only" PDFs.
- **Modular Architecture (v3.0+)**: Highly customizable parser configurations and reduced footprint for specialized deployments.

## Limitations

- **Java Based**: The core library and server run on the JVM, which can be memory-intensive. Requires Java 11+ as of version 3.0.
- **Formatting Loss**: Focuses on text extraction; original visual formatting and layout are typically lost.
- **Complex Setup**: Configuring specialized parsers (like OCR or deep object recognition) can require significant effort.

## When to use it

- When you need to extract text and metadata from a wide variety of file formats (PPT, XLS, PDF, etc.).
- For search engine indexing where you need consistent output across different document types.
- For content analysis, translation, and language detection tasks.
- When building automated document processing pipelines.

## When not to use it

- If you only need to process a single, specific format and a lightweight, specialized library exists (e.g., just plain text).
- In extremely memory-constrained environments, as the Java-based Tika server can be resource-intensive.
- If you require the highest possible OCR accuracy and speed, specialized OCR engines may be more appropriate (though Tika integrates with Tesseract).

## Getting started

### Docker installation (Tika 3.0 Baseline)
The easiest way to run Tika Server is via Docker:

```bash
docker run -d -p 9998:9998 --name tika apache/tika:3.0.0.0
```

Tika will be available at `http://localhost:9998`.

### Java Application (CLI)
You can also use the Tika application jar for local processing without a server:

```bash
# Download the latest tika-app jar (v3.0.0)
curl -O https://archive.apache.org/dist/tika/3.0.0/tika-app-3.0.0.jar

# Run it against a file
java -jar tika-app-3.0.0.jar --text document.pdf
```

### Hello World
1. Ensure the Tika Docker container is running: `docker ps | grep tika`
2. Create a test file: `echo "Hello Tika World" > test.txt`
3. Send it to Tika's REST API: `curl -T test.txt http://localhost:9998/tika`
4. Tika should return the extracted text: `Hello Tika World`

## CLI examples

You can use the Tika Server's REST API via `curl` or use the `tika-app` JAR for command-line processing.

```bash
# Extract text from a local PDF file using Tika Server
curl -T document.pdf http://localhost:9998/tika

# Extract metadata from a local document in JSON format
curl -H "Accept: application/json" -T document.docx http://localhost:9998/meta

# Detect the MIME type of a file
curl -T image.png http://localhost:9998/detect/stream

# List all available parsers (using tika-app)
java -jar tika-app.jar --list-parsers
```

## API examples

You can interact with the Tika Server using any HTTP client.

### Python (using requests)
```python
import requests

url = "http://localhost:9998/tika"
headers = {"Accept": "text/plain"}

with open("document.pdf", "rb") as f:
    response = requests.put(url, data=f, headers=headers)

print(response.text)
```

### Recursive Metadata (curl)
The `/rmeta` endpoint is powerful for getting metadata and text from both the container and all embedded documents (e.g., images inside a Word doc).

```bash
curl -T document.docx http://localhost:9998/rmeta/text --header "Accept: application/json"
```

## n8n Integration: Automated PDF-to-Markdown

Tika is frequently used as a core node in [n8n](n8n.md) workflows to convert incoming attachments into a format suitable for LLM processing or archival.

### Workflow Pattern: Email Attachment to Markdown
1.  **IMAP Email Trigger**: Watch for new emails with PDF attachments.
2.  **HTTP Request Node (Tika)**:
    - **Method**: `PUT`
    - **URL**: `http://tika:9998/tika`
    - **Body**: Attachment binary data.
    - **Headers**: `Accept: text/plain`.
3.  **Code Node (Formatting)**: Clean up the raw text and wrap it in Markdown headers or metadata blocks.
4.  **Vector Store / Storage**: Send the Markdown text to [Supabase](../tools/infrastructure/supabase.md) or save it as a file in [Nextcloud](nextcloud.md).

### Example Code Node (JS)
```javascript
// Clean up Tika output for Markdown
const rawText = $node["HTTP Request"].data["text"];
const fileName = $node["IMAP Email"].data["attachment"]["name"];

const markdown = `
# Document: ${fileName}
## Extracted Content
${rawText.replace(/\n{3,}/g, '\n\n')}
`;

return [{ json: { markdown } }];
```

## Related tools / concepts

- [Unstructured.io](../tools/process_understanding/unstructured.md) — a modern alternative for document processing in AI pipelines
- [Paperless-ngx](paperless-ngx.md) — uses Tika/OCR for document archival and searching
- [Ollama](ollama.md) — for processing Tika-extracted text with local LLMs
- [Whisper](whisper.md) — for complementary audio/video transcription
- [ChangeDetection.io](changedetection.md) — can trigger Tika when specific document links change
- [Elasticsearch](https://www.elastic.co/) — often used to store and search the text extracted by Tika
- [n8n](n8n.md) — for building automated workflows that trigger Tika on new file uploads
- [Pandoc](https://pandoc.org/) — for converting between document formats (Tika extracts, Pandoc converts)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — the engine Tika uses for optical character recognition

## Sources / References

- [Official Website](https://tika.apache.org/)
- [Tika Wiki](https://cwiki.apache.org/confluence/display/tika)
- [Unstructured.io](https://unstructured.io/)
- [Tika Server Documentation](https://cwiki.apache.org/confluence/display/TIKA/TikaServer)

## Backlog
- [x] Perform quarterly technical freshness audit (2026-05-27).

## Contribution Metadata

- Last reviewed: 2026-05-27
- Confidence: high
