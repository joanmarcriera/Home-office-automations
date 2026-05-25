# Lightpanda Browser

## What it is
Lightpanda is a headless browser built from scratch for AI agents and automation, written in Zig. It is not a fork of Chromium or WebKit.

## What problem it solves
It provides a lightweight, extremely fast, and low-memory footprint browser for agents, avoiding the overhead and "bloat" of traditional browser engines while maintaining high compatibility for web automation.

## Where it fits in the stack
**Category**: Tool / Automation Orchestration

## Typical use cases
- High-performance web scraping and data extraction.
- Browser-based agentic workflows (e.g., using `browser-use`).
- Automated UI testing with minimal resource usage.

## Strengths
- Built from scratch in Zig for performance and safety.
- Significantly lower resource usage than Chromium.
- Designed specifically for agentic/automated interactions rather than human browsing.

## Limitations
- Newer project, so it may lack some edge-case compatibility of mature engines.
- Smaller ecosystem of plugins/extensions compared to Chrome.

## When to use it
- When running browser agents at scale where memory and CPU overhead are bottlenecks.
- When you want a "clean" browser environment optimized for machine interaction.

## When not to use it
- If your task requires specific Chrome extensions or proprietary web features.
- If you need 100% pixel-perfect human-style rendering for visual debugging.

## Licensing and cost
- **Open Source**: Yes (check repo for specific license)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
Lightpanda can be installed via a one-line script or run as a Docker container.

```bash
# One-line installer (Linux/macOS)
curl -fsSL https://pkg.lightpanda.io/install.sh | bash

# Running via Docker (exposed on CDP port 9222)
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

### Hello World (CLI)
Fetch a page and dump it as Markdown directly from the terminal:

```bash
lightpanda fetch --dump markdown https://example.com
```

## CLI examples
The Lightpanda CLI is designed for direct machine interaction and scraping.

```bash
# Dump page as HTML
lightpanda fetch --dump html https://news.ycombinator.com

# Execute a custom script on a page
lightpanda fetch --script "document.querySelectorAll('a').forEach(a => console.log(a.href))" https://example.com

# Start a CDP server for external tools (Playwright/Puppeteer)
lightpanda server --host 127.0.0.1 --port 9222
```

## API examples
Lightpanda is compatible with the **Chrome DevTools Protocol (CDP)**, allowing it to be used as a drop-in replacement for Chrome in many automation frameworks.

### Connecting with Playwright (Python)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Connect to a running Lightpanda instance
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.new_context().new_page()
    page.goto("https://lightpanda.io")
    print(page.title())
    browser.close()
```

### Direct CDP Interaction (Node.js)
```javascript
const CDP = require('chrome-remote-interface');

async function example() {
    let client;
    try {
        client = await CDP({ port: 9222 });
        const {Page, Runtime} = client;
        await Page.enable();
        await Page.navigate({url: 'https://example.com'});
        await Page.loadEventFired();
        const result = await Runtime.evaluate({expression: 'document.title'});
        console.log(result.result.value);
    } catch (err) {
        console.error(err);
    } finally {
        if (client) { await client.close(); }
    }
}
example();
```

## Related tools / concepts
- [Browser Use](browser-use.md)
- [Playwright](https://playwright.dev/)
- [Puppeteer](https://pptr.dev/)
- [CDP (Chrome DevTools Protocol)](https://chromedevtools.github.io/devtools-protocol/)

## Sources / References
- [Official Website](https://lightpanda.io/)
- [GitHub Repository](https://github.com/lightpanda-io/browser)
- [Lightpanda Documentation](https://docs.lightpanda.io/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high

- [Lightpanda Browser (GitHub)](https://github.com/lightpanda-io/browser)
