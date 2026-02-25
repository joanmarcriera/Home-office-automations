# Component Map

This map categorizes all tools in the stack based on their primary function in the information and automation pipeline.

## 1. Ingest
*Tools responsible for receiving or capturing raw information.*
- **Email (IMAP)**: [Paperless-ngx](../services/paperless-ngx.md), [n8n](../services/n8n.md)
- **Scanning**: [OCRmyPDF](../tools/process_understanding/ocrmypdf.md)
- **Manual Input**: [Obsidian](../tools/ai_knowledge/obsidian.md), [Logseq](../tools/ai_knowledge/logseq.md)
- **Inventory**: [Homebox](../services/homebox.md), [Grocy](../services/grocy.md)
- **Bookmarks/Tasks**: [Linkwarden](../services/linkwarden.md), [Habitica](../services/habitica.md)
- **Downloads**: [qBittorrent](../services/qbittorrent.md), [Jackett](../services/jackett.md)

## 2. Store
*Tools where information resides in a persistent state.*
- **Document Archive**: [Paperless-ngx](../services/paperless-ngx.md)
- **File Sync/Cloud**: [Nextcloud](../services/nextcloud.md), [Syncthing](../services/syncthing.md)
- **Calendars/Contacts**: [Radicale](../services/radicale.md), [Google Calendar](../tools/calendar_tasks/google_calendar.md)
- **Media/Projects**: [Jellyfin](../services/jellyfin.md), [Focalboard](../services/focalboard.md)
- **Distributed**: [Storj Node](../services/storj.md)

## 3. Understand (Process & Reason)
*Tools that transform raw data into structured insights or actionable intelligence.*
- **OCR**: [OCRmyPDF](../tools/process_understanding/ocrmypdf.md), [Apache Tika](../services/tika.md), [Whisper](../services/whisper.md)
- **Reasoning Engines**: [Ollama](../services/ollama.md), [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Jules (Google)](../tools/ai_knowledge/jules.md)
- **Semantic Search**: [Paperless-AI](../services/paperless-ai.md)
- **Research**: [Perplexity](../tools/ai_knowledge/perplexity.md), [Diskover](../services/diskover.md)

## 4. Decide (Orchestrate)
*Tools that determine which actions to take based on processed information.*
- **Workflow Engines**: [n8n](../services/n8n.md), [Home Assistant](../services/home-assistant.md)
- **Cloud Connectors**: [Zapier](../tools/automation_orchestration/zapier.md), [Make](../tools/automation_orchestration/make.md)
- **Identity**: [Authentik](../services/authentik.md)
- **Agent Frameworks**: [LangChain](../tools/ai_knowledge/langchain.md), [LlamaIndex](../tools/ai_knowledge/llamaindex.md), [Dify](../tools/ai_knowledge/dify.md), [Flowise](../tools/ai_knowledge/flowise.md)

## 5. Act
*Tools that perform physical or digital modifications to the environment.*
- **Home Control**: [Home Assistant](../services/home-assistant.md)
- **Task Management**: [Vikunja](../services/vikunja.md)
- **Development**: [VS Code](../tools/development_ops/vscode.md), [Cursor](../tools/development_ops/cursor.md), [Zed](../tools/development_ops/zed.md), [Aider](../tools/development_ops/aider.md), [OpenHands](../tools/development_ops/openhands.md), [Anti-Gravity](../tools/development_ops/anti_gravity.md), [Junie CLI](../tools/development_ops/junie-cli.md), [Droid](../tools/development_ops/droid.md), [Terminus 2](../tools/development_ops/terminus-2.md), [Cloud Code](../tools/development_ops/cloud_code.md), [Superconductor](../tools/development_ops/superconductor.md), [GitHub Copilot](../tools/development_ops/github_copilot.md), [Continue.dev](../tools/development_ops/continue_dev.md), [Codeium](../tools/development_ops/codeium.md), [Sourcegraph Cody](../tools/development_ops/sourcegraph_cody.md), [Tabnine](../tools/development_ops/tabnine.md), [GPT Engineer](../tools/development_ops/gpt_engineer.md), [Sweep.dev](../tools/development_ops/sweep_dev.md), [Mentat](../tools/development_ops/mentat.md), [Plandex](../tools/development_ops/plandex.md), [Melty](../tools/development_ops/melty.md), [Codex (OpenAI)](../tools/development_ops/codex.md)

## 6. Sync
*Tools that ensure information is consistent across devices and platforms.*
- **Network Access**: [Tailscale](../services/tailscale.md)
- **Protocols**: [CalDAV](../tools/intake_storage/caldav.md)
- **Model Proxy**: [LiteLLM](../services/litellm.md)
- **Data Transfer**: [rclone Automation](../services/rclone-automation.md)

## 7. Benchmark
*Tools for evaluating model performance and reasoning.*
- **Reasoning**: [Humanity's Last Exam (HLE)](../tools/benchmarking/humanitys-last-exam.md), [LM Evaluation Harness](../tools/benchmarking/lm-evaluation-harness.md)
- **Agentic**: [Terminal-Bench](../tools/benchmarking/terminal-bench.md), [SWE-bench](../tools/benchmarking/swe-bench.md)
- **Local Performance**: [Ollama Benchmark CLI](../tools/benchmarking/ollama-benchmark-cli.md), [LLMPerf](../tools/benchmarking/llmperf.md)
