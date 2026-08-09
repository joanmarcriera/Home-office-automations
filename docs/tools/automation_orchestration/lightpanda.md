# Lightpanda Browser

## What it is
**Lightpanda** is a high-performance headless browser built from scratch in **Zig**, specifically architected for AI agents, web scraping, and scalable automation. Unlike most modern headless browsers, it is not a fork of Chromium, Blink, or WebKit. It uses its own lightweight engine to provide a massive performance boost for agentic workflows. As of late 2026, it is a preferred execution environment for [Gemma 3](../ai_knowledge/local_llms.md) based agents using the **FastMCP 3.1** protocol.

## What problem it solves
Traditional headless browsers (like Chrome) are extremely resource-intensive, often consuming 500MB+ of RAM per instance. Lightpanda provides a lightweight alternative that uses up to **9x less memory** and runs up to **11x faster** than Headless Chrome, making it possible to run hundreds of browser instances on modest hardware. It solves the scalability bottleneck for browser-based AI agents and high-frequency RAG ingestion pipelines.

## Where it fits in the stack
**Category**: Tool / Automation Orchestration / Browser Infrastructure. It serves as the "execution engine" for agents that need to navigate and interact with the web, sitting below orchestration layers like [Browser Use](browser-use.md) and [Skyvern](skyvern.md). It integrates natively with **FastMCP 3.1** for low-latency browser-tool interaction.

## Typical use cases
- **Agentic Web Navigation**: Powering agents that need to interact with complex SPAs (Single Page Applications).
- **High-Density Scraping**: Running massive parallel data extraction pipelines with minimal infrastructure costs.
- **AI Data Extraction**: Using the built-in `--dump markdown` feature to provide LLM-ready context from web pages.
- **Automated Testing**: Fast, low-latency UI testing in CI/CD pipelines.
- **RAG Ingestion**: Rapidly crawling and converting web content for vector database ingestion.

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
- **Extensions**: Does not support standard Chrome Extensions (.crx).

## When to use it
- When scaling browser-based AI agents where CPU/RAM costs are the primary bottleneck.
- For RAG pipelines that require high-velocity web content ingestion and Markdown conversion.
- When you need a "clean-room" browser environment for secure automation.
- For CI/CD environments where browser startup time is critical.

## When not to use it
- If your workflow depends on specific Chrome Extensions.
- For websites that require proprietary codecs (DRM) or extremely niche web standards.
- If you need 100% pixel-perfect visual rendering (e.g., for automated layout design audits).
- If you are targeting sites with extremely aggressive anti-bot protections that require specialized evasive browsers.

## Getting started
Lightpanda can be installed via a one-line script or run as a Docker container.

### Local Installation
```bash
# One-line installer (Linux/macOS)
curl -fsSL https://pkg.lightpanda.io/install.sh | bash
```

### Running via Docker
The most common way to use Lightpanda in agentic stacks is via Docker, exposing the CDP port (9222).
```bash
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

## CLI examples
The Lightpanda CLI is optimized for speed and integration into shell-based pipelines.

```bash
# Dump page as HTML with a 5-second wait for JS execution
lightpanda fetch --wait 5000 --dump html https://example.com

# Fetch a page and dump it as Markdown (perfect for LLM context)
lightpanda fetch --dump markdown https://news.ycombinator.com

# Execute a custom script and output the result
lightpanda fetch --script "Array.from(document.querySelectorAll('h1')).map(e => e.innerText)" https://example.com
```

## API examples
Lightpanda is compatible with the **Chrome DevTools Protocol (CDP)**, allowing it to work with standard libraries like Playwright. Below is an example that demonstrates how to extract page metadata using Playwright connected to Lightpanda, validated strictly against a **Pydantic v2** schema to ensure reliability in an AI agentic pipeline (utilizing models like Claude 5.1 or Gemini 4.0 Pro).

```python
import json
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from playwright.sync_api import sync_playwright

# 1. Define the Pydantic v2 data contract for scraped page metadata
class PageMetadata(BaseModel):
    title: str = Field(description="The Title of the webpage")
    canonical_url: Optional[str] = Field(None, description="The canonical URL link of the webpage")
    word_count: int = Field(default=0, description="Estimated word count of the main content")
    has_custom_zig_badge: bool = Field(default=False, description="Whether the page highlights Zig technology")

def scrape_and_validate(url: str) -> Optional[PageMetadata]:
    with sync_playwright() as p:
        try:
            # Connect to Lightpanda running on localhost:9222
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.new_context().new_page()
            page.goto(url)

            # Extract unstructured information via JavaScript
            title = page.title()
            canonical = page.locator("link[rel='canonical']").get_attribute("href") or None
            body_text = page.locator("body").inner_text() or ""
            words = len(body_text.split())
            zig_present = "zig" in body_text.lower()

            browser.close()

            # 2. Enforce strict Pydantic v2 validation
            raw_payload = {
                "title": title,
                "canonical_url": canonical,
                "word_count": words,
                "has_custom_zig_badge": zig_present
            }
            validated_metadata = PageMetadata.model_validate(raw_payload)
            return validated_metadata

        except ValidationError as ve:
            print(f"Data contract validation failed: {ve}")
        except Exception as e:
            print(f"Error during browser interaction or scraper: {e}")

    return None

if __name__ == "__main__":
    meta = scrape_and_validate("https://lightpanda.io")
    if meta:
        print(f"Successfully scraped and validated: {meta.title} (Words: {meta.word_count})")
```

## Related tools / concepts
- [Browser Use](browser-use.md) — Orchestration framework for LLMs to control Lightpanda.
- [n8n](../../services/n8n.md) — Automation platform with native Lightpanda nodes.
- [Skyvern](skyvern.md) — Browser automation agent that can leverage Lightpanda.
- [Playwright](../development_ops/playwright.md) — High-level API compatible with Lightpanda CDP.
- [MultiOn](../agents/multion.md) — Agentic browser API for autonomous web tasks.
- [Gemma 3](../ai_knowledge/local_llms.md) — High-performance local LLM often paired with Lightpanda for edge automation.
- [MCP (Model Context Protocol)](mcp.md) — The protocol used to expose Lightpanda capabilities to agents.
- [Claude Code](../development_ops/claude-code.md) — Agentic CLI that can utilize Lightpanda via MCP servers.

## Sources / references
- [Official Website](https://lightpanda.io/)
- [GitHub Repository](https://github.com/lightpanda-io/browser)
- [Lightpanda Documentation](https://docs.lightpanda.io/)
- [ScrapingBee: Lightpanda vs Chrome Headless](https://www.scrapingbee.com/blog/lightpanda-headless-browser/)

## Contribution Metadata
- Last reviewed: 2026-12-22
- Confidence: high
