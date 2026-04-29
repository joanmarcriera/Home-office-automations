# Msty

## What it is
Msty is a local-first AI desktop application designed to provide a professional, offline-capable workspace for interacting with both local models (via Ollama/Llama.cpp) and cloud-based AI providers.

## What problem it solves
It simplifies the process of running and managing local LLMs, providing tools like a VRAM calculator and a model hub, while maintaining the flexibility to route complex queries to powerful cloud models.

## Where it fits in the stack
**Category**: Infrastructure / AI Desktop App

## Typical use cases
- **Private Local Chat**: Running Llama 3 or Qwen models entirely offline for sensitive data.
- **Model Comparison**: Testing how different local and cloud models handle the same prompt in a side-by-side view.
- **Workflow Automation**: Using its "Turnstiles" feature and MCP tools to automate recurring tasks.

## Strengths
- **Developer-Friendly Tools**: Includes a built-in VRAM calculator, model cost estimator, and model "Matchmaker".
- **Local-First Design**: Optimized for local inference with deep integration for Ollama and Apple Silicon (MLX).
- **Rich Feature Set**: Supports Persona/Crew conversations, Knowledge Stacks (RAG), and a robust skill ecosystem.

## Limitations
- **Proprietary**: The core application is closed-source.
- **Paid Tier**: Advanced enterprise-grade features (Azure/Bedrock support, SSO) are locked behind an "Aurum" license.

## When to use it
- When you want the easiest possible path to running powerful local models on your desktop.
- When you need professional-grade features like RAG and multi-agent "Crews" in a local app.

## When not to use it
- If you strictly require open-source software.
- If you are looking for a web-based, collaborative platform for a large team (see [LobeHub](lobehub.md)).

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (Core features) / Paid (Aurum license for advanced features)
- **Self-hostable**: Yes (Local application)

## Related tools / concepts
- [Jan.ai](../infrastructure/jan-ai.md)
- [LM Studio](../infrastructure/lm-studio.md)
- [Ollama](../../services/ollama.md)
- [GPT Researcher](../agents/gpt-researcher.md)

## Sources / References
- [Msty Official Site](https://msty.ai/)
- [Msty Documentation](https://docs.msty.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
