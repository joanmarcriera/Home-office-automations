# Multi-On

## What it is
Multi-On is an AI agent framework and API designed specifically for autonomous web navigation and interaction. It acts as a "motor cortex" for AI, allowing agents to perform complex tasks across any website using a combination of vision and DOM-based understanding.

## What problem it solves
Standard LLMs cannot interact with the live web autonomously. Traditional web scrapers are brittle and cannot handle complex, multi-step workflows (like booking a flight or merging a PR). Multi-On provides the infrastructure to bridge LLMs with the browser, handling authentication, navigation, and interaction reliably.

## Where it fits in the stack
**Category**: Agents / Web Automation

## Typical use cases
- **Personal Assistants**: "Book me a table for two at 7 PM tonight."
- **E-commerce Automation**: "Find the best price for this monitor and add it to my cart."
- **DevOps Automation**: "Check the status of my latest PR and merge it if the tests passed."
- **Data Collection**: "Gather all recent news about generative AI from these five sources."

## Strengths
- **Autonomous Navigation**: Can handle multi-step tasks across multiple domains.
- **Vision Support**: Uses visual grounding to interact with websites more like a human.
- **Resilient Interaction**: Self-healing capabilities to recover from navigation errors or UI changes.
- **Scalable Infrastructure**: Provides a managed API to run many agents in parallel.

## Limitations
- **Latency**: Complex web interactions can take significant time.
- **Cost**: Managed API usage incurs costs based on interaction volume.
- **Privacy**: Requires trust as the agent performs actions on your behalf on the web.

## When to use it
- When you need an agent to perform actions on the live web (not just read data).
- For complex, multi-step workflows that require navigating multiple pages.
- When you want to leverage a managed service for browser-based AI agents.

## When not to use it
- For simple data extraction where a specialized scraper like Crawl4AI would be faster and cheaper.
- If you have strict requirements to run everything locally without external API calls.

## Licensing and cost
- **Open Source**: No (Proprietary API)
- **Cost**: Paid (Usage-based pricing)
- **Self-hostable**: No (Managed service)

## Getting started

### Installation
```bash
pip install multion
```

### Basic Usage (Python)
```python
from multion.client import MultiOn

client = MultiOn(api_key="YOUR_API_KEY")

# Create a new session and browse to a site
response = client.browse(
    cmd="Go to news.ycombinator.com and find the top story about AI",
    url="https://news.ycombinator.com"
)

print(response.message)
```

## API examples

### Continuous Session
```python
# Create a session
session = client.sessions.create(url="https://www.google.com")

# Perform an action in the session
result = client.sessions.step(
    session_id=session.session_id,
    cmd="Search for 'best laptop 2024' and click the first review link"
)

print(result.message)

# Close the session when done
client.sessions.close(session_id=session.session_id)
```

## Related tools / concepts
- [Stagehand](../automation_orchestration/stagehand.md) — A library for resilient web automation built on Playwright.
- [Browser Use](../automation_orchestration/browser-use.md) — Another framework for browser-based agents.
- [Skyvern](../automation_orchestration/skyvern.md) — Open-source alternative for browser automation.
- [Playwright](../development_ops/playwright.md) — The underlying technology for many web automation tools.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Optimized for web crawling and data extraction.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The broader concept of multi-step AI tasks.

## Sources / references
- [Official Website](https://www.multion.ai/)
- [MultiOn Documentation](https://docs.multion.ai/)
- [MultiOn GitHub Examples](https://github.com/multion-ai/multion-python)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
