# Browser Use

## What it is
Browser Use is an open-source Python framework designed to enable Large Language Models (LLMs) to interact directly with real web browsers. It provides a high-level API for agents to perform complex multi-step tasks such as form-filling, navigating intricate UI flows, and extracting structured data. As of July 2026, Browser Use serves as a foundational tool for "Computer Use" capabilities, featuring native support for the **Model Context Protocol (MCP) 3.0** and optimized execution patterns for frontier models like **Gemma 3**, **Claude 4.8 Opus**, and **GPT-5.5**.

## What problem it solves
It bridges the gap between static web scraping and manual browser automation. Browser Use allows agents to "see" and "interact" with the web just like a human, effectively handling dynamic, JavaScript-heavy sites that traditional scrapers cannot. By leveraging LLM reasoning for element selection and navigation, it eliminates the fragility associated with hard-coded CSS or XPath selectors, allowing for robust automation across frequently changing interfaces.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation. It acts as the execution layer for browser-based agents, typically sitting between a multi-agent framework like [LangGraph](../frameworks/langgraph.md) or [Agno](../agents/agno.md) and a browser driver like [Playwright](../development_ops/playwright.md).

## Typical use cases
- **Multi-Step Workflow Automation**: Automating complex tasks on web applications without public APIs (e.g., "Log into my insurance portal and download all claims from June 2026").
- **Agentic Data Extraction**: Gathering structured data from authenticated, paginated, or highly dynamic websites for RAG pipelines.
- **Enterprise Legacy Integration**: Bridging data between siloed web-based legacy systems that lack modern integration points.
- **Interactive Visual Research**: Allowing an agent to browse the web, compare products visually, and synthesize findings into high-fidelity reports.

## Strengths
- **MCP 3.0 Task Protocol**: Can be deployed as a standardized MCP server, enabling any MCP-compliant client to utilize browser actions as a standard toolset.
- **Vision-First Reasoning**: Optimized for vision-capable models to improve navigation accuracy through spatial awareness and visual element recognition.
- **Extreme Extensibility**: Easy to define custom actions and integrate with existing Python-based agent stacks using standard middleware.
- **Gemma 3 Integration**: Native support for Gemma 3's visual reasoning capabilities for ultra-low latency browser interaction.

## Limitations
- **High Resource Overhead**: Running a full Chromium instance is significantly more resource-intensive than standard HTTP-based requests or headless scraping.
- **Execution Latency**: The combined overhead of browser rendering and sequential LLM reasoning steps makes it unsuitable for real-time or high-frequency operations.
- **Inference Costs**: Heavy reliance on vision tokens and large DOM snapshots can lead to significant token consumption and associated costs.

## When to use it
- When an application lacks a stable API but requires complex automation or data extraction.
- For stateful web interactions that require human-like reasoning to navigate successfully.
- When building agents that need to use the web as a primary live action or knowledge source.

## When not to use it
- When a stable, documented REST, GraphQL, or gRPC API is available for the target service.
- For simple, high-speed data scraping where [Crawl4AI](../process_understanding/crawl4ai.md) or standard Playwright would be more efficient.
- In environments where resource constraints (CPU/RAM) prevent the execution of a full browser environment.

## Getting started

### Installation
```bash
pip install browser-use
```

### Basic Usage with Gemma 3
```python
from browser_use import Agent
from langchain_google_vertexai import ChatVertexAI

async def main():
    agent = Agent(
        task="Navigate to GitHub and find the most starred repository for 'MCP 3.0'",
        llm=ChatVertexAI(model="gemma-3-27b"), # Utilizing Gemma 3 for visual reasoning
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())
```

## CLI examples
```bash
# Execute a browser-use task directly from the command line
python -m browser_use "Check my latest flight status on Delta"

# Launch the interactive Web UI for real-time task monitoring
python -m browser_use --ui

# Export the current session's browser state for debugging
python -m browser_use --export-state session_debug.json
```

## API examples
```python
from browser_use import Agent, Browser, BrowserConfig
from langchain_anthropic import ChatAnthropic

# Advanced configuration with headful mode and custom viewport
browser = Browser(config=BrowserConfig(headless=False, viewport={'width': 1920, 'height': 1080}))

agent = Agent(
    task="Go to my LinkedIn feed and summarize the top three posts about AI infrastructure",
    llm=ChatAnthropic(model="claude-4-8-opus"),
    browser=browser
)

async def run_task():
    history = await agent.run()
    print(f"Task completed in {len(history.steps)} steps.")
    await browser.close()
```

## Related tools / concepts
- [Stagehand](stagehand.md) — The TypeScript-based equivalent for agentic web browsing.
- [Skyvern](skyvern.md) — An open-source browser automation platform based on visual reasoning.
- [Crawl4AI](../process_understanding/crawl4ai.md) — An LLM-friendly web crawler and scraper.
- [Playwright](../development_ops/playwright.md) — The core automation engine utilized by Browser Use.
- [Model Context Protocol (MCP)](mcp.md) — The standard protocol for connecting agents to tools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous agent execution.
- [n8n](../../services/n8n.md) — A workflow automation tool for orchestrating multi-tool pipelines.

## Sources / References
- [Browser Use GitHub Repository](https://github.com/browser-use/browser-use)
- [Official Browser Use Documentation](https://docs.browser-use.ai/)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
