# Playwright

## What it is
Playwright is Microsoft's browser automation and end-to-end testing framework for Chromium, Firefox, and WebKit. As of June 2026, it is the industry standard for both automated testing and agentic web browsing using **MCP 3.0**.

## What problem it solves
It gives teams a reliable way to automate browsers for testing, scraping, and UI workflows that cannot be covered cleanly by API-only integrations. It addresses the complexity of cross-browser consistency and reduces flakiness in automated test suites. It also serves as the "eyes" for autonomous AI assistants like **Claude 4.8 Opus** and **GPT-5.5**.

## Where it fits in the stack
**Development & Ops / Browser Automation**. It is often used both for CI/CD test suites and as the execution layer for autonomous coding agents like [Claude Code](claude-code.md).

## Typical use cases
- End-to-end web application tests in CI/CD pipelines.
- Browser automation in agentic workflows (agent-assisted research).
- Reproducing or debugging UI regressions with high fidelity.
- Automated visual regression testing using pixel-matching.
- Web scraping in complex, JavaScript-heavy environments where headers and cookies must be managed.

## Strengths
- **Native Cross-Browser Support**: Provides a single API for Chromium, WebKit, and Firefox.
- **Auto-wait Logic**: Built-in mechanisms to eliminate most `sleep` or `waitFor` calls, making tests more resilient.
- **Powerful Tooling**: Includes a Trace Viewer, Test Runner, and Code Generator for rapid development.
- **Agent Readiness**: First-class integration with the **Playwright MCP Server** for LLM-driven browsing.

## Limitations
- **Execution Speed**: Browser automation is inherently slower than API-level interaction or unit testing.
- **Resource Intensive**: Running multiple headless browser instances requires significant memory and CPU resources.
- **UI Fragility**: Frequent UI changes still require manual or AI-assisted selector updates.

## When to use it
- When you need to verify real browser behavior or handle complex client-side JavaScript interactions.
- When agents must navigate or verify web interfaces directly as part of a task.
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
- [Playwright MCP Server](../automation_orchestration/playwright-mcp.md) — Browser automation for MCP agents.
- [Browser Use](../automation_orchestration/browser-use.md) — High-level agent framework for browser interaction.
- [Claude Code](claude-code.md) — Terminal agent that utilizes Playwright for web research.
- [GitHub Actions](../../playbooks/dev-workflow-ai-assisted.md) — For running Playwright tests in CI/CD.
- [Aider](aider.md) — AI coding assistant for writing and fixing Playwright tests.
- [Cursor 3.0](cursor.md) — IDE with deep integration for Playwright workflows.
- [Superpowers](../agents/superpowers.md) — Multi-agent framework for verifiable UI automation.
- [Puppeteer](../automation_orchestration/puppeteer.md) — The precursor and primary alternative to Playwright.

## Sources / References
- [Official Playwright Website](https://playwright.dev/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright MCP GitHub Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high
