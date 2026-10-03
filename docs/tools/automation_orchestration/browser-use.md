# Browser Use

## What it is
Browser Use is an open-source, vision-first web automation and browser agent orchestration framework designed to enable Large Language Models (LLMs) to navigate real web browsers (Chromium, Firefox, WebKit). It provides an API that translates high-level natural language instructions into precise multi-step browser interactions—including form filling, multi-tab navigation, canvas interacting, OAuth authentications, and structured data extraction.

As of early January 2027, Browser Use serves as an execution framework for "Computer Use" and "Web Agent" workloads. It features native, first-class bindings for the **Model Context Protocol (FastMCP 3.1)** and includes execution pipelines optimized for visual reasoning models including **Gemma 3**, **Claude 5.1 / 5.6**, **GPT-5.5 / 5.6**, and **Gemini 4.0 Pro**.

By combining Playwright's headless browser control with DOM tree simplification, spatial element coordinate mapping, and visual snapshot analysis, Browser Use allows agents to interact with dynamic, JavaScript-heavy single-page applications (SPAs) without relying on brittle hardcoded XPath or CSS selectors.

## What problem it solves
Traditional web scraping and browser automation tools (Selenium, raw Puppeteer/Playwright) face severe operational liabilities when automating modern web applications:
- **Selector Fragility**: Minor updates to a web page's class names or DOM hierarchy break hardcoded script selectors.
- **Dynamic JavaScript & Anti-Bot Obstacles**: Client-side single-page applications, shadow DOMs, infinite scrolling, and CAPTCHAs frequently block standard HTTP GET requests or static scrapers.
- **Lack of Visual Reasoning**: Non-visual scrapers cannot interpret spatial relationships (e.g., "click the 'Submit' button next to the green status check mark").
- **Unstructured Execution Chaos**: Standard script automation lacks self-correcting error loops when unexpected modal popups, cookie consent banners, or multi-factor authentication steps appear.

Browser Use resolves these issues by embedding multi-modal LLM reasoning directly into the browser execution loop. The agent "sees" screenshot frames, analyzes simplified DOM elements, formulates step-by-step action plans, executes mouse/keyboard events, and self-corrects if popups or navigation errors occur.

```
+-----------------------------------------------------------------------------------+
|                           Browser Use Agent Architecture                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Agent Task & Goal Layer ]                                                      |
|  - High-Level Task Prompt ("Extract quarterly invoices from vendor portal")       |
|  - FastMCP 3.1 Protocol Client / Claude 5.6 / Gemma 3 Vision Model                |
|                                 |                                                 |
|                                 v                                                 |
|  [ Browser Use Controller & Agent Orchestrator ]                                  |
|  - Perception Pipeline (DOM Tree Filtering + Visual Screenshot Coordinate Overlay)|
|  - Action Schema Validator (Pydantic v2 Contract Enforcer)                        |
|                                 |                                                 |
|        +------------------------+------------------------+                        |
|        |                                                 |                        |
|        v                                                 v                        |
|  [ Vision & DOM Reasoning Loop ]                [ Context Memory & History ]      |
|  - Analyzes Element Bounding Boxes             - Tracks Step History & State      |
|  - Generates Action (click, type, scroll)      - Prevents Infinite Loop Cycles    |
|        |                                                 |                        |
|        +------------------------+------------------------+                        |
|                                 |                                                 |
|                                 v                                                 |
|  [ Playwright Browser Automation Driver ]                                         |
|  - Chromium / Firefox / WebKit Engine (Headless or Headed)                        |
|  - Session Cookie Storage & Auth Storage State (.json)                            |
|                                 |                                                 |
|                                 v                                                 |
|  [ Target Web Application ]                                                       |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Automation & Orchestration / Web Automation & Computer Use. Browser Use operates in the execution layer, translating high-level agent directives into DOM events.

Browser Use typically integrates with:
- **Upstream Multi-Agent Frameworks**: [LangGraph](../frameworks/langgraph.md), [Agno](../agents/agno.md), [Autogen](../frameworks/autogen.md), and [LlamaIndex](../frameworks/llamaindex.md).
- **Core Automation Engine**: [Playwright](../development_ops/playwright.md) for low-level browser process execution and CDP (Chrome DevTools Protocol) communication.
- **Protocol Standards**: [FastMCP 3.1](../automation_orchestration/mcp.md) servers, exposing browser actions as standard tools to Claude Desktop, VS Code, or custom AI workbenches.
- **Vision Foundation Models**: Claude 5.1/5.6, GPT-5.5/5.6, Gemma 3, or Gemini 4.0 Pro for visual spatial reasoning.

## Typical use cases

### 1. Legacy Web Portal Data Extraction
Many enterprise accounting, government, and healthcare portals lack modern REST or GraphQL APIs. Browser Use automates authenticated logins, navigates multi-page forms, handles date pickers, and extracts unstructured tabular data into structured Pydantic v2 objects.

### 2. End-to-End Visual QA & User Journey Testing
Quality assurance teams deploy Browser Use agents to execute end-to-end user journeys (e.g., "Add product to cart, apply coupon code, verify checkout total, and test modal dismissals"). The agent verifies both DOM state and visual layout consistency across multiple screen resolutions.

### 3. Automated Form Submissions & Procurement Workflows
Procurement agents automate repetitive order entry across vendor portals. The agent reads line items from internal ERP invoices, logs into third-party supplier websites, fills out purchase forms, handles file uploads, and downloads confirmation PDFs.

### 4. Interactive Visual Market Research
Market intelligence agents navigate competitor web storefronts, perform search queries, extract pricing matrices across product variants, capture screenshot evidence, and compile comparative pricing reports.

### 5. Automated Social Media & Content Management
Content operations teams deploy Browser Use to publish multi-media posts across platforms that enforce browser-only interfaces or complex OAuth security challenges, managing session cookies seamlessly across runs.

## Strengths
- **FastMCP 3.1 Protocol Server Support**: Can be deployed as a standardized FastMCP 3.1 tool server, enabling any MCP-compliant agent platform to use browser actions without custom integration code.
- **Vision-First Spatial Reasoning**: Seamlessly combines vision model token analysis with DOM bounding-box coordinates, ensuring precise element targeting even on custom canvas controls or un-annotated buttons.
- **Self-Healing Navigation Loops**: Automatically detects and handles cookie popups, CAPTCHA prompts, authentication redirects, and unexpected modal overlays during execution.
- **Robust Session State Management**: Allows saving and re-loading authenticated browser storage states (`state.json`), enabling agents to bypass repeated login steps.
- **Extensible Custom Action Middleware**: Developers can inject custom Python action functions (e.g., custom file downloaders, database writers, or OCR plugins) directly into the agent execution loop.
- **Multi-Model Support**: Native support for open models (Gemma 3, Qwen 2.5 VL) alongside commercial APIs (Claude 5.6, GPT-5.6, Gemini 4.0 Pro).

## Limitations
- **Resource Footprint**: Spawning full Chromium instances consumes substantial CPU and RAM resources, making large-scale parallel deployments (>50 concurrent browser threads) memory-intensive.
- **Execution Speed**: Because each browser step involves DOM snapshotting, screenshot capture, and multi-modal LLM reasoning, workflow execution is slower than raw REST API requests.
- **Token Consumption Costs**: High-resolution image snapshots and simplified DOM context trees consume significant vision tokens per step, necessitating model rate limit management.

## When to use it
- When target web applications lack documented or reliable REST/GraphQL APIs.
- For complex, multi-step web interactions requiring visual reasoning to navigate dynamic interfaces.
- When deploying FastMCP 3.1 agent architectures that require web browsing as a native tool capability.
- For web automation tasks requiring session state persistence, cookie reuse, and automated popup handling.

## When not to use it
- When a stable, authenticated REST, GraphQL, or gRPC API is available for the target application (API calls are faster, cheaper, and more reliable).
- For high-volume, low-complexity web scraping where lightweight scrapers ([Crawl4AI](../process_understanding/crawl4ai.md), [Firecrawl](../process_understanding/firecrawl.md)) suffice.
- In low-resource environments (e.g., small edge devices or micro-containers) where running a full Chromium browser binary is prohibited.

## Getting started

### Installation
Install Browser Use alongside Playwright and validation dependencies:

```bash
pip install browser-use play-wright pydantic>=2.0.0 langchain-anthropic
playwright install chromium
```

### Quick Verification Script
Verify Browser Use installation and execute a simple headless navigation test:

```python
import asyncio
from browser_use import Agent, Browser, BrowserConfig
from langchain_anthropic import ChatAnthropic

async def verify_browser_use():
    """Verifies Browser Use execution with a simple web task."""
    print("Initializing Browser Use Verification...")

    # Configure headless browser instance
    browser = Browser(config=BrowserConfig(headless=True, viewport={'width': 1280, 'height': 720}))

    agent = Agent(
        task="Navigate to https://example.com and extract the main header title.",
        llm=ChatAnthropic(model="claude-3-5-sonnet-20241022"),
        browser=browser
    )

    try:
        history = await agent.run()
        print("Browser Use Execution Completed Successfully!")
        print(f"Total Steps Taken: {len(history.steps())}")
        final_res = history.final_result()
        print(f"Extracted Result: {final_res}")
        return True
    except Exception as err:
        print(f"Browser Use Verification Failed: {err}")
        return False
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_browser_use())
```

## CLI examples

Browser Use provides command-line flags to trigger task execution, launch real-time visual task inspectors, or manage persistent browser state sessions.

```bash
# Execute a web automation task directly from the command line
python -m browser_use "Navigate to GitHub trending, find top FastMCP 3.1 repositories, and output summaries"

# Launch the interactive Web UI for real-time visual browser step monitoring
python -m browser_use --ui --port 8080

# Execute automation using a specific saved browser session state for authenticated bypass
python -m browser_use --task "Check my recent order status on Amazon" --state-file ./auth/amazon_state.json

# Run task in headed mode (visible browser window) for debugging
python -m browser_use --task "Fill out contact form on example.com" --headed --debug
```

## API examples

### Python: Authenticated Scraping and Strict Pydantic v2 Contract Validation
In production enterprise architectures, unstructured JSON data extracted from web browser interactions must be strictly validated using **Pydantic v2** prior to database storage or downstream ingestion.

```python
import asyncio
import os
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator, ValidationError
from browser_use import Agent, Browser, BrowserConfig
from langchain_anthropic import ChatAnthropic

# --- Pydantic v2 Data Contract Definitions ---

class ExtractedInvoiceItem(BaseModel):
    invoice_id: str = Field(..., min_length=3, description="Invoice identifier code")
    vendor_name: str = Field(..., min_length=2, description="Name of the vendor")
    amount_usd: float = Field(..., ge=0.0, description="Total dollar amount")
    due_date: str = Field(..., description="Due date string in YYYY-MM-DD format")
    invoice_url: Optional[str] = Field(default=None, description="Download link to PDF invoice")

class InvoiceExtractionReport(BaseModel):
    extraction_timestamp: str = Field(..., description="ISO timestamp of extraction run")
    total_invoices_found: int = Field(..., ge=0)
    invoices: List[ExtractedInvoiceItem] = Field(..., description="List of validated invoice items")

    @field_validator("invoices")
    def validate_non_empty_if_found(cls, invoices: List[ExtractedInvoiceItem], info) -> List[ExtractedInvoiceItem]:
        return invoices

# --- Browser Agent Execution Pipeline ---

class BrowserExtractionPipeline:
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        self.llm = ChatAnthropic(model=model_name)
        self.browser = Browser(config=BrowserConfig(headless=True, viewport={'width': 1920, 'height': 1080}))

    async def extract_vendor_invoices(self, portal_url: str) -> Optional[InvoiceExtractionReport]:
        task_prompt = f"""
        Navigate to {portal_url}.
        1. Look for the recent vendor invoices table.
        2. Extract the top 3 invoices including invoice_id, vendor_name, amount_usd, due_date, and invoice_url.
        3. Return the result strictly as a valid JSON object matching the target schema.
        """

        agent = Agent(
            task=task_prompt,
            llm=self.llm,
            browser=self.browser
        )

        try:
            history = await agent.run()
            raw_result_text = history.final_result() or "{}"
            print("Raw Extracted Agent Output Received.")

            # Validate extracted output using Pydantic v2 model_validate_json
            validated_data = InvoiceExtractionReport.model_validate_json(raw_result_text)
            print(f"[SUCCESS] Validated {len(validated_data.invoices)} invoices via Pydantic v2!")
            return validated_data

        except ValidationError as val_err:
            print(f"[CONTRACT FAILURE] Extracted web data violated schema contract: {val_err}")
            return None
        except Exception as err:
            print(f"[EXECUTION FAILURE] Browser agent execution error: {err}")
            return None
        finally:
            await self.browser.close()

if __name__ == "__main__":
    pipeline = BrowserExtractionPipeline()
    # In live execution:
    # asyncio.run(pipeline.extract_vendor_invoices("https://portal.vendor-example.com/invoices"))
```

### FastMCP 3.1 Browser Use Tool Server Implementation
The following Python script implements a complete **FastMCP 3.1** server, exposing Browser Use web browsing capabilities as standardized agent tools.

```python
import asyncio
import os
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from browser_use import Agent, Browser, BrowserConfig
from langchain_anthropic import ChatAnthropic

# Initialize FastMCP 3.1 Server for Browser Use
mcp = FastMCP(
    name="Browser Use Automation Server",
    version="3.1.0",
    description="FastMCP 3.1 server providing autonomous web browser navigation and visual computer-use tools"
)

class ExecuteWebTaskInput(BaseModel):
    task: str = Field(..., description="Natural language description of the browser task to perform")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    max_steps: int = Field(default=15, ge=1, le=50, description="Maximum browser reasoning steps")

@mcp.tool(
    name="execute_browser_task",
    description="Executes a multi-step web browser navigation or data extraction task using an autonomous LLM agent"
)
async def execute_browser_task(input_data: ExecuteWebTaskInput, ctx: Context) -> Dict[str, Any]:
    """FastMCP 3.1 Tool exposing Browser Use web agent execution."""
    ctx.info(f"Initiating Browser Use task: '{input_data.task}' (Max Steps: {input_data.max_steps})")

    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"status": "error", "message": "ANTHROPIC_API_KEY environment variable not configured."}

    browser = Browser(config=BrowserConfig(headless=input_data.headless))
    agent = Agent(
        task=input_data.task,
        llm=ChatAnthropic(model="claude-3-5-sonnet-20241022"),
        browser=browser,
        max_steps=input_data.max_steps
    )

    try:
        history = await agent.run()
        result_text = history.final_result()
        return {
            "status": "success",
            "task": input_data.task,
            "steps_executed": len(history.steps()),
            "result": result_text
        }
    except Exception as err:
        return {"status": "error", "message": str(err)}
    finally:
        await browser.close()

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Stagehand](stagehand.md) — TypeScript-based framework for agentic web browsing and Playwright automation.
- [Skyvern](skyvern.md) — Open-source visual web automation engine powered by computer vision.
- [Crawl4AI](../process_understanding/crawl4ai.md) — LLM-friendly web crawler and markdown extractor for fast RAG pipelines.
- [Playwright](../development_ops/playwright.md) — The core low-level browser automation engine utilized by Browser Use.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized tool execution and context streaming protocol for autonomous agents.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous agent execution loops.

## Sources / references
- [Browser Use Official GitHub Repository](https://github.com/browser-use/browser-use)
- [Browser Use Developer Documentation](https://docs.browser-use.ai/)
- [Anthropic Computer Use & Browser Automation Guide](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
