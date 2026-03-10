# Apache Tika

The Apache Tika toolkit detects and extracts metadata and text from over a thousand different file types.

## Description
It is useful for content analysis, search indexing, and automated document processing.

## Links
- [Official Website](https://tika.apache.org/)

## Alternatives
- [Textract](https://aws.amazon.com/textract/) (AWS)
- [Unstructured.io](https://unstructured.io/)

## Getting started

### Docker installation
The easiest way to run Tika Server is via Docker:

```bash
docker run -d -p 9998:9998 --name tika apache/tika
```

Tika will be available at `http://localhost:9998`.

## CLI examples

You can use the Tika Server's REST API via `curl` for command-line processing.

```bash
# Extract text from a local PDF file
curl -T document.pdf http://localhost:9998/tika

# Extract metadata from a local document in JSON format
curl -H "Accept: application/json" -T document.docx http://localhost:9998/meta

# Detect the MIME type of a file
curl -T image.png http://localhost:9998/detect/stream
```

## API examples

You can interact with the Tika Server using any HTTP client. Here is a Python example using the `requests` library:

```python
import requests

url = "http://localhost:9998/tika"
headers = {"Accept": "text/plain"}

with open("document.pdf", "rb") as f:
    response = requests.put(url, data=f, headers=headers)

print(response.text)
```

## Backlog
- Integrate with n8n for automated PDF-to-Markdown conversion.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://tika.apache.org/
- https://aws.amazon.com/textract/
- https://unstructured.io/
- https://tika.apache.org/2.9.2/gettingstarted.html
- https://cwiki.apache.org/confluence/display/TIKA/TikaServer
