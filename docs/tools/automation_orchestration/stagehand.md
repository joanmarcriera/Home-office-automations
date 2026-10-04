# Stagehand

## What it is
Stagehand is an open-source, AI-native browser automation framework maintained by Browserbase. Designed specifically for autonomous agents and frontier vision-language models (such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Qwen 3.6 VL**, and **DeepSeek-V4**), Stagehand acts as a semantic abstraction layer over Playwright. Instead of relying on rigid, fragile CSS selectors or XPath expressions, Stagehand allows agents to interact with web applications using natural language intent, visual spatial understanding, and automated DOM self-healing.

As of early 2027, Stagehand natively implements the **FastMCP 3.1 Task Protocol** specification, enabling low-latency, cross-process tool binding across distributed multi-agent systems.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                            AGENT ORCHESTRATION LAYER                              │
│         (Claude 5.6 / GPT-5.6 / FastMCP 3.1 Client / LangGraph / AG2)            │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                                         │ Natural Language Intent
                                         │ & Zod / Pydantic Schemas
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                STAGEHAND ENGINE                                   │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐  │
│  │   page.act()          │  │   page.extract()      │  │   page.observe()      │  │
│  │ Semantic Interactions │  │ Zod Schema Parsing    │  │ Intent Grounding      │  │
│  └───────────┬───────────┘  └───────────┬───────────┘  └───────────┬───────────┘  │
│              └──────────────────────────┼──────────────────────────┘              │
│                                         │                                         │
│                    ┌────────────────────▼────────────────────┐                    │
│                    │     AI Vision & Element Resolver      │                    │
│                    │   (LLM/LMM DOM & Spatial Mapping)    │                    │
│                    └────────────────────┬────────────────────┘                    │
└─────────────────────────────────────────┼─────────────────────────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │                                               │
┌─────────────────▼───────────────────────┐   ┌───────────────────▼─────────────────┐
│          LOCAL PLAYWRIGHT               │   │      BROWSERBASE CLOUD              │
│      (Chromium / WebKit / Firefox)      │   │  (Scalable Session Infrastructure,  │
│                                         │   │   Proxy Rotation, Session Replays) │
└─────────────────────────────────────────┘   └─────────────────────────────────────┘
```

## What problem it solves
Traditional browser automation tools (including standard Playwright, Selenium, and Puppeteer) are inherently fragile when interacting with modern web applications. Web UIs change frequently due to continuous integration deployment pipelines, A/B testing variations, dynamic class name obfuscation (e.g., Tailwind or CSS Modules), and complex JavaScript single-page application (SPA) rendering.

Stagehand solves these challenges by introducing three fundamental capabilities:
1. **Intent-Based Execution (`act`)**: Agents execute browser actions by stating intent (e.g., "Click the submit order button") rather than supplying exact DOM selectors. Stagehand resolves the target element dynamically using multimodal spatial intelligence and DOM structure inspection.
2. **Structured Extraction (`extract`)**: Extracts complex structured data directly from arbitrary web pages into verified TypeScript Zod or Python Pydantic schemas without writing DOM traversal parsers.
3. **DOM Self-Healing & Resilience**: When web UI class names or layout hierarchies change, Stagehand's AI visual grounding automatically recalculates element locations without requiring code updates.

## Where it fits in the stack
Stagehand operates in **Layer 5: Automation & Orchestration Infrastructure**, bridging high-level LLM agent orchestrators and underlying browser execution runtimes.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                  LAYER 6: AGENT & MULTI-AGENT ORCHESTRATORS                       │
│             (Agno / Bee Agent Framework / CrewAI / LangGraph / AutoGen)           │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │ FastMCP 3.1 Tool Invocation
┌────────────────────────────────────────▼──────────────────────────────────────────┐
│              LAYER 5: AUTOMATION & WEB BROWSER ORCHESTRATION                      │
│   ┌───────────────────────────────────────────────────────────────────────────┐   │
│   │                               STAGEHAND                                   │   │
│   │      (Semantic Navigation / Act / Extract / Observe / FastMCP 3.1)       │   │
│   └────────────────────────────────────┬──────────────────────────────────────┘   │
└────────────────────────────────────────┼──────────────────────────────────────────┘
                                         │ CDP (Chrome DevTools Protocol)
┌────────────────────────────────────────▼──────────────────────────────────────────┐
│                   BROWSER RUNTIME & INFRASTRUCTURE LAYER                          │
│     ┌───────────────────────────────────┐   ┌───────────────────────────────┐     │
│     │     Playwright Local Chromium     │   │   Browserbase Cloud Browsers  │     │
│     └───────────────────────────────────┘   └───────────────────────────────┘     │
└───────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases

### 1. Autonomous Agent Web Operations
Enabling AI agents to execute end-to-end multi-step tasks across third-party web portals, such as booking flight reservations, filling out complex healthcare enrollment forms, or procuring enterprise inventory.

### 2. Resilient E2E UI Test Automation
Building end-to-end software testing pipelines that test functional user intent rather than rigid DOM IDs. Test scripts remain passing even when developers refactor UI layouts or switch frontend component libraries.

### 3. Dynamic Web Data Harvesting
Extracting tabular or nested datasets from complex, heavily obfuscated single-page web applications (SPAs) where conventional HTML scraping fails due to dynamic shadow DOMs or client-side JavaScript rendering.

### 4. Legacy ERP and CRM Integration
Automating repetitive data entry or extraction workflows across legacy enterprise portals that lack REST or GraphQL APIs, replacing manual data entry teams with resilient autonomous agent workers.

## Strengths
- **Semantic Element Resolution**: Interacts with web components based on natural language intent, visual context, and spatial position, eliminating script breakage from CSS changes.
- **Native Browserbase Cloud Integration**: Scales instantly to thousands of concurrent headless or headed browser sessions with automated proxy management, captcha solving, and video session recording.
- **Multimodal Grounding**: Fully optimized for vision-language models (LMMs) like Claude 5.6 and Qwen 3.6 VL to perform precise visual bounding-box resolution on complex web interfaces.
- **Type-Safe Structured Output**: Guarantees type safety by enforcing schema constraints directly during data extraction (`page.extract`).
- **Shadow DOM & iFrame Navigation**: Handles nested iFrames, Shadow DOM trees, and custom web components without requiring manual frame switching code.

## Limitations
- **Inference Latency**: Resolving web elements via LLM visual reasoning adds latency per page action compared to instant CSS selector clicks.
- **Token API Costs**: Utilizing foundation vision models for element observation and extraction incurs token API costs per turn.
- **Browser Footprint**: Requires a full Chromium/Playwright instance runtime, making it memory-intensive compared to lightweight HTTP scraper engines like Crawl4AI.

## When to use it
- When building autonomous web agents that navigate dynamic, third-party web applications.
- When creating automated UI test suites that must survive frequent frontend design overhauls.
- When extracting structured JSON objects from complex JavaScript SPAs with shadow DOM elements.

## When not to use it
- For high-volume static HTML scraping where simple HTTP clients and HTML parsers (e.g., BeautifulSoup or Crawl4AI) achieve higher throughput.
- In ultra-low latency scenarios requiring sub-50ms DOM interactions on guaranteed stable internal UI selectors.
- In zero-budget environments where LLM API costs per browser step are prohibited.

## Getting started

### Installation
Install Stagehand via npm or yarn:

```bash
# Install Stagehand package
npm install @browserbase/stagehand@latest playwright
```

### Environment Configuration
Set required environment variables for your chosen LLM provider and Browserbase cloud access:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-proj-..."
export BROWSERBASE_API_KEY="bb_live_..."
export BROWSERBASE_PROJECT_ID="your-project-id"
```

### Basic Usage Example
Initialize Stagehand and perform a semantic browser interaction:

```typescript
import { Stagehand } from "@browserbase/stagehand";

async function run() {
  const stagehand = new Stagehand({
    env: "LOCAL", // "LOCAL" or "BROWSERBASE"
    modelName: "claude-3-5-sonnet-latest",
  });

  await stagehand.init();
  const page = stagehand.page;

  await page.goto("https://news.ycombinator.com");
  // Execute action by natural language intent
  await page.act("Click on the first article link related to artificial intelligence");

  await stagehand.close();
}

run();
```

## CLI examples

### 1. Initialize Stagehand Project Template
Scaffold a production Stagehand project with TypeScript configurations:

```bash
# Initialize project interactively
npx stagehand@latest init

# Verify installed CLI version
npx stagehand --version
```

### 2. Development Mode with Live Debugging
Run Stagehand scripts with live visual browser inspection and DOM logging:

```bash
# Execute Stagehand script in development mode
npx stagehand dev --script ./src/automation.ts --headed
```

### 3. Running Browserbase Cloud Execution
Trigger remote cloud browser execution across Browserbase infrastructure:

```bash
BROWSERBASE_API_KEY="bb_live_xxx" STAGEHAND_ENV="BROWSERBASE" npx tsx ./src/automation.ts
```

## API examples

### 1. Advanced TypeScript API with Structured Zod Extraction
Extract structured ecommerce pricing data using TypeScript and Zod schemas:

```typescript
import { Stagehand } from "@browserbase/stagehand";
import { z } from "zod";

const ProductSchema = z.object({
  title: z.string().describe("Name of the product"),
  price: z.string().describe("Current listing price"),
  inStock: z.boolean().describe("Stock availability indicator"),
  rating: z.number().optional().describe("User review score out of 5"),
});

const ExtractionResultsSchema = z.object({
  storeName: z.string(),
  products: z.array(ProductSchema),
});

async function extractCatalog() {
  const stagehand = new Stagehand({ env: "LOCAL" });
  await stagehand.init();

  const page = stagehand.page;
  await page.goto("https://example.com/store");

  // Semantic observation prior to extraction
  const observations = await page.observe("Find all product cards and pricing labels");
  console.log(`Observed ${observations.length} candidate elements`);

  // Perform type-safe extraction enforced by Zod
  const data = await page.extract({
    instruction: "Extract all featured products and store info from the page",
    schema: ExtractionResultsSchema,
  });

  console.log("Extracted Store Data:", JSON.stringify(data, null, 2));
  await stagehand.close();
}

extractCatalog();
```

### 2. FastMCP 3.1 Web Automation Protocol Server (Python & Pydantic v2)
Wrap Stagehand extraction pipelines inside a FastMCP 3.1 server with strict **Pydantic v2** validation:

```python
import json
import subprocess
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

mcp = FastMCP("stagehand-automation-gateway", version="3.1")

class ProductItem(BaseModel):
    title: str = Field(..., min_length=1, description="Product title")
    price: str = Field(..., description="Price text string")
    in_stock: bool = Field(default=True)

class ExtractionResponse(BaseModel):
    url: str = Field(..., description="Target URL processed")
    items: List[ProductItem] = Field(default_factory=list)

@mcp.tool(
    name="stagehand_web_extract",
    description="Execute Stagehand browser automation to extract structured items from target URL"
)
def stagehand_web_extract(url: str, prompt_instruction: str) -> str:
    """
    Executes a Node.js Stagehand script subprocess and validates extracted JSON payload via Pydantic v2.
    """
    cmd = ["node", "./dist/stagehand_runner.js", "--url", url, "--instruction", prompt_instruction]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        raw_output = result.stdout

        # Parse and validate with Pydantic v2
        parsed_json = json.loads(raw_output)
        validated_payload = ExtractionResponse.model_validate(parsed_json)
        return validated_payload.model_dump_json(indent=2)
    except subprocess.CalledProcessError as e:
        return f"Stagehand Execution Error: {e.stderr}"
    except ValidationError as e:
        return f"Extraction Schema Validation Failure: {e.errors()}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts
- [Playwright](../development_ops/playwright.md) — The underlying cross-browser execution engine.
- [Browser Use](browser-use.md) — Python-native agentic web navigation framework.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Asynchronous LLM-friendly web crawler and scraper.
- [Skyvern](skyvern.md) — Vision-guided web automation engine.
- [Model Context Protocol (MCP)](mcp.md) — Standardized tool connection protocol for FastMCP 3.1.
- [Local LLMs (Gemma 4)](../ai_knowledge/local_llms.md) — Local vision models for web observation.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural orchestration patterns for web agents.

## Sources / references
- [Stagehand GitHub Repository](https://github.com/browserbase/stagehand)
- [Browserbase Official Website](https://www.browserbase.com/)
- [Stagehand Documentation](https://docs.browserbase.com/stagehand)
- [FastMCP 3.1 Protocol Standard](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
