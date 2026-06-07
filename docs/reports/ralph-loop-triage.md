# Ralph-loop Triage Report — 2026-05-25

This report documents the triage of open GitHub issues and ongoing maintenance tasks as of May 25, 2026.

## Issue Status Summary

| Issue # | Title | Status | Notes |
| :--- | :--- | :--- | :--- |
| **#186-#190** | Data Copilot Series | **Verified & Closed** | Architecture, MCP, RAG, Validation, and Synthesis verified (Final cleanup 2026-06-28). |
| **#192** | Representation of all agents | **Verified & Closed** | 15+ providers documented and indexed. Added Perplexity (2026-05-12). |
| **#201** | Enterprise productive suite | **Verified & Closed** | Section created in docs/tools/enterprise/. |
| **#203** | Intelligence per value matrix | **Verified & Closed** | Integrated into api_pricing_free_tiers.md. |
| **#299** | OpenRouter log tools | **Verified & Closed** | Datadog, Sentry, Grafana, New Relic integrated. |
| **#311** | Add enterprise tools (AmpCode) | **Verified & Closed** | Doc deepened with Python examples and Data Contracts. |
| **#319** | ai_tool_access_matrix links & UI | **Verified & Closed** | UI standardized; links and status markers updated. |
| **#335** | Add model (Qwen 3.6-35B-A3B) | **Verified & Closed** | Explicitly documented in Qwen doc. |
| **#356** | Claude skills documentation | **Verified & Closed** | Skills added to skills.md. |
| **#359** | Weekly deepening (Batch 6) | **Verified & Closed** | Habitica, Trilium, Rclone, Mealie, Speedtest deepened. |
| **#360** | Category gap fill (Intake/Storage) | **Verified & Closed** | AnyType, Khoj, SilverBullet, Verba added. |
| **#404** | Claude code plugins | **Verified & Closed** | Descriptions updated and standardized. |
| **#408** | Deepen examples (Batch 7) | **Verified & Closed** | mem0, Google Opal, Project Genie, Sora, NotebookLM deepened. |
| **#421** | Weekly deepening (Batch 7) | **Verified & Closed** | Unstructured, LlamaParse, Karpathy, Matt Pocock, AmpCode deepened. |
| **#422** | Category gap fill: calendar_tasks | **Verified & Closed** | 20 docs added and indexed. |
| **#506** | Jules Sprint W3 | **Verified & Closed** | Deepened SearXNG and Syncthing to 'High Confidence'. |
| **#529** | Daily Maintenance Run (2026-05-07) | **Verified & Closed** | Step 2 (Doc audit) completed for W4 tools. |
| **#530** | [W4] Jules Sprint (AI Knowledge) | **Verified & Closed** | Deepened gemini-macos, vercel-ai-gateway, and claude-mythos. |
| **Batch 21** | Weekly deepening: AI Knowledge | **Verified & Closed** | DeepSeek R1, Perplexity, AnythingLLM, LobeHub, and Dify deepened. Verified 2026-06-01. |
| **Batch 23** | Weekly deepening: Infrastructure | **Verified & Closed** | LM Studio, Jan.ai, Msty, Google Gemini, and LibreChat deepened. Verified 2026-06-01. |
| **Batch 24** | Weekly deepening: Services | **Verified & Closed** | Paperless-ngx, SearXNG, Plex, qBittorrent, and Radicale deepened. Verified 2026-06-01. |
| **Batch 27** | Weekly deepening: Services | **Verified & Closed** | Actual Budget, Audiobookshelf, Authentik, Changedetection.io, and Diskover deepened. Verified 2026-06-01. |
| **Batch 28** | Weekly deepening: Services | **Verified & Closed** | Deepened drawio, element, excalidraw, focalboard, gitea. Verified 2026-06-01. |
| **Batch 29** | Weekly deepening: Services | **Verified & Closed** | Deepened `grocy.md`, `habitica.md`, `home-assistant.md`, `homebox.md`, `it-tools.md`. Verified 2026-06-01. |
| **Batch 30** | Weekly deepening: Services | **Verified & Closed** | Deepened `jackett.md`, `jellyfin.md`, `kiwix.md`, `linkwarden.md`, `mealie.md`. Verified 2026-06-01. |
| **Batch 31** | Weekly deepening: Services | **Verified & Closed** | Deepened `navidrome.md`, `nextcloud.md`, `omni-tools.md`, `portracker.md`, `tika.md`. Verified 2026-06-01. |
| **Batch 32** | Weekly deepening: Services | **Verified & Closed** | Deepened `trilium.md`, `tubearchivist.md`, `vikunja.md`, `whisper.md`. Verified 2026-06-01. |
| **Batch 33** | Weekly deepening: AI Knowledge | **Verified & Closed** | Deepened `google-opal.md`, `project-genie.md`, `sora.md`, `google-lyria.md`, `azure-openai.md`, `aitmpl.md`, `gemini-flash-tts.md`, `nano-banana.md`, `google-search.md`, `dex.md`. Verified 2026-06-01. |
| **Batch 34** | Weekly deepening: Knowledge Mgmt | **Verified & Closed** | Deepened `anytype.md`, `silverbullet.md`, `akiflow.md`, `morgen.md`, `component_map.md`. Verified 2026-06-01. |
| **Batch 35** | Deepening Shallow Docs | **Verified & Closed** | Media, Comm, Security, and Productivity docs deepened. Verified 2026-06-03. |
| **Batch 36** | Architecture Deepening | **Verified & Closed** | Deepened `flows.md`, `infrastructure.md`, `prompt-catalogue.md`. Verified 2026-06-01. |
| **Batch 37** | Knowledge Base Deepening | **Verified & Closed** | Deepened learning map, builder index, starter stack, economic impact, reading list. Verified 2026-06-01. |
| **Batch 38** | Playbook Deepening | **Verified & Closed** | Deepened dev workflow, doc prep, email-to-calendar, family admin, NFS CSI setup. Verified 2026-06-01. |
| **Batch 39** | Knowledge Base Deepening | **Verified & Closed** | Deepened ai_signal_sources, agent_protocols, and ai_tool_access_matrix. Verified 2026-06-01. |
| **Batch 40** | Playbook Deepening | **Verified & Closed** | Deepened raspberry-pi-kiosk-automation and scan-to-task. Verified 2026-06-01. |
| **Batch 41** | Maintenance Run (Audit Resolution) | **Verified & Closed** | 100% compliance achieved across 486/486 docs (2026-05-12). |
| **Batch 42** | Service & Automation Deepening | **Verified & Closed** | Matrix Synapse, Authentik LDAP, n8n SLOs completed. Verified 2026-06-03. |
| **Batch 44** | Maintenance Run (Oldest Backlog) | **Verified & Closed** | Deepened `standards.md`, `logseq.md`, etc. Verified 2026-06-01. |
| **Batch 45** | Maintenance Run (Oldest Backlog) | **Verified & Closed** | Deepened `llama-cpp.md`, `llm-trust-boundaries.md`, etc. Verified 2026-06-01. |
| **Batch 46** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `obsidian.md`, `make.md`, `zapier.md`, etc. Verified 2026-06-01. |
| **Batch 47** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `human-eval.md`, `gsm8k.md`, `chatbot-arena.md`, etc. Verified 2026-06-01. |
| **Batch 48** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `humanitys-last-exam.md`, `llmperf.md`, `lm-evaluation-harness.md`, etc. Verified 2026-06-01. |
| **Batch 49** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `zse.md`, `openrouter.md`, `llamaindex.md`, `flowise.md`, `localai.md`. Verified 2026-06-01. |
| **Batch 50** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `ragflow.md`, `mycelium.md`, `codeium.md`, `sourcegraph_cody.md`, `terminus-2.md`. Verified 2026-06-01. |
| **Batch 51** | Maintenance Run (Technical Deepening) | **Verified & Closed** | Deepened `pa-bench.md`, `terminal-bench.md`, `google_calendar.md`, etc. Verified 2026-06-01. |
| **Batch 52** | Maintenance Run (Technical Deepening) | **Verified & Closed** | Deepened `custom_agents.md`, `droid.md`, `gpt_engineer.md`, etc. Verified 2026-06-01. |
| **Batch 53** | Maintenance Run (Technical Deepening) | **Verified & Closed** | Deepened `mentat.md`, `openswarm.md`, `plandex.md`, etc. Verified 2026-06-01. |
| **Batch 54** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `tabnine.md`, `vscode.md`, `zed.md`, etc. Verified 2026-06-01. |
| **Batch 55** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `free-will-mcp.md`, `continue_dev.md`, etc. Verified 2026-06-01. |
| **Batch 56** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `openbb.md`, `cursor.md`, etc. Verified 2026-06-01. |
| **Batch 57** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `vercel.md`, `cloudflare-pages.md`, etc. Verified 2026-06-01. |
| **Batch 58** | Maintenance Run (Medium Confidence) | **Verified & Closed** | Deepened `netlify.md`, `langchain.md`, etc. Verified 2026-06-01. |
| **Batch 59** | Maintenance Run (Oldest Backlog) | **Verified & Closed** | Deepened `swe-bench.md`, `obsidian-vector-search.md`, etc. Verified 2026-06-01. |
| **Batch 60** | Maintenance Run (Technical Deepening) | **Verified & Closed** | Deepened `valyu.md`, `crawl4ai.md`, etc. Verified 2026-06-01. |
| **Batch 61** | Maintenance Run (Production Deepening) | **Verified & Closed** | Deepened `langsmith.md`, `firecrawl.md`, etc. Verified 2026-06-01. |
| **Batch 62** | Maintenance Run (The "Oldest" Res) | **Verified & Closed** | Deepened `teamout.md`, `claude-code-setup.md`, etc. Verified 2026-06-01. |
| **Batch 63** | Maintenance Run (The "Oldest" Res) | **Verified & Closed** | Deepened `chronos-mcp.md`, `vault-mcp.md`, etc. Verified 2026-06-01. |
| **Batch 64** | Maintenance Run (AI Knowledge) | **Verified & Closed** | Deepened `google-opal.md`, `project-genie.md`, etc. Verified 2026-06-01. |
| **Batch 65** | MCP Technical Deepening | **Verified & Closed** | Deepened `claude-code-container-mcp.md`, `desktop-commander-mcp.md`, etc. (2026-05-16). |
| **Batch 66** | Knowledge Base Deepening | **Verified & Closed** | Deepened `tool-calling-and-mcp.md`, `rag.md`, `model_comparison_and_evaluation.md`, `google_one_plans_comparison.md`, and `filesystem-context.md`. Verified 2026-06-03. |
| **Batch 69** | Maintenance Run (Oldest Res) | **Verified & Closed** | Deepened `langgraph.md`, `semantic-kernel.md`, `smolagents.md`, `docling-mcp.md`, `cohere.md`. Verified 2026-06-01. |
| **Batch 70** | Technical Deepening (Frameworks & Infra) | **Verified & Closed** | Deepened `autogen.md`, `crewai.md`, `dspy.md`, `haystack.md`, `vllm.md`. Verified 2026-06-01. |
| **Batch 71** | Infrastructure Maintenance | **Verified & Closed** | Deepened `tgi.md`, `sglang.md`, `aphrodite-engine.md`, `exllamav2.md`, `claude-code-router.md`. Verified 2026-06-01. |
| **Batch 72** | Inference Providers & Dev Studio | **Verified & Closed** | Deepened `fireworks.md`, `groq.md`, `mistral.md`, `together.md`, `firebase-studio.md`. Verified 2026-06-02. |
| **Batch 73** | High-Value AI Knowledge & Providers | **Verified & Closed** | Deepened `minimax.md`, `moonshot.md`, `copy-ai.md`, `jasper.md`, `runwayml.md`. Verified 2026-06-02. |
| **Batch 74** | Oldest Backlog Maintenance | **Verified & Closed** | Deepened `superpowers.md`, `elevenlabs.md`, `claude-cookbooks.md`, `playwright.md`, `replicate.md` (2026-05-18). |
| **Issue 2** | Supabase Deepening | **Verified & Closed** | Deepened `supabase.md` to High Confidence (2026-05-18). |
| **Batch 75** | Oldest Backlog Maintenance | **Verified & Closed** | Deepened `supabase.md`, `github-pages.md`, `fastapi.md`, `litellm.md`, `fine-tuning-open-models.md` (2026-05-18). |
| **Batch 76** | Fine-tuning Ecosystem | **Verified & Closed** | Deepened `unsloth.md`, `llama-factory.md`, `axolotl.md`, `distilabel.md`, `glaive.md` (2026-05-18). |
| **Batch 77** | Oldest Backlog Maintenance | **Verified & Closed** | Deepened `evalplus.md`, `helm.md`, `opencompass.md`, `openhands.md`, `openclaw-use-case-catalog.md` (2026-05-19). |
| **Batch 78** | Technical Deepening (Infra & Bench) | **Verified & Closed** | Deepened `docker.md`, `luma-dream-machine.md`, `bigcodebench.md`, `arc.md`, `asdiv.md`. Verified 2026-06-02. |
| **Batch 79** | Oldest Documentation Issues | **Verified & Closed** | Joplin, Devin, MMLU, HuggingFace, Proton deepened. Verified 2026-06-03. |
| **Batch 80** | Automation & Security Deepening | **Verified & Closed** | Make, Vault, Playwright-MCP deepened. Verified 2026-06-03. |
| **Batch 81** | Oldest Non-Compliant Docs | **Verified & Closed** | AWS Bedrock, Pulse-MCP, Alpaca-Eval, etc. deepened. Verified 2026-06-03. |
| **Batch 82** | Technical Deepening (Backlog) | **Verified & Closed** | Deepened `pa-bench.md`, `terminal-bench.md`, `google_calendar.md`, `anti_gravity.md`, `cloud_code.md`. Verified 2026-06-02. |
| **Batch 84** | AI Knowledge Deepening | **Verified & Closed** | Deepened `claude.md`, `chatgpt.md`, `chatbox-ai.md`, etc. Verified 2026-06-02. |
| **Batch 85** | Comprehensive Cleanup | **Verified & Closed** | Deepened `supabase.md`, `todoist.md`, `microsoft-todo.md`, etc. Resolved debt from Batch 55/56 (2026-05-21). |
| **Batch 86** | Deepening Shallow Docs | **Verified & Closed** | Deepened `inventory.md`, `cloudflare-mesh.md`, `real_time_sync_engines.md`, etc. Verified 2026-06-02. |
| **Batch 87** | Deepening Shallow Docs | **Verified & Closed** | Deepened `openai-agents-sdk.md`, `notion-ai.md`, `jules.md`, `roam-research.md`, `kumo-ai.md`. Verified 2026-06-02. |
| **Batch 88** | Technical Deepening | **Verified & Closed** | Deepened `dashworks.md`, `guru.md`, `coveo.md`, `motion.md`, `any-do.md` with technical examples. Verified 2026-06-02. |
| **Batch 89** | Deepening Shallow Docs | **Verified & Closed** | Deepened `self-healing-agent-research.md`, `mlx.md`, `home-admin-tools.md`, `perplexity-agent-api.md`, `ai-auditing-tools.md`. Verified 2026-06-02. |
| **Batch 91** | Deepening Shallow Docs | **Verified & Closed** | Headscale, Heretic-ara, JudgeGPT, Intercode, MS Graph. Verified 2026-06-03. |
| **Batch 92** | Service Maintenance & Health | **Verified & Closed** | n8n fixtures, Tailscale exit node, Grocy, Focalboard. Verified 2026-06-03. |
| **Batch 94** | Operational Verification | **Verified & Closed** | Infrastructure migrations, data guardrails, and service freshness audits (Syncthing, Gitea) verified (2026-05-25). |
| **Batch 95** | Service Maintenance (Backlog) | **Verified & Closed** | Synchronized playbook checklists and populated `## Backlog` for 54 service docs. Verified 2026-06-02. |
| **Batch 96** | Service Freshness Audit | **Verified & Closed** | LiteLLM, n8n, Trilium, Immich, Draw.io audited. Verified 2026-06-03. |
| **Batch 97** | Service Freshness Audit | **Verified & Closed** | Audited Element, Linkwarden, Audiobookshelf, Excalidraw, and Homebox for May 2026 freshness. Verified 2026-06-02. |
| **Batch 98** | Service Freshness Audit | **Verified & Closed** | Mealie, Ollama, Open WebUI, Paperless-AI, Prowlarr. Verified 2026-06-03. |
| **Batch 99** | Service Maintenance Backlog | **Verified & Closed** | All 36 service audits categorized and completed. Verified 2026-06-03. |
| **Batch 100** | Technical Freshness Audits | **Verified & Closed** | Audited HELM, OpenCompass, OpenClaw, and Docling for May 2026 technical freshness. Verified 2026-06-02. |
| **Batch 101** | Technical Freshness Audits | **Verified & Closed** | Audited Software Factories, Ubuntu AI, ColQwen, VAKRA, and Multi-Calendar Research. Verified 2026-06-03. |
| **Batch 102** | Core Architecture Freshness | **Verified & Closed** | Audited CONTRIBUTING, README, Multi-Agent KnowledgeOps, Data Copilot, and Flows. Verified 2026-06-03. |
| **Batch 103** | Technical Freshness Audits | **Verified & Closed** | Audited voice research, vector storage, vision models, family prompts, and search for May 2026 technical freshness (2026-05-28). |
| **Batch 104** | Technical Freshness Audits | **Verified & Closed** | Audited Dex CRM, NanoClaw, CodeGraphContext, Prompt Requests, and PostHog. Verified 2026-06-03. |
| **Batch 105** | Technical Freshness Audits | **Verified & Closed** | Audited Lightpanda, SHARP, Grok, Windsurf, and Gemini CLI. Verified 2026-06-03. |
| **Batch 106** | Technical Freshness Audits | **Verified & Closed** | Core index files and high-value tools (PydanticAI) updated. Verified 2026-06-03. |
| **Batch 107** | Technical Freshness Audits | **Verified & Closed** | Audited External-DNS, MinIO, big-AGI, Doc Writer, and Claude Code. Verified 2026-06-03. |
| **Batch 108** | Technical Freshness Audits | **Verified & Closed** | Audited KB README, Sync Engines, Google One, Audio Transcription, and Self-healing Agents. Verified 2026-06-03. |
| **Batch 109** | Technical Freshness Audits | **Verified & Closed** | Audited Apple Calendar, Calendly, Fantastical, Fastmail, and Microsoft To Do. Verified 2026-06-03. |
| **Batch 110** | Technical Freshness Audits | **Verified & Closed** | Audited SavvyCal, Sunsama, TickTick, Elastic, and Curiosity. Verified 2026-06-03. |
| **Batch 111** | Technical Freshness Audits | **Verified & Closed** | Audited Enterprise Index, Amie, Agentic RAG, Data Copilot Skeleton, and Nemotron. Verified 2026-06-03. |
| **Batch 112** | Technical Freshness Audits | **Verified & Closed** | Audited Airflow, Hamilton, Argo, Dagster, and Flyte. Verified 2026-06-03. |
| **Batch 113** | Technical Freshness Audits | **Verified & Closed** | Audited Rivet, AG2, Mastra, Langflow, and Superinterface. Verified 2026-06-03. |
| **Batch 114** | Technical Freshness Audits | **Verified & Closed** | Audited Ripgrep, Temporal, Ansigpt, Gemini, and LlamaIndex.TS. Verified 2026-06-03. |
| **Batch 115** | Technical Freshness Audits | **Verified & Closed** | Audited k3s-cluster-setup, infrastructure, prompt-catalogue, parea, and llmware. Verified 2026-06-07. |

## Action Plan for Remaining Work (Action C)
The following tasks are identified for future Ralph-loop runs to maintain the "High Confidence" standard:

- **Access Matrix Freshness**: **Updated (2026-05-23)** (Perplexity Gmail/Calendar updated to 🟢; Aider MCP updated to 🟠).

---
- Confidence: high
