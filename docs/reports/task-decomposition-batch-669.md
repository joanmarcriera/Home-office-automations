# Task Decomposition Report - Ralph-Loop Batch 669

## Overview
- **Batch Identifier**: Ralph-loop Batch 669
- **Date**: 2027-01-07
- **Target Scope**: Top 5 oldest service documentation issues (`docs/services/homebox.md`, `docs/services/immich.md`, `docs/services/inventory.md`, `docs/services/it-tools.md`, `docs/services/jackett.md`).
- **Goal**: Sequentially audit each of the top 5 oldest issues until closed, ensuring KnowledgeOps 13-section structure, Pydantic v2 code schema, and FastMCP 3.1 task protocol alignment.

## Task Decomposition & Status

| Task ID | Item / Target Document | Description & Context | Status |
| :--- | :--- | :--- | :--- |
| 669-1 | `docs/services/homebox.md` | Audit inventory management service doc for KnowledgeOps 13-section contract, FastMCP 3.1 asset retrieval tool, Pydantic v2 schemas, and >=7 internal cross-links | Completed |
| 669-2 | `docs/services/immich.md` | Audit photo/video management service doc for KnowledgeOps 13-section contract, FastMCP 3.1 media search, Pydantic v2 asset schemas, and >=7 internal cross-links | Completed |
| 669-3 | `docs/services/inventory.md` | Audit consolidated services inventory doc for KnowledgeOps 13-section contract, FastMCP 3.1 query tools, Pydantic v2 validation, and >=7 internal cross-links | Completed |
| 669-4 | `docs/services/it-tools.md` | Audit utility suite service doc for KnowledgeOps 13-section contract, FastMCP 3.1 transformation endpoints, Pydantic v2 request models, and >=7 internal cross-links | Completed |
| 669-5 | `docs/services/jackett.md` | Audit API proxy service doc for KnowledgeOps 13-section contract, FastMCP 3.1 indexer routing tool, Pydantic v2 result validation, and >=7 internal cross-links | Completed |

## Verification Summary
- **Catalog Consistency**: Checked via `python3 scripts/check_catalog_consistency.py`
- **Intake/New Sources Verification**: Checked via `python3 scripts/validate_new_sources.py`
- **Docs Quality & Contract Audit**: Checked via `python3 scripts/audit_docs_quality.py`
