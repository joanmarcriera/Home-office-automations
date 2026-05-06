# Jan.ai

## What it is
Jan is an open-source alternative to ChatGPT that runs 100% offline on your computer. It is built on top of `nitro`, a high-performance C++ inference engine, and provides a clean, privacy-focused desktop interface.

## What problem it solves
Jan provides a fully open-source, private, and local-first AI workspace. It allows users to own their data and models, ensuring that conversations never leave their machine unless explicitly intended.

## Where it fits in the stack
Infrastructure and Local Inference Engine. It focuses on the "Local-First" desktop experience.

## Typical use cases
- Private, offline alternative to web-based AI assistants.
- Managing a local library of models for different tasks (coding, writing, analysis).
- Extending local capabilities via its built-in extension system.

## Strengths
- **Fully Open Source**: Transparent and community-driven.
- **Privacy First**: No telemetry or cloud dependence by default.
- **Cross-Platform**: Available for Windows, macOS, and Linux.
- **Extensible**: Supports plugins and custom model configurations.

## Limitations
- **GUI Overhead**: Heavier than command-line tools for simple API needs.
- **Development Pace**: Features may trail behind proprietary alternatives.

## When to use it
- When privacy and data sovereignty are your top priorities.
- When you want an open-source, ChatGPT-like interface for local models.
- When you want to customize your local AI experience with extensions.

## When not to use it
- If you only need a raw API endpoint for other applications.
- If you prefer a more "it just works" experience with automatic hardware tuning (LM Studio might be faster for some).

## Getting started
1. Download Jan from [jan.ai](https://jan.ai/) for your OS.
2. Open the application and use the "Hub" to download a model (e.g., Llama 3).
3. Start a new thread and select the downloaded model to begin chatting.
4. (Optional) Enable the "API Server" in settings to use Jan as a local backend.

## CLI examples
Jan includes a CLI tool (often called `jan` or `janctl` depending on version) for headless operation and integration.

```bash
# Start a local model server
jan serve meta-llama-3-8b

# List available models
jan models list

# Launch an agent (like Claude Code) pre-wired to your local model
jan launch claude --model llama-3-8b
```

## API examples
Jan provides an OpenAI-compatible API on `localhost:1337` by default.

```python
import openai

client = openai.OpenAI(base_url="http://localhost:1337/v1", api_key="jan")

completion = client.chat.completions.create(
  model="meta-llama-3-8b",
  messages=[{"role": "user", "content": "How do I secure a home server?"}]
)
print(completion.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0).
- **Cost**: Free.
- **Self-hostable**: Yes (Runs locally on your machine).

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](lm-studio.md)
- [Msty](msty.md)
- [LibreChat](../ai_knowledge/librechat.md)
- [Open WebUI](../../services/open-webui.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website](https://jan.ai/)
- [Jan GitHub Repository](https://github.com/janhq/jan)
- [Jan CLI Documentation](https://jan.ai/docs/desktop/cli)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
