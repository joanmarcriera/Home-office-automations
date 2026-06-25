# Task Decomposition - Batch 139

This report decomposes the next five oldest issues identified in the repository into granular sub-tasks for technical freshness audits.

## Batch Overview
- **Status**: Triage Complete
- **Date**: 2026-06-25
- **Auditor**: Jules

## Issues for Action C (Decomposition)

### 1. `docs/playbooks/tailscale-to-headscale-migration.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Incorporate context for Headscale v0.25+ and Tailscale v1.145+ features.
  - Add mandatory `## CLI examples` and `## API examples` (e.g., for Headscale node management).
  - Verify with `scripts/check_docs_contract.py`.

### 2. `docs/playbooks/family-admin-automation.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Incorporate context for Claude 4.8 and GPT-5.5 as personal admin agents.
  - Add mandatory `## CLI examples` and `## API examples` for n8n/Home Assistant integration.
  - Verify with `scripts/check_docs_contract.py`.

### 3. `docs/playbooks/k3s-cluster-setup.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Update context for K3s v1.31 and Cilium v1.17+ as the June 2026 default.
  - Add mandatory `## CLI examples` and `## API examples` for cluster health and node joining.
  - Verify with `scripts/check_docs_contract.py`.

### 4. `docs/playbooks/email-to-calendar.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Integrate context for MCP 3.0 and Chronos MCP for calendar orchestration.
  - Add mandatory `## CLI examples` and `## API examples` for n8n extraction workflows.
  - Verify with `scripts/check_docs_contract.py`.

### 5. `docs/playbooks/school-admin-intake.md`
**Task**: Technical freshness audit for June 2026.
- **Sub-tasks**:
  - Upgrade to the exact 13-section 'High Confidence' standard.
  - Incorporate context for Llama 4 Maverick (70B) for privacy-first school admin.
  - Add mandatory `## CLI examples` and `## API examples` for Vikunja and Paperless-AI integration.
  - Verify with `scripts/check_docs_contract.py`.

## Next Steps
These tasks will be addressed sequentially in the next Ralph-loop batch (Batch 140).
