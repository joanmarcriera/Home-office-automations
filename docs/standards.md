# Standards and Conventions

This document defines the technical standards for tools to interoperate within this automation stack.

## Taxonomy

The knowledge base uses a stable set of top-level categories. Do not create new top-level sections unless strictly necessary.

| Category | Location | What belongs here |
| :--- | :--- | :--- |
| **AI & Knowledge** | `tools/ai_knowledge/` | General AI tools, knowledge management, LLM products |
| **Frameworks** | `tools/frameworks/` | Libraries for building LLM apps (LangChain, LlamaIndex, etc.) |
| **Providers** | `tools/providers/` | Companies offering LLM APIs or managed AI services |
| **Agents** | `tools/agents/` | Agent frameworks and autonomous AI tools |
| **Orchestration** | `tools/orchestration/` | Workflow automation, multi-agent routing, pipeline tools |
| **Infrastructure** | `tools/infrastructure/` | Inference engines, vector DBs, serving stacks, quantisation |
| **Benchmarking** | `tools/benchmarking/` | Eval frameworks, benchmarks, leaderboards |
| **Development & Ops** | `tools/development_ops/` | AI-assisted coding tools and IDEs |
| **Patterns** | `knowledge_base/patterns/` | Recurring design patterns (RAG, tool calling, routing, etc.) |
| **Playbooks** | `playbooks/` | Step-by-step workflow guides |

### Deduplication Rules

- **One canonical page per tool/framework/provider.** All other mentions must link to that canonical page.
- Before creating a new page, search the repo for the tool name, URL, and common aliases.
- If a source maps to an existing page, update that page rather than creating a new one.
- Merge duplicates rather than creating parallel pages.

### Source Classification Tags

Items in `new-sources.md` use these tags: `tool` · `framework` · `provider` · `paper/article` · `tutorial/guide` · `benchmark/eval` · `infrastructure` · `analysis`

### Daily Intake Log Format

New-source intake is daily-file based:

- Index: `docs/new-sources.md`
- Daily files: `docs/new-sources/YYYY-MM-DD.md`
- Required table header:
  - `Title | URL | Tags | Status | Canonical Page | Notes`
- Allowed statuses:
  - `new`, `integrated`, `duplicate`, `needs-more-info`, `low-confidence`

Validation is enforced by `scripts/validate_new_sources.py` in CI.

## Naming Conventions
- **Tags (Paperless)**: `kebab-case`. Lowercase only. Prefix status tags with `s:` and category tags with `c:`.
- **Workflows (n8n)**: `[Trigger Source] -> [Primary Action]`. Example: `IMAP -> Paperless Intake`.
- **Prompts**: Versioned using SemVer. Store as Markdown files in `reference-implementations/llm-prompts/`.

## Document Lifecycle States
1.  **Ingested**: Raw file received by the system.
2.  **OCRed**: Searchable layer added (via [OCRmyPDF](./tools/process_understanding/ocrmypdf.md)).
3.  **Classified**: Assigned a document type and category tags.
4.  **Actioned**: Any extracted tasks/events have been synced to external systems.
5.  **Archived**: Document is moved to long-term storage or its final tag state.

## Minimal Metadata Schema
Every document processed by AI should attempt to populate:
- `extraction_date`: ISO8601 of when AI ran.
- `source_origin`: Email, Scan, Webhook.
- `action_required`: Boolean.
- `due_date`: If applicable.
- `confidence_score`: 0.0 to 1.0 (from LLM).

## Interoperability
- **Data Format**: All cross-tool communication should prefer **JSON**.
- **Dates**: Always use **ISO8601** with UTC offsets.
- **IDs**: Use the internal ID of the source system (e.g. Paperless `document_id`) in the metadata of the destination system (e.g. GCal event description).

## What "Done" Means
An automated flow is considered "done" when:
1.  The primary action is completed (Event created/Task synced).
2.  The source document is updated with a `processed` or `actioned` tag.
3.  No errors were logged in the orchestration engine (n8n).
4.  If a critical failure occurred, a notification was sent to a human review channel.

## AI-Authored Documentation Metadata (Required)

For AI-authored updates to knowledge pages (`docs/tools/`, `docs/services/`, `docs/knowledge_base/`, `docs/architecture/`, `docs/playbooks/`, and `docs/reference-implementations/`), include:

- `Last reviewed`: ISO date (`YYYY-MM-DD`)
- `Confidence`: `high`, `medium`, or `low`
- `Sources / References`: at least one URL

Recommended section format:

```md
## Sources / References
- [Official docs](https://example.com)

## Contribution Metadata
- Last reviewed: 2026-02-25
- Confidence: medium
```

These requirements are enforced by `scripts/check_docs_contract.py` in pull-request CI.
