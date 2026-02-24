# Roadmap and Gaps

This document tracks missing components and planned technical improvements for the homelab automation stack.

## Missing Pieces (Must-Haves)
- **Centralized Error Queue**: A unified dashboard (e.g. specialized Home Assistant view) to see all failed n8n workflows.
- **Human-in-the-Loop (HITL) UI**: A simple web interface to approve or correct AI-extracted dates before they hit the calendar.
- **Audit Trail**: Logging which LLM version and prompt version was used for every document extraction.

## Nice-to-Haves
- **Multi-Calendar Conflict Detection**: Checking both husband and wife's calendars before suggesting an event time.
- **Voice-to-Task**: Integrating [Ollama](docs/tools/process_understanding/ollama.md) with local voice-to-text for hands-free task creation.
- **Automated Retention**: Scripts to automatically delete `Ephemeral` tagged documents after 30 days.

## Technical Next Steps

### Short-Term
- [ ] Add webhook-based ingestion for Paperless-ngx (switching from polling consumption folder).
- [ ] Refine [Task Extraction Prompt](reference-implementations/llm-prompts/extraction-and-classification.md) for better priority detection.
- [ ] Standardize [n8n](docs/tools/automation_orchestration/n8n.md) error handling using sub-workflows.

### Medium-Term
- [ ] Implement [Headscale](docs/tools/automation_orchestration/tailscale.md) for a fully self-hosted mesh network.
- [ ] Integrate [Vikunja](docs/tools/calendar_tasks/google_calendar.md) task dependencies into n8n flows.
- [ ] Deploy [LiteLLM](docs/tools/process_understanding/litellm.md) proxy to load-balance between local and cloud models.

### Long-Term
- [ ] Build a custom "Home Admin Agent" using [LangChain](docs/tools/ai_knowledge/langchain.md) that can reason across the entire document store.
- [ ] Full migration to Kubernetes (K3s) for all homelab services to improve resilience.
