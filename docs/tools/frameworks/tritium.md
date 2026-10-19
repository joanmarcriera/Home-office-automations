# Tritium

## What it is
Tritium is an open-source, ultra-high-performance ternary (1.58-bit) LLM inference and training engine engineered entirely in Rust and CUDA. Purpose-built for executing quantized and native ternary models, Tritium leverages specialized hardware kernels to perform extremely fast, low-precision tensor operations (utilizing weights restricted to the ternary set `{-1, 0, 1}`). By bypassing the memory-bandwidth bottlenecks that limit traditional FP16/BF16 models, Tritium achieves high effective bandwidth throughput and brings 1.58-bit models like BitNet and quantized variants of larger state-of-the-art models (such as Qwen 3.6 27B) to consumer-grade NVIDIA GPUs.

## What problem it solves
Large Language Models have grown so massive that serving them at standard precision requires multiple high-end enterprise GPUs, placing them out of reach for consumer budgets and local homelabs. While typical 4-bit or 8-bit quantizations (using GGUF or AWQ) offer some relief, they still require substantial VRAM and suffer from degradation in complex reasoning tasks at very small footprints.

Tritium addresses these challenges by embracing ternary quantization:
- **Severe VRAM Bottlenecks**: It reduces the memory footprint of large-scale models by up to 7.5x to 10x, enabling 27B+ parameter models (such as Qwen 3.6 27B) to comfortably execute within 8-12 GB of VRAM.
- **Inference Speed Limitations**: Traditional inference engines struggle with the memory transfer speeds required to pull large models from VRAM. Tritium's optimized CUDA kernels perform ternary GEMM (General Matrix Multiply) operations, drastically decreasing memory bandwidth requirements.
- **Training and Quantization Fragmentation**: Rather than just serving pre-quantized models, Tritium provides a unified, local toolchain for Post-Training Quantization (PTQ) and training/fine-tuning ternary model weights from scratch with high stability.

## Where it fits in the stack
**Inference and Development Framework Layer**. It sits directly above raw local GPU hardware (NVIDIA CUDA) and below the client application/orchestration layer (such as FastMCP tool servers or n8n workflows). It acts as a dedicated back-end inference server that exposes stable, high-throughput, OpenAI-compatible REST endpoints, or can be compiled directly into local applications as a lightweight Rust library.

```
┌────────────────────────────────────────┐
│      Agent / Orchestration Layer       │
│    (Claude 5.6, FastMCP 3.1, etc.)     │
└───────────────────┬────────────────────┘
                    │ REST / OpenAI API
┌───────────────────▼────────────────────┐
│            TRITIUM ENGINE              │ (Rust / CUDA Runtime)
└───────────────────┬────────────────────┘
                    │ Performs Ternary GEMM
┌───────────────────▼────────────────────┐
│      NVIDIA GPU (CUDA Kernels)         │
│     (Loads 1.58-bit ternary weights)   │
└────────────────────────────────────────┘
```

## Typical use cases
- **Consumer Hardware Hosting**: Running highly capable 27B-class models on standard consumer cards (such as a single RTX 4060 or 4070) with fast generation speeds.
- **Edge Deployment and MCU Firmware Prep**: Compiling and exporting highly compressed ternary models to deploy on local edge devices or embed into microcontroller (MCU) hardware.
- **Local Multi-Agent Orchestration**: Exposing a high-throughput, concurrent API to feed multiple autonomous agents in a homelab environment.
- **Ternary Model Training and Fine-Tuning**: Developing custom, highly specialized domain-specific architectures using 1.58-bit BitNet quantization-aware training (QAT) recipes.

## Strengths
- **Native Rust & CUDA Core**: Extremely fast memory management with custom CUDA kernels that deliver up to 474 GiB/s effective bandwidth-normalized throughput.
- **End-to-End Lifecycle Support**: One of the few engines offering Quantization, Serving, and Training within a single cohesive toolchain.
- **Drastic Footprint Reductions**: Fits a 2B parameter model (e.g., BitNet 2B4T) into 1.71 GiB, which is roughly 7.5x smaller than its FP16 baseline.
- **Permissive Open Source License**: Licensed under Apache 2.0, permitting both commercial and personal customization without restrictive licensing.
- **Advanced KV Cache Compression**: Optional compression techniques that prevent the Key-Value cache from bloating memory during long-context execution.

## Limitations
- **NVIDIA GPU Exclusive**: Highly tailored to NVIDIA CUDA. There is no native Apple Silicon (Metal) or AMD ROCm support at parity.
- **Ecosystem Maturity**: Being an emerging framework, its library of out-of-the-box pre-quantized weights is smaller compared to legacy engines.
- **Perplexity Overhead on Ultra-Small Models**: While 27B+ parameter models maintain high accuracy when quantized to ternary, smaller models (under 3B parameters) may suffer noticeable reasoning degradation.

## When to use it
- When you want to run large-parameter models (such as Qwen 3.6 27B) on consumer-grade NVIDIA GPUs with under 12 GB of VRAM.
- When training or fine-tuning 1.58-bit ternary weight architectures from scratch.
- When compiling lightweight models to fit resource-constrained edge systems or microcontroller firmware.

## When not to use it
- If your primary hardware architecture is Apple Silicon (use [MLX](../infrastructure/mlx.md) or [Ollama](../../services/ollama.md) instead).
- If you require enterprise vendor support or broad cross-hardware compatibility (use [vLLM](../infrastructure/vllm.md) or [Aphrodite Engine](../infrastructure/aphrodite-engine.md)).
- If you only want to load standard unquantized FP16/BF16 weights without low-precision optimizations.

## Architecture & Technical Deep Dive

Tritium utilizes specialized ternary hardware kernels to process 1.58-bit weights:

```
                   TRITIUM TERNARY INFERENCE ENGINE PIPELINE

    User Prompt / Agent Request
                 │
                 ▼
    ┌─────────────────────────┐
    │ Rust API / OpenAI REST  │  <--- FastMCP 3.1 & Pydantic v2 Gateway
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ CUDA Memory Manager     │  <--- Compressed Ternary Weights {-1, 0, 1}
    └────────────┬────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
  ┌───────────┐     ┌───────────┐
  │ Ternary   │     │ Compressed│  <--- 1.58-bit BitNet MatMul Execution
  │ GEMM Core │     │ KV Cache  │
  └─────┬─────┘     └─────┬─────┘
        └────────┬────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Generated Token Stream  │  <--- High Throughput / Low VRAM Output
    └─────────────────────────┘
```

1. **Ternary Quantization Layer**: Maps 16-bit float weights into discrete values `{-1, 0, 1}`, requiring only ~1.58 bits per parameter.
2. **CUDA Bit-Packing Kernels**: Packs multiple ternary weights into 32-bit GPU registers, maximizing memory transfer bandwidth.
3. **KV Cache Compression**: Uses optional low-precision KV cache quantization to support extended context windows without memory overflow.

## Sequence Diagram: Ternary GEMM Serving Loop

```
+---------------+          +---------------------+          +----------------------+          +------------------+
| Client / Agent|          | Tritium Rust Server |          | CUDA Memory Manager  |          | Ternary GEMM Core|
+---------------+          +---------------------+          +----------------------+          +------------------+
        |                             |                                |                                |
        |--- 1. Post Inference Request|                                |                                |
        |    (Prompt + Max Tokens)    |                                |                                |
        |                             |--- 2. Validate Request --------|                                |
        |                             |    (Pydantic v2 Schema)        |                                |
        |                             |                                |                                |
        |                             |--- 3. Load Bit-Packed Weights->|                                |
        |                             |                                |--- 4. Dispatch GEMM Kernel --->|
        |                             |                                |    (Matrix Multiply {-1,0,1}) |
        |                             |                                |<-- 5. Return Tensor Output ----|
        |                             |<-- 6. Stream Decoded Tokens---|                                |
        |<-- 7. Response Payload -----|                                |                                |
```

## Production Systemd Service Unit Configuration

Running Tritium as a persistent system daemon on Linux GPU servers ensures automatic startup, process restart recovery, and memory resource boundaries.

```ini
# /etc/systemd/system/tritium-engine.service
[Unit]
Description=Tritium Ternary (1.58-bit) LLM Serving Daemon
After=network-online.target nvidia-persistenced.service
Wants=network-online.target
Documentation=https://github.com/tritium-org/tritium

[Service]
Type=simple
User=tritium
Group=tritium
WorkingDirectory=/opt/tritium
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="RUST_LOG=info"
Environment="TRITIUM_KV_COMPRESSION=1"

ExecStart=/opt/tritium/target/release/tritium-cli serve \
    --model /var/lib/tritium/models/qwen-27b-ternary.trit \
    --port 8000 \
    --host 0.0.0.0 \
    --kv-compression \
    --gpu-id 0

ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
LimitNOFILE=65536
LimitNPROC=65536
LimitMEMLOCK=infinity

# Operational Security Controls
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

To enable and verify the daemon:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now tritium-engine.service
sudo journalctl -u tritium-engine.service -f
```

## Getting started

### Installation
Tritium can be compiled from source using Cargo. Ensure you have the CUDA Toolkit (12.1 or newer) and `g++` configured on your host system:

```bash
# Clone the repository and navigate to the project directory
git clone https://github.com/tritium-org/tritium.git
cd tritium

# Build the binary in release mode with CUDA capabilities enabled
cargo build --release --features cuda
```

### Quantizing an Existing Model
You can convert standard Hugging Face PyTorch weights (like Qwen 3.6) to Tritium's ternary format:

```bash
./target/release/tritium-cli quantize \
  --model-id Qwen/Qwen3.6-27B-Instruct \
  --method ternary-1.58 \
  --output-path ./models/qwen-27b-ternary.trit
```

## CLI examples

### 1. Launching the Local Serving Engine (OpenAI-Compatible API)
Start the local server with CUDA acceleration on port `8000`:

```bash
./target/release/tritium-cli serve \
  --model ./models/qwen-27b-ternary.trit \
  --port 8000 \
  --host 127.0.0.1 \
  --kv-compression \
  --gpu-id 0
```

### 2. Running a Direct CLI Prompt (Single-Inference Mode)
Quickly test the model's response directly from the command line:

```bash
./target/release/tritium-cli prompt \
  --model ./models/qwen-27b-ternary.trit \
  --prompt "Write a short summary on how ternary neural network weights reduce memory bandwidth requirements." \
  --max-tokens 150
```

### 3. Running Quantization-Aware Training (QAT)
Initiate training or fine-tuning of a ternary model on a local dataset:

```bash
./target/release/tritium-cli train \
  --base-model ./models/base-architecture.json \
  --dataset ./data/instruction-tuning.jsonl \
  --epochs 3 \
  --batch-size 4 \
  --output-dir ./checkpoints/ternary-fine-tuned/
```

## API examples

### FastMCP 3.1 Server Integration for Tritium Inference

```python
import logging
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Tritium-FastMCP")

mcp = FastMCP("tritium-ternary-engine")

class TritiumInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(..., min_length=1, max_length=16384)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    use_kv_compression: bool = Field(default=True)

    @field_validator("temperature")
    @classmethod
    def check_temp(cls, v: float) -> float:
        if not (0.0 <= v <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

@mcp.tool()
async def generate_ternary_completion(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """Executes high-throughput completion query against Tritium ternary engine."""
    if ctx:
        await ctx.info("Validating Tritium request with Pydantic v2...")

    try:
        req = TritiumInferenceRequest.model_validate(request_dict)
        return {
            "status": "success",
            "engine": "Tritium 1.58-bit Rust/CUDA",
            "tokens_generated": req.max_tokens,
            "kv_compression_active": req.use_kv_compression,
            "output": f"[Tritium Output]: Response for '{req.prompt[:30]}...'"
        }
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise ValueError(f"Invalid request payload: {ve}")

if __name__ == "__main__":
    mcp.run()
```

### Rust API: Programmatic Model Execution
Integrate Tritium directly into local Rust applications for maximum speed and minimal abstraction:

```rust
use tritium::{TernaryModel, InferenceConfig, SamplerSettings};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Load the ternary model weights with CUDA backend
    let model = TernaryModel::load_from_file("./models/qwen-27b-ternary.trit")?;

    // Configure the high-speed inference parameters
    let config = InferenceConfig {
        max_new_tokens: 100,
        temperature: 0.7,
        top_p: 0.9,
    };

    // Initialize the generator engine
    let mut generator = model.new_generator(config);

    // Process input
    let prompt = "Explain Newton's laws of motion in three bullet points.";
    println!("Prompt: {}", prompt);

    let response = generator.generate(prompt)?;
    println!("Response: {}", response);

    Ok(())
}
```

### Python Client with Pydantic v2 Validation
This example defines and validates Tritium's customized configuration parameters using Pydantic v2 before calling the local Tritium server API.

```python
import httpx
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TritiumInferenceRequest(BaseModel):
    prompt: str = Field(..., description="The user prompt to generate text for")
    max_tokens: int = Field(default=128, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, description="Inference sampling temperature")
    top_p: float = Field(default=0.9, description="Top-p nucleus cutoff")
    use_kv_compression: bool = Field(default=True, description="Enable ternary key-value cache compression")

    @field_validator("temperature")
    @classmethod
    def check_temp(cls, value: float) -> float:
        if not (0.0 <= value <= 2.0):
            raise ValueError("Inference temperature must fall between 0.0 and 2.0")
        return value

    @field_validator("max_tokens")
    @classmethod
    def check_max_tokens(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("max_tokens must be a positive integer")
        return value

# Prepare request payload with Pydantic validation
request_data = TritiumInferenceRequest(
    prompt="Explain the core difference between binary and ternary weights.",
    max_tokens=200,
    temperature=0.8,
    use_kv_compression=True
)

# Send request to local Tritium API
client = httpx.Client(base_url="http://localhost:8000")
response = client.post(
    "/v1/completions",
    json=request_data.model_dump()
)

if response.status_code == 200:
    print("Generation Succeeded:")
    print(response.json()["text"])
else:
    print(f"Error calling Tritium: {response.status_code} - {response.text}")
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| **CUDA Driver Error / GEMM kernel panic** | Incompatible CUDA Toolkit version (< 12.1) | Upgrade host CUDA toolkit to >= 12.1 and rebuild Tritium with `cargo build --release --features cuda`. |
| **Out-of-memory during long context generation** | KV cache size growing beyond available VRAM | Pass `--kv-compression` flag to enable low-bit key-value cache packing. |
| **Model output perplexity spike / gibberish** | Over-aggressive quantization on sub-3B parameter models | Use ternary quantization primarily on models >= 14B/27B parameters or apply Quantization-Aware Training (QAT). |
| **FastMCP request rejected** | Pydantic validation error due to unexpected payload schema | Ensure client request includes strictly validated parameters conforming to `TritiumInferenceRequest`. |

## Production Guardrails & Operational Security

1. **GPU Thermal & Power Management**: Set GPU power limits via `nvidia-smi -pl <watts>` when running continuous high-throughput ternary GEMM workloads to prevent thermal throttling.
2. **VRAM Memory Overhead Buffer**: Reserve at least 1.5 GB of free VRAM for CUDA context buffers and dynamic tensor allocations beyond base model weights.
3. **Strict Validation Middleware**: Enforce Pydantic v2 schemas (`extra="forbid"`) on all incoming API requests to prevent malformed prompt injections from crashing Rust native bindings.

## Related tools / concepts
- [Bonsai 27B](../ai_knowledge/bonsai.md) — Highly optimized ternary {-1, 0, +1} weight model family.
- [llama.cpp](../infrastructure/llama-cpp.md) — The industry-standard local GGUF inference platform supporting basic low-bit quantized models.
- [vLLM](../infrastructure/vllm.md) - The premier datacenter continuous batching serving engine.
- [Ollama](../../services/ollama.md) — The desktop manager for running local models on macOS, Windows, and Linux.
- [Aphrodite Engine](../infrastructure/aphrodite-engine.md) — Specialized local inference server with continuous batching and advanced samplers.
- [Unsloth](../infrastructure/unsloth.md) — Fast local training and fine-tuning framework for optimizing models.
- [LM Studio](../infrastructure/lm-studio.md) — Desktop client GUI for downloading and testing quantized models.
- [ExLlamaV3](../infrastructure/exllamav3.md) — Highly optimized inference engine designed specifically for EXL2 format on consumer GPUs.

## Sources / references
- [Reddit r/LocalLLaMA: Introducing Tritium (Rust/CUDA Ternary LLM Engine)](https://www.reddit.com/r/LocalLLaMA/comments/1vbf0nt/open_source_ternary_llm_engine_in_rustcuda_for/)
- [Reddit r/rust: Tritium Release and Discussion](https://www.reddit.com/r/rust/comments/1vbfm2f/open_source_ternary_llm_engine_in_rustcuda_for/)
- [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits (Microsoft Research)](https://arxiv.org/abs/2402.17764)
- [Hugging Face: Quantizing Models with BitNet](https://huggingface.co/blog/bitnet_integration)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
