# Task Decomposition Report - Ralph-Loop Batch 671

## Overview
- **Batch Identifier**: Ralph-loop Batch 671
- **Date**: 2027-01-07
- **Target Scope**: Top 5 oldest service documentation issues (`docs/services/omni-tools.md`, `docs/services/open-webui.md`, `docs/services/paperless-ai.md`, `docs/services/paperless-ngx.md`, `docs/services/plex-automation.md`).
- **Goal**: Sequentially audit each of the target issues until closed, ensuring KnowledgeOps 13-section structure, Pydantic v2 code schema, and FastMCP 3.1 task protocol alignment.

## Task Decomposition & Status

| Task ID | Item / Target Document | Description & Context | Status |
| :--- | :--- | :--- | :--- |
| 671-1 | `docs/services/omni-tools.md` | Audit web utility collection service doc for KnowledgeOps 13-section contract, FastMCP 3.1 payload transformation tool, Pydantic v2 schemas, and >=7 internal cross-links | Completed |
| 671-2 | `docs/services/open-webui.md` | Audit AI chat frontend service doc for KnowledgeOps 13-section contract, FastMCP 3.1 model listing tool, Pydantic v2 session models, and >=7 internal cross-links | Completed |
| 671-3 | `docs/services/paperless-ai.md` | Audit document AI companion service doc for KnowledgeOps 13-section contract, FastMCP 3.1 task protocol, Pydantic v2 document metadata models, and >=7 internal cross-links | Completed |
| 671-4 | `docs/services/paperless-ngx.md` | Audit document management service doc for KnowledgeOps 13-section contract, FastMCP 3.1 API tools, Pydantic v2 ingestion response models, and >=7 internal cross-links | Completed |
| 671-5 | `docs/services/plex-automation.md` | Audit media server automation service doc for KnowledgeOps 13-section contract, FastMCP 3.1 library tools, Pydantic v2 session alert models, and >=7 internal cross-links | Completed |

## Verification Summary
- **Catalog Consistency**: Checked via `python3 scripts/check_catalog_consistency.py`
- **Intake/New Sources Verification**: Checked via `python3 scripts/validate_new_sources.py`
- **Docs Quality & Contract Audit**: Checked via `python3 scripts/audit_docs_quality.py`
