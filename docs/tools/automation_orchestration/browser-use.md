# Browser Use

## What it is
Browser Use is an open-source Python framework designed to enable LLMs to interact with real web browsers. It provides a high-level API for agents to perform tasks like form-filling, navigating complex UI flows, and extracting structured data. As of June 2026, Browser Use is a primary tool for building "Computer Use" capabilities into agents, with native support for the **Model Context Protocol (MCP)** and optimized integration for **Claude 4.8 Opus** and **GPT-5.5**.

## What problem it solves
It bridges the gap between static scraping and manual browser automation. Browser Use allows agents to "see" and "interact" with the web just like a human, handling dynamic, JavaScript-heavy sites that traditional scrapers (like Beautiful Soup) cannot. By using LLMs for reasoning, it avoids the fragility of hard-coded CSS/XPath selectors.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation. It acts as the execution layer for browser-based agents, typically sitting between a framework like LangGraph and a browser driver like Playwright.

## Typical use cases
- **Multi-Step Workflow Automation**: Automating tasks on web apps without APIs (e.g., "Log into my insurance portal and download all claims from May").
- **Agentic Data Extraction**: Gathering structured data from complex, authenticated, or paginated websites.
- **Enterprise Ops**: Bridging data between siloed web-based legacy systems.
- **Interactive Research**: Allowing an agent to browse, compare products, and synthesize findings into a report.

## Strengths
- **Native MCP Support**: Can be deployed as an MCP server, allowing any MCP-compliant client (like Claude Desktop) to use it as a tool.
- **Vision-First Reasoning**: Optimized for vision-capable models to improve navigation accuracy and spatial awareness.
- **Highly Extensible**: Easy to define custom actions and integrate with existing Python-based agent stacks.
- **Robust Community**: Rapidly growing ecosystem with extensive middleware for handling common browser hurdles (CAPTCHAs, cookie banners).

## Limitations
- **High Resource Consumption**: Running a full browser (Chromium) is significantly more resource-intensive than HTTP-based requests.
- **Latency**: The overhead of browser rendering plus LLM reasoning makes it unsuitable for high-frequency or real-time tasks.
- **Inference Cost**: Heavy use of vision and DOM-reasoning can lead to significant token consumption.

## When to use it
- When an application lacks a public API but requires automation.
- For complex, stateful web interactions that require human-like reasoning.
- When building agents that need to use the web as their primary knowledge or action source.

## When not to use it
- When a stable, documented REST or GraphQL API is available.
- For simple, high-speed data scraping where [Crawl4AI](../process_understanding/crawl4ai.md) or standard Playwright would be faster.
- In low-latency environments where every millisecond counts.

## Getting started

### Installation
```bash
pip install browser-use
```

### Basic Usage
```python
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

async def main():
    agent = Agent(
        task="Go to Hacker News and find the top story about Agentic Workflows.",
        llm=ChatAnthropic(model="claude-3-5-sonnet-20240620"), # Or Claude 4.8
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())
```

## CLI examples
```bash
# Run a browser-use task directly from the CLI
python -m browser_use "Search for the latest Llama 4 benchmarks on X"

# Launch the interactive Web UI for task monitoring and creation
python -m browser_use --ui

# List available agent configurations and installed plugins
python -m browser_use --list-agents
```

## API examples
```python
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI

# Advanced configuration with headful mode for debugging
browser = Browser(config=BrowserConfig(headless=False))

agent = Agent(
    task="Navigate to my GitHub dashboard and summarize recent notifications",
    llm=ChatOpenAI(model="gpt-4o"), # Or GPT-5.5
    browser=browser
)

async def run_task():
    history = await agent.run()
    print(f"Task completed in {len(history.steps)} steps.")
    await browser.close()
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free (Self-hosted)
- **Self-hostable**: Yes

## Related tools / concepts
- [Stagehand](stagehand.md) — The TypeScript equivalent for agentic browsing.
- [Skyvern](skyvern.md) — Visual-reasoning based automation platform.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Optimized scraper for LLM ingestion.
- [Playwright](../development_ops/playwright.md) — The underlying automation engine.
- [n8n](../../services/n8n.md) — For orchestrating Browser Use within wider workflows.
- [mem0](../agents/mem0.md) — To give browser agents persistent memory across sessions.
- [Model Context Protocol](mcp.md) — For standardizing the tool interface.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for browser-based agents.

## Sources / References
- [Browser Use GitHub](https://github.com/browser-use/browser-use)
- [Official Documentation](https://docs.browser-use.ai/)
- [MCP Server Implementation](https://github.com/browser-use/browser-use-mcp)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
