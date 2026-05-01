# Stagehand

## What it is
Stagehand is a library designed for "browser-use" automation, specifically focused on making web interactions for AI agents more reliable and easier to script. It provides a higher-level abstraction over Playwright, optimized for the way LLMs perceive and interact with web pages.

## What problem it solves
Traditional web automation (like vanilla Playwright or Selenium) is brittle; if a CSS selector changes, the script breaks. Stagehand solves this by allowing agents to interact with elements based on semantic meaning and visual layout, making automation much more resilient to UI changes.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation

## Typical use cases
- **Agentic Web Browsing**: Enabling an agent to "go find the pricing page and tell me the cost of the Pro plan."
- **Automated Data Extraction**: Scraping complex, dynamic websites without writing custom CSS selectors.
- **Testing**: Creating resilient end-to-end tests that don't break on every minor frontend update.

## Strengths
- **Resiliency**: Uses LLMs to "heal" selectors and understand the page structure.
- **Simplified API**: Reduces the boilerplate code needed for complex web interactions.
- **Playwright Powered**: Built on top of a rock-solid, industry-standard browser automation engine.
- **Visual Grounding**: Optimized for use with vision-capable models (LMMs).

## Limitations
- **Latency**: LLM-based element discovery is slower than traditional CSS/XPath selection.
- **Token Cost**: Requires LLM calls for reasoning about the page content.

## Getting started

### Installation
```bash
npm install @browserbase/stagehand
```

### Basic Usage
```typescript
import { Stagehand } from "@browserbase/stagehand";

const stagehand = new Stagehand();
await stagehand.init();
const page = stagehand.page;

await page.goto("https://news.ycombinator.com");
// Stagehand-specific semantic interaction
await page.act("Find the first article about AI and click its comments link");
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md)
- [Browser Use](browser-use.md)
- [Lightpanda](lightpanda.md)
- [Skyvern](skyvern.md)

## Sources / references
- [Stagehand GitHub Repository](https://github.com/browserbase/stagehand)
- [Browserbase Website](https://www.browserbase.com/)

## Contribution Metadata
- Last reviewed: 2026-05-09
- Confidence: high
