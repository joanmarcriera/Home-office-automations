# Patterns

Recurring architectural and design patterns in AI/LLM systems — RAG, tool calling, routing, guardrails, and more.

## Contents

<!-- New pattern pages are added here by Jules -->

- [Retrieval-Augmented Generation (RAG)](rag.md) — Grounding LLM output with retrieved context
- [Tool Calling & Model Context Protocol (MCP)](tool-calling-and-mcp.md) — Universal standard for connecting LLMs to external tools and data
- [Claude Tool Search Pattern](claude-tool-search.md)
- [Agent Skills Best Practices](skills-best-practices.md) — Skill authoring, trigger design, permission model, validation checklist
- [Fine-tuning Open Models](fine-tuning-open-models.md) — LoRA/QLoRA, Unsloth, axolotl, MLX, dataset prep, GGUF export for Ollama
- [OpenClaw Workflow Prompt Library Pattern](openclaw-workflow-prompts.md)
- [LLM Trust Boundaries Pattern](llm-trust-boundaries.md)
- [Software Factories Pattern](software-factories.md) — Non-interactive development via seed, validation, and feedback loops
- [Filesystem-as-Interface Pattern](filesystem-context.md) — Filesystem as the primary interface and persistence layer for agents

## Common Patterns

- **RAG (Retrieval-Augmented Generation)** — Grounding LLM output with retrieved context
- **Fine-tuning** — Adapting open models via LoRA/QLoRA for domain-specific behaviour
- **Tool Calling & MCP** — LLMs invoking external tools via structured schemas and the Model Context Protocol (MCP)
- **Skills** — Self-contained behaviour modules with triggers, instructions, and permissions
- **Routing** — Directing queries to specialised models or agents
- **Guardrails** — Input/output validation and safety filtering
- **Chain-of-Thought** — Structured reasoning prompts
- **Multi-Agent Collaboration** — Multiple agents coordinating on a task
