# AI Tool Access Matrix

This matrix compares AI assistants, coding agents, local workspaces, workflow tools, and agent frameworks by practical access surface: local execution, Gmail, Calendar, local files, deep research, interface shape, MCP/tool ecosystem, provider flexibility, and paid-plan availability.

Use it as a shortlist filter before doing row-level procurement checks. The entries treat "access" as either a native feature or an officially documented connector, plugin, node, extension, SDK, or MCP path. Unofficial hacks are excluded. "BYO remote AI" is marked Yes only where the product officially documents OpenAI-compatible/custom base URL support or another direct provider path that would make providers such as Z.ai realistic.

## Legend

| Code | Meaning |
| :--- | :--- |
| Y | Yes or native support |
| V | Via official connector, plugin, node, extension, SDK, or MCP path |
| U | Upload or import only |
| P | Partial or limited support |
| N | No documented path in the reviewed sources |

## Fast read

If the priority is one tool that already does Gmail, Calendar, files, and deep research well, the strongest shortlist is [ChatGPT](../tools/ai_knowledge/chatgpt.md), Claude, and [Gemini Apps](../tools/ai_knowledge/google-gemini.md). ChatGPT and Claude are broader cross-app assistants; Gemini is strongest when the operating surface is already Google Workspace.

If the priority is local-first or self-hosted work, the strongest shortlist is [AnythingLLM](../tools/ai_knowledge/anythingllm.md), LibreChat, [Open WebUI](../services/open-webui.md), Jan, and Goose. These give better control over local models, self-hosting, and private files, but Gmail and Calendar usually arrive through MCP or external integrations rather than first-party connectors.

If the priority is coding-first integration potential, the strongest shortlist is [Claude Code](../tools/development_ops/claude-code.md), [Codex CLI](../tools/development_ops/codex.md), Gemini CLI, Cline, Roo Code, [Cursor](../tools/development_ops/cursor.md), and Windsurf. Gemini CLI has the cleanest official Workspace story in this matrix, while Cline and Roo Code are better candidates for provider flexibility and custom endpoints.

If the priority is reliable workflow automation rather than chat, [n8n](../services/n8n.md) and [Zapier](../tools/automation_orchestration/zapier.md) belong in a separate top tier. They are less elegant as daily chat interfaces, but stronger when the requirement is to read Gmail, inspect Calendar, and perform actions repeatably.

## Primary assistant and agent matrix

| Tool | Category | Local | Gmail | Calendar | Files | Research | UI | TUI | CLI | OSS/self-host | MCP/tools | BYO remote AI | Paid | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| ChatGPT | General assistant | N | Y | Y | Y | Y | Y | N | N | N | Y | N | Y | Strongest all-rounder for native research, files, and app connectors. |
| Claude | General assistant | N | Y | Y | Y | Y | Y | N | N | N | Y | N | Y | Strong for cited research and Google Workspace connectors. |
| Gemini Apps | General assistant | N | Y | Y | Y | Y | Y | N | N | N | P | N | Y | Strongest Google-native fit for Gmail and Calendar workflows. |
| Perplexity | Research/search | N | N | N | Y | Y | Y | N | N | N | P | N | Y | Excellent web research; weaker first-party Gmail and Calendar story. |
| NotebookLM | Research/notebooks | N | N | N | Y | P | Y | N | N | N | N | N | Y | Best for source-grounded research on owned materials; less of an action agent. |
| GitHub Copilot | Coding assistant | N | V | V | Y | N | Y | N | N | N | Y | N | Y | Good code agent in IDE; external app access is mainly via MCP. |
| Cursor | AI IDE | Y | V | V | Y | N | Y | N | N | N | Y | N | Y | Strong coding IDE; external systems mainly through MCP. |
| Windsurf | AI IDE | Y | V | V | Y | N | Y | N | N | N | Y | N | Y | Similar to Cursor; MCP is the main integration route. |
| Claude Code | Coding agent | Y | V | V | Y | N | Y | Y | Y | N | Y | N | Y | Terminal-first coding agent with broad MCP reach. |
| Codex CLI | Coding agent | Y | V | V | Y | N | N | Y | Y | Y | Y | N | Y | Strong local terminal workflow; OpenAI-centric rather than provider-agnostic. |
| Gemini CLI | Coding / terminal agent | Y | Y | Y | Y | N | N | Y | Y | Y | Y | N | Y | Good terminal choice when official Workspace access is important. |
| Aider | Terminal pair programmer | Y | N | N | Y | N | N | Y | Y | Y | N | Y | Y | Practical for local repos; broad model and provider flexibility. |
| Continue | IDE coding agent/checks | Y | N | N | Y | N | Y | N | N | Y | Y | Y | Y | Useful for repo checks plus flexible model backends. |
| Cline | VS Code coding agent | Y | V | V | Y | N | Y | N | Y | Y | Y | Y | Y | Strong editor agent with browser support and custom provider URL options. |
| Roo Code | VS Code coding agent | Y | V | V | Y | N | Y | N | N | Y | Y | Y | Y | Similar to Cline, with explicit OpenAI-compatible and Z.ai-oriented provider paths. |
| OpenHands | Agent platform | Y | N | N | Y | N | Y | Y | Y | Y | P | P | Y | More of a software-agent runtime than a personal productivity assistant. |
| Open WebUI | Self-hosted AI workspace | Y | V | V | Y | P | Y | N | N | Y | Y | Y | N | Strong self-hosted front end for local and cloud models. |
| LibreChat | Self-hosted chat/agents | Y | V | V | Y | P | Y | N | N | Y | Y | Y | N | Flexible self-hosted stack with custom endpoints and agents. |
| AnythingLLM | Local-first workspace/agents | Y | V | V | Y | P | Y | N | N | Y | Y | Y | Y | Local-first and practical for private document and agent use. |
| LM Studio | Local model runner | Y | V | V | V | N | Y | N | N | N | Y | N | N | Best as a local model host rather than a full productivity agent. |
| Jan | Local AI app | Y | V | V | V | N | Y | N | N | Y | Y | P | N | Local, open-source chat client with MCP support. |
| TypingMind | Multi-model UI | P | V | V | Y | P | Y | N | N | N | Y | P | Y | Good front end when plugins, Zapier, or MCP matter more than native apps. |
| Open Interpreter | Local computer-use agent | Y | N | N | Y | N | P | Y | Y | Y | N | Y | Y | Strong for local computer, files, and terminal; not a native Gmail or Calendar tool. |
| Goose | Local general-purpose agent | Y | V | V | Y | P | Y | Y | Y | Y | Y | P | Y | Broad local agent with deep MCP emphasis. |
| Langflow | Visual agent builder | Y | V | V | Y | P | Y | N | N | Y | Y | P | Y | Better as a builder and orchestrator than as an end-user assistant. |
| Flowise | Visual agent builder | Y | V | V | Y | P | Y | N | N | Y | Y | Y | Y | Good no-code-ish orchestration with MCP and OpenAI-compatible backends. |
| n8n | Automation/AI workflows | Y | Y | Y | V | P | Y | N | N | Y | P | Y | Y | Strongest when the priority is actual business automation over chat UX. |
| Zapier AI / AI Actions | Automation/AI actions | N | Y | Y | V | P | Y | N | N | N | Y | P | Y | Best SaaS route for turning an AI front end into app actions; Zapier MCP is the current strategic path. |

## Supplementary tool matrix

The supplementary list extends the comparison beyond end-user assistants into frameworks, observability systems, gateways, browser agents, and workflow infrastructure.

| Tool | Category | Local | Gmail | Calendar | Files | Research | UI | TUI | CLI | OSS/self-host | MCP/tools | BYO remote AI | Paid | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| LangChain | Agent framework | Y | N | N | Y | P | N | N | N | Y | P | Y | Y | Core framework layer, not an end-user assistant. |
| LangGraph | Agent orchestration | Y | N | N | Y | P | N | N | N | Y | N | Y | Y | Strong graph/runtime choice for custom agents. |
| LangSmith | Observability / agent IDE | P | N | N | P | N | Y | N | P | Y | N | N | Y | Observability and testing surface rather than an access agent. |
| CrewAI | Multi-agent framework | Y | N | N | Y | P | N | N | N | Y | N | Y | Y | Framework for multi-agent app construction. |
| AutoGen | Multi-agent framework | Y | N | N | Y | P | N | N | N | Y | N | Y | Y | Framework for agent coordination and experiments. |
| AutoGen Studio | Low-code agent UI | Y | N | N | P | P | Y | N | N | Y | N | Y | Y | UI layer for AutoGen-style agent workflows. |
| Semantic Kernel | Agent SDK | Y | N | N | P | P | N | N | N | Y | N | Y | Y | SDK for embedding agents into applications. |
| Microsoft Agent Framework | Agent framework | Y | N | N | P | P | N | N | N | P | N | Y | Y | Microsoft-centered agent framework path. |
| Agno | Agent runtime / framework | Y | N | N | Y | P | Y | N | N | Y | N | Y | Y | Agent framework with practical local and app-building focus. |
| Haystack | RAG / agent framework | Y | N | N | Y | P | N | N | N | Y | N | Y | Y | Strong RAG framework, not a productivity assistant. |
| PydanticAI | Agent framework | Y | N | N | P | P | P | N | N | Y | P | Y | N | Developer framework centered on typed Python agents. |
| LlamaIndex | Context / agent framework | Y | N | N | Y | P | N | N | N | Y | N | Y | Y | Strong context and RAG layer. |
| LlamaIndex.TS | TypeScript context / agent framework | Y | N | N | Y | P | N | N | N | Y | N | Y | Y | TypeScript counterpart for context-heavy apps. |
| LlamaParse | Document AI / OCR | N | N | N | Y | N | Y | N | N | N | N | N | Y | Document parsing service rather than an agent. |
| Dify | Agent/workflow platform | Y | N | N | Y | P | Y | N | N | Y | Y | Y | Y | App builder with workflow and agent surfaces. |
| Vellum | AI workflow / agent platform | N | N | N | Y | P | Y | N | N | N | N | N | Y | Hosted workflow platform. |
| Rivet | Visual AI IDE | Y | N | N | P | P | Y | N | N | P | Y | P | N | Visual workflow IDE; self-host status depends on deployment path. |
| LiteLLM | LLM gateway | Y | N | N | N | N | Y | N | N | Y | Y | Y | Y | High-value provider abstraction and routing layer. |
| OpenRouter | Model router / API | N | N | N | N | N | Y | N | N | N | N | Y | Y | Hosted model router with broad OpenAI-compatible API coverage. |
| Vercel AI SDK | App / agent SDK | Y | N | N | Y | P | P | N | N | Y | N | Y | Y | App SDK for AI interfaces and agents, not a standalone assistant. |
| Temporal | Durable workflow engine | Y | N | N | P | N | N | N | N | Y | N | N | Y | Durable orchestration substrate. |
| AgentOps | Agent observability | N | N | N | N | N | Y | N | N | Y | N | N | Y | Observability product for agent runs. |
| Langfuse | LLM observability | Y | N | N | N | N | Y | N | N | Y | Y | N | Y | Open-source observability with self-host path. |
| Opik | LLM observability / eval | Y | N | N | N | N | Y | N | N | Y | N | N | Y | Evaluation and tracing surface. |
| Promptfoo | Eval / red-team | Y | N | N | Y | N | Y | N | Y | Y | N | Y | Y | Practical CLI-driven eval and red-team tool. |
| Ragas | Evaluation library | Y | N | N | Y | N | N | N | Y | Y | N | Y | N | Library for RAG and LLM evaluation. |
| Helicone | AI gateway / observability | Y | N | N | N | N | Y | N | Y | Y | N | Y | Y | Gateway and observability layer with provider flexibility. |
| Arize Phoenix | Observability / eval | Y | N | N | N | N | Y | N | N | Y | N | N | Y | Open-source evaluation and tracing stack. |
| Parea | Observability / eval | N | N | N | Y | N | Y | N | N | N | N | N | Y | Hosted observability and evaluation platform. |
| LastMile AI | Eval / guardrails / workbooks | N | N | N | Y | N | Y | N | N | N | N | N | Y | Hosted workbench and evaluation surface. |
| Fiddler | Guardrails / observability | N | N | N | N | N | Y | N | N | N | N | N | Y | Enterprise observability and governance. |
| Browser Use | Browser agent | Y | N | N | P | P | Y | N | Y | Y | N | Y | Y | Browser automation agent layer. |
| Stagehand | Browser automation framework | Y | N | N | P | N | N | N | N | N | Y | Y | Y | Browser automation framework rather than productivity assistant. |
| Composio | Tool / auth layer for agents | N | V | V | N | N | Y | N | N | N | Y | N | Y | Tool and auth layer for connecting agents to SaaS apps. |
| Gumloop | No-code agents / workflows | N | V | P | V | P | Y | N | N | N | Y | N | Y | SaaS workflow layer with useful app integrations. |
| Braintrust | Observability / eval | Y | N | N | Y | N | Y | N | Y | Y | N | N | Y | Evaluation, prompt, and tracing infrastructure. |
| DSPy | Programming framework | Y | N | N | Y | P | N | N | N | Y | Y | Y | N | Programmatic prompting and optimization framework. |
| Instructor | Structured output library | Y | N | N | Y | N | N | N | N | Y | P | Y | N | Lightweight library for structured outputs. |
| Mem0 | Memory layer | Y | N | N | Y | N | Y | N | N | Y | N | Y | Y | Agent memory layer rather than a full assistant. |
| LobeHub | Self-hosted AI workspace | Y | N | N | Y | P | Y | N | N | Y | Y | Y | N | Self-hostable multi-model workspace. |
| Chatbox AI | Desktop chat client | Y | N | N | Y | P | Y | N | N | N | N | Y | Y | Desktop multi-model chat client. |
| Msty | Local AI desktop app | Y | N | N | Y | P | Y | N | N | N | N | Y | Y | Local AI desktop app with model flexibility. |
| AirOps | Content / workflow platform | N | V | N | Y | Y | Y | N | N | N | Y | N | Y | Workflow/content platform with app integrations. |
| Google ADK | Agent framework | Y | N | N | P | P | N | N | N | Y | Y | Y | N | Google-centered agent development kit. |
| Firebase Genkit | Full-stack AI framework | Y | N | N | P | P | Y | N | N | Y | N | Y | N | Full-stack AI framework for app developers. |
| OpenAI Agents SDK | Agent SDK | Y | N | N | P | P | N | N | N | Y | N | N | N | OpenAI-centered SDK path for agents. |
| big-AGI | Expert AI workspace | Y | N | N | Y | P | Y | N | N | Y | N | Y | Y | Expert workspace/front end; row should be row-source checked before procurement. |
| AG2 | Multi-agent framework | Y | N | N | P | P | N | N | N | Y | Y | Y | N | Multi-agent framework descended from AutoGen ecosystem work. |
| Mastra | TypeScript agent framework | Y | N | N | P | P | N | N | Y | Y | N | Y | Y | TypeScript agent framework with developer-first focus. |
| Superinterface | AI assistant UI / infra | N | N | N | P | N | Y | N | N | Y | N | N | Y | Assistant UI and infrastructure layer. |
| W&B Weave | Observability / eval | N | N | N | N | N | Y | N | N | N | Y | N | Y | Observability and evaluation layer in the W&B ecosystem. |
| LLMWare | Local / private AI framework | Y | N | N | Y | P | P | N | N | Y | N | Y | Y | Local and private AI framework. |
| Portkey AI Gateway | AI gateway | Y | N | N | N | N | Y | N | Y | Y | N | Y | Y | Gateway and provider abstraction layer. |

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

- Last reviewed: 2026-04-15
- Confidence: medium
