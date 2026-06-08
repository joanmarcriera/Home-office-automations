# Design: Cherry-Pick Major Gains from Closed PRs

**Date**: 2026-06-08  
**Status**: Approved  
**Branch**: `feat/cherry-pick-major-gains-from-closed-prs`

## Goal

Extract the most valuable documentation and script changes from 16 closed/conflicting PRs and apply them cleanly on top of current `main` as a single new PR.

## Selection Criteria

- Files where the branch version has ≥20 more lines than current `main` (genuine content enrichment, not noise)
- Files entirely new to `main` (heygen.md)
- New utility scripts not present in `main`

## File Inventory (34 files)

### New file
| File | Source branch |
|---|---|
| `docs/tools/ai_knowledge/heygen.md` | `origin/ralph-loop-batch-56-60-14332896274658620492` |

### Enriched service docs (+20 to +176 lines)
| File | Delta | Source branch |
|---|---|---|
| `docs/services/tubearchivist.md` | +176 | `origin/ralph-loop-batch-99-sub-1-media-freshness-audit-14838447504829357713` |
| `docs/services/jellyfin.md` | +78 | same |
| `docs/services/navidrome.md` | +75 | same |
| `docs/services/jackett.md` | +67 | same |
| `docs/services/plex.md` | +21 | same |
| `docs/services/plex-automation.md` | +7 | same |
| `docs/services/grocy.md` | +44 | `origin/ralph-loop-batch-99-sub-2-7429795985516843168` |
| `docs/services/actual-budget.md` | +34 | same |
| `docs/services/focalboard.md` | +21 | same |
| `docs/services/habitica.md` | +48 | same |
| `docs/services/it-tools.md` | +33 | same |
| `docs/services/vikunja.md` | +74 | `origin/ralph-loop-freshness-batch-99-sub-2-vikunja-1589986518803363299` |
| `docs/services/syncthing.md` | +68 | `origin/ralph-loop-batch-94-resolution-4332415108223708556` |
| `docs/services/gitea.md` | +61 | same |
| `docs/services/trilium.md` | +48 | `origin/trilium-freshness-audit-2529060529777763237` |

### Enriched tool docs
| File | Delta | Source branch |
|---|---|---|
| `docs/tools/development_ops/llmfit.md` | +87 | `origin/issue-resolution-batch-freshness-audit-10508511053722809236` |
| `docs/tools/benchmarking/helm.md` | +76 | `origin/ralph-loop-batch-100-12179161220186892849` |
| `docs/tools/benchmarking/evalplus.md` | +52 | `origin/docs/batch-77-issue-1-evalplus-7788724441553733546` |
| `docs/tools/frameworks/firebase-genkit.md` | +40 | `origin/issue-resolution-batch-freshness-audit-10508511053722809236` |
| `docs/tools/frameworks/instructor.md` | +38 | same |
| `docs/tools/development_ops/google-stitch.md` | +23 | same |
| `docs/tools/infrastructure/aphrodite-engine.md` | +19 | `origin/ralph-loop-maintenance-2026-06-02-3871319807512746608` |
| `docs/tools/ai_knowledge/elevenlabs.md` | +15 | `origin/ralph-loop-batch-74-deepening-elevenlabs-10952158861147126697` |

### Enriched knowledge base / patterns
| File | Delta | Source branch |
|---|---|---|
| `docs/knowledge_base/patterns/data-copilot-agentic-rag.md` | +64 | `origin/ralph-loop-batch-111-4109746271122170512` |
| `docs/knowledge_base/ai_company_starter_stack.md` | +61 | `origin/jules/audit-batch-june-07-9101608677968828562` |
| `docs/knowledge_base/ai_reading_list.md` | +60 | same |
| `docs/knowledge_base/patterns/openclaw-use-case-catalog.md` | +37 | `origin/ralph-loop-batch-100-12179161220186892849` |
| `docs/knowledge_base/home-admin-agent-architecture.md` | +42 | `origin/jules/audit-batch-june-07-9101608677968828562` |
| `docs/reference-implementations/data-copilot/skeleton-guide.md` | +57 | `origin/ralph-loop-batch-111-4109746271122170512` |
| `docs/playbooks/knowledge-base-health.md` | +38 | `origin/jules/audit-batch-june-07-9101608677968828562` |

### New scripts
| File | Source branch |
|---|---|
| `scripts/sql_validator.py` | `origin/ralph-loop-batch-94-resolution-4332415108223708556` |
| `scripts/test_sql_validator.py` | same |
| `scripts/verify_node_headscale.py` | same |
| `find_oldest_docs.py` | `origin/ralph-loop-batch-100-12179161220186892849` |
| `find_oldest_issues.py` | `origin/issue-resolution-batch-freshness-audit-10508511053722809236` |

## mkdocs.yml

Add `heygen.md` entry under the `ai_knowledge` nav section.

## Method

1. Create branch `feat/cherry-pick-major-gains-from-closed-prs` from `main`
2. For each file: `git show <source-branch>:<path>` → overwrite local file
3. For new scripts/files: create parent dirs as needed, write file
4. Update `mkdocs.yml` for heygen.md
5. Commit in logical groups (services, tools, KB, scripts)
6. Open PR against `main`
