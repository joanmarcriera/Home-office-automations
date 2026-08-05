# DeerFlow

## What it is
DeerFlow is an enterprise-grade open-source agentic deep-research workflow orchestrator developed by ByteDance. By late December 2026, it is recognized as a premier reference architecture for building high-autonomy research and information-synthesis agents that leverage frontier models including **Claude 5.1**, **GPT-5.5**, and **Gemma 3**.

## What problem it solves
It streamlines the creation of highly complex, multi-step deep-search and document-synthesis pipelines. Instead of stitching together fragile web scraper and search API scripts, DeerFlow provides a structured, containerized, and fault-tolerant framework for recursive browsing, semantic query expansion, information extraction, and citation-accurate report synthesis. When aligned with the **MCP 3.1 Task Protocol**, it ensures that long-running evaluation and research tasks execute with predictable schemas and high fidelity.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — Sits as a specialized, long-running research agent orchestration engine, interfacing between standard tool catalogs and high-level analytical dashboards while utilizing [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) for tool retrieval.

## Typical use cases
- **Competitive Intelligence**: Auto-monitoring and generating extensive landscaping reports on competitor features, pricing, and personnel movements.
- **Academic and Patent Synthesis**: Aggregating, deduplicating, and extracting core methodology details from thousands of research papers or filings.
- **Enterprise Sales Enablement**: Automating target accounts profiling, identifying buying signals, and mapping executive relationships.
- **Compliance & Regulatory Auditing**: Scanning global multi-jurisdictional regulatory updates to highlight relevant legal impacts for specific products.

## Strengths
- **Native Task Protocol Support**: Aligned with the **MCP 3.1 Task Protocol** for standardized research session management and multi-node coordination.
- **Rich Citation Validation**: Advanced heuristics to map extracted facts back to verified source URLs and page anchors, reducing hallucinations.
- **Multi-Model Orchestration**: Intelligently distributes tasks—using lightweight local [Gemma 3](../ai_knowledge/local_llms.md) for simple retrieval/filtering, and [Claude 5.1](anthropic-agent-skills.md) for complex structural synthesis.
- **Self-Correction Logic**: Automated recovery from rate-limits, Captchas, or scrapers getting blocked.

## Limitations
- **High Resource Footprint**: Running deep research loops often entails heavy token consumption, requiring active token-budget controls and redis caching.
- **Setup Complexity**: Requires robust sandboxing (such as Docker) to safely execute dynamic page browsing and scraping code.
- **API Dependencies**: Relying heavily on third-party search indexes (e.g., [Tavily](../providers/tavily.md)) means changes in downstream API behaviors can disrupt workflows.

## When to use it
- When building customized, multi-step research assistants that must generate evidence-based, citation-linked reports.
- For integrating structured, self-hostable research capabilities directly into corporate intranet portals.
- When executing complex benchmarking or automated analytical jobs matching **MCP 3.1** constraints.

## When not to use it
- For quick, single-shot search responses where a simple API request to [Tavily](../providers/tavily.md) is sufficient.
- In low-latency applications where responses must be returned to the user in sub-second intervals.

## Getting started

### Installation
DeerFlow is highly recommended to run in containerized environments (Docker) to isolate web scrapers and browsers:
```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make config
make docker-init
make docker-start
```

### Configuration
Update the generated `config.yaml` to specify your frontier API endpoints and preferred model configurations:
```yaml
research_engine:
  primary_model: "claude-5.1-sonnet"
  fallback_model: "gemma-3-27b"
  search_provider: "tavily"
  max_depth: 3
  mcp_endpoint: "http://localhost:8000/v1/task-protocol"
```

## CLI examples
```bash
# Generate the default configuration schema
make config

# Spin up the DeerFlow orchestration dashboard locally
make dev

# Run a dedicated deep-research task from the terminal
python3 -m deerflow.harness run --task "Decentralized database landscapes in 2026" --model "claude-5.1-sonnet"
```

## API examples

### Submitting and Validating Research Results using Pydantic v2
This Python snippet demonstrates how to submit research prompts to a DeerFlow engine and structurally validate the returned citations and summaries using strict Pydantic v2 schemas.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
import requests

# 1. Define strict Pydantic v2 schemas for verification
class FactCitation(BaseModel):
    source_url: HttpUrl = Field(..., description="Verified citation URL")
    title: str = Field(..., min_length=2)
    extracted_snippet: str = Field(..., description="Verbatim text extracted from page")

class SynthesizedReport(BaseModel):
    task_id: str = Field(..., pattern=r"^task_[a-zA-Z0-9]+$")
    topic: str
    executive_summary: str = Field(..., min_length=50)
    findings: List[str] = Field(..., min_length=1)
    citations: List[FactCitation] = Field(default_factory=list)
    confidence_rating: float = Field(..., ge=0.0, le=1.0)

# 2. Function to fetch and validate the completed report
def retrieve_completed_research(task_id: str) -> Optional[SynthesizedReport]:
    endpoint = f"http://localhost:2026/api/v1/tasks/{task_id}/report"
    try:
        response = requests.get(endpoint, timeout=15)
        response.raise_for_status()
        raw_data = response.json()

        # Perform strict Pydantic v2 validation
        validated_report = SynthesizedReport.model_validate(raw_data)
        return validated_report
    except Exception as e:
        print(f"Validation failed for report {task_id}: {e}")
        return None

if __name__ == "__main__":
    report = retrieve_completed_research("task_abc123")
    if report:
        print(f"Successfully validated report on: {report.topic}")
        print(f"Confidence score: {report.confidence_rating * 100}%")
```

## Related tools / concepts
- [Tavily](../providers/tavily.md) - Standard search API partner.
- [Browser Use](../automation_orchestration/browser-use.md) - Native interactive web interactions.
- [mem0](mem0.md) - Persistent agent memory layer.
- [Symphony](symphony.md) - Autonomous implementation fleets.
- [LangGraph](../frameworks/langgraph.md) - State-machine orchestrator.
- [Aider](../development_ops/aider.md) - Git-native programming assistant.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) - Standard tool coordination protocol.
- [Gemma 3](../ai_knowledge/local_llms.md) - Local-first reasoning model.
- [Anthropic Agent Skills](anthropic-agent-skills.md) - Skill definitions.
- [Perplexity Agent API](perplexity-agent-api.md) - Search API alternative.

## Sources / References
- [DeerFlow GitHub Repository](https://github.com/bytedance/deer-flow)
- [ByteDance DeerFlow 2.0 Architectural Whitepaper (Apidog)](https://apidog.com/blog/deer-flow-guide-2026/)
- [Anthropic: Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contribution Metadata
- Last reviewed: 2026-12-05
- Confidence: high
