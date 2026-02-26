# Local LLMs (Ollama, MLX, llama.cpp)

## What it is
Tools and frameworks that allow running Large Language Models directly on your own hardware (Homelab, Workstation, Mac).

- **Ollama**: The easiest way to get up and running with a simple CLI and API.
- **MLX**: Apple's framework for high-performance AI on Apple Silicon.
- **llama.cpp**: The foundational C++ library for running LLMs on consumer hardware.

## What problem it solves
Provides 100% privacy, works offline, has no per-token costs, and allows for infinite experimentation without API limits.

## Where it fits in the stack
**LLM / Reasoning Engine (Self-hosted)**. Replaces cloud providers for tasks that don't require the massive scale of GPT-4.

## Architecture overview
The model weights are downloaded and stored locally. Inference is performed using your local CPU/GPU/NPU.

## Typical workflows
- **Local Development**: Testing agent logic without incurring costs.
- **Sensitive Data Processing**: Summarizing private documents or logs.
- **Always-on Low-latency Tasks**: Simple classification or formatting that needs to happen fast and often.

## Strengths
- **Privacy**: No data leaves your machine.
- **Cost**: Free (after purchasing the hardware).
- **Latency**: No network round-trip to external APIs.
- **Customization**: Use any open-weight model (Llama 3, Mistral, Qwen, etc.).

## Limitations
- **Performance**: Generally lower reasoning capability than the largest cloud models (GPT-4o/Claude 3.5).
- **Hardware Requirement**: Requires significant RAM (especially for larger models) and GPU/NPU acceleration.
- **Maintenance**: You are responsible for updating software and managing model files.

## When to use it
- For any task involving sensitive or personal data.
- When you want to avoid recurring costs for high-volume, simpler tasks.
- For local coding assistants (e.g., using `llama-3-8b` or `deepseek-coder` locally).

## When not to use it
- When you need the absolute highest reasoning performance available today.
- If you lack dedicated hardware (GPU with 12GB+ VRAM or 16GB+ Mac Unified Memory).

## Security considerations
- **Local API Access**: By default, Ollama and others might listen on `localhost`. Be careful when exposing these to your local network.
- **Model Integrity**: Download models from trusted sources (like the official Ollama library or reputable HuggingFace users).

## Links to related pages
- [Ollama (Service)](../../services/ollama.md)
- [DeepSeek](deepseek.md)
- [SSH Execution Patterns](../../architecture/ssh_execution_patterns.md)

## Sources / References

- [Reference](https://github.com/joanmarcriera/Home-office-automations)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
