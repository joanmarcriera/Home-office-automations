# LlamaParse

## What it is
A specialized PDF parsing service from LlamaIndex designed to extract structured data from complex documents (tables, diagrams, nested layouts).

## What problem it solves
Overcomes the limitations of standard PDF text extraction by using vision-aware parsing to maintain document semantics.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing

## Typical use cases
- **Complex PDF Extraction**: Parsing documents with multi-column layouts, nested tables, and embedded diagrams.
- **Markdown-first RAG**: Converting PDFs directly to high-quality Markdown for LLM consumption.
- **Financial Report Analysis**: Extracting tabular data from annual reports and statements with high fidelity.

## Strengths
- **Vision-Aware**: Uses advanced vision models to understand document layout better than traditional OCR.
- **Markdown Output**: Optimized for LLMs, preserving hierarchies and table structures in clean Markdown.
- **Cost Optimizer**: Automatically routes simple pages to cheaper tiers while keeping complex pages on premium tiers.
- **Ecosystem Integration**: Seamlessly connects with LlamaIndex for end-to-end RAG development.

## Parsing Tiers
LlamaParse offers four tiers that trade off cost, latency, and accuracy:

| Tier | Best For | Cost (Credits/Page) |
| :--- | :--- | :---: |
| **Fast** | Plain text, single column, no tables. | 0.5 |
| **Cost Effective** | Text with simple tables; clean markdown. | 3 |
| **Agentic** | Scanned pages, multi-column, charts. | 10 |
| **Agentic Plus** | Dense financial reports, mission-critical accuracy. | 45 |

## Limitations
- **Cloud Dependency**: Primarily a cloud-based service, which may not suit air-gapped environments.
- **Latency**: High-accuracy vision-based parsing can be slower than simple text extraction.
- **Cost at Scale**: Beyond the free tier, it operates on a credit-based system that can become significant for massive datasets.

## When to use it
- When traditional PDF parsers fail on complex layouts or tables.
- When you want "LLM-ready" Markdown output without manual cleaning.
- When you are already using the LlamaIndex framework.

## When not to use it
- For simple, text-only PDFs where `PyPDF2` or `marker` would be faster and cheaper.
- If your data cannot leave your local environment (though local versions are evolving).

## Licensing and cost
- **Open Source**: No (Proprietary service)
- **Cost**: Freemium (1,000 pages per month free)
- **Self-hostable**: Limited (Docker image available for enterprise)

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
# Create a parse job using the REST API (v2)
curl -X POST 'https://api.cloud.llamaindex.ai/api/v2/parse' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \
  --data '{
    "file_id": "cafe1337-e0dd-4762-b5f5-769fef112558",
    "tier": "agentic",
    "version": "latest"
  }'

# Retrieve results (Markdown)
curl 'https://api.cloud.llamaindex.ai/api/v2/parse/{job_id}?expand=markdown' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"

# List completed jobs
curl 'https://api.cloud.llamaindex.ai/api/v2/parse?page_size=10&status=COMPLETED' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"
```

## Related tools / concepts

- [Unstructured.io](unstructured.md)
- [Docling](../process_understanding/docling.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [RAG](../../knowledge_base/patterns/rag.md)

## Sources / references
- [LlamaParse (LlamaIndex)](https://www.llamaindex.ai/llamaparse)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
