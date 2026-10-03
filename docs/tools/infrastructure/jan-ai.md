# Jan.ai

## What it is
Jan.ai is a privacy-first, open-source alternative to ChatGPT and cloud AI portals that runs 100% offline on local consumer and enterprise workstations. Built on top of the **Nitro Engine**—a high-performance C++ inference execution layer written in C++/C and leveraging `llama.cpp` runtimes—Jan provides a desktop workspace and server interface. As of early 2027, Jan has evolved to version **v1.8+**, featuring native support for the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** servers, allowing local models like **Gemma 4**, **Llama 4**, **Qwen 3.6 VL**, **DeepSeek-R1**, and **Mistral Nemo** to operate as autonomous, privacy-preserving agent tool-orchestrators directly on macOS, Linux, and Windows hardware.

## What problem it solves
Cloud-hosted LLM services present severe data privacy, compliance, and cost challenges for developers, enterprises, and research organizations handling sensitive source code, confidential customer records, or intellectual property. Furthermore, local model execution engines often suffer from complex setup procedures, fragmenting GPU acceleration libraries across Apple Silicon Metal, NVIDIA CUDA/TensorRT, and AMD ROCm. Jan.ai solves these problems by providing an all-in-one desktop application and headless server engine that automates local model downloading (from Hugging Face and ModelScope), hardware acceleration detection, context window capping, and FastMCP 3.1 tool orchestration—ensuring zero data leakage and offline availability.

## Where it fits in the stack
**Infrastructure / Local Inference Engine / Offline Agent Client**. Jan.ai operates as the local inference and execution runtime. It sits between user desktop workflows or local network client applications and underlying hardware accelerators (GPUs, NPUs, CPUs). It provides an OpenAI-compatible REST API on port `1337` while connecting directly to local FastMCP 3.1 tool servers to perform autonomous action execution.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Jan Desktop Application UI                         │
│               (Privacy-First Chat / Agent Thread Workspace)                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Local REST API / Thread Events
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    Jan Core App / Local HTTP Server                         │
│                    (OpenAI-Compatible API on :1337)                         │
└──────────────┬──────────────────────────────────────────────┬───────────────┘
               │                                              │
               │ Hardware Inference Requests                  │ FastMCP 3.1 Protocol
┌──────────────▼──────────────┐                ┌──────────────▼───────────────┐
│     Nitro C++ Engine        │                │   FastMCP 3.1 Tool Servers    │
│  (llama.cpp C++ Backend)    │                │  (Local Files, SQLite, CLI)  │
└──────────────┬──────────────┘                └──────────────────────────────┘
               │
 ┌─────────────┼──────────────────────────────┐
 │             │ Hardware Execution Layer     │
 ▼             ▼                              ▼
Metal       CUDA / ROCm                  AVX-512 CPU
(Apple M-Series) (NVIDIA / AMD GPUs)     (Fallback CPU)
```

## Typical use cases
- **Air-Gapped Sovereign AI Workstations**: Running secure document processing, code analysis, and agent thread execution in air-gapped environments without external internet connectivity.
- **Hardware-Accelerated Local Inference**: Utilizing Apple Silicon Metal (M3/M4/M5/M6), NVIDIA CUDA (Hopper/Blackwell/RTX), or AMD ROCm/HIP on Linux to run 8B to 70B parameter quantized models (GGUF, EXL2) at high token-per-second rates.
- **Local OpenAI-Compatible API Gateway**: Serving local models to developer applications, coding assistants (Continue.dev, VS Code extensions), or internal web portals via standard OpenAI-format REST API endpoints.
- **Offline FastMCP 3.1 Tool Orchestration**: Connecting local GGUF models (Gemma 4, Llama 4) to local MCP tool servers to run autonomous database queries, local filesystem edits, and task scripts safely.

## Strengths
- **100% Offline & Private**: Zero telemetries, cloud dependencies, or tracking; models run entirely on local host hardware.
- **Nitro Engine Performance**: C++ core execution layer built on `llama.cpp` ensures fast time-to-first-token (TTFT) and high memory bandwidth utilization.
- **Cross-Platform Hardware Acceleration**: Native compiled backends for Apple Silicon Metal, NVIDIA CUDA (v12+), AMD ROCm/HIP, and CPU SIMD (AVX-512, ARM Neon).
- **FastMCP 3.1 Protocol Native**: Integrated tool discovery and task execution protocols enable local models to invoke external tools safely.
- **User-Friendly Model Hub**: Single-click downloads, GGUF quantization selection, context window auto-tuning, and thread management.

## Limitations
- **Hardware Dependent**: Inference throughput and maximum context length are strictly bounded by available host system VRAM and unified memory.
- **GUI Desktop Overhead**: While a headless CLI (`jan serve`) is included, the primary experience includes an Electron/Tauri desktop GUI wrapper.
- **Quantization Precision Loss**: Running 4-bit or 5-bit GGUF models on consumer GPUs may exhibit slight reasoning degradation compared to full 16-bit float cloud models.

## When to use it
- When strict compliance, HIPAA, GDPR, or corporate secrecy policies forbid sending data to external cloud LLM APIs.
- When configuring local developer machines or homelabs for offline model evaluation and FastMCP 3.1 agent testing.
- When running desktop environments on AMD GPUs under Linux where ROCm support is required out-of-the-box.
- When a simple OpenAI-compatible API on `localhost:1337` is required for local code assistants.

## When not to use it
- For ultra-large-scale multi-user cloud serving requiring dynamic batching across dozens of GPU nodes (use [vLLM](../infrastructure/vllm.md) or [TGI](tgi.md) instead).
- When operating in constrained microcontrollers or minimal CLI-only containers where lightweight binaries like `ollama` or raw `llama.cpp` binaries fit better.

## Getting started

To set up Jan.ai on your local system:

1. **Download & Install**:
   Download the installer for macOS, Windows, or Linux from the official portal ([jan.ai](https://jan.ai/)).

2. **Launch & Hardware Detection**:
   Open Jan; the Nitro engine automatically scans available GPUs (NVIDIA CUDA, Apple Metal, AMD ROCm) and allocates VRAM layers.

3. **Download Model from Hub**:
   In the "Hub" tab, search for **Gemma 4**, **Llama 4**, or **Qwen 3.6** and select a quantization profile matching your system VRAM:
   - 8B models (Q4_K_M): ~6 GB VRAM required.
   - 14B models (Q4_K_M): ~10 GB VRAM required.
   - 32B/70B models: Requires 24GB+ VRAM or unified memory.

4. **Start Local Server or Chat**:
   Interact directly in the chat UI or enable the API server under Settings -> Local Server (`http://localhost:1337`).

## CLI examples

Jan includes the `jan` CLI binary for headless execution, model serving, and thread management:

```bash
# Start the Jan headless API server on port 1337
jan serve --model gemma-4-27b --port 1337 --threads 8

# Inspect system GPU capability and Nitro Engine status
jan doctor

# List all locally installed GGUF models in Jan store
jan models list

# Download a model from Hugging Face directly into Jan
jan models pull hf:lmstudio-community/gemma-4-27b-it-GGUF

# Invoke one-off chat completion from terminal
jan chat --model gemma-4-27b --prompt "Explain FastMCP 3.1 server setup on Nitro engine."
```

## API examples

### Python: Interacting with Jan Local Server using Async OpenAI Client & Pydantic v2
Jan exposes an OpenAI-compatible REST API on `http://localhost:1337/v1`. Below is an asynchronous Python snippet demonstrating strict **Pydantic v2** model validation for inference configurations and structured outputs:

```python
import asyncio
import os
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ValidationError
import openai

# 1. Pydantic v2 configuration and payload validation schemas
class JanInferenceParams(BaseModel):
    model_name: str = Field(default="gemma-4-27b", alias="model")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, gt=0)
    stream: bool = Field(default=False)
    mcp_enabled: bool = Field(default=True, alias="mcpEnabled")

class ChatChoiceMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatChoiceMessage
    finish_reason: Optional[str] = None

class JanUsageReport(BaseModel):
    prompt_tokens: int = Field(..., alias="prompt_tokens")
    completion_tokens: int = Field(..., alias="completion_tokens")
    total_tokens: int = Field(..., alias="total_tokens")

class JanChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[JanUsageReport] = None

# 2. Async execution driver contacting Jan local port 1337
async def generate_jan_completion(prompt: str, params: JanInferenceParams) -> JanChatCompletionResponse:
    # Connect to Jan local server port 1337
    client = openai.AsyncOpenAI(
        base_url="http://localhost:1337/v1",
        api_key="jan-local-key" # Placeholder key accepted by local Jan engine
    )

    response = await client.chat.completions.create(
        model=params.model_name,
        messages=[
            {"role": "system", "content": "You are a private local software assistant running inside Jan.ai."},
            {"role": "user", "content": prompt}
        ],
        temperature=params.temperature,
        top_p=params.top_p,
        max_tokens=params.max_tokens,
        stream=params.stream
    )

    # 3. Validate raw JSON output via Pydantic v2 model_validate
    raw_dict = response.model_dump()
    validated_response = JanChatCompletionResponse.model_validate(raw_dict)
    return validated_response

# 4. Main runner
async def main():
    config = JanInferenceParams(model="gemma-4-27b", temperature=0.1)
    prompt_query = "What are the core performance advantages of the C++ Nitro engine in Jan.ai?"

    try:
        res = await generate_jan_completion(prompt_query, config)
        print(f"Jan Inference Successful [Model: {res.model}]")
        print(f"Response: {res.choices[0].message.content}")
        if res.usage:
            print(f"Token Breakdown - Prompt: {res.usage.prompt_tokens}, Completion: {res.usage.completion_tokens}")
    except Exception as e:
        print(f"Jan Local Inference Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### FastMCP 3.1 Local Tool Server Binding for Jan Agent Execution
Setting up a Python FastMCP 3.1 server that Jan can connect to locally for task execution:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp_server = FastMCP(
    name="Jan-Local-System-Tools",
    version="3.1.0"
)

class FileReadParams(BaseModel):
    filepath: str = Field(..., description="Path to local file to inspect")
    max_bytes: int = Field(default=4096, description="Maximum bytes to read")

@mcp_server.tool(name="read_local_log", description="Reads system log files securely for Jan agent thread analysis")
def read_local_log(params: FileReadParams) -> dict:
    try:
        with open(params.filepath, "r", encoding="utf-8") as f:
            data = f.read(params.max_bytes)
        return {"status": "success", "content": data, "bytes_read": len(data)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp_server.run(transport="sse", host="127.0.0.1", port=8000)
```

## Comparative Matrix: Jan.ai vs Alternative Local Inference Environments

| Capability / Feature | Jan.ai (v1.8+) | Ollama | LM Studio | Open WebUI |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Interface** | Desktop GUI + Headless Server | CLI-First + Background Daemon | Desktop GUI | Self-Hosted Web Portal |
| **Underlying Engine** | Nitro C++ Engine (`llama.cpp`) | Custom `llama.cpp` runner | `llama.cpp` native wrapper | External API dependent (Ollama/vLLM) |
| **FastMCP 3.1 Native** | First-Class Integration | Limited / Experimental | Plugin Extensions | Web-Tool Integrations |
| **Hardware Support** | Metal, CUDA, ROCm, DirectX | Metal, CUDA, ROCm | Metal, CUDA, ROCm | N/A (Delegated to Backend) |
| **Open Source License** | AGPL-3.0 Open Source | MIT License | Proprietary / Closed Source | MIT License |
| **Context Window Auto-Capping**| Native Automatic Context Capping | Manual `--ctx` parameter | Manual Model Settings | Server Admin Configured |
| **OpenAI API Compatibility**| `http://localhost:1337/v1` | `http://localhost:11434/v1` | `http://localhost:1234/v1` | Proxy Endpoint |

## Production Deployment & Optimization Checklist

1. **Hardware & VRAM Memory Allocation**:
   - Verify GPU layer offloading: Ensure all transformer layers are fully offloaded to VRAM (`--n-gpu-layers 99`).
   - Enable Flash Attention (`--flash-attn`) in Nitro Engine settings to cut memory usage during long context generation by up to 40%.

2. **Context Window Capping**:
   - Set default context limit (`n_ctx: 8192` or `16384`) matching host RAM limits to prevent out-of-memory (OOM) crashes during long agent reasoning loops.

3. **FastMCP 3.1 Security & Sandbox Boundary**:
   - Restrict local FastMCP tool servers bound to Jan to `localhost` loopback IP (`127.0.0.1`) to prevent external local network exploitation.
   - Enforce explicit user confirmation prompts in Jan GUI before executing destructive file or bash tools.

4. **Headless System Service Setup**:
   - On Linux servers, set up systemd services for `jan serve` to ensure automatic engine restarts following host reboots.

## Step-by-Step Troubleshooting Guide

### Issue 1: "Nitro Engine falls back to CPU despite active NVIDIA GPU"
- **Root Cause**: NVIDIA CUDA driver mismatch or missing CUDNN / CUDA toolkit runtime environment variables.
- **Resolution**:
  1. Check CUDA installation with `nvidia-smi`. Ensure CUDA version is 12.1 or newer.
  2. In Jan settings, toggle Hardware Acceleration -> Force CUDA.
  3. Inspect Nitro engine logs in `~/.jan/logs/nitro.log` for missing dynamic library symbols (`libcuda.so` or `nvcuda.dll`).

### Issue 2: "Inference fails with CUDA Out of Memory (OOM) error"
- **Root Cause**: The selected GGUF model size or target context window exceeds available GPU VRAM.
- **Resolution**:
  1. Switch to a higher quantization compression profile (e.g., transition from `Q8_0` to `Q4_K_M`).
  2. Reduce `n_ctx` in model settings from 32,768 down to 8,192.
  3. Enable GPU layer splitting between VRAM and System RAM if supported by host architecture.

### Issue 3: "FastMCP 3.1 tool call fails to respond or hangs thread"
- **Root Cause**: Local FastMCP tool server port `8000` is blocked by local firewall or SSE transport connection timed out.
- **Resolution**:
  1. Test tool server health independently with `curl http://127.0.0.1:8000/sse`.
  2. Ensure Jan's settings explicitly enable MCP tools (`mcp_enabled: true`).
  3. Verify JSON-RPC payload parsing errors in Jan's developer tools console (`Ctrl+Shift+I` / `Cmd+Option+I`).

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Fast, lightweight local LLM execution framework.
- [LM Studio](lm-studio.md) — Cross-platform desktop interface for GGUF model exploration.
- [Msty](msty.md) — Offline AI workspace desktop client.
- [LibreChat](../ai_knowledge/librechat.md) — Advanced open-source AI web UI.
- [Open WebUI](../../services/open-webui.md) — Feature-rich web interface for local LLM engines.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Supported protocol for extending Jan's capabilities.
- [Gemma 4](../ai_knowledge/local_llms.md) — Next-generation local model family supported by Jan.
- [Llama.cpp](../infrastructure/llama-cpp.md) — Core underlying C++ tensor inference engine behind Nitro.

## Sources / references
- [Jan.ai Official Portal](https://jan.ai/)
- [Jan Documentation & User Manual](https://jan.ai/docs)
- [Jan GitHub Repository](https://github.com/janhq/jan)
- [Nitro C++ Engine Architecture Specs](https://github.com/janhq/nitro)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
