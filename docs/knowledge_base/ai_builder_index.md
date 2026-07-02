# AI Builder Index

## What it is
The AI Builder Index is the primary discovery portal for the automation and AI engineering stack documented in this repository. It serves as a high-signal directory that routes builders to the appropriate playbooks, tools, and architectural patterns based on their desired outcomes. As of July 2026, it is optimized for the **MCP 3.0 Task Protocol** ecosystem, helping users navigate the complex landscape of frontier models like [Gemma 3](../tools/ai_knowledge/local_llms.md) and enterprise-grade agentic frameworks.

## What problem it solves
The repository contains a vast array of specialized tools, which can be overwhelming for new users. The AI Builder Index solves "discovery friction" by organizing technical documentation into logical "outcome buckets." Instead of browsing a flat file list, builders can start with a goal (e.g., "Build a private RAG system") and immediately find the curated set of tools and standards needed to achieve it, reducing decision fatigue and implementation errors.

## Where it fits in the stack
**Knowledge Base / Navigation Layer**. It sits at the top of the documentation hierarchy, acting as the bridge between the [Home Index](../../index.md) and the deep technical specifications in `docs/tools/`, `docs/services/`, and `docs/playbooks/`. It defines the "Practical Defaults" for the entire KnowledgeOps system.

## Typical use cases
- **New User Onboarding**: Rapidly identifying the "Starter Stack" for home or small business automation.
- **Agentic Workflow Design**: Selecting the right framework (e.g., [LangGraph](../tools/frameworks/langgraph.md)) and protocol (MCP 3.0) for multi-step tasks.
- **Enterprise RAG Implementation**: Navigating the tools required for high-signal retrieval, such as [Tavily](../tools/providers/tavily.md) and [mem0](../tools/agents/mem0.md).
- **Rapid Prototyping**: Launching MVPs using the [Free AI Website Playbook](free_ai_website_playbook.md) and hosted providers like [Vercel](../tools/development_ops/vercel.md).
- **Local AI Orchestration**: Setting up private, secure environments with [LocalAI](../tools/infrastructure/localai.md) and [Ollama](../../services/ollama.md).

## Strengths
- **Outcome-Driven Navigation**: Focuses on "Jobs to be Done" rather than individual tool features.
- **MCP 3.0 Alignment**: Explicitly highlights tools that support the latest Model Context Protocol standards for agentic interoperability.
- **Visual Mapping**: Utilizes Mermaid diagrams and grid cards for rapid mental model formation.
- **Opinionated Defaults**: Provides clear "Practical Defaults" to help builders ship faster with proven tool combinations.

## Limitations
- **Manual Indexing**: Requires proactive updates as the AI ecosystem (e.g., new [Gemma 3](../tools/ai_knowledge/local_llms.md) variants) evolves.
- **Abstraction Layer**: Provides the roadmap but does not contain the low-level implementation details found in specific tool docs.
- **Path Dependency**: Highly optimized for the repository's core philosophy of AI-assisted development and automation.

## When to use it
- When you are new to the repository and need a structured entry point.
- When starting a new project and deciding on an architecture (e.g., Agentic vs. Flow-based).
- When you need a high-level overview of how [Agentic Workflows](patterns/agentic-workflows.md) and [Infrastructure](../architecture/infrastructure.md) components integrate.

## When not to use it
- If you already know the specific tool you need (use the global search or category indices).
- When seeking low-level API reference documentation (go directly to the tool page in `docs/tools/`).
- For tracking daily repository changes (use the [AI Daily Digest](../../ai-daily-digest/index.md) instead).

## Getting started

To get the most out of the AI Builder Index, follow these steps:

1. **Identify your Goal**: Scan the "Start by outcome" table below.
2. **Follow the Path**: Click the link in the "Start here" column for your chosen goal.
3. **Adopt Defaults**: If unsure, reference the "Recommended entry paths" grid.

### Start by outcome

| Goal | Start here | Then go to | Best for |
| :--- | :--- | :--- | :--- |
| Build a website or app for free | [Free AI Website Playbook](free_ai_website_playbook.md) | [Vercel](../tools/development_ops/vercel.md), [GitHub Pages](../tools/development_ops/github-pages.md), [Supabase](../tools/infrastructure/supabase.md) | Founders, consultants |
| Set up an AI-driven company | [AI Company Starter Stack](ai_company_starter_stack.md) | [n8n](../../services/n8n.md), [mem0](../tools/agents/mem0.md), [Vault](../tools/automation_orchestration/hashicorp-vault.md) | Teams building leverage |
| Choose an agent stack | [Agent Framework Learning Map](agent_framework_learning_map.md) | [LangGraph](../tools/frameworks/langgraph.md), [OpenClaw](../tools/development_ops/openclaw.md) | Builders deciding on frameworks |
| Research markets & leads | [AI Company Starter Stack](ai_company_starter_stack.md) | [Tavily](../tools/providers/tavily.md), [Browser Use](../tools/automation_orchestration/browser-use.md) | Sales and strategy teams |
| Run private / local AI | [AI Company Starter Stack](ai_company_starter_stack.md) | [LocalAI](../tools/infrastructure/localai.md), [Ollama](../../services/ollama.md) | Privacy-sensitive teams |

### Recommended entry paths

<div class="grid cards" markdown>

-   **Build Websites**
    ---
    Start with [Free AI Website Playbook](free_ai_website_playbook.md). Best for rapid deployment on [GitHub Pages](../tools/development_ops/github-pages.md).

-   **Ship AI Products**
    ---
    Start with [AI Tooling Landscape](ai_tooling_landscape.md). Navigate providers and [Agentic Workflows](patterns/agentic-workflows.md).

-   **Run Operations**
    ---
    Start with [AI Company Starter Stack](ai_company_starter_stack.md). Optimize with [n8n](../../services/n8n.md) and [Vault](../tools/automation_orchestration/hashicorp-vault.md).

-   **Private / Local AI**
    ---
    Start with [LocalAI](../tools/infrastructure/localai.md) and [llmfit](../tools/development_ops/llmfit.md) for secure, off-grid intelligence.

</div>

## CLI examples
The AI Builder Index is a documentation portal and does not have a direct CLI. However, you can search the index and related docs using standard terminal tools:

```bash
# Search for specific outcomes within the knowledge base
grep -r "Build a website" docs/knowledge_base/

# Find all tools mentioned in the builder index
grep -o "\[.*\](.*)" docs/knowledge_base/ai_builder_index.md
```

## API examples
The AI Builder Index does not provide a public API. It is designed to be consumed as a static documentation resource within the KnowledgeOps framework. For programmatic access to the underlying data, consider parsing the repository's [mkdocs.yml](../../mkdocs.yml).

## Related tools / concepts
- [Free AI Website Playbook](free_ai_website_playbook.md) — Step-by-step launch guide.
- [AI Company Starter Stack](ai_company_starter_stack.md) — The operational blueprint.
- [AI Tooling Landscape](ai_tooling_landscape.md) — The broader ecosystem map.
- [Agent Framework Learning Map](agent_framework_learning_map.md) — Comparing [LangGraph](../tools/frameworks/langgraph.md) and [OpenClaw](../tools/development_ops/openclaw.md).
- [Agentic Workflows](patterns/agentic-workflows.md) — Designing multi-step [Gemma 3](../tools/ai_knowledge/local_llms.md) tasks.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — The communication standard.
- [Home Index](../../index.md) — Root of the documentation tree.
- [Infrastructure](../architecture/infrastructure.md) — The hardware and software foundation.

## Sources / references
- [KnowledgeOps Documentation Standards](../../standards-and-conventions.md)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/docs/concepts/tasks)
- [Awesome Claude AI Curated List](https://awesomeclaude.ai/)
- [Gemma 3 Technical Report](https://storage.googleapis.com/deepmind-media/gemma/gemma-3-report.pdf)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
