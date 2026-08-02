# Landscape Overview

## What it is
The Landscape Overview is a high-level mapping and statistical summary of the entire AI tool and service ecosystem documented in this repository. It provides a bird's-eye view of the catalogue, showing current metrics, connectivity, and recent additions. As of **November 2026**, it reflects the state of a highly mature, multi-agent KnowledgeOps repository.

## What problem it solves
Navigating hundreds of specialized tools and services can be overwhelming. This overview provides structure, category-based discovery, and growth metrics to help users understand the "big picture" of the repository's contents and the broader AI landscape. It helps identify mature segments and areas ripe for expansion.

## Where it fits in the stack
**Knowledge Base / Ecosystem Map**. It sits at the top of the Knowledge Base layer of the Multi-Agent KnowledgeOps framework, acting as the primary entry point for understanding the breadth and depth of documented resources.

## Typical use cases
- **Discovery**: Finding new tools within a specific category (e.g., "Agents" or "Infrastructure") that fit a specific technical requirement.
- **Triage**: Identifying underdeveloped areas where the repository is actively seeking contributions or technical audits.
- **Trend Analysis**: Tracking the growth and shifting focus of the AI ecosystem over time, such as the rise of Agent Skills and FastMCP 3.1 servers.
- **Onboarding**: Providing a comprehensive map for new agents or human contributors to understand the repository's scope.

## Strengths
- **Data-Driven**: Grounded in repository metadata and growth metrics from `data/growth-metrics.json`.
- **Structural Clarity**: Organizes complex information into distinct categories for easy navigation.
- **Graph Insight**: Highlights the most connected and influential tools in the knowledge base, indicating their importance in the stack.
- **November 2026 Context**: Reflects the transition toward autonomous "Software Factories" and agentic orchestration with FastMCP 3.1 standards.

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
- **Last Generated:** 2026-11-15
- **Total Docs Documented:** 452 (Steady growth from 446 in late July)

## Category Breakdown
Current tool count and focus per category, verified against `all_tools.json` and `growth-metrics.json`:

| Category | Count | Summary |
| :--- | :--- | :--- |
| **AI Assistants & Knowledge (ai_knowledge)** | 81 | General-purpose chat interfaces, RAG platforms, and local knowledge bases. |
| **Development & Ops (development_ops)** | 59 | Coding assistants, IDEs, and agentic development tools (e.g., Claude Code, Cursor). |
| **Services** | 53 | Self-hosted AI-related services and utilities (e.g., Paperless-ngx, Immich). |
| **Benchmarking (benchmarking)** | 38 | Evaluation frameworks, security benchmarks (SharpAI), and performance tools. |
| **Process & Understanding (process_understanding)** | 32 | Data extraction, OCR, telemetry, and document processing (Docling). |
| **Automation & Orchestration (automation_orchestration)** | 30 | Workflow automation, tool integration servers, and MCP implementations. |
| **Infrastructure (infrastructure)** | 28 | Model serving (vLLM), inference engines (Ollama), and vector databases. |
| **Agents (agents)** | 27 | Multi-agent orchestration frameworks (Letta, Phidata, CrewAI). |
| **Providers (providers)** | 27 | LLM API providers and model marketplaces (Anthropic, DeepSeek). |
| **Frameworks (frameworks)** | 25 | Development libraries for building AI-powered applications (AG2, Mastra). |
| **Calendar & Tasks (calendar_tasks)** | 21 | Scheduling and task management integrations (Sunsama, Amie). |
| **Enterprise AI (enterprise)** | 12 | Enterprise-grade AI search and productivity suites (Elastic, Curiosity). |
| **Intake & Storage (intake_storage)** | 10 | Data collection, self-hosted storage, and document management. |
| **Orchestration (orchestration)** | 9 | Advanced workflow engines (Argo, ZenML) and data pipeline orchestrators. |

## Top 10 Most-Connected Tools
Based on internal links in their 'Related tools / concepts' sections (November 2026):

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

## What's New This Month (November 2026)
Significant updates and new additions from the November execution phases:
- **Benchmarking:** Fully audited GPQA, HumanEval, MMLU, and specialized LLM benchmarks.
- **Development & Ops:** Standardized setup and configuration guides for Claude Code, Aider, and Windsurf.
- **Model Context Protocol:** Universal adoption of FastMCP 3.1 with standardized Python/TypeScript API client schemas.
- **Frontier Models:** Native integration of Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, and Gemma 3 features across all active modules.

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

### Pydantic v2 Category Metrics Validation
Using **Pydantic v2** to programmatically validate growth snapshot structures, category document counts, and delta calculations:

```python
from pydantic import BaseModel, Field
from typing import Dict

class CategoryMetric(BaseModel):
    """Pydantic model validating category tool counts inside catalog metrics."""
    category_name: str = Field(..., description="E.g., ai_knowledge, development_ops")
    document_count: int = Field(..., ge=0, description="Total number of files in category")

class GrowthMetricsSnapshot(BaseModel):
    """Pydantic model for overall repository growth metrics snapshot validation."""
    snapshot_date: str = Field(..., description="Snapshot generation date YYYY-MM-DD")
    total_docs: int = Field(..., ge=1, description="Aggregated file count")
    tool_docs: int = Field(..., ge=1, description="Number of tool pages")
    service_docs: int = Field(..., ge=1, description="Number of service pages")
    by_category: Dict[str, int] = Field(..., description="Map of category names to page counts")

# Sample validation check
snapshot_data = {
    "snapshot_date": "2026-11-15",
    "total_docs": 452,
    "tool_docs": 399,
    "service_docs": 53,
    "by_category": {
        "agents": 27,
        "ai_knowledge": 81,
        "development_ops": 59,
        "benchmarking": 38
    }
}
validated_snapshot = GrowthMetricsSnapshot(**snapshot_data)
print(f"Validated snapshot for {validated_snapshot.snapshot_date} with {validated_snapshot.total_docs} total docs.")
```

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
- [Growth Metrics Snapshot](https://github.com/joanmarcriera/Home-office-automations/blob/main/data/growth-metrics.json)
- [MCP 3.1 Standard Specification](https://modelcontextprotocol.io)
- [Gemma 3 Release Notes](https://blog.google/technology/ai/google-gemma-3/)

## Contribution Metadata
- Last reviewed: 2026-11-15
- Confidence: high
