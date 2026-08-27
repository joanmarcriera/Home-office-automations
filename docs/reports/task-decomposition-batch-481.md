# Task Decomposition Report - Batch 481

## Overview
- **Execution Date**: 2027-01-07
- **Batch Type**: Oldest Stale AI Knowledge Documentation Upgrade
- **Open Intake Pipeline Audit**: Verified `docs/new-sources/*.md` across 71 daily log files; 0 open/new issues found.
- **Target Items**: The 5 oldest stale AI knowledge documentation files identified in the repository:
  1. `docs/tools/ai_knowledge/mellum2.md` (Last reviewed: 2026-11-25 -> 2027-01-07)
  2. `docs/tools/ai_knowledge/moondream.md` (Last reviewed: 2026-11-25 -> 2027-01-07)
  3. `docs/tools/ai_knowledge/roam-research.md` (Last reviewed: 2026-11-25 -> 2027-01-07)
  4. `docs/tools/ai_knowledge/wan-dancer.md` (Last reviewed: 2026-11-25 -> 2027-01-07)
  5. `docs/tools/ai_knowledge/bonsai.md` (Last reviewed: 2026-11-26 -> 2027-01-07)

## Item Breakdown & Upgrade Actions

### 1. `docs/tools/ai_knowledge/mellum2.md`
- **Scope**: Multi-token prediction (MTP v2) low-latency local LLM.
- **Upgrades**: Integrated FastMCP 3.1 endpoints, updated frontier model references (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra), updated dates and Pydantic v2 schemas.

### 2. `docs/tools/ai_knowledge/moondream.md`
- **Scope**: Tiny sparse MoE vision-language model for edge perception and computer use.
- **Upgrades**: Enhanced FastMCP 3.1 visual reasoning tools, updated frontier models context, updated dates and Pydantic v2 vision schemas.

### 3. `docs/tools/ai_knowledge/roam-research.md`
- **Scope**: Networked-thought personal knowledge graph platform.
- **Upgrades**: Upgraded graph query integrations to FastMCP 3.1 protocol, updated dates and Pydantic v2 API integration schemas.

### 4. `docs/tools/ai_knowledge/wan-dancer.md`
- **Scope**: 14B parameter hierarchical music-to-dance long-form video diffusion framework.
- **Upgrades**: Upgraded pose transfer and generation pipelines, FastMCP 3.1 tool calls, updated dates and Pydantic v2 request configuration schemas.

### 5. `docs/tools/ai_knowledge/bonsai.md`
- **Scope**: PrismML extreme low-bit (1-bit / ternary) 27B-parameter edge reasoning model family.
- **Upgrades**: Updated FastMCP 3.1 integration patterns, refreshed dates to early January 2027, and maintained Pydantic v2 visual analysis schemas.

## Verification & Validation Plan
- Run `python3 scripts/validate_new_sources.py`
- Run `python3 scripts/check_catalog_consistency.py`
- Run `python3 scripts/check_docs_contract.py` on modified files
- Run `python3 scripts/audit_docs_quality.py`
