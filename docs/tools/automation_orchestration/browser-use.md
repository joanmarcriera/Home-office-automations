# Browser Use

## What it is
Browser Use is an open-source Python framework designed to enable Large Language Models (LLMs) to interact directly with real web browsers. It provides a high-level API for agents to perform complex multi-step tasks such as form-filling, navigating intricate UI flows, and extracting structured data. As of late 2026, Browser Use serves as a foundational tool for "Computer Use" capabilities, featuring native support for the **Model Context Protocol (MCP) 3.1** and **FastMCP 3.1** protocol, with optimized execution patterns for frontier models like **Gemma 3**, **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**.

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
- **FastMCP 3.1 Integration**: Can be deployed as a standardized MCP server, enabling any MCP-compliant client to utilize browser actions as a standard toolset.
- **Vision-First Reasoning**: Optimized for vision-capable models to improve navigation accuracy through spatial awareness and visual element recognition.
- **Extreme Extensibility**: Easy to define custom actions and integrate with existing Python-based agent stacks using standard middleware.
- **Gemma 3 & Claude 5.1 Support**: Native support for Gemma 3 and Claude 5.1's advanced visual reasoning capabilities for ultra-low latency browser interaction.

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
pip install browser-use pydantic
```

### Basic Usage with Gemma 3
```python
from browser_use import Agent
from langchain_google_vertexai import ChatVertexAI

async def main():
    agent = Agent(
        task="Navigate to GitHub and find the most starred repository for 'FastMCP 3.1'",
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
A key design pattern for robust agent operations is ensuring that extracted unstructured data is validated against a strict Pydantic v2 data contract before downstream consumption.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from browser_use import Agent, Browser, BrowserConfig
from langchain_anthropic import ChatAnthropic

# 1. Define strict output schemas using Pydantic v2
class SecurityPost(BaseModel):
    title: str = Field(description="Title of the security or AI infrastructure post")
    author: str = Field(description="Author of the post")
    likes: int = Field(default=0, description="Number of likes or reactions")
    summary: str = Field(description="A concise 2-sentence summary of the post content")

class LinkedInExtraction(BaseModel):
    posts: List[SecurityPost] = Field(description="List of extracted posts")
    source_url: str = Field(description="URL of the page where the posts were found")

# 2. Advanced configuration with custom viewport
browser = Browser(config=BrowserConfig(headless=True, viewport={'width': 1920, 'height': 1080}))

agent = Agent(
    task="Go to LinkedIn and find three posts about AI infrastructure security. Return the post titles, authors, and summaries.",
    llm=ChatAnthropic(model="claude-5-1-sonnet"),
    browser=browser
)

async def run_task():
    try:
        history = await agent.run()
        # Assume the history contains raw extracted JSON in the final result step
        raw_result_str = history.final_result() or '{"posts": [], "source_url": "https://linkedin.com"}'

        # Validate raw data strictly using Pydantic v2 model_validate_json
        validated_data = LinkedInExtraction.model_validate_json(raw_result_str)
        print("Successfully validated LinkedIn extraction against data contract!")
        for post in validated_data.posts:
            print(f"- {post.title} by {post.author} ({post.likes} likes)")
    except ValidationError as ve:
        print(f"Data contract validation failed: {ve}")
    except Exception as e:
        print(f"Error during agent execution: {e}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_task())
```

## Related tools / concepts
- [Stagehand](stagehand.md) — The TypeScript-based equivalent for agentic web browsing.
- [Skyvern](skyvern.md) — An open-source browser automation platform based on visual reasoning.
- [Crawl4AI](../process_understanding/crawl4ai.md) — An LLM-friendly web crawler and scraper.
- [Playwright](../development_ops/playwright.md) — The core automation engine utilized by Browser Use.
- [Model Context Protocol (MCP)](mcp.md) — The standard protocol for connecting agents to tools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous agent execution.
- [n8n](../../services/n8n.md) — A workflow automation tool for orchestrating multi-tool pipelines.

## Sources / references
- [Browser Use GitHub Repository](https://github.com/browser-use/browser-use)
- [Official Browser Use Documentation](https://docs.browser-use.ai/)
- [Anthropic Browser-Use Tool - The New Stack](https://thenewstack.io/anthropic-browser-use-tool/)
- [FastMCP Specification and Tools API](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-12-22
- Confidence: high
