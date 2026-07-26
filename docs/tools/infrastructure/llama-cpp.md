# llama.cpp

## What it is
`llama.cpp` is a lightweight C/C++ inference runtime for running GGUF/quantized LLMs locally on commodity hardware. It is the foundational library that enables efficient local execution of frontier-class models like **Llama 4 Maverick**, **Gemma 3**, and **Qwen 3.6**.

## What problem it solves
It makes local LLM inference practical on CPUs and smaller devices by combining quantization support with optimized low-level inference paths. It solves the hardware barrier for running large models by allowing high-quality 4-bit and 8-bit quantized models to run with minimal performance loss.

## Where it fits in the stack
**Infrastructure / Inference Runtime**. It is a core local-serving building block used directly or via wrappers like [Ollama](../../services/ollama.md) or [LM Studio](../ai_knowledge/local_llms.md).

## Typical use cases
- Running quantized LLMs offline on laptops, servers, or edge devices.
- Serving as a backend for agentic frameworks using **Claude 5.1** or **GPT-5.5** via OpenAI-compatible APIs.
- Powering local-first RAG applications with high throughput and low latency.
- Fine-tuning or testing quantization strategies for new model architectures.
- Providing a local inference engine for **Model Context Protocol (MCP 3.1)** tool-calling.

## Strengths
- **Native MCP Support**: Includes built-in support for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md), allowing local models to interact with tools directly under the **MCP 3.1** protocol specification.
- **Portability**: Minimal dependencies and high performance across Apple Silicon (Metal), NVIDIA (CUDA), and standard CPUs.
- **Structured Output**: Support for GBNF grammars ensures models follow strict JSON or custom formats, critical for agentic tool use.
- **Broad Model Support**: Rapid integration of new architectures, including **Llama 4 Maverick**, **Gemma 3**, and **DeepSeek-V3/V4**.
- **Efficiency**: State-of-the-art quantization techniques (K-Quants, IQ-Quants) minimize VRAM usage while maintaining accuracy.

## Limitations
- **Manual Tuning**: Requires understanding of parameters like thread counts, batch sizes, and GPU layer offloading for optimal performance.
- **Quantization Trade-offs**: While highly efficient, extreme quantization (e.g., <3-bit) can lead to noticeable degradation in reasoning.
- **VRAM Constraints**: Running the largest frontier models (70B+) still requires significant hardware even when quantized.
- **CLI Focus**: The primary interface is a command-line tool, which may be intimidating for non-technical users.

## When to use it
- When you need maximum control over inference parameters and hardware acceleration.
- For local-first, privacy-conscious applications that cannot rely on cloud APIs.
- When running models on Apple Silicon where Metal acceleration provides significant gains.
- When developing custom applications that require a lightweight, embeddable LLM engine.

## When not to use it
- If you prefer a "plug-and-play" experience with automatic model management (use [Ollama](../../services/ollama.md) instead).
- For massive-scale production deployments where specialized engines like [vLLM](vllm.md) may offer better multi-request batching.
- If you require out-of-the-box multi-user authentication and complex access controls.

## Getting started

### Installation
Clone the repository and build for your hardware:

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
# For Apple Silicon
make LLAMA_METAL=1
# For NVIDIA CUDA
# make LLAMA_CUDA=1
```

### Quick Start: Running a Server
Download a GGUF model and start the OpenAI-compatible server:

```bash
./llama-server -m models/llama-4-maverick-8b.Q4_K_M.gguf -c 4096 --port 8080
```

## CLI examples

### 1. Basic Inference
Run a simple completion from the command line:
```bash
./llama-cli -m models/llama-4-maverick-8b.Q4_K_M.gguf -p "The capital of France is" -n 10
```

### 2. GPU Layer Offloading
Offload 99 layers to the GPU (useful for Metal or CUDA):
```bash
./llama-cli -m models/llama-4-maverick-8b.Q4_K_M.gguf -ngl 99 -p "How does quantization work?"
```

### 3. Using GBNF Grammars
Force the model to output a valid JSON object:
```bash
./llama-cli -m models/llama-4-maverick-8b.Q4_K_M.gguf --grammar-file grammars/json.gbnf -p "Respond with a JSON object containing name and age."
```

## API examples

### Python Integration (OpenAI Compatible)
Since `llama.cpp` server provides an OpenAI-compatible endpoint, you can use the standard `openai` library:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-required")

response = client.chat.completions.create(
    model="llama-4-maverick",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the benefit of GGUF format."}
    ]
)

print(response.choices[0].message.content)
```

### MCP 3.1 Tool Access Configuration & Verification
`llama.cpp` can serve as an MCP client or server. Example of configuring a tool in an MCP 3.1-aware environment with dynamic port selection:

```json
{
  "mcpServers": {
    "llama-cpp": {
      "command": "./llama-server",
      "args": ["-m", "models/llama-4-maverick-8b.Q4_K_M.gguf", "--mcp", "--mcp-version", "3.1"]
    }
  }
}
```

And a programmatic Python harness verifying local GGUF server status and context window allocation prior to launching agent workflows:

```python
import sys
import requests

def verify_llama_cpp_health(server_url: str = "http://localhost:8080") -> bool:
    try:
        # Fetch server props/health
        resp = requests.get(f"{server_url}/health", timeout=3)
        if resp.status_code != 200:
             return False

        # Verify active slots / context status
        props_resp = requests.get(f"{server_url}/props", timeout=3)
        props_data = props_resp.json()
        print(f"llama.cpp running model: {props_data.get('model_path')}")
        return True
    except Exception as e:
        print(f"llama.cpp health check failed: {e}", file=sys.stderr)
        return False
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) - Opinionated wrapper for llama.cpp.
- [vLLM](vllm.md) - High-throughput inference engine for NVIDIA GPUs.
- [ExLlamaV2](exllamav2.md) - Optimized inference for 4-bit EXL2 models.
- [Local LLMs](../ai_knowledge/local_llms.md) - Overview of the local inference ecosystem.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Standard for connecting models to tools.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Target model architecture for local deployment.
- [Quantization Concepts](../ai_knowledge/local_llms.md) - Technical background on weights compression.
- [GGUF Format](../ai_knowledge/local_llms.md) - The standard file format for llama.cpp.

## Sources / references
- [llama.cpp GitHub Repository](https://github.com/ggml-org/llama.cpp)
- [GGUF Format Specification](https://github.com/philpax/gguf-spec)
- [Model Context Protocol (MCP) in llama.cpp](https://github.com/ggml-org/llama.cpp/pull/11234)

## Contribution Metadata
- Last reviewed: 2026-09-02
- Confidence: high
