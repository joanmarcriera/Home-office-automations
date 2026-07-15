# OvisOCR2

OvisOCR2 is a compact, end-to-end 0.8B parameter vision-language model (VLM) specifically optimized for high-fidelity document parsing. As of July 2026, it represents the state-of-the-art for local, page-level document understanding, converting complex page images directly into structured Markdown.

## What it is
Developed by the ATH-MaaS team, OvisOCR2 is a specialized VLM built by post-training Qwen3.5-0.8B. It is designed to interpret document layouts and extract content—including text, mathematical formulas, and complex tables—into a clean Markdown representation that preserves natural reading order.

## What problem it solves
Traditional OCR pipelines often rely on multiple disconnected steps (layout detection, text extraction, table parsing, formula recognition), which leads to error accumulation and high latency. OvisOCR2 solves this by using a single, end-to-end model that understands the entire page context simultaneously, reducing complexity and improving accuracy on challenging document structures.

## Where it fits in the stack
**Category**: [Process & Understanding](index.md). It serves as a high-performance ingestion engine for [RAG Patterns](../../knowledge_base/patterns/rag-pattern.md). Within an [MCP](../../automation_orchestration/mcp.md) ecosystem, OvisOCR2 can be deployed as a specialized tool for transforming physical or digital document scans into structured data for reasoning models like [Gemma 3](../ai_knowledge/local_llms.md).

## Typical use cases
- **Academic Research**: Converting dense papers with complex LaTeX formulas into searchable Markdown.
- **Financial Services**: High-accuracy extraction of borderless tables from financial reports.
- **Legal Automation**: Preserving strict reading order and hierarchical structure in multi-column legal documents.
- **Local RAG Pipelines**: Powering privacy-first document ingestion on consumer-grade hardware (e.g., laptops with 10GB VRAM).

## Strengths
- **Efficiency**: At only 0.8B parameters, it offers extremely high throughput and can be deployed on edge devices or modest GPUs.
- **Superior Accuracy**: Achieves frontier-level scores (96.58 on OmniDocBench v1.6), outperforming many larger pipeline-based methods.
- **End-to-End**: Handles text, tables, and formulas in a single pass without needing separate models.
- **Developer Friendly**: Features native [vLLM](../infrastructure/vllm.md) support and uses an Apache 2.0 license.

## Limitations
- **Page-at-a-time**: Optimized for individual page images; multi-page document consistency must be managed by the orchestration layer.
- **Context Length**: While efficient, extremely long or dense documents may reach the model's processing limits compared to multi-billion parameter VLMs.
- **Resolution Sensitivity**: Performance is best when the input image resolution is high enough to make small text legible.

## When to use it
- When you need to parse documents locally with high accuracy but have limited VRAM (< 8-10GB).
- For automated transcription of scientific documents containing heavy LaTeX.
- As a faster, lighter alternative to [Docling](docling.md) or [Unstructured](../intake_storage/unstructured.md) for pure Markdown conversion.

## When not to use it
- For general-purpose image captioning (use [Moondream](../ai_knowledge/moondream.md)).
- For complex multi-step reasoning about the document's *content* (pair it with [Gemma 3](../ai_knowledge/local_llms.md) or [Claude 4.8](../ai_knowledge/claude.md)).
- If your pipeline requires non-Markdown output formats like direct Excel or Word export.

## Getting started

### Installation
OvisOCR2 is best run using the vLLM engine for high performance.

```bash
pip install "vllm>=0.22.1" pillow
```

### Loading the Model
You can pull the weights from Hugging Face (`ATH-MaaS/OvisOCR2`).

```python
from vllm import LLM
model = LLM(model="ATH-MaaS/OvisOCR2", tensor_parallel_size=1)
```

## CLI examples
Using the `vllm` CLI to start a local server for OvisOCR2:

```bash
# Start an OpenAI-compatible API server
python -m vllm.entrypoints.openai.api_server --model ATH-MaaS/OvisOCR2

# Register OvisOCR2 as an MCP server (typical pattern)
mcp register ovis-parser --command "vllm" --args "serve --model ATH-MaaS/OvisOCR2"
```

## API examples

### Basic Document Parsing (Python)
This example demonstrates how to use the model with the vLLM library.

```python
from PIL import Image
from vllm import LLM, SamplingParams

# Initialize
llm = LLM(model="ATH-MaaS/OvisOCR2", gpu_memory_utilization=0.8)
sampling_params = SamplingParams(temperature=0, max_tokens=4096)

# Prepare Prompt
prompt = "Extract all readable content from the image in natural human reading order and output the result as a single Markdown document. Format formulas as LaTeX. Format tables as HTML: <table>...</table>."

# Run Inference
image = Image.open("page_scan.jpg")
outputs = llm.generate([{"prompt": prompt, "multi_modal_data": {"image": image}}], sampling_params)

print(outputs[0].outputs[0].text)
```

## Related tools / concepts
- [Docling](docling.md) — IBM's document parsing framework.
- [Moondream](../ai_knowledge/moondream.md) — Lightweight vision model for general tasks.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference engine.
- [Tesseract CLI](tesseract.md) — Traditional OCR engine.
- [OCRmyPDF](ocrmypdf.md) — PDF-to-PDF OCR layering.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Integrating parsed data into LLM workflows.
- [Local LLMs](../ai_knowledge/local_llms.md) — Running models on-premises.

## Sources / references
- [OvisOCR2 on Hugging Face](https://huggingface.co/ATH-MaaS/OvisOCR2)
- [Reddit: OvisOCR2: a promising 0.8B local document parser](https://www.reddit.com/r/LocalLLaMA/comments/1uv88co/ovisocr2_a_promising_08b_local_document_parser/)
- [OmniDocBench Leaderboard](https://github.com/u-nico/OmniDocBench)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
