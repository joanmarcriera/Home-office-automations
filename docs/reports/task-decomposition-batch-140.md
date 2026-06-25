# Task Decomposition - Batch 140

This report decomposes the next five oldest issues identified in the repository into granular sub-tasks for technical freshness audits.

## Batch Overview
- **Status**: Triage Complete
- **Date**: 2026-06-25
- **Auditor**: Jules

## Issues for Action C (Decomposition)

### 1. `docs/architecture/infrastructure.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Incorporate June 2026 architectural standards (EKS Auto Mode, Karpenter, Cilium v1.17+).
  - Add mandatory `## CLI examples` and `## API examples` for infrastructure health monitoring.
  - Verify with `scripts/check_docs_contract.py`.

### 2. `docs/architecture/prompt-catalogue.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Update system prompts for Claude 4.8 and GPT-5.5 reasoning models.
  - Add mandatory `## CLI examples` and `## API examples` for automated prompt testing (Promptfoo).
  - Verify with `scripts/check_docs_contract.py`.

### 3. `docs/architecture/ssh_execution_patterns.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Integrate context for agentic SSH execution via MCP 3.0.
  - Add mandatory `## CLI examples` and `## API examples` for secure remote command execution.
  - Verify with `scripts/check_docs_contract.py`.

### 4. `docs/knowledge_base/patterns/agentic-workflows.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Update for June 2026 model identifiers (Claude 4.8, GPT-5.5).
  - Incorporate "Self-Healing Agentic Loop" and MCP 3.0 orchestration patterns.
  - Add mandatory `## CLI examples` and `## API examples`.
  - Verify with `scripts/check_docs_contract.py`.

### 5. `docs/knowledge_base/patterns/n8n-error-handling.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Incorporate n8n v1.50+ features for error management.
  - Integrate "LLM-based Log Reasoning" for autonomous remediation.
  - Add mandatory `## CLI examples` and `## API examples`.
  - Verify with `scripts/check_docs_contract.py`.

## Next Steps
These tasks will be addressed sequentially in the next Ralph-loop batch (Batch 141).
