# Lightpanda Browser

## What it is
Lightpanda is a high-performance headless browser built from scratch in **Zig**, specifically architected for AI agents, web scraping, and scalable automation. Unlike most modern headless browsers, it is not a fork of Chromium, Blink, or WebKit.

## What problem it solves
Traditional headless browsers (like Chrome) are extremely resource-intensive, often consuming 500MB+ of RAM per instance. Lightpanda provides a lightweight alternative that uses up to **9x less memory** and runs up to **11x faster** than Headless Chrome, making it possible to run hundreds of browser instances on modest hardware.

## Where it fits in the stack
**Category**: Tool / Automation Orchestration / Browser Infrastructure.

## Typical use cases
- **Agentic Web Navigation**: Powering agents that need to interact with complex SPAs (Single Page Applications).
- **High-Density Scraping**: Running massive parallel data extraction pipelines with minimal infrastructure costs.
- **AI Data Extraction**: Using the built-in `--dump markdown` feature to provide LLM-ready context from web pages.
- **Automated Testing**: Fast, low-latency UI testing in CI/CD pipelines.

## Strengths
- **Native Zig Implementation**: Extreme memory efficiency and execution speed.
- **CDP Compatibility**: Works as a drop-in replacement for many Playwright, Puppeteer, and `chromedp` workflows.
- **Built-in LLM Optimization**: Native support for dumping pages as Markdown or structured text.
- **V8 JavaScript Engine**: High compatibility with modern JavaScript despite the custom browser core.
- **Compliance**: Native `--obey-robots` flag for ethical scraping.

## Limitations
- **Beta Maturity**: As a "from-scratch" engine, some obscure CSS or JS features may still be in development.
- **Anti-Bot Detection**: While fast, it may be easier for advanced anti-bot systems to fingerprint than a full Chrome instance.
- **No GUI**: Strictly headless; no head-on mode for visual manual debugging.

## When to use it
- When scaling browser-based AI agents where CPU/RAM costs are the primary bottleneck.
- For RAG pipelines that require high-velocity web content ingestion.
- When you need a "clean-room" browser environment for secure automation.

## When not to use it
- If your workflow depends on specific Chrome Extensions (.crx files).
- For websites that require proprietary codecs (DRM) or extremely niche web standards.
- If you need 100% pixel-perfect visual rendering (e.g., for automated layout design audits).

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0 License).
- **Cost**: Free for self-hosted use.
- **Self-hostable**: Yes.

## Getting started

### Installation
Lightpanda can be installed via a one-line script or run as a Docker container.

```bash
# One-line installer (Linux/macOS)
curl -fsSL https://pkg.lightpanda.io/install.sh | bash

# Running via Docker (exposed on CDP port 9222)
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

### Basic Scraping
Fetch a page and dump it as Markdown directly from the terminal (perfect for LLM context):

```bash
lightpanda fetch --dump markdown https://news.ycombinator.com
```

## CLI examples
The Lightpanda CLI is optimized for speed and integration into shell-based pipelines.

```bash
# Dump page as HTML with a 5-second wait for JS execution
lightpanda fetch --wait 5000 --dump html https://example.com

# Execute a custom script and output the result
lightpanda fetch --script "Array.from(document.querySelectorAll('h1')).map(e => e.innerText)" https://example.com

# Take a screenshot of a specific element
lightpanda screenshot --selector "#main-content" --output screenshot.png https://example.com

# Start a CDP server for external tools
lightpanda server --host 0.0.0.0 --port 9222
```

## API examples
Lightpanda is compatible with the **Chrome DevTools Protocol (CDP)**.

### Connecting with Playwright (Python)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Connect to Lightpanda running on localhost:9222
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.new_context().new_page()
    page.goto("https://lightpanda.io")
    # Native Zig browser title
    print(f"Page Title: {page.title()}")
    browser.close()
```

### Direct CDP Interaction (Node.js)
Using the `chrome-remote-interface` library:
```javascript
const CDP = require('chrome-remote-interface');

async function scrape() {
    let client;
    try {
        client = await CDP({ port: 9222 });
        const {Page, Runtime} = client;
        await Page.enable();
        await Page.navigate({url: 'https://example.com'});
        await Page.loadEventFired();
        const {result} = await Runtime.evaluate({expression: 'document.body.innerText'});
        console.log(result.value);
    } finally {
        if (client) await client.close();
    }
}
```

## n8n / Make / Zapier Integration
As of May 2026, Lightpanda provides official nodes/integrations for major automation platforms:
- **n8n**: Use the "Lightpanda" node to perform high-speed web actions without a separate Selenium/Playwright cluster.
- **Make**: Integration via the Lightpanda Scraper API for serverless browser execution.
- **Zapier**: Connect Lightpanda to 6000+ apps for automated data extraction.

## Related tools / concepts
- [Browser Use](browser-use.md) — Orchestration framework for LLMs to control Lightpanda.
- [n8n](../../services/n8n.md) — Automation platform with native Lightpanda support.
- [Make](make.md) — Cloud automation with Lightpanda integration.
- [Zapier](zapier.md) — No-code automation.
- [Playwright](https://playwright.dev/) — High-level API compatible with Lightpanda CDP.
- [Zig](https://ziglang.org/) — The language Lightpanda is built with.

## Sources / References
- [Official Website](https://lightpanda.io/)
- [GitHub Repository](https://github.com/lightpanda-io/browser)
- [Lightpanda Documentation](https://docs.lightpanda.io/)
- [ScrapingBee: Lightpanda vs Chrome Headless](https://www.scrapingbee.com/blog/lightpanda-headless-browser/)

## Contribution Metadata
- Last reviewed: 2026-05-29
- Confidence: high
