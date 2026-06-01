# Landscape Overview

## What it is
The Landscape Overview is a high-level mapping and statistical summary of the entire AI tool and service ecosystem documented in this repository. It provides a bird's-eye view of the catalogue, showing current metrics, connectivity, and recent additions.

## What problem it solves
Navigating hundreds of specialized tools and services can be overwhelming. This overview provides structure, category-based discovery, and growth metrics to help users understand the "big picture" of the repository's contents and the broader AI landscape.

## Where it fits in the stack
It sits at the top of the **Knowledge Base** layer of the Multi-Agent KnowledgeOps framework, acting as the primary entry point for understanding the breadth and depth of documented resources.

## Typical use cases
- **Discovery**: Finding new tools within a specific category (e.g., "Agents" or "Infrastructure").
- **Triage**: Identifying underdeveloped areas where the repository is actively seeking contributions.
- **Trend Analysis**: Tracking the growth and shifting focus of the AI ecosystem over time.

## Strengths
- **Data-Driven**: Grounded in repository metadata and growth metrics.
- **Structural Clarity**: Organizes complex information into manageable categories.
- **Graph Insight**: Highlights the most connected and influential tools in the knowledge base.

## Limitations
- **Repository-Scoped**: Reflects the current documentation coverage rather than the entire global AI market.
- **Snapshot-Based**: Information is updated monthly and may not reflect real-time changes in frontier models.

## When to use it
- When you are new to the repository and need a map of its contents.
- When you are planning a new integration and want to see existing tools in that space.
- When you want to see the latest "High Engineering" additions to the catalogue.

## When not to use it
- When you need deep technical setup instructions for a specific tool (refer to its canonical page).
- When looking for real-time price comparisons (use the [Access Matrix](ai_tool_access_matrix.md) or [Pricing Matrix](api_pricing_free_tiers.md) instead).

## Overview
- **Last Generated:** 2026-06-01
- **Total Tools Documented:** 423 (Significant growth from 371 in the May report)

## Category Breakdown

Current tool count and focus per category, verified against `all_tools.json`:

| Category | Count | Summary |
| :--- | :--- | :--- |
| **AI Assistants & Knowledge** | 72 | General-purpose chat interfaces, RAG platforms, and knowledge bases. |
| **Development & Ops** | 58 | Coding assistants, IDEs, and agentic development tools. |
| **Process & Understanding** | 42 | Data extraction, OCR, and document processing. |
| **Automation & Orchestration** | 36 | Workflow automation and tool integration servers. |
| **Benchmarking** | 31 | Evaluation frameworks and performance measurement tools. |
| **Intake & Storage** | 26 | Data collection, self-hosted storage, and document management. |
| **Agents** | 25 | Multi-agent orchestration frameworks. |
| **Frameworks** | 24 | Development libraries for building AI-powered applications. |
| **Providers** | 22 | LLM API providers and model marketplaces. |
| **Calendar & Tasks** | 21 | Scheduling and task management integrations. |
| **Infrastructure** | 18 | Model serving, inference engines, and fine-tuning platforms. |
| **Enterprise AI** | 11 | Enterprise-grade AI search and productivity suites. |
| **Orchestration** | 9 | Advanced workflow engines and data pipeline orchestrators. |
| **Media & Entertainment** | 6 | Self-hosted media servers and creative content tools. |
| **Patterns** | 5 | Standardized approaches and architectural patterns. |
| **Knowledge Base** | 4 | Deep-dive research and comparison articles. |
| **Creative & Communication** | 4 | Diagramming and secure messaging services. |
| **Services** | 4 | Specialized automation services for third-party tools. |
| **Reference Implementations** | 3 | Skeleton code and reference designs for AI patterns. |
| **Architecture** | 1 | High-level system design and component maps. |
| **Playbooks** | 1 | Step-by-step guides for specific AI implementations. |

## Top 10 Most-Connected Tools
Based on the number of internal links in their 'Related tools / concepts' sections.

| Tool | Related Links |
| :--- | :--- |
| Gemini | 14 |
| OpenAI | 14 |
| AI Templates | 13 |
| Google Lyria | 13 |
| Portracker | 13 |
| rclone Automation | 13 |
| Docker | 12 |
| MCP Registry | 12 |
| Navidrome | 12 |
| ansigpt | 11 |

## Underdeveloped Categories
Categories with fewer than 8 docs are identified as areas where the repository is actively expanding:
- Media & Entertainment (6)
- Patterns (5)
- Knowledge Base (4)
- Creative & Communication (4)
- Services (4)
- Reference Implementations (3)
- Architecture (1)
- Playbooks (1)

## What's New This Month
Key additions and integrations from the May 2026 execution phases:
- **Agents:** Cline, Letta, mem0, Phidata, Replit Agent, Roo Code.
- **AI Assistants & Knowledge:** DeepSeek R1, Gemini Canvas, LlamaIndex.TS, Qwen3-Coder-Next, Trilium Notes.
- **Automation & Orchestration:** Browser Use, Gumloop, Open Interpreter, Skyvern, Stagehand, Vault MCP Server.
- **Benchmarking:** Humanity's Last Exam (HLE), SWE-bench, SharpAI Security.
- **Development & Ops:** Claude Code, Cursor, Devin, OpenHands, Windsurf.
- **Frameworks:** AG2, Mastra, PydanticAI, Smolagents.
- **Infrastructure:** SGLang, Unsloth, vLLM.
- **Process & Understanding:** ClickHouse, Docling, Snowflake.

## Critical Risks & Future Outlook
The "Humanity's Last Gasp" analysis suggests that the current era of "AI assisting humans to work harder" may be a transient state. As benchmarks like SWE-Bench Pro become saturated and AGI superclusters approach, the "Software Factory" pattern and "Prompt Requests" will likely redefine the role of the engineer.

## Related tools / concepts
- [Architecture Component Map](../architecture/component_map.md)
- [Model Routing Guide](model_routing_guide.md)
- [Model Classes](model_classes.md)
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)
- [AI Builder Index](ai_builder_index.md)
- [Agent Frameworks Learning Map](agent_framework_learning_map.md)
- [AI Tool Access Matrix](ai_tool_access_matrix.md)

## Sources / References
- [Humanity's Last Gasp (Latent Space)](https://www.latent.space/p/ainews-humanitys-last-gasp)
- [All Tools Metadata](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/all_tools.json)
- [Growth Metrics](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/growth-metrics.json)
- [GitHub Repository](https://github.com/joanmarcriera/Home-office-automations)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
