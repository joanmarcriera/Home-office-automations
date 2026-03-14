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

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Browser Use](../automation_orchestration/browser-use.md)
- [Claude Hooks](claude-hooks.md)
- [n8n](../../services/n8n.md)

## Sources / References
- [Official Website](https://playwright.dev/)
- [Documentation](https://playwright.dev/docs/intro)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: high
