# Playwright MCP Server

## What it is
The Playwright MCP Server is a Model Context Protocol (MCP) implementation that provides AI agents with a "headless browser" interface. As of June 2026, it is the primary tool for enabling frontier models like `claude-4-8-opus-20260528` and GPT-5.5 to interact with the live web, navigate complex SPAs (Single Page Applications), and perform multi-step browser-based tasks.

## What problem it solves
Most LLMs lack direct access to the web or can only "see" through static screenshots or text-only scrapers. Playwright MCP provides structured access to the DOM and the **Accessibility Tree**, allowing agents to click buttons, fill forms, and extract data from JavaScript-heavy sites reliably without needing a dedicated REST API.

## Where it fits in the stack
**Agent Tooling / Browser Automation**. It sits between the AI reasoning engine and the interactive web. It is often used as a fallback or "last mile" tool when official [API Providers](../providers/index.md) are unavailable or limited.

## Typical use cases
- **Dynamic Web Scraping**: Extracting data from sites that require JavaScript execution or user interaction.
- **Agentic Workflows**: Allowing an AI to perform tasks like booking travel, purchasing items, or managing SaaS dashboards.
- **Automated Testing**: Writing and running E2E tests through a natural language interface where the AI "explores" the UI.
- **Visual Verification**: Generating screenshots and PDFs of web pages for agentic review and reporting.

## Strengths
- **Accessibility Tree Focus**: Emphasizes semantic structure over raw pixels, making interaction faster and more robust against minor CSS changes.
- **Cross-Browser Support**: Leverages Playwright's native support for Chromium, Firefox, and WebKit.
- **Standardized Protocol**: Compatible with any MCP host (Claude Desktop, [Claude Code](../development_ops/claude-code-setup.md), etc.).
- **Sandboxed Execution**: Can be easily run in [Docker](../infrastructure/docker.md) to isolate browser sessions from the host system.

## Limitations
- **High Resource Usage**: Running a browser instance (even headless) consumes significantly more CPU and RAM than lightweight MCP servers.
- **Latency**: Each browser interaction (navigate, click, wait) introduces substantial delay compared to direct API calls.
- **Detection Risk**: Headless browsers are frequently flagged by anti-bot systems (Cloudflare, Akamai) without sophisticated stealth plugins.

## When to use it
- When an AI agent needs to perform actions on a website that lacks a public API.
- For "self-healing" automation where the agent can adapt to UI changes in real-time.
- When you need to extract data that is only visible after complex client-side state changes.

## When not to use it
- If a stable and documented REST/GraphQL API is available for the target service.
- For high-throughput scraping where the overhead of a full browser is prohibitive.
- In low-memory environments (e.g., small VPS or edge devices) where browser instances might cause OOM errors.

## Getting started

### Installation
The server can be run on-demand via `npx`:

```bash
# Run the Playwright MCP server
npx -y @modelcontextprotocol/server-playwright
```

### Configuration (Claude Desktop)
To enable the tool in Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-playwright"
      ]
    }
  }
}
```

## CLI examples

### Running via Docker
For a sandboxed environment with all dependencies pre-installed:

```bash
docker run -i --rm mcr.microsoft.com/playwright:v1.49.0-noble npx -y @modelcontextprotocol/server-playwright
```

### Manual Verification
You can test the server's basic connectivity using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-playwright
```

## API examples

### Agentic Tool Call (Conceptual)
When an agent uses the server, it issues JSON-RPC calls. Here is what a navigation call looks like:

```json
{
  "method": "tools/call",
  "params": {
    "name": "playwright_navigate",
    "arguments": {
      "url": "https://news.ycombinator.com"
    }
  }
}
```

### Performing a Click
An agent might then click the "new" link based on the accessibility tree:

```json
{
  "method": "tools/call",
  "params": {
    "name": "playwright_click",
    "arguments": {
      "selector": "text=new"
    }
  }
}
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md) — The underlying automation library.
- [Browser Use](browser-use.md) — A specialized library for LLM-browser interaction.
- [Stagehand](stagehand.md) — An AI-native web automation wrapper.
- [Skyvern](skyvern.md) — A platform for automating browser-based workflows.
- [Puppeteer](puppeteer.md) — The primary alternative to Playwright.
- [Claude Code](../development_ops/claude-code-setup.md) — A terminal-based agent that frequently uses this MCP.

## Sources / references
- [Playwright MCP GitHub Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)
- [Official MCP Documentation](https://modelcontextprotocol.io)
- [Playwright Official Documentation](https://playwright.dev)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
