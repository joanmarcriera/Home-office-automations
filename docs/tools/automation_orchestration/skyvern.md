# Skyvern

## What it is
Skyvern is an open-source browser automation platform that leverages Large Language Models (LLMs) and advanced Computer Vision to automate complex workflows on any website. Unlike traditional automation tools that rely on the underlying DOM (Document Object Model), Skyvern utilizes visual reasoning to interact with web elements. As of early January 2027, Skyvern is a premier solution for enterprise-scale browser automation, offering native support for the **MCP 3.1 / FastMCP 3.1 Task Protocol** and optimized integration with **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
It effectively addresses the "fragility" problem inherent in web automation. Traditional frameworks (like Playwright or Selenium) often fail when a website's internal CSS classes, IDs, or HTML structures are updated. Skyvern "sees" the page exactly as a human does, identifying buttons, fields, and informational elements based on their visual appearance and semantic context. This approach makes it exceptionally resilient to UI redesigns and anti-bot measures that obfuscate the DOM.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation. It provides a robust, visual-reasoning execution layer for autonomous agents. Skyvern is frequently integrated into Business Process Automation (BPA) pipelines and orchestrated via tools like [n8n](../../services/n8n.md) or [Agno](../agents/agno.md).

## Typical use cases
- **Cross-Vendor Workflow Standardization**: Executing identical tasks (e.g., "Download the May 2026 invoice") across hundreds of distinct vendor portals, each with a unique UI.
- **Legacy Interface Automation**: Automating interactions with aged web-based systems that lack modern APIs and possess inconsistent or legacy DOM structures.
- **Semantic Visual Extraction**: Gathering data from websites where information is presented visually (e.g., interactive charts, dynamic maps) rather than in static HTML.
- **Automated Visual Compliance**: Verifying the presence and correct visual placement of legal disclosures or specific UI elements across a vast array of web properties.

## Strengths
- **Inherent Visual Resilience**: Operates independently of the DOM; if a human can find it, Skyvern can too.
- **Zero-Shot Task Execution**: Capable of automating tasks on entirely new websites without prior selector mapping or manual training.
- **Enterprise Observability**: Features a comprehensive dashboard with detailed logs, step-by-step screenshots, and video recordings for full auditability.
- **MCP 3.1 / FastMCP 3.1 Compliance**: Seamlessly integrates into standardized agentic ecosystems, allowing Skyvern "Goals" to be called as standard FastMCP 3.1 tools.

## Limitations
- **Substantial Resource Requirements**: Visual reasoning and screenshot processing necessitate significant GPU acceleration or high-cost vision-LLM API calls.
- **Execution Latency**: The pipeline of capturing screenshots, visual processing, and LLM reasoning is naturally slower than direct script-based interaction.
- **Highly Complex Interactivity**: May still encounter difficulties with non-standard elements like nested iframe-based editors or complex 3D WebGL canvases.

## When to use it
- When you need to automate tasks across a wide variety of unrelated and frequently changing websites.
- For services where the HTML is intentionally obfuscated (anti-scraping) or where DOM-based selectors are unreliable.
- When automation reliability and "human-like" interaction are more critical than raw speed.

## When not to use it
- For high-speed data scraping of a single, stable website where a simple [Crawl4AI](../process_understanding/crawl4ai.md) setup or direct API would be more cost-effective.
- In low-latency scenarios where tasks must be completed in milliseconds.
- On hardware environments that lack the necessary compute power for vision-based reasoning.

## Getting started

### Installation
Skyvern is best deployed using Docker to manage its vision and browser dependencies.

```bash
git clone https://github.com/Skyvern-AI/skyvern.git
cd skyvern
docker-compose up -d
```

### Basic Usage with FastMCP 3.1
Once deployed, Skyvern exposes a FastMCP 3.1 server. You can connect it to a client like [Claude Desktop](../ai_knowledge/claude-desktop.md) or a custom [FastMCP](mcp.md) host:

1. Add the Skyvern MCP endpoint to your configuration.
2. Provide a natural language goal: "Log in to my utility portal and report my current usage."

## CLI examples
```bash
# Start the Skyvern stack in detached mode
docker-compose up -d

# View the status of the Skyvern workers and vision processors
docker-compose ps

# Tail logs for a specific Skyvern worker to debug visual reasoning
docker-compose logs -f skyvern-worker
```

## API examples

### Programmatic Automation with Pydantic v2 Validation
To maintain compliance with January 2027 data verification checks, visual goal configurations dispatched to Skyvern are strictly validated before invocation.

```python
import requests
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from typing import Dict, Any, Optional

# 1. Define strict validation schemas using Pydantic v2
class ProxyConfiguration(BaseModel):
    proxy_type: str = Field(default="residential", pattern="^(residential|datacenter|none)$")
    country_code: Optional[str] = Field(None, max_length=2, min_length=2, description="ISO country code")

class ScrapingGoal(BaseModel):
    url: HttpUrl
    goal: str = Field(..., min_length=10, max_length=1000)
    vision_model: str = Field(default="qwen-3.6-vl", pattern="^(qwen-3.6-vl|claude-5.6|gpt-5.6|gemini-4.0-ultra|gemma-4|deepseek-v4)$")
    proxy_config: ProxyConfiguration = Field(default_factory=ProxyConfiguration)

# 2. Programmatic target execution utilizing validation and Skyvern REST API
def submit_skyvern_goal(payload: Dict[str, Any]) -> str:
    try:
        # Strict validation of input using Pydantic v2
        validated_payload = ScrapingGoal.model_validate(payload)
    except ValidationError as e:
        print(f"Goal validation failed: {e}")
        raise

    # Convert Pydantic model to dict, ensuring serializable types (like HttpUrl to str)
    request_data = validated_payload.model_dump(mode="json")

    headers = {
        "Authorization": "Bearer ${SKYVERN_API_KEY}",
        "Content-Type": "application/json"
    }

    # Post verified schema to Skyvern local endpoint
    response = requests.post(
        "http://localhost:8000/api/v1/goals",
        json=request_data,
        headers=headers
    )
    response.raise_for_status()
    return response.json()["id"]

# Example invocation
if __name__ == "__main__":
    payload = {
        "url": "https://shipping.example.com",
        "goal": "Find the tracking number for the last order and update the status",
        "vision_model": "claude-5.6",
        "proxy_config": {
            "proxy_type": "residential",
            "country_code": "US"
        }
    }
    try:
        goal_id = submit_skyvern_goal(payload)
        print(f"Goal successfully submitted to Skyvern. Goal ID: {goal_id}")
    except Exception as e:
        pass
```

## Related tools / concepts
- [Browser Use](browser-use.md) — A Python-based framework for agentic browser interaction.
- [Stagehand](stagehand.md) — A TypeScript equivalent focusing on semantic web automation.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Optimized web crawling and scraping for LLMs.
- [n8n](../../services/n8n.md) — For orchestrating Skyvern within broader multi-app workflows.
- [Playwright](../development_ops/playwright.md) — The underlying automation driver for Skyvern.
- [Model Context Protocol (MCP)](mcp.md) — The protocol used for standardized tool integration.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous browser agents.
- [Agno](../agents/agno.md) — A multi-agent framework that can utilize Skyvern as a tool.

## Sources / References
- [Skyvern GitHub Repository](https://github.com/Skyvern-AI/skyvern)
- [Official Skyvern Website](https://www.skyvern.com/)
- [Skyvern Technical Documentation](https://docs.skyvern.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
