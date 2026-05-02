# AI Tool Access Matrix

This matrix compares AI assistants, coding agents, local workspaces, workflow tools, and agent frameworks by practical access surface: local execution, Gmail, Calendar, local files, deep research, interface shape, MCP/tool ecosystem, provider flexibility, and paid-plan availability.

Use it as a shortlist filter before doing row-level procurement checks. The entries treat "access" as either a native feature or an officially documented connector, plugin, node, extension, SDK, or MCP path. Unofficial hacks are excluded. "BYO remote AI" is marked Yes only where the product officially documents OpenAI-compatible/custom base URL support or another direct provider path that would make providers such as Z.ai realistic.

## Legend

| Code | Meaning |
| :---: | :--- |
| 🟢 | Yes or native support |
| 🔵 | Via official connector, plugin, node, extension, SDK, or MCP path |
| ⚪ | Upload or import only |
| 🟠 | Partial or limited support |
| 🔴 | No documented path in the reviewed sources |



## Fast read

If the priority is one tool that already does Gmail, Calendar, files, and deep research well, the strongest shortlist is [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Claude](../tools/ai_knowledge/claude.md), and [Gemini Apps](../tools/ai_knowledge/gemini.md). ChatGPT and Claude are broader cross-app assistants; Gemini is strongest when the operating surface is already Google Workspace.

If the priority is local-first or self-hosted work, the strongest shortlist is [AnythingLLM](../tools/ai_knowledge/anythingllm.md), LibreChat, [Open WebUI](../services/open-webui.md), [Jan](../tools/infrastructure/jan-ai.md), and [Goose](../tools/automation_orchestration/goose.md). These give better control over local models, self-hosting, and private files, but Gmail and Calendar usually arrive through MCP or external integrations rather than first-party connectors.

If the priority is coding-first integration potential, the strongest shortlist is [Claude Code](../tools/development_ops/claude-code.md), [Codex CLI](../tools/development_ops/codex.md), [Gemini CLI](../tools/ai_knowledge/gemini-cli.md), [Cline](../tools/agents/cline.md), [Roo Code](../tools/agents/roo-code.md), [Cursor](../tools/development_ops/cursor.md), and [Windsurf](../tools/development_ops/windsurf.md). Gemini CLI has the cleanest official Workspace story in this matrix, while Cline and Roo Code are better candidates for provider flexibility and custom endpoints.

If the priority is reliable workflow automation rather than chat, [n8n](../services/n8n.md) and [Zapier](../tools/automation_orchestration/zapier.md) belong in a separate top tier. They are less elegant as daily chat interfaces, but stronger when the requirement is to read Gmail, inspect Calendar, and perform actions repeatably.

## Primary assistant and agent matrix

| Tool | Category | Local | Gmail | Calendar | Files | Research | UI | TUI | CLI | OSS/self-host | MCP/tools | BYO remote AI | Paid | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [ChatGPT](../tools/ai_knowledge/chatgpt.md) | General assistant | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Strongest all-rounder for native research, files, and app connectors. |
| [Claude](../tools/ai_knowledge/claude.md) | General assistant | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Strong for cited research and Google Workspace connectors. |
| [Gemini Apps](../tools/ai_knowledge/gemini.md) | General assistant | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | Strongest Google-native fit for Gmail and Calendar workflows. |
| [Perplexity](../tools/ai_knowledge/perplexity.md) | Research/search | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | Excellent web research; weaker first-party Gmail and Calendar story. |
| [NotebookLM](../tools/ai_knowledge/notebooklm.md) | Research/notebooks | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Best for source-grounded research on owned materials; less of an action agent. |
| [GitHub Copilot](../tools/development_ops/github_copilot.md) | Coding assistant | 🔴 | 🔵 | 🔵 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Good code agent in IDE; external app access is mainly via MCP. |
| [Cursor](../tools/development_ops/cursor.md) | AI IDE | 🟢 | 🔵 | 🔵 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Strong coding IDE; external systems mainly through MCP. |
| [Windsurf](../tools/development_ops/windsurf.md) | AI IDE | 🟢 | 🔵 | 🔵 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Similar to Cursor; MCP is the main integration route. |
| [Claude Code](../tools/development_ops/claude-code.md) | Coding agent | 🟢 | 🔵 | 🔵 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | Terminal-first coding agent with broad MCP reach. |
| [Codex CLI](../tools/development_ops/codex.md) | Coding agent | 🟢 | 🔵 | 🔵 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | Strong local terminal workflow; OpenAI-centric rather than provider-agnostic. |
| [Gemini CLI](../tools/ai_knowledge/gemini-cli.md) | Coding / terminal agent | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | Good terminal choice when official Workspace access is important. |
| [Aider](../tools/development_ops/aider.md) | Terminal pair programmer | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Practical for local repos; broad model and provider flexibility. |
| [Continue](../tools/development_ops/continue_dev.md) | IDE coding agent/checks | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | Useful for repo checks plus flexible model backends. |
| [Cline](../tools/agents/cline.md) | VS Code coding agent | 🟢 | 🔵 | 🔵 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | Strong editor agent with browser support and custom provider URL options. |
| [Roo Code](../tools/agents/roo-code.md) | VS Code coding agent | 🟢 | 🔵 | 🔵 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | Similar to Cline, with explicit OpenAI-compatible and Z.ai-oriented provider paths. |
| [OpenHands](../tools/development_ops/openhands.md) | Agent platform | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | 🟠 | 🟢 | More of a software-agent runtime than a personal productivity assistant. |
| [Open WebUI](../services/open-webui.md) | Self-hosted AI workspace | 🟢 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Strong self-hosted front end for local and cloud models. |
| [LibreChat](../tools/ai_knowledge/librechat.md) | Self-hosted chat/agents | 🟢 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Flexible self-hosted stack with custom endpoints and agents. |
| [AnythingLLM](../tools/ai_knowledge/anythingllm.md) | Local-first workspace/agents | 🟢 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | Local-first and practical for private document and agent use. |
| [LobeHub](../tools/ai_knowledge/lobehub.md) | Self-hosted AI workspace | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Self-hostable multi-model workspace with rich plugin ecosystem. |
| [Chatbox AI](../tools/ai_knowledge/chatbox-ai.md) | Desktop chat client | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | Desktop multi-model chat client with cross-device sync. |
| [Msty](../tools/infrastructure/msty.md) | Local AI desktop app | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | Local AI desktop app with integrated model hub and RAG. |
| [big-AGI](../tools/ai_knowledge/big-agi.md) | Expert AI workspace | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Expert workspace for multi-model reasoning and zero-latency UI. |
| [LM Studio](../tools/infrastructure/lm-studio.md) | Local model runner | 🟢 | 🔵 | 🔵 | 🔵 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | Best as a local model host rather than a full productivity agent. |
| [Jan](../tools/infrastructure/jan-ai.md) | Local AI app | 🟢 | 🔵 | 🔵 | 🔵 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟠 | 🔴 | Local, open-source chat client with MCP support. |
| [TypingMind](../tools/ai_knowledge/typingmind.md) | Multi-model UI | 🟠 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | Good front end when plugins, Zapier, or MCP matter more than native apps. |
| [Open Interpreter](../tools/automation_orchestration/open-interpreter.md) | Local computer-use agent | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟠 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Strong for local computer, files, and terminal; not a native Gmail or Calendar tool. |
| [Goose](../tools/automation_orchestration/goose.md) | Local general-purpose agent | 🟢 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | 🟢 | Broad local agent with deep MCP emphasis. |
| [Langflow](../tools/frameworks/langflow.md) | Visual agent builder | 🟢 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟠 | 🟢 | Better as a builder and orchestrator than as an end-user assistant. |
| [Flowise](../tools/ai_knowledge/flowise.md) | Visual agent builder | 🟢 | 🔵 | 🔵 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | Good no-code-ish orchestration with MCP and OpenAI-compatible backends. |
| [n8n](../services/n8n.md) | Automation/AI workflows | 🟢 | 🟢 | 🟢 | 🔵 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🟢 | Strongest when the priority is actual business automation over chat UX. |
| [Zapier](../tools/automation_orchestration/zapier.md) | Automation/AI actions | 🔴 | 🟢 | 🟢 | 🔵 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | Best SaaS route for turning an AI front end into app actions; Zapier MCP is the current strategic path. |

## Supplementary tool matrix

The supplementary list extends the comparison beyond end-user assistants into frameworks, observability systems, gateways, browser agents, and workflow infrastructure.

| Tool | Category | Local | Gmail | Calendar | Files | Research | UI | TUI | CLI | OSS/self-host | MCP/tools | BYO remote AI | Paid | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [LangChain](../tools/ai_knowledge/langchain.md) | Agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🟢 | Core framework layer, not an end-user assistant. |
| [LangGraph](../tools/frameworks/langgraph.md) | Agent orchestration | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Strong graph/runtime choice for custom agents. |
| [LangSmith](../tools/benchmarking/langsmith.md) | Observability / agent IDE | 🟠 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | 🔴 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | Observability and testing surface rather than an access agent. |
| [CrewAI](../tools/frameworks/crewai.md) | Multi-agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Framework for multi-agent app construction. |
| [AutoGen](../tools/frameworks/autogen.md) | Multi-agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Framework for agent coordination and experiments. |
| [AutoGen Studio](../tools/frameworks/autogen.md) | Low-code agent UI | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | UI layer for AutoGen-style agent workflows. |
| [Semantic Kernel](../tools/frameworks/semantic-kernel.md) | Agent SDK | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | SDK for embedding agents into applications. |
| [Microsoft Agent Framework](../tools/frameworks/microsoft-agent-framework.md) | Agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | 🟢 | Microsoft-centered agent framework path. |
| [Agno](../tools/agents/agno.md) | Agent runtime / framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Agent framework with practical local and app-building focus. |
| [Haystack](../tools/frameworks/haystack.md) | RAG / agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Strong RAG framework, not a productivity assistant. |
| [PydanticAI](../tools/frameworks/pydantic-ai.md) | Agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | Developer framework centered on typed Python agents. |
| [LlamaIndex](../tools/ai_knowledge/llamaindex.md) | Context / agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Strong context and RAG layer. |
| [LlamaIndex.TS](../tools/ai_knowledge/llamaindex-ts.md) | TypeScript context / agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | TypeScript counterpart for context-heavy apps. |
| [LlamaParse](../tools/intake_storage/llamaparse.md) | Document AI / OCR | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Document parsing service rather than an agent. |
| [Dify](../tools/ai_knowledge/dify.md) | Agent/workflow platform | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | App builder with workflow and agent surfaces. |
| [Vellum](../tools/automation_orchestration/vellum.md) | AI assistant / orchestration | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Hosted workflow platform with local computer-use. |
| [Rivet](../tools/frameworks/rivet.md) | Visual AI IDE | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🔴 | 🟠 | 🟢 | 🟠 | 🔴 | Visual workflow IDE; self-host status depends on deployment path. |
| [LiteLLM](../services/litellm.md) | LLM gateway | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | High-value provider abstraction and routing layer. |
| [OpenRouter](../tools/ai_knowledge/openrouter.md) | Model router / API | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | Hosted model router with broad OpenAI-compatible API coverage. |
| [Vercel AI SDK](../tools/development_ops/vercel.md) | App / agent SDK | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | App SDK for AI interfaces and agents, not a standalone assistant. |
| [Temporal](../tools/frameworks/temporal.md) | Durable workflow engine | 🟢 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Durable orchestration substrate. |
| [AgentOps](../tools/process_understanding/agentops.md) | Agent observability | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Observability product for agent runs. |
| [Langfuse](../tools/process_understanding/langfuse.md) | LLM observability | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | Open-source observability with self-host path. |
| [Opik](../tools/process_understanding/comet-opik.md) | LLM observability / eval | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Evaluation and tracing surface. |
| [Promptfoo](../tools/benchmarking/promptfoo.md) | Eval / red-team | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Practical CLI-driven eval and red-team tool. |
| [Ragas](../tools/process_understanding/ragas.md) | Evaluation library | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | Library for RAG and LLM evaluation. |
| [Helicone](../tools/process_understanding/helicone.md) | AI gateway / observability | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Gateway and observability layer with provider flexibility. |
| [Arize Phoenix](../tools/process_understanding/arize-ai.md) | Observability / eval | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Open-source evaluation and tracing stack. |
| [Parea](../tools/process_understanding/parea.md) | Observability / eval | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Hosted observability and evaluation platform. |
| [LastMile AI](../tools/process_understanding/lastmile.md) | Eval / guardrails / workbooks | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Hosted workbench and evaluation surface. |
| [Fiddler](../tools/process_understanding/fiddler.md) | Guardrails / observability | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Enterprise observability and governance. |
| [Browser Use](../tools/automation_orchestration/browser-use.md) | Browser agent | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Browser automation agent layer. |
| [Stagehand](../tools/automation_orchestration/stagehand.md) | Browser automation framework | 🟢 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | Browser automation framework rather than productivity assistant. |
| [Composio](../tools/agents/composio.md) | Tool / auth layer for agents | 🔴 | 🔵 | 🔵 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Tool and auth layer for connecting agents to SaaS apps. |
| [Gumloop](../tools/automation_orchestration/gumloop.md) | No-code agents / workflows | 🔴 | 🔵 | 🟠 | 🔵 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | SaaS workflow layer with useful app integrations. |
| [Braintrust](../tools/process_understanding/braintrust.md) | Observability / eval | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🔴 | 🟢 | Evaluation, prompt, and tracing infrastructure. |
| [DSPy](../tools/frameworks/dspy.md) | Programming framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Programmatic prompting and optimization framework. |
| [Instructor](../tools/frameworks/instructor.md) | Structured output library | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | Lightweight library for structured outputs. |
| [Mem0](../tools/agents/mem0.md) | Memory layer | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Agent memory layer rather than a full assistant. |
| [AirOps](../tools/automation_orchestration/airops.md) | Content / workflow platform | 🔴 | 🔵 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Workflow/content platform with app integrations. |
| [Google ADK](../tools/frameworks/google-adk.md) | Agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Google-centered agent development kit. |
| [Firebase Genkit](../tools/frameworks/firebase-genkit.md) | Full-stack AI framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | Full-stack AI framework for app developers. |
| [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) | Agent SDK | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | OpenAI-centered SDK path for agents. |
| [AG2](../tools/frameworks/ag2.md) | Multi-agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Multi-agent framework descended from AutoGen ecosystem work. |
| [Mastra](../tools/frameworks/mastra.md) | TypeScript agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | TypeScript agent framework with developer-first focus. |
| [Superinterface](../tools/frameworks/superinterface.md) | AI assistant UI / infra | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Assistant UI and infrastructure layer. |
| [W&B Weave](../tools/process_understanding/wandb-weave.md) | Observability / eval | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Observability and evaluation layer in the W&B ecosystem. |
| [LLMWare](../tools/automation_orchestration/llmware.md) | Local / private AI framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Local and private AI framework. |
| [Portkey AI Gateway](../tools/providers/portkey.md) | AI gateway | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Gateway and provider abstraction layer. |

## Practical scoring dimensions

For personal or home-office selection, score each candidate against these weights before committing:

| Dimension | Why it matters | Useful default weight |
| :--- | :--- | :---: |
| Local-first/private files | Reduces data exposure and keeps private archives usable. | 25% |
| Gmail and Calendar reach | Determines whether the assistant can operate where the work actually lives. | 25% |
| Deep research quality | Matters for market scans, purchasing decisions, technical research, and source synthesis. | 20% |
| Provider flexibility | Determines whether you can route to non-default providers such as Z.ai, OpenRouter, or local OpenAI-compatible servers. | 15% |
| Self-hostability and automation | Determines long-term control, reproducibility, and ability to automate without a chat UI. | 15% |

## Takeaways

Very few tools have first-party Gmail and Calendar access. Most non-Google products reach those systems indirectly through MCP, OAuth connectors, workflow tools, or automation layers.

Native deep-research capability remains concentrated in end-user assistants rather than frameworks. Frameworks can build research systems, but they are not generally turnkey research products by themselves.

Provider flexibility is strongest in local coding agents, self-hosted chat workspaces, gateways, and libraries. It is weakest in hosted end-user assistants where model choice is part of the product boundary.

The most practical stack is often layered: a native assistant for research, a local coding agent for repo work, a self-hosted workspace for private files, and n8n or Zapier MCP for durable app actions.

## Related

- [AI Tooling Landscape - 2026 Overview](ai_tooling_landscape.md)
- [AI Company Starter Stack](ai_company_starter_stack.md)
- [Tool Calling and Model Context Protocol](patterns/tool-calling-and-mcp.md)
- [API Pricing and Free Tier Matrix](api_pricing_free_tiers.md)
- [Model Routing Guide](model_routing_guide.md)

## Sources / References

- [ChatGPT synced connectors](https://help.openai.com/en/articles/10847137-internal-knowledge-on-chatgpt-faq)
- [OpenAI deep research guide](https://platform.openai.com/docs/guides/deep-research)
- [Claude Gmail and Google Calendar integration](https://support.anthropic.com/zh-TW/articles/11088742-%E4%BD%BF%E7%94%A8-gmail-%E5%92%8C-google-calendar-%E6%95%B4%E5%90%88%E5%8A%9F%E8%83%BD)
- [Google Workspace Gemini privacy and app context](https://support.google.com/meet/answer/14615114)
- [Model Context Protocol introduction](https://www.anthropic.com/news/model-context-protocol)
- [Open WebUI MCP support](https://docs.openwebui.com/openapi-servers/mcp/)
- [Zapier Developer Documentation - Zapier MCP](https://docs.zapier.com/)
- [Cline Vercel AI Gateway provider documentation](https://docs.cline.bot/provider-config/vercel-ai-gateway)
- [Roo Code documentation](https://docs.roocode.com/)
- [Aider advanced model settings](https://aider.chat/docs/config/adv-model-settings.html)
- [n8n documentation](https://docs.n8n.io/)
- [Z.ai docs](https://docs.z.ai/)
- [OpenRouter documentation](https://openrouter.ai/docs)
- [LiteLLM documentation](https://docs.litellm.ai/)

## Contribution Metadata

- Last reviewed: 2026-05-02
- Confidence: high
