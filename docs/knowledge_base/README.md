# Knowledge Base

This section contains deep dives into the technologies, protocols, and conceptual frameworks that power the AI Hub.

## Start By Goal

<div class="grid cards" markdown>

-   **Build A Website Or App**

    ---

    Start with [AI Builder Index](ai_builder_index.md), then use the [Free AI Website Playbook](free_ai_website_playbook.md).

-   **Build An AI-Driven Company Stack**

    ---

    Start with [AI Company Starter Stack](ai_company_starter_stack.md).

-   **Understand The Full Ecosystem**

    ---

    Start with [AI Tooling Landscape — 2026 Overview](ai_tooling_landscape.md).

-   **Choose An Assistant Or Agent**

    ---

    Start with [AI Tool Access Matrix](ai_tool_access_matrix.md).

-   **Choose The Right Model**

    ---

    Start with [Model Routing Guide](model_routing_guide.md).

-   **Review The Strongest Repos From GitHub Stars**

    ---

    Start with [Starred AI / Agent Repositories Over 10K Stars](starred_ai_agent_repos.md).

</div>

## Getting Started with the KB

The Knowledge Base (KB) is designed to take you from conceptual understanding to production-ready implementation. To get the most out of this resource, we recommend the following tiered approach:

### 1. Orientation & Landscape
Begin by understanding the "Big Picture" of the current AI ecosystem.
- **Review**: [AI Tooling Landscape](ai_tooling_landscape.md) for a categorical overview.
- **Matrix**: Consult the [AI Tool Access Matrix](ai_tool_access_matrix.md) to see which tools have the permissions (Gmail, Files, etc.) you need.

### 2. Strategic Selection
Once oriented, choose the specific models and stacks that fit your goals.
- **Model Choice**: Use the [Model Routing Guide](model_routing_guide.md) to determine if you need Haiku, Sonnet, or an O-series reasoning model.
- **Default Stacks**: If building a company, start with the [AI Company Starter Stack](ai_company_starter_stack.md).

### 3. Implementation Patterns
Transition from "what to use" to "how to build" using canonical patterns.
- **Foundational**: Master the [RAG Pattern](patterns/rag-pattern.md) and [Agentic Workflows](patterns/agentic-workflows.md).
- **Advanced**: Explore [Data Copilot Agentic RAG](patterns/data-copilot-agentic-rag.md) for complex data synthesis.

### 4. Safety & Governance
Ensure your AI systems are resilient and secure before deployment.
- **Security**: Audit your [LLM Trust Boundaries](patterns/llm-trust-boundaries.md).
- **Quality**: Review the [Standards](standards.md) to ensure your own documentation and workflows remain high-confidence.

## Curated Guides

- [**AI Builder Index**](ai_builder_index.md) - Discovery-oriented entry point for building websites, products, operations, and internal AI systems.
- [**Free AI Website Playbook**](free_ai_website_playbook.md) - Which website types fit free tiers, which hosts to choose, and how to prompt an LLM to build them.
- [**AI Company Starter Stack**](ai_company_starter_stack.md) - Opinionated default stack for building a company where AI is part of daily operations.
- [**AI Tooling Landscape — 2026 Overview**](ai_tooling_landscape.md) - High-level map of the entire AI tooling ecosystem in this repository.
- [**AI Tool Access Matrix**](ai_tool_access_matrix.md) - Capability matrix for assistants, coding agents, workflow tools, self-hosted workspaces, and agent frameworks.
- [**Model Routing Guide**](model_routing_guide.md) - Clear defaults and escalation rules for Haiku, Sonnet, Opus, GPT-5.4 effort levels, and GPT-5.3 Codex.
- [**Starred AI / Agent Repositories Over 10K Stars**](starred_ai_agent_repos.md) - Practical ranking and usage guide based on your starred GitHub repos.

## Deep Dives

- [**Model Classes**](model_classes.md) - Understanding the different types of LLMs (MoE, Reasoning, Multimodal, etc.).
- [**System Prompts**](system_prompts.md) - Foundational instructions for frontier models and "high engineering" persona design.
- [**Model Comparison and Evaluation**](model_comparison_and_evaluation.md) - Guide to LLM leaderboards, benchmarks, and metrics.
- [**Model Routing Guide**](model_routing_guide.md) - Practical task-routing guidance for choosing the right model and effort level.
- [**AI Tool Access Matrix**](ai_tool_access_matrix.md) - Side-by-side access surface comparison across Gmail, Calendar, files, research, MCP, local use, and provider flexibility.
- [**Agent Protocols**](agent_protocols.md) - Deep dive into MCP (Model Context Protocol) and ACP (Agent Control Protocol).
- [**API Pricing & Free Tier Matrix**](api_pricing_free_tiers.md) - Canonical tracker for provider pricing links and current free-tier availability.
- [**AI Signal Sources**](ai_signal_sources.md) - Curated company and independent technical blogs worth monitoring.
- [**Essential AI Reading List**](ai_reading_list.md) — A curated guide to high-signal blogs, newsletters, and podcasts.
- [**Architecture & Flows**](../architecture/README.md) - High-level system design.

## Implementation Patterns

- [**RAG Pattern**](patterns/rag-pattern.md) - Canonical implementation for Retrieval Augmented Generation.
- [**Agentic Workflows**](patterns/agentic-workflows.md) - Designing loops and multi-agent systems.
- [**LLM Trust Boundaries**](patterns/llm-trust-boundaries.md) - Security patterns for handling untrusted data.
- [**Data Copilot MCP Tooling**](patterns/data-copilot-mcp-tooling.md) - Leveraging the Model Context Protocol for tool discovery and data synthesis.
- [**Data Copilot Agentic RAG**](patterns/data-copilot-agentic-rag.md) - Advanced RAG patterns using multi-agent orchestration for data tasks.
- [**n8n Error Handling**](patterns/n8n-error-handling.md) - Building resilient automation workflows.

## Learning Paths

### For Developers
- [AI Builder Index](ai_builder_index.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Software Factories](patterns/software-factories.md)

### For Operations
- [AI Company Starter Stack](ai_company_starter_stack.md)
- [n8n Error Handling](patterns/n8n-error-handling.md)
- [OpenClaw Workflow Prompts](patterns/openclaw-workflow-prompts.md)

### For Researchers
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [AI Signal Sources](ai_signal_sources.md)
- [Essential AI Reading List](ai_reading_list.md)

## 🚀 Purpose
The knowledge base serves as the "theory" section of the repository, providing the necessary context to effectively connect and configure the tools in the [Tool Catalogue](../tools/README.md). It is designed to be a living resource that evolves alongside the frontier of AI capabilities.

## 🛠️ Contribution
We welcome deep dives into new technologies. Please follow the [Contributing Guide](../CONTRIBUTING.md). When adding new articles, ensure they follow the [Standards](standards.md) and include relevant [Architecture](../architecture/README.md) cross-links.

## Knowledge Maintenance
This KB is maintained through automated "Ralph-loops" that:
- Audit document quality and structural compliance.
- Update model capability matrices based on new releases.
- Deepen "Medium Confidence" documents into "High Confidence" references.
- Verify cross-link integrity across the repository.

## Sources / References
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [OpenAI Platform](https://platform.openai.com/docs)
- [Home](../index.md)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high
