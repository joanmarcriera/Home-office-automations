# AGENTS.md

Repository-wide operating contract for autonomous or assisted LLM agents.

## Objective

Maintain this repository as a reliable, canonical knowledge base for home-office automation and AI tooling.

## Non-Negotiable Rules

1. Keep **one canonical page per tool/topic**. Never create duplicates.
2. Follow taxonomy and structure in [`docs/standards.md`](docs/standards.md).
3. When adding a new tool/framework/provider page, update both:
   - `data/all_tools.json`
   - `mkdocs.yml` navigation
4. Preserve required metadata for AI-authored docs:
   - `Last reviewed` (`YYYY-MM-DD`)
   - `Confidence` (`high|medium|low`)
   - `Sources / references`
5. Do not submit PRs with unresolved conflicts, broken nav links, or catalog mismatches.

## Section Ownership Map

- `docs/tools/`: canonical tool documentation
- `docs/services/`: self-hosted services documentation
- `docs/knowledge_base/`: concepts, patterns, ecosystem overviews
- `docs/playbooks/`: executable operational guides
- `docs/reference-implementations/`: reusable artifacts/templates
- `docs/new-sources*`: intake queue and daily ingestion logs
- `.github/workflows/`: automation and CI behavior

## Standard Task Checklists

### A) Add or update a tool page

1. Search for existing canonical page (name + aliases).
2. Update existing page when possible; create new page only if absent.
3. Ensure required sections and metadata are complete.
4. Update `data/all_tools.json` and `mkdocs.yml` when adding new canonical pages.
5. Run checks listed in **Validation Commands**.

### B) Process intake queue (`docs/new-sources*`)

1. Work rows where `Status = new`.
2. Map each item to canonical page or create one using templates.
3. Mark rows `integrated` and update canonical links.
4. Keep daily logs structurally valid.

### C) Edit workflows or automation behavior

1. Keep schedule/trigger intent explicit in comments.
2. Add guard conditions to prevent duplicate issue/PR spam.
3. Preserve required `permissions` scopes.
4. Prefer idempotent behavior for scheduled runs.

### D) Merge and cleanup operations

1. Confirm required checks are green before merge.
2. Prefer deleting merged topic branches after merge.
3. Keep `main` and deployment branches (`gh-pages`) intact unless explicitly requested.

## Validation Commands

Run relevant checks before pushing:

```bash
python3 scripts/check_catalog_consistency.py
python3 scripts/check_docs_contract.py
python3 scripts/validate_new_sources.py
ruby -ryaml -e 'YAML.load_file("mkdocs.yml"); puts "mkdocs.yml OK"'
```

## PR Quality Bar

A good PR is:

- focused on one intent,
- structurally consistent with repository taxonomy,
- backed by source links,
- passing quality gates,
- and easy for the next agent to continue.

## Handoff Notes

When handing off work, include:

1. What changed.
2. Why it changed.
3. Which checks were run.
4. Any known follow-up tasks.
