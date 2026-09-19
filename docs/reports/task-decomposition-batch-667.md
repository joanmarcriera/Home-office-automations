# Task Decomposition Report - Ralph-Loop Batch 667

## Overview
- **Batch Identifier**: Ralph-loop Batch 667
- **Date**: 2027-01-07
- **Target Scope**: Top 5 oldest service documentation issues (`docs/services/authentik.md`, `docs/services/cloudflare-mesh.md`, `docs/services/drawio.md`, `docs/services/element.md`, `docs/services/grocy.md`).
- **Goal**: Sequentially audit each of the top 5 oldest issues until closed, ensuring KnowledgeOps 13-section structure, Pydantic v2 code schema, and FastMCP 3.1 task protocol alignment.

## Task Decomposition & Status

| Task ID | Item / Target Document | Description & Context | Status |
| :--- | :--- | :--- | :--- |
| 667-1 | `docs/services/authentik.md` | Audit IdP service doc for KnowledgeOps 13-section contract, FastMCP 3.1 token refresh tool, Pydantic v2 validation, and >=7 internal cross-links | Completed |
| 667-2 | `docs/services/cloudflare-mesh.md` | Audit zero-trust network tunnel service doc for KnowledgeOps 13-section contract, FastMCP 3.1 tunnel health tool, Pydantic v2 schemas, and >=7 internal cross-links | Completed |
| 667-3 | `docs/services/drawio.md` | Audit graph diagramming service doc for KnowledgeOps 13-section contract, FastMCP 3.1 visual task protocol, Pydantic v2 diagram schemas, and >=7 internal cross-links | Completed |
| 667-4 | `docs/services/element.md` | Audit Matrix chat service doc for KnowledgeOps 13-section contract, FastMCP 3.1 alert manager tool, Pydantic v2 message schemas, and >=7 internal cross-links | Completed |
| 667-5 | `docs/services/grocy.md` | Audit household inventory service doc for KnowledgeOps 13-section contract, FastMCP 3.1 stock orchestration, Pydantic v2 stock validation schemas, and >=7 internal cross-links | Completed |

## Verification Summary
- **Catalog Consistency**: Checked via `python3 scripts/check_catalog_consistency.py`
- **Intake/New Sources Verification**: Checked via `python3 scripts/validate_new_sources.py`
- **Docs Quality & Contract Audit**: Checked via `python3 scripts/audit_docs_quality.py`
