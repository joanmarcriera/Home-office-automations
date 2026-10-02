# OvisOCR2

## What it is
OvisOCR2 is a highly compact, end-to-end 0.8B parameter vision-language model (VLM) specifically post-trained and optimized for high-fidelity document parsing, layout understanding, and structured data extraction. Developed by the ATH-MaaS research team, it represents the state of the art for local, page-level document intelligence, converting complex scanned pages, technical blueprints, dense mathematical formulas, and multi-column tables directly into structured Markdown, HTML, or validated JSON.

In early 2027, OvisOCR2 serves as a core edge vision layer within enterprise document processing workflows and autonomous agent pipelines. By post-training the highly efficient Qwen3.5-0.8B base architecture, OvisOCR2 achieves page-level parsing accuracy on par with proprietary multi-billion parameter vision models while requiring less than 2.5 GB of GPU VRAM. Featuring native compatibility with high-throughput inference engines like [vLLM](../infrastructure/vllm.md) and standardized agent protocol bindings via **FastMCP 3.1**, OvisOCR2 enables fully local, air-gapped document ingesting for retrieval-augmented generation ([RAG](../../knowledge_base/patterns/rag-pattern.md)) architectures.

## What problem it solves
Legacy document parsing architectures rely on fragmented, multi-stage pipelines that combine heuristic layout segmentation engines, optical character recognition (OCR) line extractors, table region detection models, and LaTeX post-processors. These multi-stage systems suffer from cumulative error propagation, high latency, complex container management, and fragile layout reconstruction. OvisOCR2 addresses these core operational issues:

1. **Eliminates Multi-Stage Pipeline Complexity:** Traditional parsing requires maintaining separate services for text OCR (Tesseract), table extraction, and layout detection (LayoutLM). OvisOCR2 processes the entire document image in a single forward vision-language pass, outputting fully formatted Markdown and structured tables simultaneously.
2. **Preserves Dense Reading Order & Complex Hierarchy:** Standard OCR engines frequently scramble multi-column layouts, footnotes, sidebar annotations, and inline mathematical expressions. OvisOCR2 retains native reading order across academic papers, legal briefs, and financial filings.
3. **Reduces Hardware & Latency Constraints:** Unlike multi-billion parameter vision models that require enterprise GPU clusters, OvisOCR2's 0.8B footprint allows real-time document parsing on edge devices, consumer laptops, or cost-effective cloud instances with sub-second page throughput.
4. **Ensures Air-Gapped Privacy & Regulatory Compliance:** Organizations handling confidential legal contracts, medical records (HIPAA), or sensitive financial ledgers can process documents completely on-premises without streaming raw page images to third-party cloud vision APIs.

## Where it fits in the stack
**Layer 5: Process & Understanding / Vision-Language Document Intelligence.** OvisOCR2 functions as the primary visual ingestion engine in document processing pipelines. It consumes raw image binaries (PNG, JPEG, WebP) or converted PDF pages, extracts layout hierarchy, formulas, and tabular structures, and feeds sanitized Markdown/JSON artifacts into downstream indexing engines, vector databases (Qdrant, ChromaDB), or agentic reasoning orchestrators powered by [Claude 5.1](../providers/anthropic.md), [Gemma 4](../ai_knowledge/local_llms.md), or [OpenAI GPT-5.5](openai.md).

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             Unstructured Document Sources                                │
│       (Scanned PDF Pages / Historical Books / Medical Records / Legal Filings)            │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                     Raw Image Stream
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            OvisOCR2 Vision-Language Engine                               │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Visual Encoder (ViT / Qwen3.5-Vision Backbone)                  │  │
│  │     High-Resolution Patch Extraction & Spatial Layout Position Embeddings          │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    0.8B Parameter Causal Language Decoder                          │  │
│  │     Autoregressive Generation of Markdown, LaTeX Formulas, & HTML Tables           │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    FastMCP 3.1 Server / vLLM Async API Gateway                      │  │
│  │     Exposes /v1/chat/completions & Native MCP Document Parsing Tools               │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            Structured Knowledge Artifacts                                │
│       (Validated JSON Schemas / Clean Markdown / Vector Database Chunk Embeddings)        │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Academic Paper & Formula Parsing:** Extracting dense mathematical formulas (LaTeX), theorems, and multi-author citations from multi-column arXiv PDF scans.
- **Financial Statement & Balance Sheet Extraction:** Converting borderless corporate balance sheets, quarterly income tables, and earnings reports into clean Markdown/HTML tables.
- **Legal Brief & Contract Indexing:** Ingesting complex legal filings while preserving section hierarchies, footers, paragraph numbering, and marginalia.
- **Medical Chart & Prescription Digitalization:** Extracting hand-written diagnostic notes, lab results, and patient charts into HIPAA-compliant local database schemas.
- **Air-Gapped Local RAG Pipelines:** Powering high-throughput document ingestion pipelines in secure defense, healthcare, or financial enterprise networks without external internet dependencies.

## Strengths
- **Incredibly Lightweight Footprint:** Uses only 0.8 billion parameters, requiring less than 2.5 GB VRAM for FP16 inference, making it runnable on consumer GPUs, Apple Silicon, or edge hardware.
- **SOTA Parsing Accuracy:** Scores 96.6+ on the OmniDocBench v1.6 evaluation suite, outperforming closed-source multi-billion parameter cloud vision models on complex table and formula parsing.
- **Single-Pass End-to-End Decoding:** Eliminates fragile multi-model pipelines by outputting text, LaTeX, layout markers, and Markdown in a single visual forward pass.
- **High-Throughput vLLM & FastMCP 3.1 Integration:** Built-in support for vLLM tensor parallel serving, continuous batching, and FastMCP 3.1 agent tool execution.
- **Permissive Open-Source License:** Released under the Apache 2.0 license, permitting unrestricted commercial distribution, modification, and embedding into proprietary software.

## Limitations
- **Single-Page Focus:** Optimized primarily for individual page image inputs; multi-page document stitching, table continuation, and cross-page indexing must be handled by external orchestrators.
- **Sensitivity to Image Resolution:** Extremely low-resolution scans (< 100 DPI) or severely distorted page warps can lead to hallucinated characters or dropped table cells.
- **Narrow Specialization:** Tailored specifically for document parsing and OCR; it is not designed for general-purpose visual conversational QA or open-ended image descriptions (pair with [Moondream](../ai_knowledge/moondream.md) or [Gemma 4](../ai_knowledge/local_llms.md)).

## When to use it
- When you require **fast, local, privacy-compliant document OCR** on modest hardware with zero external cloud dependencies.
- For converting technical papers containing mixed text, borderless tables, and complex LaTeX equations into clean Markdown.
- As a lightweight, high-performance alternative to heavier multi-stage document processors like [Docling](docling.md) or [Unstructured](../intake_storage/unstructured.md).

## When not to use it
- For general-purpose visual dialogue, object detection, or natural image description — use [Moondream](../ai_knowledge/moondream.md) or [Qwen-VL](qwen-vl.md).
- When your application requires direct output to proprietary binary formats like Microsoft Word (.docx) or Excel (.xlsx) — use [Docling](docling.md).

## Getting started

### Installation
OvisOCR2 can be deployed via PyTorch or high-throughput serving engines like vLLM:

```bash
# Install vLLM, PyTorch, Pillow, and Pydantic v2
pip install "vllm>=0.22.1" pillow "pydantic>=2.10.0" requests
```

### Basic Inference with vLLM (Python)
```python
from vllm import LLM, SamplingParams
from PIL import Image

# Initialize OvisOCR2 with vLLM engine
llm = LLM(model="ATH-MaaS/OvisOCR2", gpu_memory_utilization=0.5, max_model_len=4096)
sampling_params = SamplingParams(temperature=0.0, max_tokens=2048)

# Load document image
image = Image.open("sample_page.png")

# Execute vision-language page extraction
prompt = "<|im_start|>system\nYou are a precise document OCR engine. Extract all text, tables, and formulas from the page in structured Markdown.<|im_end|>\n<|im_start|>user\n<image>\nExtract the document content:<|im_end|>\n<|im_start|>assistant\n"

outputs = llm.generate([{"prompt": prompt, "multi_modal_data": {"image": image}}], sampling_params)
print("Extracted Markdown:\n", outputs[0].outputs[0].text)
```

## CLI examples

### Serving OvisOCR2 over an OpenAI-Compatible vLLM Endpoint
```bash
# Launch local OpenAI REST server on port 8000 using vLLM
python3 -m vllm.entrypoints.openai.api_server \
  --model ATH-MaaS/OvisOCR2 \
  --port 8000 \
  --gpu-memory-utilization 0.6 \
  --max-model-len 4096 \
  --trust-remote-code
```

### Performing Page Extraction via cURL
```bash
# Convert image to base64 and send to OpenAI-compatible endpoint
IMAGE_B64=$(base64 -w 0 sample_page.png)

curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ATH-MaaS/OvisOCR2",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Extract all content from this page into structured Markdown with LaTeX formulas."},
          {"type": "image_url", "image_url": {"url": "data:image/png;base64,'"$IMAGE_B64"'"}}
        ]
      }
    ],
    "max_tokens": 2048,
    "temperature": 0.0
  }'
```

## API examples

### FastMCP 3.1 OvisOCR2 Document Extraction Server
The python script below implements a complete FastMCP 3.1 server that exposes document extraction tools and validates extracted layout structures using strict **Pydantic v2** models.

```python
import base64
import io
import requests
from typing import List, Literal, Optional
from PIL import Image
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("OvisOCR2-Document-Processor")

# ============================================================================
# Pydantic v2 Models for Layout & Document Extraction Validation
# ============================================================================

class ExtractedBlock(BaseModel):
    block_type: Literal["header", "paragraph", "table", "formula", "footer"] = Field(..., description="Classification of the layout block")
    reading_order: int = Field(..., ge=0, description="Sequential reading order index")
    content: str = Field(..., min_length=1, description="Extracted text, LaTeX, or HTML content")

class PageExtractionResult(BaseModel):
    page_number: int = Field(default=1, ge=1)
    detected_language: str = Field(default="en")
    blocks: List[ExtractedBlock] = Field(default_factory=list)
    has_latex_formulas: bool = Field(default=False)
    has_tables: bool = Field(default=False)
    raw_markdown: str = Field(..., description="Full raw Markdown output")

class ServerStatus(BaseModel):
    status: str
    server_url: str
    model_name: str = "ATH-MaaS/OvisOCR2"

# ============================================================================
# FastMCP 3.1 Tools
# ============================================================================

@mcp.tool(
    name="ovis_parse_document_page",
    description="Sends a local image file to the OvisOCR2 server to extract structured Markdown and LaTeX content."
)
def parse_document_page(
    image_filepath: str,
    vllm_server_url: str = "http://localhost:8000",
    max_tokens: int = 2048
) -> str:
    try:
        # Load and validate local image file
        with Image.open(image_filepath) as img:
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as img_err:
        return f"Error loading image file '{image_filepath}': {str(img_err)}"

    endpoint = f"{vllm_server_url.rstrip('/')}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    prompt_text = (
        "Extract all text, tables, and mathematical formulas from this document page. "
        "Format output as structured Markdown. Use LaTeX for math ($...$ or $$...$$) and HTML for complex tables."
    )

    payload = {
        "model": "ATH-MaaS/OvisOCR2",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.0
    }

    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        if res.status_code == 200:
            data = res.json()
            raw_text = data["choices"][0]["message"]["content"]

            # Simple heuristic detection for LaTeX and Tables
            has_math = "$" in raw_text or "\\begin{" in raw_text
            has_table = "|---" in raw_text or "<table>" in raw_text

            result = PageExtractionResult(
                page_number=1,
                raw_markdown=raw_text,
                has_latex_formulas=has_math,
                has_tables=has_table
            )
            return result.model_dump_json(indent=2)
        else:
            return f"vLLM API Error ({res.status_code}): {res.text}"
    except Exception as err:
        return f"Execution Failure: {str(err)}"

@mcp.tool(
    name="ovis_check_server_status",
    description="Validates connectivity to the background vLLM OvisOCR2 engine."
)
def check_server_status(vllm_server_url: str = "http://localhost:8000") -> str:
    endpoint = f"{vllm_server_url.rstrip('/')}/v1/models"
    try:
        res = requests.get(endpoint, timeout=5)
        if res.status_code == 200:
            status = ServerStatus(status="healthy", server_url=vllm_server_url)
            return status.model_dump_json(indent=2)
        return f"Server Error ({res.status_code}): {res.text}"
    except Exception as err:
        return f"Connection Failed: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## Benchmark & Performance Comparison Matrix

OvisOCR2 achieves remarkable accuracy on document parsing benchmarks while maintaining a fraction of the parameter count of competing models.

| Vision Model Engine | Parameter Count | VRAM Footprint (FP16) | OmniDocBench v1.6 Score | Math / LaTeX Accuracy | Table Extraction Score | Average Page Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OvisOCR2 (ATH-MaaS)** | **0.8 Billion** | **2.2 GB VRAM** | **96.6 / 100** | **94.8%** | **95.2%** | **0.45 sec** |
| **Moondream2** | 1.8 Billion | 3.8 GB VRAM | 82.1 / 100 | 71.4% | 76.0% | 0.85 sec |
| **Got-OCR2.0** | 5.0 Billion | 10.5 GB VRAM | 91.4 / 100 | 88.2% | 89.1% | 1.40 sec |
| **Qwen2-VL 7B** | 7.0 Billion | 15.2 GB VRAM | 94.2 / 100 | 92.0% | 93.5% | 2.10 sec |
| **Tesseract 5 (Traditional)**| N/A (Rule Engine)| < 0.2 GB RAM | 61.5 / 100 | 12.0% | 45.0% | 0.12 sec |

## Document Extraction & Operational Troubleshooting Runbook

### Scenario: Setting Up an On-Premises Bulk Document Ingestion Worker
1. **Prepare Host Environment:**
   - Provision Ubuntu 24.04 LTS server with an NVIDIA RTX 4090 or L4 GPU (minimum 8GB VRAM).
   - Verify CUDA 12.x drivers and vLLM dependencies:
     ```bash
     nvidia-smi
     python3 -c "import torch; print(torch.cuda.is_available())"
     ```

2. **Deploy vLLM Background Service:**
   Create `/etc/systemd/system/ovisocr2.service`:
   ```ini
   [Unit]
   Description=OvisOCR2 vLLM Serving Engine
   After=network.target

   [Service]
   Type=simple
   User=ollama
   Group=ollama
   ExecStart=/usr/local/bin/python3 -m vllm.entrypoints.openai.api_server \
     --model ATH-MaaS/OvisOCR2 \
     --host 127.0.0.1 \
     --port 8000 \
     --gpu-memory-utilization 0.5 \
     --max-model-len 4096
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. **Batch Image Preprocessing Protocol:**
   - Normalize source document page scans to 300 DPI PNG format.
   - Resize oversized high-resolution images (> 4096px edge) to prevent context window overflow while maintaining text clarity.

4. **Troubleshooting Common Parsing Issues:**
   - **Error: `CUDA Out of Memory` during vLLM launch:** Reduce `--gpu-memory-utilization` from `0.9` to `0.5` or lower `--max-model-len` to `4096`.
   - **Garbled Table Outputs:** If complex borderless tables collapse into continuous paragraphs, append explicit layout instruction prompts: `"Extract tables as clean HTML <table>...</table> structures."`
   - **Dropped Formula Subscripts:** Ensure input images are correctly oriented (upright). Rotate sideways scans prior to sending base64 payloads to the OvisOCR2 vision encoder.

## Related tools / concepts
- [Docling](docling.md) — IBM's enterprise multi-format document conversion engine.
- [Moondream](../ai_knowledge/moondream.md) — Ultra-lightweight general-purpose vision VLM.
- [vLLM](../infrastructure/vllm.md) — Blazing-fast inference serving framework.
- [Tesseract CLI](tesseract.md) — Traditional command-line OCR engine.
- [OCRmyPDF](ocrmypdf.md) — PDF searchable layer injector.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Enterprise knowledge retrieval strategies.
- [Local LLMs](../ai_knowledge/local_llms.md) — On-premises privacy-first inference.

## Sources / references
- [ATH-MaaS Team: OvisOCR2 Repository on Hugging Face](https://huggingface.co/ATH-MaaS/OvisOCR2)
- [OmniDocBench Evaluation Benchmark Suite](https://github.com/u-nico/OmniDocBench)
- [Qwen3.5 Vision-Language Architecture Reference](https://huggingface.co/Qwen)
- [vLLM Multi-Modal Serving Guide](https://docs.vllm.ai/en/latest/models/multimodal.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
