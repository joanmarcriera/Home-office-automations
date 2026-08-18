# Tool Catalogue

Canonical documentation for every AI tool, framework, provider, agent, and infrastructure component used in or evaluated for this stack. One page per tool — no duplicates.

## Current Sections

| Directory | Category label | What lives here |
| :--- | :--- | :--- |
| [ai_knowledge/](ai_knowledge/index.md) | AI & Knowledge | LLM interfaces, knowledge bases, creative AI, local model frontends |
| [agents/](agents/index.md) | Agents | Autonomous coding and task agents (Jules, Claude Code, Goose, Superpowers, etc.) |
| [automation_orchestration/](automation_orchestration/index.md) | Automation & Orchestration | MCP servers (FastMCP 3.1), workflow connectors, browser automation |
| [benchmarking/](benchmarking/index.md) | Benchmarking | LLM evaluation suites, leaderboards, multi-language coding harnesses (Inspect AI, MultiPL-E, etc.) |
| [development_ops/](development_ops/index.md) | Development & Ops | AI coding assistants, DevOps tooling, documentation tools (OpenCode, MkDocs, etc.) |
| [frameworks/](frameworks/index.md) | Frameworks | LLM application frameworks (LangChain, LlamaIndex, Dify, AutoGen, etc.) |
| [infrastructure/](infrastructure/index.md) | Infrastructure | Inference engines, vector stores, proxies, fine-tuning suites (vLLM, SGLang, Qdrant, PEFT, TensorRT-LLM, Triton) |
| [providers/](providers/index.md) | Providers | API and cloud AI providers (OpenAI, Anthropic, Google AI Studio, Azure AI Search, DeepSeek, etc.) |
| [calendar_tasks/](calendar_tasks/index.md) | Calendar & Tasks | Time management, scheduling, CalDAV integrations |
| [intake_storage/](intake_storage/index.md) | Intake & Storage | Standard protocols and storage tools (CalDAV, MinIO, S3, etc.) |
| [process_understanding/](process_understanding/index.md) | Process & Understanding | Document analysis, OCR, web crawling, observability (Crawl4AI, Docling, Prometheus, Tempo, Logfire, Grafana) |
| [orchestration/](orchestration/index.md) | Orchestration | Workflow engines and data pipeline tools (Temporal, Airflow, Dagster, Kestra, etc.) |
| [enterprise/](enterprise/index.md) | Enterprise AI | Workplace-specific productivity suites, identity, and search (Glean, Hebbia, Okta, Proton Mail, etc.) |

> **Note on taxonomy drift**: `automation_orchestration/` and `orchestration/` currently coexist. Per [standards.md](../standards.md), `orchestration/` is the canonical location for workflow DAG/pipeline engines. New orchestration tool pages go there; `automation_orchestration/` content focuses on MCP protocols and agent integration harnesses.

> **Self-hosted services** (Paperless-ngx, n8n, Nextcloud, Ollama, etc.) live in [Services](../services/README.md) — they carry operational deployment context alongside tool documentation.

---

## How to Find the Right Tool

**I need to automate a multi-step task** → [Automation & Orchestration](automation_orchestration/index.md), [Orchestration](orchestration/index.md), or [Playbooks](../playbooks/index.md)

**I need to run a model locally** → [Infrastructure](infrastructure/index.md) or [Services → Ollama](../services/ollama.md)

**I need an LLM-powered app framework** → [Frameworks](frameworks/index.md)

**I need to pick an API provider** → [Providers](providers/index.md) and [Knowledge Base → Model Routing Guide](../knowledge_base/model_routing_guide.md)

**I need an autonomous agent to write code** → [Agents](agents/index.md)

**I need to evaluate or compare models** → [Benchmarking](benchmarking/index.md) and [Knowledge Base → Model Comparison](../knowledge_base/model_comparison_and_evaluation.md)

**I need to ingest or process documents** → [Process & Understanding](process_understanding/index.md) or [Services → Paperless-ngx](../services/paperless-ngx.md)

---

## Catalogue Rules

Every page must follow the [standard template](../templates/tool_template.md) with these required sections:

`## What it is` · `## What problem it solves` · `## Where it fits in the stack` · `## Typical use cases` · `## Strengths` · `## Limitations` · `## When to use it` · `## When not to use it` · `## Related tools / concepts` · `## Sources / references`

AI-authored pages must also carry:

```
## Sources / References
- [Official docs](https://example.com)

## Contribution Metadata
- Last reviewed: YYYY-MM-DD
- Confidence: high | medium | low
```

See [Standards](../standards.md) for the full taxonomy and dedup policy, and [Contributing](../CONTRIBUTING.md) for how to add a new tool page.

## Sources / References
- [Standards](../standards.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
