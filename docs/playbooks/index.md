# Operational Playbooks

Step-by-step execution guides for recurring workflows. Each playbook is self-contained: it lists prerequisites, the exact sequence of steps, the tools involved, and how to verify the outcome.

## Choose by Goal

| If you want to… | Use this playbook |
| :--- | :--- |
| Transfer models and ZIMs to air-gapped servers | [Air-gapped Provisioning](air-gapped-provisioning.md) |
| Protect critical data with a 3-2-1 backup strategy | [Backup & Disaster Recovery](backup-disaster-recovery.md) |
| Validate AI-generated SQL queries for safety and performance | [Data Copilot SQL Validation](data-copilot-sql-validation.md) |
| Automate a coding or review task end-to-end with AI assistance | [Dev Workflow (AI-Assisted)](dev-workflow-ai-assisted.md) |
| Prepare office documents for LLM training or retrieval ingestion | [Document Preparation for LLM Training](document-preparation-for-llm-training.md) |
| Route emails into calendar events automatically | [Email to Calendar](email-to-calendar.md) |
| Automate household paperwork — school letters, appointments, admin | [Family Admin Automation](family-admin-automation.md) |
| Deploy a private, air-gapped AI stack locally | [Fully Offline Assistant](fully-offline-assistant.md) |
| Configure automatic cloud-to-local failover | [Graceful Degradation](graceful-degradation.md) |
| Deploy a 3-node HA cluster for resilient workloads | [K3s Cluster Setup](k3s-cluster-setup.md) |
| Audit, repair, or improve the knowledge base and documentation | [Knowledge Base Health](knowledge-base-health.md) |
| Configure NFS CSI driver for persistent volumes on K3s | [NFS CSI Setup](nfs-csi-setup.md) |
| Transcribe audio and extract tasks locally | [Offline Transcription Pipeline](offline-transcription-pipeline.md) |
| Display dashboards or a kiosk on a Raspberry Pi without a desktop | [Raspberry Pi Kiosk Automation](raspberry-pi-kiosk-automation.md) |
| Convert a scanned document into an actionable task | [Scan to Task](scan-to-task.md) |
| Ingest and process school admin emails, letters, or attachments | [School Admin Intake](school-admin-intake.md) |
| Migrate from Tailscale to a self-hosted Headscale instance | [Tailscale to Headscale Migration](tailscale-to-headscale-migration.md) |

---

## All Playbooks

### [Air-gapped Provisioning](air-gapped-provisioning.md)
Workflow for securely transferring and verifying model weights (Ollama, vLLM, GGUF), vector datasets, and Kiwix ZIM archives onto disconnected or restricted networks.

**Stack**: Ollama · vLLM · Kiwix · Docker · sha256sum · FastMCP 3.1

---

### [Backup & Disaster Recovery](backup-disaster-recovery.md)
Comprehensive operational strategy for protecting homelab data and AI knowledge stores using a 3-2-1 backup topology with deduplicated, encrypted snapshots.

**Stack**: restic · BorgBackup · Kopia · MinIO / S3 · FastMCP 3.1

---

### [Data Copilot SQL Validation](data-copilot-sql-validation.md)
A technical blueprint and operational framework for validating AI-generated SQL queries before they reach production databases. Includes static analysis, dry-runs, AST mutation, and LLM-based semantic verification.

**Stack**: SQLGlot · Pydantic v2 · SQLite · PostgreSQL · Qwen 3.8 / Claude 5.1

---

### [Dev Workflow (AI-Assisted)](dev-workflow-ai-assisted.md)
Uses Claude Code, GitHub Actions, and local open-weight LLMs to accelerate development workflows — from issue triage to automated pull request creation and verification.

**Stack**: Claude Code · Ollama · GitHub Actions · n8n · FastMCP 3.1

---

### [Document Preparation for LLM Training](document-preparation-for-llm-training.md)
Normalizes `docx`, `pdf`, `pptx`, spreadsheets, and Google Workspace exports into machine-readable text plus metadata. Includes OCRmyPDF, Docling MCP, deduplication, and chunking guidance.

**Stack**: OCRmyPDF · Apache Tika · Docling MCP · Google Workspace CLI · Paperless-ngx

---

### [Email to Calendar](email-to-calendar.md)
Parses incoming emails to extract event details and creates calendar entries automatically via n8n and CalDAV. Handles multi-lingual extraction and ambiguous date/time formats.

**Stack**: n8n · Radicale (CalDAV) · Ollama · Paperless-ngx · Pydantic v2

---

### [Family Admin Automation](family-admin-automation.md)
Reduces manual overhead for household administration: school letters, medical records, appointments, shared task lists, and recurring paperwork are processed and routed automatically.

**Stack**: Paperless-ngx · n8n · Ollama · Nextcloud · Vikunja

---

### [Fully Offline Assistant](fully-offline-assistant.md)
Operates a completely private, air-gapped AI stack on local hardware. Integrates local inference engines, web interfaces, vector search, and offline knowledge bases.

**Stack**: Ollama · Open WebUI · Qdrant · Kiwix · FastMCP 3.1

---

### [Graceful Degradation](graceful-degradation.md)
Operationalizes cloud-to-local failover for LLM services during internet outages, provider rate-limiting, or cloud degradation events.

**Stack**: LiteLLM · Open WebUI · Ollama · vLLM · FastMCP 3.1

---

### [K3s Cluster Setup](k3s-cluster-setup.md)
Step-by-step operational guide for deploying a lightweight, 3-node highly available Kubernetes cluster using K3s with embedded etcd and automated ingress/DNS synchronization.

**Stack**: K3s · Ubuntu/Talos OS · etcd · External-DNS · Traefik

---

### [Knowledge Base Health](knowledge-base-health.md)
Audits document structure, catalog consistency, internal links, and metadata freshness. Generates a prioritized fix list and opens automated Jules remediation issues.

**Stack**: Python scripts · Jules · GitHub Actions · MkDocs Material

---

### [NFS CSI Setup](nfs-csi-setup.md)
Configures the NFS CSI driver on a K3s cluster to connect persistent volumes to TrueNAS SCALE or dedicated ZFS storage pools with dynamic provisioning verification.

**Stack**: K3s · TrueNAS SCALE · Helm · NFS CSI driver

---

### [Offline Transcription Pipeline](offline-transcription-pipeline.md)
Privacy-first workflow for converting audio and video recordings to formatted transcripts, summaries, and actionable tasks without cloud service exposure.

**Stack**: faster-whisper · Paperless-ngx · Vikunja · n8n · Pydantic v2

---

### [Raspberry Pi Kiosk Automation](raspberry-pi-kiosk-automation.md)
Configures a Raspberry Pi to display rotating dashboards (Home Assistant, Grocy, calendar) in kiosk mode without a full desktop environment, featuring auto-recovery and remote management.

**Stack**: Raspberry Pi OS Lite · Chromium · Home Assistant · Tailscale / Headscale

---

### [Scan to Task](scan-to-task.md)
Scans physical documents, executes OCR, extracts structured actionable items via LLM, and creates prioritized tasks in Vikunja with low end-to-end latency.

**Stack**: Paperless-ngx · Apache Tika · Ollama · Vikunja · n8n

---

### [School Admin Intake](school-admin-intake.md)
Monitors email and document repositories for school-related communications, classifies items (event / task / information), extracts key dates, and syncs to calendar and task lists.

**Stack**: n8n · Ollama · Radicale · Vikunja · Pydantic v2

---

### [Tailscale to Headscale Migration](tailscale-to-headscale-migration.md)
Outlines the steps required to migrate homelab nodes from Tailscale SaaS servers to a self-hosted Headscale instance for complete network sovereignty and privacy.

**Stack**: Headscale · Tailscale · Authentik · Docker

---

## Related

- [Tool Catalogue](../tools/README.md) — canonical docs for every tool used above
- [Architecture & Flows](../architecture/README.md) — how the automation pipelines are wired together
- [Contributing](../CONTRIBUTING.md) — how to add or improve a playbook

## Sources / References
- [Standards](../standards.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Architecture: Automated Contributions](../architecture/automated_contributions.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
