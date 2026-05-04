# GPT Researcher

## What it is
GPT Researcher is an autonomous agent designed for comprehensive online research on any given topic. It plans the research, browses the web, and synthesizes a final report with citations. It uses a "master-agent" and "research-agent" pattern to break down complex queries.

## What problem it solves
It automates the time-consuming process of manual research, gathering information from multiple sources and producing high-quality, grounded summaries. It specifically addresses LLM hallucinations by grounding every claim in a retrieved web source.

## Where it fits in the stack
**Category**: Agent / Research Automation

## The Research Process
GPT Researcher follows a structured 3-step autonomous workflow:
1. **Plan**: Generates a set of research questions that form an objective plan for the topic.
2. **Research**: For each question, it triggers a research agent to scrape 20+ web sources for relevant information.
3. **Report**: Aggregates all findings, filters out duplicates, and synthesizes a final Markdown report with full citations.

## Typical use cases
- **Market Research**: Analyzing industry trends and competitor offerings.
- **Technical Deep Dives**: Researching new frameworks or hardware specifications.
- **Academic/Legal Preparation**: Gathering sources and summaries for specific inquiries.
- **Daily Intelligence**: Generating briefings on evolving news topics.

## Strengths
- **High Recall**: Scrapes dozens of sources per task, far exceeding standard "search" tools.
- **Citation-First**: Every report includes a comprehensive bibliography of the sources used.
- **Customizable**: Allows defining specific "research tasks" and report formats (PDF, Markdown, etc.).

## Limitations
- **Cost**: Scraping and synthesizing many sources can consume significant LLM tokens.
- **Speed**: A thorough research task can take several minutes to complete.
- **Quality**: Dependent on the quality of search results and the LLM used for synthesis (best with GPT-4o or Claude 3.5 Sonnet).

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

### CLI Example
```bash
# Run a research task directly from the terminal
python -m gpt_researcher.cli --query "What are the latest breakthroughs in solid-state batteries?" --report_type research_report
```

### Python API Usage
```python
from gpt_researcher import GPTResearcher
import asyncio

async def main():
    query = "Future of home-office automation 2026"
    researcher = GPTResearcher(query=query, report_type="research_report")

    # Conduct research and generate report
    await researcher.conduct_research()
    report = await researcher.write_report()

    print(report)

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts

- [Tavily](../providers/tavily.md)
- [Perplexity Agent API](perplexity-agent-api.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Open Agents](open-agents.md)

## Sources / references
- [GPT Researcher GitHub](https://github.com/assafelovic/gpt-researcher)
- [Autonomous Research for LLMs](https://gpt-researcher.com/docs/)

## Contribution Metadata
- Last reviewed: 2026-05-16
- Confidence: high
