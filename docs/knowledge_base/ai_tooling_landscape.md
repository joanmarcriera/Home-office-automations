# AI Tooling Landscape — 2026 Overview

This is a high-level map of the entire AI tooling ecosystem as documented in this repository. It serves as the main entry point for understanding how various tools, frameworks, and protocols connect to form a modern AI-powered stack.

## Purpose
A living overview that maps the AI tooling landscape into layers, showing how tools relate to each other. It helps navigate the repository by providing a conceptual framework for the diverse range of tools catalogued here.

## The Stack (Layered View)

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

### Layer 7: Applications
The top of the stack where AI meets the end-user. These tools provide polished interfaces for chat, search, and specialized tasks.
- **Tools**: [ChatGPT](../tools/ai_knowledge/chatgpt.md), [Perplexity](../tools/ai_knowledge/perplexity.md), [Open WebUI](../services/open-webui.md), [Claude Code](../tools/development_ops/claude-code.md), [Cursor](../tools/development_ops/cursor.md), [Aider](../tools/development_ops/aider.md).
- **Trends**: Consolidation of "chat" into multimodal workspaces and the rise of agentic IDEs.

### Layer 6: Agents & Orchestration
Systems that move beyond single prompts to autonomous or semi-autonomous execution of workflows.
- **Tools**: [CrewAI](../tools/frameworks/crewai.md), [AutoGen](../tools/frameworks/autogen.md), [LangGraph](../tools/agents/langgraph.md), [n8n](../services/n8n.md), [Agency Swarm](../tools/agents/agency-swarm.md), [Agno](../tools/agents/agno.md), [Bee Agent Framework](../tools/agents/bee-agent-framework.md), [Composio](../tools/agents/composio.md), [Phidata](../tools/agents/phidata.md), [OpenHands](../tools/development_ops/openhands.md), [Droid](../tools/development_ops/droid.md).
- **Trends**: Shift from linear chains to graph-based agentic workflows with long-term memory.

### Layer 5: Frameworks
The building blocks for AI developers. These libraries abstract provider APIs and provide tools for RAG and chain-of-thought.
- **Tools**: [LangChain](../tools/ai_knowledge/langchain.md), [LlamaIndex](../tools/ai_knowledge/llamaindex.md), [Haystack](../tools/frameworks/haystack.md), [DSPy](../tools/frameworks/dspy.md), [Semantic Kernel](../tools/frameworks/semantic-kernel.md), [Smolagents](../tools/frameworks/smolagents.md).
- **Trends**: Frameworks are becoming more lightweight, focusing on "un-opinionated" orchestration.

### Layer 4: Protocols & Standards
Ensuring interoperability between models and the environments they operate in.
- **Tools**: [Model Context Protocol (MCP)](agent_protocols.md), [Claude Tool Search](patterns/claude-tool-search.md), [Agent Protocols](agent_protocols.md).
- **Trends**: MCP is rapidly becoming the standard for connecting LLMs to local and remote data sources.

### Layer 3: Inference & Serving
How we run models, either locally or in self-hosted environments.
- **Tools**: [vLLM](../tools/infrastructure/vllm.md), [Text Generation Inference (TGI)](../tools/infrastructure/tgi.md), [Ollama](../services/ollama.md), [SGLang](../tools/infrastructure/sglang.md), [Aphrodite Engine](../tools/infrastructure/aphrodite-engine.md), [ExLlamaV2](../tools/infrastructure/exllamav2.md), [llama.cpp](../tools/infrastructure/llama-cpp.md), [MLX](../tools/infrastructure/mlx.md).
- **Trends**: Layer 3 is consolidating around vLLM and SGLang for high-throughput serving.

### Layer 2: Models
The reasoning engines themselves.
- **Tools**: [OpenAI GPT-4](../tools/ai_knowledge/openai.md), [Anthropic Claude](../tools/providers/anthropic.md), [Meta Llama](../tools/ai_knowledge/local_llms.md), [Mistral](../tools/providers/mistral.md), [Google Gemini](../tools/ai_knowledge/google-gemini.md), [DeepSeek](../tools/ai_knowledge/deepseek.md).
- **Trends**: Rapid advancement in reasoning-specialized models (e.g., DeepSeek-R1, OpenAI o1).

### Layer 1: Providers
The platforms that make models accessible via API.
- **Tools**: [OpenRouter](../tools/ai_knowledge/openrouter.md), [Groq](../tools/providers/groq.md), [Fireworks AI](../tools/providers/fireworks.md), [Together AI](../tools/providers/together.md), [Replicate](../tools/providers/replicate.md), [Mistral AI](../tools/providers/mistral.md), [Cohere](../tools/providers/cohere.md).
- **Trends**: Providers are competing on speed (Groq) and breadth of model access (OpenRouter).

### Layer 0: Infrastructure
The foundation of the lab.
- **Tools**: [Home Lab Architecture](../architecture/infrastructure.md), [TrueNAS SCALE](../architecture/infrastructure.md), [Tailscale](../services/tailscale.md).
- **Components**: GPUs (NVIDIA/Apple Silicon), quantization techniques, and vector databases (integrated into RAG patterns).

## Key Patterns
Common architectural blueprints used across the stack:
- **[RAG (Retrieval-Augmented Generation)](patterns/rag.md)**: Grounding models with external data.
- **[Tool Calling & MCP](patterns/claude-tool-search.md)**: Standardized ways for LLMs to use external functions.
- **[LLM Trust Boundaries](patterns/llm-trust-boundaries.md)**: Security and privacy considerations in agentic systems.
- **[Agent Skills Best Practices](patterns/skills-best-practices.md)**: Optimizing agent performance.

## How to use this repo

### Personas Guide
- **"I want to run LLMs locally"** → Start with [Ollama](../services/ollama.md) and [Open WebUI](../services/open-webui.md). Explore [llama.cpp](../tools/infrastructure/llama-cpp.md) or [MLX](../tools/infrastructure/mlx.md) for more control.
- **"I want to build an AI agent"** → Look at [CrewAI](../tools/frameworks/crewai.md) or [LangGraph](../tools/agents/langgraph.md). Use [MCP](agent_protocols.md) to give them tools.
- **"I want to add AI to my app"** → Start with [LangChain](../tools/ai_knowledge/langchain.md) or [LlamaIndex](../tools/ai_knowledge/llamaindex.md) and connect to a [Provider](../tools/providers/index.md).
- **"I want to evaluate models"** → Check the [Benchmarking](../tools/benchmarking/index.md) section for tools like [Chatbot Arena](../tools/benchmarking/chatbot-arena.md) or [LM Evaluation Harness](../tools/benchmarking/lm-evaluation-harness.md).
- **"I want to stay current"** → Follow the [Reading List](ai_reading_list.md) and monitor the [Daily Ingestion Logs](../new-sources.md).

## Sources / references
- [Sequoia Capital: Generative AI's Act Two](https://www.sequoiacap.com/article/generative-ai-act-two/)
- [A16Z: Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications/)
- [MAD Landscape (Machine Learning, AI & Data)](https://mad.firstmark.com/)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
