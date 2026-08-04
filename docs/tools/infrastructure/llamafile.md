# Llamafile

## What it is
Llamafile is an open-source project (originally from Mozilla) that packages an entire LLM — model weights **and** the inference runtime — into a **single executable file** that runs on macOS, Linux, Windows, and BSD without installation. It combines [llama.cpp](llama-cpp.md) with the Cosmopolitan Libc "Actually Portable Executable" format, so one downloaded file launches a local chat server with no dependencies. As of late 2026, Llamafile has integrated native support for [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.1 endpoints, facilitating portable, offline tool execution.

## What problem it solves
It collapses the usual local-LLM setup (install runtime, fetch weights, configure flags) into "download one file and run it." This makes local inference trivially reproducible and ideal for **air-gapped distribution**: you can hand someone a USB stick with a single file and they have a working offline assistant, with zero external package installations.

## Where it fits in the stack
**Infrastructure / Self-contained local inference.** It is the lowest-friction way to ship or archive a runnable model. It exposes an OpenAI-compatible endpoint, so it can act as a drop-in local backend for agents, automation in [n8n](../../services/n8n.md), or offline desktop applications.

## Typical use cases
- Distributing a ready-to-run offline model to machines with no internet or package managers.
- Keeping a long-term, dependency-free archive of a model that will still run years later.
- Quick local experimentation: download, `chmod +x`, run, and get a chat server instantly.
- Embedding a portable local LLM into a larger offline appliance or hardware kiosk.

## Strengths
- **Single-file portability:** no install, no runtime, no virtualenv — one file is the whole stack.
- **Truly offline & archival:** self-contained binaries keep working without network or future dependency drift.
- **OpenAI-compatible server:** integrates with existing tooling expecting an OpenAI API.
- **Cross-platform from one artifact:** the same file runs across major OSes and CPU architectures.
- **Licensing and Cost:** Highly permissive (Apache 2.0 tooling) and completely free and self-hostable.

## Limitations
- **Large files:** weights are embedded, so binaries can be several gigabytes.
- **Platform quirks:** some OSes impose executable-size limits or require an extra step for very large files.
- **Single-model artifact:** each file is one model; managing many models is less convenient than a model manager like [Ollama](../../services/ollama.md).
- **Performance ceiling:** inherits llama.cpp's characteristics; not aimed at high-concurrency enterprise serving.

## When to use it
- When you need a **zero-install, offline** model that "just runs" on heterogeneous machines.
- For air-gapped or archival scenarios where future reproducibility matters.
- For demos or handoffs where you cannot assume any local toolchain.

## When not to use it
- When you juggle many models and want central management — use [Ollama](../../services/ollama.md).
- For scaled, multi-user, high-throughput serving — use [vLLM](vllm.md).

## Getting started

### Installation
Download a pre-built llamafile for a specific model (e.g., Llama 4 or Qwen 3.6) from the [Mozilla-Ocho Hugging Face](https://huggingface.co/mozilla-ai) repository.

### Hello World Example
```bash
# 1. Download the executable
curl -LO https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-0.8B-Q8_0.llamafile

# 2. Make it executable
chmod +x Qwen3.5-0.8B-Q8_0.llamafile

# 3. Run the local chat server
./Qwen3.5-0.8B-Q8_0.llamafile
```
Windows users should rename the file to end in `.exe` before running.

## CLI examples
```bash
# Start the server on a specific port
./model.llamafile --port 9000

# Run in text completion mode (no server)
./model.llamafile -p "Write a hello world script in Python:" -n 128

# Offload layers to GPU (if available)
./model.llamafile --n-gpu-layers 35
```

## API examples
Llamafile provides an OpenAI-compatible API. Once the llamafile is running, you can interact with it using standard tools. Below is a robust Python example utilizing strict **Pydantic v2** validation to verify and parse Llamafile health and configuration attributes.

```python
import requests
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl

# 1. Define Llamafile endpoint configuration and metadata schemas using Pydantic v2
class LlamafileServerConfig(BaseModel):
    endpoint_url: HttpUrl = Field(default="http://localhost:8080")
    timeout_seconds: int = Field(default=10, ge=1)
    target_model_alias: Optional[str] = Field(default="LLaMA_CPP")

class ModelInfo(BaseModel):
    model_name: str = Field(alias="id")
    object: str
    owned_by: str

class LlamafileStatusResponse(BaseModel):
    status: str
    active_models: List[ModelInfo] = Field(default_factory=list)

# 2. Programmatic validator class to interact with Llamafile API
class LlamafileClient:
    def __init__(self, config: LlamafileServerConfig):
        self.config = config

    def check_health(self) -> LlamafileStatusResponse:
        try:
            # Query the OpenAI-compatible models endpoint
            url = f"{self.config.endpoint_url}v1/models"
            response = requests.get(url, timeout=self.config.timeout_seconds)

            if response.status_code == 200:
                raw_data = response.json()
                # Parse models list
                models_list = raw_data.get("data", [])
                parsed_models = [ModelInfo.model_validate(m) for m in models_list]
                return LlamafileStatusResponse(status="healthy", active_models=parsed_models)
        except Exception as e:
            print(f"Llamafile health check failed: {e}")

        return LlamafileStatusResponse(status="unreachable", active_models=[])

# 3. Driver block
if __name__ == "__main__":
    server_config = LlamafileServerConfig(endpoint_url="http://localhost:8080")
    client = LlamafileClient(server_config)
    status = client.check_health()
    print(f"Llamafile Connection Status: {status.status}")
    for model in status.active_models:
        print(f"Loaded Model ID: {model.model_name}")
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — The inference engine Llamafile embeds.
- [Ollama](../../services/ollama.md) — Multi-model local runtime and manager.
- [GPT4All](gpt4all.md) — Desktop offline assistant with document RAG.
- [LM Studio](lm-studio.md) — Desktop local-LLM application.
- [Kiwix](../../services/kiwix.md) — Companion pattern for offline knowledge distribution.
- [LocalAI](localai.md) — Self-hosted OpenAI-compatible local API server.
- [vLLM](vllm.md) — High-throughput serving engine for the scaled case.
- [MLX](mlx.md) — Apple-silicon local inference backend.

## Sources / references
- [Llamafile GitHub (Mozilla-Ocho)](https://github.com/Mozilla-Ocho/llamafile)
- [Cosmopolitan Libc](https://github.com/jart/cosmopolitan)
- [Introducing Llamafile (Mozilla blog)](https://hacks.mozilla.org/2023/11/introducing-llamafile/)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
