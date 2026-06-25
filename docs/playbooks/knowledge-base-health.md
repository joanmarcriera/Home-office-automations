# Playbook: Knowledge Base Health

## What it is
Knowledge Base Health is a set of operational procedures and automated checks designed to ensure the repository remains accurate, up-to-date, and discoverable. It combines periodic manual audits with continuous integration (CI) quality gates.

## What problem it solves
In a rapidly evolving technical environment, documentation quickly becomes stale or fragmented. This playbook prevents "documentation rot" by establishing clear ownership, a structured review cadence, and automated enforcement of formatting standards, ensuring users can always trust the information in the repository.

## Where it fits in the stack
This playbook belongs to the **Governance and Maintenance** layer. It provides the "metabolic process" that keeps the [KnowledgeOps](../architecture/multi_agent_knowledgeops.md) system healthy and prevents entropy from degrading the quality of the shared knowledge base.

## Typical use cases
- Performing a weekly quality check to identify non-compliant documents.
- Managing the intake of new tools and patterns from community sources.
- Cleaning up obsolete information and ensuring model names are current.
- Maintaining consistency between the filesystem, the `mkdocs.yml` navigation, and the `data/all_tools.json` catalog.

## Strengths
- **Multi-Layered Enforcement**: Combines automated PR gates with deeper, periodic manual/automated audits.
- **Traceability**: Uses `Last reviewed` and `Confidence` metadata to provide clear signals to users about data reliability.
- **Automated Discovery**: Includes scripts to detect "drift" between user stars/activity and what is actually documented.

## Limitations
- **Maintenance Overhead**: Requires dedicated effort to fix the issues identified by the audit scripts.
- **Script Dependency**: The health of the system relies on the accuracy and maintenance of the underlying Python scripts.

## When to use it
- During every pull request to ensure immediate compliance.
- Once a week to perform a broader scan of the entire repository.
- When onboarding new automated agents to define their quality boundaries.

## When not to use it
- For very small, personal repositories where formal governance processes are overkill.
- For temporary "scratchpad" notes that are not intended to be part of the canonical knowledge base.

## Getting started
The objective of this playbook is to maintain content quality, freshness, and discoverability across the knowledge base through regular audits and automated checks.

### Process Flow
```mermaid
flowchart TD
    A[Start Audit] --> B[Run audit_docs_quality.py]
    B --> C{Issues Found?}
    C -- No --> D[Check Staleness]
    C -- Yes --> E[Fix Priority Issues]
    E --> F[Update data/all_tools.json]
    F --> G[Verify Nav/Index Consistency]
    G --> D
    D --> H[Update Review Dates]
    H --> I[End Audit]
```

### Pre-requisites
- [Quality audit script](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/audit_docs_quality.py) (`scripts/audit_docs_quality.py`)
- [Docs contract checker](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/check_docs_contract.py) (`scripts/check_docs_contract.py`)
- [Catalog consistency checker](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/check_catalog_consistency.py) (`scripts/check_catalog_consistency.py`)
- [Doc freshness checker](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/check_doc_freshness.py) (`scripts/check_doc_freshness.py`)
- [API pricing summary generator](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/update_api_pricing_capability_summary.py) (`scripts/update_api_pricing_capability_summary.py`)
- [Model account policy validator](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/validate_model_account_pool.py) (`scripts/validate_model_account_pool.py`)
- [Starred repo intake checker](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/check_starred_repo_intake.py) (`scripts/check_starred_repo_intake.py`)
- [Standards reference](../standards.md)

### Review cadence

| Check | Frequency | Owner | How |
|:---|:---|:---|:---|
| Intake queue (`new-sources/`) | Daily | Jules (automated) | `daily-jules-maintenance.yml` opens a structured issue |
| Doc contract CI gate | Every PR | CI | `docs-quality-gates.yml` runs `check_docs_contract.py` |
| Catalog consistency CI gate | Every PR | CI | `catalog-quality-gates.yml` runs `check_catalog_consistency.py` |
| Generated pricing summary gate | PRs touching pricing tracker | CI | `generated-content-gates.yml` runs summary sync + freshness checks |
| API pricing maintenance | Weekly | CI | `api-pricing-maintenance.yml` refreshes capacity summaries and flags stale review metadata |
| External link health | Weekly + docs PRs | CI | `docs-link-health.yml` (Lychee) checks markdown links |
| Model-account routing policy gate | PRs touching policy file | CI | `model-account-policy-gates.yml` validates multi-account routing rules |
| Full quality audit | Weekly (manual) | Maintainer | `python3 scripts/audit_docs_quality.py` |
| Starred repo drift check | Weekly (manual/local) | Maintainer | `python3 scripts/check_starred_repo_intake.py --ai-only --min-stars 5000` |
| Staleness review (docs >90 days old) | Monthly | Maintainer | See "Staleness check" below |
| Taxonomy alignment | Quarterly | Maintainer | Verify category dirs match `standards.md` |

### Step-by-step: weekly quality audit

1. **Run the audit script**:
   ```bash
   python3 scripts/audit_docs_quality.py
   ```
2. **Review the output**:
    - **Legacy-format docs**: prioritise upgrading high-traffic pages first.
    - **Missing metadata**: add `Last reviewed` / `Confidence` / `Sources` blocks.
    - **Per-category breakdown**: identify categories with the lowest compliance rate.
3. **Fix the top 5 issues**: focus on the docs that will fail CI the next time they are touched.
4. **Update `data/all_tools.json`**: ensure every page in `mkdocs.yml` nav has a matching entry.
5. **Verify nav ↔ index consistency**: each `index.md` in `docs/tools/*/` should list all sibling tool pages.
6. **Check starred-repo drift**:
   ```bash
   python3 scripts/check_starred_repo_intake.py --ai-only --min-stars 5000
   ```

### Step-by-step: staleness check

1. **Find docs not reviewed in 90+ days**:
   ```bash
   grep -rl "Last reviewed:" docs/ | xargs grep "Last reviewed:" | \
     awk -F': ' '{print $NF, $1}' | sort | head -20
   ```
2. **For each stale doc**, decide:
    - **Still accurate** — update the `Last reviewed` date.
    - **Needs refresh** — update content and bump the date.
    - **Obsolete** — remove from `mkdocs.yml`, `data/all_tools.json`, and the category `index.md`.

### Quality metrics

| Metric | Target | How to measure |
|:---|:---|:---|
| Template compliance rate | >90% | `audit_docs_quality.py` → compliant / total |
| Legacy-format docs remaining | 0 | `audit_docs_quality.py` → legacy count |
| Docs with metadata | 100% | `audit_docs_quality.py` → missing metadata count |
| Average doc age (days since last review) | <60 days | `grep "Last reviewed"` across all docs |
| Catalog consistency (nav ↔ JSON) | 100% | `check_catalog_consistency.py` exit code |
| Intake queue backlog | 0 `new` items | `grep "new" docs/new-sources/*.md` |

### Common failure modes

- **Category index out of sync**: a new tool doc is added to `mkdocs.yml` but not to its `index.md`.
- **Orphaned JSON entries**: a tool page is deleted but its `all_tools.json` entry remains.
- **Duplicate pages**: two pages document the same tool.
- **Stale model references**: docs reference old model names (e.g., "Claude 4.6" instead of "Claude 4.8").
- **Starred-repo drift**: you star new GitHub repos but never stage them into `docs/new-sources/`.

## CLI examples
```bash
# Run the full quality audit across the repository
python3 scripts/audit_docs_quality.py

# Verify the KnowledgeOps contract for a specific file
python3 scripts/check_docs_contract.py docs/tools/ai_knowledge/claude.md

# Find documentation pages that are stale or missing metadata
python3 scripts/check_doc_freshness.py
```

## API examples
The health of the knowledge base can be checked programmatically via the following scripts.

```python
import subprocess

# Example: Programmatic check of catalog consistency
def check_catalog():
    result = subprocess.run(["python3", "scripts/check_catalog_consistency.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Catalog mismatch found: {result.stdout}")
    else:
        print("Catalog is consistent.")

# check_catalog()
```

## Related tools / concepts
- [Standards](../standards.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Automated Contributions](../architecture/automated_contributions.md)
- [Quality Audit Script](../../scripts/audit_docs_quality.py)
- [Check Docs Contract Script](../../scripts/check_docs_contract.py)
- [Catalog Consistency Script](../../scripts/check_catalog_consistency.py)
- [KnowledgeOps Standards](../standards.md)
- [Jules Agent](../tools/ai_knowledge/jules.md)

## Sources / References
- [Project standards](../standards.md)
- [MkDocs Material docs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub CLI](https://cli.github.com/)

## Contribution Metadata

- Last reviewed: 2026-06-26
- Confidence: high
