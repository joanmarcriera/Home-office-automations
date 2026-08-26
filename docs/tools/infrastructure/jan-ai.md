# Jan.ai

## What it is
Jan is an open-source alternative to ChatGPT that runs 100% offline on your computer. It is built on top of the **Nitro Engine**, a high-performance C++ inference engine, and provides a clean, privacy-focused desktop interface. As of early 2027, Jan has expanded its hardware support and modular architecture to include native [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.1 and FastMCP 3.1 integration, acting as a robust tool-orchestrator and local client for frontier models.

## What problem it solves
Jan provides a fully open-source, private, and local-first AI workspace. It allows users to own their data and models, ensuring that conversations never leave their machine. It specifically addresses the "resource-heavy agent" problem by prioritizing a simpler, safer, and more practical agent experience, while supporting modern local models like [Gemma 3](../ai_knowledge/local_llms.md), Llama 4, and Qwen 3.6 on consumer hardware.

## Where it fits in the stack
**Category**: Infrastructure / Local Inference Engine. It focuses on the "Local-First" desktop experience and provides a native, high-performance engine (Nitro) for various hardware backends, leveraging [FastMCP 3.1](../automation_orchestration/mcp.md) for tool orchestration and agentic reasoning loops.

```
┌──────────────────────────────────────────────┐
│        Jan Desktop UI / Agent Client         │
│     (Privacy-First Desktop Workspace)        │
├──────────────────────────────────────────────┤
│         Tool Orchestration & Agents          │
│        (FastMCP 3.1 / Local Server)          │
├──────────────────────────────────────────────┤
│             Inference Layer                  │
│     (Nitro C++ Engine / Llama.cpp backend)   │
├──────────────────────────────────────────────┤
│            Hardware Acceleration             │
│   (Apple Silicon Metal, CUDA, AMD ROCm)      │
└──────────────────────────────────────────────┘
```

## Typical use cases
- **Private, Offline Chat**: Serving as a privacy-first alternative to web-based AI assistants using [Gemma 3](../ai_knowledge/local_llms.md), Llama 4, or Qwen 3.6.
- **Hardware-Optimized Inference**: Leveraging AMD ROCm/HIP on Linux, NVIDIA CUDA (Hopper/Blackwell), or Apple Silicon (M5/M6 optimized) for high-speed local processing.
- **Headless Model Serving**: Using Jan as a local API backend for other applications via its built-in server.
- **Context-Aware Assistance**: Utilizing its context management to handle large documents without exceeding RAM limits, supporting up to 256k context windows.

## Strengths
- **Fully Open Source**: AGPL-3.0 licensed, transparent, and community-driven.
- **Hardware Agnostic**: Native support for Mac, Windows (NVIDIA/DirectX), and Linux (AMD/ROCm).
- **Efficient Performance**: The Nitro engine and phased-startup loader ensure fast time-to-first-paint and deferred heavy resource loading.
- **MCP 3.1 Native**: Built-in support for the latest [Model Context Protocol](../automation_orchestration/mcp.md) standards for tool and server integration.

## Limitations
- **Selective Ecosystem**: Does not integrate with legacy agents to preserve system stability and security.
- **GUI Overhead**: While it has a CLI, the primary experience is a desktop application compared to raw engines like Llama.cpp.
- **Local Resources**: Performance is dependent on local hardware capabilities (VRAM/RAM).

## When to use it
- When privacy and data sovereignty are your top priorities in a desktop AI app.
- When you want an open-source, ChatGPT-like interface that is easy to install and manage.
- If you are running on AMD hardware on Linux and need native ROCm support.

## When not to use it
- If you strictly require legacy agent integrations that have been deprecated in favor of MCP.
- For simple, low-level CLI tasks where a lightweight binary like Ollama would be faster to invoke.

## Getting started
1. **Download**: Obtain the latest stable version from [jan.ai](https://jan.ai/).
2. **Onboarding**: Launch the app and allow it to remotely fetch the latest model metadata.
3. **Download Model**: Use the "Hub" to download a hardware-optimized model (e.g., [Gemma 3](../ai_knowledge/local_llms.md) or Llama 4); downloads are resumable.
4. **Chat**: Select your model and begin a thread; Jan will automatically manage context capping for optimal performance.

## CLI examples
Jan includes a CLI tool for headless operation, model management, and automation.

```bash
# Start the Jan API server on a specific model
jan serve gemma-3-27b

# List all locally installed and available models
jan models list

# Run a quick inference via terminal
jan chat --model mistral-nemo --prompt "Explain quantum entanglement."
```

## API examples
Jan provides an OpenAI-compatible API on `localhost:1337` by default. Below is a Python example utilizing modern, asynchronous calls and strict **Pydantic v2** validation to model and parse the local response payloads from Jan's server.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
import openai

# 1. Define strict Pydantic v2 validation schemas for Jan inference configurations
class JanInferenceConfig(BaseModel):
    model_name: str = Field(alias="model", default="gemma-3-27b")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0)
    stream: bool = Field(default=False)
    mcp_enabled: bool = Field(default=True)
    mcp_servers: List[HttpUrl] = Field(default_factory=list)

class ChoiceMessage(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: Optional[str] = None

class JanChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]

# 2. Asynchronous client interacting with Jan's local inference engine
async def query_local_jan_engine(prompt: str, config: JanInferenceConfig) -> JanChatCompletionResponse:
    # Connect using OpenAI's async client to the local Jan port (default 1337)
    client = openai.AsyncOpenAI(base_url="http://localhost:1337/v1", api_key="jan")

    response = await client.chat.completions.create(
        model=config.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        stream=config.stream
    )

    # 3. Validate raw dictionary output through Pydantic v2
    raw_response_dict = response.model_dump()
    validated_response = JanChatCompletionResponse.model_validate(raw_response_dict)
    return validated_response

# 4. Driver execution
async def main():
    config = JanInferenceConfig(model="gemma-3-27b", temperature=0.1)
    prompt_text = "What is the role of FastMCP 3.1 in local AI coordination?"

    try:
        result = await query_local_jan_engine(prompt_text, config)
        print(f"Validated Model: {result.model}")
        print(f"Response: {result.choices[0].message.content}")
    except Exception as e:
        print(f"Failed local inference: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Fast, lightweight local CLI inference.
- [LM Studio](lm-studio.md) — GUI for exploring GGUF models.
- [Msty](msty.md) — Modular "AI OS" for the desktop.
- [LibreChat](../ai_knowledge/librechat.md) — Advanced self-hosted web UI.
- [Open WebUI](../../services/open-webui.md) — Collaborative web interface for local LLMs.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Supported for extending Jan's capabilities.
- [Gemma 3](../ai_knowledge/local_llms.md) — High-performance local model supported by Jan.
- [Llama.cpp](../infrastructure/llama-cpp.md) — Underlying technology for many local engines.

## Sources / references
- [Jan Official Website](https://jan.ai/)
- [Jan Changelog](https://jan.ai/changelog/)
- [Jan GitHub Repository](https://github.com/janhq/jan)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
