# Component Map

This map categorizes all tools in the stack based on their primary function in the information and automation pipeline.

## 1. Ingest
*Tools responsible for receiving or capturing raw information.*
- **Email (IMAP)**: [Paperless-ngx](../tools/intake_storage/paperless-ngx.md), [n8n](../tools/automation_orchestration/n8n.md)
- **Scanning**: [OCRmyPDF](../tools/process_understanding/ocrmypdf.md)
- **Manual Input**: [Obsidian](../tools/ai_knowledge/obsidian.md), [Logseq](../tools/ai_knowledge/logseq.md)
- **Inventory**: [Homebox](../tools/intake_storage/homebox.md), [Grocy](../tools/intake_storage/grocy.md)

## 2. Store
*Tools where information resides in a persistent state.*
- **Document Archive**: [Paperless-ngx](../tools/intake_storage/paperless-ngx.md)
- **File Sync/Cloud**: [Nextcloud](../tools/intake_storage/nextcloud.md), [Syncthing](../tools/intake_storage/syncthing.md)
- **Calendars/Contacts**: [Radicale](../tools/intake_storage/radicale.md), [Google Calendar](../tools/calendar_tasks/google_calendar.md)

## 3. Understand (Process & Reason)
*Tools that transform raw data into structured insights or actionable intelligence.*
- **OCR**: [OCRmyPDF](../tools/process_understanding/ocrmypdf.md), [Tika](../tools/process_understanding/tika.md)
- **Reasoning Engines**: [Ollama](../tools/process_understanding/ollama.md), [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Jules](../tools/ai_knowledge/jules.md)
- **Semantic Search**: [Paperless-AI](../tools/process_understanding/paperless-ai.md)
- **Research**: [Perplexity](../tools/ai_knowledge/perplexity.md)

## 4. Decide (Orchestrate)
*Tools that determine which actions to take based on processed information.*
- **Workflow Engines**: [n8n](../tools/automation_orchestration/n8n.md), [Home Assistant](../tools/automation_orchestration/home_assistant.md)
- **Cloud Connectors**: [Zapier](../tools/automation_orchestration/zapier.md), [Make](../tools/automation_orchestration/make.md)
- **Agent Frameworks**: [LangChain](../tools/ai_knowledge/langchain.md), [LlamaIndex](../tools/ai_knowledge/llamaindex.md), [Dify](../tools/ai_knowledge/dify.md), [Flowise](../tools/ai_knowledge/flowise.md)

## 5. Act
*Tools that perform physical or digital modifications to the environment.*
- **Home Control**: [Home Assistant](../tools/automation_orchestration/home_assistant.md)
- **Task Management**: [Vikunja](../tools/calendar_tasks/vikunja.md)
- **Development**: [VS Code](../tools/development_ops/vscode.md), [Cursor](../tools/development_ops/cursor.md), [Aider](../tools/development_ops/aider.md), [OpenHands](../tools/development_ops/openhands.md), [Anti-Gravity](../tools/development_ops/anti_gravity.md)

## 6. Sync
*Tools that ensure information is consistent across devices and platforms.*
- **Network Access**: [Tailscale](../tools/automation_orchestration/tailscale.md)
- **Protocols**: [CalDAV](../tools/intake_storage/caldav.md)
- **Model Proxy**: [LiteLLM](../tools/process_understanding/litellm.md)
