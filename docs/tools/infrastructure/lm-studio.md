# LM Studio

## What it is
LM Studio is a desktop application that allows users to discover, download, and run local Large Language Models (LLMs) on their own hardware. It provides a user-friendly graphical interface (GUI) for managing GGUF-formatted models.

## What problem it solves
It lowers the barrier to entry for running local AI by providing a simple "one-click" experience. It handles model downloading from Hugging Face, hardware acceleration (including Apple Silicon and NVIDIA GPUs), and provides a local OpenAI-compatible server for integration with other tools.

## Where it fits in the stack
Infrastructure and Local Inference Engine. It is a desktop-centric alternative to [Ollama](../../services/ollama.md).

## Typical use cases
- Testing different open-source models (Llama, Mistral, etc.) without writing code.
- Running a local, private chatbot.
- Providing a local API for tools like [Cursor](../../docs/tools/development_ops/cursor.md) or [Claude Code](../../docs/tools/development_ops/claude_code.md).

## Strengths
- **Ease of Use**: Excellent GUI for discovery and configuration.
- **Hardware Auto-Detection**: Automatically configures GPU offloading.
- **In-App Discovery**: Integrated search and download from Hugging Face.
- **Model Compatibility**: Broad support for GGUF quants.

## Limitations
- **Closed Source**: The application itself is proprietary, though it runs open-source models.
- **Desktop Only**: Primarily designed for interactive desktop use, not headless server environments.
- **Resource Intensive**: Requires significant RAM and VRAM for larger models.

## When to use it
- When you want a GUI-first experience for managing local LLMs.
- When you are on macOS or Windows and want the easiest possible setup.
- When you need to quickly benchmark different quantization levels.

## When not to use it
- If you need a lightweight, headless server (use [Ollama](../../services/ollama.md)).
- If you require a fully open-source stack.
- For high-concurrency production workloads.

## Licensing and cost
- **Open Source**: No (Proprietary application).
- **Cost**: Free for personal use.
- **Self-hostable**: Yes (Runs locally on your machine).

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [Hugging Face](../providers/huggingface.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website](https://lmstudio.ai/)
- [LM Studio Documentation](https://lmstudio.ai/docs)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-04-06
