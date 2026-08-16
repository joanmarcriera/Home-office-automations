# Patterns

Recurring architectural and design patterns in AI/LLM systems — RAG, tool calling, routing, guardrails, security operations, and agentic workflows in early 2027 SOTA environments (incorporating FastMCP 3.1, Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4).

## Contents

- [Agent Skills Best Practices](skills-best-practices.md) — Skill authoring, trigger design, permission model, validation checklist
- [Agentic Workflows](agentic-workflows.md) — Architectural taxonomy, dynamic looping, autonomous reflection, and state orchestration
- [Claude Tool Search Pattern](claude-tool-search.md) — Dynamic tool discovery and context compression for large tool catalogues
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md) — Hybrid retrieval pattern for diagnostic analytics
- [Data Copilot MCP Tooling](data-copilot-mcp-tooling.md) — Standardizing data access for Text-to-SQL pipelines using MCP
- [Date Extraction](date-extraction.md) — Parsing and normalizing relative temporal references into ISO 8601
- [Extraction and Classification](extraction-and-classification.md) — Schema-first structured data extraction and multi-label classification
- [Fallback Patterns](fallback-patterns.md) — Architecting resilience via model failover and fail-safe routing
- [Filesystem-as-Interface Pattern](filesystem-context.md) — Filesystem as the primary interface and persistence layer for agents
- [Fine-tuning Open Models](fine-tuning-open-models.md) — LoRA/QLoRA, Unsloth, axolotl, MLX, dataset prep, GGUF export for Ollama
- [LLM Trust Boundaries Pattern](llm-trust-boundaries.md) — Boundary enforcement, untrusted input containment, and privileged tool segregation
- [n8n Error Handling & Resilience](n8n-error-handling.md) — Defensive automation workflows, auto-retry policies, dead-letter routing, and alerting
- [OpenClaw Security Operations](openclaw-security-operations.md) — Threat modeling, secrets management, permission boundaries, and audit logging
- [OpenClaw Use Case Catalog](openclaw-use-case-catalog.md) — Real-world deployment patterns and operational automation recipes
- [OpenClaw Workflow Prompt Library Pattern](openclaw-workflow-prompts.md) — Standardized meta-prompt structure, parameter contracts, and system instructions
- [Prompt Requests & Specification](prompt_requests.md) — Structured intake schema for AI task specifications and automated execution prompts
- [RAG Pattern](rag-pattern.md) — Enterprise Retrieval-Augmented Generation with hybrid search, re-ranking, and citation tracking
- [Retrieval-Augmented Generation (RAG)](rag.md) — Grounding LLM output with retrieved context
- [Search Patterns & Query Transformation](search-patterns.md) — Query expansion, re-ranking, hybrid sparse-dense retrieval, and semantic deduplication
- [Software Factories Pattern](software-factories.md) — Non-interactive development via seed, validation, and feedback loops
- [Tool Calling & Model Context Protocol (MCP)](tool-calling-and-mcp.md) — Universal standard for connecting LLMs to external tools and data

## Common Patterns

- **RAG (Retrieval-Augmented Generation)** — Grounding LLM output with retrieved context
- **Fine-tuning** — Adapting open models via LoRA/QLoRA for domain-specific behaviour
- **Tool Calling & MCP** — LLMs invoking external tools via structured schemas and the Model Context Protocol (MCP)
- **Skills** — Self-contained behaviour modules with triggers, instructions, and permissions
- **Routing** — Directing queries to specialised models or agents
- **Guardrails** — Input/output validation and safety filtering
- **Chain-of-Thought** — Structured reasoning prompts
- **Multi-Agent Collaboration** — Multiple agents coordinating on a task

## Contribution Metadata

- Last reviewed: 2027-01-06
- Confidence: high
