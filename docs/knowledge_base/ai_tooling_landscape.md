# AI Tooling Landscape — 2026 Overview

This is a high-level map of the entire AI tooling ecosystem as documented in this repository. It serves as the main entry point for understanding how everything connects.

## Purpose
A living overview that maps the AI tooling landscape into layers, showing how tools relate to each other.

## The Stack (layered view)

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Layer 7: Applications (ChatGPT, Perplexity, Open WebUI)                   │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 6: Agents & Orchestration (CrewAI, AutoGen, LangGraph, n8n)         │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 5: Frameworks (LangChain, LlamaIndex, Haystack, DSPy)               │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 4: Protocols & Standards (MCP, Tool Calling, A2A)                   │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 3: Inference & Serving (vLLM, TGI, Ollama, SGLang)                  │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 2: Models (GPT-4, Claude, Llama, Mistral, Gemini, Qwen)             │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 1: Providers (OpenAI, Anthropic, Google, Meta, Mistral, OpenRouter) │
├───────────────────────────────────────────────────────────────────────────┤
│ Layer 0: Infrastructure (GPUs, quantization, vector DBs)                  │
└───────────────────────────────────────────────────────────────────────────┘
```

### Layer 7: Applications
User-facing interfaces and platforms where humans interact with AI. These provide the final product experience, abstracting the underlying layers for end-users. This layer includes both general-purpose chat interfaces and specialized AI-enhanced development environments.
- **Relevant Pages**: [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Perplexity](../tools/ai_knowledge/perplexity.md), [Open WebUI](../services/open-webui.md), [Claude Code](../tools/development_ops/claude-code.md), [Cursor](../tools/development_ops/cursor.md), [Aider](../tools/development_ops/aider.md), [Zed](../tools/development_ops/zed.md), [Obsidian](../tools/ai_knowledge/obsidian.md), [Logseq](../tools/ai_knowledge/logseq.md), [TeamOut](../tools/ai_knowledge/teamout.md), [Valyu](../tools/ai_knowledge/valyu.md), [ansigpt](../tools/ai_knowledge/ansigpt.md), [Continue Dev](../tools/development_ops/continue_dev.md), [Codeium](../tools/development_ops/codeium.md), [GitHub Copilot](../tools/development_ops/github_copilot.md), [VS Code](../tools/development_ops/vscode.md), [Tabnine](../tools/development_ops/tabnine.md), [Mentat](../tools/development_ops/mentat.md), [GPT Engineer](../tools/development_ops/gpt_engineer.md), [Melty](../tools/development_ops/melty.md), [Superconductor](../tools/development_ops/superconductor.md), [Terminus 2](../tools/development_ops/terminus-2.md), [Junie CLI](../tools/development_ops/junie-cli.md).
- **Key Trends**: Moving from simple chat to agentic IDEs and multimodal research assistants.

### Layer 6: Agents & Orchestration
Systems that coordinate multiple steps, tools, and agents to achieve complex goals. This layer handles reasoning, planning, and task execution using underlying models and frameworks.
- **Relevant Pages**: [Mistral Agents](../tools/providers/mistral.md), [CrewAI](../tools/frameworks/crewai.md), [AutoGen](../tools/frameworks/autogen.md), [LangGraph](../tools/agents/langgraph.md), [n8n](../services/n8n.md), [Agency Swarm](../tools/agents/agency-swarm.md), [Agno](../tools/agents/agno.md), [Bee Agent Framework](../tools/agents/bee-agent-framework.md), [Composio](../tools/agents/composio.md), [Phidata](../tools/agents/phidata.md), [OpenHands](../tools/development_ops/openhands.md), [Droid](../tools/development_ops/droid.md), [Plandex](../tools/development_ops/plandex.md), [OpenSwarm](../tools/development_ops/openswarm.md), [OpenClaw](../tools/development_ops/openclaw.md), [Jules](../tools/ai_knowledge/jules.md), [Browser Use](../tools/automation_orchestration/browser-use.md), [Zapier](../tools/automation_orchestration/zapier.md), [Make](../tools/automation_orchestration/make.md), [Skyvern](../tools/automation_orchestration/skyvern.md), [Atlassian Jira MCP](../tools/automation_orchestration/atlassian-jira-mcp.md), [ServiceNow MCP](../tools/automation_orchestration/servicenow-mcp.md), [CliHub](../tools/automation_orchestration/clihub.md).
Systems that coordinate multiple steps, tools, and agents to achieve complex goals. This layer handles reasoning, planning, and task execution using underlying models and frameworks. It is where autonomous decision-making and environment interaction are managed.
- **Key Trends**: Shift from linear chains to complex, stateful multi-agent graphs.



### Layer 5: Frameworks
Development libraries used to build AI applications, handling prompt management, tool integration, and RAG logic. They provide the abstraction layer between models and applications. These frameworks simplify the process of constructing complex AI workflows and integrating various data sources.
- **Relevant Pages**: [LangChain](../tools/ai_knowledge/langchain.md), [LlamaIndex](../tools/ai_knowledge/llamaindex.md), [Haystack](../tools/frameworks/haystack.md), [DSPy](../tools/frameworks/dspy.md), [Semantic Kernel](../tools/frameworks/semantic-kernel.md), [Smolagents](../tools/frameworks/smolagents.md), [Mycelium](../tools/frameworks/mycelium.md), [Dify](../tools/ai_knowledge/dify.md), [Flowise](../tools/ai_knowledge/flowise.md), [RAGFlow](../tools/process_understanding/ragflow.md).
- **Key Trends**: Increased focus on programmatic prompt optimization and modular RAG.

### Layer 4: Protocols & Standards
The "glue" that allows models to interact with tools and other agents consistently. These standards ensure interoperability across the ecosystem. By establishing common interfaces, they prevent vendor lock-in and enable tool reuse across different frameworks.
- **Relevant Pages**: [Model Context Protocol (MCP)](agent_protocols.md), [Agent Client Protocol (ACP)](agent_protocols.md), [Tool Calling & MCP Patterns](patterns/tool-calling-and-mcp.md), [Mistral AI (Native MCP)](../tools/providers/mistral.md), [MCP Registry](../tools/automation_orchestration/mcp-registry.md).
- **Key Trends**: Rapid adoption of MCP as the standard for model-to-tool communication.

### Layer 3: Inference & Serving
Engines that run model weights and provide APIs for applications to consume. This layer is responsible for the actual execution of model inference. It optimizes performance, handles concurrency, and provides the necessary scaling for production deployments.
- **Relevant Pages**: [vLLM](../tools/infrastructure/vllm.md), [Text Generation Inference (TGI)](../tools/infrastructure/tgi.md), [Ollama](../services/ollama.md), [SGLang](../tools/infrastructure/sglang.md), [Aphrodite Engine](../tools/infrastructure/aphrodite-engine.md), [ExLlamaV2](../tools/infrastructure/exllamav2.md), [llama.cpp](../tools/infrastructure/llama-cpp.md), [MLX](../tools/infrastructure/mlx.md), [LiteLLM](../services/litellm.md).
- **Key Trends**: Layer 3 is consolidating around vLLM and SGLang for high-performance serving.

### Layer 2: Models
The core reasoning engines (LLMs, VLMs) that process information and generate text or actions. These are the fundamental units of intelligence in the stack. This layer includes both general-purpose foundation models and specialized models for coding, reasoning, or multimodality.
- **Relevant Pages**: [OpenAI Models](../tools/ai_knowledge/openai.md), [Anthropic Claude](../tools/providers/anthropic.md), [Meta Llama](../tools/ai_knowledge/local_llms.md), [Mistral](../tools/providers/mistral.md), [Google Gemini](../tools/ai_knowledge/google-gemini.md), [DeepSeek](../tools/ai_knowledge/deepseek.md), [Model Classes](model_classes.md).
- **Key Trends**: Rise of specialized reasoning models using test-time compute.

### Layer 1: Providers
Companies and platforms that host models and provide them as-a-service via API. They handle the scale and infrastructure required for model access. These providers offer varying levels of cost, speed, and privacy, allowing users to choose the best fit for their needs.
- **Relevant Pages**: [OpenRouter](../tools/ai_knowledge/openrouter.md), [Groq](../tools/providers/groq.md), [Fireworks AI](../tools/providers/fireworks.md), [Together AI](../tools/providers/together.md), [Replicate](../tools/providers/replicate.md), [Mistral AI](../tools/providers/mistral.md), [Cohere](../tools/providers/cohere.md).
- **Key Trends**: Providers are competing on speed (tokens/sec) and lower costs.

### Layer 0: Infrastructure
The underlying hardware, storage, and low-level optimizations like quantization and vector databases that power the entire stack. This foundation ensures that higher-level services run efficiently and securely. It also includes the critical data supply chain components for ingestion and preparation.
- **Relevant Pages**: [Home Lab Architecture](../architecture/infrastructure.md), [TrueNAS SCALE](../architecture/infrastructure.md), [Tailscale](../services/tailscale.md), [OpenPipe (Fine-tuning)](../tools/infrastructure/openpipe.md), [Crawl4AI](../tools/process_understanding/crawl4ai.md), [Firecrawl](../tools/process_understanding/firecrawl.md), [OCRmyPDF](../tools/process_understanding/ocrmypdf.md), [PageIndex](../tools/process_understanding/pageindex.md), [CalDAV](../tools/intake_storage/caldav.md), [ZSE](../tools/infrastructure/zse.md).
- **Key Trends**: Move towards hybrid infrastructure combining local GPU power with cloud scaling.

---

## Key Patterns
- **[Retrieval-Augmented Generation (RAG)](patterns/rag.md)**: Grounding models with external data to improve accuracy.
- **[Tool Calling & MCP](patterns/tool-calling-and-mcp.md)**: Standardized interaction between models and external functions.
- **[LLM Trust Boundaries](patterns/llm-trust-boundaries.md)**: Security and privacy considerations in agentic systems.
- **[Agent Skills Best Practices](patterns/skills-best-practices.md)**: Optimizing how agents use tools.
- **[Claude Tool Search](patterns/claude-tool-search.md)**: Specific patterns for maximizing Anthropic's tool use.
- **[OpenClaw Workflow Prompts](patterns/openclaw-workflow-prompts.md)**: Library of prompts for specialized workflows.

## How to use this repo
- **"I want to run LLMs locally"** → [Ollama](../services/ollama.md), [MLX](../tools/infrastructure/mlx.md), [llama.cpp](../tools/infrastructure/llama-cpp.md), [ExLlamaV2](../tools/infrastructure/exllamav2.md)
- **"I want to build an AI agent"** → [CrewAI](../tools/frameworks/crewai.md)/[AutoGen](../tools/frameworks/autogen.md) + [LangGraph](../tools/agents/langgraph.md) + [MCP](agent_protocols.md)
- **"I want to add AI to my app"** → [LangChain](../tools/ai_knowledge/langchain.md)/[LlamaIndex](../tools/ai_knowledge/llamaindex.md) + [OpenRouter](../tools/ai_knowledge/openrouter.md) (provider API)
- **"I want to evaluate models"** → [Benchmarking tools](../tools/benchmarking/index.md)
- **"I want to stay current"** → [Essential AI Reading List](ai_reading_list.md)

## Sources / references
- [Sequoia: Generative AI's Act Two](https://www.sequoiacap.com/article/generative-ai-act-two/)
- [A16Z: Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications/)
- [MAD Landscape 2024](https://mad.firstmark.com/)

## Contribution Metadata
- Last reviewed: 2026-03-02
- Confidence: high
