# GPT Researcher

## What it is
GPT Researcher (v4.5+, early January 2027) is an autonomous agent designed for comprehensive online research on any given topic. It plans the research, browses the web, and synthesizes a final report with deep citations. It uses a "master-agent" and "research-agent" pattern to break down complex queries into manageable sub-tasks, supporting multi-modal search and the **FastMCP 3.1 Task Protocol**.

```
+-----------------------------------------------------------------------------------+
|                        GPT RESEARCHER SYSTEM ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+

  +-------------------------------------------------------------------------------+ |
  |                         MASTER RESEARCH ORCHESTRATOR                          | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | Query Decomposer &  |   | Multi-Agent Task    |   | Context Window      | | |
  |   | Sub-Goal Planner    |   | Dispatcher          |   | Aggregator          | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                         PARALLEL RESEARCH AGENT POOL                          | |
  |                                                                               | |
  |   +------------------+   +------------------+   +------------------+          | |
  |   | Agent 1: Search  |   | Agent 2: Scraper |   | Agent 3: RAG &   |          | |
  |   | (Tavily/SearXNG) |   | (Crawl4AI Nodes) |   | Source Evaluator |          | |
  |   +------------------+   +------------------+   +------------------+          | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                       FAST MCP 3.1 & PYDANTIC VALIDATION                      | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | Source Metadata     |   | Link Verification & |   | FastMCP 3.1 Tool    | | |
  |   | Pydantic v2 Schema  |   | Anti-Hallucination  |   | Protocol Exposer    | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                     REPORT SYNTHESIS & DRAFTING ENGINE                        | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | Markdown / PDF      |   | Citation & Source   |   | Multi-Modal Media   | | |
  |   | Publisher           |   | Bibliography Cross  |   | Attachment Injector | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
```

## What problem it solves
It automates the time-consuming process of manual research, gathering information from multiple sources and producing high-quality, grounded summaries. It specifically addresses LLM hallucinations by grounding every claim in a retrieved web source (via Tavily/SearXNG) and providing a verifiable bibliography.

- **Manual Research Overhead**: Eliminates hours spent opening dozens of browser tabs, extracting text, and cross-checking references manually.
- **Hallucination in LLM Generation**: Solves standard LLM hallucination issues by enforcing strict source attribution and grounding every statement in retrieved web context.
- **Single-Source Bias**: Avoids shallow or biased outputs by querying multiple web search indexes and scraping diverse domain sources simultaneously.

## Where it fits in the stack
**Category**: Agent / Research Automation. It serves as a specialized "Knowledge Acquisition" layer in an agentic stack, feeding structured data and reports into other agents or long-term memory stores like [Letta](letta.md).

```
+-----------------------------------------------------------------------------------+
|                            STACK INTEGRATION MATRIX                               |
+-----------------------------------------------------------------------------------+
  Data Acquisition       : Tavily Search API, SearXNG Local, Crawl4AI Web Scraper
  Validation Layer       : Pydantic v2 Citation & Metadata Sanitizers
  Tool Export Protocol   : FastMCP 3.1 Task Protocol & REST API Gateway
  Downstream Consumers   : Letta Memory, Claude 5.6 Workspace, Ralph-Loop Agents
+-----------------------------------------------------------------------------------+
```

## Key Features & Operational Capabilities

### 1. Master-Subagent Decomposition Architecture
When given a research query (e.g., "Impact of FastMCP 3.1 on AI Agent Latency"), the master agent creates a research plan with 3-7 sub-queries. Individual research sub-agents are spawned asynchronously to execute these queries against search APIs and web scrapers in parallel.

### 2. Multi-Tier Scraping and RAG Pipeline
Scraped page contents are processed through an inline vector store (or local embedding model) to rank relevant chunks before passing them to the final report generation prompt, minimizing context dilution.

```
+-----------------------------------------------------------------------------------+
|                        PARALLEL AGENT RESEARCH PIPELINE                           |
+-----------------------------------------------------------------------------------+
  User Query --> Master Planner --> [ Sub-Query 1, Sub-Query 2, Sub-Query 3 ]
                                          |             |            |
                                          v             v            v
                                    Agent Alpha    Agent Beta   Agent Gamma
                                          |             |            |
                                          +-------------+------------+
                                                        |
                                                        v
                                         Vector RAG Chunk Extraction
                                                        |
                                                        v
                                          Synthesized Citation Report
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Market Research**: Analyzing industry trends, competitor offerings, and financial reports.
- **Technical Deep Dives**: Researching new software frameworks, hardware specifications, or architectural patterns.
- **Academic/Legal Preparation**: Gathering sources, summaries, and case law for specific inquiries.
- **Daily Intelligence**: Generating automated briefings on evolving news topics or specific market sectors.
- **Agentic Knowledge Base Population**: Automatically generating documentation for new tools identified during a crawl.

## Strengths
- **High Recall**: Scrapes dozens of sources per task, far exceeding standard "search" tools or single-shot RAG.
- **Citation-First**: Every report includes a comprehensive bibliography with direct links to sources.
- **Customizable**: Allows defining specific "research tasks", tones, and report formats (PDF, Markdown, JSON).
- **Agentic Tooling**: Native support for **FastMCP 3.1**, allowing it to be used as a tool by other agents like [Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), or [Gemma 4](../ai_knowledge/local_llms.md).

## Limitations
- **Cost**: Scraping and synthesizing many sources can consume significant LLM tokens and API credits (Tavily).
- **Speed**: A thorough research task can take several minutes to complete as it operates asynchronously across many sources.
- **Quality Dependency**: Final report quality is heavily dependent on the quality of the underlying LLM used for synthesis and the search engine results.

## When to use it
- **Exhaustive Research**: When you need to gather information from dozens of sources simultaneously and summarize them into a single coherent report.
- **Fact-Checking**: To verify information against current web data and receive a cited bibliography for verification.
- **Automated Long-Form Synthesis**: When you need to create comprehensive, structured reports on complex topics without manual browsing.

## When not to use it
- **Real-Time Fact Retrieval**: For single-shot questions (e.g., "What is the capital of France?"), standard search tools or basic RAG are faster and cheaper.
- **Creative Writing**: It is optimized for factual synthesis and technical reporting, not creative or conversational tasks.
- **Strict Budget Constraints**: High token usage and search API costs make it expensive for high-volume, low-value tasks.

## Getting started

### Installation
```bash
pip install gpt-researcher pydantic>=2.0.0
```

### Environment Setup
```bash
export OPENAI_API_KEY='your-key'
export TAVILY_API_KEY='your-key'
```

### Basic Usage
Run a research task via the Python API to generate a markdown report.

## Detailed Code Example: Enterprise FastMCP 3.1 Research Server

The following complete Python application demonstrates embedding GPT Researcher inside a FastMCP 3.1 tool server with Pydantic v2 data contract validation and async execution queues.

```python
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator, ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] GPTResearcherServer: %(message)s")
logger = logging.getLogger("GPTResearcherMCP")

# --- Pydantic v2 Schema Definitions ---

class CitationSource(BaseModel):
    title: str = Field(..., description="Title of scraped website or document")
    url: str = Field(..., description="Source URL")
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    snippet: str = Field(..., description="Extracted key information excerpt")

    @field_validator("url")
    @classmethod
    def validate_url_protocol(cls, v: str) -> str:
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(f"URL must begin with http:// or https://, got: {v}")
        return v

class ResearchJobRequest(BaseModel):
    topic: str = Field(..., min_length=5, description="Main topic or query to research")
    report_type: str = Field(default="research_report", description="research_report, detailed_report, or outline")
    tone: str = Field(default="technical", description="Tone of synthesized output")
    max_sources: int = Field(default=10, ge=2, le=50, description="Max source pages to scrape")
    domains_filter: List[str] = Field(default_factory=list, description="Restrict search to specific domains")

class ResearchJobResponse(BaseModel):
    job_id: str = Field(..., description="Unique job execution identifier")
    status: str = Field(..., description="completed, in_progress, or failed")
    topic: str
    markdown_report: str
    sources: List[CitationSource]
    execution_time_seconds: float

# --- FastMCP 3.1 Server Routine ---

class FastMCPResearchService:
    def __init__(self):
        self.active_jobs: Dict[str, ResearchJobResponse] = {}

    async def execute_research_task(self, req: ResearchJobRequest) -> ResearchJobResponse:
        logger.info(f"Starting async research job for topic: '{req.topic}' (Max sources: {req.max_sources})")
        start_time = asyncio.get_event_loop().time()

        # Simulate multi-agent crawling & Tavily search execution
        await asyncio.sleep(1.5)  # Simulating web research delay

        mock_sources = [
            CitationSource(
                title="Model Context Protocol 3.1 Specification",
                url="https://modelcontextprotocol.io/spec/3.1",
                relevance_score=0.96,
                snippet="FastMCP 3.1 introduces optimized binary RPC frames for agent tool distribution."
            ),
            CitationSource(
                title="Autonomous Web Scraping Benchmarks 2027",
                url="https://crawl4ai.com/benchmarks/2027",
                relevance_score=0.91,
                snippet="Parallel DOM extraction reduces per-page context retrieval latency down to 180ms."
            )
        ]

        synthesized_md = (
            f"# Technical Research Report: {req.topic}\n\n"
            f"## Executive Summary\n"
            f"Based on analysis across {len(mock_sources)} primary verified web sources, "
            f"the research confirms high efficiency gains when using FastMCP 3.1 protocols.\n\n"
            f"## Key Findings\n"
            f"- **Protocol Latency**: Sub-20ms agent tool dispatch.\n"
            f"- **Context Precision**: Pydantic v2 schemas prevent invalid LLM argument injection.\n\n"
            f"## Bibliography\n"
            f"1. [{mock_sources[0].title}]({mock_sources[0].url})\n"
            f"2. [{mock_sources[1].title}]({mock_sources[1].url})\n"
        )

        elapsed = round(asyncio.get_event_loop().time() - start_time, 2)
        response = ResearchJobResponse(
            job_id="job_gptr_9941a",
            status="completed",
            topic=req.topic,
            markdown_report=synthesized_md,
            sources=mock_sources,
            execution_time_seconds=elapsed
        )
        self.active_jobs[response.job_id] = response
        logger.info(f"Research job completed in {elapsed}s. Citations: {len(mock_sources)}")
        return response

# --- Runner Function ---

async def main():
    service = FastMCPResearchService()

    raw_payload = {
        "topic": "FastMCP 3.1 performance and Pydantic v2 integration",
        "report_type": "detailed_report",
        "tone": "technical",
        "max_sources": 8,
        "domains_filter": ["modelcontextprotocol.io", "pydantic.dev"]
    }

    try:
        # Validate input via Pydantic v2
        job_request = ResearchJobRequest(**raw_payload)
        report_output = await service.execute_research_task(job_request)

        print("\n=== GENERATED RESEARCH REPORT ===")
        print(report_output.markdown_report)
        print("=== VERIFIED CITATIONS JSON ===")
        print(json.dumps([s.model_dump() for s in report_output.sources], indent=2))

    except ValidationError as e:
        logger.error(f"Payload validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
```bash
# Run a quick research report on a topic
python -m gpt_researcher.cli "Future of solid-state batteries in 2027" --report_type research_report

# Generate a detailed, in-depth report with a specific tone
python -m gpt_researcher.cli "Impact of FastMCP 3.1 on agentic ecosystems" --report_type detailed_report --tone analytical

# Conduct research filtered by specific domains
python -m gpt_researcher.cli "Latest SpaceX launches" --report_type research_report --query_domains spacex.com,nasa.gov
```

## API examples

### Example: Running a Simple Research Session
```python
from gpt_researcher import GPTResearcher
import asyncio

async def run_research():
    researcher = GPTResearcher(
        query="Evolution of agentic frameworks in early 2027",
        report_type="research_report",
        tone="technical"
    )
    await researcher.conduct_research()
    report = await researcher.write_report()
    return report
```

### Example: Programmatic Web Scraping and Citation Validation
In order to guarantee that all scraped data feeds are valid and carry legitimate, parseable URLs and metadata, GPT Researcher workflows utilize **Pydantic v2** validation before compiling report bibliographies.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator

# Define Pydantic v2 schemas for validating scraped sources
class ScrapedCitation(BaseModel):
    title: str = Field(..., min_length=2, description="Title of the source webpage")
    url: HttpUrl = Field(..., description="Fully qualified HTTP/HTTPS url of the source")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Confidence rating of source relevance")
    summary: str = Field(..., description="Extracted relevant summary text")

class ResearchReport(BaseModel):
    topic: str = Field(..., description="Query topic")
    sources: List[ScrapedCitation]
    synthesized_markdown: str = Field(..., min_length=10, description="The main compiled report content")

    @field_validator('sources')
    @classmethod
    def enforce_minimum_citations(cls, citations_list: List[ScrapedCitation]) -> List[ScrapedCitation]:
        # Enforce that a high-quality report must ground its findings in at least 2 citations
        if len(citations_list) < 2:
            raise ValueError("High-quality research reports must include at least two distinct citations.")
        return citations_list

def parse_and_validate_report(raw_data: dict) -> Optional[ResearchReport]:
    try:
        validated_report = ResearchReport.model_validate(raw_data)
        print(f"Report validated successfully for topic: '{validated_report.topic}'")
        print(f"Citations Verified: {len(validated_report.sources)}")
        for i, src in enumerate(validated_report.sources):
            print(f"  [{i+1}] {src.title} -> {src.url}")
        return validated_report
    except Exception as e:
        print(f"Research report validation failed: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initializing GPT Researcher citation validator (Pydantic v2)...")

    # Valid payload containing two distinct citations
    valid_payload = {
        "topic": "FastMCP 3.1 optimization benchmarks",
        "sources": [
            {
                "title": "Model Context Protocol 3.1 Specifications",
                "url": "https://modelcontextprotocol.io/spec/3.1",
                "relevance_score": 0.98,
                "summary": "Introduces high-throughput session protocols and multi-threading parameters."
            },
            {
                "title": "FastMCP benchmarking on local Gemma 4 models",
                "url": "https://huggingface.co/blog/gemma-4-mcp",
                "relevance_score": 0.89,
                "summary": "Demonstrates sub-10ms tool call latency when run locally."
            }
        ],
        "synthesized_markdown": "## Executive Summary\\n\\nFastMCP 3.1 represents a massive leap in low-latency orchestration..."
    }

    parse_and_validate_report(valid_payload)
```

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [Perplexity Agent API](perplexity-agent-api.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [SearXNG Automation](../../services/searXNG-automation.md)
- [Letta](letta.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Gemma 4](../ai_knowledge/local_llms.md)
- [Claude 5.6](../ai_knowledge/claude.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md)

## Sources / references
- [GPT Researcher GitHub Repository](https://github.com/assafelovic/gpt-researcher)
- [GPT Researcher Official Documentation](https://docs.gptr.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
