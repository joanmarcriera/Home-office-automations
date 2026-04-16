# Roadmap and Gaps

This document tracks missing components and planned technical improvements for the homelab automation stack.

## Missing Pieces (Must-Haves)
- **Centralized Error Queue**: A unified dashboard (e.g. specialized Home Assistant view) to see all failed n8n workflows.
- **Human-in-the-Loop (HITL) UI**: A simple web interface to approve or correct AI-extracted dates before they hit the calendar.
- [x] **Audit Trail**: Logging which LLM version and prompt version was used for every document extraction (see [Standards](docs/standards.md)).

## Nice-to-Haves
- **Multi-Calendar Conflict Detection**: Checking both husband and wife's calendars before suggesting an event time.
- **Voice-to-Task**: Integrating [Ollama](./services/ollama.md) with local voice-to-text for hands-free task creation.
- **Automated Retention**: Scripts to automatically delete `Ephemeral` tagged documents after 30 days.

## 🌟 Future Projects (Home-Centric AI)

### Home Operations
- **AI-Powered Warranty & Manual Assistant**:
    - *Goal*: Automatically track warranty expiration from scanned receipts and provide chat-based troubleshooting using scanned manuals.
    - *Stack*: [Paperless-ngx](./services/paperless-ngx.md), [n8n](./services/n8n.md), local LLM (RAG).
- **Smart Energy Anomaly Detection**:
    - *Goal*: Use local reasoning to detect unusual power spikes or appliances left on, providing proactive alerts.
    - *Stack*: [Home Assistant](./services/home-assistant.md), [Ollama](./services/ollama.md).

### Family Knowledge Management
- **Personalized Family "Daily Briefing"**:
    - *Goal*: A unified morning report (voice or chat) summarizing the day's schedule, chores, weather, and "On This Day" memories.
    - *Stack*: [n8n](./services/n8n.md), [Vikunja](./services/vikunja.md), [Google Calendar](./tools/calendar_tasks/google_calendar.md).
- **Semantic Search for Family History**:
    - *Goal*: Natural language search across decades of family documents, journals, and logs.
    - *Stack*: [Paperless-ngx](./services/paperless-ngx.md), [Obsidian](./tools/ai_knowledge/obsidian.md), local Vector DB.

### Media & Entertainment
- **AI-Categorized Home Video Archive**:
    - *Goal*: Automated tagging and semantic search for home videos (e.g., "Find the video of the birthday party").
    - *Stack*: Local vision models (CLIP/Whisper), TrueNAS storage.
- **Local Audio Library Enrichment**:
    - *Goal*: Automated transcription of personal audiobooks and podcasts for full-text search.
    - *Stack*: Whisper (local), [Ollama](./services/ollama.md).

### Advanced Infrastructure
- **Self-Healing Homelab Agent**:
    - *Goal*: An AI agent that monitors [TrueNAS SCALE](architecture/infrastructure.md) logs and automatically restarts services or alerts on hardware failure.
    - *Stack*: [n8n](./services/n8n.md), [Tailscale](./services/tailscale.md), local specialized agent.
- **Sovereign Identity & SSO**:
    - *Goal*: Fully self-hosted single sign-on for all family members across all services.
    - *Stack*: Authentik or LL-LDAP.

## Technical Next Steps

### Short-Term
- [x] Add [webhook-based ingestion](docs/reference-implementations/paperless/webhook-ingestion.md) for Paperless-ngx.
- [x] Refine [Task Extraction Prompt](reference-implementations/llm-prompts/extraction-and-classification.md) for better priority detection.
- [x] Standardize [n8n](./services/n8n.md) error handling using sub-workflows (see [Error Handling Pattern](docs/knowledge_base/patterns/n8n-error-handling.md)).
- [x] Roll out the Multi-Agent KnowledgeOps contract (see [Standards](docs/standards.md)).

### Medium-Term
- [ ] Implement [Headscale](./services/tailscale.md) for a fully self-hosted mesh network.
    - [ ] Deploy Headscale container.
    - [ ] Configure OIDC for Headscale.
    - [ ] Migrate first 3 nodes from Tailscale SaaS to Headscale.
- [ ] Integrate [Vikunja](./services/vikunja.md) task dependencies into n8n flows.
    - [ ] Create n8n node/workflow for "Get Task Dependencies".
    - [ ] Implement logic to delay task start until blockers are closed.
- [ ] Deploy [LiteLLM](./services/litellm.md) proxy.
    - [ ] Configure local Ollama and OpenAI as backends.
    - [ ] Implement API key management for internal services.

### Long-Term
- [ ] Build a custom "Home Admin Agent" using [LangChain](./tools/ai_knowledge/langchain.md).
    - [ ] Implement RAG over Paperless-ngx documents.
    - [ ] Integrate agent with Vikunja for task status updates.
    - [ ] Add voice interface via Whisper/Piper.
- [ ] Full migration to Kubernetes (K3s) for all homelab services.
    - [ ] Set up 3-node K3s cluster.
    - [ ] Define Helm charts for core services (n8n, Paperless).
    - [ ] Implement Longhorn for distributed storage.
