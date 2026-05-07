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

## When to use it
- **Exhaustive Research**: When you need to gather information from dozens of sources simultaneously and summarize them into a single report.
- **Fact-Checking**: To verify information against current web data and receive a cited bibliography.
- **Automated Summarization**: When you need to create comprehensive, long-form reports on complex topics without manual browsing.

## When not to use it
- **Real-Time Fact Retrieval**: For single-shot questions (e.g., "What is the capital of France?"), standard RAG or search tools are faster and cheaper.
- **Creative Writing**: It is optimized for factual synthesis, not creative or conversational tasks.
- **Strict Latency Limits**: Because it performs multi-source scraping and analysis, reports can take minutes to generate.

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
Run a simple research task using the Python library to generate a report.

## CLI examples
```bash
# Run a quick research report on a topic
python -m gpt_researcher.cli "What is the future of solid-state batteries?" --report_type research_report

# Generate a detailed, in-depth report (takes longer)
python -m gpt_researcher.cli "Impact of AI on software engineering 2026" --report_type detailed_report --tone analytical

# Conduct research with a specific source domain filter
python -m gpt_researcher.cli "Latest SpaceX launches" --report_type research_report --query_domains spacex.com,nasa.gov
```

## API examples
```python
from gpt_researcher import GPTResearcher
import asyncio

async def main():
    # 1. Initialize the researcher
    researcher = GPTResearcher(query="Future of home-office automation 2026", report_type="research_report")

    # 2. Conduct research
    await researcher.conduct_research()

    # 3. Write the final report
    report = await researcher.write_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
```

## Strengths
- **High Recall**: Scrapes dozens of sources per task, far exceeding standard "search" tools.
- **Citation-First**: Every report includes a comprehensive bibliography of the sources used.
- **Customizable**: Allows defining specific "research tasks" and report formats (PDF, Markdown, etc.).

## Limitations
- **Cost**: Scraping and synthesizing many sources can consume significant LLM tokens.
- **Speed**: A thorough research task can take several minutes to complete.
- **Quality**: Dependent on the quality of search results and the LLM used for synthesis.

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [Perplexity Agent API](perplexity-agent-api.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Open Agents](open-agents.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)

## Sources / references
- [GPT Researcher GitHub](https://github.com/assafelovic/gpt-researcher)
- [Official Documentation](https://docs.gptr.dev/)

## Contribution Metadata
- Last reviewed: 2026-05-29
- Confidence: high
