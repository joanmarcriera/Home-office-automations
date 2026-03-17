# LM Studio

## What it is
LM Studio is a desktop application for discovering, downloading, running, and chatting with local models.

## What problem it solves
It lowers the barrier to local LLM experimentation by packaging model discovery, downloads, chat, and an OpenAI-compatible local server into one desktop workflow.

## Where it fits in the stack
**AI & Knowledge / Local Model Workbench**. It is a practical bridge between end-user experimentation and local inference.

## Typical use cases
- Testing local models without a CLI-heavy setup
- Running a local OpenAI-compatible endpoint for development
- Comparing small and medium models on a laptop or workstation

## Strengths
- Easy local-model onboarding
- Friendly UI for experimentation
- Useful stepping stone before deeper infrastructure choices

## Limitations
- Less flexible than lower-level inference stacks for production
- Desktop-first workflow is not ideal for multi-user deployment

## When to use it
- When you want the fastest path to trying local models
- When you need a simple local server for app development or evaluation

## When not to use it
- When you need multi-user, server-grade inference
- When you already operate [Ollama](../../services/ollama.md) or [vLLM](../infrastructure/vllm.md) successfully

## Licensing and cost
- **Open Source**: No
- **Cost**: Free desktop app
- **Self-hostable**: Local desktop runtime only

## Related tools / concepts

- [Local LLMs (Ollama, MLX, llama.cpp)](local_llms.md)
- [Ollama](../../services/ollama.md)
- [llama.cpp](../infrastructure/llama-cpp.md)

## Sources / References
- [Official Website](https://lmstudio.ai/)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: high
