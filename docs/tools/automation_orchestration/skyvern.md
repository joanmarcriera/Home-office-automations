# Skyvern

## What it is
Skyvern is an open-source browser automation platform that leverages LLMs and Computer Vision to automate complex workflows on any website. Unlike traditional automation tools that rely on the DOM (Document Object Model), Skyvern uses visual reasoning to interact with websites. As of June 2026, it is widely used for enterprise-scale browser automation where reliability across diverse and changing UIs is paramount.

## What problem it solves
It solves the "fragility" problem of web automation. Traditional scripts (Playwright, Selenium) break whenever a website's CSS classes, IDs, or internal structure changes. Skyvern "sees" the page like a human, allowing it to find buttons, fields, and information based on visual appearance and context, making it extremely resilient to UI updates and redesigns.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation. It provides a robust, visual-reasoning layer for agents, often integrated into larger business process automation (BPA) pipelines or used alongside tools like [n8n](../../services/n8n.md).

## Typical use cases
- **Cross-Platform Workflows**: Executing the same task (e.g., "Extract monthly invoice") across dozens of different vendor portals with unique UIs.
- **Legacy System Integration**: Automating interaction with old web-based systems that lack APIs and have inconsistent DOM structures.
- **Visual Data Gathering**: Extracting information from websites where the data is presented visually (e.g., charts, maps) or in heavily obfuscated HTML.
- **Automated Compliance Audits**: Visually verifying that certain elements or disclosures are present across a large number of web pages.

## Strengths
- **Visual Resilience**: Doesn't break on DOM changes; relies on what the user actually sees.
- **Zero-Shot Automation**: Can often automate a new website without any prior training or selector mapping.
- **Workflow Builder**: Includes a low-code interface for designing complex multi-step automations.
- **Observability**: Provides detailed logs and video recordings of every step the agent takes for auditability.

## Limitations
- **Computational Cost**: Visual reasoning requires significant GPU resources for local inference or expensive vision-LLM calls.
- **Latency**: Processing screenshots and reasoning visually is slower than direct DOM interaction.
- **Complex UI Hurdles**: May still struggle with extremely non-standard interactive elements like complex 3D canvases or highly unconventional navigation patterns.

## When to use it
- When you need to automate a task across many different, unrelated websites.
- For websites where the internal HTML structure is intentionally obfuscated or frequently changed.
- When reliability is more important than raw execution speed.

## When not to use it
- For simple scraping of a single, stable website where a basic CSS selector or API would be faster and cheaper.
- In high-throughput scenarios where thousands of pages must be processed per minute.
- When running on hardware without sufficient GPU acceleration for visual processing.

## Getting started

### Installation
Skyvern is typically deployed via Docker.

```bash
git clone https://github.com/Skyvern-AI/skyvern.git
cd skyvern
docker-compose up
```

### Basic Usage
After deployment, the Skyvern UI is accessible at `http://localhost:8000`. You can define a "Goal" (e.g., "Log in to my bank and download the statement") and Skyvern will attempt to execute it autonomously.

## CLI examples
```bash
# Start Skyvern infrastructure
docker-compose up -d

# Check worker health
docker-compose ps

# Monitor real-time logs from the worker
docker-compose logs -f worker
```

## API examples
```python
import requests

# Triggering a goal via the Skyvern API
response = requests.post(
    "http://localhost:8000/api/v1/goals",
    json={
        "url": "https://portal.example.com",
        "goal": "Find the 'Billing' section and extract the balance due",
        "proxy_config": {"use_residential": True}
    },
    headers={"Authorization": "Bearer YOUR_SECRET_KEY"}
)

print(f"Goal ID: {response.json()['goal_id']}")
```

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0)
- **Cost**: Free (Self-hosted) / Paid (Skyvern Cloud for managed infrastructure).
- **Self-hostable**: Yes

## Related tools / concepts
- [Browser Use](browser-use.md) — Python-based agentic browser framework.
- [Stagehand](stagehand.md) — TypeScript-based semantic browser automation.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Efficient scraper for LLM data ingestion.
- [n8n](../../services/n8n.md) — For scheduling and orchestrating Skyvern tasks.
- [Playwright](../development_ops/playwright.md) — The underlying driver for browser interaction.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Best practices for browser-based agents.
- [Model Context Protocol](mcp.md) — For standardizing tool access for agents.
- [Lightpanda](lightpanda.md) — A lightweight, high-performance browser alternative.

## Sources / References
- [Skyvern GitHub](https://github.com/Skyvern-AI/skyvern)
- [Official Website](https://www.skyvern.com/)
- [Skyvern Documentation](https://docs.skyvern.com/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
