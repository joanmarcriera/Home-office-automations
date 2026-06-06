# Puppeteer

## What it is
Puppeteer is a Node.js library which provides a high-level API to control Chrome/Chromium over the DevTools Protocol. It runs in headless mode by default but can be configured to run in full (non-headless) Chrome/Chromium.

## What problem it solves
It automates tasks that are typically performed manually in a web browser. This includes generating screenshots and PDFs of pages, crawling a Single Page Application (SPA) and generating pre-rendered content (SSR), and automating form submission, UI testing, and keyboard input.

## Where it fits in the stack
**Development & Ops / Automation**. Similar to [Playwright](playwright.md), it is a foundational tool for browser-based automation. While Playwright is often preferred for multi-browser support, Puppeteer remains a standard for Chromium-centric automation and deep integration with Chrome-specific features.

## Typical use cases
- **Automated UI Testing**: Ensuring that web applications behave correctly across different Chromium versions.
- **Web Scraping**: Extracting data from modern web apps that require JavaScript execution to render content.
- **PDF/Screenshot Generation**: Creating visual snapshots of web pages for reports or previews.
- **Performance Auditing**: Using the Chrome DevTools Protocol to capture timeline traces and diagnose performance bottlenecks.
- **Agentic Browsing**: Serving as the "eyes and hands" for AI agents like [OpenHands](../development_ops/openhands.md).

## Strengths
- **First-Class Chromium Support**: Developed by the Chrome DevTools team, ensuring tight integration and early access to new browser features.
- **Mature Ecosystem**: Large community, extensive documentation, and a vast library of plugins (e.g., `puppeteer-extra`).
- **Deep DevTools Integration**: Direct access to the Chrome DevTools Protocol (CDP) for advanced browser manipulation.
- **Performance**: Generally lightweight and fast for Chromium-specific tasks.

## Limitations
- **Chromium-Centric**: While experimental support for Firefox exists, it is primarily designed for Chrome/Chromium.
- **Node.js Only**: The official library is restricted to the Node.js environment.
- **No Native Multi-Browser**: Does not provide the same level of unified API for WebKit or Firefox as [Playwright](playwright.md) does.

## When to use it
- When your automation is strictly targeted at Chrome or Chromium.
- When you need to use specific Chrome DevTools features not easily accessible via other libraries.
- For high-performance headless browsing where multi-browser support is not required.
- When working within an existing Node.js codebase that already uses Puppeteer.

## When not to use it
- When you need to test or automate across multiple browser engines (use [Playwright](playwright.md) instead).
- When working in non-JavaScript environments (though unofficial ports exist).
- For simple web scraping that doesn't require JavaScript execution (use `Cheerio` or [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for efficiency).

## Getting started

### Installation
```bash
npm i puppeteer # Downloads compatible Chromium
# OR
npm i puppeteer-core # Doesn't download Chromium
```

### Basic Example
```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({path: 'example.png'});

  await browser.close();
})();
```

## Technical Patterns

### Handling Dynamic Content
Waiting for a specific element to appear before interacting:

```javascript
await page.goto('https://example.com');
await page.waitForSelector('.dynamic-content');
const text = await page.$eval('.dynamic-content', el => el.textContent);
console.log(text);
```

### PDF Generation
```javascript
await page.goto('https://news.ycombinator.com', {
  waitUntil: 'networkidle2',
});
await page.pdf({path: 'hn.pdf', format: 'a4'});
```

## Related tools / concepts
- [Playwright](playwright.md)
- [Playwright MCP Server](playwright-mcp.md)
- [Browser Use](browser-use.md)
- [Stagehand](stagehand.md)
- [Skyvern](skyvern.md)
- [Claude Code](../development_ops/claude-code-setup.md)
- [OpenHands](../development_ops/openhands.md)

## Sources / references
- [Official Website](https://pptr.dev/)
- [Puppeteer GitHub Repository](https://github.com/puppeteer/puppeteer)
- [Chrome DevTools Protocol (CDP)](https://chromedevtools.github.io/devtools-protocol/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
