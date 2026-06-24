# Task Decomposition - Batch 138

This report decomposes the next five oldest issues identified in the repository into granular sub-tasks for technical freshness audits.

## Batch Overview
- **Status**: Triage Complete
- **Date**: 2026-06-24
- **Auditor**: Jules

## Issues for Action C (Decomposition)

### 1. `docs/knowledge_base/invisible_kubernetes.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the 13-section 'High Confidence' standard.
  - Incorporate context for Claude 4.8 and GPT-5.5 as SRE agents.
  - Update sections on EKS Auto Mode and Karpenter with latest 2026 performance data.
  - Verify with `scripts/check_docs_contract.py`.

### 2. `docs/knowledge_base/agent_framework_learning_map.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the 13-section 'High Confidence' standard.
  - Re-evaluate framework rankings for June 2026 (LangGraph, OpenAI Agents SDK, CrewAI).
  - Add sections for MCP 3.0 integration within framework learning paths.
  - Update "Recommended Learning Order" with 2026 model defaults (Claude 4.8 reasoning).
  - Verify with `scripts/check_docs_contract.py`.

### 3. `docs/playbooks/dev-workflow-ai-assisted.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the 13-section 'High Confidence' standard.
  - Update the Mermaid diagram to include MCP 3.0 and Anti-Gravity orchestration.
  - Refine the "PR-readiness gate" with June 2026 automated verification patterns.
  - Add CLI/API examples for Aider and Jules integration.
  - Verify with `scripts/check_docs_contract.py`.

### 4. `docs/playbooks/scan-to-task.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the 13-section 'High Confidence' standard.
  - Integrate Vision-Language Model (VLM) context for GPT-5.5 and Claude 4.8.
  - Update OCR and document processing tools (Crawl4AI, PageIndex) to 2026 versions.
  - Add CLI examples for batch scanning and task extraction.
  - Verify with `scripts/check_docs_contract.py`.

### 5. `docs/playbooks/document-preparation-for-llm-training.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the 13-section 'High Confidence' standard.
  - Update context for synthetic data generation using Llama 4 Maverick.
  - Refine sections on RAG-readiness vs. fine-tuning preparation.
  - Add API examples for automated data cleaning pipelines using MCP 3.0.
  - Verify with `scripts/check_docs_contract.py`.

## Next Steps
These tasks will be addressed sequentially in the next Ralph-loop batch (Batch 139).
