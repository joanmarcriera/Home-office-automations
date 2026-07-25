# Playbook: Document Preparation for LLM Training

## What it is

This playbook defines a repeatable architectural process for preparing heterogeneous business documents (`docx`, `pdf`, `pptx`, spreadsheets) for use in LLM fine-tuning or retrieval-augmented generation (RAG) pipelines. It focuses on normalization, metadata preservation, and selective consolidation to create a safe and consistent training corpus.

## What problem it solves

Raw business documents are often fragmented, inconsistent, and unstructured, making them difficult for LLMs to process effectively. This playbook solves the "garbage in, garbage out" problem by providing a systematic workflow for OCR, text extraction, and deduplication. It ensures that document boundaries and provenance are preserved, preventing loss of context during ingestion.

## Where it fits in the stack

**Category**: Playbook / Process. It sits in the **data engineering layer**, acting as the bridge between raw document storage (e.g., [Paperless-ngx](../services/paperless-ngx.md), [Nextcloud](../services/nextcloud.md)) and the vector stores or training harnesses used by AI agents.

## Typical use cases

- **Corpus Construction**: Building a supervised fine-tuning dataset from existing office files.
- **RAG Pre-processing**: Normalizing a fragmented knowledge base into Markdown for high-fidelity retrieval.
- **Data Auditing**: Cleaning and deduplicating an archive of board packs and policy manuals.
- **Synthetic Data Generation**: Using GPT-5.5 to generate high-quality training pairs from normalized document text.
- **High-Fidelity Extraction**: Using Claude 5.1 for section-aware parsing of complex layout PDFs.

## Strengths

- **High Fidelity**: Prioritizes structured extraction (e.g., [Docling](../tools/process_understanding/docling-mcp.md)) over simple copy-pasting.
- **Metadata-Rich**: Includes a mandatory JSON manifest for every document to preserve provenance.
- **Mac-Friendly**: Optimized for local execution using standard macOS and Docker tools.
- **Scalable**: Provides clear rules for when to merge or split documents based on topical coherence.
- **MCP Enabled**: Integrated with Docling MCP 3.1 for seamless tool-based extraction within agentic workflows.

## Limitations

- **OCR Dependency**: Highly dependent on the quality of the OCR engine ([OCRmyPDF](../tools/process_understanding/ocrmypdf.md)) for scanned sources.
- **Manual Spot Checks**: Still requires human review for 5-10% of outputs to ensure extraction quality.
- **Intellectual Property**: Requires rigorous upfront verification of document rights and redaction needs.

## When to use it

- When building a custom knowledge base for an internal AI assistant.
- When preparing a dataset for an LLM evaluation benchmark.
- When migrating document workflows from SaaS to local-first infrastructure.

## When not to use it

- For ad hoc, single-file Q&A (use direct retrieval tools instead).
- If you do not have legal rights to the documents for model training.
- For documents that are purely image-based with no viable OCR path.

## Getting started

To begin document preparation:

```mermaid
flowchart TD
    A[Raw Document Storage] --> B{Document Type?}
    B -- Scanned PDF --> C[OCRmyPDF]
    B -- Born-digital/Office --> D[Extraction Pass]
    C --> D
    D -- Apache Tika / Docling MCP --> E[Markdown Normalization]
    E --> F[Manifest Generation JSON]
    F --> G[Semantic Deduplication / GPT-5.5]
    G --> H[Semantic Merging / Claude 5.1]
    H --> I[Final Training Corpus]
```

1. **Setup Staging**: Create the recommended directory structure (`raw`, `normalized`, `manifests`, `merged`).
2. **Run OCR**: Use [OCRmyPDF](../tools/process_understanding/ocrmypdf.md) on any scanned PDFs.
3. **Extract and Normalize**: Use [Apache Tika](../services/tika.md) or [Docling MCP](../tools/process_understanding/docling-mcp.md) to convert files to Markdown.
4. **Generate Manifests**: Create a JSON sidecar for every file capturing source provenance and checksums.
5. **Deduplicate**: Use GPT-5.5 to identify and remove repeated template noise (headers, footers) before merging related documents.

## CLI examples

### Batch OCR with OCRmyPDF
Converting all scanned PDFs in a directory to searchable versions.
```bash
# Using a Docker-based OCRmyPDF loop
for f in raw/*.pdf; do
  docker run --rm -v "$PWD:/home/docker" jbarlow83/ocrmypdf "$f" "normalized/${f%.pdf}-ocr.pdf"
done
```

### Extraction via Tika Server
Retrieving text from a born-digital Word document.
```bash
# Sending a file to a running Tika container
curl -T raw/manual.docx http://localhost:9998/tika > normalized/manual.txt
```

## API examples

### Structured Extraction with Docling MCP
An agent using Docling MCP to extract tables and hierarchy from a complex PDF.
```python
from mcp_client import MCPClient

async def extract_structured_data(filepath):
    client = MCPClient("http://docling-mcp.local")
    result = await client.call_tool("extract_markdown", {"path": filepath, "mode": "accurate"})
    return result['content']

# Returns structured Markdown with tables preserved as GitHub Flavored Markdown (GFM)
markdown_data = await extract_structured_data("raw/q4-report.pdf")
```

### Generating a Document Manifest (JSON)
Standardized metadata sidecar for every ingested document, adhering to MCP 3.1 schemas.
```json
{
  "source_path": "raw/2026-03-16-policy-manual-original.docx",
  "source_type": "docx",
  "document_title": "Corporate Travel Policy 2026",
  "authors_or_owner": "HR Department",
  "created_at": "2026-01-10T09:00:00Z",
  "exported_at": "2026-08-20T14:30:00Z",
  "language": "en",
  "sensitivity": "internal",
  "ocr_used": false,
  "merge_group": "hr-policies",
  "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "mcp_meta": {
    "schema_version": "3.1",
    "task_binding": "doc-prep-task-1"
  }
}
```

## Related tools / concepts

- [OCRmyPDF](../tools/process_understanding/ocrmypdf.md)
- [Docling MCP](../tools/process_understanding/docling-mcp.md)
- [PageIndex](../tools/process_understanding/pageindex.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Apache Tika](../services/tika.md)
- [Google Workspace CLI](../tools/automation_orchestration/google-workspace-cli.md)
- [RAG Pattern](../knowledge_base/patterns/rag.md)
- [Anytype](../tools/intake_storage/anytype.md)
- [Silverbullet](../tools/intake_storage/silverbullet.md)
- [Knowledge Base Health](knowledge-base-health.md)

## Sources / References
- [OCRmyPDF documentation](https://ocrmypdf.readthedocs.io/)
- [Apache Tika Server](https://cwiki.apache.org/confluence/display/TIKA/TikaServer)
- [Google Drive export MIME types](https://developers.google.com/workspace/drive/api/guides/ref-export-formats)
- [Docling MCP repository](https://github.com/docling-project/docling-mcp)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.org/spec)

## Contribution Metadata
- Last reviewed: 2026-08-20
- Confidence: high
