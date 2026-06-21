# Landscape Overview

## What it is
The Landscape Overview is a high-level mapping and statistical summary of the entire AI tool and service ecosystem documented in this repository. It provides a bird's-eye view of the catalogue, showing current metrics, connectivity, and recent additions. As of June 2026, it reflects the state of a rapidly evolving multi-agent KnowledgeOps repository.

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
- **Structural Clarity**: Organizes complex information into 13+ distinct categories for easy navigation.
- **Graph Insight**: Highlights the most connected and influential tools in the knowledge base, indicating their importance in the stack.
- **June 2026 Context**: Reflects the transition toward autonomous "Software Factories" and agentic orchestration.

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
- **Last Generated:** 2026-06-21
- **Total Tools Documented:** 426 (Steady growth from 423 in early June)

## Category Breakdown
Current tool count and focus per category, verified against `all_tools.json`:

| Category | Count | Summary |
| :--- | :--- | :--- |
| **AI Assistants & Knowledge** | 73 | General-purpose chat interfaces, RAG platforms, and local knowledge bases. |
| **Development & Ops** | 57 | Coding assistants, IDEs, and agentic development tools (e.g., Claude Code, Cursor). |
| **Benchmarking** | 37 | Evaluation frameworks, security benchmarks (SharpAI), and performance tools. |
| **Process & Understanding** | 30 | Data extraction, OCR (Tesseract), and document processing (Docling). |
| **Automation & Orchestration** | 29 | Workflow automation, tool integration servers, and MCP implementations. |
| **Agents** | 27 | Multi-agent orchestration frameworks (Letta, Phidata, CrewAI). |
| **Frameworks** | 24 | Development libraries for building AI-powered applications (AG2, Mastra). |
| **Providers** | 23 | LLM API providers and model marketplaces (Anthropic, DeepSeek). |
| **Infrastructure** | 22 | Model serving (vLLM), inference engines (Ollama), and vector databases. |
| **Calendar & Tasks** | 21 | Scheduling and task management integrations (Sunsama, Amie). |
| **Enterprise AI** | 12 | Enterprise-grade AI search and productivity suites (Elastic, Curiosity). |
| **Intake & Storage** | 9 | Data collection, self-hosted storage, and document management. |
| **Orchestration** | 9 | Advanced workflow engines (Argo, ZenML) and data pipeline orchestrators. |

## Top 10 Most-Connected Tools
Based on internal links in their 'Related tools / concepts' sections (June 2026):

| Tool | Related Links |
| :--- | :--- |
| Gemini | 17 |
| OpenAI | 15 |
| Portracker | 15 |
| rclone Automation | 14 |
| Google Lyria | 13 |
| AI Templates | 13 |
| Docker | 12 |
| ansigpt | 12 |
| qBittorrent Automation | 12 |
| Element | 12 |

## Underdeveloped Categories
Categories identified as areas where the repository is actively seeking expansion (fewer than 10 docs):
- Intake & Storage (9)
- Orchestration (9)
- Reference Implementations (3)
- Architecture (1)
- Playbooks (1)

## What's New This Month (June 2026)
Key additions and major version upgrades from the June execution phases:
- **Agents:** ZenML Agent Skills, Letta v1.5.x, Phidata improvements.
- **Orchestration:** Argo Workflows v4.0.6 (Artifact Plugins), ZenML v0.95.1 (MCP 3.0).
- **Enterprise AI:** Elasticsearch v9.4.2 (ES|QL subqueries), Curiosity Workspace (LLM dashboards).
- **Benchmarking:** SharpAI Security Benchmark (Agentic resilience evaluation).
- **Development & Ops:** Claude Code (v17.4.x+), Windsurf (Agentic IDE).

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
- [Growth Metrics Snapshot (June 2021)](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/growth-metrics.json)
- [ZenML v0.95 Release: Agent Skills](https://www.zenml.io/blog)
- [Elasticsearch 9.4 Release: ES|QL Subqueries](https://www.elastic.co/blog)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
