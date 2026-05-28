# Automation Flows

## What it is

Automation Flows represent the orchestration logic and sequential "pipelines" that connect disparate services in the home lab. They define how data moves from ingestion points (like scanners or email) through processing engines (OCR, LLMs) to final storage and notification sinks.

## What problem it solves

In a complex home lab with dozens of services, manual data entry and disjointed tool usage lead to "information silos" and cognitive load. Automation flows bridge these gaps by creating autonomous loops that handle repetitive tasks—like filing documents or updating calendars—without human intervention, ensuring consistency and saving time.

## Where it fits in the stack

**Category**: Architecture / Orchestration. Flows sit above individual services (like [Paperless-ngx](../services/paperless-ngx.md) or [Ollama](../services/ollama.md)), acting as the **connective tissue** that uses tools like [n8n](../services/n8n.md) or [Home Assistant](../services/home-assistant.md) to manage the lifecycle of an event or document.

## Typical use cases

### 1. School Activity Extraction
**Goal**: Automatically add school activities mentioned in emails to the family calendar.
1. **Ingest**: A new email arrives from the school domain.
2. **Store**: [n8n](../services/n8n.md) triggers on the email, extracts the PDF attachment, and uploads it to [Paperless-ngx](../services/paperless-ngx.md).
3. **Understand**: [Paperless-AI](../services/paperless-ai.md) (using [Ollama](../services/ollama.md)) scans the document for dates and event descriptions.
4. **Decide**: The AI determines if the document contains a calendar event. If yes, it formats the data (JSON).
5. **Act**: [n8n](../services/n8n.md) receives the JSON and creates an event in [Google Calendar](../tools/calendar_tasks/google_calendar.md).

### 2. Physical Mail to Action
**Goal**: Digitizing physical mail and creating follow-up tasks.
1. **Ingest**: Physical document is scanned using a mobile scanner app.
2. **Store**: The scan is saved to a folder monitored by [Syncthing](../services/syncthing.md).
3. **Process**: [OCRmyPDF](../tools/process_understanding/ocrmypdf.md) adds a searchable text layer.
4. **Understand**: [Paperless-ngx](../services/paperless-ngx.md) applies tags (e.g., "urgent").
5. **Act**: [Home Assistant](../services/home-assistant.md) sends a notification to the family chat.
6. **Sync**: A task is created in [Vikunja](../services/vikunja.md) with the document link.

### 3. Local Development to Automated Deployment
**Goal**: Streamlining the build and deployment of home scripts.
1. **Dev**: Use [Cursor](../tools/development_ops/cursor.md) or [Aider](../tools/development_ops/aider.md) to build a new script.
2. **Reason**: [Jules](../tools/ai_knowledge/jules.md) assists in writing tests and refactoring.
3. **Act**: Code is committed to a local [Gitea](../services/gitea.md) repository.
4. **Sync**: [n8n](../services/n8n.md) detects the commit and triggers a deployment to a Docker host.

### 4. KnowledgeOps Maintenance (The Ralph-loop)
**Goal**: Autonomous repository self-improvement and documentation freshness.
1. **Ingest**: Daily scripts scan for new tool releases, GitHub stars, and stale documentation.
2. **Bridge**: Qualifying items are staged in [`docs/new-sources/`](new-sources.md).
3. **Trigger**: GitHub Actions open a "Jules" issue with the `jules` label.
4. **Execute**: [Jules](../tools/ai_knowledge/jules.md) follows the Ralph-loop (Work, Link, or Decompose) to resolve the issue.
5. **Verify**: Automated quality gates (`audit_docs_quality.py`, `check_docs_contract.py`) validate the changes before merge.

## Strengths

- **Consistency**: Ensures every document or event is handled according to the same rules every time.
- **Speed**: Processing happens in seconds or minutes, much faster than manual sorting.
- **Traceability**: Audit logs in [n8n](../services/n8n.md) or [Home Assistant](../services/home-assistant.md) provide a clear history of how data was processed.
- **Integration**: Combines "dumb" storage with "smart" AI reasoning engines seamlessly.

## Limitations

- **Brittle**: Changes in external APIs (like school email formats) can break extraction logic.
- **Complexity**: Debugging a flow that spans five different services requires significant technical knowledge.
- **Resource Heavy**: Complex AI-driven flows can spike CPU/RAM usage on the home server.

## When to use it

- When you have repetitive tasks that involve moving data between two or more services.
- When you want to apply "intelligence" (like LLM classification) to incoming data automatically.
- When you need to ensure that physical records are reliably digitized and indexed.

## When not to use it

- For one-off tasks that take less time to do manually than to automate.
- When the data is highly sensitive and you are uncomfortable with an LLM (even a local one) processing it.
- If the "cost" of automation failure (e.g., missing a medical appointment) outweighs the benefit of autonomy.

## Related tools / concepts

- [n8n](../services/n8n.md) — The primary workflow engine for complex multi-step logic.
- [Home Assistant](../services/home-assistant.md) — For event-driven automation and notifications.
- [Paperless-ngx](../services/paperless-ngx.md) — The central repository for digitized documents.
- [Ollama](../services/ollama.md) — Provides the local reasoning power for understanding content.
- [Vikunja](../services/vikunja.md) — The target destination for actionable tasks derived from flows.
- [Syncthing](../services/syncthing.md) — For moving files from mobile devices into the ingestion pipeline.
- [Gitea](../services/gitea.md) — For versioning the scripts that power these automations.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Often used within flows to provide context to the processing LLM.

## Contribution Metadata

- Last reviewed: 2026-05-28
- Confidence: high

## Sources / References

- [n8n Documentation](https://docs.n8n.io/)
- [Home Assistant Automation Docs](https://www.home-assistant.io/docs/automation/)
- [Local LLM Workflow Patterns](https://github.com/joanmarcriera/Home-office-automations)
