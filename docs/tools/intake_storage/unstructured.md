# Unstructured.io

## What it is
Unstructured.io is an open-source data pre-processing platform and Python library engineered to transform messy, un-structured enterprise documents (PDFs, PPTX, DOCX, HTML, EPUB, scanned images) into clean, LLM-ready structured text, JSON, and Markdown. In early 2027, Unstructured serves as a critical document intake engine for autonomous agent frameworks, Retrieval-Augmented Generation (RAG) vector stores, and enterprise knowledge indexing pipelines.

## What problem it solves
Raw enterprise documents suffer from inconsistent formatting, complex visual elements, embedded multi-column tables, scanned OCR artifacts, and ambiguous structural headers. Traditional plain-text extractors lose layout context, scramble tabular structures, and obscure parent-child document hierarchies. Unstructured eliminates this "garbage-in, garbage-out" problem by partitioning raw binary files using multi-modal layout detection, semantic vision models, and table structure inference—ensuring frontier LLMs like **Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, and **Gemini 4.0 Ultra** receive clean, contextually intact chunks.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing. It operates as the "ETL for LLMs and Agents," sitting directly between multi-modal raw document stores (S3, MinIO, Google Drive, SharePoint) and downstream vector databases ([Weaviate](../infrastructure/weaviate.md), [Qdrant](../infrastructure/qdrant.md), [Pinecone](../infrastructure/pinecone.md)) or agent memory layers ([mem0](../agents/mem0.md)).

## Architecture Diagram
```
+-----------------------------------------------------------------------------------+
|                            Unstructured.io Processing Engine                      |
|                                                                                   |
|  +--------------------+    +----------------------+    +-----------------------+  |
|  | Raw Document Input |===>| Document Partition   |===>| Strategy Selector     |  |
|  | (PDF, DOCX, PPTX)  |    | (Auto-Detection Engine|    | (Fast, Hi-Res, VLM)   |  |
|  +--------------------+    +----------------------+    +-----------------------+  |
|                                                                   ||              |
|                                                                   \/              |
|  +--------------------+    +----------------------+    +-----------------------+  |
|  | Vector Store / RAG |<===| Chunking & Element   |<===| Vision / OCR / Layout |  |
|  | Ingestion Engine   |    | Metadata Annotation  |    | Inference Model       |  |
|  +--------------------+    +----------------------+    +-----------------------+  |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 FastMCP 3.1 Tool Server Interface (UNS-MCP)                 |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Enterprise RAG Ingestion**: Partitioning thousands of complex technical PDFs with multi-column layouts and embedded diagrams into structured vector embeddings.
- **Data Lake Normalization**: Continuous batch intake converting heterogeneous file stores into unified Markdown/JSON schemas.
- **Knowledge Graph Extraction**: Extracting structural headers, sub-sections, and inline table matrices to seed graph database nodes.
- **Agentic Document Analysis**: Providing autonomous agents with real-time, on-demand document parsing via the FastMCP 3.1 protocol (`UNS-MCP`).

## Strengths
- **Broad Format Coverage**: Native partition support for over 20 document formats (PDF, DOCX, PPTX, HTML, MSG, EML, EPUB, XLSX, TXT).
- **Strategy Flexibility**: Tailored execution modes ranging from high-speed rule-based string parsing (`fast`) to deep Vision Language Model layout understanding (`vlm`).
- **Rich Metadata Extraction**: Enriches parsed elements with section titles, page numbers, coordinates, parent sub-headers, and file tags.
- **FastMCP 3.1 & Agent Native**: Direct integration with agentic tool protocol servers (`UNS-MCP`), allowing LLM agents to execute document partitioning tool calls.

## Limitations
- **High Resource Requirements for Hi-Res Mode**: Processing scanned documents or complex PDFs using layout vision models requires substantial GPU/CPU resources.
- **Heavy System Dependencies**: Native execution requires low-level system binaries (Poppler, Tesseract OCR, Libmagic) for full multi-file support.
- **Latency Trade-Offs**: Complex vision-based partitioning strategies introduce processing latency that requires batch processing or background execution.

## When to use it
- When ingestion sources contain mixed, unstructured formats (scanned documents, corporate decks, complex financial spreadsheets).
- When document structure, tables, and section hierarchies must be preserved for accurate semantic chunking.
- When giving autonomous agents real-time tool access to inspect and digest external file attachments.

## When not to use it
- For plain, uniform markdown or clean JSON where basic text string splits are sufficient.
- When sub-millisecond document parsing is strictly required without background queuing.

## Getting started

### Installation
```bash
pip install "unstructured[all-docs]" pydantic fastmcp
```

### Basic Usage
```python
from unstructured.partition.auto import partition

# Partition file using automatic format detection
elements = partition(filename="quarterly_report.pdf")

for element in elements:
    print(f"[{element.category}] {element.text[:100]}...")
```

### Advanced Ingestion Pipeline with S3 Connector
```python
import os
from unstructured.ingest.connector.s3 import S3AccessConfig, SimpleS3Config
from unstructured.ingest.interfaces import ProcessorConfig, ReadConfig
from unstructured.ingest.runner import S3Runner

# Configure S3 connector for automated document intake
runner = S3Runner(
    processor_config=ProcessorConfig(
        verbose=True,
        output_dir="s3-unstructured-output",
        num_processes=4,
        reprocess=False
    ),
    read_config=ReadConfig(),
    connector_config=SimpleS3Config(
        access_config=S3AccessConfig(
            key=os.getenv("AWS_ACCESS_KEY_ID"),
            secret=os.getenv("AWS_SECRET_ACCESS_KEY")
        ),
        remote_url="s3://enterprise-documents/2027/q1/",
        recursive=True
    ),
)

runner.run()
```

### Partitioning Strategies Matrix
| Strategy | Type | Best For | Trade-offs |
| :--- | :--- | :--- | :--- |
| `auto` | Hybrid | Mixed file types | Balances speed and accuracy automatically. |
| `fast` | Rule-based | Clean digital PDFs & text | 100x faster than model-based; bypasses visual layout/tables. |
| `hi_res` | Layout Model | Complex multi-column PDFs | High layout accuracy; higher CPU/GPU overhead. |
| `ocr_only` | OCR Engine | Scanned PDFs & image files | Recovers text from rasterized pixels; requires Tesseract/Paddle. |
| `vlm` | Vision LLM | Complex diagrams & tables | Maximum semantic recovery; relies on vision inference calls. |

## CLI examples
```bash
# Ingest local directory with multi-process processing
unstructured-ingest local \
  --input-path ./raw-documents \
  --output-dir ./parsed-output \
  --num-processes 4 \
  --recursive \
  --verbose

# Run FastMCP 3.1 server for agentic document processing
uvx uns_mcp --mcp-version 3.1
```

## API examples
The following complete code snippet demonstrates running an Unstructured FastMCP 3.1 tool server integration alongside Pydantic v2 validation models for enterprise document partitioning requests:

```python
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP

# 1. Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="unstructured-ingestion-server",
    version="3.1"
)

# 2. Define Pydantic v2 Partitioning Request Model
class PartitionRequestSchema(BaseModel):
    file_path: str = Field(..., description="Absolute path to the file to process")
    strategy: str = Field(default="auto", description="Partitioning strategy: auto, fast, hi_res, ocr_only, vlm")
    chunk_by_title: bool = Field(default=True, description="Whether to chunk elements by document titles")
    max_characters: int = Field(default=1500, ge=100, le=8000, description="Maximum characters per chunk")

    @field_validator("strategy")
    @classmethod
    def validate_strategy(cls, v: str) -> str:
        allowed = {"auto", "fast", "hi_res", "ocr_only", "vlm"}
        if v not in allowed:
            raise ValueError(f"Strategy must be one of {allowed}")
        return v

# 3. Define Pydantic v2 Output Response Model
class DocumentElementSchema(BaseModel):
    element_id: str = Field(..., description="Unique element identifier")
    category: str = Field(..., description="Element category (e.g. Title, NarrativeText, Table)")
    text: str = Field(..., description="Extracted text string")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extracted element metadata")

class PartitionResponseSchema(BaseModel):
    success: bool
    total_elements: int
    elements: List[DocumentElementSchema]
    error_message: Optional[str] = None

# 4. Expose FastMCP 3.1 Tool
@mcp.tool(name="partition_document", description="Partition a document into structured elements and chunks")
def partition_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    """FastMCP 3.1 tool endpoint for document partitioning."""
    try:
        # Validate input with Pydantic v2
        request = PartitionRequestSchema.model_validate(payload)

        if not os.path.exists(request.file_path):
            return PartitionResponseSchema(
                success=False,
                total_elements=0,
                elements=[],
                error_message=f"File not found: {request.file_path}"
            ).model_dump()

        from unstructured.partition.auto import partition
        from unstructured.chunking.title import chunk_by_title

        raw_elements = partition(
            filename=request.file_path,
            strategy=request.strategy
        )

        if request.chunk_by_title:
            processed_elements = chunk_by_title(
                raw_elements,
                max_characters=request.max_characters
            )
        else:
            processed_elements = raw_elements

        parsed_items = []
        for idx, el in enumerate(processed_elements):
            parsed_items.append(
                DocumentElementSchema(
                    element_id=getattr(el, "id", f"el-{idx}"),
                    category=getattr(el, "category", "Uncategorized"),
                    text=str(el),
                    metadata=getattr(el, "metadata", {}).to_dict() if hasattr(getattr(el, "metadata", None), "to_dict") else {}
                )
            )

        return PartitionResponseSchema(
            success=True,
            total_elements=len(parsed_items),
            elements=parsed_items
        ).model_dump()

    except Exception as e:
        return PartitionResponseSchema(
            success=False,
            total_elements=0,
            elements=[],
            error_message=str(e)
        ).model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [LlamaParse](llamaparse.md) — Document parsing platform from LlamaIndex.
- [Docling](../process_understanding/docling.md) — IBM document parsing framework.
- [Paperless-ngx](../../services/paperless-ngx.md) — Self-hosted document management system.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architecture for document augmentation.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standardized agent tool protocol.
- [Weaviate](../infrastructure/weaviate.md) — Vector database for structured ingestion.
- [Khoj](khoj.md) — Personal AI knowledge search engine.

## Sources / references
- [Unstructured.io Official Site](https://unstructured.io/)
- [Unstructured Ingest Documentation](https://unstructured-io.github.io/unstructured/ingest/overview.html)
- [Chunking Strategies Reference](https://unstructured-io.github.io/unstructured/core/chunking.html)
- [Unstructured UNS-MCP GitHub Repository](https://github.com/Unstructured-IO/UNS-MCP)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
