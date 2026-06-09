# Unstructured.io

## What it is
An open-source library and platform for pre-processing and "unstructuring" messy data (PDFs, HTML, Word docs) into AI-ready formats. It is a foundational tool for building high-quality RAG pipelines.

## What problem it solves
It automates the ingestion of diverse document types, handling complex layouts and extracting clean text and metadata. It eliminates the "garbage in, garbage out" problem by ensuring that LLMs like **Claude 4.7** and **GPT-5.5** receive structured, high-signal context.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing. It acts as the "ETL for LLMs," sitting between raw data sources and vector databases.

## Typical use cases
- **RAG Pipelines**: Extracting text and metadata from varied document sets for ingestion into [Weaviate](../infrastructure/weaviate.md) or [Pinecone](../infrastructure/pinecone.md).
- **Data Lake Hydration**: Normalizing disparate document formats (PDF, Word, Email) into a standard JSON/Markdown format.
- **Knowledge Graph Construction**: Extracting structured elements and relationships from messy documents.
- **Agentic Workflows**: Using the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) to give agents real-time parsing capabilities.

## Strengths
- **Broad Format Support**: Handles 20+ file types including PDF, HTML, Word, and PowerPoint.
- **Open-Source & Local**: Can be run fully offline without data leaving your infrastructure.
- **Layout Awareness**: Not just OCR; it understands headers, lists, and tables.
- **June 2026 Optimized**: Fully supports **Llama 4 Maverick** tokenization and native [MCP](../automation_orchestration/mcp.md) integration via the `UNS-MCP` server.

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

## Partitioning Strategies
The Unstructured library offers several strategies for preprocessing documents, specified via the `strategy` parameter.

| Strategy | Type | Best For | Trade-offs |
| :--- | :--- | :--- | :--- |
| `auto` | Hybrid | Most documents | Default; balances speed and accuracy automatically. |
| `fast` | Rule-based | Plain text / clean PDFs | 100x faster than model-based; fails on tables/images. |
| `hi_res` | Model-based | Complex layouts / Tables | Highest accuracy for structural elements; slower. |
| `ocr_only` | Model-based | Scanned docs / Images | Pure OCR approach; ignores non-image text paths. |
| `vlm` | Vision-model | Challenging/Handwritten | Uses Vision Language Models for maximum semantic recovery. |

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

### Python S3 Ingestion Example
```python
import os
from unstructured.ingest.connector.s3 import S3AccessConfig, SimpleS3Config
from unstructured.ingest.interfaces import ProcessorConfig, ReadConfig
from unstructured.ingest.runner import S3Runner

# Set credentials via env vars or S3AccessConfig
os.environ["AWS_ACCESS_KEY_ID"] = "YOUR_KEY"
os.environ["AWS_SECRET_ACCESS_KEY"] = "YOUR_SECRET"

runner = S3Runner(
    processor_config=ProcessorConfig(
        verbose=True,
        output_dir="s3-output",
        num_processes=2,
        reprocess=False # Skip files already processed
    ),
    read_config=ReadConfig(),
    connector_config=SimpleS3Config(
        access_config=S3AccessConfig(),
        remote_url="s3://my-bucket/documents/",
        recursive=True
    ),
)

runner.run()
```

### Advanced Pipeline: Chunking for RAG
```python
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

elements = partition_pdf(
    filename="research_paper.pdf",
    strategy="hi_res",
    extract_images_in_pdf=False,
    infer_table_structure=True,
    chunking_strategy="by_title",
    max_characters=1000,
    combine_text_under_n_chars=200
)

# Access clean, structured chunks
for chunk in elements:
    print(f"Type: {chunk.category}")
    print(f"Content: {chunk.text[:50]}...")
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
  --output-dir s3-output \
  --anonymous \
  --recursive

# Start the UNS-MCP server (June 2026)
uvx uns_mcp
```

## API examples
```python
import requests

url = "https://api.unstructured.io/general/v0/general"
headers = {"Accept": "application/json", "unstructured-api-key": "YOUR_API_KEY"}
files = {"files": open("example.pdf", "rb")}

# Add strategy and coordinates parameters
data = {
    "strategy": "hi_res",
    "coordinates": "true"
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

## Related tools / concepts

- [LlamaParse](llamaparse.md)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Docling](../process_understanding/docling.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude 4.7](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)
- [Weaviate](../infrastructure/weaviate.md)

## Sources / references
- [Unstructured.io Website](https://unstructured.io/)
- [Unstructured Ingest Documentation](https://unstructured-io.github.io/unstructured/ingest/overview.html)
- [Chunking Strategies](https://unstructured-io.github.io/unstructured/core/chunking.html)
- [Unstructured MCP Server (UNS-MCP)](https://github.com/Unstructured-IO/UNS-MCP)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
