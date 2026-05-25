# Task Decomposition: Batch 94 (Operational Verification & Freshness)

This report implements **Action C** for the remaining operational debt and technical freshness identified in the repository playbooks and service backlogs.

## Sub-Batch 94.1: Infrastructure Migration Verification
Verification tasks from `docs/playbooks/tailscale-to-headscale-migration.md`.
- [ ] **TrueNAS Migration**: Complete SSH logout/login and reachability verification.
- [ ] **K3s Node Migration**: Complete migration and update service advertisements.
- [ ] **Home Assistant Migration**: Complete HA Terminal logout/login and external access verification.

## Sub-Batch 94.2: Data Governance Guardrails
Verification tasks from `docs/playbooks/data-copilot-sql-validation.md`.
- [ ] **Row Limit Enforcement**: Verify automated appending of `LIMIT` clauses.
- [ ] **Table Allowlist Validation**: Verify blocking of queries to unlisted tables.
- [ ] **Mutation Blocking**: Verify detection of `DROP`, `DELETE`, etc.
- [ ] **PII/PHI Masking**: Verify exclusion of sensitive columns from outputs.

## Sub-Batch 94.3: Service Freshness
Ongoing maintenance tasks for core services.
- [ ] `docs/services/syncthing.md`: Perform quarterly technical freshness audit.
- [ ] `docs/services/gitea.md`: Perform quarterly technical freshness audit.

---
- Status: Actionable backlog created.
- Next Step: Integrate Kimi CLI into the Access Matrix as part of Batch 94.1 initialization.
- Date: 2026-05-25
- Created by: Jules
