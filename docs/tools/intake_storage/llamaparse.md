# LlamaParse

## What it is
A specialized PDF parsing service from LlamaIndex designed to extract structured data from complex documents (tables, diagrams, nested layouts).

## What problem it solves
Overcomes the limitations of standard PDF text extraction by using vision-aware parsing to maintain document semantics.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing

## Getting started

### Installation
```bash
pip install llama-parse
```

### Basic usage
```python
import os
from llama_parse import LlamaParse

# Set up the parser
parser = LlamaParse(
    api_key="llx-...",  # can also be set via LLAMA_CLOUD_API_KEY env var
    result_type="markdown"
)

# Parse a document
documents = parser.load_data("./my_document.pdf")

# Access the content
for doc in documents:
    print(doc.text)
```

## CLI examples
LlamaParse is primarily used via its SDKs or REST API. However, it can be triggered from the LlamaIndex CLI if integrated into a RAG pipeline.

```bash
# Example of using a LlamaIndex RAG CLI that might use LlamaParse internally
llamaindex-cli rag --files "./data/*.pdf" --parse-tier agentic
```

## API examples
```bash
# Upload and parse using the REST API (v2)
curl -X POST \
  'https://api.cloud.llamaindex.ai/api/v2/parse' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \
  --data '{
    "file_id": "cafe1337-e0dd-4762-b5f5-769fef112558",
    "tier": "agentic",
    "version": "latest"
  }'
```

## Related tools / concepts

- [Actual Budget](../../services/actual-budget.md)
- [AnyType](anytype.md)
- [CalDAV](caldav.md)
- [Diskover](../../services/diskover.md)
- [Focalboard](../../services/focalboard.md)

## Sources / references
- [LlamaParse (LlamaIndex)](https://www.llamaindex.ai/llamaparse)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
