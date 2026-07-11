# Jan.ai

## What it is
Jan is an open-source alternative to ChatGPT that runs 100% offline on your computer. It is built on top of `nitro`, a high-performance C++ inference engine, and provides a clean, privacy-focused desktop interface. As of July 2026 (v0.8.x+), Jan has expanded its hardware support, modular architecture, and native integration with the **MCP 3.0** standard.

## What problem it solves
Jan provides a fully open-source, private, and local-first AI workspace. It allows users to own their data and models, ensuring that conversations never leave their machine. It specifically addresses the "resource-heavy agent" problem by prioritizing a simpler, safer, and more practical agent experience over complex third-party integrations, while now offering controlled tool-use through **MCP 3.0**.

## Where it fits in the stack
**Infrastructure / Local Inference Engine**. It focuses on the "Local-First" desktop experience and provides a native, high-performance engine (`nitro`) for various hardware backends, serving as a private alternative to cloud AI providers.

## Typical use cases
- **Private, Offline Chat**: Serving as a privacy-first alternative to web-based AI assistants using models like [Gemma 3](../ai_knowledge/local_llms.md).
- **Hardware-Optimized Inference**: Leveraging AMD ROCm/HIP on Linux or Apple Silicon (M5 optimized) for high-speed local processing.
- **Headless Model Serving**: Using Jan as a local API backend for other applications via its built-in OpenAI-compatible server.
- **Context-Aware Assistance**: Utilizing its smarter context management to handle large documents without exceeding RAM limits.

## Strengths
- **Fully Open Source**: AGPL-3.0 licensed, transparent, and community-driven.
- **Hardware Agnostic**: Native support for Mac, Windows (NVIDIA/DirectX), and Linux (AMD/ROCm).
- **Efficient Performance**: The Nitro engine and phased-startup loader ensure fast time-to-first-paint and deferred heavy resource loading.
- **Privacy First**: No telemetry or cloud dependence by default, with local data location management.

## Limitations
- **Selective Ecosystem**: Does not integrate with "resource-heavy" agents (e.g., OpenClaw) to preserve system stability and security.
- **GUI Overhead**: While it has a CLI, the primary experience is a relatively heavy desktop application compared to raw engines like Llama.cpp.
- **Tool Complexity**: While MCP 3.0 is supported, setting up complex tool chains requires more manual configuration than some proprietary competitors.

## When to use it
- When privacy and data sovereignty are your top priorities in a desktop AI app.
- When you want an open-source, ChatGPT-like interface that is easy to install and manage.
- If you are running on AMD hardware on Linux and need native ROCm support.
- When you want to leverage [Gemma 3](../ai_knowledge/local_llms.md) in a private, local-first GUI.

## When not to use it
- If you strictly require integration with the OpenClaw agent ecosystem (which was removed in v0.7.9).
- For simple, low-level CLI tasks where a lightweight binary like Ollama would be faster to invoke.
- If you need a multi-user, web-based interface (consider Open WebUI instead).

## Getting started
1. **Download**: Obtain the latest stable version from [jan.ai](https://jan.ai/).
2. **Onboarding**: Launch the app and allow it to remotely fetch the latest model metadata.
3. **Download Model**: Use the "Hub" to download a hardware-optimized model like [Gemma 3](../ai_knowledge/local_llms.md); downloads are now resumable.
4. **Chat**: Select your model and begin a thread; Jan will automatically manage context capping for optimal performance.

## CLI examples
Jan includes a CLI tool for headless operation, model management, and automation.

```bash
# Start the Jan API server on a specific model
jan serve meta-llama-3.1-8b

# List all locally installed and available models
jan models list

# Run a quick inference via terminal using Gemma 3
jan chat --model gemma-3-27b --prompt "Explain the benefits of local LLMs."
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
- [Nitro Engine](nitro-engine.md) — The underlying high-performance C++ engine for Jan.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for extending Jan's capabilities (MCP 3.0).
- [Local LLMs (Gemma 3)](../ai_knowledge/local_llms.md) — Canonical source for local reasoning engines.

## Sources / References
- [Jan Official Website](https://jan.ai/)
- [Jan Changelog: v0.8.2 and Beyond](https://jan.ai/changelog/)
- [Jan GitHub Repository](https://github.com/janhq/jan)
- [Nitro Engine Documentation](https://nitro.jan.ai/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
