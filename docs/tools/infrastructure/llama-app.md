# llama.app

## What it is
`llama.app` is a native macOS graphical user interface and companion desktop client for `llama.cpp` and `llama-server`. Designed specifically for macOS and Apple Silicon hardware (M1/M2/M3/M4 Series), it provides a clean, user-friendly interface for managing local GGUF models, launching local OpenAI-compatible inference servers, and chatting with LLMs offline.

## What problem it solves
While `llama.cpp` is the gold standard for high-performance GGUF local inference, configuring its command-line parameters (`-m`, `-c`, `-ngl`, `--temp`, `-b`) can be complex and intimidating for developers and non-technical users. `llama.app` wraps `llama.cpp` and `llama-server` into a native macOS app, offering zero-config model discovery, hardware-accelerated Metal execution, and visual server management.

## Where it fits in the stack
**Infrastructure / Local Inference Client**. It sits directly on top of `llama.cpp` and `llama-server` on macOS, providing local inference capabilities to local LLM clients, browser extensions, and agent frameworks via standard OpenAI REST endpoints.

## Typical use cases
- **Native macOS Local Chat**: Interacting with local GGUF models (e.g., Llama 4 Maverick, DeepSeek-V4, Gemma 4, Qwen 3.6) with zero cloud dependency.
- **Background OpenAI Endpoint**: Running `llama-server` in the background with custom VRAM and Metal layer offloading settings for agent integration.
- **Model Library Management**: Browsing, downloading, and organising local GGUF files across custom local directories.

## Strengths
- **Native Metal Optimization**: Fully utilizes Apple Silicon Unified Memory and GPU cores via optimized Metal shaders.
- **Zero-Configuration Server**: Automatically manages `llama-server` processes and exposes standard OpenAI-compatible API endpoints (`http://localhost:8080/v1`).
- **Low Overhead**: Lightweight native macOS application without heavy WebKit or Electron memory footprints.
- **Privacy-First**: Operates 100% offline without telemetry or external tracking.

## Limitations
- **macOS Exclusive**: Tailored specifically for macOS; not available on Linux or Windows.
- **GUI Abstraction**: Advanced fine-tuning options or niche GBNF grammar configurations available in raw `llama.cpp` CLI may require manual CLI overrides.

## When to use it
- On Apple Silicon Mac workstations where you want a simple native interface to manage local `llama.cpp` models.
- When serving local GGUF models to developer tools like VS Code extensions or local FastMCP agents.

## When not to use it
- On Linux or Windows operating systems (use [LM Studio](lm-studio.md), [Jan.ai](jan-ai.md), or raw [llama.cpp](llama-cpp.md)).
- In headless Linux server or containerized production deployment environments.

## Getting started

### Installation
1. Download the latest release `.dmg` from the official repository or community release page.
2. Drag `llama.app` to your `/Applications` folder.
3. Open `llama.app` and select your local model directory containing `.gguf` files.

### Server Integration
Once started, `llama.app` exposes an OpenAI-compatible REST server:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-4-maverick",
    "messages": [{"role": "user", "content": "Hello from local Mac server!"}]
  }'
```

## CLI examples
```bash
# Check running llama-server process bound by llama.app
pgrep -af llama-server

# Point local Python OpenAI client to llama.app server
export OPENAI_API_BASE="http://localhost:8080/v1"
export OPENAI_API_KEY="not-needed"
```

## API examples
```python
import openai

# Connect OpenAI Python SDK to local llama.app server
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="llama-4-maverick",
    messages=[{"role": "user", "content": "Explain quantisation in 2 sentences."}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- **[llama.cpp](llama-cpp.md)**: Foundational C/C++ local GGUF inference runtime.
- **[LM Studio](lm-studio.md)**: Cross-platform local LLM desktop GUI client.
- **[Jan.ai](jan-ai.md)**: Open-source desktop assistant for local model execution.

## Sources / references
- [llama.app Reddit Release Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1vdt1i2/psa_llamaapp_mac_app_and_llama_serve_from_llamacpp/?ref=2026-09-21-audit)
- [llama.cpp Repository](https://github.com/ggerganov/llama.cpp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
