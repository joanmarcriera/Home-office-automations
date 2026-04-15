# Apache Tika

The Apache Tika toolkit detects and extracts metadata and text from over a thousand different file types.

## Description
It is useful for content analysis, search indexing, and automated document processing. It provides a single interface for parsing all these file types, making it a cornerstone for many search engines and content analysis tools.

## When to use it
- When you need to extract text and metadata from a wide variety of file formats (PPT, XLS, PDF, etc.).
- For search engine indexing where you need consistent output across different document types.
- For content analysis, translation, and language detection tasks.
- When building automated document processing pipelines.

## When not to use it
- If you only need to process a single, specific format and a lightweight, specialized library exists (e.g., just plain text).
- In extremely memory-constrained environments, as the Java-based Tika server can be resource-intensive.
- If you require the highest possible OCR accuracy and speed, specialized OCR engines may be more appropriate (though Tika integrates with Tesseract).

## Links
- [Official Website](https://tika.apache.org/)
- [Tika Wiki](https://cwiki.apache.org/confluence/display/tika)

## Alternatives
- [Textract](https://aws.amazon.com/textract/) (AWS)
- [Unstructured.io](https://unstructured.io/)
- [Pandoc](https://pandoc.org/) (mainly for document conversion)

## Getting started

### Docker installation
The easiest way to run Tika Server is via Docker:

```bash
docker run -d -p 9998:9998 --name tika apache/tika
```

Tika will be available at `http://localhost:9998`.

### Java Application (CLI)
You can also use the Tika application jar for local processing without a server:

```bash
# Download the latest tika-app jar
curl -O https://archive.apache.org/dist/tika/2.9.2/tika-app-2.9.2.jar

# Run it against a file
java -jar tika-app-2.9.2.jar --text document.pdf
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

## Backlog
- Integrate with n8n for automated PDF-to-Markdown conversion.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-02

## Sources / References
- https://tika.apache.org/
- https://aws.amazon.com/textract/
- https://unstructured.io/
- https://tika.apache.org/2.9.2/gettingstarted.html
- https://cwiki.apache.org/confluence/display/TIKA/TikaServer
