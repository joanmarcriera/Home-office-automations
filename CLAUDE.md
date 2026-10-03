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

5. **Odd-day chained pipeline (2026-09-25, chained 2026-10-03)** — every even day of the month has zero scheduled jobs. `odd-day-pipeline.yml` is the ONLY daily cron (`30 0 1-31/2 * *`); every maintenance lane exposes `workflow_call` and runs as a `needs:` chain in dependency order (hygiene → Jules watcher/backlog → digest → intake bridge → weekly producers → issue openers → link check). Weekly lanes run on fixed odd days of the month picked by the pipeline's `plan` job (1,7,13,19,25 growth+pricing · 3,9,15,21,27 coverage · 5,11,17,23,29 links); the rollup merge keeps its own retry cron on 1,7,13,19,25. Never combine day-of-month and day-of-week in a cron (GitHub ORs them). Reusable workflows, not `workflow_run`: GitHub caps `workflow_run` chains at 3 levels. The health watchdog runs via `workflow_run` after the pipeline and derives stall thresholds from the largest gap between scheduled days (`1-31/2` → 4 days). Month ends give two consecutive active days (31st → 1st) — accepted. To add a scheduled lane: give it `workflow_call` and add a job to the pipeline instead of a new cron.

## Skills (use instead of manual work)

- `/knowledge-base-update` — Process `docs/new-sources.md` intake queue into canonical docs.
- `/new-tool-doc <name> <category>` — Scaffold new tool page from template.

## Primary maintenance docs

- `AGENTS.md` — Non-negotiable rules for agents working here.
- `skills.md` — Reusable task patterns + required checks per skill.
- `docs/CONTRIBUTING.md` — Human + agent contribution gates.
- `docs/standards.md` — Taxonomy, canonical-page contract, validation rules.
