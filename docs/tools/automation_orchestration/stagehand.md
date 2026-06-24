# Stagehand

## What it is
Stagehand is a high-level library designed for "browser-use" automation, specifically focused on making web interactions for AI agents reliable, resilient, and easy to script. In June 2026, it is the standard abstraction layer over Playwright, optimized for the way frontier models like **Claude 4.8 Opus** and **GPT-5.5** perceive and interact with web applications.

## What problem it solves
Traditional web automation (like vanilla Playwright or Selenium) is notoriously brittle; if a CSS selector changes or the DOM is restructured, the script breaks. Stagehand solves this by allowing agents to interact with elements based on semantic meaning and visual layout, using LLMs to "heal" selectors and understand the page structure in real-time, making automation resilient to UI updates.

## Where it fits in the stack
**Automation & Orchestration / Web Automation**. It sits between the agent's reasoning engine and the browser (Playwright), providing a semantic interface for web-based task execution.

## Typical use cases
- **Agentic Web Navigation**: Enabling an agent to perform complex, multi-step tasks like "Go to the AWS console, find the EC2 instance named 'Production', and upgrade its instance type."
- **Reliable Data Extraction**: Scraping dynamic, JS-heavy websites (e.g., social media, internal dashboards) without maintaining complex CSS selectors.
- **Automated QA Testing**: Creating E2E tests that describe user behavior in natural language, ensuring tests don't break on every minor frontend deployment.
- **Form Filling and Submission**: Automating complex checkout or registration processes where field IDs and labels change frequently.

## Strengths
- **Semantic Resiliency**: Uses LLMs to navigate and act on pages based on intent, rather than brittle DOM paths.
- **Playwright Foundation**: Built on the industry-standard Playwright engine, ensuring broad browser compatibility and performance.
- **Visual Grounding**: Highly optimized for use with multimodal (vision-capable) models for superior element discovery.
- **Simplified Developer Experience**: Reduces the lines of code required for complex interactions by an order of magnitude.

## Limitations
- **Inference Latency**: semantic element discovery adds overhead compared to direct CSS selection.
- **Token Usage Cost**: Requires continuous LLM calls for page reasoning and action validation.
- **Privacy Considerations**: Page metadata and occasionally screenshots are sent to the LLM provider for analysis.

## When to use it
- When building AI agents that need to perform actions (click, type, drag) on the live web.
- For automation tasks where the target website UI changes frequently or is highly dynamic.
- When you want to combine the reliability of Playwright with the semantic understanding of **Claude 4.8 Opus**.

## When not to use it
- For high-speed, high-volume scraping of static content where traditional tools like [Crawl4AI](../process_understanding/crawl4ai.md) or simple `fetch` calls are more efficient.
- If you have a zero-budget for LLM token usage (Stagehand requires inference for its core features).
- For simple automations on websites you control where stable CSS selectors can be maintained.

## Getting started

### Installation
Install the core Stagehand library and its dependencies:
```bash
npm install @browserbase/stagehand
```

### Basic Initialization
Initialize the Stagehand instance with your preferred environment:
```typescript
import { Stagehand } from "@browserbase/stagehand";

const stagehand = new Stagehand({
  env: "LOCAL", # Or "BROWSERBASE" for cloud execution
});

await stagehand.init();
```

## CLI examples

### Project Initialization & Management
```bash
# Initialize a new Stagehand project with a configuration scaffold
npx stagehand init

# Start the Stagehand visual development environment
npx stagehand dev

# Verify the current installation and dependencies
npx stagehand --version
```

## API examples

### Semantic Navigation and Action (June 2026)
Performing a complex web task using natural language instructions.

```typescript
const page = stagehand.page;
await page.goto("https://www.github.com/trending");

# Use 'act' for semantic interaction
await page.act("Find the first repository written in Rust and star it");

# Use 'extract' for structured data retrieval
const repoInfo = await page.extract({
  instruction: "Get the owner name and star count of the top 3 repositories",
  schema: z.array(z.object({
    owner: z.string(),
    stars: z.string()
  }))
});
```

### Observation and Reasoning
```typescript
# Observe the page to get a semantic summary for the agent
const observation = await page.observe({
  instruction: "Identify the main navigation links and the primary call-to-action button"
});
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md)
- [Browser Use](browser-use.md)
- [Skyvern](skyvern.md)
- [Lightpanda](lightpanda.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Multi-On](../agents/multion.md)
- [Tavily](../providers/tavily.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Stagehand Official Documentation](https://docs.browserbase.com/stagehand)
- [GitHub Repository](https://github.com/browserbase/stagehand)
- [Browserbase Blog: The Future of Browser-Use](https://www.browserbase.com/blog)
- [Playwright Project](https://playwright.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
