# Automation Flows

This document describes typical end-to-end automation scenarios within the home lab and family automation stack.

## 1. School Activity Extraction
**Goal**: Automatically add school activities mentioned in emails to the family calendar.

1. **Ingest**: A new email arrives from the school domain.
2. **Store**: [n8n](../services/n8n.md) triggers on the email, extracts the PDF attachment, and uploads it to [Paperless-ngx](../services/paperless-ngx.md).
3. **Understand**: [Paperless-AI](../services/paperless-ai.md) (using [Ollama](../services/ollama.md)) scans the document for dates and event descriptions.
4. **Decide**: The AI determines if the document contains a calendar event. If yes, it formats the data (JSON).
5. **Act**: [n8n](../services/n8n.md) receives the JSON and creates an event in [Google Calendar](../tools/calendar_tasks/google_calendar.md).
6. **Sync**: The event is automatically synced to the family's shared calendar via [CalDAV](../tools/intake_storage/caldav.md) or native apps.

## 2. Physical Mail to Action
**Goal**: Digitizing physical mail and creating follow-up tasks.

1. **Ingest**: Physical document is scanned using a mobile scanner app or dedicated hardware.
2. **Store**: The scan is saved to a folder monitored by [Syncthing](../services/syncthing.md) or uploaded directly to [Nextcloud](../services/nextcloud.md).
3. **Process**: [OCRmyPDF](../tools/process_understanding/ocrmypdf.md) automatically adds a searchable text layer.
4. **Understand**: [Paperless-ngx](../services/paperless-ngx.md) ingest the document and applies tags (e.g., "urgent", "invoice").
5. **Act**: [Home Assistant](../services/home-assistant.md) detects a new "urgent" document and sends a notification to the family chat.
6. **Sync**: A corresponding task is created in [Vikunja](../services/vikunja.md) with the document link for follow-up.

## 3. Local Development to Automated Deployment
**Goal**: Streamlining the creation and deployment of home automation scripts.

1. **Dev**: Developer uses [Cursor](../tools/development_ops/cursor.md) or [Aider](../tools/development_ops/aider.md) to build a new Python script.
2. **Reason**: [Jules](../tools/ai_knowledge/jules.md) assists in writing tests and refactoring the code for reliability.
3. **Act**: Code is committed to local [GitHub](https://github.com) or Gitea repository.
4. **Sync**: [Cloud Code](../tools/development_ops/cloud_code.md) or [n8n](../services/n8n.md) detects the commit and triggers a deployment to the local Kubernetes cluster or a Docker host.
5. **Verify**: Automated agents in [Anti-Gravity](../tools/development_ops/anti_gravity.md) verify the live deployment by running browser-based tests.
