# Automation Improvement PR Template

## Summary
<!-- Briefly describe the automation improvement and the n8n failure pattern it addresses. -->
Addresses failure pattern: `[Workflow ID: Error Message]`

## Type of Change
- [ ] Documentation Update
- [ ] Workflow Logic Refinement
- [ ] New Test Case / Guardrail
- [ ] Infrastructure / Credential Configuration

## Implementation Details
<!-- Describe the specific changes made. -->
- Updated `docs/...` to clarify ...
- Modified `n8n/workflows/...` to handle ...
- Added `scripts/...` for ...

## Verification Results
- [ ] `scripts/check_docs_contract.py` passed (if docs changed)
- [ ] Manual verification of n8n node configuration
- [ ] Unit tests for new scripts

## Rollback Plan
<!-- How to undo this change if it causes regressions. -->
- Revert commit `abc1234`
- Restore previous workflow JSON from `n8n/backups/`

## Related Issues
- Related to: Sub-Batch 42.4 (Jules Report Automation)
