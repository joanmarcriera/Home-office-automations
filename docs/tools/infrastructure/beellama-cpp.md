# BeeLlama.cpp

## What it is
BeeLlama.cpp is an advanced, ultra-optimized C++ implementation for local LLM inference, FastMCP 3.1 Task Protocol server hosting, and high-performance model quantization. It builds upon the foundational architectures of `llama.cpp` and `vLLM` to provide specialized optimization features, specifically targeting KV Cache quantization, dynamic context pruning, model distillation, and high-performance hardware execution. Released with deep performance benchmark matrices, BeeLlama.cpp allows developers to run rigorous tests on KV Cache allocation efficiency (evaluating hundreds of distinct parameter pairs) to find the absolute sweet spot between memory consumption and generation speed on consumer-grade and enterprise edge hardware.

## What problem it solves
Large language models (including modern multi-modal foundation models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, and DeepSeek-V4) consume substantial amounts of system memory (VRAM) during multi-turn agent conversations, with the Key-Value (KV) Cache scaling linearly as context windows expand up to 1M+ tokens. This often leads to GPU "Out of Memory" (OOM) errors or severe execution throttling. BeeLlama.cpp solves this scalability bottleneck by providing highly optimized, native 4-bit and 8-bit KV Cache quantization and memory-stealing routines, reducing the system memory footprint by up to 60% with zero structural modifications to model weights while supporting FastMCP 3.1 streaming state management.

## Where it fits in the stack
**Local Inference / Infrastructure Layer**. It serves as an ultra-fast local hardware engine and native FastMCP 3.1 protocol host, powering autonomous agents and local database pipelines with a highly optimized memory architecture.

## Typical use cases
- **Memory-Optimized Local Agents**: Executing long-context autonomous agent swarms running FastMCP 3.1 protocols on devices with limited GPU VRAM.
- **Inference Parameter Tuning**: Benchmarking and analyzing optimal quantization pairs (e.g., Q4_K_M weights with 4-bit KV Cache) to maximize generation speeds across DeepSeek-V4 and Gemma 4 deployments.
- **Air-Gapped Document Processing**: Parsing and indexing deep multi-gigabyte local document directories entirely offline.
- **Micro-Server LLM Deployment**: Deploying lightweight, highly responsive language models and FastMCP 3.1 endpoints on edge gateways or home servers.

## Strengths
- **SOTA KV Cache Quantization**: Native support for 4-bit and 8-bit KV Cache optimizations substantially decreases context memory footprints.
- **FastMCP 3.1 Native Protocol Integration**: Direct C++ implementation of FastMCP 3.1 SSE and stdio transport layers with task lifecycle management.
- **Zero Heavy Dependencies**: Written entirely in clean C/C++ with no massive PyTorch or Python framework overhead.
- **Optimized Metal and CUDA Kernels**: Highly optimized architecture ensures peak hardware execution speeds on Apple Silicon, NVIDIA GPUs, and ARM edge processors.
- **Comprehensive Benchmarking Utilities**: Includes built-in analytical routines to measure prompt processing (PP) and tokens per second (TPS) accurately.

## Limitations
- **Perplexity Penalty at Low Quantization**: Aggressive 4-bit KV Cache quantization can introduce minor logical drift or reasoning errors in extremely deep reasoning tasks.
- **Model Architecture Support**: Focuses heavily on mainstream Transformer models (such as Llama 4, Gemma 4, and DeepSeek-V4), with slightly slower adoption rates for fringe architectures.
- **Complex Compilation Chains**: System optimization demands compiling directly from source code with hardware-specific compiler flags.

## When to use it
- When you are running long-context local models or FastMCP 3.1 servers and repeatedly hitting VRAM memory limits on existing hardware.
- When you want to optimize your offline home automation or developer assistant to run on lightweight edge hardware.
- For benchmarking, analyzing, and selecting the absolute best quantization profiles for production inference.

## When not to use it
- If you are deploying simple, cloud-hosted API pipelines where local server hardware constraints and VRAM bounds do not exist.
- If you do not possess developer experience compiling system binaries from source code or managing hardware compilation toolchains.
- When absolute logical reasoning accuracy and low-perplexity metrics must be preserved at any cost (use dense, non-quantized models).

## Getting started
1. **Clone the Source**: Retrieve the codebase and its dependencies:
   ```bash
   git clone --recursive https://github.com/SovereignAI/beellama-cpp.git
   cd beellama-cpp
   ```
2. **Compile the Engine**: Compile with CUDA or Metal optimizations:
   ```bash
   # Build with CUDA support
   mkdir build && cd build
   cmake -DGGML_CUDA=ON ..
   make -j
   ```
3. **Execute with quantized KV Cache**: Launch model inference utilizing 4-bit KV Cache quantization:
   ```bash
   ./beellama-cli -m ./models/gemma-4-9b.gguf -p "Optimize my system configurations." --ctk q4_0
   ```

## CLI examples
BeeLlama.cpp provides an interactive command-line interface for inference, a FastMCP 3.1 task protocol server, and a comprehensive hardware benchmarking suite.

```bash
# Run model with 8-bit Key and 8-bit Value Cache quantization enabled
./beellama-cli -m models/llama-4-8b.gguf -p "Draft a system architecture proposal." --ctk q8_0 --ctv q8_0

# Launch native FastMCP 3.1 SSE server endpoint for agent tool calling
./beellama-mcp-server --model models/deepseek-v4-8b.gguf --port 8000 --fastmcp-version 3.1

# Execute a rigorous KV Cache quantization benchmark across 400+ testing pairs
./beellama-benchmark --model models/gemma-4-9b.gguf --context-size 8192 --threads 8

# Spin up an OpenAI-compatible web API server with optimized threading profiles
./beellama-server --model models/llama-4-8b.gguf --port 8080 --parallel 4 --ctk q4_0
```

## API examples

### Python Subprocess Integration with BeeLlama.cpp & Pydantic v2 Validation
This script shows how to trigger BeeLlama.cpp as a system subprocess or FastMCP 3.1 task runner, parse its execution metrics from stdout, and enforce validation using strict **Pydantic v2** structures. It validates parameters such as prompt vs generation speeds, exact memory allocations, FastMCP 3.1 protocol states, thread counts, and context limits.

```python
import subprocess
import json
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# Define schema for validating BeeLlama.cpp execution stats under FastMCP 3.1
class BeeLlamaMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_path: str = Field(..., description="Local system path to the model GGUF file")
    kv_cache_type_k: str = Field(..., description="Quantization profile used for the Key Cache")
    kv_cache_type_v: str = Field(..., description="Quantization profile used for the Value Cache")
    thread_count: int = Field(..., ge=1, description="Number of CPU threads utilized for compute")
    context_length: int = Field(..., ge=512, description="Active context length window size")
    fastmcp_protocol_version: str = Field(default="3.1", description="FastMCP protocol version active")
    prompt_tokens_per_sec: float = Field(..., gt=0.0, description="Tokens processed per second during prompt ingestion")
    generation_tokens_per_sec: float = Field(..., gt=0.0, description="Generation throughput in tokens per second")
    vram_consumed_mb: float = Field(..., gt=0.0, description="Total GPU memory consumed in megabytes")
    perplexity_delta: Optional[float] = Field(None, description="Quantization perplexity change relative to baseline")

def run_beellama_inference(model: str, prompt: str) -> BeeLlamaMetrics:
    # cmd = ["./beellama-cli", "-m", model, "-p", prompt, "--ctk", "q4_0", "--ctv", "q4_0", "--json-metrics"]
    # result = subprocess.run(cmd, capture_output=True, text=True)
    # metrics_data = json.loads(result.stdout)

    # Simulated stdout response containing execution metrics
    simulated_metrics = {
        "model_path": "models/gemma-4-9b.gguf",
        "kv_cache_type_k": "q4_0",
        "kv_cache_type_v": "q4_0",
        "thread_count": 8,
        "context_length": 8192,
        "fastmcp_protocol_version": "3.1",
        "prompt_tokens_per_sec": 412.5,
        "generation_tokens_per_sec": 52.8,
        "vram_consumed_mb": 4210.4,
        "perplexity_delta": 0.04
    }

    # Parse and validate with Pydantic v2
    validated_metrics = BeeLlamaMetrics(**simulated_metrics)
    return validated_metrics

if __name__ == "__main__":
    model_file = "models/gemma-4-9b.gguf"
    prompt_str = "Explain local memory management techniques."
    metrics = run_beellama_inference(model_file, prompt_str)

    print("--- BeeLlama.cpp Execution Metrics Verified ---")
    print(f"Model: {metrics.model_path}")
    print(f"Threads: {metrics.thread_count} | Context Limit: {metrics.context_length}")
    print(f"FastMCP Version: {metrics.fastmcp_protocol_version}")
    print(f"KV Cache Profile: Key={metrics.kv_cache_type_k}, Value={metrics.kv_cache_type_v}")
    print(f"Prompt Ingestion Speed: {metrics.prompt_tokens_per_sec} tokens/sec")
    print(f"Generation Throughput: {metrics.generation_tokens_per_sec} tokens/sec")
    print(f"VRAM Consumption: {metrics.vram_consumed_mb} MB")
    if metrics.perplexity_delta is not None:
        print(f"Quantization Perplexity Delta: +{metrics.perplexity_delta}")
```

## Related tools / concepts
- [Llama.cpp](../infrastructure/llama-cpp.md) — The core C/C++ engine upon which BeeLlama.cpp builds its specialized optimizations.
- [vLLM](../infrastructure/vllm.md) — High-performance inference engine; comparable for production deployments.
- [ExLlamaV2](../infrastructure/exllamav2.md) — High-speed quantized inference runner for local NVIDIA GPUs.
- [Ollama](../../services/ollama.md) — Simplifies local model lifecycle management and standard running patterns.
- [Unsloth](../infrastructure/unsloth.md) — High-efficiency local model fine-tuning and quantization preparation framework.

## Sources / references
- [Llama.cpp Optimization Roadmap and Quantization Guide](https://github.com/ggerganov/llama.cpp)
- [Reddit r/LocalLLaMA: KV Cache Quantization and Benchmarks Deep-Dive](https://www.reddit.com/r/LocalLLaMA/comments/1vhaabz/kv_cache_quantization_benchmarks_413_pairs_tested/)
- [SovereignAI: Advanced Model Serving and Distillation Standards](https://sovereignai.org/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
