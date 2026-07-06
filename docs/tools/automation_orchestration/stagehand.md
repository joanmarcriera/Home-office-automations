# Stagehand

## What it is
Stagehand is a specialized library for "browser-use" automation, designed to make web interactions for AI agents reliable, resilient, and easy to script. As of July 2026, it is maintained by Browserbase and serves as a high-level abstraction over Playwright, specifically optimized for how frontier models like **Claude 4.8 Opus**, **GPT-5.5**, and **Gemma 3** perceive and interact with web pages using both text and vision.

## What problem it solves
Traditional web automation (vanilla Playwright, Selenium) is notoriously brittle, often breaking when CSS selectors or DOM structures change. Stagehand solves this by allowing agents to interact with elements based on semantic meaning and visual layout. It leverages LLMs to "heal" broken paths and interpret the UI dynamically, significantly reducing the maintenance overhead of web-based agentic workflows.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation. It sits between the LLM orchestration layer (like LangGraph or Agency Swarm) and the browser execution engine (Playwright/Browserbase), providing the "semantic bridge" for reliable navigation. In July 2026, it integrates with FastMCP 3.0 for ultra-low latency browser tool hosting.

## Typical use cases
- **Agentic Web Browsing**: Enabling an agent to perform multi-step tasks on arbitrary websites (e.g., "Find the cheapest direct flight to Tokyo in October").
- **Automated Data Extraction**: Scraping complex, dynamic SPAs (Single Page Applications) without pre-defined selectors.
- **Resilient E2E Testing**: Creating test suites that survive UI redesigns by focusing on user intent rather than technical implementation details.
- **Form Automation**: Automating complex enterprise software (ERP/CRM) that lacks official APIs.

## Strengths
- **LLM-Powered Resiliency**: Automatically adapts to UI changes using semantic element discovery.
- **Browserbase Native**: Deeply integrated with Browserbase for massive scaling and observability.
- **Vision Support**: Optimized for use with vision-capable models (LMMs) for improved spatial reasoning.
- **TypeScript First**: Provides excellent developer experience and type safety for complex automation logic.
- **Shadow DOM Support**: Handles modern web components and complex UI structures transparently.

## Limitations
- **Latency**: Semantic discovery and LLM-based reasoning introduce significant latency compared to raw CSS selectors.
- **Inference Costs**: Every "act" or "extract" call typically incurs LLM token costs.
- **Overhead**: Requires a full browser environment, making it heavier than simple HTTP-based scrapers.

## When to use it
- When automating websites with frequently changing UIs or obfuscated DOMs.
- When building autonomous agents that need to navigate the web like a human.
- When you want to combine the reliability of Playwright with the intelligence of Claude 4.8 or GPT-5.5.

## When not to use it
- For high-speed, high-volume scraping of static sites where direct API or simple CSS selectors suffice.
- In latency-critical paths where sub-second response times are required.
- If you have zero budget for LLM token usage for automation tasks.

## Getting started

### Installation
```bash
npm install @browserbase/stagehand
```

### Basic Usage
```typescript
import { Stagehand } from "@browserbase/stagehand";

const stagehand = new Stagehand({
  env: "LOCAL", // or "BROWSERBASE"
  apiKey: process.env.BROWSERBASE_API_KEY,
});

await stagehand.init();
const page = stagehand.page;

await page.goto("https://news.ycombinator.com");
// Perform a semantic action
await page.act("Find the first article about AI and click its comments link");
```

## CLI examples
```bash
# Initialize a new Stagehand project
npx stagehand init

# Run Stagehand in development mode with observability
npx stagehand dev

# Verify the installation and version
npx stagehand --version
```

## API examples
```typescript
import { Stagehand } from "@browserbase/stagehand";
import { z } from "zod";

const stagehand = new Stagehand();
await stagehand.init();

// Use natural language to extract structured data
const data = await stagehand.page.extract({
  instruction: "Extract the names and prices of all products on this page",
  schema: z.array(z.object({
    name: z.string(),
    price: z.string()
  })),
});

// Use 'observe' to find interactable elements semantically
const elements = await stagehand.page.observe("The 'Add to Cart' button for the premium plan");

await stagehand.close();
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md) — The underlying browser engine.
- [Browser Use](browser-use.md) — Python-based alternative for agentic browsing.
- [Skyvern](skyvern.md) — Visual-reasoning based automation platform.
- [Crawl4AI](../process_understanding/crawl4ai.md) — LLM-friendly web scraping library.
- [Local LLMs (Gemma 3)](../ai_knowledge/local_llms.md) — Canonical guide for vision-capable local models.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns for web agents.
- [Multi-On](../agents/multion.md) — Managed agentic browsing service.
- [Tavily](../providers/tavily.md) — Agentic search engine for data gathering.
- [Model Context Protocol](mcp.md) — For exposing browser capabilities to agents.

## Sources / references
- [Stagehand GitHub Repository](https://github.com/browserbase/stagehand)
- [Browserbase Website](https://www.browserbase.com/)
- [Stagehand Documentation](https://docs.browserbase.com/stagehand)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
