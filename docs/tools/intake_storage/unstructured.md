# Unstructured.io

## What it is
An open-source library and platform for pre-processing and "unstructuring" messy data (PDFs, HTML, Word docs) into AI-ready formats.

## What problem it solves
It automates the ingestion of diverse document types, handling complex layouts and extracting clean text and metadata for RAG pipelines.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing

## Typical use cases
- **RAG Pipelines**: Extracting text and metadata from varied document sets for vector database ingestion.
- **Data Lake Hydration**: Normalizing disparate document formats (PDF, Word, Email) into a standard JSON/Markdown format.
- **Knowledge Graph Construction**: Extracting structured elements and relationships from messy documents.

## Strengths
- **Broad Format Support**: Handles 20+ file types including PDF, HTML, Word, and PowerPoint.
- **Open-Source & Local**: Can be run fully offline without data leaving your infrastructure.
- **Layout Awareness**: Not just OCR; it understands headers, lists, and tables.

## Limitations
- **Resource Intensive**: Complex partitioning (especially with vision models) requires significant CPU/GPU.
- **Dependency Heavy**: The "all-docs" installation is large and can have version conflicts.
- **Performance Variability**: Extraction quality can vary significantly based on the partitioning strategy chosen (fast vs. hi-res).

## When to use it
- When you have a high volume of diverse, messy document types.
- When data privacy requires local processing of sensitive documents.
- When you need more than just raw text (e.g., you need to preserve document structure).

## When not to use it
- For very simple text files or clean Markdown where standard readers suffice.
- If you need real-time, low-latency parsing (it is optimized for batch ETL).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (Self-hosted) / Paid (Unstructured API / Platform)
- **Self-hostable**: Yes

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

- [LlamaParse](llamaparse.md)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Docling](../process_understanding/docling.md)
- [RAG](../../knowledge_base/patterns/rag.md)

## Sources / references
- [Unstructured.io Website](https://unstructured.io/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
