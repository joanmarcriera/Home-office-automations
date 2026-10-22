# Tesseract CLI

## What it is
Tesseract is a highly versatile, open-source Optical Character Recognition (OCR) engine. In early January 2027, Tesseract (v5.5.0+) features enhanced LSTM (Long Short-Term Memory) OCR models, optimized SIMD execution, and robust support for hundreds of languages. It operates entirely locally, making it a critical tool for home-lab ingestion, privacy-first automation pipelines, and localized document processing under [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) using models like [Gemma 4](../ai_knowledge/local_llms.md), Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.

```
+---------------------------------------------------------------------------------------------------+
|                                 TESSERACT INGESTION & PROCESSING PIPELINE                         |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------+       +---------------------------------------------------------+  |
|  | Scanned Image / PDF Page  | ----> | Image Pre-processing Engine                             |  |
|  | (PNG, TIFF, JPEG, Scans)  |       | (Deskewing, Binarization, Contrast, Resolution 300 DPI)|  |
|  +---------------------------+       +---------------------------------------------------------+  |
|                                                                  |                                |
|                                                                  v                                |
|                                      +---------------------------------------------------------+  |
|                                      | Page Segmentation Mode (PSM) & Layout Analyzer          |  |
|                                      +---------------------------------------------------------+  |
|                                                                  |                                |
|                                                                  v                                |
|                                      +---------------------------------------------------------+  |
|                                      | Tesseract v5.5 LSTM Neural Network Engine               |  |
|                                      | (SIMD Parallel Execution & Multilingual Language Data)  |  |
|                                      +---------------------------------------------------------+  |
|                                                                  |                                |
|                                                                  v                                |
|  +---------------------------+       +---------------------------------------------------------+  |
|  | FastMCP 3.1 Tool Host /   | <---- | Structured Output Formatter                             |  |
|  | Local Agent Reasoning Core|       | (Plain Text, hOCR, Bounding Box TSV, Searchable PDF)    |  |
|  +---------------------------+       +---------------------------------------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### FastMCP 3.1 OCR Extraction & Validation Sequence

```
+---------------+        +----------------------+        +---------------------+        +--------------------+
| FastMCP Agent |        | FastMCP Tool Server  |        | Image Preprocessor  |        | Tesseract Engine   |
+---------------+        +----------------------+        +---------------------+        +--------------------+
        |                           |                               |                             |
        |--- 1. OCR Request ------->|                               |                             |
        |    (Image Path / PSM)     |--- 2. Deskew & Binarize ----->|                             |
        |                           |<-- 3. Preprocessed Bitmap ----|                             |
        |                           |                                                             |
        |                           |--- 4. Execute LSTM OCR Pass (--psm 6 -l eng) -------------->|
        |                           |<-- 5. Return TSV / Word BBoxes + Confidence ----------------|
        |                           |                                                             |
        |                           |--- 6. Validate Pydantic v2 Contract                         |
        |                           |    (Check overall confidence >= 70%)                        |
        |<-- 7. Verified OCR Output-|                                                             |
```

## What problem it solves
It solves the problem of extracting machine-readable text from raw images (e.g., PNGs, JPGs, TIFFs) or non-searchable PDF pages. For autonomous agents, image files are flat binary data; Tesseract transforms this data into semantic text strings, layout tables, and structured coordinates. This enables local LLMs to reason over physical mail, receipts, screenshots, and visual interfaces without resorting to high-latency or high-cost cloud vision APIs.

Furthermore, processing confidential personal records (e.g., tax forms, medical records, bank statements) through remote cloud OCR endpoints introduces severe privacy risks. Tesseract guarantees 100% air-gapped, zero-exfiltration processing while maintaining low latency on standard hardware.

## Where it fits in the stack
**Process & Understanding**. It forms the foundational, low-level OCR engine in the ingestion plane. It sits underneath high-level PDF automation frameworks like [OCRmyPDF](ocrmypdf.md) and powers the integrated OCR capabilities of document repositories such as [Paperless-ngx](../../services/paperless-ngx.md) and [Paperless-AI](../../services/paperless-ai.md).

```
+---------------------------------------------------------------------------------------------------+
|                                DOCUMENT INGESTION STACK POSITIONING                               |
+---------------------------------------------------------------------------------------------------+
|  Agent Reasoning      |  Claude 5.6 / Local LLMs (Gemma 4) / FastMCP 3.1 Agent Sessions           |
+-----------------------+---------------------------------------------------------------------------+
|  Document Management  |  Paperless-ngx / Paperless-AI / Docling / Unstructured                    |
+-----------------------+---------------------------------------------------------------------------+
|  High-Level Wrappers  |  OCRmyPDF (PDF Text Layer Injection & Image Optimization)                 |
+-----------------------+---------------------------------------------------------------------------+
|  Core OCR Engine      |  TESSERACT OCR v5.5 (LSTM Model / C++ Engine Engine / SIMD Execution)     |
+---------------------------------------------------------------------------------------------------+
```

### Feature & Performance Comparison
The matrix below compares Tesseract against alternative open-source and cloud OCR solutions across key performance indicators:

| Feature / Metric | Tesseract v5.5 | PaddleOCR | EasyOCR | Cloud Vision APIs (AWS/GCP) |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Latency** | Ultra-Fast (<200ms/page) | Moderate (~800ms/page) | Slow (~1200ms/page) | Variable Network Latency |
| **Hardware Requirements**| Low CPU / Minimal RAM | Requires GPU for Speed | Requires GPU for Speed | None (Cloud Based) |
| **Privacy / Air-Gap** | 100% Local / Air-Gapped | 100% Local / Air-Gapped | 100% Local / Air-Gapped | Remote Cloud Service |
| **Output Formats** | Text, hOCR, PDF, TSV | Text, Bounding Box JSON | Text, Coordinates | JSON Payload |
| **Multilingual Support**| 100+ Trained Languages | 80+ Languages | 80+ Languages | 100+ Languages |
| **Complex Table Support**| Moderate (Requires PSM) | High (Native Layout) | Moderate | Very High |

## Typical use cases
- **Privacy-First Invoice Parsing**: Local extraction of billing data from receipt images, verifying dates and totals using [Instructor](../frameworks/instructor.md).
- **FastMCP 3.1 OCR Tooling**: Exposing raw image OCR tools to local assistants via modern [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) FastMCP 3.1 Task Protocol servers.
- **Visual Terminal Automation**: Converting console screenshots to raw text to help self-healing scripts diagnose OS-level errors.
- **Multilingual Transcription**: Utilizing customized language training files to extract historical documents in complex non-Latin scripts.
- **Searchable PDF Generation**: Injecting invisible text layers into scanned documents within Paperless-ngx pipelines.

## Page Segmentation Mode (PSM) & OEM Reference Matrix

| PSM Flag | Target Layout & Orientation | Recommended Use Case |
| :--- | :--- | :--- |
| `--psm 0` | Orientation and script detection (OSD) only | Auto-detect page rotation before OCR pass |
| `--psm 1` | Automatic page segmentation with OSD | Complex multi-page scanned PDF documents |
| `--psm 3` | Fully automatic page segmentation (Default) | Standard single-column or multi-column documents |
| `--psm 4` | Single column of text of variable sizes | Receipts, invoices, elongated column clippings |
| `--psm 6` | Uniform single block of text | Form field blocks, paragraphs, single-page letters |
| `--psm 11` | Sparse text; find as much text as possible | Watermarks, scattered labels, complex diagrams |

## Strengths
- **Fully Offline**: 100% local processing guarantees total security for sensitive personal or corporate documents.
- **Extensive Language Assets**: Supports over 100 languages with community-trained, high-fidelity LSTM data models.
- **Performance & Efficiency**: Highly optimized C++ codebase that runs quickly even on low-power single-board computers or older NAS devices.
- **Rich Output Formats**: Generates plain text, HTML-based hOCR, PDF, or TSV containing bounding boxes and word confidence values.
- **Deterministic Execution**: Predictable output behavior without generative hallucination risks.

## Limitations
- **Format Requirements**: Requires external pre-processing (such as deskewing, binarization, or DPI adjustment) to yield high OCR accuracy.
- **Complex Layouts**: Can struggle with non-linear multi-column articles or complex tables without prior segmentation.
- **Messy Handwriting**: Remains less accurate on dense script or cursive compared to large deep learning models like PaddleOCR or EasyOCR plugins.

## When to use it
- When you need a reliable, fully local, open-source OCR engine with low latency.
- When building backend Python microservices that need to extract raw text from image attachments.
- When privacy constraints prevent sending visual records to third-party LLM APIs.

## When not to use it
- For "born-digital" documents that already have a structured text layer (use standard text extraction libraries instead).
- When a document requires sophisticated document layout reconstruction (use [Docling](docling.md) or [OCRmyPDF](ocrmypdf.md) instead).

### Failure Modes & Diagnostic Matrix

| Failure Mode / Symptom | Probable Cause | Diagnostic Command | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Low Accuracy on Small Text** | Image resolution below 300 DPI | `identify -format "%x x %y" scan.png` | Upscale and smooth scan using ImageMagick Lanczos resize |
| **Garbled Output on Sideways Scans** | Incorrect page orientation angle | `tesseract scan.png output --psm 0` | Run orientation detection and auto-rotate image using Leptonica |
| **Multi-Column Text Bleeding** | Unsegmented horizontal scanning across columns | `tesseract scan.png output --psm 3` | Switch PSM mode to column-aware `--psm 4` or `--psm 6` |
| **Language Model Missing Error** | Specified language data pack `.traineddata` not installed | `tesseract --list-langs` | Download required language traineddata pack into `tessdata` directory |
| **FastMCP Timeout on Batch Processing** | Large uncompressed TIFF file blocking CPU worker pool | `mcp-server --log-level DEBUG` | Pre-convert TIFF assets to compressed 300 DPI PNG before calling FastMCP tool |

### Operational Best Practices
- **Optimize Page Segmentation Mode (PSM)**: Select the appropriate PSM flag (e.g., `--psm 6` for uniform text blocks, `--psm 11` for sparse text) to drastically improve accuracy.
- **Combine Language Vectors for Bilingual Documents**: Pass multiple language flags (e.g., `-l eng+deu+fra`) to parse mixed-language receipts.
- **Cache Pre-Processed Bitmaps**: Save binarized image assets during batch processing to avoid re-executing contrast routines during retry loops.

## Getting started

### Installation (Local)
On Debian-based systems and macOS:
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
```

### Installation (Docker)
Using Docker is recommended for consistent, headless environments:
```bash
docker pull tesseractocr/tesseract:latest
```

## CLI examples

### Basic Text Extraction
```bash
# Extracts text from scan.png and writes it to output.txt
tesseract scan.png output -l eng
```

### Bounding Box and hOCR Output
```bash
# Generates a structured HTML file with bounding box coordinates (output.hocr)
tesseract scan.png output hocr
```

### Page Segmentation Mode Control
```bash
# Force single block uniform text parsing
tesseract scan.png output --psm 6 -l eng
```

### Listing Available Language Packs
```bash
# Lists all language data files currently installed
tesseract --list-langs
```

## API examples

### Programmatic Python Extraction with FastMCP 3.1 & Strict Pydantic v2 Validation
This example showcases how to execute Tesseract OCR programmatically (using `pytesseract` or C++ bindings) and validate raw text output, bounding boxes, and word-level confidences against strict Pydantic v2 schemas within a FastMCP 3.1 tool server. This ensures that any OCR pipeline anomalies are caught and corrected before the text is sent to [Gemma 4](../ai_knowledge/local_llms.md) or [Claude](../ai_knowledge/claude.md) for further reasoning.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TesseractOCRServer", version="3.1.0")

# 1. Define strict Pydantic v2 schemas for OCR bounding boxes and results
class BoundingBox(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    left: int = Field(..., ge=0, description="Pixel coordinate from left boundary")
    top: int = Field(..., ge=0, description="Pixel coordinate from top boundary")
    width: int = Field(..., gt=0, description="Bounding box width in pixels")
    height: int = Field(..., gt=0, description="Bounding box height in pixels")

class OcrWord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    word_text: str = Field(..., min_length=1, description="Recognized character string")
    confidence: float = Field(..., ge=0.0, le=100.0, description="Tesseract confidence score percentage")
    box: BoundingBox

    @field_validator("word_text")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

class VerifiedOcrOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    image_name: str
    language: str = Field("eng", pattern=r"^[a-z]{3}(\+[a-z]{3})*$")
    full_text: str = Field(..., min_length=1)
    words: List[OcrWord]
    overall_confidence: float = Field(..., ge=0.0, le=100.0)

    @field_validator("overall_confidence")
    @classmethod
    def validate_confidence_threshold(cls, v: float) -> float:
        if v < 70.0:
            raise ValueError(f"Overall OCR confidence ({v}%) falls below quality standard (70.0%)")
        return v

# 2. Executable FastMCP 3.1 tool endpoint
@mcp.tool()
def parse_and_verify_tesseract_output(raw_ocr_payload: dict) -> dict:
    """Validates raw pytesseract extraction output against Pydantic v2 runtime contracts."""
    try:
        # Validate raw dictionary against the Pydantic v2 schema
        validated_data = VerifiedOcrOutput.model_validate(raw_ocr_payload)
        return {
            "status": "success",
            "image_name": validated_data.image_name,
            "full_text": validated_data.full_text,
            "overall_confidence": validated_data.overall_confidence,
            "word_count": len(validated_data.words)
        }
    except ValidationError as e:
        return {
            "status": "validation_error",
            "errors": e.errors(include_url=False)
        }

class OcrQualityReport(BaseModel):
    image_path: str
    total_words: int = Field(..., ge=0)
    low_confidence_word_count: int = Field(..., ge=0)
    average_confidence: float = Field(..., ge=0.0, le=100.0)

@mcp.tool()
def audit_ocr_quality(report_json: str) -> dict:
    """FastMCP 3.1 tool for auditing OCR character recognition quality metrics."""
    try:
        report = OcrQualityReport.model_validate_json(report_json)
        is_acceptable = report.average_confidence >= 80.0 and report.low_confidence_word_count <= (report.total_words * 0.1)
        return {
            "status": "audited",
            "image_path": report.image_path,
            "pass_quality_gate": is_acceptable,
            "average_confidence": report.average_confidence
        }
    except ValidationError as err:
        return {"status": "error", "validation_errors": err.errors(include_url=False)}

if __name__ == "__main__":
    # Simulated pytesseract raw dictionary extraction
    simulated_pytesseract_dict = {
        "image_name": "receipt_scan.png",
        "language": "eng",
        "full_text": "TOTAL: $45.90",
        "words": [
            {
                "word_text": "TOTAL:",
                "confidence": 96.5,
                "box": {"left": 50, "top": 120, "width": 80, "height": 20}
            },
            {
                "word_text": "$45.90",
                "confidence": 98.2,
                "box": {"left": 140, "top": 120, "width": 70, "height": 20}
            }
        ],
        "overall_confidence": 97.35
    }

    result = parse_and_verify_tesseract_output(simulated_pytesseract_dict)
    print(f"FastMCP Tool Result: {result}")
```

## Production Deployment & Systemd Service Architecture

To run Tesseract FastMCP 3.1 OCR server workers as resilient background daemons on enterprise Linux hosts, use the systemd unit template below:

```ini
[Unit]
Description=Tesseract FastMCP 3.1 OCR Tool Server
After=network.target local-fs.target
Requires=local-fs.target

[Service]
Type=simple
User=tesseract-mcp
Group=tesseract-mcp
WorkingDirectory=/opt/tesseract-mcp
ExecStart=/usr/bin/python3 -m mcp.server.fastmcp run tesseract_server.py
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
Environment=OMP_THREAD_LIMIT=4

# Security and Isolation Guardrails
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
MemoryDenyWriteExecute=true

[Install]
WantedBy=multi-user.target
```

## Enterprise Security & Air-Gap Privacy Guardrails

1. **Air-Gapped Processing Enforcement**: Tesseract execution runs entirely in local memory or container sandbox environments without network socket binding.
2. **PII Masking at Image Pass**: Pre-processing scripts mask designated region-of-interest coordinates (such as credit card CVVs or national security IDs) before OCR text extraction.
3. **Ephemeral Temp File Cleanup**: All intermediate pre-processed image bitmaps (`/tmp/ocr_binarized_*.png`) must be deleted immediately after Pydantic schema validation.

## Related tools / concepts
- [OCRmyPDF](ocrmypdf.md) — High-level PDF wrapper that uses Tesseract as its core OCR engine.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system powered by Tesseract OCR.
- [Docling](docling.md) — Visual-language layout analyzer and high-performance table converter.
- [Firecrawl](firecrawl.md) — Ingestion engine for turning web content into markdown.
- [RAGFlow](ragflow.md) — Local visual extraction and evaluations platform.
- [Unstructured](../intake_storage/unstructured.md) — General framework for parsing unstructured assets.
- [LlamaParse](../intake_storage/llamaparse.md) — Cloud-hosted parsing optimized for complex PDF layouts.
- [Instructor](../frameworks/instructor.md) — Structured JSON data extraction from OCR-extracted text.
- [Paperless-AI](../../services/paperless-ai.md) — AI enrichment sidecar for Paperless-ngx.
- [Claude](../ai_knowledge/claude.md) — Frontier LLM utilized for advanced OCR text corrections.
- [Local LLMs (Gemma 4)](../ai_knowledge/local_llms.md) — Privacy-preserving models optimized for agentic text reasoning.
- [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) — Context-aware workflow and session coordination protocols.

## Sources / references
- [Tesseract OCR Main GitHub Repository](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Documentation Portal](https://tesseract-ocr.github.io/)
- [Tesseract v5.5 Release Specifications](https://github.com/tesseract-ocr/tesseract/releases)

## Contribution Metadata
- Last reviewed: 2026-10-12
- Confidence: high
