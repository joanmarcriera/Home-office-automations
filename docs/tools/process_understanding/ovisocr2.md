# OvisOCR2

OvisOCR2 is a highly compact, end-to-end 0.8B parameter vision-language model (VLM) specifically optimized for high-fidelity document parsing and structured extraction. As of early January 2027, it represents the state-of-the-art for local, page-level document understanding, converting complex scanned pages, diagrams, and hand-written formulas directly into structured Markdown and validated JSON.

## What it is
Developed by the ATH-MaaS team, OvisOCR2 is a specialized VLM built by post-training the highly efficient Qwen3.5-0.8B architecture. It is designed to interpret page layouts, read dense multi-lingual texts, parse mathematical expressions, and map multi-column tables directly into structurally clean representations (Markdown/HTML) while preserving reading order.

## What problem it solves
Traditional OCR pipelines rely on multiple disconnected models (layout detection, line extraction, table segmenters, LaTeX OCR). These multi-stage systems suffer from error propagation, high latency, and massive compute overhead. OvisOCR2 solves this with an end-to-end VLM architecture that decodes text, layout, and complex tables simultaneously in a single forward pass, severely reducing latency and footprint on edge hardware.

## Where it fits in the stack
[Layer 5: Process & Understanding](index.md) — Serves as a high-performance local ingestion and parsing engine for [RAG Patterns](../../knowledge_base/patterns/rag-pattern.md). Within a [FastMCP 3.1](../automation_orchestration/mcp.md) tool ecosystem, OvisOCR2 is typically deployed as a secure local service converting unstructured physical scans into clean, parsed text for large orchestrators using [Gemma 4](../ai_knowledge/local_llms.md) or [Claude 5.6](../providers/anthropic.md).

## Typical use cases
- **Dense Formula Parsing**: Converting math-heavy research papers with multiple LaTeX formulas into clean, readable Markdown blocks.
- **Borderless Table Extraction**: Directly parsing dense financial sheets or corporate balance tables without losing row/column mappings.
- **Legal Scanned Document Search**: Indexing multi-column legal briefs with precise retention of hierarchy and footnotes.
- **Local Privacy-First Pipelines**: Enabling high-fidelity document parsing in air-gapped environments on consumer-grade hardware (< 8GB VRAM).

## Strengths
- **Incredibly Efficient Footprint**: With only 0.8B parameters, it offers blazing inference speeds and easily runs on laptops, edge devices, or modest GPUs.
- **Top-Tier Performance**: Achieves 96.6+ on OmniDocBench v1.6, outperforming closed models many times its size.
- **Single-Pass Execution**: Removes the need to maintain distinct pipelines for text, tables, and image captions.
- **Native Serving Engine Compatibility**: Full support for [vLLM](../infrastructure/vllm.md) and FastMCP 3.1 tool integration under an Apache 2.0 open license.

## Limitations
- **Single-Page Target**: Optimized for individual page images; multi-page consistency and indexing must be controlled by an external orchestration layer.
- **Resolution Sensitivity**: Very small font sizes or highly blurred page scans can lead to diminished OCR accuracy.
- **Limited Multi-modal Reasoning**: It is a specialized parsing engine; do not use it for general visual reasoning or chat (pair it with [Gemma 4](../ai_knowledge/local_llms.md)).

## When to use it
- When you require ultra-fast, local, or privacy-compliant document parsing with limited GPU resources.
- For transcribing technical papers, academic filings, and scanned books with mixed LaTeX equations.
- As a faster, lighter alternative to heavier multi-stage libraries like [Docling](docling.md) or [Unstructured](../intake_storage/unstructured.md).

## When not to use it
- For general image captioning and multi-modal dialogue (use [Moondream](../ai_knowledge/moondream.md)).
- If your target pipeline requires native conversion into proprietary document formats like direct Word (.docx) or Excel (.xlsx) binaries.

## Getting started

### Installation
OvisOCR2 is optimized to run inside the high-performance vLLM engine:
```bash
pip install "vllm>=0.22.1" pillow pydantic>=2.0
```

### Loading the Model
Load the official weights directly from Hugging Face (`ATH-MaaS/OvisOCR2`):
```python
from vllm import LLM
model = LLM(model="ATH-MaaS/OvisOCR2", tensor_parallel_size=1)
```

## CLI examples
Starting a local vLLM server to expose OvisOCR2 over an OpenAI-compatible endpoint:
```bash
# Launch local OpenAI-compatible API serving the Ovis model
python -m vllm.entrypoints.openai.api_server --model ATH-MaaS/OvisOCR2 --port 8000

# Register OvisOCR2 within your local MCP config to handle document parsing tools
mcp register ovis-parser --command "vllm" --args "serve --model ATH-MaaS/OvisOCR2"
```

## API examples

### End-to-End Structured Document Parsing with Pydantic v2
This example shows how to perform page OCR using OvisOCR2 with vLLM, and validate the resulting layout and table blocks structurally using Pydantic v2.

```python
from typing import List, Literal, Optional
from PIL import Image
from pydantic import BaseModel, Field, conlist
from vllm import LLM, SamplingParams

# 1. Define the Pydantic v2 models for structured layout validation
class ExtractedBlock(BaseModel):
    block_type: Literal["header", "text", "table", "formula", "footer"]
    reading_order_index: int = Field(..., ge=0)
    raw_content: str = Field(..., min_length=1)
    language_detected: str = Field("en", pattern="^[a-z]{2}$")

class ParsedPage(BaseModel):
    page_number: int = Field(..., gt=0)
    blocks: List[ExtractedBlock] = Field(..., min_length=1)
    has_latex: bool
    is_complete: bool

# 2. Set up the local vLLM pipeline
llm = LLM(model="ATH-MaaS/OvisOCR2", gpu_memory_utilization=0.7)
sampling_params = SamplingParams(temperature=0, max_tokens=4096)

def parse_page_image(image_path: str) -> Optional[ParsedPage]:
    prompt = """
    Parse the following document image. Break the parsed layout into structured blocks (headers, main text, tables, and formulas).
    Output the final result as a validated JSON object conforming to the ParsedPage model structure.
    Return JSON ONLY.
    """
    try:
        image = Image.open(image_path)
        # Execute the model inference
        outputs = llm.generate([{"prompt": prompt, "multi_modal_data": {"image": image}}], sampling_params)
        raw_text = outputs[0].outputs[0].text

        # Parse and validate the output against our Pydantic v2 schema
        page_data = ParsedPage.model_validate_json(raw_text)
        return page_data
    except Exception as e:
        print(f"Error parsing document page {image_path}: {e}")
        return None

if __name__ == "__main__":
    page = parse_page_image("scanned_document.jpg")
    if page:
        print(f"Validated Page {page.page_number} containing {len(page.blocks)} layout blocks.")
```

## Related tools / concepts
- [Docling](docling.md) — IBM's enterprise-grade multi-format parser.
- [Moondream](../ai_knowledge/moondream.md) — Ultra-lightweight general-purpose vision VLM.
- [vLLM](../infrastructure/vllm.md) — Blazing-fast inference serving framework.
- [Tesseract CLI](tesseract.md) — Traditional command-line OCR tool.
- [OCRmyPDF](ocrmypdf.md) — PDF searchable layer injector.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Enterprise knowledge retrieval strategies.
- [Local LLMs](../ai_knowledge/local_llms.md) — On-premises privacy-first inference.

## Sources / references
- [ATH-MaaS Team: OvisOCR2 on Hugging Face](https://huggingface.co/ATH-MaaS/OvisOCR2)
- [Reddit: LocalLLaMA OvisOCR2 Release Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1uv88co/ovisocr2_a_promising_08b_local_document_parser/)
- [OmniDocBench Evaluation Benchmark](https://github.com/u-nico/OmniDocBench)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
