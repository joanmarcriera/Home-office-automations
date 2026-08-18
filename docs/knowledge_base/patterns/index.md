# Patterns

Recurring architectural and design patterns in AI/LLM systems — RAG, tool calling, agentic workflows, routing, guardrails, and security trust boundaries. Updated for early January 2027 SOTA standards (incorporating Claude 5.1, FastMCP 3.1, GPT-5.5/5.6, Gemini 4.0 Pro, Llama 4, and Pydantic v2 validation).

## Contents

<!-- New pattern pages are added here by Jules -->

- [Agent Skills Best Practices](skills-best-practices.md) — Skill authoring, trigger design, permission model, and validation checklist
- [Agentic Workflows Pattern](agentic-workflows.md) — Autonomous multi-step loops, tool execution, state management, and human-in-the-loop control
- [Claude Tool Search Pattern](claude-tool-search.md) — Dynamic tool discovery and deferred parameter resolution for massive agentic tool sets
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md) — Hybrid retrieval pattern for diagnostic analytics and SQL schema navigation
- [Data Copilot MCP Tooling](data-copilot-mcp-tooling.md) — Standardizing data access for Text-to-SQL pipelines using Model Context Protocol (MCP 3.1)
- [Date Extraction Pattern](date-extraction.md) — Parsing and normalizing relative temporal references into ISO 8601 with strict Pydantic v2 schemas
- [Extraction and Classification Pattern](extraction-and-classification.md) — Schema-first structured data extraction and multi-label classification
- [Fallback Patterns](fallback-patterns.md) — Architecting resilience via model failover, multi-provider redundancy, and fail-safe routing
- [Filesystem-as-Interface Pattern](filesystem-context.md) — Filesystem as the primary interface and persistence layer for agents
- [Fine-tuning Open Models](fine-tuning-open-models.md) — LoRA/QLoRA, Unsloth, axolotl, MLX, dataset prep, and GGUF export for local runtimes
- [LLM Trust Boundaries Pattern](llm-trust-boundaries.md) — Zero-trust agent architecture, boundary isolation, and prompt injection defense
- [n8n Error Handling Pattern](n8n-error-handling.md) — Enterprise error trapping, dead-letter queues, and automated incident recovery in workflow automation
- [OpenClaw Security Operations Pattern](openclaw-security-operations.md) — Operational security, identity federation, and audit logging for autonomous claw deployments
- [OpenClaw Use Case Catalog](openclaw-use-case-catalog.md) — Reference architecture catalog for enterprise OpenClaw agent deployment
- [OpenClaw Workflow Prompt Library Pattern](openclaw-workflow-prompts.md) — Standardized meta-prompts and execution contracts for autonomous agent pipelines
- [Prompt Requests Pattern](prompt_requests.md) — Structured request formatting, template versioning, and prompt optimization
- [RAG Pattern Architecture](rag-pattern.md) — Advanced hybrid retrieval-augmented generation with vector and structural indexing
- [Retrieval-Augmented Generation (RAG)](rag.md) — Grounding LLM output with retrieved context, hybrid search, and semantic re-ranking
- [Search Patterns](search-patterns.md) — Multi-modal search, hybrid dense/sparse retrieval, and iterative query refinement
- [Software Factories Pattern](software-factories.md) — Non-interactive development via seed, validation, and automated feedback loops
- [Tool Calling & Model Context Protocol (MCP)](tool-calling-and-mcp.md) — Universal standard (FastMCP 3.1) for connecting LLMs to external tools and data

## Common Patterns

- **RAG (Retrieval-Augmented Generation)** — Grounding LLM output with retrieved context via vector and tree-based indices
- **Agentic Workflows & Multi-Agent Collaboration** — Autonomous iterative execution loops with state management and dynamic handoffs
- **Tool Calling & MCP 3.1** — LLMs invoking external tools via FastMCP 3.1 structured schemas and type-safe contracts
- **Fine-tuning & Open Models** — Adapting open models (Llama 4, Gemma 3, Qwen 3.8) via LoRA/QLoRA for domain-specific behavior
- **Skills & Capability Modules** — Self-contained behavior modules with explicit triggers, system instructions, and permission constraints
- **Routing & Trust Boundaries** — Zero-trust query routing, boundary isolation, and security sanitization across multi-tier LLMs
- **Guardrails & Structured Validation** — Pydantic v2 schema-first input/output validation, safety filtering, and structured JSON output

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

- [Sandboxed Code Execution](sandboxed-execution.md) — Pattern for safely executing untrusted code in isolated container/microVM runtimes.

- [System Prompt Engineering](system-prompts.md) — Methodology and design patterns for system prompts in LLM and agentic workflows.
