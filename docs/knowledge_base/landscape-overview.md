# Landscape Overview

## What it is
The Landscape Overview is a high-level mapping and statistical summary of the entire AI tool and service ecosystem documented in this repository. It provides a bird's-eye view of the catalogue, showing current metrics, connectivity, and recent additions. As of July 2026, it reflects the state of a rapidly evolving multi-agent KnowledgeOps repository.

## What problem it solves
Navigating hundreds of specialized tools and services can be overwhelming. This overview provides structure, category-based discovery, and growth metrics to help users understand the "big picture" of the repository's contents and the broader AI landscape. It helps identify mature segments and areas ripe for expansion.

## Where it fits in the stack
**Knowledge Base / Ecosystem Map**. It sits at the top of the Knowledge Base layer of the Multi-Agent KnowledgeOps framework, acting as the primary entry point for understanding the breadth and depth of documented resources.

## Typical use cases
- **Discovery**: Finding new tools within a specific category (e.g., "Agents" or "Infrastructure") that fit a specific technical requirement.
- **Triage**: Identifying underdeveloped areas where the repository is actively seeking contributions or technical audits.
- **Trend Analysis**: Tracking the growth and shifting focus of the AI ecosystem over time, such as the rise of Agent Skills and MCP servers.
- **Onboarding**: Providing a comprehensive map for new agents or human contributors to understand the repository's scope.

## Strengths
- **Data-Driven**: Grounded in repository metadata and growth metrics from `data/growth-metrics.json`.
- **Structural Clarity**: Organizes complex information into 21 distinct categories for easy navigation.
- **Graph Insight**: Highlights the most connected and influential tools in the knowledge base, indicating their importance in the stack.
- **July 2026 Context**: Reflects the transition toward autonomous "Software Factories" and agentic orchestration.

## Limitations
- **Repository-Scoped**: Reflects current documentation coverage rather than the entire global AI market.
- **Snapshot-Based**: Metrics are updated during technical audits and may lag behind the absolute latest main branch commits.
- **Manual Synthesis**: While metrics are automated, the strategic "What's New" analysis requires agentic synthesis.

## When to use it
- When you are new to the repository and need a comprehensive map of its contents.
- When you are planning a new integration and want to see existing tools and patterns in that space.
- When you want to see the latest "High Engineering" additions to the catalogue (e.g., Claude Code, ZenML Agent Skills).

## When not to use it
- When you need deep technical setup instructions for a specific tool (refer to its canonical page instead).
- When looking for real-time price comparisons (use the [API Pricing Matrix](api_pricing_free_tiers.md)).
- For fine-grained architectural diagrams (see the [Architecture Component Map](../architecture/component_map.md)).

## Overview
- **Last Generated:** 2026-07-21
- **Total Tools Documented:** 446 (Steady growth from 426 in late June)

## Category Breakdown
Current tool count and focus per category, verified against `all_tools.json`:

| Category | Count | Summary |
| :--- | :--- | :--- |
| **AI Assistants & Knowledge** | 76 | General-purpose chat interfaces, RAG platforms, and local knowledge bases. |
| **Development & Ops** | 58 | Coding assistants, IDEs, and agentic development tools (e.g., Claude Code, Cursor). |
| **Process & Understanding** | 43 | Data extraction, OCR (Tesseract), and document processing (Docling). |
| **Automation & Orchestration** | 37 | Workflow automation, tool integration servers, and MCP implementations. |
| **Benchmarking** | 37 | Evaluation frameworks, security benchmarks (SharpAI), and performance tools. |
| **Agents** | 27 | Multi-agent orchestration frameworks (Letta, Phidata, CrewAI). |
| **Intake & Storage** | 26 | Data collection, self-hosted storage, and document management. |
| **Frameworks** | 24 | Development libraries for building AI-powered applications (AG2, Mastra). |
| **Providers** | 24 | LLM API providers and model marketplaces (Anthropic, DeepSeek). |
| **Infrastructure** | 23 | Model serving (vLLM), inference engines (Ollama), and vector databases. |
| **Calendar & Tasks** | 22 | Scheduling and task management integrations (Sunsama, Amie). |
| **Enterprise AI** | 12 | Enterprise-grade AI search and productivity suites (Elastic, Curiosity). |
| **Orchestration** | 9 | Advanced workflow engines (Argo, ZenML) and data pipeline orchestrators. |
| **Media & Entertainment** | 6 | AI tools for media generation and consumption. |
| **Patterns** | 5 | Common architectural patterns for agentic workflows. |
| **Knowledge Base** | 4 | Foundational AI concepts and research documentation. |
| **Creative & Communication** | 4 | AI tools for creativity and messaging. |
| **Services** | 4 | Self-hosted AI-related services and utilities. |
| **Reference Implementations** | 3 | Working code examples and schema definitions. |
| **Architecture** | 1 | High-level system design and component maps. |
| **Playbooks** | 1 | Step-by-step guides for complex AI workflows. |

## Top 10 Most-Connected Tools
Based on internal links in their 'Related tools / concepts' sections (July 2026):

| Tool | Related Links |
| :--- | :--- |
| MMLU | 13 |
| Gemini | 12 |
| Portracker | 12 |
| qBittorrent Automation | 12 |
| Tabnine | 12 |
| Authentik | 11 |
| Claude Code Container MCP | 11 |
| ClickHouse | 11 |
| Copy.ai | 11 |
| Docker | 11 |

## Underdeveloped Categories
Categories with fewer than 8 documents identified as priority areas for expansion:
- Architecture (1)
- Playbooks (1)
- Reference Implementations (3)
- Knowledge Base (4)
- Creative & Communication (4)
- Services (4)
- Patterns (5)
- Media & Entertainment (6)

## What's New This Month (July 2026)
Significant updates and new additions from the July execution phases:
- **Benchmarking:** Added/upgraded 37 benchmarks (e.g., GPQA, HumanEval, MMLU, SharpAI).
- **Development & Ops:** New tools including Claude Code, Windsurf, and specialized MCP servers.
- **Agents:** Orchestration frameworks Letta, Agno, and Agency Swarm.
- **Process & Understanding:** High-volume telemetry and processing with ClickHouse and Docling.
- **Infrastructure:** Updated support for vLLM, Ollama, and vector databases (Milvus, Pinecone).

## Getting started
To contribute to the landscape or audit existing docs:
1. Run `python3 scripts/growth_tracker.py` to see current metrics.
2. Use `python3 find_oldest_issues.py` to find stale documentation.
3. Follow the 13-section 'High Confidence' standard in `docs/standards.md`.

## CLI examples
The repository metrics can be audited via the CLI:

```bash
# Update the growth metrics snapshot
python3 scripts/growth_tracker.py

# Check for unlinked tool mentions to improve connectivity
python3 scripts/cross_link_report.py

# List categories with fewer than 10 documents
python3 -c "import json; d=json.load(open('data/growth-metrics.json')); print([k for k,v in d['by_category'].items() if v < 10])"
```

## API examples
N/A - This is a documentation/knowledge base overview.

## Related tools / concepts
- [Architecture Component Map](../architecture/component_map.md)
- [Model Routing Guide](model_routing_guide.md)
- [Model Classes](model_classes.md)
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)
- [Agent Frameworks Learning Map](agent_framework_learning_map.md)
- [AI Tool Access Matrix](ai_tool_access_matrix.md)
- [Multi-Agent KnowledgeOps Architecture](../architecture/multi_agent_knowledgeops.md)

## Sources / References
- [All Tools Metadata](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/all_tools.json)
- [Growth Metrics Snapshot (July 2026)](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/growth-metrics.json)
- [MCP 3.0 Standard](https://modelcontextprotocol.io)
- [Gemma 3 Release Notes](https://blog.google/technology/ai/google-gemma-3/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
