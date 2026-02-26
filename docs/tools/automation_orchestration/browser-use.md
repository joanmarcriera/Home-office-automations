# Browser Use

## What it is
Browser Use is an open-source framework that allows LLMs to interact with real browsers, enabling them to perform web-based tasks like form-filling, scraping, and application navigation.

## What problem it solves
It bridges the gap between static scraping (which fails on dynamic, JS-heavy sites) and manual browser automation, allowing agents to "see" and "interact" with the web just like a human would.

## Where it fits in the stack
**Infrastructure / Framework**. It provides the interface for agents to drive browsers via Playwright or similar drivers.

## Typical use cases
- **Complex Scraping**: Extracting data from authenticated or multi-step web processes.
- **Workflow Automation**: Automating tasks on web apps that lack official APIs.
- **Agent Testing**: Verifying browser-based agent behaviors.

## Strengths
- **Native MCP Support**: Can be used as an MCP server with Claude Desktop.
- **High Success Rate**: Reportedly high accuracy on benchmarks like WebVoyager.
- **Multi-LLM**: Works with any major LLM through standard providers.
- **Active Community**: Rapidly growing star count (78k+).

## Limitations
- **Overhead**: Driving a real browser is slower and more resource-intensive than API calls.
- **Cost**: High token consumption for vision-based or detailed DOM-reasoning tasks.
- **Fragility**: Still subject to breakage on massive UI changes, though more robust than traditional XPaths.

## When to use it
- When an application has no API but needs to be automated.
- For deep web research that requires multi-tab navigation or interactive sessions.

## When not to use it
- When a fast, stable REST API is available for the same task.
- For high-frequency, low-latency data extraction.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (Self-hosted)
- **Self-hostable**: Yes

## Related tools / concepts
- [Skyvern](skyvern.md)
- [Firecrawl](../process_understanding/firecrawl.md)
- [Playwright MCP Server](https://github.com/microsoft/playwright-mcp)

## Sources / References
- [GitHub](https://github.com/browser-use/browser-use)
- [Official Docs](https://docs.browser-use.ai/)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high
