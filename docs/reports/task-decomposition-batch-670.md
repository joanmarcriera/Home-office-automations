# Task Decomposition Report - Ralph-Loop Batch 670

## Overview
- **Batch Identifier**: Ralph-loop Batch 670
- **Date**: 2027-01-07
- **Target Scope**: Top 5 oldest service documentation issues (`docs/services/jellyfin.md`, `docs/services/kiwix.md`, `docs/services/navidrome.md`, `docs/services/nextcloud.md`, `docs/services/ollama.md`).
- **Goal**: Sequentially audit each of the top 5 oldest issues until closed, ensuring KnowledgeOps 13-section structure, Pydantic v2 code schema, and FastMCP 3.1 task protocol alignment.

## Task Decomposition & Status

| Task ID | Item / Target Document | Description & Context | Status |
| :--- | :--- | :--- | :--- |
| 670-1 | `docs/services/jellyfin.md` | Audit media streaming service doc for KnowledgeOps 13-section contract, FastMCP 3.1 media search tool, Pydantic v2 metadata schemas, and >=7 internal cross-links | Completed |
| 670-2 | `docs/services/kiwix.md` | Audit offline reader service doc for KnowledgeOps 13-section contract, FastMCP 3.1 offline ZIM search tool, Pydantic v2 query schemas, and >=7 internal cross-links | Completed |
| 670-3 | `docs/services/navidrome.md` | Audit music server service doc for KnowledgeOps 13-section contract, FastMCP 3.1 audio stream tools, Pydantic v2 track models, and >=7 internal cross-links | Completed |
| 670-4 | `docs/services/nextcloud.md` | Audit collaboration platform service doc for KnowledgeOps 13-section contract, FastMCP 3.1 WebDAV tools, Pydantic v2 share request schemas, and >=7 internal cross-links | Completed |
| 670-5 | `docs/services/ollama.md` | Audit local inference service doc for KnowledgeOps 13-section contract, FastMCP 3.1 model proxy tools, Pydantic v2 query schemas, and >=7 internal cross-links | Completed |

## Verification Summary
- **Catalog Consistency**: Checked via `python3 scripts/check_catalog_consistency.py`
- **Intake/New Sources Verification**: Checked via `python3 scripts/validate_new_sources.py`
- **Docs Quality & Contract Audit**: Checked via `python3 scripts/audit_docs_quality.py`
