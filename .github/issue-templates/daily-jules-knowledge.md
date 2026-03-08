## Daily Knowledge Expansion - @jules

Objective: make the repo better on every run by extending or improving documentation. Prefer FREE/open AI tools when possible and keep broad awareness of trending AI ecosystem tools.

Open **ONE PR** only.

## Non-negotiable guardrails

1. Additive-only changes:
   - Do NOT delete files, sections, or registry entries.
   - Do NOT remove existing tools/content unless explicitly asked in a human-authored issue.
2. Minimize overlap:
   - Before editing a file, check if it changed in the last 24h:
     `git log --since="24 hours ago" --name-only --pretty=format: | sort -u`
   - Prefer files not touched recently.
3. Metadata discipline:
   - Do NOT update `Last reviewed` / `Confidence` unless that file has substantive content changes.
4. Stay small and mergeable:
   - Max 6 files changed per run.
   - Max 1 intent/lane per PR.
5. Rebase before push:
   - `git fetch origin main && git rebase origin/main`

---

## Work selection ladder (pick first lane that has real work, then stop)

### Lane A - User issue first (highest priority)

If there are open human-authored issues labeled `jules` (excluding daily automation issues), resolve exactly one.

- Include `Fixes #<issue-number>` in PR body.
- Do only the scoped work from that issue.

If no such issue exists, go to Lane B.

### Lane B - Intake integration

Process up to 3 `new` rows from `docs/new-sources/YYYY-MM-DD.md`.

For each row:
1. Deduplicate against canonical docs in `docs/tools/` and `docs/services/`.
2. If canonical exists, enrich it with source-backed updates and mark row `integrated`.
3. If canonical does not exist, create it using templates and taxonomy, then update:
   - `data/all_tools.json` (if tool/framework/provider)
   - `mkdocs.yml` nav
4. Keep index links in `docs/new-sources.md` as `/new-sources/YYYY-MM-DD/`.

If no `new` rows exist, go to Lane C.

### Lane C - Source refresh for trending/free AI

Pick 1 existing canonical doc focused on free/open or trending AI tools.

Add:
- 1-2 high-signal new sources (official docs/blog/release notes preferred)
- a short “What changed” update section with concrete technical changes

Do not rewrite the full page.

If no strong source update is found, go to Lane D.

### Lane D - Depth improvements for shallow docs

Use `data/growth-metrics.json` → `shallow_docs`.
Pick up to 2 docs that still lack practical depth and add:
- `## Getting started` with runnable commands
- `## CLI examples` (if CLI exists)
- `## API examples` (if API/SDK exists)

No placeholder snippets (`...`), no pseudo-commands.

If no suitable docs exist, go to Lane E.

### Lane E - Link and structure hardening

Fix up to 5 broken internal links or missing related-tool links in docs touched infrequently.
Do not do mass reformatting.

---

## Required checks before opening PR

Run all:

1. `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
2. `python3 scripts/validate_new_sources.py`
3. `python3 scripts/check_catalog_consistency.py`
4. `CHANGED_DOCS=$(git diff --name-only origin/main...HEAD | grep '^docs/.*\\.md$' || true); if [ -n \"$CHANGED_DOCS\" ]; then python3 scripts/check_docs_contract.py $CHANGED_DOCS; fi`

If any check fails, fix the PR before opening.

## PR requirements

- Title: `docs: daily knowledge expansion YYYY-MM-DD HHMM UTC`
- Body must include:
  - Selected lane (A/B/C/D/E)
  - Files changed and why
  - Validation commands executed
  - If Lane A: `Fixes #<issue-number>`
