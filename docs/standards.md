# Standards and Conventions

## What it is
This document defines the technical standards and operational conventions for the homelab automation stack. It ensures interoperability between diverse tools, maintains documentation quality, and provides a clear protocol for autonomous agents and human contributors.

## What problem it solves
In a complex, multi-tool environment with frequent contributions from AI agents, fragmentation and inconsistency are high risks. These standards eliminate ambiguity in naming, document structure, metadata, and cross-tool communication, ensuring the repository remains a reliable source of truth.

## Where it fits in the stack
Governance Layer — acts as the foundational contract for all activities within the repository, from documentation updates to new service deployments.

## Typical use cases
- **Documentation Audits**: Providing the criteria used by scripts like `check_docs_contract.py` to verify page quality.
- **Agent Onboarding**: Giving new AI agents the "rules of the road" for how to contribute safely and effectively.
- **Workflow Design**: Setting the expectations for how n8n workflows should be named and how data should be formatted.

## Strengths
- **Consistency**: Enforces a uniform "look and feel" across hundreds of documentation pages.
- **Automation-Friendly**: Standards are defined with programmatic verification in mind (using Python scripts).
- **Interoperability**: Standardized data formats (JSON) and date types (ISO8601) simplify tool integration.

## Limitations
- **Overhead**: Requires contributors to follow specific steps (registry updates, metadata additions) which can be slower for manual edits.
- **Enforcement Gap**: While many standards are script-verified, some (like "one canonical page") still require human or advanced AI judgment.

## When to use it
- Whenever creating a new tool page or reference implementation.
- When designing a new n8n workflow or drafting a system prompt.
- Before submitting a Pull Request to ensure all quality gates pass.

## When not to use it
- For temporary, local-only notes that will not be merged into the repository.
- During rapid prototyping where speed is prioritized over documentation (though standards should be retrofitted before merge).

## Core Taxonomy

The knowledge base uses a stable set of top-level categories. Do not create new top-level sections unless strictly necessary.

| Category | Location | What belongs here |
| :--- | :--- | :--- |
| **AI & Knowledge** | `docs/tools/ai_knowledge/` | General AI tools, knowledge management, LLM products |
| **Frameworks** | `docs/tools/frameworks/` | Libraries for building LLM apps (LangChain, LlamaIndex, etc.) |
| **Providers** | `docs/tools/providers/` | Companies offering LLM APIs or managed AI services |
| **Agents** | `docs/tools/agents/` | Agent frameworks and autonomous AI tools |
| **Orchestration** | `docs/tools/orchestration/` | Workflow automation, multi-agent routing, pipeline tools |
| **Infrastructure** | `docs/tools/infrastructure/` | Inference engines, vector DBs, serving stacks, quantisation |
| **Benchmarking** | `docs/tools/benchmarking/` | Eval frameworks, benchmarks, leaderboards |
| **Development & Ops** | `docs/tools/development_ops/` | AI-assisted coding tools and IDEs |
| **Patterns** | `docs/knowledge_base/patterns/` | Recurring design patterns (RAG, tool calling, routing, etc.) |
| **Playbooks** | `docs/playbooks/` | Step-by-step workflow guides |

## KnowledgeOps Contract

### 1. Deduplication & Canonicals
- **One canonical page per tool/topic.** All other mentions must link to that canonical page.
- Before creating a new page, search the repo for the tool name, URL, and common aliases.
- Update `data/all_tools.json` and `mkdocs.yml` navigation when adding a new canonical.

### 2. Required Document Sections
Every high-confidence documentation page must include these 13 sections:
1. `What it is`
2. `What problem it solves`
3. `Where it fits in the stack`
4. `Typical use cases`
5. `Strengths`
6. `Limitations`
7. `When to use it`
8. `When not to use it`
9. `Getting started` (must include installation and hello-world example)
10. `CLI examples` (at least 3 practical commands)
11. `API examples` (minimal code snippet with standardized variables like `API_URL` and `headers`)
12. `Related tools / concepts` (>= 7 relative markdown links)
13. `Sources / references` (at least one valid URL)

> [!NOTE]
> If official documentation for `Getting started`, `CLI examples`, or `API examples` is unavailable, these sections must still be present with a note indicating their status.

### 3. Contribution Metadata (Required)
Every knowledge page must include this section at the bottom:
- `Last reviewed`: ISO date (`YYYY-MM-DD`)
- `Confidence`: `high`, `medium`, or `low`

## Technical Conventions

### Naming
- **Tags (Paperless)**: `kebab-case`. Lowercase only. Prefix status tags with `s:` and category tags with `c:`.
- **Workflows (n8n)**: `[Trigger Source] -> [Primary Action]`. Example: `IMAP -> Paperless Intake`.
- **Prompts**: Versioned using SemVer. Store as Markdown files in `reference-implementations/llm-prompts/`.
- **API Constants**: Use `API_URL`, `API_TOKEN`, or `API_KEY` (uppercase) for global configuration and `headers` (lowercase) for local request headers.

### Model Benchmarking (June 2026 Standards)
When referencing frontier models in documentation, use the following standardized identifiers:
- **Claude**: `Claude 4.7` (Haiku/Sonnet) or `Claude 4.8` (Opus).
- **GPT**: `GPT-5.5` (standard or reasoning).
- **Llama**: `Llama 4 Maverick`.
- **Protocol**: `Model Context Protocol (MCP)` is the default for all tool integrations.

### Interoperability
- **Data Format**: All cross-tool communication should prefer **JSON**.
- **Dates**: Always use **ISO8601** with UTC offsets.
- **IDs**: Use the internal ID of the source system (e.g. Paperless `document_id`) in destination metadata.

## Related tools / concepts
- [AGENTS.md](../AGENTS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [Multi-Agent KnowledgeOps contract](knowledge_base/patterns/agentic-workflows.md)
- [n8n Service](services/n8n.md)
- [Paperless-ngx](services/paperless-ngx.md)
- [Audit Docs Quality Script](../scripts/audit_docs_quality.py)
- [Check Docs Contract Script](../scripts/check_docs_contract.py)

## Sources / references
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [n8n Best Practices](https://docs.n8n.io/workflows/best-practices/)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
