# Roadmap and Gaps

This document tracks missing components and planned technical improvements for the homelab automation stack.

## Missing Pieces (Must-Haves)
- **Centralized Error Queue**: A unified dashboard (e.g. specialized Home Assistant view) to see all failed n8n workflows.
    - [x] Research dashboard tools for n8n error visualization (e.g., Home Assistant, custom Grafana dashboard).
    - [x] Define a standardized error schema for n8n sub-workflows (status, model, workflow_id, timestamp).
    - [x] Implement a "Push to Error Queue" sub-workflow in n8n for global reuse (see [Error Handler Workflow](docs/reference-implementations/n8n/error-handler.json)).
    - [x] Create a basic Home Assistant dashboard to display the error queue via REST sensor or MQTT (see [Dashboard Config](docs/knowledge_base/patterns/n8n-error-handling.md)).

- **Human-in-the-Loop (HITL) UI**: A simple web interface to approve or correct AI-extracted dates before they hit the calendar.
    - [x] Define Backend API endpoints (GET `/staged-docs`, POST `/approve/{id}`, POST `/reject/{id}`) (see [HITL UI Design](docs/reference-implementations/hitl-ui-design.md)).
    - [x] Select Frontend framework (Streamlit for rapid prototyping vs React for durability).
    - [x] Design database schema for staged extractions (staged_at, original_metadata, corrected_metadata).
    - [x] Implement reference implementation for HITL UI (see [HITL UI Implementation](docs/reference-implementations/hitl-ui/)).
    - [x] Integrate verified dates with Google/Proton Calendar:
        - [x] Implement Google Calendar API integration (POST /events) (see [Reference Script](scripts/gcal_sync_reference.py)).
        - [x] Implement Proton Calendar event creation via [Chronos MCP](./tools/automation_orchestration/chronos-mcp.md) (see [Reference Script](scripts/chronos_sync_reference.py)).

- [x] **Audit Trail**: Logging which LLM version and prompt version was used for every document extraction (see [Standards](docs/standards.md)).

## Nice-to-Haves
- **Multi-Calendar Conflict Detection**: Checking both husband and wife's calendars before suggesting an event time.
    - [x] Research Google Calendar Free/Busy API for availability checks (see [Multi-Calendar Research](docs/knowledge_base/multi-calendar-conflict-research.md)).
    - [x] Research [Chronos MCP](./tools/automation_orchestration/chronos-mcp.md) for multi-calendar reading capabilities (see [Multi-Calendar Research](docs/knowledge_base/multi-calendar-conflict-research.md)).
    - [x] Implement n8n logic to aggregate availability and identify conflicts (see [Multi-Calendar Conflict Checker](docs/reference-implementations/n8n/multi-calendar-conflict-checker.json)).
        - [x] Design n8n workflow to fetch Free/Busy data from multiple Google accounts.
        - [x] Implement JSON logic to find overlapping busy slots and identify available 'free' gaps.
        - [x] Create n8n 'Conflict Alert' notification for Telegram.
- **Voice-to-Task**: Integrating [Ollama](./services/ollama.md) with local voice-to-text for hands-free task creation.
    - [x] Research Whisper.cpp for local high-performance Speech-to-Text (STT) (see [Voice-to-Task Research](docs/knowledge_base/voice-to-task-research.md)).
    - [x] Integrate STT with Home Assistant Assist voice pipeline (see [Voice-to-Task Research](docs/knowledge_base/voice-to-task-research.md)).
    - [x] Create n8n trigger to process voice-extracted tasks and route to Vikunja (see [Voice to Vikunja](docs/reference-implementations/n8n/voice-to-vikunja.json)).
        - [x] Deploy Wyoming-Whisper container on the compute node.
        - [x] Configure 'Voice Assistant' in Home Assistant using the Wyoming STT service.
        - [x] Create n8n webhook trigger to receive transcribed text from HA and parse into Vikunja tasks.
- [x] **Automated Retention**: Scripts to automatically delete `Ephemeral` tagged documents after 30 days (see `scripts/paperless_retention.py`).

## 🌟 Future Projects (Home-Centric AI)

### Home Operations
- **AI-Powered Warranty & Manual Assistant**:
    - *Goal*: Automatically track warranty expiration from scanned receipts and provide chat-based troubleshooting using scanned manuals.
    - *Stack*: [Paperless-ngx](./services/paperless-ngx.md), [n8n](./services/n8n.md), local LLM (RAG).
    - [x] Define Paperless-ngx tag schema for warranties and manuals.
    - [x] Create n8n workflow to extract expiration dates from warranty documents (see [Warranty Extraction Prompt](docs/reference-implementations/llm-prompts/warranty-extraction.md)).
    - [x] Set up Vector DB index for scanned manuals:
        - [x] Research Milvus vs Chroma vs Qdrant for local manual RAG storage (see [Vector DB Comparison](docs/knowledge_base/vector-db-comparison.md)).
        - [x] Design metadata schema for manuals (model number, manufacturer, year, document type) (see [Manuals Schema](docs/reference-implementations/metadata-schemas/manuals.md)).
        - [ ] Implement chunking and embedding pipeline for OCR'd PDF manuals.
            - [ ] Create Python script for section-aware PDF chunking using `PyMuPDF` or `LangChain`.
            - [ ] Implement metadata extraction logic to pull `model_number` and `manufacturer` from OCR text.
            - [ ] Configure ChromaDB or Qdrant collection for manual storage.
        - [ ] Verify retrieval accuracy and relevance with a test set of common household manuals.
    - [ ] Implement chat-based troubleshooting interface using RAG over manuals.
        - [ ] Create Streamlit or Open WebUI frontend for "Manual Assistant".
        - [ ] Implement n8n or Python backend for hybrid search (keyword + vector).
- **Smart Energy Anomaly Detection**:
    - *Goal*: Use local reasoning to detect unusual power spikes or appliances left on, providing proactive alerts.
    - *Stack*: [Home Assistant](./services/home-assistant.md), [Ollama](./services/ollama.md).
    - [x] Identify candidate power monitoring sensors in Home Assistant for key appliances (Washer, Fridge, EV) (see [Baseline Logic](docs/knowledge_base/energy-anomaly-detection-baseline.md)).
    - [x] Research Home Assistant "Utility Meter" and "Derivative" sensors for baseline usage patterns.
    - [x] Define baseline vs anomaly logic (e.g., spike duration, time-of-day weighting) in a new reference implementation file.
    - [x] Create n8n workflow for LLM-based reasoning using Ollama node to classify spikes as "Normal" or "Anomaly" (see [Workflow Template](docs/reference-implementations/n8n/energy-anomaly-classifier.json)).

### Family Knowledge Management
- **Personalized Family "Daily Briefing"**:
    - *Goal*: A unified morning report (voice or chat) summarizing the day's schedule, chores, weather, and "On This Day" memories.
    - *Stack*: [n8n](./services/n8n.md), [Vikunja](./services/vikunja.md), [Google Calendar](./tools/calendar_tasks/google_calendar.md).
    - [x] Research n8n "Google Calendar" and "Vikunja" nodes for event aggregation (see [Integration Details](docs/reference-implementations/llm-prompts/daily-briefing.md)).
    - [x] Design Daily Briefing prompt template in `docs/reference-implementations/llm-prompts/daily-briefing.md`.
    - [x] Implement n8n workflow for scheduled morning delivery via Telegram/Email (see [Workflow Template](docs/reference-implementations/n8n/daily-briefing-flow.json)).
- **Semantic Search for Family History**:
    - *Goal*: Natural language search across decades of family documents, journals, and logs.
    - *Stack*: [Paperless-ngx](./services/paperless-ngx.md), [Obsidian](./tools/ai_knowledge/obsidian.md), local Vector DB.
    - [x] Define Paperless-ngx document types for historical archives (see [Tag Taxonomy](reference-implementations/paperless/tag-taxonomy.md)).
    - [x] Research vector embedding scripts for Obsidian journals (see [Obsidian Vector Search](docs/knowledge_base/obsidian-vector-search.md)).
    - [ ] Set up local Vector DB index for OCR'd text search.
        - [ ] Export OCR'd text from Paperless-ngx via API.
        - [ ] Implement incremental indexing for new Obsidian vault entries.
        - [ ] Create a unified search CLI for cross-source (Paperless + Obsidian) queries.

### Media & Entertainment
- **AI-Categorized Home Video Archive**:
    - *Goal*: Automated tagging and semantic search for home videos (e.g., "Find the video of the birthday party").
    - *Stack*: Local vision models (CLIP/Whisper), TrueNAS storage.
    - [x] Research local vision models for video frame embedding (see [Vision Models Research](docs/knowledge_base/vision-models-research.md)).
    - [ ] Prototype metadata extraction script using Whisper and CLIP.
    - [ ] Set up Vector DB for semantic search over video metadata.
- **Local Audio Library Enrichment**:
    - *Goal*: Automated transcription of personal audiobooks and podcasts for full-text search.
    - *Stack*: Whisper (local), [Ollama](./services/ollama.md).

### Advanced Infrastructure
- **Self-Healing Homelab Agent**:
    - *Goal*: An AI agent that monitors [TrueNAS SCALE](architecture/infrastructure.md) logs and automatically restarts services or alerts on hardware failure.
    - *Stack*: [n8n](./services/n8n.md), [Tailscale](./services/tailscale.md), local specialized agent.
    - [x] Research TrueNAS SCALE log streaming via syslog or webhooks for real-time monitoring (see [Self-Healing Agent Research](docs/knowledge_base/self-healing-agent-research.md)).
    - [x] Identify critical service health check endpoints (e.g., Paperless-ngx, Home Assistant).
    - [x] Define automated restart logic for Docker containers vs K3s pods.
- **Sovereign Identity & SSO**:
    - *Goal*: Fully self-hosted single sign-on for all family members across all services.
    - *Stack*: Authentik or LL-LDAP.
    - [x] Research Authentik vs Kanidm vs LL-LDAP for family use (see [SSO Comparison](docs/knowledge_base/sso-comparison.md)).
    - [x] Deploy chosen SSO solution via Docker (see [Authentik Service](docs/services/authentik.md)).
    - [x] Configure OIDC for first 3 services (Nextcloud, Vikunja, Gitea).
    - [x] Set up 2FA for all family member accounts (see [Authentik 2FA Guide](docs/services/authentik.md#family-2fa-onboarding)).

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
- [x] Deploy [LiteLLM](./services/litellm.md) proxy.
    - [x] Configure Prometheus/Grafana monitoring for LiteLLM.
    - [x] Implement usage-based quotas for internal API keys.
    - [x] Set up load balancing between multiple Ollama instances.
    - [x] Configure local Ollama and OpenAI as backends.
    - [x] Implement API key management for internal services.

### Long-Term
- [ ] Build a custom "Home Admin Agent" using [LangChain](./tools/ai_knowledge/langchain.md).
    - [ ] **Agent Architecture**:
        - [ ] Design LangChain agent structure and tool definitions.
        - [ ] Research and select state management for agent memory (e.g., LangGraph).
        - [ ] Implement persistent checkpointer for long-running family tasks.
    - [ ] **Tool Integrations**:
        - [ ] Implement Paperless-ngx tool for RAG retrieval using `langchain-community` document loaders.
        - [ ] Integrate agent with Vikunja for task status updates and creation via Vikunja API.
        - [ ] Create a "Calendar Tool" using Chronos MCP / Google Calendar API.
        - [ ] Add "Home Assistant Tool" to control lights/scenes via the agent.
    - [ ] **User Interface**:
        - [ ] Implement a simple Chat UI for the agent.
        - [ ] Add voice interface via local Whisper (STT) and Piper (TTS).
- [ ] Full migration to Kubernetes (K3s) for all homelab services.
    - [ ] Evaluate [Talos OS](https://www.talos.dev/) vs Ubuntu for node OS.
    - [ ] **Networking & Ingress**:
        - [ ] **Load Balancing**: Configure [MetalLB](https://metallb.universe.tf/) for LoadBalancer support in Layer2 mode.
        - [ ] **Ingress Controller**: Set up [Traefik](https://traefik.io/traefik/) or Ingress-Nginx to handle incoming traffic.
        - [ ] **TLS Management**: Install [Cert-Manager](https://cert-manager.io/) and configure Let's Encrypt with DNS-01 challenge for internal services.
        - [ ] **DNS Automation**: Configure External-DNS for automated DNS record management with local/cloud providers.
    - [ ] **Storage**:
        - [ ] **Distributed Storage**: Implement Longhorn for high-availability distributed block storage across nodes.
        - [ ] **Legacy Integration**: Configure NFS CSI driver for persistent volumes stored on TrueNAS SCALE.
    - [ ] **Compute**:
        - [ ] Set up 3-node K3s cluster.
        - [ ] Implement node affinity/taints for specialized workloads (e.g., GPU).
    - [ ] **Deployment & Observability**:
        - [ ] Define Helm charts for core services (n8n, Paperless).
        - [ ] Set up Prometheus/Grafana stack for cluster monitoring.
