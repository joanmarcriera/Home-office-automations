# Operational Playbooks

Step-by-step execution guides for recurring workflows. Each playbook is self-contained: it lists prerequisites, the exact sequence of steps, the tools involved, and how to verify the outcome.

## Choose by Goal

| If you want to… | Use this playbook |
| :--- | :--- |
| Automate a coding or review task end-to-end with AI assistance | [Dev Workflow (AI-Assisted)](dev-workflow-ai-assisted.md) |
| Prepare office documents for LLM training or retrieval ingestion | [Document Preparation for LLM Training](document-preparation-for-llm-training.md) |
| Route emails into calendar events automatically | [Email to Calendar](email-to-calendar.md) |
| Automate household paperwork — school letters, appointments, admin | [Family Admin Automation](family-admin-automation.md) |
| Display dashboards or a kiosk on a Raspberry Pi without a desktop | [Raspberry Pi Kiosk Automation](raspberry-pi-kiosk-automation.md) |
| Convert a scanned document into an actionable task | [Scan to Task](scan-to-task.md) |
| Ingest and process school admin emails, letters, or attachments | [School Admin Intake](school-admin-intake.md) |
| Audit, repair, or improve the knowledge base and documentation | [Knowledge Base Health](knowledge-base-health.md) |
| Configure NFS CSI driver for persistent volumes on K3s | [NFS CSI Setup](nfs-csi-setup.md) |
| Deploy a 3-node HA cluster for resilient workloads | [K3s Cluster Setup](k3s-cluster-setup.md) |
| Validate AI-generated SQL queries for safety and performance | [Data Copilot SQL Validation](data-copilot-sql-validation.md) |
| Migrate from Tailscale to a self-hosted Headscale instance | [Tailscale to Headscale Migration](tailscale-to-headscale-migration.md) |
| Deploy a private, air-gapped AI stack locally | [Fully Offline Assistant](fully-offline-assistant.md) |
| Configure automatic cloud-to-local failover | [Graceful Degradation](graceful-degradation.md) |
| Protect critical data with a 3-2-1 backup strategy | [Backup & Disaster Recovery](backup-disaster-recovery.md) |
| Transfer models and ZIMs to air-gapped servers | [Air-gapped Provisioning](air-gapped-provisioning.md) |
| Transcribe audio and extract tasks locally | [Offline Transcription Pipeline](offline-transcription-pipeline.md) |

---

## All Playbooks

### [Dev Workflow (AI-Assisted)](dev-workflow-ai-assisted.md)
Uses Claude Code, GitHub, and local LLMs to accelerate coding tasks — from issue triage to PR creation. Covers prompt engineering tips, safe automation boundaries, and review checkpoints.

**Stack**: Claude Code · Ollama · GitHub Actions · n8n

---

### [Document Preparation for LLM Training](document-preparation-for-llm-training.md)
Normalizes `docx`, `pdf`, `pptx`, spreadsheet files, and Google Workspace exports into machine-readable text plus metadata. Includes OCR, deduplication, and selective merge guidance for fragmented corpora.

**Stack**: OCRmyPDF · Apache Tika · Docling MCP · Google Workspace CLI · Paperless-ngx

---

### [Email to Calendar](email-to-calendar.md)
Parses incoming emails to extract event details and creates calendar entries automatically via n8n and CalDAV. Handles multiple languages and ambiguous date formats.

**Stack**: n8n · Radicale (CalDAV) · Ollama · Paperless-ngx

---

### [Family Admin Automation](family-admin-automation.md)
Reduces manual overhead for household administration: school letters, appointments, shared task lists, and recurring paperwork are processed and routed to the right place automatically.

**Stack**: Paperless-ngx · n8n · Ollama · Nextcloud

---

### [Raspberry Pi Kiosk Automation](raspberry-pi-kiosk-automation.md)
Sets up a Pi to display a rotating dashboard (Home Assistant, Grocy, calendar) in kiosk mode with no desktop environment, auto-recovery on crash, and remote management via Tailscale.

**Stack**: Raspberry Pi OS Lite · Chromium · Home Assistant · Tailscale

---

### [Scan to Task](scan-to-task.md)
Scans a physical document, runs OCR, extracts actionable items via LLM, and creates tasks in Vikunja. End-to-end latency under 60 seconds from scan to task creation.

**Stack**: Paperless-ngx · Apache Tika · Ollama · Vikunja · n8n

---

### [School Admin Intake](school-admin-intake.md)
Watches an email folder for school-related messages, classifies them (event / action / info), extracts due dates, and routes to calendar or task list accordingly.

**Stack**: n8n · Ollama · Radicale · Vikunja

---

### [Knowledge Base Health](knowledge-base-health.md)
Audits doc structure, catalog consistency, broken links, and stale metadata. Generates a prioritised fix list and optionally opens Jules issues for automated remediation.

**Stack**: Python scripts · Jules · GitHub Actions · MkDocs

---

### [NFS CSI Setup](nfs-csi-setup.md)
Step-by-step instructions for configuring the NFS CSI driver on a K3s cluster to use persistent storage hosted on a TrueNAS SCALE server. Covers driver installation, StorageClass configuration, and dynamic provisioning verification.

**Stack**: K3s · TrueNAS SCALE · Helm · NFS CSI

---

### [Data Copilot SQL Validation](data-copilot-sql-validation.md)
A technical blueprint and operational framework for validating AI-generated SQL queries before they reach the database. Includes static analysis, dry-runs, and LLM-based semantic checks.

**Stack**: SQLGlot · Pydantic · SQLite · Qwen 2.5 7B

---

### [Tailscale to Headscale Migration](tailscale-to-headscale-migration.md)
Outlines the steps required to migrate homelab nodes from the Tailscale SaaS coordination server to a self-hosted Headscale instance for 100% data sovereignty.

**Stack**: Headscale · Tailscale · Authentik · Docker

---

### [K3s Cluster Setup](k3s-cluster-setup.md)
Step-by-step operational guide for deploying a lightweight, 3-node highly available Kubernetes cluster using K3s with embedded etcd.

**Stack**: K3s · Ubuntu/Talos OS · etcd

---

### [Fully Offline Assistant](fully-offline-assistant.md)
Operates a private AI stack on local hardware. Integrates inference, interface, local embeddings, and offline knowledge.

**Stack**: Ollama · Open WebUI · Qdrant · Kiwix

---

### [Graceful Degradation](graceful-degradation.md)
Operationalizes cloud-to-local failover for LLM services during outages or rate-limiting events.

**Stack**: LiteLLM · Open WebUI · Ollama

---

### [Backup & Disaster Recovery](backup-disaster-recovery.md)
Comprehensive strategy for protecting homelab data using a 3-2-1 approach with deduplicated, encrypted snapshots.

**Stack**: restic · BorgBackup · Kopia · S3

---

### [Air-gapped Provisioning](air-gapped-provisioning.md)
Workflow for securely transferring and verifying models and knowledge artifacts onto disconnected servers.

**Stack**: Ollama · Kiwix · Docker · sha256sum

---

### [Offline Transcription Pipeline](offline-transcription-pipeline.md)
Privacy-first workflow for converting audio to text and tasks without cloud exposure.

**Stack**: faster-whisper · Paperless-ngx · Vikunja · n8n

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
- Last reviewed: 2026-05-30
- Confidence: high
