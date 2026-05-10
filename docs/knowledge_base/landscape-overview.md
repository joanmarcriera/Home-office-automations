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
- **Last Generated:** 2026-05-01
- **Total Tools Documented:** 371 (Significant growth from 211 in the April report)

## Category Breakdown

Current tool count and focus per category, verified against `all_tools.json`:

| Category | Count | Summary |
| :--- | :--- | :--- |
| **AI Assistants & Knowledge** | 67 | General-purpose chat interfaces, RAG platforms, and knowledge bases. |
| **Development & Ops** | 57 | Coding assistants, IDEs, and agentic development tools. |
| **Process & Understanding** | 36 | Data extraction, OCR, and document processing. |
| **Benchmarking** | 31 | Evaluation frameworks and performance measurement tools. |
| **Automation & Orchestration** | 29 | Workflow automation and tool integration servers. |
| **Intake & Storage** | 25 | Data collection, self-hosted storage, and document management. |
| **Agents** | 25 | Multi-agent orchestration frameworks. |
| **Frameworks** | 21 | Development libraries for building AI-powered applications. |
| **Providers** | 20 | LLM API providers and model marketplaces. |
| **Infrastructure** | 16 | Model serving, inference engines, and fine-tuning platforms. |
| **Calendar & Tasks** | 13 | Scheduling and task management integrations. |
| **Enterprise AI** | 9 | Enterprise-grade AI search and productivity suites. |
| **Patterns** | 5 | Standardized approaches and architectural patterns. |
| **Media & Entertainment** | 5 | Self-hosted media servers and creative content tools. |
| **Reference Implementations** | 3 | Skeleton code and reference designs for AI patterns. |
| **Knowledge Base** | 3 | Deep-dive research and comparison articles. |
| **Creative & Communication** | 3 | Diagramming and secure messaging services. |
| **Playbooks** | 1 | Step-by-step guides for specific AI implementations. |
| **Architecture** | 1 | High-level system design and component maps. |
| **AI & Knowledge** | 1 | Legacy or specialized AI knowledge documentation. |

## Top 10 Most-Connected Tools
Based on the number of internal links in their 'Related tools / concepts' sections.

| Tool | Related Links |
| :--- | :--- |
| OpenClaw | 11 |
| Claude Code | 10 |
| OpenAI | 9 |
| Fine-tuning Open Models | 8 |
| Supabase | 8 |
| n8n | 7 |
| OpenHands | 7 |
| Runway ML | 7 |
| TeamOut | 7 |
| ansigpt | 6 |

## Underdeveloped Categories
Categories with fewer than 8 docs are identified as areas where the repository is actively expanding:
- Patterns (5)
- Media & Entertainment (5)
- Reference Implementations (3)
- Knowledge Base (3)
- Creative & Communication (3)
- Playbooks (1)
- Architecture (1)
- AI & Knowledge (1)

## What's New This Month
Key additions and integrations from the Batch 2 (Agent Frameworks), Batch 3 (SDKs), and Batch 6 (Storage) execution phases:
- **Agent Frameworks:** AG2, Langflow, Mastra, Rivet, Superinterface, Temporal.
- **SDKs & Tooling:** LlamaIndex.TS, Vercel AI SDK, Instructor, Google ADK, Firebase Genkit, Portkey.
- **Storage & Observability:** ClickHouse, Snowflake, S3 Storage, W&B Weave, OpenTelemetry Collector, Webhook.
- **Enterprise Productivity:** Dashworks, Guru, Curiosity, Coveo, Elastic, AmpCode.
- **Benchmarking:** Humanity's Last Exam (HLE), SWE-bench Pro, SharpAI Security.

## Critical Risks & Future Outlook
The "Humanity's Last Gasp" analysis (April 2026) suggests that the current era of "AI assisting humans to work harder" may be a transient state (the "Turkey Problem"). As benchmarks like SWE-Bench Pro become saturated and AGI superclusters approach, the "Software Factory" pattern and "Prompt Requests" will likely redefine the role of the engineer.

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
- Last reviewed: 2026-05-10
- Confidence: high
