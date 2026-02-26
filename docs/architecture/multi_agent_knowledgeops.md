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

## CI Quality Gates

To make the contract enforceable, PR automation should check:

1. Required metadata exists on changed knowledge pages.
2. `Sources / References` exists and includes at least one URL.
3. Confidence label is present and valid.
4. Last reviewed date is valid ISO format.

These checks are implemented by `scripts/check_docs_contract.py` and run on pull requests.

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

## Sources / References

- [AI Hub Standards](../standards.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Automated Contributions](./automated_contributions.md)
- [GitHub Actions: Events that trigger workflows](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: high
