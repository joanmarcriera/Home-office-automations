# Playwright

## What it is
**Playwright** is Microsoft's cross-browser automation, web scraping, and end-to-end testing framework for Chromium, Firefox, and WebKit. As of early 2027, it serves as both the enterprise standard for web application quality assurance and the foundational execution engine for autonomous AI web browsing agents operating via the **Model Context Protocol (FastMCP 3.1)**.

By controlling browser instances programmatically through native devtools protocols, Playwright enables frontier AI models—including **Claude 5.1**, **GPT-5.5 / GPT-5.6**, and **Gemini 4.0 Pro / Ultra**—to inspect web DOM trees, execute user interactions, intercept network traffic, and capture visual state snapshots.

```
+-----------------------------------------------------------------------------------+
|                            AGENTIC / TEST RUNNER LAYER                            |
|             (Playwright Test / Claude Code / FastMCP 3.1 Browser Agent)           |
+------------------------------------------+----------------------------------------+
                                           |
                              FastMCP 3.1 / DevTools Protocol
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                             PLAYWRIGHT BROWSER ENGINE                             |
|  +-----------------------+   +------------------------+   +--------------------+  |
|  | Multi-Context Router  |   | Auto-Wait & Selector   |   | Network Interceptor|  |
|  | (Chromium/Firefox/WK) |   | Engine                 |   | & Trace Recorder   |  |
|  +-----------+-----------+   +-----------+------------+   +---------+----------+  |
+-------------|---------------------------|---------------------------|-------------+
              |                           |                           |
              v                           v                           v
+-----------------------------------------------------------------------------------+
|                             HEADLESS BROWSER INSTANCES                            |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  | Chromium Engine    |  | Firefox Engine     |  | WebKit (Safari) Engine      |  |
|  +--------------------+  +--------------------+  +-----------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Modern single-page applications (SPAs) built with React, Vue, Svelte, and Next.js rely heavily on dynamic JavaScript rendering, shadow DOMs, and asynchronous network state:
- **Flaky Test Suites**: Traditional Selenium or HTTP-request automation scripts fail due to race conditions, rigid timing sleeps, and unhandled DOM state shifts.
- **Cross-Browser Inconsistencies**: Web applications display layout or JS discrepancies across Chromium, WebKit, and Firefox engines.
- **Agentic Blind Spots**: Autonomous AI agents restricted to static HTTP scrapers cannot authenticate behind complex SSO flows, render JS charts, or interact with canvas elements.
- **Debugging Friction**: Diagnosing transient CI test failures without full DOM snapshots, console logs, and network trace files consumes significant developer hours.

Playwright eliminates these issues by providing auto-waiting mechanisms, unified multi-browser execution, resilient CSS/role selectors, and high-fidelity trace recording.

## Where it fits in the stack
Playwright operates in the **Development & Ops / Browser Automation & AI Web Execution** layer. It functions as both a CI/CD end-to-end testing runner and the underlying execution backend for FastMCP 3.1 browser agents.

```
+-----------------------------------------------------------------------------------+
|                             DEVELOPER APPLICATION / AGENT                         |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                          PLAYWRIGHT FASTMCP 3.1 SERVER                            |
|             (Pydantic v2 Schema Enforcement & Async Browser Protocol)             |
+------------------------------------------+----------------------------------------+
                                           |
                              CDP / WebSocket Protocol
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                           BROWSER DOM & EXECUTION MATRIX                          |
|         (Headless Chromium, Firefox, WebKit, Trace Viewers, Visual Comparisons)   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases

### 1. End-to-End Visual & Functional CI/CD Testing
Running parallel, cross-browser test suites in GitHub Actions to verify user sign-up flows, checkout funnels, and accessibility standards across multiple viewports.

### 2. Autonomous Web Research & Interaction via FastMCP 3.1
Exposing browser tools (`navigate`, `click`, `type`, `screenshot`, `evaluate_js`) to Claude 5.1 or GPT-5.6, enabling agents to log into web applications, fill out forms, and extract dynamic data.

### 3. Visual Regression Testing & DOM Snapshotting
Comparing visual pixel diffs across deployment builds to prevent layout shifts, responsive design breakage, and unhandled CSS regressions.

### 4. JavaScript-Heavy Scraping & Network Interception
Scraping dynamic web data behind anti-bot protections by intercepting network API calls, injecting custom headers, or managing session cookies.

## Strengths
- **Native Cross-Browser Alignment**: Controls Chromium, Firefox, and WebKit using a single unified API.
- **Built-in Auto-Wait Logic**: Waits for elements to be visible, enabled, and stable before performing actions, drastically reducing test flakiness.
- **FastMCP 3.1 Ready**: First-class integration with the [Playwright MCP Server](../automation_orchestration/playwright-mcp.md) for direct LLM agent control.
- **Rich Tooling Ecosystem**: Includes built-in Test Runner, Trace Viewer, Code Generator (`codegen`), and visual comparison tools out of the box.
- **Context Isolation**: Fast context creation (`browser.newContext()`) allows thousands of isolated sessions to execute without full browser restarts.

## Limitations
- **Resource Footprint**: Running multiple headed or headless browser instances requires substantial memory and CPU allocation in CI environments.
- **Slower Than API Mocks**: Browser-based automation inherently incurs higher execution latency compared to pure HTTP API tests.
- **Selector Fragility**: Frequently updated DOM hierarchies require robust role-based or test-id selectors to avoid maintenance overhead.

## When to use it
- When verifying real user interactions and visual rendering in web applications across desktop and mobile viewports.
- When enabling AI agents to navigate, inspect, and interact with complex web applications via FastMCP 3.1.
- When generating reproducible traces and visual DOM snapshots for debugging CI failures.

## When not to use it
- For backend-only microservice testing where direct HTTP/gRPC requests provide faster and lighter coverage.
- For simple static HTML fetching where lightweight HTTP clients (e.g., `requests`, `httpx`, or `curl`) suffice.

## Getting started

### Installation
Initialize Playwright in your Node.js or Python repository:

```bash
# Node.js Project Setup
npm init playwright@latest

# Or Python Project Setup
pip install playwright pydantic mcp
playwright install chromium firefox webkit
```

### Basic Node.js / TypeScript Test
Create a test file `tests/example.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

test('Verify homepage title and agent callout', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);

  const getStarted = page.getByRole('link', { name: 'Get started' });
  await expect(getStarted).toBeVisible();
  await getStarted.click();
});
```

### Executing Tests
Execute test suites across browsers in parallel:

```bash
npx playwright test --project=chromium --headed
```

## CLI examples

### 1. Code Generation (`codegen`)
Record browser actions and generate executable Playwright scripts automatically:

```bash
npx playwright codegen https://example.com --target=typescript
```

### 2. Inspecting Test Traces
Open the interactive Trace Viewer to debug network requests, DOM state, and visual screenshots:

```bash
npx playwright show-trace ./test-results/example-has-title-chromium/trace.zip
```

### 3. Running Specific Tests in Debug Mode
Run tests with Playwright Inspector enabled for step-by-step DOM debugging:

```bash
PWDEBUG=1 npx playwright test tests/example.spec.ts
```

## API examples

### Full Python FastMCP 3.1 Browser Agent Server
Below is a production-grade Python FastMCP 3.1 server exposing Playwright browser capabilities to LLM agents:

```python
import os
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "Playwright Agentic Browser",
    version="3.1.0",
    description="Provides headless browser navigation and DOM inspection for FastMCP agents"
)

class NavigateRequest(BaseModel):
    url: str = Field(..., description="Target web URL to navigate")
    wait_until: str = Field(default="domcontentloaded", description="Navigation wait threshold")

    @field_validator("url")
    @classmethod
    def validate_url_scheme(cls, v: str) -> str:
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

class PageDetailsResponse(BaseModel):
    url: str
    title: str
    headings: List[str]
    status_code: int

@mcp.tool()
async def agent_navigate_and_extract(req: NavigateRequest) -> PageDetailsResponse:
    """Navigates to a target URL using Playwright and extracts page metadata."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.newContext(viewport={"width": 1280, "height": 720})
        page = await context.newPage()

        response = await page.goto(req.url, wait_until=req.wait_until)
        status = response.status if response else 0
        title = await page.title()

        # Extract H1 and H2 tags from DOM
        elements = await page.query_selector_all("h1, h2")
        headings = []
        for el in elements:
            text = await el.text_content()
            if text:
                headings.append(text.strip())

        await browser.close()

        return PageDetailsResponse(
            url=req.url,
            title=title,
            headings=headings[:10],
            status_code=status
        )

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Browser Context Configuration Validator (Pydantic v2)
Validate browser viewport, header, and timeout configurations prior to launching agent sessions:

```python
from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from typing import Dict, Optional

class ViewportSize(BaseModel):
    width: int = Field(1280, ge=320, le=3840)
    height: int = Field(720, ge=240, le=2160)

class PlaywrightContextSpec(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    headless: bool = Field(True, description="Run in headless execution mode")
    browser_type: str = Field("chromium", description="Target browser engine: chromium, firefox, webkit")
    viewport: ViewportSize = Field(default_factory=ViewportSize)
    user_agent: Optional[str] = Field(None, alias="userAgent")
    extra_http_headers: Optional[Dict[str, str]] = Field(None, alias="extraHTTPHeaders")
    timeout_ms: int = Field(30000, ge=1000, le=120000)

    @field_validator("browser_type")
    @classmethod
    def validate_engine(cls, v: str) -> str:
        valid = ["chromium", "firefox", "webkit"]
        if v.lower() not in valid:
            raise ValueError(f"Invalid browser engine '{v}'. Must be one of {valid}")
        return v.lower()

# Verification Example
config_data = {
    "headless": True,
    "browser_type": "chromium",
    "viewport": {"width": 1920, "height": 1080},
    "userAgent": "Mozilla/5.0 (FastMCP Agent 2027)",
    "extraHTTPHeaders": {"X-Agent-Source": "Playwright-FastMCP"},
    "timeout_ms": 45000
}

spec = PlaywrightContextSpec.model_validate(config_data)
print(f"Validated Playwright Engine: {spec.browser_type}")
print(f"User Agent: {spec.user_agent}")
```

## Comparative Metrics & Browser Engine Matrix

| Performance Metric | Chromium | Firefox | WebKit (Safari) |
| :--- | :--- | :--- | :--- |
| **Startup Latency** | **Fast (~120ms)** | Moderate (~210ms) | Fast (~140ms) |
| **Memory Footprint / Tab** | ~85 MB | ~110 MB | ~70 MB |
| **DevTools Protocol Depth** | Full (Native CDP) | Partial (Juggler) | Partial (WKProtocol) |
| **FastMCP 3.1 Agent Fit** | **Primary / Best** | Secondary | Mobile Verification |
| **Parallel Instance Capacity** | High | Medium | High |

## Troubleshooting & Edge Case Handling

### 1. Handling Headless Anti-Bot / Captcha Blocks
When automation targets block headless user agents, customize launch contexts with realistic headers and stealth flags:

```python
context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    viewport={"width": 1920, "height": 1080},
    locale="en-US"
)
```

### 2. Resolving Memory Leaks in Multi-Step Agent Runs
Ensure browser contexts are explicitly closed in `try...finally` blocks to prevent zombie processes in CI:

```python
context = await browser.new_context()
try:
    page = await context.new_page()
    await page.goto("https://target-site.com")
finally:
    await context.close()
```

## Related tools / concepts
- [Playwright MCP Server](../automation_orchestration/playwright-mcp.md) — FastMCP 3.1 server for LLM browser integration.
- [Browser Use](../automation_orchestration/browser-use.md) — Agent framework built on top of browser automation.
- [Puppeteer](../automation_orchestration/puppeteer.md) — Node.js browser automation library for Chromium.
- [Claude Code](claude-code-setup.md) — Terminal agent using Playwright for web research.
- [Aider](aider.md) — AI coding pair programmer.
- [Cursor](cursor.md) — AI-native IDE with deep testing integration.

## Sources / references
- [Official Playwright Portal](https://playwright.dev/)
- [Playwright API Documentation](https://playwright.dev/docs/intro)
- [Playwright FastMCP Server Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
