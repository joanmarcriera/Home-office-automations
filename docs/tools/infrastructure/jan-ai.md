# Jan.ai

## What it is
Jan is an open-source alternative to ChatGPT that runs 100% offline on your computer. It is built on top of the **Nitro Engine**, a high-performance C++ inference engine, and provides a clean, privacy-focused desktop interface. As of July 2026 (v0.9.0+), Jan has expanded its hardware support and modular architecture to include native [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.0 integration.

## What problem it solves
Jan provides a fully open-source, private, and local-first AI workspace. It allows users to own their data and models, ensuring that conversations never leave their machine. It specifically addresses the "resource-heavy agent" problem by prioritizing a simpler, safer, and more practical agent experience, while supporting modern local models like [Gemma 3](../ai_knowledge/local_llms.md).

## Where it fits in the stack
**Category**: Infrastructure / Local Inference Engine. It focuses on the "Local-First" desktop experience and provides a native, high-performance engine (Nitro) for various hardware backends, now leveraging [FastMCP 3.0](../automation_orchestration/mcp.md) for tool orchestration.

## Typical use cases
- **Private, Offline Chat**: Serving as a privacy-first alternative to web-based AI assistants using [Gemma 3](../ai_knowledge/local_llms.md).
- **Hardware-Optimized Inference**: Leveraging AMD ROCm/HIP on Linux, NVIDIA CUDA, or Apple Silicon (M5 optimized) for high-speed local processing.
- **Headless Model Serving**: Using Jan as a local API backend for other applications via its built-in server.
- **Context-Aware Assistance**: Utilizing its smarter context management to handle large documents without exceeding RAM limits.

## Strengths
- **Fully Open Source**: AGPL-3.0 licensed, transparent, and community-driven.
- **Hardware Agnostic**: Native support for Mac, Windows (NVIDIA/DirectX), and Linux (AMD/ROCm).
- **Efficient Performance**: The Nitro engine and phased-startup loader ensure fast time-to-first-paint and deferred heavy resource loading.
- **MCP 3.0 Native**: Built-in support for the latest [Model Context Protocol](../automation_orchestration/mcp.md) standards for tool and server integration.

## Limitations
- **Selective Ecosystem**: Does not integrate with "resource-heavy" legacy agents to preserve system stability and security.
- **GUI Overhead**: While it has a CLI, the primary experience is a relatively heavy desktop application compared to raw engines like Llama.cpp.
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
3. **Download Model**: Use the "Hub" to download a hardware-optimized model (e.g., [Gemma 3](../ai_knowledge/local_llms.md) or Qwen 2.5); downloads are now resumable.
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
Jan provides an OpenAI-compatible API on `localhost:1337` by default.

```python
import openai

# Connect to Jan's local server
client = openai.OpenAI(base_url="http://localhost:1337/v1", api_key="jan")

completion = client.chat.completions.create(
  model="gemma-3-27b",
  messages=[{"role": "user", "content": "How do I secure a home server?"}]
)
print(completion.choices[0].message.content)
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

## Sources / References
- [Jan Official Website](https://jan.ai/)
- [Jan Changelog: v0.9.0 and Beyond](https://jan.ai/changelog/)
- [Jan GitHub Repository](https://github.com/janhq/jan)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
