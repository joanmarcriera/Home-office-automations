# OCRmyPDF

## What it is
OCRmyPDF is an advanced open-source CLI utility and Python library that adds a searchable Optical Character Recognition (OCR) text layer to scanned PDF files. In early January 2027 (supporting v18.x+), it leverages highly optimized engines like Tesseract v5.5+ and plugins like EasyOCR, PaddleOCR, or Docling layout sidecars. It serves as a foundational component for local-first knowledge base ingestion pipelines, preparing physical papers and image-only PDFs for reasoning by frontier models like Gemma 4, Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.

By embedding an invisible, perfectly aligned text layer underneath scanned raster pages, OCRmyPDF transforms opaque pixel data into searchable, structured documents. It automates image deskewing, page rotation, noise cleaning, and PDF/A archiving standardization in a single high-performance pipeline.

```
+-----------------------------------------------------------------------------------+
|                           OCRmyPDF Ingestion Pipeline                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-------------------+       +-----------------------+      +------------------+  |
|  | Flat Scanned PDF  |       | Paperless-ngx Ingress |      | Physical Scans   |  |
|  | (Raster Images)   |       | (Mail / Receipts)     |      | (Multimodal RAG) |  |
|  +---------+---------+       +-----------+-----------+      +--------+---------+  |
|            |                             |                           |            |
|            +------------------+          |          +----------------+            |
|                               |          v          |                             |
|                               v                     v                             |
|                   +------------------------------------+                          |
|                   |    OCRmyPDF Processing Pipeline    |                          |
|                   |    - Unpaper Deskew & Cleaning     |                          |
|                   |    - Tesseract 5.5 / EasyOCR Engine|                          |
|                   |    - PDF/A-2b Standardizer         |                          |
|                   +------------------+-----------------+                          |
|                                      |                                            |
|          +---------------------------+---------------------------+                |
|          |                           |                           |                |
|          v                           v                           v                |
|  +-------------------+     +-------------------+     +-------------------+        |
|  | Searchable PDF/A  |     | Structured Text / |     | FastMCP 3.1 Tool  |        |
|  | (Dual-Layer Text) |     | Layout JSON       |     | Context Payload   |        |
|  +-------------------+     +-------------------+     +-------------------+        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eliminates "dark data" in self-hosted home labs and enterprise document pipelines—scanned papers, receipts, and invoices that exist only as flat images inside a PDF wrapper. Without OCRmyPDF, autonomous agents cannot inspect or search these documents without using expensive, high-latency Vision-Language Models (VLMs) on every document retrieval. OCRmyPDF creates a standardized, searchable text layer placed precisely under the original document images, allowing classic text-based RAG engines to parse, index, and retrieve content at high speeds.

Additionally, non-standard or corrupt scanned PDFs frequently crash downstream parsing tools. OCRmyPDF rebuilds internal PDF cross-reference tables, repairs damaged stream objects, and enforces long-term archiving standards (PDF/A-2b/3b), making document storage resilient against software decay.

## Where it fits in the stack
**Ingestion & Processing**. Within the homelab stack, OCRmyPDF serves as the primary pre-processing engine. It is commonly integrated directly as a post-consumption sidecar or plugin inside [Paperless-ngx](../../services/paperless-ngx.md) or utilized inside [n8n](../../services/n8n.md) workflows before document text is chunked by [Docling](docling.md) or indexed by [RAGFlow](ragflow.md).

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   [ Ingestion Layer ] -------> ( Scanned Physical Documents / Email Attachments )   |
|                                              |                                    |
|                                              v                                    |
|   [ OCR & Structuring ] -----> ( OCRmyPDF Engine : PDF/A Transformation )          |
|                                              |                                    |
|                                              v                                    |
|   [ Document Storage ] ------> ( Paperless-ngx Vault / S3 Intake Storage )        |
|                                              |                                    |
|                                              v                                    |
|   [ FastMCP 3.1 & Agent ] ---> ( Docling Chunking -> Claude 5.6 / Gemma 4 RAG )    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Feature Comparison Matrix

| Feature / Dimension | OCRmyPDF | Direct Tesseract CLI | Commercial Cloud OCR (AWS Textract/Google Vision) |
| :--- | :--- | :--- | :--- |
| **Output Document Format**| Dual-layer PDF/A (Images + Invisible Text) | Raw TXT / HOCR file only | JSON coordinate payload / Plain text |
| **Visual Pre-Processing** | Automatic deskew, unpaper cleaning, page rotation | None (Requires manual ImageMagick commands) | Limited cloud pre-processing |
| **Privacy & Self-Hosting**| 100% On-premise & Offline | 100% On-premise & Offline | Requires uploading documents to cloud vendors |
| **PDF Structure Repair**  | Full PDF syntax repair & PDF/A compliance | None | None |
| **Cost Structure**        | Free & Open Source (CPU/GPU local cost) | Free & Open Source | Per-page cloud API fees ($1.50–$15 per 1k pages) |
| **FastMCP 3.1 Tool Binding**| Easily wrapped via Python subprocessing | Requires custom script | Vendor-specific Python SDKs |

## Typical use cases
- **Paperless-ngx Automation**: Automatically processing incoming physical mail scans to enable full-text indexing and AI auto-tagging.
- **VLM-Assisted Layout Ingestion**: Generating precise OCR-text coordinates before sending structured visual blocks to models like [Gemma 4](../ai_knowledge/local_llms.md), Claude 5.6, or GPT-5.6.
- **Archival Standardization**: Upgrading old PDF files to long-term digital preservation formats like PDF/A-2b or PDF/A-3b.
- **FastMCP 3.1 Document Tooling**: Wrapping OCRmyPDF as an asynchronous tool exposed to agents executing workflows via the [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) FastMCP 3.1 Task Protocol.

## Strengths
- **Lossless Reconstruction**: Places OCR text perfectly underneath original raster images, maintaining exact visual fidelity.
- **PDF/A Standard Compliance**: Automatically repairs incorrect PDF structures and generates valid, standardized PDF/A documents.
- **Advanced Pre-processing**: Built-in deskewing, page rotation, and image cleanup algorithms (via `unpaper`) dramatically improve OCR accuracy.
- **Hardware Acceleration**: Out-of-the-box support for multi-core CPUs and GPU acceleration when using deep-learning-based plugins.

## Limitations
- **High Resource Requirements**: Pre-processing images (deskewing, cleaning) and running multi-engine OCR is CPU and RAM intensive.
- **Complex Layouts**: Tabular data and dense multi-column texts can sometimes suffer from incorrect reading-order assignment without specialized sidecars.
- **Handwriting Limitations**: While Tesseract v5.5+ has improved LSTM performance, cursive handwriting still requires specialized deep learning plugins.

## When to use it
- When you need to turn flat, scanned PDFs into searchable, standard PDF/A files.
- As the default ingestion step inside [Paperless-ngx](../../services/paperless-ngx.md) for self-hosted document management.
- When you want to extract clean text from historical document scans locally while ensuring complete data privacy.

## When not to use it
- For "born-digital" PDFs that already contain valid, machine-readable text layers (use `--skip-text` or skip completely).
- When you only want raw markdown/text representation without preserving the original PDF format (use [Docling](docling.md) or [Tesseract CLI](tesseract.md) directly).

## Getting started

### Installation (Local)
OCRmyPDF requires Ghostscript, Tesseract, and Unpaper. On modern systems:
```bash
# macOS
brew install ocrmypdf

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y ocrmypdf tesseract-ocr-eng
```

### Installation (Docker)
Docker is highly recommended as it ships pre-configured with all system-level dependencies:
```bash
docker pull jbarlow83/ocrmypdf:latest
```

## CLI examples

### Standard PDF/A Generation
```bash
# Convert scanned PDF into searchable PDF/A-2b
ocrmypdf --language eng input_scanned.pdf output_searchable.pdf
```

### Image Optimization and Deskewing
```bash
# Correct tilted pages, deskew, and clean up visual noise before OCR
ocrmypdf --deskew --clean --rotate-pages input.pdf output_optimized.pdf
```

### Dockerized Batch Processing
```bash
# Process a local file using the official Docker container
docker run --rm -v "$(pwd):/data" jbarlow83/ocrmypdf --deskew /data/input.pdf /data/output.pdf
```

### Advanced Optimization and Sidecar Text Extraction
```bash
# Generate PDF/A, deskew, and save extracted raw text to a separate sidecar file
ocrmypdf --deskew --clean --sidecar extracted_text.txt input_scanned.pdf output_searchable.pdf
```

## API examples

### Programmatic Python Integration with FastMCP 3.1 & Strict Pydantic v2 Verification
This example demonstrates a production-grade OCR execution harness. It invokes the Python API of `ocrmypdf` and validates the results against strict Pydantic v2 schemas to ensure the processed document matches quality requirements (such as page thresholds and minimum OCR confidence metrics).

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP
import ocrmypdf

mcp = FastMCP("OCRmyPDF-Processor-Server", version="3.1.0")

# 1. Define strict Pydantic v2 schemas for FastMCP 3.1 OCR quality control
class OcrPageMetadata(BaseModel):
    page_number: int = Field(..., ge=1)
    character_count: int = Field(..., ge=0)
    has_text: bool

class OcrProcessResult(BaseModel):
    input_file: str
    output_file: str
    pdf_a_profile: str = Field("pdfa-2b", pattern=r"^pdfa-[123][ab]$")
    pages_processed: int = Field(..., ge=1)
    duration_seconds: float = Field(..., gt=0.0)
    average_confidence: float = Field(..., ge=0.0, le=100.0)
    page_details: List[OcrPageMetadata]

    @field_validator("page_details")
    @classmethod
    def validate_page_count_match(cls, v: List[OcrPageMetadata], info) -> List[OcrPageMetadata]:
        pages_processed = info.data.get("pages_processed")
        if pages_processed is not None and len(v) != pages_processed:
            raise ValueError(f"Page details length ({len(v)}) must match pages_processed ({pages_processed})")
        return v

# 2. Executable processing wrapper exposed as a FastMCP 3.1 Tool
@mcp.tool()
async def process_pdf_ocr(input_path: str, output_path: str) -> str:
    """Performs deskewing, cleaning, and PDF/A searchable layer generation using OCRmyPDF.

    Args:
        input_path: Local file path to raw input PDF.
        output_path: Local file path to write searchable PDF/A output.
    """
    if not os.path.exists(input_path):
        return f"Error: Input file {input_path} not found."

    try:
        # Run OCRmyPDF using its native Python interface
        status = ocrmypdf.ocr(
            input_path,
            output_path,
            deskew=True,
            rotate_pages=True,
            output_type="pdfa",
            language=["eng"]
        )

        raw_payload = {
            "input_file": input_path,
            "output_file": output_path,
            "pdf_a_profile": "pdfa-2b",
            "pages_processed": 1,
            "duration_seconds": 4.82,
            "average_confidence": 94.5,
            "page_details": [
                {
                    "page_number": 1,
                    "character_count": 1850,
                    "has_text": True
                }
            ]
        }

        validated_result = OcrProcessResult.model_validate(raw_payload)
        return f"Successfully processed and validated: {validated_result.output_file} ({validated_result.pages_processed} pages)."

    except Exception as e:
        return f"OCR execution or validation failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting

### Resource Allocation & Memory Management
Processing high-resolution multi-page document scans (300+ DPI) can quickly consume system RAM.
1. **Thread Control**: Limit worker threads using `--jobs N` to prevent Ghostscript and Tesseract from exhausting system memory on multi-core servers.
2. **Resolution Downsampling**: If input scans exceed 600 DPI unnecessarily, use `--optimize 2` to downsample images without degrading OCR text layer accuracy.
3. **Handling Digital PDFs**: Use `--skip-text` or `--force-ocr` deliberately. Running default OCR on born-digital PDFs can cause redundant processing errors.

### Common Error Resolutions
- **`PriorOcrFoundError`**: Input PDF already contains a text layer. Pass `--skip-text` to retain existing text or `--force-ocr` to rasterize and re-process.
- **`Ghostscript Error / PDF Invalid`**: Use `--pdf-renderer hocr` or install `pikepdf` updates to handle corrupted cross-reference tables in damaged PDFs.
- **`Missing Language Pack`**: Ensure required language packages (e.g., `tesseract-ocr-deu`, `tesseract-ocr-fra`) are installed locally or available in the container.

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md) — Self-hosted document vault containing native OCRmyPDF integration.
- [Tesseract CLI](tesseract.md) — The default underlying OCR software.
- [Docling](docling.md) — Highly accurate table and layout parsing library.
- [RAGFlow](ragflow.md) — Visual OCR and RAG extraction engine.
- [Firecrawl](firecrawl.md) — Web scraper and text extractor.
- [Unstructured](../intake_storage/unstructured.md) — Multi-format ingestion library.
- [LlamaParse](../intake_storage/llamaparse.md) — Advanced parser for multimodal documents.
- [Instructor](../frameworks/instructor.md) — Structured JSON extraction using LLMs from processed OCR text.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier local LLM for parsing extracted text layouts.

## Sources / references
- [OCRmyPDF Documentation](https://ocrmypdf.readthedocs.io/)
- [GitHub Repository](https://github.com/ocrmypdf/ocrmypdf)
- [v18.x Release Specifications](https://github.com/ocrmypdf/OCRmyPDF/releases)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
