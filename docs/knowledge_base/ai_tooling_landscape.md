# AI Tooling Landscape — 2026 Overview

This is a high-level map of the entire AI tooling ecosystem as documented in this repository. It serves as the main entry point for understanding how various tools, frameworks, and protocols connect to form a modern AI-powered stack.

## Purpose
A living overview that maps the AI tooling landscape into layers, showing how tools relate to each other. It helps navigate the repository by providing a conceptual framework for the diverse range of tools catalogued here.

## The Stack (Layered View)

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Layer 7: Applications (ChatGPT, Perplexity, Open WebUI, Cursor)           │
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

| Layer | Category | Description |
| :--- | :--- | :--- |
| **Layer 7** | **Applications** | User-facing interfaces and platforms where humans interact with AI. |
| **Layer 6** | **Agents & Orchestration** | High-level systems that coordinate multiple steps, tools, and agents to achieve complex goals. |
| **Layer 5** | **Frameworks** | Development libraries used to build AI applications, handling prompt management and tool integration. |
| **Layer 4** | **Protocols & Standards** | The "glue" that allows models to interact with tools and other agents consistently. |
| **Layer 3** | **Inference & Serving** | Engines that run model weights and provide APIs for applications to consume. |
| **Layer 2** | **Models** | The core reasoning engines (LLMs, VLMs) that process information and generate text/actions. |
| **Layer 1** | **Providers** | Companies and platforms that host models and provide them as-a-service. |
| **Layer 0** | **Infrastructure** | The underlying hardware, storage, and low-level optimizations that power everything. |

---

### Layer 7: Applications
The top of the stack where AI meets the end-user. These tools provide polished interfaces for chat, search, and specialized tasks like coding or knowledge management. They abstract the underlying complexity, allowing non-technical users to leverage model capabilities directly in their workflows.
- **Relevant Pages**: [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Perplexity](../tools/ai_knowledge/perplexity.md), [Open WebUI](../services/open-webui.md), [Claude Code](../tools/development_ops/claude-code.md), [Cursor](../tools/development_ops/cursor.md), [Aider](../tools/development_ops/aider.md), [Zed](../tools/development_ops/zed.md), [Obsidian](../tools/ai_knowledge/obsidian.md).
- **Key Trends**: Consolidation of "chat" into multimodal workspaces and the rapid rise of agentic IDEs that can execute code autonomously.

### Layer 6: Agents & Orchestration
Systems that move beyond single prompts to autonomous or semi-autonomous execution of complex workflows. These agents use reasoning to plan, use tools, and iterate until a goal is achieved. This layer is responsible for maintaining state and managing long-running tasks that require multiple model interactions.
- **Relevant Pages**: [CrewAI](../tools/frameworks/crewai.md), [AutoGen](../tools/frameworks/autogen.md), [LangGraph](../tools/agents/langgraph.md), [n8n](../services/n8n.md), [Agency Swarm](../tools/agents/agency-swarm.md), [Agno](../tools/agents/agno.md), [Bee Agent Framework](../tools/agents/bee-agent-framework.md), [Composio](../tools/agents/composio.md), [Phidata](../tools/agents/phidata.md), [OpenHands](../tools/development_ops/openhands.md), [Droid](../tools/development_ops/droid.md), [Browser Use](../tools/automation_orchestration/browser-use.md).
- **Key Trends**: Shift from linear chains to graph-based agentic workflows with long-term memory and human-in-the-loop confirmation.

### Layer 5: Frameworks
The building blocks for AI developers. These libraries abstract provider APIs and provide standardized tools for RAG, prompt engineering, and evaluation. Frameworks allow developers to swap models easily and build complex logic that bridges the gap between raw models and agentic behavior.
- **Relevant Pages**: [LangChain](../tools/ai_knowledge/langchain.md), [LlamaIndex](../tools/ai_knowledge/llamaindex.md), [Haystack](../tools/frameworks/haystack.md), [DSPy](../tools/frameworks/dspy.md), [Semantic Kernel](../tools/frameworks/semantic-kernel.md), [Smolagents](../tools/frameworks/smolagents.md), [Dify](../tools/ai_knowledge/dify.md), [Flowise](../tools/ai_knowledge/flowise.md).
- **Key Trends**: Frameworks are moving toward "un-opinionated" orchestration, focusing on observability and better integration with production monitoring.

### Layer 4: Protocols & Standards
Ensuring interoperability between models, the tools they use, and the environments they operate in. These standards allow a single tool to be used across multiple different agents or platforms without rewriting integration logic. They provide the common language that defines how data and capabilities are exchanged.
- **Relevant Pages**: [Model Context Protocol (MCP)](agent_protocols.md), [Tool Calling & MCP Patterns](patterns/tool-calling-and-mcp.md), [Agent Client Protocol (ACP)](agent_protocols.md).
- **Key Trends**: MCP is rapidly becoming the industry standard for connecting any LLM to any local or remote data source or tool.

### Layer 3: Inference & Serving
How we run model weights, either in the cloud or on local consumer hardware. This layer handles the conversion of model parameters into a functional API that can process tokens at scale. It includes optimizations for throughput, latency, and memory efficiency to make running models cost-effective.
- **Relevant Pages**: [vLLM](../tools/infrastructure/vllm.md), [Text Generation Inference (TGI)](../tools/infrastructure/tgi.md), [Ollama](../services/ollama.md), [SGLang](../tools/infrastructure/sglang.md), [Aphrodite Engine](../tools/infrastructure/aphrodite-engine.md), [ExLlamaV2](../tools/infrastructure/exllamav2.md), [llama.cpp](../tools/infrastructure/llama-cpp.md), [MLX](../tools/infrastructure/mlx.md), [LiteLLM](../services/litellm.md).
- **Key Trends**: Layer 3 is consolidating around vLLM and SGLang for high-throughput enterprise serving, while Ollama dominates local developer use.

### Layer 2: Models
The core reasoning engines themselves, categorized by their capabilities and training objectives. These models are the "brains" of the entire operation, trained on vast datasets to understand and generate human language, code, and images. They are increasingly specialized into different classes, from general-purpose assistants to deep-reasoning experts.
- **Relevant Pages**: [OpenAI Models](../tools/ai_knowledge/openai.md), [Anthropic Claude](../tools/providers/anthropic.md), [Meta Llama](../tools/ai_knowledge/local_llms.md), [Mistral](../tools/providers/mistral.md), [Google Gemini](../tools/ai_knowledge/google-gemini.md), [DeepSeek](../tools/ai_knowledge/deepseek.md), [Model Classes](model_classes.md).
- **Key Trends**: Rapid advancement in reasoning-specialized models (e.g., DeepSeek-R1, OpenAI o1) that use test-time compute.

### Layer 1: Providers
The platforms and marketplaces that make models accessible via unified APIs. These providers manage the infrastructure and scaling required to serve models to millions of users simultaneously. They offer additional services like fine-tuning, monitoring, and safety filtering alongside raw model access.
- **Relevant Pages**: [OpenRouter](../tools/ai_knowledge/openrouter.md), [Groq](../tools/providers/groq.md), [Fireworks AI](../tools/providers/fireworks.md), [Together AI](../tools/providers/together.md), [Replicate](../tools/providers/replicate.md), [Mistral AI](../tools/providers/mistral.md), [Cohere](../tools/providers/cohere.md).
- **Key Trends**: Providers are competing on inference speed (LPUs) and breadth of access to both open and closed models.

### Layer 0: Infrastructure
The foundation of the lab: hardware, storage, and networking optimizations. This layer includes the physical GPUs and CPUs that perform the computations, as well as the storage systems for model weights and vector data. It also covers the networking protocols that ensure low-latency communication between services.
- **Relevant Pages**: [Home Lab Architecture](../architecture/infrastructure.md), [TrueNAS SCALE](../architecture/infrastructure.md), [Tailscale](../services/tailscale.md), [OpenPipe (Fine-tuning)](../tools/infrastructure/openpipe.md).
- **Key Trends**: Move toward hybrid local/cloud setups using tools like Tailscale to securely bridge home-lab resources with cloud providers.

---

## Key Patterns
Common architectural blueprints used across the stack:
- **[Retrieval-Augmented Generation (RAG)](patterns/rag.md)**: Grounding models with external data to improve accuracy and reduce hallucinations.
- **[Tool Calling & MCP](patterns/tool-calling-and-mcp.md)**: Standardized ways for LLMs to use external functions and interact with data sources.
- **[LLM Trust Boundaries](patterns/llm-trust-boundaries.md)**: Security and privacy considerations in agentic systems, defining where data can flow.
- **[Agent Skills Best Practices](patterns/skills-best-practices.md)**: Optimizing agent performance through better tool descriptions and execution patterns.
- **[Claude Tool Search](patterns/claude-tool-search.md)**: Specific patterns for maximizing the effectiveness of Anthropic's tool-calling capabilities.

---

## How to use this repo

### Personas Guide
- **"I want to run LLMs locally"** → Start with [Ollama](../services/ollama.md) and [Open WebUI](../services/open-webui.md). For advanced optimization on specific hardware, explore [llama.cpp](../tools/infrastructure/llama-cpp.md), [MLX](../tools/infrastructure/mlx.md) (for Mac), or [ExLlamaV2](../tools/infrastructure/exllamav2.md).
- **"I want to build an AI agent"** → Look at [CrewAI](../tools/frameworks/crewai.md) or [AutoGen](../tools/frameworks/autogen.md) for multi-agent workflows, or [LangGraph](../tools/agents/langgraph.md) for stateful, cyclic graphs. Use [MCP](agent_protocols.md) to give them tools.
- **"I want to add AI to my app"** → Start with [LangChain](../tools/ai_knowledge/langchain.md) or [LlamaIndex](../tools/ai_knowledge/llamaindex.md) and connect to a [Provider](../tools/providers/index.md) like [OpenRouter](../tools/ai_knowledge/openrouter.md).
- **"I want to evaluate models"** → Check the [Benchmarking](../tools/benchmarking/index.md) section for tools like [Chatbot Arena](../tools/benchmarking/chatbot-arena.md), [SWE-bench](../tools/benchmarking/swe-bench.md), or [LM Evaluation Harness](../tools/benchmarking/lm-evaluation-harness.md).
- **"I want to stay current"** → Follow the [Essential AI Reading List](ai_reading_list.md) and monitor the [Daily Ingestion Logs](../new-sources.md) for new tool discoveries.

---

## Sources / references
- [Sequoia Capital: Generative AI's Act Two](https://www.sequoiacap.com/article/generative-ai-act-two/)
- [A16Z: Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications/)
- [MAD Landscape (Machine Learning, AI & Data)](https://mad.firstmark.com/)
- [MCP Documentation (Anthropic)](https://modelcontextprotocol.io/)

---

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
