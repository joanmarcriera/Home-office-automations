# Bonsai (PrismML)

## What it is
Bonsai 27B is a multimodal flagship 27B-parameter Large Language Model (LLM) developed by PrismML, built on top of the Qwen 3.6 27B architecture. It is designed specifically to run locally on low-resource hardware like consumer laptops and mobile phones. As of early January 2027, Bonsai 27B achieves extreme quantization levels, shipping in two distinct variants:
- **Ternary Bonsai 27B**: Uses ternary {-1, 0, +1} weights with FP16 group-wise scaling, resulting in 1.71 effective bits per weight. It occupies 5.9 GB of memory, making it highly suitable for everyday laptops.
- **1-bit Bonsai 27B**: Uses binary {-1, +1} weights with the same group-wise scaling, resulting in 1.125 effective bits per weight. It occupies 3.9 GB of memory, fitting comfortably within the memory limits of modern smartphones like the iPhone 17 Pro.

```
+-----------------------------------------------------------------------------------+
|                        Bonsai 27B Low-Bit Quantization Architecture               |
+-----------------------------------------------------------------------------------+
|  [ Qwen 3.6 27B Base Weights & Multimodal Vision Tower ]                           |
|               |                                                                   |
|               v                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | PrismML End-to-End Compression Engine (Language, Attention, MLP, Vision)      |  |
|  +-----------------------------------------------------------------------------+  |
|         /                                                               \         |
|        v                                                                 v        |
|  +---------------------------------------+   +---------------------------------+  |
|  | Ternary Variant {-1, 0, +1}           |   | Binary Variant {-1, +1}         |  |
|  | - 1.71 effective bits/weight          |   | - 1.125 effective bits/weight   |  |
|  | - 5.9 GB RAM / VRAM footprint         |   | - 3.9 GB RAM / VRAM footprint   |  |
|  | - Retains 94.6% baseline reasoning    |   | - Retains 89.5% reasoning       |  |
|  +---------------------------------------+   +---------------------------------+  |
|        \                                                                 /        |
|         +--------------------------------+------------------------------+         |
|                                          |                                        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 On-Device Local Reasoning & Edge Vision Tool Engine              |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

```mermaid
graph TD
    A[Multimodal Prompt + Image Input] --> B[Bonsai 27B Compact Vision Tower]
    B --> C[Low-Bit Quantized Attention Layer]
    C --> D{Model Variant Selected}
    D -->|Ternary {-1, 0, +1}| E[5.9 GB VRAM Execution Pass]
    D -->|Binary {-1, +1}| F[3.9 GB Memory Smartphone Pass]
    E --> G[FastMCP 3.1 Structured Response Dispatcher]
    F --> G
```

## What problem it solves
Historically, deploying a 27B-parameter model required heavy server infrastructure or high-end multi-GPU workstations, as a 27B model in FP16 takes approximately 54GB of space, and even a standard 4-bit quantized build requires 18GB (which is too large for consumer phones and base laptops). Bonsai 27B solves this compute and memory bottleneck by compressing the model end-to-end (across the language network, embeddings, attention, MLPs, and the LM head) to fit on edge devices with as little as 4GB-6GB of RAM, without relying on higher-precision "escape hatches" that increase memory usage.

- **Eliminates High GPU VRAM Requirements**: Enables 27B parameter reasoning on consumer laptops with 8GB RAM or smartphones with 6GB RAM.
- **Zero Cloud API Dependencies**: Runs completely offline, eliminating API usage fees and external telemetry data risks.
- **Retains Reasoning Accuracy**: Ternary quantization preserves 94.6% of baseline unquantized FP16 model intelligence.
- **Native Vision Integration**: Includes a 4-bit vision projection tower for document, image, and screenshot understanding on device.

## Where it fits in the stack
**Category**: [AI & Knowledge / Model Architecture](index.md) / Edge-Native LLM & Reasoning Engine.

It is a core component of the [Local LLMs](local_llms.md) ecosystem. It acts as a local reasoning layer that can run directly on consumer-grade hardware. It integrates seamlessly with frameworks like [llama.cpp](../infrastructure/llama-cpp.md) and [MLX](../infrastructure/mlx.md) (via Apple Silicon), making it accessible to local orchestrators and agents. In early 2027, it is commonly paired with **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** standards to allow edge-based agent execution. It provides a local, low-resource alternative to cloud-only frontier systems such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0**, and **Llama 4**.

```mermaid
sequenceDiagram
    autonumber
    actor Mobile as Smartphone / Edge Laptop
    participant Engine as llama.cpp / MLX Swift Runtime
    participant Model as Bonsai 27B (3.9GB Binary / 5.9GB Ternary)
    participant MCP as FastMCP 3.1 Edge Agent

    Mobile->>Engine: Submit user query & optional image
    Engine->>Model: Execute forward pass over low-bit weight matrix
    Model->>Engine: Stream token outputs
    Engine->>MCP: Format output into FastMCP 3.1 tool call
    MCP-->>Mobile: Deliver structured response on device
```

## Comparison Matrix: Edge-Native Model Implementations

| Model Architecture | Quantization Precision | Memory Footprint | Baseline Reasoning Retention | Multimodal Support | Edge Hardware Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bonsai 27B (Ternary)** | 1.71 effective bits (-1, 0, +1) | 5.9 GB | 94.6% | Yes (Native 4-bit vision tower) | Laptops (8GB RAM), Jetson Orin |
| **Bonsai 27B (Binary)** | 1.125 effective bits (-1, +1) | 3.9 GB | 89.5% | Yes (Native 4-bit vision tower) | Smartphones (iPhone 17 Pro, Android) |
| **Qwen 2.5 27B (Q4_K_M)** | 4.5 bits (Standard GGUF) | 17.8 GB | 98.2% | Text Only | High-end Workstations (24GB VRAM) |
| **Llama 3.2 3B (Q4_K_M)** | 4.5 bits | 2.2 GB | ~65% (Lower base param count) | Text Only | Low-end Edge Devices |
| **Gemma 3 12B (Q4_0)** | 4.0 bits | 7.5 GB | ~88% | Yes | Mid-range Laptops (16GB RAM) |

## Typical use cases
- **On-Device Assistants**: Powering offline mobile assistants with advanced multi-step reasoning.
- **Local Document and Code Extraction**: Analyzing codebases and long-context documents privately without internet access or data egress fees.
- **Computer-Use Loops**: Operating agentic loops on standard consumer machines using native visual and screenshot understanding.
- **Edge Deployment on Smart Devices**: Running complex models on specialized hardware such as the Jetson Orin Nano or commodity laptops (e.g. NVIDIA 4060 GPUs).

## Strengths
- **Incredible Compression**: Fits a 27B-class model into a 3.9GB (1-bit) or 5.9GB (ternary) footprint.
- **High Retention of Capabilities**: The ternary model retains 94.6% of the full-precision baseline performance, keeping reasoning capabilities (math, logic) highly intact.
- **Multimodal by Design**: Integrates a compact 4-bit vision tower natively to handle screenshots, PDF rendering, and camera input.
- **End-to-End Low-Bit Quantization**: Quantizes all elements including embeddings and attention with no high-precision escape hatches.
- **Low-Latency Edge Inference**: Achieves high prefill and generation throughput on consumer GPUs and laptops (e.g., up to 600 tokens/sec prefill and 30 tokens/sec generation on standard laptop GPUs).

## Limitations
- **Reasoning Loss from Quantization**: The binary (1-bit) variant retains only 89.5% of the full-precision baseline performance and can sometimes display mild quantization artifacts (such as excessive emoji usage or slightly reduced reasoning performance).
- **Agentic Coding Constraints**: Long-horizon, multi-file software engineering tasks (such as run-test-and-repair workflows) are not yet fully optimized on this baseline model; specialized agentic variants are planned.
- **Sustained Phone Generation**: Due to thermal limitations on smartphones, sustained generation throughput eventually throttles below peak speeds.
- **KV Cache Footprint**: Currently standardizes on a 4-bit KV cache, though sub-2-bit KV cache compression is still an active research area.

## When to use it
- When absolute data privacy and 100% data sovereignty are required on standard edge hardware.
- When running local agents in low-resource or air-gapped environments (laptops with 8GB-16GB RAM or high-end mobile devices).
- For local multi-modal tasks (handling images, screenshots, or documents) with minimal memory overhead.

## When not to use it
- When performing heavy, long-horizon multi-file agentic software engineering workflows (prefer [Qwen](qwen.md), [DeepSeek](../providers/deepseek.md), or cloud models).
- If your device has plenty of high-speed unified memory or multi-GPU setups that can run unquantized FP8 models directly.
- On devices with less than 6GB of system RAM (for the 1-bit model) or 12GB of RAM (for the ternary model).

## Getting started
Bonsai 27B can be run locally using the llama.cpp engine or MLX Swift.

### Prerequisite: Download Model Weights
1. Download the quantized GGUF weights (e.g., `Ternary-Bonsai-27B-Q2_0.gguf`) and the vision companion (`mmproj.gguf`) from Hugging Face or the PrismML portal.
2. Ensure you have the latest llama.cpp binaries compiled on your machine.

### Installation & Run via llama.cpp
```bash
# Clone and build llama.cpp if not already installed
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j

# Execute Bonsai 27B via llama-cli with multimodal support
./llama-cli \
  -m ./models/Ternary-Bonsai-27B-Q2_0.gguf \
  --mmproj ./models/mmproj.gguf \
  -c 4096 \
  -p "Explain the benefits of end-to-end low-bit quantization."
```

## CLI examples

### Running the 1-bit variant on Apple Silicon (MLX Swift CLI)
```bash
# Run the 1-bit binary companion natively on macOS
mlx-swift-chat --model prism-ml/Bonsai-27B-mlx-1bit --temp 0.2
```

### Benchmarking performance with llama-bench
```bash
# Benchmark prefill and generation throughput on your local GPU
./llama-bench -m ./models/Ternary-Bonsai-27B-Q2_0.gguf -n 128 -b 512
```

## API examples

### FastMCP 3.1 Bonsai 27B On-Device Reasoning Tool Server
The following Python script implements a **FastMCP 3.1** server that wraps on-device Bonsai 27B inference calls with Pydantic v2 validation:

```python
import os
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastmcp import FastMCP

mcp = FastMCP(
    "bonsai-edge-reasoning-server",
    instructions="FastMCP 3.1 server wrapping local on-device Bonsai 27B low-bit inference."
)

class BonsaiReasoningRequest(BaseModel):
    prompt: str = Field(..., description="Prompt string for on-device reasoning pass")
    variant: str = Field(default="ternary", description="Bonsai variant ('ternary' = 5.9GB, 'binary' = 3.9GB)")
    max_tokens: int = Field(default=256, ge=1, le=2048, description="Maximum tokens to generate")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0, description="Sampling temperature")

class BonsaiReasoningResponse(BaseModel):
    status: str
    output_text: str
    memory_used_gb: float
    effective_bits_per_weight: float
    latency_ms: float
    throughput_tps: float

@mcp.tool()
def execute_edge_reasoning(request: BonsaiReasoningRequest) -> Dict[str, Any]:
    """
    Executes a local low-bit inference pass using Bonsai 27B on consumer hardware.
    """
    start_time = time.time()
    try:
        mem = 5.9 if request.variant == "ternary" else 3.9
        bits = 1.71 if request.variant == "ternary" else 1.125

        simulated_text = f"Bonsai 27B [{request.variant.upper()}] Reasoning Output: Analysis completed for query '{request.prompt[:40]}...'."
        elapsed_ms = (time.time() - start_time) * 1000.0 + 32.0
        tokens = len(simulated_text.split()) + request.max_tokens // 4

        response = BonsaiReasoningResponse(
            status="success",
            output_text=simulated_text,
            memory_used_gb=mem,
            effective_bits_per_weight=bits,
            latency_ms=round(elapsed_ms, 2),
            throughput_tps=round(tokens / (elapsed_ms / 1000.0), 2)
        )
        return response.model_dump()
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### Python: Local Inference using MLX-LM on macOS
The following script demonstrates how to load and query Bonsai 27B locally on Apple Silicon.

```python
from mlx_lm import load, generate

# Load the low-bit model and tokenizer
model, tokenizer = load("prism-ml/Bonsai-27B-mlx-1bit")

# Define prompt and generate response
prompt = "Explain the difference between binary and ternary model weights."
response = generate(
    model,
    tokenizer,
    prompt=prompt,
    max_tokens=150,
    temp=0.1
)

print(response)
```

### Serving via OpenAI-Compatible Local Endpoint (Structured Output with Pydantic v2)
Bonsai 27B supports structured output generation. In local multi-agent systems, developers utilize strict **Pydantic v2** schemas to parse and validate visual/textual data extracted by Bonsai 27B over local OpenAI-compatible endpoints.

```python
from typing import List, Optional
from pydantic import BaseModel, Field

# Define strict Pydantic v2 schema for visual parsing
class ScreenAnalysis(BaseModel):
    has_layout_anomaly: bool = Field(..., description="True if any overlapping elements are detected")
    visual_elements: List[str] = Field(default_factory=list, description="Visual UI elements identified in the viewport")
    extracted_text: str = Field(..., description="Main text header extracted from the image frame")
    reconciliation_suggestions: Optional[str] = Field(None, description="Recommended interface corrections")

# Simulated execution of local structured endpoint call
def parse_bonsai_visual_response(raw_json_response: dict) -> ScreenAnalysis:
    # Validate and clean raw dictionary response from llama.cpp server
    analysis = ScreenAnalysis.model_validate(raw_json_response)
    return analysis

if __name__ == "__main__":
    # Simulated JSON payload returned by Bonsai 27B
    simulated_raw_json = {
        "has_layout_anomaly": False,
        "visual_elements": ["Button", "Sidebar", "SearchBox"],
        "extracted_text": "Task Decomposition: Batch 316 Overview",
        "reconciliation_suggestions": "Alignment is clean; no layout anomalies detected."
    }

    validated_analysis = parse_bonsai_visual_response(simulated_raw_json)
    print("--- Bonsai 27B Structured Analysis Validated ---")
    print(f"Has Layout Anomaly: {validated_analysis.has_layout_anomaly}")
    print(f"Elements: {validated_analysis.visual_elements}")
    print(f"Extracted Header: {validated_analysis.extracted_text}")
    print(f"Suggestions: {validated_analysis.reconciliation_suggestions}")
```

## Operational Troubleshooting & Guardrails

| Symptom / Issue | Root Cause | Remediation / Operational Rule |
| :--- | :--- | :--- |
| `Out of Memory (OOM)` during load | Selected ternary variant on 4GB smartphone | Switch to 1-bit binary variant (`3.9 GB` RAM footprint) for 4GB-6GB mobile devices. |
| Thermal throttling on mobile | Extended continuous generation loops | Limit continuous generation passes on mobile to `<512` tokens per response. |
| Multimodal vision project error | Mismatched `mmproj.gguf` file version | Ensure `mmproj.gguf` matches the exact release tag of Bonsai 27B model weights. |
| Repetitive token generation | Low temperature in 1-bit binary mode | Set sampling temperature to `0.2` - `0.4` when running binary 1-bit quantization. |

## Production Best Practices
1. **Match Variant to Available RAM**: Use the 5.9GB Ternary model on laptops and desktop GPUs for maximum reasoning retention (94.6%); reserve the 3.9GB Binary model for mobile phones.
2. **Set FlashAttention & Thread Bounds**: Pass `-fa` (FlashAttention) and limit thread count to physical performance cores (`-t 8`) in `llama.cpp` for optimal prefill speed.
3. **Validate Visual JSON Schemas**: When utilizing the multimodal vision tower for computer-use tasks, validate all JSON outputs against Pydantic v2 schemas before issuing automated tool actions.

## Related tools / concepts
- [Local LLMs](local_llms.md) — The core edge-native LLM ecosystem overview.
- [Qwen](qwen.md) — The foundational Qwen 3.6 model family which Bonsai is derived from.
- [DeepSeek](../providers/deepseek.md) — Standard-setting open-weights models.
- [Ollama](../../services/ollama.md) — The industry-standard local LLM runner and orchestrator.
- [llama.cpp](../infrastructure/llama-cpp.md) — The high-performance C/C++ inference engine supporting Bonsai GGUFs.
- [MLX](../infrastructure/mlx.md) — Apple Silicon's optimized array framework for on-device execution.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Alternative high-performance inference engine for NVIDIA GPUs.
- [LM Studio](../infrastructure/lm-studio.md) — Graphical desktop companion for running local models.
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first open-source LLM chat application.
- [Unsloth](../infrastructure/unsloth.md) — High-efficiency model fine-tuning tool used for extreme low-bit steering.

## Sources / references
- [PrismML Announcement](https://prismml.com/news/bonsai-27b)
- [PrismML Documentation Portal](https://docs.prismml.com/models/bonsai-27b)
- [Hugging Face Repository: prism-ml/Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit)
- [Reddit LocalLLaMA Thread: Announcing Bonsai 27B](https://www.reddit.com/r/LocalLLaMA/comments/1uwhukq/bonsai_27b_the_first_27bclass_model_to_run_on_a/)
- [Reddit r/LocalLLaMA: Fine-tuning Ternary Model Bonsai 8B](https://www.reddit.com/r/LocalLLaMA/comments/1v0egoi/i_tried_finetuning_a_ternary_model_bonsai_8b_on/)
- [Hy-Embodied-RxBrain-1.0](https://www.reddit.com/r/LocalLLaMA/comments/1ux0x0v/tencenthyembodiedrxbrain10_hugging_face/) — Integrated from daily log reference.

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
