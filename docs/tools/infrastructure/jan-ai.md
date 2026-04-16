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

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0).
- **Cost**: Free.
- **Self-hostable**: Yes (Runs locally on your machine).

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](lm-studio.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website](https://jan.ai/)
- [Jan GitHub Repository](https://github.com/janhq/jan)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-04-06
