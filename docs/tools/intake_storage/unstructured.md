# Unstructured.io

## What it is
An open-source library and platform for pre-processing and "unstructuring" messy data (PDFs, HTML, Word docs, PowerPoint) into AI-ready formats. As of early January 2027, it is a foundational ETL tool for building high-quality RAG pipelines and autonomous agent context ingestion.

## What problem it solves
It automates the ingestion of diverse document types, handling complex layouts and extracting clean text, tables, and metadata. It eliminates the "garbage in, garbage out" problem by ensuring that frontier LLMs like **Claude 5.1** and **GPT-5.5** receive structured, high-signal context.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing. It acts as the "ETL for LLMs," sitting between raw data sources and vector databases or agent frameworks.

## Typical use cases
- **RAG Pipelines**: Extracting text and metadata from varied document sets for ingestion into [Weaviate](../infrastructure/weaviate.md) or [Pinecone](../infrastructure/pinecone.md).
- **Data Lake Hydration**: Normalizing disparate document formats (PDF, Word, Email) into a standard JSON/Markdown format.
- **Knowledge Graph Construction**: Extracting structured elements and relationships from messy documents.
- **Agentic Workflows**: Using the [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) to give autonomous agents real-time document parsing capabilities.

## Strengths
- **Broad Format Support**: Handles 20+ file types including PDF, HTML, Word, PowerPoint, and EPUB.
- **Open-Source & Local**: Can be run fully offline without sensitive data leaving your infrastructure.
- **Layout Awareness**: Understands complex structural headers, lists, and multi-column tables.
- **Early 2027 Optimized**: Fully supports **Llama 4** tokenization and native [FastMCP 3.1](../automation_orchestration/mcp.md) integration via the `UNS-MCP` server.

## Limitations
- **Resource Intensive**: Complex partitioning (especially with vision models / VLM strategies) requires significant CPU/GPU.
- **Dependency Heavy**: The full installation package is large and requires proper system libraries (Poppler, Tesseract).
- **Performance Variability**: Extraction quality and execution time vary based on the partitioning strategy chosen (fast vs. hi-res).

## When to use it
- When you have a high volume of diverse, messy document types requiring extraction.
- When data privacy requires local, on-premises processing of sensitive enterprise documents.
- When you need more than raw text (e.g., preserving document section hierarchy, headers, and table structures).

## When not to use it
- For very simple text files or clean Markdown where native readers suffice.
- If you need sub-millisecond, low-latency parsing (it is optimized for thorough batch and agentic document processing).

## Getting started

### Installation
```bash
pip install "unstructured[all-docs]" pydantic
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

### Partitioning Strategies
The Unstructured library offers several strategies for preprocessing documents, specified via the `strategy` parameter.

| Strategy | Type | Best For | Trade-offs |
| :--- | :--- | :--- | :--- |
| `auto` | Hybrid | Most documents | Default; balances speed and accuracy automatically. |
| `fast` | Rule-based | Plain text / clean PDFs | 100x faster than model-based; fails on tables/images. |
| `hi_res` | Model-based | Complex layouts / Tables | Highest accuracy for structural elements; slower. |
| `ocr_only` | Model-based | Scanned docs / Images | Pure OCR approach; ignores non-image text paths. |
| `vlm` | Vision-model | Challenging/Handwritten | Uses Vision Language Models for maximum semantic recovery. |

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

# Start the UNS-MCP server (FastMCP 3.1 Standard)
uvx uns_mcp --mcp-version 3.1
```

## API examples
The Unstructured REST API provides scalable document processing. Python integrations in early 2027 utilize robust **Pydantic v2** validation to model API parameters and parsed results.

### Unstructured API Payload Validation (Python)
```python
import requests
from pydantic import BaseModel, Field
from typing import Optional, List

# Define a robust Pydantic v2 model for the API requests
class UnstructuredAPIRequest(BaseModel):
    strategy: str = Field(default="hi_res", pattern="^(hi_res|fast|auto|ocr_only|vlm)$")
    coordinates: bool = Field(default=False)
    output_format: str = Field(default="application/json")
    extract_image_block_types: Optional[List[str]] = Field(default=None)
    languages: Optional[List[str]] = Field(default=None)

# Sample parameters
raw_params = {
    "strategy": "hi_res",
    "coordinates": True,
    "languages": ["eng"]
}

try:
    # Validate payload under Pydantic v2 guidelines
    validated_payload = UnstructuredAPIRequest.model_validate(raw_params)
    print(f"Successfully validated API request parameters: {validated_payload.model_dump()}")

    url = "https://api.unstructured.io/general/v0/general"
    headers = {
        "Accept": "application/json",
        "unstructured-api-key": "YOUR_API_KEY"
    }

    # Send the validated payload alongside files
    files = {"files": ("example.pdf", open("example.pdf", "rb"))}
    data = validated_payload.model_dump(mode="json")

    # response = requests.post(url, headers=headers, files=files, data=data)
except Exception as e:
    print(f"Validation failed: {e}")
```

## Related tools / concepts
- [LlamaParse](llamaparse.md) — Document parsing platform from LlamaIndex.
- [Paperless-ngx](../../services/paperless-ngx.md) — Self-hosted document management.
- [Docling](../process_understanding/docling.md) — IBM document parsing framework.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architecture for document augmentation.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Open protocol for agentic tools.
- [Claude 5.1](../providers/anthropic.md) — Frontier LLM for reasoning and synthesis.
- [GPT-5.5](../ai_knowledge/openai.md) — OpenAI frontier reasoning model.
- [Llama 4](../ai_knowledge/local_llms.md) — Open-weights local model family.
- [Weaviate](../infrastructure/weaviate.md) — Vector database for structured ingestion.
- [Khoj](khoj.md) — Personal AI knowledge search engine.

## Sources / references
- [Unstructured.io Website](https://unstructured.io/)
- [Unstructured Ingest Documentation](https://unstructured-io.github.io/unstructured/ingest/overview.html)
- [Chunking Strategies](https://unstructured-io.github.io/unstructured/core/chunking.html)
- [Unstructured MCP Server (UNS-MCP)](https://github.com/Unstructured-IO/UNS-MCP)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
