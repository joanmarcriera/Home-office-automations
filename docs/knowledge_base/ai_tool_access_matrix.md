# AI Tool Access Matrix

This matrix compares AI assistants, coding agents, local workspaces, workflow tools, and agent frameworks by practical access surface: local execution, Gmail, Calendar, local files, deep research, interface shape, MCP/tool ecosystem, provider flexibility, and paid-plan availability.

Use it as a shortlist filter before doing row-level procurement checks. The entries treat "access" as either a native feature or an officially documented connector, plugin, node, extension, SDK, or MCP path. Unofficial hacks are excluded. "BYO remote AI" is marked Yes only where the product officially documents OpenAI-compatible/custom base URL support or another direct provider path that would make providers such as Z.ai realistic.

## Legend

| Code | Meaning |
| :---: | :--- |
| <span class="status-y">Y</span> | Yes or native support |
| <span class="status-v">V</span> | Via official connector, plugin, node, extension, SDK, or MCP path |
| <span class="status-u">U</span> | Upload or import only |
| <span class="status-p">P</span> | Partial or limited support |
| <span class="status-n">N</span> | No documented path in the reviewed sources |

<style>
.status-y { background-color: #2ea44f; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
.status-v { background-color: #0969da; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
.status-u { background-color: #6e7781; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
.status-p { background-color: #9a6700; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
.status-n { background-color: #cf222e; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
</style>

## Fast read

If the priority is one tool that already does Gmail, Calendar, files, and deep research well, the strongest shortlist is [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Claude](../tools/ai_knowledge/claude.md), and [Gemini Apps](../tools/ai_knowledge/gemini.md). ChatGPT and Claude are broader cross-app assistants; Gemini is strongest when the operating surface is already Google Workspace.

If the priority is local-first or self-hosted work, the strongest shortlist is [AnythingLLM](../tools/ai_knowledge/anythingllm.md), LibreChat, [Open WebUI](../services/open-webui.md), [Jan](../tools/infrastructure/jan-ai.md), and Goose. These give better control over local models, self-hosting, and private files, but Gmail and Calendar usually arrive through MCP or external integrations rather than first-party connectors.

If the priority is coding-first integration potential, the strongest shortlist is [Claude Code](../tools/development_ops/claude-code.md), [Codex CLI](../tools/development_ops/codex.md), Gemini CLI, Cline, Roo Code, [Cursor](../tools/development_ops/cursor.md), and Windsurf. Gemini CLI has the cleanest official Workspace story in this matrix, while Cline and Roo Code are better candidates for provider flexibility and custom endpoints.

If the priority is reliable workflow automation rather than chat, [n8n](../services/n8n.md) and [Zapier](../tools/automation_orchestration/zapier.md) belong in a separate top tier. They are less elegant as daily chat interfaces, but stronger when the requirement is to read Gmail, inspect Calendar, and perform actions repeatably.

## Primary assistant and agent matrix

| Tool | Category | Local | Gmail | Calendar | Files | Research | UI | TUI | CLI | OSS/self-host | MCP/tools | BYO remote AI | Paid | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [ChatGPT](../tools/ai_knowledge/chatgpt.md) | General assistant | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Strongest all-rounder for native research, files, and app connectors. |
| [Claude](../tools/ai_knowledge/claude.md) | General assistant | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Strong for cited research and Google Workspace connectors. |
| [Gemini Apps](../tools/ai_knowledge/gemini.md) | General assistant | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-p">P</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Strongest Google-native fit for Gmail and Calendar workflows. |
| [Perplexity](../tools/ai_knowledge/perplexity.md) | Research/search | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-p">P</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Excellent web research; weaker first-party Gmail and Calendar story. |
| [NotebookLM](../tools/ai_knowledge/notebooklm.md) | Research/notebooks | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Best for source-grounded research on owned materials; less of an action agent. |
| [GitHub Copilot](../tools/development_ops/github_copilot.md) | Coding assistant | <span class="status-n">N</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Good code agent in IDE; external app access is mainly via MCP. |
| [Cursor](../tools/development_ops/cursor.md) | AI IDE | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Strong coding IDE; external systems mainly through MCP. |
| [Windsurf](../tools/development_ops/windsurf.md) | AI IDE | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Similar to Cursor; MCP is the main integration route. |
| [Claude Code](../tools/development_ops/claude-code.md) | Coding agent | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Terminal-first coding agent with broad MCP reach. |
| [Codex CLI](../tools/development_ops/codex.md) | Coding agent | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Strong local terminal workflow; OpenAI-centric rather than provider-agnostic. |
| Gemini CLI | Coding / terminal agent | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | Good terminal choice when official Workspace access is important. |
| [Aider](../tools/development_ops/aider.md) | Terminal pair programmer | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Practical for local repos; broad model and provider flexibility. |
| [Continue](../tools/development_ops/continue_dev.md) | IDE coding agent/checks | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Useful for repo checks plus flexible model backends. |
| Cline | VS Code coding agent | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Strong editor agent with browser support and custom provider URL options. |
| Roo Code | VS Code coding agent | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Similar to Cline, with explicit OpenAI-compatible and Z.ai-oriented provider paths. |
| [OpenHands](../tools/development_ops/openhands.md) | Agent platform | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | More of a software-agent runtime than a personal productivity assistant. |
| [Open WebUI](../services/open-webui.md) | Self-hosted AI workspace | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | Strong self-hosted front end for local and cloud models. |
| LibreChat | Self-hosted chat/agents | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | Flexible self-hosted stack with custom endpoints and agents. |
| [AnythingLLM](../tools/ai_knowledge/anythingllm.md) | Local-first workspace/agents | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Local-first and practical for private document and agent use. |
| [LM Studio](../tools/infrastructure/lm-studio.md) | Local model runner | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | Best as a local model host rather than a full productivity agent. |
| [Jan](../tools/infrastructure/jan-ai.md) | Local AI app | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-n">N</span> | Local, open-source chat client with MCP support. |
| TypingMind | Multi-model UI | <span class="status-p">P</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | Good front end when plugins, Zapier, or MCP matter more than native apps. |
| Open Interpreter | Local computer-use agent | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Strong for local computer, files, and terminal; not a native Gmail or Calendar tool. |
| Goose | Local general-purpose agent | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | Broad local agent with deep MCP emphasis. |
| Langflow | Visual agent builder | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | Better as a builder and orchestrator than as an end-user assistant. |
| [Flowise](../tools/ai_knowledge/flowise.md) | Visual agent builder | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-v">V</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Good no-code-ish orchestration with MCP and OpenAI-compatible backends. |
| [n8n](../services/n8n.md) | Automation/AI workflows | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | Strongest when the priority is actual business automation over chat UX. |
| [Zapier](../tools/automation_orchestration/zapier.md) | Automation/AI actions | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-y">Y</span> | <span class="status-v">V</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-n">N</span> | <span class="status-y">Y</span> | <span class="status-p">P</span> | <span class="status-y">Y</span> | Best SaaS route for turning an AI front end into app actions; Zapier MCP is the current strategic path. |

## Supplementary tool matrix

The supplementary list extends the comparison beyond end-user assistants into frameworks, observability systems, gateways, browser agents, and workflow infrastructure.

| Tool | Category | Local | Gmail | Calendar | Files | Research | UI | TUI | CLI | OSS/self-host | MCP/tools | BYO remote AI | Paid | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [LangChain](../tools/ai_knowledge/langchain.md) | Agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🟢 | Core framework layer, not an end-user assistant. |
| [LangGraph](../tools/frameworks/langgraph.md) | Agent orchestration | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Strong graph/runtime choice for custom agents. |
| [LangSmith](../tools/benchmarking/langsmith.md) | Observability / agent IDE | 🟠 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | 🔴 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | Observability and testing surface rather than an access agent. |
| [CrewAI](../tools/frameworks/crewai.md) | Multi-agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Framework for multi-agent app construction. |
| [AutoGen](../tools/frameworks/autogen.md) | Multi-agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Framework for agent coordination and experiments. |
| AutoGen Studio | Low-code agent UI | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | UI layer for AutoGen-style agent workflows. |
| [Semantic Kernel](../tools/frameworks/semantic-kernel.md) | Agent SDK | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | SDK for embedding agents into applications. |
| Microsoft Agent Framework | Agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | 🟢 | Microsoft-centered agent framework path. |
| [Agno](../tools/agents/agno.md) | Agent runtime / framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Agent framework with practical local and app-building focus. |
| [Haystack](../tools/frameworks/haystack.md) | RAG / agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Strong RAG framework, not a productivity assistant. |
| PydanticAI | Agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | Developer framework centered on typed Python agents. |
| [LlamaIndex](../tools/ai_knowledge/llamaindex.md) | Context / agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Strong context and RAG layer. |
| LlamaIndex.TS | TypeScript context / agent framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | TypeScript counterpart for context-heavy apps. |
| [LlamaParse](../tools/intake_storage/llamaparse.md) | Document AI / OCR | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Document parsing service rather than an agent. |
| [Dify](../tools/ai_knowledge/dify.md) | Agent/workflow platform | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | App builder with workflow and agent surfaces. |
| Vellum | AI workflow / agent platform | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Hosted workflow platform. |
| Rivet | Visual AI IDE | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🔴 | 🟠 | 🟢 | 🟠 | 🔴 | Visual workflow IDE; self-host status depends on deployment path. |
| [LiteLLM](../services/litellm.md) | LLM gateway | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | High-value provider abstraction and routing layer. |
| [OpenRouter](../tools/ai_knowledge/openrouter.md) | Model router / API | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | Hosted model router with broad OpenAI-compatible API coverage. |
| Vercel AI SDK | App / agent SDK | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | App SDK for AI interfaces and agents, not a standalone assistant. |
| Temporal | Durable workflow engine | 🟢 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Durable orchestration substrate. |
| AgentOps | Agent observability | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Observability product for agent runs. |
| [Langfuse](../tools/process_understanding/langfuse.md) | LLM observability | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | Open-source observability with self-host path. |
| Opik | LLM observability / eval | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Evaluation and tracing surface. |
| Promptfoo | Eval / red-team | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Practical CLI-driven eval and red-team tool. |
| Ragas | Evaluation library | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | Library for RAG and LLM evaluation. |
| Helicone | AI gateway / observability | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Gateway and observability layer with provider flexibility. |
| Arize Phoenix | Observability / eval | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Open-source evaluation and tracing stack. |
| Parea | Observability / eval | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Hosted observability and evaluation platform. |
| LastMile AI | Eval / guardrails / workbooks | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Hosted workbench and evaluation surface. |
| Fiddler | Guardrails / observability | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | Enterprise observability and governance. |
| [Browser Use](../tools/automation_orchestration/browser-use.md) | Browser agent | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Browser automation agent layer. |
| Stagehand | Browser automation framework | 🟢 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | Browser automation framework rather than productivity assistant. |
| [Composio](../tools/agents/composio.md) | Tool / auth layer for agents | 🔴 | 🔵 | 🔵 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Tool and auth layer for connecting agents to SaaS apps. |
| Gumloop | No-code agents / workflows | 🔴 | 🔵 | 🟠 | 🔵 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | SaaS workflow layer with useful app integrations. |
| [Braintrust](../tools/process_understanding/braintrust.md) | Observability / eval | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🔴 | 🟢 | Evaluation, prompt, and tracing infrastructure. |
| [DSPy](../tools/frameworks/dspy.md) | Programming framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Programmatic prompting and optimization framework. |
| Instructor | Structured output library | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | Lightweight library for structured outputs. |
| [Mem0](../tools/agents/mem0.md) | Memory layer | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Agent memory layer rather than a full assistant. |
| LobeHub | Self-hosted AI workspace | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Self-hostable multi-model workspace. |
| Chatbox AI | Desktop chat client | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | Desktop multi-model chat client. |
| Msty | Local AI desktop app | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | Local AI desktop app with model flexibility. |
| AirOps | Content / workflow platform | 🔴 | 🔵 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Workflow/content platform with app integrations. |
| Google ADK | Agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Google-centered agent development kit. |
| Firebase Genkit | Full-stack AI framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 | Full-stack AI framework for app developers. |
| [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) | Agent SDK | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | OpenAI-centered SDK path for agents. |
| big-AGI | Expert AI workspace | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Expert workspace/front end; row should be row-source checked before procurement. |
| AG2 | Multi-agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | Multi-agent framework descended from AutoGen ecosystem work. |
| Mastra | TypeScript agent framework | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | TypeScript agent framework with developer-first focus. |
| Superinterface | AI assistant UI / infra | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | Assistant UI and infrastructure layer. |
| W&B Weave | Observability / eval | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | Observability and evaluation layer in the W&B ecosystem. |
| LLMWare | Local / private AI framework | 🟢 | 🔴 | 🔴 | 🟢 | 🟠 | 🟠 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | Local and private AI framework. |
| Portkey AI Gateway | AI gateway | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | Gateway and provider abstraction layer. |

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

- Last reviewed: 2026-04-27
- Confidence: high
