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
| **Unattended Pipeline Triage** | Board piled up or Jules pipeline stalled (conflicting orphan PRs, stale control issues). | `.github/workflows/**`, open PRs/issues | `gh pr list` mergeable states; confirm throttles + pr-hygiene |
| **Coverage Self-Evolution** | Expanding coverage toward the frontier; clearing dangling links. | `data/frontier_watchlist.json`, `data/all_tools.json`, `docs/**` | `coverage_gap_scan.py`, `fix_internal_links.py`, `check_catalog_consistency` |
| **Superpowers** | High-level agent orchestration and skill management. | `.claude/skills/`, `.claude/agents/` | Verify skill discovery and execution. |
| **Documentation Writer** | Automated generation and maintenance of project docs. | `docs/**`, `README.md` | Run `check_docs_contract`. |
| **Grill-me** | Rigorous cross-examination and verification of plans. | Issue/Task context | Confirm robust plan before execution. |
| **Everything Claude Code** | Production-ready setup with security scanning and research-first development. | `.claude/config.json`, `CLAUDE.md`, hooks | Run security and consistency checks. |
| **last30days-skill** | Weekly AI ecosystem news summarization and skill gap analysis. | Scheduled tasks, knowledge base | Verify summary accuracy and source links. |
| **Claude How-To** | Hand-on guides for advanced agentic workflows and MCP. | Documentation, configuration examples | Confirm step-by-step reproducibility. |
| **UI Prototyping** | Production-grade frontend generation. | `frontend/**`, `src/components/**` | Lint check, accessibility scan |
| **Web Automation** | Live web research and multi-site orchestration. | `docs/research/**`, `.claude/session.log` | Verify URL reachability, content extraction quality |
| **Autonomous Security** | Automated pen-testing and vulnerability scanning. | `src/**`, `package.json`, `.github/workflows/**` | Run security audit, verify no new vulnerabilities |
| **Code Refinement** | Architectural simplification and quality reviews. | `src/**`, `docs/architecture/**` | Maintain test coverage, run complexity analysis |
| **Automation Health Triage** | A lane is failing/stalled, or the `automation-health` issue is open. | `.github/workflows/automation-health.yml`, `scripts/automation_health.py` | Dry-run the watchdog, confirm issue reflects reality |

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
4. Trigger and verify a run when practical. To exercise an edited version of an
   already-registered workflow without merging, dispatch it on the branch:
   `gh workflow run "<name>" --ref <branch>` (a `workflow_dispatch` workflow that
   exists *only* on a feature branch is NOT triggerable until it lands on the
   default branch).
5. **Bot-PR detection must have ONE definition.** The "is this a Jules/automation
   PR" heuristic (title/body/label/branch-regex) is duplicated across
   `jules-auto-merge`, `pr-hygiene`, and the three throttle lanes
   (`process-jules-backlog`, `daily-jules-knowledge`, `daily-jules-maintenance`,
   `jules-sprint-workers`). If you change one, change ALL of them — drift means
   PRs get throttle-counted but never auto-merged (a silent pileup). Current token
   set includes `jules|...|ralph-loop|freshness-audit|audit-batch|batch-`.
6. **Throttles must ignore CONFLICTING PRs.** Counting an un-mergeable orphan
   stalls the lane forever. Count only live PRs (fetch `mergeable` per-PR; skip
   `CONFLICTING`). `pr-hygiene.yml` closes the orphans in parallel.
7. **Bash gotchas that bit us:** never put backticks in a double-quoted `--body`
   string (command substitution → step fails under `set -euo pipefail`; single-quote
   it). A `while read` loop after a pipe runs in a subshell, so counters don't
   survive — use process substitution `done < <(...)`.
8. PRs opened by the default `GITHUB_TOKEN` do NOT trigger `on: pull_request`
   checks. For `peter-evans/create-pull-request`, pass
   `token: ${{ secrets.AUTOMATION_PAT || secrets.GITHUB_TOKEN }}`.

### 5) Issue-to-PR Resolver

1. Confirm issue scope and acceptance criteria.
2. Implement minimal, testable change.
3. Link PR with `Fixes #<issue>` when appropriate.
4. Merge only after required checks pass.

### 6) Branch Janitor

1. Confirm no open PR depends on target branches.
2. Delete merged remote branches except protected deployment branches.
3. Prune local refs and verify clean state.

### 7) Staff Reviewer Pattern (Meta-Skill)

1. When a plan is proposed, spin up a secondary agent context.
2. The secondary agent must "grill" the plan, looking for edge cases, security flaws, or over-engineering.
3. Refine the plan based on feedback until both contexts reach consensus.

### 8) Context Isolation Pattern (Meta-Skill)

1. For high-compute reasoning or tasks requiring many file reads (50+), use subagents.
2. The main session should only receive the final conclusion or artifacts from the subagent.
3. Use `/compact` aggressively in the subagent session to manage token rot.

### 9) Code Refinement

1. Identify complex or redundant code paths using complexity analysis tools.
2. Propose architectural simplifications that maintain existing behavior.
3. Implement changes surgically, matching the surrounding style exactly.
4. Verify no regressions using existing test suites.

### 10) Unattended Pipeline Triage

Use when the issue/PR board has piled up or the Jules pipeline looks stalled.

1. **Diagnose, don't bulk-act.** List open PRs with `mergeable` state. The classic
   failure is parallel batch branches editing overlapping docs → only one merges,
   the rest become permanently `CONFLICTING` orphans. Before closing, confirm the
   target file already got an equivalent change on `main` (same-day sibling branch).
2. Close superseded orphans with an explanatory comment. Do NOT `--delete-branch`
   without explicit owner authorization (it's destructive); `pr-hygiene.yml` handles
   branch deletion going forward.
3. Fix the *cause*, not just the symptom: ensure `pr-hygiene` runs, all throttles are
   conflict-aware, and the bot-PR regex is consistent (see Workflow Maintainer #5–6).
4. The repo is PUBLIC → Actions minutes are free; the real free-tier ceiling is the
   **Jules daily task quota**. The pipeline is sequential & self-throttling (a lane
   creates work only when no live PR and no same-type issue is open; a merge triggers
   the next issue). Preserve that pacing — don't add unthrottled issue-creating lanes.
5. Stale singleton control issues (`Daily Maintenance Run -`, etc.) expire by age via
   `cleanup-automation-issues.yml`; don't close them by hand unless clearly abandoned.

### 11) Coverage Self-Evolution

Use to make the bots EXPAND coverage toward the industry frontier, not just re-audit.

1. `data/frontier_watchlist.json` is the offline, in-repo "where the industry is going"
   signal. Add entries (with `aliases` to avoid false gaps) as the landscape shifts.
2. `scripts/coverage_gap_scan.py` diffs the watchlist against `data/all_tools.json` and
   reports frontier gaps + dangling `Related tools` links + thin categories;
   `--create-issue` opens ONE throttled gap-fill issue. Runs weekly via
   `coverage-gap-scan.yml`. An entry stops being flagged once it's catalogued.
3. For broken internal links, run `scripts/fix_internal_links.py` (dry-run first; it
   only rewrites unambiguous unique-basename matches). `lychee` runs `fail: false`, so
   internal link rot is otherwise silent.
4. Route large content work (playbooks, missing hub pages) through `jules`-labelled
   issues / the watchlist rather than hand-authoring — that's what the pipeline is for.

### 12) Automation Health Triage

The watchdog (`automation-health.yml`, daily 05:40 UTC) scans every scheduled
lane, auto-reruns a failed run's failed jobs once, and maintains ONE
`automation-health`-labelled issue (updated in place, auto-closed when green).

1. Read the open `Automation health:` issue — it lists which lanes fail/stall and why.
2. A `❌ latest run concluded failure` after "already rerun once" means the failure is
   NOT transient: open the run log and fix the root cause; do not just re-dispatch.
3. A `💤`/stalled or `disabled_*` lane means the schedule itself stopped — re-enable the
   workflow (`gh workflow enable <file>`) or fix/retire the lane.
4. Never add `jules`/`autofix` to the health issue; it is a report, not bot work
   (the router skips it by label and title).
5. Verify a fix with `python3 scripts/automation_health.py --dry-run`, then let the next
   scheduled scan close the issue itself.

Lesson learned (2026-07): `jules-sprint-workers.yml` hit its hardcoded
`SPRINT_END` (2026-06-07) and silently no-oped every 4 hours for five weeks —
retired along with `scripts/open_jules_sprint_issues.py` (both recoverable from
git history for the next sprint). Time-bounded lanes must fail LOUDLY when
their window lapses; the watchdog now exists to surface that class of death.

## Completion Template

When finishing any skill, report:

1. Changed files
2. Validation commands run and results
3. Remaining risks or follow-up items

## Sources / references

- [Superpowers](https://github.com/obra/superpowers)
- [Documentation Writer Skill](https://skills.sh/github/awesome-copilot/documentation-writer)
- [Grill-me Skill](https://github.com/mattpocock/skills/blob/main/grill-me/SKILL.md)
- [Claude Skills Ecosystem](docs/tools/agents/claude-skills-ecosystem.md)
- [Claude Code Best Practices](docs/tools/development_ops/claude-code.md)
