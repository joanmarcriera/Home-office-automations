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

### 1. Rust API: Programmatic Model Execution
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

### 2. Python Client with Pydantic v2 Validation
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

### 3. cURL: Request with Native Sampler Adjustments
Send a high-throughput completion query directly to the running HTTP endpoint:

```bash
curl http://127.0.0.1:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Compare ternary (1.58b) weights with traditional 4-bit integer quantization.",
    "max_tokens": 256,
    "temperature": 0.5,
    "top_p": 0.85
  }'
```

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
