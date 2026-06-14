# Playwright

## What it is
Playwright is Microsoft's browser automation and end-to-end testing framework for Chromium, Firefox, and WebKit. As of June 2026, it is the industry standard for both automated testing and agentic web browsing.

## What problem it solves
It gives teams a reliable way to automate browsers for testing, scraping, and UI workflows that cannot be covered cleanly by API-only integrations. It addresses:
- **Cross-Browser Consistency**: Ensuring web applications work across all modern engines.
- **Flakiness**: Using auto-wait and robust selector engines to reduce unstable test suites.
- **Agentic Eyes**: Providing a structured interface for AI agents to "see" and interact with the web through the [Playwright MCP](../automation_orchestration/playwright-mcp.md).

## Where it fits in the stack
**Development & Ops / Browser Automation**. It is often used both for CI/CD test suites and as the execution layer for autonomous coding agents like [Claude Code](claude-code.md).

## Typical use cases
- End-to-end web application tests.
- Browser automation in agentic workflows (agent-assisted research).
- Reproducing or debugging UI regressions.
- Automated visual regression testing.
- Web scraping in complex, JavaScript-heavy environments.

## Strengths
- **Native Cross-Browser Support**: Single API for Chromium, WebKit, and Firefox.
- **Auto-wait Logic**: Eliminates most `sleep` or `waitFor` calls.
- **Powerful Tooling**: Includes a Trace Viewer, Test Runner, and Code Generator.
- **Agent Readiness**: First-class integration with MCP for LLM-driven browsing.

## Limitations
- **Speed**: Browser automation is inherently slower than API-level interaction.
- **Resource Intensive**: Running multiple browser instances requires significant memory and CPU.
- **Maintenance**: UI changes still require selector updates, though AI-assisted tools like [Aider](aider.md) can mitigate this.

## When to use it
- When you need to verify real browser behavior or handle complex JS interactions.
- When agents must navigate or verify web interfaces directly.
- When you require high-fidelity visual or accessibility testing.

## When not to use it
- When a stable REST or GraphQL API is available for the same task.
- When the overhead of maintaining browser-based flows exceeds the value of the automation.
- For simple HTTP requests (use `curl` or a request library instead).

## Getting started

### Installation
Playwright can be added to any Node.js project:

```bash
# Initialize Playwright in your project
npm init playwright@latest

# Install specific browser binaries
npx playwright install chromium
```

### Hello-world Test
Create a simple test in `tests/example.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);
});
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
Playwright provides a rich API for fine-grained browser control.

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

## Related tools / concepts
- [Playwright MCP Server](../automation_orchestration/playwright-mcp.md) — Browser automation capabilities for MCP agents.
- [Browser Use](../automation_orchestration/browser-use.md) — High-level agent framework for browser interaction.
- [Claude Code](claude-code.md) — Terminal agent that utilizes Playwright for web research.
- [GitHub Actions](github-pages.md) — For running Playwright tests in CI/CD.
- [Aider](aider.md) — AI coding assistant for writing and fixing Playwright tests.
- [Cursor](cursor.md) — IDE with deep integration for Playwright workflows.
- [Superpowers](../agents/superpowers.md) — Multi-agent framework for verifiable UI automation.
- [Puppeteer](../automation_orchestration/puppeteer.md) — The precursor and primary alternative to Playwright.

## Sources / references
- [Official Playwright Website](https://playwright.dev/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright MCP GitHub Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
