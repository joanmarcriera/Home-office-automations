# Landscape Overview

## What it is
The Landscape Overview is a high-level mapping and statistical summary of the entire AI tool and service ecosystem documented in this repository. It provides a bird's-eye view of the catalogue, showing current metrics, connectivity, and recent additions. As of **early January 2027**, it reflects the state of a highly mature, multi-agent KnowledgeOps repository.

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
- **Data-Driven**: Grounded in repository metadata and growth metrics from `data/growth-metrics.json` and `data/all_tools.json`.
- **Structural Clarity**: Organizes complex information into distinct categories for easy navigation.
- **Graph Insight**: Highlights the most connected and influential tools in the knowledge base, indicating their importance in the stack.
- **January 2027 Context**: Reflects the transition toward autonomous "Software Factories" and agentic orchestration with FastMCP 3.1 standards, Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.

## Limitations
- **Repository-Scoped**: Reflects current documentation coverage rather than the entire global AI market.
- **Snapshot-Based**: Metrics are updated during technical audits and may lag behind the absolute latest main branch commits.
- **Manual Synthesis**: While metrics are automated, the strategic "What's New" analysis requires agentic synthesis.

## When to use it
- When you are new to the repository and need a comprehensive map of its contents.
- When you are planning a new integration and want to see existing tools and patterns in that space.
- When you want to see the latest "High Engineering" additions to the catalogue (e.g., Kiro Crew, FastMCP 3.1 Task Protocol servers).

## When not to use it
- When you need deep technical setup instructions for a specific tool (refer to its canonical page instead).
- When looking for real-time price comparisons (use the [API Pricing Matrix](api_pricing_free_tiers.md)).
- For fine-grained architectural diagrams (see the [Architecture Component Map](../architecture/component_map.md)).

## Overview
- **Last Generated:** 2027-01-07
- **Total Docs Documented:** 524 (including 471 tool docs and 53 service docs)

## Category Breakdown
Current tool count per category verified against `data/growth-metrics.json` and `data/all_tools.json`:

| Category | Count | Summary |
| :--- | :--- | :--- |
| **AI Assistants & Knowledge (`ai_knowledge`)** | 95 | General-purpose chat interfaces, RAG platforms, and local knowledge bases. |
| **Development & Ops (`development_ops`)** | 63 | Coding assistants, IDEs, agentic development tools, and CLI context servers. |
| **Infrastructure (`infrastructure`)** | 45 | Model serving engines, inference runtimes, vector databases, and compute acceleration. |
| **Benchmarking (`benchmarking`)** | 41 | LLM evaluation frameworks, agentic test suites, and performance benchmark suites. |
| **Process & Understanding (`process_understanding`)** | 40 | Data extraction, OCR, speech recognition, telemetry, and document understanding tools. |
| **Providers (`providers`)** | 36 | Cloud LLM API providers, model marketplaces, and specialized model hosting. |
| **Agents (`agents`)** | 34 | Multi-agent orchestration frameworks, autonomous coding agents, and agentic skills. |
| **Frameworks (`frameworks`)** | 33 | Development libraries and SDKs for building LLM applications and agent pipelines. |
| **Automation & Orchestration (`automation_orchestration`)** | 30 | Workflow automation engines, MCP server implementations, and integration servers. |
| **Calendar & Tasks (`calendar_tasks`)** | 21 | Scheduling tools, task management integrations, and calendar synchronization servers. |
| **Enterprise AI (`enterprise`)** | 14 | Enterprise search engines, identity systems, and enterprise productivity suites. |
| **Intake & Storage (`intake_storage`)** | 10 | Data ingestion tools, self-hosted object storage, and document stores. |
| **Orchestration (`orchestration`)** | 9 | Advanced workflow orchestrators, data pipeline engines, and DAG runners. |

### Categories with Fewer than 8 Docs
None. All 13 active tool categories currently meet or exceed the target threshold of 8 documents, ranging from **9 docs** in `orchestration` to **95 docs** in `ai_knowledge`.

## Top 10 Most-Connected Tools
The top 10 most-connected tools based on the number of outgoing links in their `## Related` sections:

| Tool | Related Links | Canonical Document Path |
| :--- | :--- | :--- |
| **Kestra** | 17 | `docs/tools/orchestration/kestra.md` |
| **ZenML** | 17 | `docs/tools/orchestration/zenml.md` |
| **Hamilton** | 16 | `docs/tools/orchestration/apache-hamilton.md` |
| **Flyte** | 15 | `docs/tools/orchestration/flyte.md` |
| **Apache Airflow** | 15 | `docs/tools/orchestration/apache-airflow.md` |
| **RAGFlow** | 14 | `docs/tools/process_understanding/ragflow.md` |
| **Terminus 2 (Terminal-Bench)** | 14 | `docs/tools/development_ops/terminus-2.md` |
| **Cloud Code** | 14 | `docs/tools/development_ops/cloud_code.md` |
| **Melty** | 14 | `docs/tools/development_ops/melty.md` |
| **Argo Workflows** | 14 | `docs/tools/orchestration/argo-workflows.md` |

## What's New This Month
New tool documentation added under `docs/tools/` in the last 30 days (verified via `git log` intake tracking):

- **Agents (`agents`)**: Integrated **Kiro Crew** (`docs/tools/agents/kiro-crew.md`), **Agency-Agents**, **Anthropic Agent Skills**, **Perplexity Agent API**, and **Symphony (OpenAI)**.
- **Frameworks (`frameworks`)**: Integrated **GraphRAG** (`docs/tools/frameworks/graphrag.md`), **OpenAI Agents SDK**, **Pydantic AI**, **Smolagents**, **Google ADK**, and **Firebase Genkit**.
- **Process & Understanding (`process_understanding`)**: Added **BreezeTTS2** (`docs/tools/process_understanding/breezetts2.md`), **OvisOCR2**, **Docling MCP Server**, **Crawl4AI**, and **Comet Opik**.
- **Infrastructure (`infrastructure`)**: Added **FreeToken** (`docs/tools/infrastructure/freetoken.md`), **ROCm** (`docs/tools/infrastructure/rocm.md`), **Aphrodite Engine**, **ExLlamaV3**, **Diagrid Catalyst**, and **ClawRouter**.
- **Development & Ops (`development_ops`)**: Added **Bionic Shell** (`docs/tools/development_ops/bionic-shell.md`), **Claude Code Router**, **Junie CLI**, **Free Will MCP**, and **Desktop Commander MCP**.
- **Automation & Orchestration (`automation_orchestration`)**: Added **Vault MCP Server**, **Atlassian Jira MCP**, **Stagehand**, **Lightpanda**, and **Open WebUI Computer**.

## Getting started
To contribute to the landscape or audit existing docs:
1. Run `python3 scripts/growth_tracker.py` to update current repository metrics.
2. Use `python3 scripts/find_oldest_issues.py` to locate open intake items.
3. Follow the 13-section 'High Confidence' standard in `docs/standards.md`.

## CLI examples
The repository metrics can be audited via the CLI:

```bash
# Update the growth metrics snapshot
python3 scripts/growth_tracker.py

# Check for unlinked tool mentions to improve connectivity
python3 scripts/cross_link_report.py

# Verify categories with fewer than 8 documents
python3 -c "import json; d=json.load(open('data/growth-metrics.json')); print([k for k,v in d['by_category'].items() if v < 8])"
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
    "snapshot_date": "2027-01-07",
    "total_docs": 524,
    "tool_docs": 471,
    "service_docs": 53,
    "by_category": {
        "agents": 34,
        "ai_knowledge": 95,
        "development_ops": 63,
        "benchmarking": 41
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
- [FastMCP Task Protocol Specification](https://github.com/jupysql/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
