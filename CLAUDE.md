# Claude Code — Project Memory

## Project purpose

**Home-Office Automation & AI Hub**: A production-grade, agent-maintained knowledge repository documenting home-lab automation, privacy-first AI stack (Ollama, n8n, Paperless-ngx), and orchestration patterns. Published as live docs at [ai.riera.co.uk](https://ai.riera.co.uk) via MkDocs + GitHub Pages.

**1700+ commits, actively maintained** — CI infrastructure ensures catalog consistency, validates doc contracts, processes source intake, and upgrades documentation via automated workflows.

## How to run/test

```bash
# Validate docs contract and catalog consistency (run before opening PRs)
python3 scripts/check_catalog_consistency.py
python3 scripts/validate_new_sources.py

# Validate mkdocs.yml (auto-run on edits via hook)
python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"

# Build docs locally
mkdocs serve          # Runs on http://localhost:8000
```

## Repository structure

| Path | Purpose |
|------|---------|
| `docs/tools/` | Canonical tool documentation (AI, frameworks, providers, agents, infra, benchmarking) |
| `docs/services/` | Self-hosted service docs (storage, automation, media, networking) |
| `docs/knowledge_base/` | Conceptual: MCP/ACP, model classes, RAG, security, landscape overviews |
| `docs/playbooks/` | Step-by-step operational runbooks |
| `docs/architecture/` | Infrastructure diagrams, component maps, data flows |
| `data/all_tools.json` | Catalog index (sync manually with docs when adding tools) |
| `AGENTS.md` | Non-negotiable rules for autonomous agent work on this repo |
| `skills.md` | Reusable task patterns (Intake Integrator, Doc Updater, Workflow Maintainer, etc.) |
| `.github/workflows/` | Scheduled: weekly rollup producer, API pricing maintenance, digest ingestion, ralph-loop batch processing, automation health watchdog |
| `scripts/` | Utilities: consistency checks, link fixing, doc freshness auditing, catalog validation |

## Key conventions

- **One canonical page per tool** — no duplicates; search before creating.
- **Taxonomy enforcement** — tool pages must live in `docs/tools/<category>/`; validate before merge.
- **Doc contract** — required sections: What it is, problem it solves, strengths, limitations, sources.
- **mkdocs.yml** — any add/move/rename triggers validation hook; check YAML syntax + nav consistency.
- **Intake process** — new sources land in `docs/new-sources.md`, processed via `knowledge-base-update` skill and `validate_new_sources.py`.

## Active hooks (.claude/settings.json)

- **PostToolUse**: Validates mkdocs.yml YAML syntax after edits.
- **PreToolUse**: Blocks direct workflow file edits (require explicit user confirmation).

## Gotchas from recent commits

1. **Rollup PR preservation** — Multiple CI lanes share `automation/weekly-rollup` branch. Recent fix: lanes must merge pending work before their own changes, or the rollup PR closes with lost work.
2. **Stale model slugs** — OpenRouter free-model IDs change frequently; `fix(ai): replace dead slugs` fix applied across all workflows (2026-09-05).
3. **Jules worker retirement** — `julep-sprint-workers` lane deprecated; use `digest-ingestion` + `knowledge-base-update` instead.
4. **Watchdog escalation** — New automation health watchdog flags unmerged rollup PRs; confirms throttles are active before closure.

## Skills (use instead of manual work)

- `/knowledge-base-update` — Process `docs/new-sources.md` intake queue into canonical docs.
- `/new-tool-doc <name> <category>` — Scaffold new tool page from template.

## Primary maintenance docs

- `AGENTS.md` — Non-negotiable rules for agents working here.
- `skills.md` — Reusable task patterns + required checks per skill.
- `docs/CONTRIBUTING.md` — Human + agent contribution gates.
- `docs/standards.md` — Taxonomy, canonical-page contract, validation rules.
