# Home-Office Automation & AI Hub

A structured, agent-maintained knowledge repository for building and operating a privacy-first home-office automation stack.

## What You Will Find Here

- Canonical docs for AI tools, self-hosted services, and orchestration patterns.
- Practical playbooks for recurring workflows.
- Architecture maps and data-flow documentation.
- Automated intake and maintenance workflows that continuously expand the knowledge base.

## Repository Map

| Section | Path | What it contains | Start here if you need to... |
| :--- | :--- | :--- | :--- |
| Documentation home | [`docs/index.md`](docs/index.md) | The MkDocs landing page and high-level navigation. | Understand the full docs structure quickly. |
| Tool catalogue | [`docs/tools/`](docs/tools/) | Canonical pages for AI tools, frameworks, providers, agents, infra, and benchmarking. | Compare tooling options or add a new tool page. |
| Self-hosted services | [`docs/services/`](docs/services/) | Service-level docs for the homelab stack (storage, automation, media, networking). | Deploy or evaluate a self-hosted component. |
| Knowledge base | [`docs/knowledge_base/`](docs/knowledge_base/) | Cross-cutting concepts: MCP/ACP, model classes, RAG, security, and landscape overviews. | Learn the underlying concepts before implementation. |
| Playbooks | [`docs/playbooks/`](docs/playbooks/) | Step-by-step operational runbooks. | Execute a concrete workflow end-to-end. |
| Reference implementations | [`docs/reference-implementations/`](docs/reference-implementations/) | Reusable prompts, mapping rules, and workflow exports. | Reuse proven templates/config patterns. |
| Architecture | [`docs/architecture/`](docs/architecture/) | Component map, flow diagrams, governance, and automation model. | Understand how systems connect and why. |
| Intake queue | [`docs/new-sources.md`](docs/new-sources.md) | Source ingestion process plus dated logs under `docs/new-sources/`. | Track what is new, pending, and integrated. |
| Standards | [`docs/standards.md`](docs/standards.md) | Taxonomy, canonical-page rules, and documentation contract. | Validate structure before opening a PR. |
| Contribution workflow | [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | Human + agent contribution requirements and quality gates. | Contribute safely without breaking repo contracts. |
| Agent operating guide | [`AGENTS.md`](AGENTS.md) | Durable rules/checklists for autonomous LLM agents working in this repo. | Run maintenance work with consistent outputs. |
| Agent skills guide | [`skills.md`](skills.md) | Reusable task patterns for intake, docs updates, and quality checks. | Execute recurring tasks with low variance. |

## Recommended Entry Points

- New maintainer: [`docs/index.md`](docs/index.md)
- New contributor: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)
- LLM/automation agent: [`AGENTS.md`](AGENTS.md) then [`skills.md`](skills.md)
- Architecture review: [`docs/architecture/README.md`](docs/architecture/README.md)
- Tool selection: [`docs/knowledge_base/ai_tooling_landscape.md`](docs/knowledge_base/ai_tooling_landscape.md)

## Utility Commands

```bash
# List all known tools/services from the catalog
python3 scripts/compare_agents.py list

# Open the canonical documentation path for a tool id
python3 scripts/compare_agents.py doc paperless-ngx

# Validate catalog/nav consistency before a docs PR
python3 scripts/check_catalog_consistency.py
```

## Project Scope

This repository is optimized for long-term maintainability:

- One canonical page per tool/framework/provider.
- Cross-linked documentation with stable taxonomy.
- CI quality gates for catalog consistency and docs contract compliance.
- Scheduled GitHub workflows for source intake and backlog processing.
