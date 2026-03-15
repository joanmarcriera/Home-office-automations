# Operational Playbooks

Step-by-step execution guides for recurring workflows. Each playbook is self-contained: it lists prerequisites, the exact sequence of steps, the tools involved, and how to verify the outcome.

## Choose by Goal

| If you want to… | Use this playbook |
| :--- | :--- |
| Automate a coding or review task end-to-end with AI assistance | [Dev Workflow (AI-Assisted)](dev-workflow-ai-assisted.md) |
| Route emails into calendar events automatically | [Email to Calendar](email-to-calendar.md) |
| Automate household paperwork — school letters, appointments, admin | [Family Admin Automation](family-admin-automation.md) |
| Display dashboards or a kiosk on a Raspberry Pi without a desktop | [Raspberry Pi Kiosk Automation](raspberry-pi-kiosk-automation.md) |
| Convert a scanned document into an actionable task | [Scan to Task](scan-to-task.md) |
| Ingest and process school admin emails, letters, or attachments | [School Admin Intake](school-admin-intake.md) |
| Audit, repair, or improve the knowledge base and documentation | [Knowledge Base Health](knowledge-base-health.md) |

---

## All Playbooks

### [Dev Workflow (AI-Assisted)](dev-workflow-ai-assisted.md)
Uses Claude Code, GitHub, and local LLMs to accelerate coding tasks — from issue triage to PR creation. Covers prompt engineering tips, safe automation boundaries, and review checkpoints.

**Stack**: Claude Code · Ollama · GitHub Actions · n8n

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

## Related

- [Tool Catalogue](../tools/README.md) — canonical docs for every tool used above
- [Architecture & Flows](../architecture/README.md) — how the automation pipelines are wired together
- [Contributing](../CONTRIBUTING.md) — how to add or improve a playbook

## Sources / References
- [Standards](../standards.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Architecture: Automated Contributions](../architecture/automated_contributions.md)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: high
