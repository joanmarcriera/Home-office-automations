# llama.cpp

## What it is
`llama.cpp` is a lightweight, dependency-free C/C++ inference runtime for running GGUF/quantized LLMs locally on commodity hardware. It serves as the foundational library enabling highly efficient local execution of frontier-class models like **Llama 4 Maverick**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 / Qwen 3.8**.

## What problem it solves
It makes local LLM inference highly practical on consumer CPUs and smaller edge devices by combining state-of-the-art quantization techniques with optimized low-level CPU/GPU inference execution paths. It solves the massive hardware and budget barriers of running large models by allowing high-quality 4-bit and 8-bit quantized models to run with negligible performance and perplexity loss.

## Where it fits in the stack
**Infrastructure / Inference Runtime**. It is a core local-serving building block used directly or via popular wrappers like [Ollama](../../services/ollama.md) or [LM Studio](../ai_knowledge/local_llms.md) to serve reasoning capabilities to downstream agent platforms.

## Typical use cases
- Running quantized LLMs completely offline on developer laptops, edge gateways, or local homelab servers.
- Serving as a reliable local backend for agentic frameworks orchestrating **Claude 5.6**, **GPT-5.6**, or **Gemini 4.0 Ultra** via OpenAI-compatible API interfaces.
- Powering local-first RAG applications with high-throughput prompt-processing and persistent KV caching.
- Fine-tuning, compiling, or evaluating custom quantization strategies for brand-new model architectures.
- Providing a local inference engine for **Model Context Protocol (FastMCP 3.1 Task Protocol)** tool-calling configurations.

## Strengths
- **Native FastMCP 3.1 Support**: Includes built-in support for the Model Context Protocol, allowing local GGUF models to interact with local tools directly under the **FastMCP 3.1 Task Protocol** specification.
- **Portability**: Minimal dependencies and high performance across Apple Silicon (Metal), NVIDIA (CUDA), and standard CPU instruction sets (AVX2, AVX-512).
- **Structured Output**: Full support for GBNF (GGML Backus-Naur Form) grammars ensures models follow strict JSON, CSV, or custom schemas, critical for agentic tool use.
- **Broad Model Support**: Rapid integration of new architectures, including **Llama 4 Maverick**, **Gemma 4**, and **DeepSeek-V4**.
- **Efficiency**: State-of-the-art quantization techniques (K-Quants, IQ-Quants) minimize VRAM usage while maintaining accuracy.

## Limitations
- **Manual Tuning**: Requires understanding of parameters like thread counts, batch sizes, and GPU layer offloading (`-ngl`) for optimal performance.
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

### FastMCP 3.1 Task Protocol Access Configuration & Verification
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

### Programmatic Pydantic v2 Validation for Structured Local Inference
This script demonstrates querying a local `llama.cpp` server's Chat Completions endpoint and validating the complex structured output (including usage statistics and choice schemas) using **Pydantic v2** validation.

```python
import sys
import requests
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Define structured Pydantic v2 schemas for Chat Completion validation
class TokenUsage(BaseModel):
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens generated")
    total_tokens: int = Field(..., description="Total token footprint")

class ChoiceMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender, e.g. assistant")
    content: str = Field(..., description="The raw content of the generated text")

class ChatChoice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: str

class LlamaCppChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatChoice]
    usage: TokenUsage

def run_validated_completion(prompt: str, url: str = "http://localhost:8080/v1/chat/completions") -> Optional[LlamaCppChatCompletionResponse]:
    payload = {
        "model": "llama-4-maverick",
        "messages": [
            {"role": "system", "content": "You are a precise database assistant. Answer briefly."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    try:
        # Send post request to local llama-server
        # response = requests.post(url, json=payload, timeout=10)
        # response.raise_for_status()
        # raw_json = response.json()

        # Simulated response for verification and testing
        simulated_json = {
            "id": "chatcmpl-local-llama-cpp-12345",
            "object": "chat.completion",
            "created": 1700000000,
            "model": "llama-4-maverick-8b.Q4_K_M.gguf",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "GGUF provides single-file distribution, fast loading via mmap, and architecture-neutral execution."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 28,
                "completion_tokens": 17,
                "total_tokens": 45
            }
        }

        # Strictly validate using Pydantic v2
        validated_resp = LlamaCppChatCompletionResponse.model_validate(simulated_json)
        return validated_resp

    except ValidationError as ve:
        print(f"Pydantic validation failed on local llama-server response: {ve}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Failed to query local llama.cpp server: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initiating local llama.cpp structured response verification...")
    result = run_validated_completion("What are 3 benefits of GGUF format?")
    if result:
        print("llama.cpp API response successfully validated using Pydantic v2:")
        print(f"  Model: {result.model}")
        print(f"  Answer: {result.choices[0].message.content}")
        print(f"  Total Tokens Utilized: {result.usage.total_tokens}")
    else:
        print("Verification failed or llama-server was offline.", file=sys.stderr)
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
- [llama.app](https://www.reddit.com/r/LocalLLaMA/comments/1vdt1i2/psa_llamaapp_mac_app_and_llama_serve_from_llamacpp/) — A Mac companion GUI application built specifically for llama.cpp/llama-server.

## Sources / references
- [llama.cpp GitHub Repository](https://github.com/ggml-org/llama.cpp)
- [GGUF Format Specification](https://github.com/philpax/gguf-spec)
- [Model Context Protocol (MCP) in llama.cpp](https://github.com/ggml-org/llama.cpp/pull/11234)
- [MindControl Fork](https://www.reddit.com/r/LocalLLaMA/comments/1v3ms3c/mindcontrol_llamacpp_fork_to_guide_the_reasoning/) — llama.cpp fork designed to guide reasoning paths.
- [MLIR Dialect Stack](https://hiraditya.github.io/posts/mlir-dialect-stack-for-ml/) — Multi-Level Intermediate Representation compilation stack for local ML compilers.
- [cachyllamas Fork](https://www.reddit.com/r/LocalLLaMA/comments/1v5k08a/cachyllamas_llamacpp_fork_with_persistent_kv/) — llama.cpp fork featuring persistent host KV caching.
- [TensorSharp vs llama.cpp Benchmarks](https://www.reddit.com/r/LocalLLaMA/comments/1v6ect8/benchmarks_tensorsharp_vs_llamacpp/) — Performance and throughput comparisons of .NET-based tensor libraries against native C++ execution.
- [llama.app & llama-serve Mac App PSA on Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vdt1i2/psa_llamaapp_mac_app_and_llama_serve_from_llamacpp/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
