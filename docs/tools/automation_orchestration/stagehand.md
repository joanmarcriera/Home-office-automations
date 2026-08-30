# Stagehand

## What it is
Stagehand is an open-source library for agentic browser automation maintained by Browserbase. It provides a high-level, semantic abstraction layer over Playwright specifically optimized for how frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL** perceive, navigate, and interact with dynamic web pages. As of early 2027, Stagehand natively integrates with **FastMCP 3.1 Task Protocol** for low-latency tool hosting across agentic ecosystems.

## What problem it solves
Traditional web automation tools (like raw Playwright or Selenium) are notoriously fragile, frequently breaking when web page CSS selectors, DOM trees, or layout class names change. Stagehand solves this by enabling agents to interact with web elements based on natural language intent, semantic meaning, and visual context. It uses LLMs and vision models to self-heal broken interaction paths and visually reason over modern web UIs, drastically lowering maintenance costs for browser automation workflows.

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation Infrastructure. It sits between the high-level LLM agent orchestration layer (such as LangGraph, AG2, or FastMCP servers) and browser execution backends (Playwright or Browserbase cloud browsers), providing the semantic bridge for web navigation.

## Typical use cases
- **Autonomous Agent Web Browsing**: Enabling AI agents to perform complex multi-step web tasks (e.g., "Find direct flights to Tokyo under $1000 and fill out the passenger detail form").
- **Dynamic Data Extraction**: Scraping unstructured or complex Single Page Applications (SPAs) without pre-defining brittle CSS/XPath selectors.
- **Resilient E2E UI Testing**: Building end-to-end user experience test suites that survive UI redesigns by testing intent rather than brittle DOM IDs.
- **Legacy Enterprise UI Automation**: Automating interaction with legacy CRMs, ERPs, or internal portals that lack official REST/GraphQL APIs.

## Strengths
- **Semantic Element Discovery & Self-Healing**: Automatically locates and interacts with web components using natural language instructions, automatically adapting to DOM changes.
- **Browserbase Cloud Scaling**: Deep integration with Browserbase for massive parallel browser session execution, proxy rotation, and session replay recording.
- **Multimodal & Vision Reasoning**: Optimized for vision-capable frontier models (LMMs) for precise visual element grounding and spatial reasoning.
- **TypeScript First API**: Provides strong type safety, IDE autocompletion, and robust asynchronous error handling.
- **Shadow DOM & iFrame Support**: Transparently navigates complex modern web architectures including Web Components and Shadow DOM roots.

## Limitations
- **LLM Reasoning Overhead**: Natural language element resolution introduces additional latency compared to direct CSS selector clicks.
- **Inference Cost**: Utilizing LLMs for element discovery and structured extraction incurs token API costs per action.
- **Browser Runtime Footprint**: Requires running a full Playwright/Chromium browser engine, making it heavier than HTTP-based HTML parsers.

## When to use it
- When automating web applications with obfuscated, dynamic, or frequently changing user interfaces.
- When building autonomous web agents that navigate arbitrary websites like human users.
- When combining Playwright execution reliability with the visual intelligence of Claude 5.6, GPT-5.6, or Qwen 3.6 VL.

## When not to use it
- For high-speed, high-volume web scraping on static websites where direct HTTP requests or lightweight parsers (e.g., BeautifulSoup, Crawl4AI) suffice.
- In sub-second latency constraints where traditional CSS selectors can be guaranteed stable.
- When operating under strict zero-LLM-budget constraints.

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
// Perform a semantic action using natural language intent
await page.act("Find the first article discussing FastMCP 3.1 and click its comments link");
```

## CLI examples

```bash
# Initialize a new Stagehand project
npx stagehand init

# Run Stagehand in development mode with live debugging and observability
npx stagehand dev

# Verify current installed version of Stagehand CLI
npx stagehand --version
```

## API examples

### TypeScript API with Zod Schema Extraction
```typescript
import { Stagehand } from "@browserbase/stagehand";
import { z } from "zod";

const stagehand = new Stagehand();
await stagehand.init();

// Extract structured data semantically using Zod validation
const data = await stagehand.page.extract({
  instruction: "Extract the names, pricing tiers, and main features of products on this page",
  schema: z.array(z.object({
    name: z.string(),
    price: z.string(),
    features: z.array(z.string())
  })),
});

// Observe page elements semantically before interacting
const elements = await stagehand.page.observe("The 'Subscribe Now' button for enterprise plans");

await stagehand.close();
```

### Python: Validating Extraction Payloads with Pydantic v2
When running Stagehand in a Node.js microservice or FastMCP tool wrapper, Python orchestrators parse extracted JSON payloads. Enforcing strict **Pydantic v2** data contracts guarantees type safety before processing.

```python
import json
from typing import List
from pydantic import BaseModel, Field, ValidationError

class StagehandProductItem(BaseModel):
    name: str = Field(..., min_length=1, description="Extracted product name")
    price: str = Field(..., description="Extracted product price string (e.g. '$199/mo')")
    features: List[str] = Field(default_factory=list, description="Extracted feature list")

class StagehandExtractionPayload(BaseModel):
    items: List[StagehandProductItem] = Field(..., description="List of validated extracted products")

def validate_extraction_response(raw_json: str) -> StagehandExtractionPayload:
    """
    Validates raw JSON returned from Stagehand's extraction execution.
    """
    try:
        parsed = json.loads(raw_json)
        if isinstance(parsed, list):
            parsed = {"items": parsed}
        return StagehandExtractionPayload.model_validate(parsed)
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Extraction payload contract validation failed: {e}")
        raise

if __name__ == "__main__":
    extracted_output = '[{"name": "FastMCP 3.1 Gateway", "price": "$99/mo", "features": ["Task Protocol", "Low Latency"]}]'
    try:
        validated_data = validate_extraction_response(extracted_output)
        for product in validated_data.items:
            print(f"Verified Product: {product.name} ({product.price}) - Features: {len(product.features)}")
    except ValidationError:
        pass
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md) — The underlying browser engine.
- [Browser Use](browser-use.md) — Python framework for agentic web browsing.
- [Skyvern](skyvern.md) — Vision-reasoning browser automation platform.
- [Crawl4AI](../process_understanding/crawl4ai.md) — LLM-friendly web scraping library.
- [Local LLMs (Gemma 4)](../ai_knowledge/local_llms.md) — Canonical guide for vision-capable local models.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns for web agents.
- [MultiOn](../agents/multion.md) — Autonomous browser agent platform.
- [Tavily](../providers/tavily.md) — Agentic search engine for data gathering.
- [Model Context Protocol (MCP)](mcp.md) — Protocol standard for FastMCP 3.1 browser tool integration.

## Sources / references
- [Stagehand GitHub Repository](https://github.com/browserbase/stagehand)
- [Browserbase Official Site](https://www.browserbase.com/)
- [Stagehand Product Documentation](https://docs.browserbase.com/stagehand)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
