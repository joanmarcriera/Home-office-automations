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
5. **Bot-PR detection has ONE definition: `scripts/ci/trusted_actor.py`.** Every
   "is there an open bot PR / control issue?" lookup goes through
   `trusted_actor.py list prs|issues ...` (or `list_trusted()` from Python), which
   queries GitHub once per trusted author (`--author`), so outsiders' items never
   enter the result window: they cannot push a real control issue off the page
   or inflate a count. Never fail closed on a count that includes untrusted
   items. Query bots as `github-actions[bot]` — `app/github-actions` silently
   matches nothing in `gh issue list --author` without `--search`/`--label`.
   Identity decides first — author is the repo owner or a known bot
   (`github-actions`, `google-labs-jules`, only in the app forms GitHub sets) and,
   for PRs, `isCrossRepository == false` (not a fork) — then the title/body/
   label/branch heuristic classifies what is left. Title or branch name alone is
   forgeable by anyone and used to let outsiders pause lanes or reach the
   auto-merger. Users: `jules-auto-merge`, `pr-hygiene`, `weekly-automation-rollup-merge`,
   the three throttle lanes, `api-pricing-maintenance`, `issue-automation-router`
   and `jules_issue_watcher.py` (outsiders' issues are no longer auto-queued for
   Jules — label them by hand), `automation_health.py` (rollup flow). Change the
   heuristic or the bot list there, never inline; tests in
   `scripts/ci/test_trusted_actor.py`.
6. **Throttles must ignore CONFLICTING PRs.** Counting an un-mergeable orphan
   stalls the lane forever. Count only live PRs (fetch `mergeable` per-PR; skip
   `CONFLICTING`). `pr-hygiene.yml` closes the orphans in parallel.
7. **Bash gotchas that bit us:** never put backticks in a double-quoted `--body`
   string (command substitution → step fails under `set -euo pipefail`; single-quote
   it). A `while read` loop after a pipe runs in a subshell, so counters don't
   survive — use process substitution `done < <(...)`.
8. Pushes/PRs made with the default `GITHUB_TOKEN` start NO `on: push` /
   `on: pull_request` workflows (newer GitHub creates them as `action_required`
   runs needing approval). Required checks on bot PRs are satisfied by
   dispatching the gate workflows on the PR branch
   (`scripts/dispatch_pr_gate_workflows.py`): the `workflow_dispatch` check runs
   report `knowledgeops-contract` / `link-check` on the head commit, which is what
   the ruleset requires. `daily-digest` and `weekly-planner` open the PR with
   `AUTOMATION_PAT || GITHUB_TOKEN` (see `.github/automation-token-setup.md`);
   don't spread that PAT further, approve runs by API, or use `--admin` to get
   past the approval gate — the dispatched gate runs are the mechanism. Likewise a bot merge never triggers
   `deploy-docs.yml` on push — the pipeline's last lane deploys, and
   `jules-auto-merge.yml` dispatches a deploy after merging.
9. **No new crons.** Scheduled work runs on odd days of the month only, from ONE
   entry point: `odd-day-pipeline.yml`. A new lane gets `on: workflow_call` (plus
   `workflow_dispatch`) and a job in the pipeline with `needs: [<previous lane>]`
   and `if: ${{ !cancelled() }}`, plus a `permissions:` block covering what the
   lane needs. Weekly lanes go in the `plan` job's odd day-of-month lists. Never
   restrict both day-of-month and day-of-week (cron ORs them), and do not chain
   lanes with `workflow_run`, which GitHub stops after three levels.
10. **Every lane supports dry run.** Lanes take a boolean `dry_run` input on both
   `workflow_call` and `workflow_dispatch`; set `DRY_RUN: ${{ inputs.dry_run &&
   'true' || 'false' }}` on the job, run `bash scripts/ci/install_gh_dry_run_shim.sh`
   after checkout when it is true (it turns every mutating `gh` call into a log
   line), and guard git pushes / `create-pull-request` with `env.DRY_RUN != 'true'`.
   Test changes end to end with
   `gh workflow run odd-day-pipeline.yml --ref <branch> -f weekly_lanes=all -f dry_run=true`.
11. **Event lanes use JOB-level concurrency.** A workflow-level group is joined by
   every triggered run, including the many `skipped` `issue_comment`/`issues`
   runs, and GitHub keeps only one pending run per group — a burst can cancel the
   pipeline's queued call. Put the group on the job, below its `if:`.
12. **Gates read trusted state only and fail closed.** Dedupe/throttle checks
   count only PRs/issues from trusted actors (see 5; outsiders can open
   look-alike titles) and, if the lookup errors or looks truncated, create
   nothing and exit non-zero (`weekly_planner.py` and `trusted_actor.py` exit 2)
   rather than assume "nothing open" — the failed lane is what the watchdog
   reports and reruns. Unit tests: `scripts/test_weekly_planner.py`,
   `scripts/test_prune_stale_branches.py`, `scripts/ci/test_trusted_actor.py`
   (run by `automation-script-tests.yml`).
13. **Credential hygiene.** Never execute code from a non-main branch in a job
   holding a write token: check out with `persist-credentials: false`, merge
   other branches in a separate worktree, and give git the token per command
   (`git -c 'credential.helper=!gh auth git-credential' push ...`).

### 5) Issue-to-PR Resolver

1. Confirm issue scope and acceptance criteria.
2. Implement minimal, testable change.
3. Link PR with `Fixes #<issue>` when appropriate.
4. Merge only after required checks pass.

### 6) Branch Janitor

Remote branches are pruned by the `branch-cleanup.yml` lane of the odd-day
pipeline (`scripts/prune_stale_branches.py`). It is REPORT-ONLY until the repo
variable `BRANCH_CLEANUP_LIVE` is `true` (cap per run: `BRANCH_CLEANUP_MAX`,
default 50). It deletes only branches fully merged into `main` or whose own PR
(same head repo + ref) is merged/closed with the tip unchanged, never `main`,
`gh-pages`, `automation/*`, open-PR heads/bases or tips younger than 3 days,
and deletes by compare-and-swap on the evaluated SHA.

1. Read the lane's "Branch cleanup" step summary for the candidate count.
2. Manual one-off: `python3 scripts/prune_stale_branches.py` (dry run) — add
   `--apply` only with the owner's go-ahead; bulk deletion is destructive.
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

The watchdog (`automation-health.yml`, chained via `workflow_run` after
`odd-day-pipeline.yml` completes, plus a dead-man cron at 12:45 UTC on days
3,11,19,27 in case the pipeline itself stops) scans every scheduled
lane (a failed pipeline run names the failed lane jobs), auto-reruns a failed run's failed jobs once, and maintains ONE
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
6. It only judges runs on `main` from `schedule` / `workflow_dispatch` /
   `workflow_run`, ignoring `skipped` placeholders, so branch test dispatches and
   event noise never raise (or auto-rerun) anything.

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
