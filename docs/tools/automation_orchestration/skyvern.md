# Skyvern

## What it is
Skyvern is an open-source browser automation platform that uses LLMs and Computer Vision to automate complex workflows on any website.

## What problem it solves
It replaces brittle, DOM-based automation (like traditional Playwright or Selenium scripts) with a visual-reasoning approach that "sees" the page, making it resistant to layout changes.

## Where it fits in the stack
**Infrastructure / Framework**. It provides a high-level, visual-reasoning-driven layer for browser-based agents.

## Typical use cases
- **Multi-Site Workflows**: Applying the same task (e.g., "download invoice") across dozens of different sites.
- **Visual Validation**: Checking UI elements and workflows based on visual appearance.
- **Workflow Automation**: Replacing unreliable DOM-parsing scripts.

## Strengths
- **Resilient**: Vision-based reasoning doesn't break when CSS classes or XPaths change.
- **No-Code / Low-Code**: Includes a workflow builder for non-technical users.
- **Playwright Compatible**: Can be integrated into existing Playwright-based SDKs.
- **High Stars**: Popular project with 20k+ stars.

## Limitations
- **Vision Model Costs**: Requires high-quality vision models, which are slower and more expensive.
- **Inference Latency**: Visual reasoning takes time, making it unsuitable for real-time applications.
- **Resource Intensive**: Requires significant compute (GPU) for local vision processing.

## When to use it
- When you need to automate workflows across many different websites.
- For tasks where DOM parsing is extremely difficult or unreliable.

## When not to use it
- For high-speed, simple data extraction from single-site APIs.
- When budget or latency constraints are strict.

## Getting started

### Installation
Skyvern is typically deployed via Docker for local use or accessed via the Skyvern Cloud.

```bash
git clone https://github.com/Skyvern-AI/skyvern.git
cd skyvern
docker-compose up
```

### Basic Usage
Once the Docker containers are running, you can access the Skyvern UI at `http://localhost:8000` to create your first automation workflow.

## CLI examples
```bash
# Start the Skyvern server and worker using Docker
docker-compose up -d

# Check the status of the Skyvern worker
docker-compose ps worker

# View logs from the Skyvern API server
docker-compose logs -f api
```

## API examples
```python
import requests

# Trigger a Skyvern workflow via the API
response = requests.post(
    "http://localhost:8000/api/v1/workflows/execute",
    json={
        "url": "https://example.com/login",
        "navigation_goal": "Log in and navigate to the invoices page",
        "extraction_goal": "Extract the last 3 invoice numbers and amounts"
    },
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

print(response.json())
```

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (Self-hosted) / Paid (Skyvern Cloud)
- **Self-hostable**: Yes

## Related tools / concepts
- [Browser Use](browser-use.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [n8n](../../services/n8n.md)
- [Stagehand](stagehand.md)
- [Playwright](../development_ops/playwright.md)
- [Lightpanda](lightpanda.md)

## Sources / References
- [GitHub](https://github.com/Skyvern-AI/skyvern)
- [Official Website](https://www.skyvern.com/)

## Contribution Metadata

- Last reviewed: 2026-05-22
- Confidence: high
