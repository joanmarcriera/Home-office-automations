# skills.md

Practical skill patterns for LLM agents maintaining this repository.

## How to Use This File

Pick the skill that matches your task. Execute its steps in order. Apply the listed checks before opening or merging a PR.

## Skill Catalogue

| Skill | Use when | Typical files touched | Required checks |
| :--- | :--- | :--- | :--- |
| **Intake Integrator** | Processing newly discovered sources into canonical docs. | `docs/new-sources.md`, `docs/new-sources/*.md`, `docs/tools/**`, `docs/services/**`, `data/all_tools.json`, `mkdocs.yml` | `validate_new_sources`, `check_catalog_consistency` |
| **Canonical Doc Updater** | Improving an existing tool/service/knowledge page. | `docs/tools/**` or `docs/services/**` or `docs/knowledge_base/**` | `check_docs_contract` |
| **Navigation Maintainer** | Any doc move/add/remove that affects docs nav. | `mkdocs.yml`, related docs pages | YAML parse, `check_catalog_consistency` |
| **Workflow Maintainer** | Adjusting schedules, issue automation, CI behavior. | `.github/workflows/**`, optional `scripts/**` | Validate YAML, confirm workflow logic via `gh run` |
| **Issue-to-PR Resolver** | Converting open issues into merged fixes. | Issue-specific files + branch/PR metadata | Relevant repo checks + green PR status checks |
| **Branch Janitor** | Post-merge cleanup of remote/local branches and stale PR refs. | Git branches/PR state | Verify open PR list and branch list after cleanup |

## Skill Playbooks

### 1) Intake Integrator

1. Read `docs/new-sources.md` and pending daily logs.
2. For each `new` row, locate canonical page or create one from template.
3. Update links/status to `integrated`.
4. If new canonical page: update `data/all_tools.json` and `mkdocs.yml`.
5. Run checks.

### 2) Canonical Doc Updater

1. Confirm canonical page already exists.
2. Improve sections with concrete technical detail.
3. Maintain metadata (`Last reviewed`, `Confidence`, `Sources / references`).
4. Run docs contract checks.

### 3) Navigation Maintainer

1. Apply nav changes in `mkdocs.yml`.
2. Keep section ordering and naming consistent.
3. Validate YAML and catalog consistency.

### 4) Workflow Maintainer

1. Keep workflow steps idempotent.
2. Add duplicate-prevention guards for scheduled issue creation.
3. Ensure minimum required permission scopes.
4. Trigger and verify a run when practical.

### 5) Issue-to-PR Resolver

1. Confirm issue scope and acceptance criteria.
2. Implement minimal, testable change.
3. Link PR with `Fixes #<issue>` when appropriate.
4. Merge only after required checks pass.

### 6) Branch Janitor

1. Confirm no open PR depends on target branches.
2. Delete merged remote branches except protected deployment branches.
3. Prune local refs and verify clean state.

## Completion Template

When finishing any skill, report:

1. Changed files
2. Validation commands run and results
3. Remaining risks or follow-up items
