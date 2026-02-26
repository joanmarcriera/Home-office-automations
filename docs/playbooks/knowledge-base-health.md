# Playbook: Knowledge Base Health

## Objective
Maintain content quality, freshness, and discoverability across the knowledge base through regular audits and automated checks.

## Pre-requisites
- [Quality audit script](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/audit_docs_quality.py) (`scripts/audit_docs_quality.py`)
- [Docs contract checker](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/check_docs_contract.py) (`scripts/check_docs_contract.py`)
- [Catalog consistency checker](https://github.com/joanmarcriera/Home-office-automations/blob/main/scripts/check_catalog_consistency.py) (`scripts/check_catalog_consistency.py`)
- [Standards reference](../standards.md)

## Review cadence

| Check | Frequency | Owner | How |
|:---|:---|:---|:---|
| Intake queue (`new-sources/`) | Daily | Jules (automated) | `daily-jules-maintenance.yml` opens a structured issue |
| Doc contract CI gate | Every PR | CI | `docs-quality-gates.yml` runs `check_docs_contract.py` |
| Catalog consistency CI gate | Every PR | CI | `catalog-quality-gates.yml` runs `check_catalog_consistency.py` |
| Full quality audit | Weekly (manual) | Maintainer | `python3 scripts/audit_docs_quality.py` |
| Staleness review (docs >90 days old) | Monthly | Maintainer | See "Staleness check" below |
| Taxonomy alignment | Quarterly | Maintainer | Verify category dirs match `standards.md` |

## Step-by-step: weekly quality audit

1. **Run the audit script**:
   ```bash
   python3 scripts/audit_docs_quality.py
   ```
2. **Review the output**:
    - **Legacy-format docs**: prioritise upgrading high-traffic pages first (tools you reference in playbooks or architecture docs).
    - **Missing metadata**: add `Last reviewed` / `Confidence` / `Sources` blocks.
    - **Per-category breakdown**: identify categories with the lowest compliance rate.
3. **Fix the top 5 issues**: focus on the docs that will fail CI the next time they are touched.
4. **Update `data/all_tools.json`**: ensure every page in `mkdocs.yml` nav has a matching entry.
5. **Verify nav ↔ index consistency**: each `index.md` in `docs/tools/*/` should list all sibling tool pages.

## Step-by-step: staleness check

1. **Find docs not reviewed in 90+ days**:
   ```bash
   grep -rl "Last reviewed:" docs/ | xargs grep "Last reviewed:" | \
     awk -F': ' '{print $NF, $1}' | sort | head -20
   ```
2. **For each stale doc**, decide:
    - **Still accurate** — update the `Last reviewed` date.
    - **Needs refresh** — update content and bump the date.
    - **Obsolete** — remove from `mkdocs.yml`, `data/all_tools.json`, and the category `index.md`.

## Quality metrics

Track these over time to measure knowledge base health:

| Metric | Target | How to measure |
|:---|:---|:---|
| Template compliance rate | >90% | `audit_docs_quality.py` → compliant / total |
| Legacy-format docs remaining | 0 | `audit_docs_quality.py` → legacy count |
| Docs with metadata | 100% | `audit_docs_quality.py` → missing metadata count |
| Average doc age (days since last review) | <60 days | `grep "Last reviewed"` across all docs |
| Catalog consistency (nav ↔ JSON) | 100% | `check_catalog_consistency.py` exit code |
| Intake queue backlog | 0 `new` items | `grep "new" docs/new-sources/*.md` |

## Common failure modes

- **Category index out of sync**: a new tool doc is added to `mkdocs.yml` but not to its `index.md`. Fix: update the index file whenever adding a nav entry.
- **Orphaned JSON entries**: a tool page is deleted but its `all_tools.json` entry remains. Fix: always update both when removing a page.
- **Duplicate pages**: two pages document the same tool. Fix: merge into the canonical page and redirect/remove the duplicate.
- **Stale model references**: docs reference old model names (e.g., "Claude 3.5 Sonnet" instead of "Claude Sonnet 4.6"). Fix: search-and-replace during staleness reviews.

## Related tools / concepts
- [Standards](../standards.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Automated Contributions](../architecture/automated_contributions.md)

## Sources / references
- [Project standards](../standards.md)
- [MkDocs Material docs](https://squidfox.dev/mkdocs-material/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: high
