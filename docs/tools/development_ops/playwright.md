# Playwright

## What it is
Playwright is Microsoft's browser automation and end-to-end testing framework for Chromium, Firefox, and WebKit. As of January 2027, it serves as the industry standard for both automated testing and agentic web browsing using the **Model Context Protocol (FastMCP 3.1)**.

## What problem it solves
It gives teams a reliable way to automate browsers for testing, scraping, and UI workflows that cannot be covered cleanly by API-only integrations. It addresses the complexity of cross-browser consistency and reduces flakiness in automated test suites. It also serves as the "eyes and ears" for autonomous AI assistants like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, and **Gemini 4.0 Pro / Ultra**.

## Where it fits in the stack
**Development & Ops / Browser Automation**. It is used both for CI/CD test suites and as the core execution layer for autonomous coding agents like [Claude Code](claude-code-setup.md).

## Typical use cases
- End-to-end web application tests in CI/CD pipelines with parallel worker execution.
- Browser automation in agentic workflows (agent-assisted research and web interaction via FastMCP 3.1).
- Reproducing or debugging UI regressions with high fidelity using Trace Viewer and DOM snapshotting.
- Automated visual regression testing using pixel-matching and AI-assisted element selection.
- Web scraping in complex, JavaScript-heavy environments where headers, cookies, and fingerprinting must be managed.

## Strengths
- **Native Cross-Browser Support**: Provides a single API for Chromium, WebKit, and Firefox.
- **Auto-wait Logic**: Built-in mechanisms to eliminate most `sleep` or `waitFor` calls, making tests more resilient.
- **Powerful Tooling**: Includes a Trace Viewer, Test Runner, and Code Generator for rapid development.
- **Agent Readiness**: First-class integration with the **Playwright FastMCP Server (MCP 3.1)** for LLM-driven browsing and UI action execution.

## Limitations
- **Execution Speed**: Browser automation is inherently slower than API-level interaction or unit testing.
- **Resource Intensive**: Running multiple headless browser instances requires significant memory and CPU resources.
- **UI Fragility**: Frequent UI changes still require manual or AI-assisted selector updates.

## When to use it
- When you need to verify real browser behavior or handle complex client-side JavaScript interactions.
- When agents must navigate or verify web interfaces directly as part of a task via FastMCP 3.1.
- When you require high-fidelity visual or accessibility testing that unit tests cannot provide.

## When not to use it
- When a stable REST or GraphQL API is available for the same task.
- When the overhead of maintaining browser-based flows exceeds the value of the automation.
- For simple HTTP requests (use `curl` or a request library instead).

## Getting started

### 1. Installation
Playwright can be added to any Node.js project. Use the initializer to set up the recommended structure:

```bash
# Initialize Playwright in your project
npm init playwright@latest

# Install specific browser binaries
npx playwright install chromium
```

### 2. Hello-world Test
Create a simple test in `tests/example.spec.ts` to verify your setup:

```typescript
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);
});
```

### 3. Running Your Test
Execute the test runner to see Playwright in action:

```bash
npx playwright test
```

## CLI examples
The Playwright CLI is the primary way to run tests and generate code.

```bash
# Run all tests in the project
npx playwright test

# Generate code by recording your actions in the browser
npx playwright codegen https://example.com

# Open the Trace Viewer to debug a failed run
npx playwright show-trace path/to/trace.zip

# Run tests in headed mode to watch the execution
npx playwright test --headed
```

## API examples

### Basic Page Interaction (TypeScript)
```typescript
import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://news.ycombinator.com');

  // Extract data using CSS selectors
  const titles = await page.$$eval('.titleline > a', links =>
    links.map(link => link.textContent)
  );

  console.log(titles);
  await browser.close();
})();
```

### Programmatic Playwright Context Validation using Pydantic v2
This Python script parses and validates Playwright browser context configurations against standard schemas using **Pydantic v2** before launching automated sessions in agentic workflows:

```python
import json
from typing import Dict, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class ViewportSize(BaseModel):
    width: int = Field(..., ge=320, le=3840, description="Viewport width in pixels")
    height: int = Field(..., ge=240, le=2160, description="Viewport height in pixels")

class BrowserLaunchConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    headless: bool = Field(True, description="Whether to run browser in headless mode")
    channel: Optional[str] = Field(None, description="Specific browser channel (e.g. chrome, msedge)")
    viewport: ViewportSize = Field(
        default_factory=lambda: ViewportSize(width=1280, height=720),
        description="Default viewport size for pages"
    )
    user_agent: Optional[str] = Field(
        None,
        alias="userAgent",
        description="Custom User-Agent header string"
    )
    timeout: int = Field(30000, ge=0, description="Default navigation timeout in milliseconds")

def validate_launch_config(raw_json: str) -> Optional[BrowserLaunchConfig]:
    try:
        data = json.loads(raw_json)
        # Validate configuration using Pydantic v2
        config = BrowserLaunchConfig.model_validate(data)
        return config
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

# Example usage:
if __name__ == "__main__":
    sample_config = """
    {
        "headless": true,
        "userAgent": "Mozilla/5.0 (Playwright FastMCP Agent 2027)",
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "timeout": 45000
    }
    """
    validated = validate_launch_config(sample_config)
    if validated:
        print("Playwright configuration validated successfully!")
        print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Playwright MCP Server](../automation_orchestration/playwright-mcp.md) — Browser automation for MCP / FastMCP 3.1 agents.
- [Browser Use](../automation_orchestration/browser-use.md) — High-level agent framework for browser interaction.
- [Claude Code](claude-code-setup.md) — Terminal agent that utilizes Playwright for web research.
- [GitHub Actions](../../playbooks/dev-workflow-ai-assisted.md) — For running Playwright tests in CI/CD.
- [Aider](aider.md) — AI coding assistant for writing and fixing Playwright tests.
- [Cursor](cursor.md) — IDE with deep integration for Playwright workflows.
- [Superpowers](../agents/superpowers.md) — Multi-agent framework for verifiable UI automation.
- [Puppeteer](../automation_orchestration/puppeteer.md) — The precursor and primary alternative to Playwright.

## Sources / references
- [Official Playwright Website](https://playwright.dev/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright FastMCP Server GitHub Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
