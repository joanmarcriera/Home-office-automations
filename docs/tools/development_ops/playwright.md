# Playwright

## What it is
Playwright is Microsoft's browser automation and end-to-end testing framework for Chromium, Firefox, and WebKit.

## What problem it solves
It gives teams a reliable way to automate browsers for testing, scraping, and UI workflows that cannot be covered cleanly by API-only integrations.

## Where it fits in the stack
**Development & Ops / Browser Automation**. It is often used both for test suites and as the browser execution layer for coding agents.

## Typical use cases
- End-to-end web application tests
- Browser automation in agent workflows
- Reproducing or debugging UI regressions

## Strengths
- Cross-browser support
- Strong automation primitives and test tooling
- Useful both as a test runner and an agent browser backend

## Limitations
- Browser automation is slower and more brittle than API-level integration
- Requires careful test design to avoid flaky suites

## When to use it
- When you need real browser behavior
- When agents must navigate or verify web interfaces directly

## When not to use it
- When an API integration is available and sufficient
- When the maintenance cost of browser flows outweighs the value

## Selection comments
- Playwright is the preferred tool for high-reliability browser automation due to its "auto-wait" features and robust selector engine.
- For AI agent integration, use the [Playwright MCP](https://github.com/microsoft/playwright-mcp) to give agents direct "eyes" on a web page.
- Combine with [Superpowers](../agents/superpowers.md) for verifiable UI testing and automation cycles.

## CLI examples

```bash
# Install Playwright and browsers
npm init playwright@latest

# Generate code by recording your actions
npx playwright codegen https://example.com

# Run tests in headed mode
npx playwright test --headed

# Debugging with Playwright Inspector
PWDEBUG=1 npx playwright test
```

## API examples

### Basic Page Interaction (TypeScript)
```typescript
import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://news.ycombinator.com');

  // Extract data from the page
  const titles = await page.$$eval('.titleline > a', links =>
    links.map(link => link.textContent)
  );

  console.log(titles);
  await browser.close();
})();
```

### Visual Regression Testing
```typescript
import { test, expect } from '@playwright/test';

test('homepage visual check', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveScreenshot('homepage.png');
});
```

## Example workflow: Agentic Browsing
1. **Trigger**: An agent receives a request to find the price of a specific product on a site without an API.
2. **Execution**: The agent uses the [Playwright MCP](https://github.com/microsoft/playwright-mcp) to launch a Chromium instance.
3. **Navigation**: The agent instructs Playwright to `page.goto()`, `page.fill()` (search bar), and `page.click()`.
4. **Extraction**: The agent parses the DOM for price elements using CSS selectors or text matching.
5. **Verification**: Playwright takes a screenshot of the results to provide visual proof to the user.

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Browser Use](../automation_orchestration/browser-use.md)
- [Claude Hooks](claude-hooks.md)
- [n8n](../../services/n8n.md)
- [GitHub Copilot](github_copilot.md)
- [VS Code](vscode.md)
- [Aider](aider.md)
- [Cursor](cursor.md)
- [Superpowers](../agents/superpowers.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)

## Sources / References
- [Official Website](https://playwright.dev/)
- [Documentation](https://playwright.dev/docs/intro)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
