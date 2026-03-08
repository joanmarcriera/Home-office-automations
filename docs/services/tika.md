# Apache Tika

The Apache Tika toolkit detects and extracts metadata and text from over a thousand different file types.

## Description
It is useful for content analysis, search indexing, and automated document processing.

## Typical use cases
- **Document Ingestion**: Extracting text from PDFs, Word docs, and spreadsheets for LLM processing.
- **Search Indexing**: Pre-processing files to make them searchable in a database.
- **Metadata Extraction**: Identifying authors, creation dates, and other properties of files.

## When to use it
- When you need to process a wide variety of file formats (1000+ supported).
- When you need a robust, enterprise-grade extraction engine.
- When building automated RAG (Retrieval-Augmented Generation) pipelines.

## When not to use it
- For simple text files where basic reading suffices.
- If you require advanced layout-aware extraction (consider OCR-specific tools for complex scanned PDFs).

## Getting started

### Docker
Run the Tika Server using the official Docker image:

```bash
docker run -d -p 9998:9998 apache/tika
```

The server will be available at `http://localhost:9998`.

## API examples

### Extract Text
Send a file to the `/tika` endpoint:

```bash
curl -T my-document.pdf http://localhost:9998/tika --header "Accept: text/plain"
```

### Extract Metadata (JSON)
Request metadata for a file in JSON format:

```bash
curl -T my-document.pdf http://localhost:9998/meta --header "Accept: application/json"
```

### Extract Both Text and Metadata
Get a combined JSON response:

```bash
curl -T my-document.pdf http://localhost:9998/rmeta/text
```

## Links
- [Official Website](https://tika.apache.org/)

## Alternatives
- [Textract](https://aws.amazon.com/textract/) (AWS)
- [Unstructured.io](https://unstructured.io/)

## Backlog
- Integrate with n8n for automated PDF-to-Markdown conversion.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-08

## Sources / References
- https://tika.apache.org/
- https://cwiki.apache.org/confluence/display/TIKA/TikaServer
- https://aws.amazon.com/textract/
- https://unstructured.io/
