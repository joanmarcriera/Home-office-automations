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
- **Web Crawling**: [Crawl4AI](../tools/process_understanding/crawl4ai.md), [Firecrawl](../tools/process_understanding/firecrawl.md)

## 2. Store
*Tools where information resides in a persistent state.*
- **Document Archive**: [Paperless-ngx](../services/paperless-ngx.md)
- **File Sync/Cloud**: [Nextcloud](../services/nextcloud.md), [Syncthing](../services/syncthing.md)
- **Calendars/Contacts**: [Radicale](../services/radicale.md), [Google Calendar](../tools/calendar_tasks/google_calendar.md)
- **Media/Projects**: [Jellyfin](../services/jellyfin.md), [Focalboard](../services/focalboard.md)
- **Distributed**: [Storj Node](../services/storj.md)

## 3. Understand (Reasoning Engines)
*The brains of the stack that process and reason over information.*
- **Proprietary APIs**: [OpenAI](../tools/ai_knowledge/openai.md), [Anthropic](../tools/ai_knowledge/anthropic.md), [DeepSeek](../tools/ai_knowledge/deepseek.md), [Google Gemini](../tools/ai_knowledge/google-gemini.md)
- **Local Models**: [Ollama](../services/ollama.md), [Local LLMs (MLX, llama.cpp)](../tools/ai_knowledge/local_llms.md), [ansigpt](../tools/ai_knowledge/ansigpt.md), [ZSE](../tools/infrastructure/zse.md)
- **Aggregators**: [OpenRouter](../tools/ai_knowledge/openrouter.md), [Perplexity](../tools/ai_knowledge/perplexity.md), [Valyu](../tools/ai_knowledge/valyu.md)
- **Semantic Search**: [Paperless-AI](../services/paperless-ai.md), [RAGFlow](../tools/process_understanding/ragflow.md), [PageIndex](../tools/process_understanding/pageindex.md)

## 4. Decide (Orchestrate & Route)
*Tools that determine which actions to take and how to route requests.*
- **Routing Layers**: [LiteLLM](../services/litellm.md), [OpenRouter](../tools/ai_knowledge/openrouter.md), [MCP Registry](../tools/automation_orchestration/mcp-registry.md)
- **Workflow Engines**: [n8n](../services/n8n.md), [Home Assistant](../services/home-assistant.md), [Mycelium](../tools/frameworks/mycelium.md)
- **Cloud Connectors**: [Zapier](../tools/automation_orchestration/zapier.md), [Make](../tools/automation_orchestration/make.md)
- **Identity**: [Authentik](../services/authentik.md)

## 5. Act (Agents & Execution)
*Tools that perform modifications to the environment.*
- **Autonomous Agents**: [OpenHands](../tools/development_ops/openhands.md), [Droid](../tools/development_ops/droid.md), [TeamOut](../tools/ai_knowledge/teamout.md), [OpenSwarm](../tools/development_ops/openswarm.md), [OpenClaw](../tools/development_ops/openclaw.md)
- **Browser Agents**: [Browser Use](../tools/automation_orchestration/browser-use.md), [Skyvern](../tools/automation_orchestration/skyvern.md)
- **Coding Assistants**: [Aider](../tools/development_ops/aider.md), [Cursor](../tools/development_ops/cursor.md), [Zed](../tools/development_ops/zed.md), [VS Code](../tools/development_ops/vscode.md), [Claude Code](../tools/development_ops/claude-code.md)
- **Custom Orchestration**: [Custom Agents (SSH + LLM Loop)](../tools/development_ops/custom_agents.md)
- **Execution Plane**: [SSH Execution Patterns](ssh_execution_patterns.md)
- **Home Control**: [Home Assistant](../services/home-assistant.md)

## 6. Sync & Infrastructure
*Tools that ensure consistency and secure connectivity.*
- **Network Access**: [Tailscale](../services/tailscale.md)
- **Protocols**: [CalDAV](../tools/intake_storage/caldav.md)
- **Data Transfer**: [rclone Automation](../services/rclone-automation.md)

## 7. Benchmark
*Tools for evaluating model performance and reasoning.*
- **Reasoning**: [Humanity's Last Exam (HLE)](../tools/benchmarking/humanitys-last-exam.md), [LM Evaluation Harness](../tools/benchmarking/lm-evaluation-harness.md), [DREAM Benchmark](../tools/benchmarking/dream.md)
- **Agentic**: [Terminal-Bench](../tools/benchmarking/terminal-bench.md), [SWE-bench](../tools/benchmarking/swe-bench.md), [LongCLI-Bench](../tools/benchmarking/longcli-bench.md), [PA-bench](../tools/benchmarking/pa-bench.md)
- **Local Performance**: [Ollama Benchmark CLI](../tools/benchmarking/ollama-benchmark-cli.md), [LLMPerf](../tools/benchmarking/llmperf.md)

## Sources / References

- [Stack Overview](https://home-toolset.riera.co.uk)
- [Component Map Source Data](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/all_tools.json)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high
