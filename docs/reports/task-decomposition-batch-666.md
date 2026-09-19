# Task Decomposition Report - Ralph-Loop Batch 666

## Overview
- **Batch Identifier**: Ralph-loop Batch 666
- **Date**: 2027-01-07
- **Target Scope**: Top 5 oldest service documentation issues (`docs/services/searXNG-automation.md`, `docs/services/excalidraw.md`, `docs/services/focalboard.md`, `docs/services/actual-budget.md`, `docs/services/audiobookshelf.md`).
- **Goal**: Sequentially audit each of the top 5 oldest issues until closed, ensuring KnowledgeOps 13-section structure, Pydantic v2 code schema, and FastMCP 3.1 task protocol alignment.

## Task Decomposition & Status

| Task ID | Item / Target Document | Description & Context | Status |
| :--- | :--- | :--- | :--- |
| 666-1 | `docs/services/searXNG-automation.md` | Audit meta-search engine automation service doc for KnowledgeOps 13-section contract, FastMCP 3.1 search tool, Pydantic v2 validation, and >=7 internal cross-links | Completed |
| 666-2 | `docs/services/excalidraw.md` | Audit visual sketching canvas service doc for KnowledgeOps 13-section contract, FastMCP 3.1 visual reasoning, Pydantic v2 diagram schemas, and >=7 internal cross-links | Completed |
| 666-3 | `docs/services/focalboard.md` | Audit Kanban task management service doc for KnowledgeOps 13-section contract, FastMCP 3.1 task bridges, Pydantic v2 board schemas, and >=7 internal cross-links | Completed |
| 666-4 | `docs/services/actual-budget.md` | Audit personal finance service doc for KnowledgeOps 13-section contract, FastMCP 3.1 financial auditing, Pydantic v2 transaction validation, and >=7 internal cross-links | Completed |
| 666-5 | `docs/services/audiobookshelf.md` | Audit audiobook/podcast server service doc for KnowledgeOps 13-section contract, FastMCP 3.1 library orchestration, Pydantic v2 metadata validation, and >=7 internal cross-links | Completed |

## Verification Summary
- **Catalog Consistency**: Checked via `python3 scripts/check_catalog_consistency.py`
- **Intake/New Sources Verification**: Checked via `python3 scripts/validate_new_sources.py`
- **Docs Quality & Contract Audit**: Checked via `python3 scripts/audit_docs_quality.py`
