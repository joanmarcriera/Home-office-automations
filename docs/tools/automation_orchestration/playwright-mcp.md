# Playwright MCP Server

## What it is
The Playwright MCP Server is a Model Context Protocol (MCP) implementation that gives AI agents a "headless browser" interface. It allows agents to interact with web pages using Playwright, enabling them to browse the internet, interact with UIs, and extract data.

## What problem it solves
Most LLMs lack direct access to the web or can only "see" through screenshots. Playwright MCP provides structured access to the DOM and accessibility tree, allowing agents to navigate, click, and extract data reliably without needing a traditional REST API.

## Where it fits in the stack
**Agent Tooling / Automation**. It bridges the gap between AI reasoning and the interactive web. It often acts as a fallback when official [API Providers](../providers/index.md) are unavailable.

## Typical use cases
- **Web Scraping**: Extracting data from dynamic, JavaScript-heavy websites.
- **Automated Testing**: Writing and running end-to-end tests through a natural language interface.
- **Agentic Browsing**: Allowing an AI agent to perform tasks on a website (e.g., booking a flight, ordering groceries).
- **Dashboard Interaction**: Automating internal tools that don't have public APIs.

## Getting started

### Installation
The server is typically run via `npx` or as a persistent process.

```bash
# Run the server via npx
npx -y @modelcontextprotocol/server-playwright
```

### Configuration
To use it with a host like Claude Desktop, add it to your configuration file:

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

## Technical Patterns

### Tool Usage Example
Once connected, an agent can call tools like `playwright_navigate` and `playwright_click`:

```json
// Example call from an agent
{
  "name": "playwright_navigate",
  "arguments": {
    "url": "https://news.ycombinator.com"
  }
}
```

### Accessibility Tree Focus
Unlike vision-based agents, this MCP server emphasizes the **Accessibility Tree**. This provides the agent with a semantic understanding of the page elements (e.g., "Login button" vs "Rectangle at 100,200"), which significantly improves reliability.

## Deployment Options

### Local Mode
Runs on your local machine, allowing the agent to access your local network and authenticated browser sessions (if configured).

### Containerized Mode
Running the server in [Docker](../infrastructure/docker.md) provides a clean, sandboxed environment for browser sessions:

```bash
docker run -i --rm mcr.microsoft.com/playwright:v1.49.0-noble npx -y @modelcontextprotocol/server-playwright
```

## Strengths
- **Accessibility Tree Focus**: Uses structural data rather than pixels, making it faster and more reliable than vision-based browsing.
- **Cross-Browser Support**: Supports Chromium, Firefox, and WebKit.
- **Standardized Protocol**: Integrates seamlessly with any MCP host (Claude Desktop, etc.).
- **JavaScript Execution**: Can run custom JS in the browser context for complex interactions.

## Limitations
- **Latency**: Browser automation is inherently slower than direct API calls.
- **Anti-Bot Detection**: Headless browsers are easily detected by advanced security systems like Cloudflare or Akamai.
- **Resource Intensive**: Running a browser instance consumes significant CPU and Memory compared to other MCP servers.

## When to use it
- When an AI agent needs to interact with a website that does not have an official API.
- For "self-healing" automation scripts that can adapt to UI changes.
- When you need a "web agent" that can perform multi-step interactions (login, search, filter, export).

## When not to use it
- When a stable REST or GraphQL API is available.
- For high-frequency data extraction where speed and cost are critical.
- If you are operating in an environment with low memory or restricted outbound internet access.

## Related tools / concepts
- [Playwright](../development_ops/playwright.md)
- [Model Context Protocol (MCP)](mcp.md)
- [Browser Use](browser-use.md)
- [Stagehand](stagehand.md)
- [Skyvern](skyvern.md)
- [Claude Code](../development_ops/claude-code-setup.md)
- [OpenHands](../development_ops/openhands.md)
- [Puppeteer](../development_ops/puppeteer.md)

## Sources / references
- [Playwright MCP GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)
- [MCP Official Documentation](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
