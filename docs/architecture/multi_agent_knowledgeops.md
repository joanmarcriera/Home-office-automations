# Multi-Agent KnowledgeOps Governance

## What it is

Multi-Agent KnowledgeOps Governance is a structured framework that defines how multiple AI agents (e.g., Google Jules) can safely and consistently grow a shared knowledge repository. It establishes a "durable documentation system" where agents contribute in parallel while preserving canonical ownership, source traceability, and freshness signals.

## What problem it solves

The primary scaling risk in AI-augmented documentation is not a lack of content, but rather the rapid accumulation of low-quality, duplicate, or stale information. Without a shared operating contract, multiple agents eventually create conflicting guidance and redundant pages. This governance model provides a common contract and quality gates to keep throughput high while preventing entropy and information decay.

## Where it fits in the stack

KnowledgeOps Governance sits in the **Process and Governance** layer of the repository architecture. It acts as the "policy engine" for the [Automated Contribution System](./automated_contributions.md), ensuring that all automated updates comply with repository [standards](../standards.md) and [taxonomies](../standards.md).

## Typical use cases

- **Parallel Documentation Scaling**: Managing multiple agent lanes (Intake, Curation, Audit) working on different parts of the repository simultaneously.
- **Consistency Maintenance**: Ensuring every AI-authored page includes mandatory sections, metadata, and verifiable sources.
- **Conflict Resolution**: Preventing "PR collisions" by defining clear file boundaries and sequencing rules for autonomous workers.
- **Quality Auditing**: Using automated scripts (e.g., `audit_docs_quality.py`) to enforce the governance contract.

## Strengths

- **Predictable Growth**: Ensures all contributions meet the "High Confidence" standard regardless of which agent authored them.
- **Scalability**: Allows the knowledge base to expand rapidly without a linear increase in human review effort.
- **Traceability**: Every fact in the repository is tied to a specific source and review date, creating a verifiable audit trail.
- **Deduplication**: Built-in rules for canonical ownership prevent the fragmentation of information across multiple pages.

## Limitations

- **Process Overhead**: Requires agents to perform extra checks (duplication searches, metadata validation) which can increase per-task token costs.
- **Rigidity**: Highly structured templates may sometimes struggle to accommodate very unique or non-standard documentation needs.
- **Review Lag**: While it automates many gates, final high-stakes architectural alignment still requires human "North Star" guidance.

## When to use it

- When operating a repository that receives contributions from more than one automated agent or worker lane.
- When the goal is to maintain a "High Confidence" knowledge base with 100+ pages of technical documentation.
- To provide a clear "Role Model" for AI agents to follow during autonomous sprints.

## When not to use it

- For small, personal repositories where the volume of change is low and human review is instantaneous.
- For informal, low-stakes "scratchpad" projects where strict structure and metadata are unnecessary.

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

## Parallel Lane Rules: The Ralph-loop Strategy

When multiple agents are active simultaneously, they must adhere to the **Ralph-loop** strategy for conflict avoidance and task closure.

| Lane | Primary Scope | Strategy |
| :--- | :--- | :--- |
| **Intake** | `docs/new-sources*`, `data/all_tools.json`, `mkdocs.yml` | **Action B (Link)**: Focus on staging new items and updating indexes. |
| **Curation** | `docs/tools/`, `docs/services/` | **Action A (Work)**: Deepen documentation to "High Confidence" standards. |
| **Maintenance** | Entire repository | **Action A (Work)**: Execute batch audits and automated fixes (Batch 100+ patterns). |
| **Decomposition** | `docs/reports/` | **Action C (Decompose)**: Triage complex issues into smaller sub-batches. |

### Conflict Mitigation
- **File Locks**: Agents should treat `mkdocs.yml` and `data/all_tools.json` as shared resources; avoid concurrent edits by checking for open PRs touching these files.
- **Rebase First**: Always run `git fetch origin main && git rebase origin/main` before starting work to avoid stale state.
- **Narrow Focus**: Prefer one changed canonical page per PR to minimize merge conflicts.

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
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Ralph-loop Execution Reports](reports/)

## Related tools / concepts

- [Automated Contribution System](./automated_contributions.md)
- [Jules Agent](../tools/ai_knowledge/jules.md)
- [KnowledgeOps Standards](../standards.md)
- [Data Copilot Architecture](data-copilot-text-to-sql.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Quality Audit Script](../../scripts/audit_docs_quality.py)
- [Check Docs Contract Script](../../scripts/check_docs_contract.py)
- [Catalog Consistency Script](../../scripts/check_catalog_consistency.py)
- [Ralph-loop Implementation](../CONTRIBUTING.md)

## Contribution Metadata

- Last reviewed: 2026-05-28
- Confidence: high
