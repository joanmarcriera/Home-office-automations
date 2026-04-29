# Unstructured.io

## What it is
An open-source library and platform for pre-processing and "unstructuring" messy data (PDFs, HTML, Word docs) into AI-ready formats.

## What problem it solves
It automates the ingestion of diverse document types, handling complex layouts and extracting clean text and metadata for RAG pipelines.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing

## Getting started

### Installation
```bash
pip install "unstructured[all-docs]"
```

### Basic usage
```python
from unstructured.partition.auto import partition

elements = partition(filename="example.pdf")

for element in elements:
    print(element)
```

## CLI examples
```bash
# Process a local directory and output JSON
unstructured-ingest local \
  --input-path example-docs \
  --output-dir unstructured-output \
  --num-processes 2 \
  --recursive \
  --verbose

# Process from S3 (requires [s3] extra)
unstructured-ingest s3 \
  --remote-url s3://my-bucket/documents/ \
  --output-dir s3-output
```

## API examples
```python
import requests

url = "https://api.unstructured.io/general/v0/general"
headers = {"Accept": "application/json", "unstructured-api-key": "YOUR_API_KEY"}
files = {"files": open("example.pdf", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

## Related tools / concepts

- [Actual Budget](../../services/actual-budget.md)
- [AnyType](anytype.md)
- [CalDAV](caldav.md)
- [Diskover](../../services/diskover.md)
- [Focalboard](../../services/focalboard.md)

## Sources / references
- [Unstructured.io Website](https://unstructured.io/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
