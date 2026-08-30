# Playwright MCP Server

## What it is
The Playwright MCP Server is a Model Context Protocol (MCP) implementation that provides AI agents with a "headless browser" interface. As of early 2027, it is the primary tool for enabling frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL** to interact with the live web using the **FastMCP 3.1** Task Protocol.

## What problem it solves
Most LLMs lack direct access to the web or can only "see" through static screenshots or text-only scrapers. Playwright MCP provides structured access to the DOM and the **Accessibility Tree**, allowing agents to click buttons, fill forms, and extract data from JavaScript-heavy sites reliably without needing a dedicated REST API.

## Where it fits in the stack
**Agent Tooling / Browser Automation**. It sits between the AI reasoning engine and the interactive web. It is often used as a fallback or "last mile" tool when official [API Providers](../providers/index.md) are unavailable or limited.

## Typical use cases
- **Dynamic Web Scraping**: Extracting data from sites that require JavaScript execution or user interaction.
- **Agentic Workflows**: Allowing an AI to perform tasks like booking travel, purchasing items, or managing SaaS dashboards.
- **Automated Testing**: Writing and running E2E tests through a natural language interface where the AI "explores" the UI.
- **Visual Verification**: Generating screenshots and PDFs of web pages for agentic review and reporting.

## Strengths
- **Accessibility Tree Focus**: Emphasizes semantic structure over raw pixels, making interaction faster and more robust.
- **Cross-Browser Support**: Leverages Playwright's native support for Chromium, Firefox, and WebKit.
- **FastMCP 3.1 Task Protocol**: Fully compatible with the FastMCP 3.1 Task Protocol for standardized benchmarking, execution, and task tracking across autonomous multi-agent systems.
- **Sandboxed Execution**: Can be easily run in [Docker](../infrastructure/docker.md) to isolate browser sessions.

## Limitations
- **High Resource Usage**: Running a browser instance consumes significantly more CPU and RAM than lightweight MCP servers.
- **Latency**: Each browser interaction introduces substantial delay compared to direct API calls.
- **Detection Risk**: Headless browsers are frequently flagged by anti-bot systems without sophisticated stealth plugins.

## When to use it
- When an AI agent needs to perform actions on a website that lacks a public API.
- For "self-healing" automation where the agent can adapt to UI changes in real-time.
- When you need to extract data that is only visible after complex client-side state changes.

## When not to use it
- If a stable and documented REST/GraphQL API is available for the target service.
- For high-throughput scraping where the overhead of a full browser is prohibitive.
- In low-memory environments where browser instances might cause OOM errors.

## Getting started

### Installation
The server can be run on-demand via `npx`:

```bash
# Run the Playwright MCP server
npx -y @modelcontextprotocol/server-playwright
```

### Configuration (Claude Desktop)
To enable the tool in Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-playwright"
      ]
    }
  }
}
```

## CLI examples

### Running via Docker
For a sandboxed environment with all dependencies pre-installed:

```bash
docker run -i --rm mcr.microsoft.com/playwright:v1.49.0-noble npx -y @modelcontextprotocol/server-playwright
```

### Manual Verification
You can test the server's basic connectivity using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-playwright
```

## API examples

### Programmatic Setup with Pydantic v2 Validation & FastMCP 3.1 Task Tracking
To maintain the safety, integrity, and rate of headless interactions in early 2027, browser operations must be strictly validated. Below is a Python script employing **Pydantic v2** validation schemas and **FastMCP 3.1** task protocol context parameters.

```python
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
import asyncio

# 1. Define schemas using strict Pydantic v2 annotations with FastMCP 3.1 Task Protocol support
class BrowserNavigateAction(BaseModel):
    url: str = Field(..., description="The fully qualified HTTP/HTTPS URL to navigate to.")
    wait_until: str = Field(default="domcontentloaded", pattern="^(load|domcontentloaded|networkidle|commit)$")
    timeout_ms: int = Field(default=30000, ge=1000, le=120000)

class ClickAction(BaseModel):
    selector: str = Field(..., min_length=1, description="CSS or Playwright text/selector.")
    click_count: int = Field(default=1, ge=1, le=5)

class BrowserSessionRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 Task Protocol identifier for correlation tracking.")
    navigation: BrowserNavigateAction
    click: Optional[ClickAction] = None

# 2. Programmatic execution utilizing validation
async def run_validated_browser_session(payload: dict) -> str:
    try:
        # Strict validation of input using Pydantic v2
        request = BrowserSessionRequest.model_validate(payload)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        raise

    print(f"[Task {request.task_id}] Navigating to {request.navigation.url} (wait: {request.navigation.wait_until})...")

    # In a FastMCP 3.1 setup, this triggers the Playwright MCP server calls.
    # Here we simulate the browser action sequence.
    output_log = f"[Task {request.task_id}] Successfully loaded {request.navigation.url}."

    if request.click:
        print(f"[Task {request.task_id}] Clicking selector: '{request.click.selector}' {request.click.click_count} time(s)...")
        output_log += f"\nPerformed {request.click.click_count} click(s) on selector '{request.click.selector}'."

    return output_log

# Example invocation in early 2027
if __name__ == "__main__":
    action_payload = {
        "task_id": "task-playwright-2027-0107",
        "navigation": {
            "url": "https://news.ycombinator.com",
            "wait_until": "networkidle",
            "timeout_ms": 15000
        },
        "click": {
            "selector": "text=new",
            "click_count": 1
        }
    }

    result = asyncio.run(run_validated_browser_session(action_payload))
    print(result)
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md) — The underlying automation library.
- [Browser Use](browser-use.md) — A specialized library for LLM-browser interaction.
- [Stagehand](stagehand.md) — An AI-native web automation wrapper.
- [Skyvern](skyvern.md) — A platform for automating browser-based workflows.
- [Puppeteer](puppeteer.md) — The primary alternative to Playwright.
- [Claude Code](../development_ops/claude-code-setup.md) — A terminal-based agent that frequently uses this MCP.
- [Model Context Protocol](mcp.md) — The standard for connecting tools to LLMs.
- [Local LLMs](../ai_knowledge/local_llms.md) — Self-hosted models that can host this MCP.

## Sources / references
- [Playwright MCP GitHub Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)
- [Official MCP Documentation](https://modelcontextprotocol.io)
- [Playwright Official Documentation](https://playwright.dev)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high