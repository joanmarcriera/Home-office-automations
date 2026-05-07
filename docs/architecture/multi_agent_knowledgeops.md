# Multi-Agent KnowledgeOps Governance

This document defines how multiple AI agents can safely and consistently grow this repository over time without creating duplication, stale content, or low-confidence noise.

## Goal

Build a durable documentation system where many agents can contribute in parallel while preserving:

- Canonical ownership (one page per tool/topic)
- Source traceability
- Freshness and confidence signals
- Reviewability through predictable PRs

## Why this is the highest-leverage move

The main scaling risk is not "too little content", it is low-quality content growth. Without a shared operating contract, multiple agents eventually create duplicate pages, weak sourcing, and conflicting guidance. A common contract plus quality gates keeps throughput high and entropy low.

## Multi-Agent KnowledgeOps Contract (Mandatory)

All AI-authored documentation PRs must satisfy the contract below.

1. Respect canonical ownership.
   - Before creating a page, search for existing tool/topic names and aliases.
   - Update an existing canonical page when possible.
2. Use repository templates and taxonomy.
   - `docs/templates/tool_template.md` for tools/frameworks/providers.
   - `docs/templates/article_template.md` for papers/articles.
   - Place files in the taxonomy defined in `docs/standards.md`.
3. Include auditable metadata in every AI-authored knowledge page update.
   - `Last reviewed` date in ISO format (`YYYY-MM-DD`)
   - `Confidence` level (`high`, `medium`, or `low`)
   - `Sources / References` with at least one URL
4. Limit each PR to one intent.
   - Intake integration, curation pass, or audit fix.
   - Avoid mixed PRs that combine unrelated tasks.
5. Leave clear review context.
   - State what was added, why it belongs, and what was deduplicated.

## Role Model for Agents

Use role-specific behavior to reduce overlap and improve predictability.

### Intake Agent

- Scans sources and stages candidates in `docs/new-sources.md`
- Proposes canonical destination and taxonomy tags
- Does not perform broad refactors

### Curation Agent

- Integrates staged items into canonical pages
- Normalizes structure to template and standards
- Updates `data/all_tools.json` and `mkdocs.yml` when required

### Audit Agent

- Verifies metadata, links, and section completeness
- Flags stale pages for refresh
- Fixes low-risk quality issues in small PRs

## Parallel Lane Rules

When multiple agents are active at the same time, each agent must work inside a lane with an explicit file boundary.

| Lane | Primary scope | Merge risk |
| :--- | :--- | :--- |
| Intake | `docs/new-sources*`, `data/all_tools.json`, `mkdocs.yml` | High if several agents edit the same daily log or navigation block |
| Tool curation | One canonical page under `docs/tools/` or `docs/services/` | Medium if pages share related-tool links or catalog entries |
| Playbooks | One page under `docs/playbooks/` or `docs/reference-implementations/` | Low when the PR avoids shared index churn |
| Architecture / KB | One concept page under `docs/architecture/` or `docs/knowledge_base/` | Medium because cross-links can touch multiple overview pages |

Prefer one changed canonical page plus required metadata/source updates. If a task needs catalog or navigation edits, treat those files as part of the same lane and avoid opening a second PR that touches them until the first one merges.

## PR Sequencing for Automation

For autonomous sprint work:

1. Open one PR per issue or worker lane.
2. Enable automerge only after local validation has passed.
3. Wait for the merge queue or automerge workflow before opening another PR that touches overlapping files.
4. If a PR becomes conflict-dirty, do not keep piling new changes onto the branch. Rebase or replace it with a fresh branch from `main`.
5. Close or supersede duplicate branches once a newer PR has already landed the same issue scope.

This keeps the repository moving without turning `main`, `mkdocs.yml`, or `data/all_tools.json` into shared conflict points.

## CI Quality Gates

To make the contract enforceable, PR automation should check:

1. Required metadata exists on changed knowledge pages.
2. `Sources / References` exists and includes at least one URL.
3. Confidence label is present and valid.
4. Last reviewed date is valid ISO format.

These checks are implemented by `scripts/check_docs_contract.py` and run on pull requests.

In this repository, the practical gate stack also includes catalog consistency, intake validation, link health, and generated-content checks depending on which files changed.

## Phased Rollout Plan

### Phase 1: Contract and Structure

- Publish this governance document.
- Add contract language to `docs/CONTRIBUTING.md`.
- Add metadata requirements to `docs/standards.md`.

### Phase 2: Enforcement

- Enable CI quality gate for changed Markdown docs.
- Block merges when required metadata/sources are missing.

### Phase 3: Reliability and Auditability

- Add periodic audit runs for stale pages.
- Track common failure modes and update agent prompts.

## Definition of Done for AI-Authored PRs

A PR is complete only when:

1. Target pages follow template/section expectations.
2. Metadata and sources are present and valid.
3. Canonical duplication checks were performed.
4. Navigation/data indexes were updated when required.
5. The PR body lists the checks run and names any unavailable local tools.

## Sources / References

- [AI Hub Standards](../standards.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Automated Contributions](./automated_contributions.md)
- [GitHub Actions: Events that trigger workflows](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows)
- [Repository standards](../standards.md)

## Related

- [Home](../index.md)
- [Automated Contributions](./automated_contributions.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Contribution Metadata

- Last reviewed: 2026-05-07
- Confidence: high
