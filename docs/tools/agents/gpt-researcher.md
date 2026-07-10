# GPT Researcher

## What it is
GPT Researcher (v4.0+, July 2026) is an autonomous agent designed for comprehensive online research on any given topic. It plans the research, browses the web, and synthesizes a final report with deep citations. It uses a "master-agent" and "research-agent" pattern to break down complex queries into manageable sub-tasks, now supporting multi-modal search and the **MCP 3.0 Task Protocol**.

## What problem it solves
It automates the time-consuming process of manual research, gathering information from multiple sources and producing high-quality, grounded summaries. It specifically addresses LLM hallucinations by grounding every claim in a retrieved web source (via Tavily/SearXNG) and providing a verifiable bibliography.

## Where it fits in the stack
**Category**: Agent / Research Automation. It serves as a specialized "Knowledge Acquisition" layer in an agentic stack, feeding structured data and reports into other agents or long-term memory stores like [Letta](letta.md).

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
- **Agentic Tooling**: Native support for **MCP 3.0**, allowing it to be used as a tool by other agents like [Claude 4.8](../ai_knowledge/claude.md) or [Gemma 3](../ai_knowledge/local_llms.md).

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
pip install gpt-researcher
```

### Environment Setup
```bash
export OPENAI_API_KEY='your-key'
export TAVILY_API_KEY='your-key'
```

### Basic Usage
Run a research task via the Python API to generate a markdown report.

## CLI examples
```bash
# Run a quick research report on a topic
python -m gpt_researcher.cli "Future of solid-state batteries in 2027" --report_type research_report

# Generate a detailed, in-depth report with a specific tone
python -m gpt_researcher.cli "Impact of MCP 3.0 on agentic ecosystems" --report_type detailed_report --tone analytical

# Conduct research filtered by specific domains
python -m gpt_researcher.cli "Latest SpaceX launches" --report_type research_report --query_domains spacex.com,nasa.gov
```

## API examples
```python
from gpt_researcher import GPTResearcher
import asyncio

async def main():
    # 1. Initialize the researcher with a specific query
    researcher = GPTResearcher(
        query="Evolution of agentic frameworks in July 2026",
        report_type="research_report",
        tone="technical"
    )

    # 2. Conduct research across multiple sources
    await researcher.conduct_research()

    # 3. Write and save the final report
    report = await researcher.write_report()
    with open("report.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [Perplexity Agent API](perplexity-agent-api.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [SearXNG Automation](../../services/searXNG-automation.md)
- [Letta](letta.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Claude 4.8](../ai_knowledge/claude.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md)

## Sources / references
- [GPT Researcher GitHub Repository](https://github.com/assafelovic/gpt-researcher)
- [GPT Researcher Official Documentation](https://docs.gptr.dev/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
