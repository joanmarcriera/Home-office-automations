# Puppeteer

## What it is
Puppeteer is a Node.js library which provides a high-level API to control Chrome/Chromium over the DevTools Protocol. Developed by the Chrome DevTools team, it runs in headless mode by default but can be configured to run in full (non-headless) Chrome/Chromium. As of June 2026 (v25+), it features native **WebDriver BiDi** support and deep integration with **Chrome for Testing**.

## What problem it solves
It automates tasks that are typically performed manually in a web browser. It solves the "execution gap" for AI agents by providing a programmable interface to navigate, interact with, and extract data from modern, complex web applications that require JavaScript execution, authentication, and state management.

## Where it fits in the stack
Puppeteer sits in the **Automation & Orchestration** and **Browser Control** layer. It serves as a foundational primitive for "Computer Use" agents and high-fidelity web scraping pipelines.

## Typical use cases
- **Agentic Browser Navigation**: Serving as the "eyes and hands" for autonomous agents like [OpenHands](../development_ops/openhands.md) or [Stagehand](stagehand.md).
- **High-Fidelity Web Scraping**: Extracting data from Single Page Applications (SPAs) and sites with complex anti-bot mechanisms.
- **Automated Content Generation**: Generating screenshots, PDFs, and pre-rendered HTML for reports and SEO.
- **Performance & Accessibility Auditing**: Using the Chrome DevTools Protocol (CDP) to capture traces and run automated Lighthouse audits.
- **Visual Regression Testing**: Ensuring UI consistency across deployments by comparing pixel-perfect screenshots.

## Strengths
- **Native Chrome Integration**: Developed by Google, ensuring 1:1 parity with the latest Chrome features and security updates.
- **WebDriver BiDi**: Support for the new bidirectional protocol enables high-performance, cross-browser-compatible automation patterns.
- **Granular Control**: Direct access to the Chrome DevTools Protocol (CDP) for network interception, heap snapshots, and emulation.
- **Mature Ecosystem**: Extensive support via `puppeteer-extra` for stealth browsing, ad-blocking, and captcha solving.
- **Chrome for Testing**: Bundles specific, pinned browser versions to eliminate "it works on my machine" inconsistencies.

## Limitations
- **Chromium-First**: While BiDi support improves cross-browser compatibility, it remains primarily optimized for the Chromium engine.
- **Node.js Runtime Only**: No official first-party support for Python or other languages (unlike [Playwright](../development_ops/playwright.md)).
- **High Resource Overhead**: Running full browser instances in a serverless or containerized environment requires significant memory and CPU.

## When to use it
- When your automation task requires deep, low-level access to the Chrome engine.
- For high-performance web scraping where you need to intercept and modify network requests in real-time.
- When working in a Node.js-centric agentic framework that requires stable browser control.
- To generate deterministic PDFs or screenshots that match the latest Chrome rendering engine.

## When not to use it
- When you need to test or automate across multiple non-Chromium engines (use [Playwright](../development_ops/playwright.md)).
- For simple web scraping tasks that don't require JavaScript (use `Cheerio` or [Unstructured](../intake_storage/unstructured.md)).
- If you are building a Python-based agent (use Playwright's Python SDK).

## Getting started

### Installation
```bash
# Recommended for most users (includes Chromium)
npm i puppeteer

# For custom browser installations
npm i puppeteer-core
```

### Initial Setup
```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: "shell", // Optimized headless mode
  args: ['--no-sandbox']
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

## CLI examples
Puppeteer can be used from the CLI via `npx` for quick tasks.

```bash
# Take a screenshot of a website
npx puppeteer-cli screenshot https://google.com --path google.png

# Generate a PDF of a local HTML file
npx puppeteer-cli pdf ./index.html --path report.pdf

# Run a script with a specific Chrome version
PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) node my-script.js
```

## API examples

### Agentic Navigation with BiDi
Using the new bidirectional protocol for faster event handling.

```javascript
const browser = await puppeteer.launch({ protocol: 'webDriverBiDi' });
const page = await browser.newPage();

// High-performance event listening
await page.on('console', msg => console.log('PAGE LOG:', msg.text()));

await page.goto('https://news.ycombinator.com');
const results = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.titleline > a')).map(a => a.innerText);
});

await browser.close();
```

### Network Interception (CDP)
Blocking unnecessary resources to save bandwidth and improve speed.

```javascript
await page.setRequestInterception(true);
page.on('request', (request) => {
  if (['image', 'stylesheet', 'font'].includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md) - High-performance multi-browser automation.
- [Playwright MCP Server](playwright-mcp.md) - Model Context Protocol integration for browser control.
- [Stagehand](stagehand.md) - LLM-driven browser automation library.
- [Skyvern](skyvern.md) - Browser automation using AI vision and reasoning.
- [OpenHands](../development_ops/openhands.md) - Autonomous AI software engineer.
- [Browser Use](browser-use.md) - Standardized protocol for agentic browser interaction.
- [Stealth Patterns](../../knowledge_base/patterns/llm-trust-boundaries.md) - Techniques for avoiding bot detection.

## Sources / References
- [Official Website](https://pptr.dev/)
- [Puppeteer Documentation](https://pptr.dev/docs)
- [Puppeteer GitHub Repository](https://github.com/puppeteer/puppeteer)
- [WebDriver BiDi Progress Report (2026)](https://developer.chrome.com/blog/webdriver-bidi-status)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-24
