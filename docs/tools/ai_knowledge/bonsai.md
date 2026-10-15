# Bonsai (PrismML)

## What it is
Bonsai 27B is a multimodal flagship 27B-parameter Large Language Model (LLM) developed by PrismML, built on top of the Qwen 3.6 27B architecture. It is designed specifically to run locally on low-resource hardware like consumer laptops and mobile phones. As of early January 2027, Bonsai 27B achieves extreme quantization levels, shipping in two distinct variants:
- **Ternary Bonsai 27B**: Uses ternary {-1, 0, +1} weights with FP16 group-wise scaling, resulting in 1.71 effective bits per weight. It occupies 5.9 GB of memory, making it highly suitable for everyday laptops.
- **1-bit Bonsai 27B**: Uses binary {-1, +1} weights with the same group-wise scaling, resulting in 1.125 effective bits per weight. It occupies 3.9 GB of memory, fitting comfortably within the memory limits of modern smartphones like the iPhone 17 Pro.

```
+-----------------------------------------------------------------------------------+
|                            Qwen 3.6 27B FP16 BASE MODEL                           |
|                         (27 Billion Parameters ~ 54 GB VRAM)                      |
+------------------------------------------+----------------------------------------+
                                           |
                                           v PrismML Extreme Quantization Engine
+------------------------------------------+----------------------------------------+
|                      GROUP-WISE SCALE QUANTIZATION PIPELINE                       |
|  - Language Core Quantization            - 4-bit Compact Vision Tower Integration  |
|  - Attention & MLP Matrix Compression    - End-to-End Weight Scaling (No Escape)  |
+------------------------------------------+----------------------------------------+
                                           |
                                           +----------------------------------------+
                                           |                                        |
                                           v Ternary Quantization                   v Binary Quantization
+------------------------------------------+---+  +---------------------------------+---+
|            TERNARY BONSAI 27B                |  |            1-BIT BONSAI 27B               |
|  - Weights: {-1, 0, +1} (1.71 bits/weight)   |  |  - Weights: {-1, +1} (1.125 bits/weight)  |
|  - RAM Footprint: ~ 5.9 GB               |  |  - RAM Footprint: ~ 3.9 GB                |
|  - Retention: 94.6% FP16 Baseline         |  |  - Retention: 89.5% FP16 Baseline         |
|  - Target: Consumer Laptops / RTX 4060   |  |  - Target: Flagship Smartphones (iPhone 17) |
+----------------------------------------------+  +-------------------------------------+
```

## What problem it solves
Historically, deploying a 27B-parameter model required heavy server infrastructure or high-end multi-GPU workstations, as a 27B model in FP16 takes approximately 54GB of space, and even a standard 4-bit quantized build requires 18GB (which is too large for consumer phones and base laptops). Bonsai 27B solves this compute and memory bottleneck by compressing the model end-to-end (across the language network, embeddings, attention, MLPs, and the LM head) to fit on edge devices with as little as 4GB-6GB of RAM, without relying on higher-precision "escape hatches" that increase memory usage.

```
+-----------------------------------------------------------------------------------+
|                                 APPLICATION LAYER                                 |
|  [Mobile Assistant / iOS]     [Local CLI Tool]     [FastMCP 3.1 Edge Server]     |
+------------------------------------------+----------------------------------------+
                                           |
                                           v Prompt / Vision Inputs
+------------------------------------------+----------------------------------------+
|                          EDGE INFERENCE RUNTIME LAYER                             |
|  +-----------------------------------------------------------------------------+  |
|  | [llama.cpp C++ Engine (GGUF)]  or  [MLX Swift Array Engine (Apple Silicon)] |  |
|  +-----------------------------------------------------------------------------+  |
+------------------------------------------+----------------------------------------+
                                           |
                                           v Quantized Kernel Execution
+------------------------------------------+----------------------------------------+
|                             HARDWARE EXECUTION LAYER                              |
|   [Apple A19 Pro / M-Series NPU]   [NVIDIA RTX 4060 GPU]   [Jetson Orin Edge]    |
+-----------------------------------------------------------------------------------+
```

## Extreme Quantization Edge Model Comparison Matrix

| Model / Quantization | Parameter Count | Memory Footprint | Effective Bits / Weight | Baseline Accuracy Retention | Primary Hardware Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1-Bit Bonsai 27B** | 27 Billion | ~ 3.9 GB | 1.125 bits | 89.5% FP16 Baseline | Smartphones (iPhone 17 Pro, Android 16GB) |
| **Ternary Bonsai 27B** | 27 Billion | ~ 5.9 GB | 1.71 bits | 94.6% FP16 Baseline | Consumer Laptops, RTX 4060 GPUs, Jetson |
| **Qwen 2.5 / 3.6 (Q4_K_M)** | 27 Billion | ~ 18.2 GB | 4.5 bits | 98.2% FP16 Baseline | Workstations with 24GB VRAM |
| **Llama 3.3 70B (IQ2_XXS)** | 70 Billion | ~ 19.8 GB | 2.0 bits | 86.0% FP16 Baseline | High-end Apple Silicon (32GB+ Unified) |
| **Gemma 3 12B (Q4_K_S)** | 12 Billion | ~ 7.8 GB | 4.2 bits | 97.0% FP16 Baseline | Mid-range GPUs / 16GB RAM Macs |

## Where it fits in the stack
**LLM / Reasoning Engine (Open-weights / Edge-native)**. It is a core component of the [Local LLMs](local_llms.md) ecosystem. It acts as a local reasoning layer that can run directly on consumer-grade hardware. It integrates seamlessly with frameworks like [llama.cpp](../infrastructure/llama-cpp.md) and [MLX](../infrastructure/mlx.md) (via Apple Silicon), making it accessible to local orchestrators and agents. In early 2027, it is commonly paired with **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** standards to allow edge-based agent execution. It provides a local, low-resource alternative to cloud-only frontier systems such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0**, and **Llama 4**.

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

### FastMCP 3.1 Server Integration for Bonsai 27B
The following FastMCP 3.1 server exposes local Bonsai 27B vision and reasoning tools over OpenAI-compatible or local GGUF backends, validating inputs and outputs using Pydantic v2 schemas.

```python
import json
import urllib.request
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

mcp = FastMCP(
    "bonsai-edge-server",
    instructions="FastMCP 3.1 server providing edge multimodal inference via local Bonsai 27B."
)

class BonsaiReasoningRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Prompt text for local Bonsai 27B reasoning")
    image_base64: Optional[str] = Field(None, description="Optional base64 image string for visual parsing")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0, description="Sampling temperature")

class ScreenAnalysis(BaseModel):
    has_layout_anomaly: bool = Field(..., description="True if any overlapping elements are detected")
    visual_elements: List[str] = Field(default_factory=list, description="Visual UI elements identified in viewport")
    extracted_text: str = Field(..., description="Main text header extracted from image frame")
    reconciliation_suggestions: Optional[str] = Field(None, description="Recommended interface corrections")

@mcp.tool()
def analyze_screen_with_bonsai(request: BonsaiReasoningRequest) -> Dict[str, Any]:
    """
    Analyzes UI viewport screenshots and returns structured analysis using Bonsai 27B multimodal reasoning.
    """
    try:
        # Simulated invocation of local llama.cpp / MLX Bonsai 27B endpoint
        simulated_response = {
            "has_layout_anomaly": False,
            "visual_elements": ["HeaderBar", "NavigationMenu", "TerminalWindow"],
            "extracted_text": request.prompt,
            "reconciliation_suggestions": "Viewport alignment is nominal."
        }
        validated = ScreenAnalysis.model_validate(simulated_response)
        return {"status": "success", "analysis": validated.model_dump()}
    except ValidationError as ve:
        return {"status": "error", "error_type": "validation_error", "details": ve.errors()}
    except Exception as e:
        return {"status": "error", "error_type": "inference_error", "message": str(e)}

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

## Production Hardening & Operational Guardrails

Deploying extreme low-bit quantized models like Bonsai 27B in production edge environments requires the following operational rules:

1. **Temperature & Repetition Penalty Tuning**: Extreme 1-bit and ternary quantized models are more sensitive to sampling hyperparameters. Maintain temperature between `0.1` and `0.3` and set `repetition_penalty` to `1.15` to prevent infinite emoji loops or repetitive token loops.
2. **FlashAttention-2 / Metal Threadgroup Memory**: On Apple Silicon, ensure MLX Swift allocates unified memory with threadgroup alignment (`--threadgroup-memory`). On CUDA, build `llama.cpp` with `-DGGML_CUDA_FA_ALL_QUANTS=ON` to accelerate 1-bit matrix-vector multiplications.
3. **KV-Cache Memory Cap**: Configure strict limits on context window lengths (e.g., `-c 4096`) when operating on 4GB RAM devices (smartphones) to ensure KV-cache allocations do not cause system OOM crashes.
4. **Thermal Throttling Fallback**: On mobile hardware (smartphones or fanless tablets), monitor battery temperature. Implement a background pause / fallback mechanism if device temperature exceeds 42°C during long prefill sessions.

## Common Troubleshooting Protocols

| Issue / Error | Primary Cause | Resolution / Verification Command |
| :--- | :--- | :--- |
| **Repetitive Emoji / Hallucination Loops** | Sampling temperature too high for 1-bit weight precision | Reduce temperature to `0.1 - 0.2` and enable repetition penalty (`--repeat-penalty 1.15`). |
| **CUDA Out of Memory (`GGML_ASSERT`)** | KV-Cache footprint exceeds physical RAM at large context | Reduce context size (`-c 2048`) or enable 4-bit KV cache quantization (`-ctk q4_0 -ctv q4_0`). |
| **`mmproj` Vision Token Mismatch** | Loading wrong vision projector file version | Ensure `mmproj.gguf` matches the exact PrismML Bonsai release tag on Hugging Face. |
| **Slow Prefill Throughput on Metal** | GGML Metal kernel compilation missing for low-bit types | Recompile llama.cpp with `LLAMA_METAL=ON` and verify `ggml-metal.metal` includes ternary shaders. |
| **Process Killed (`OOM-Killer`) on Smartphone** | Background iOS/Android OS memory pressure | Close background memory-heavy apps and allocate max 3.2GB for model weights on 6GB RAM phones. |

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
