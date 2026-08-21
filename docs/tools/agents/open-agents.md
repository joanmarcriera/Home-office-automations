# Open Agents

## What it is
Open Agents is an open-source framework and collection of deployable AI agents created by Vercel Labs. It is designed to enable "Computer Use" and "Web Use" capabilities, allowing autonomous agents to navigate the web, interact with authenticated SaaS applications, run code in sandboxes, and perform complex multi-step workflows. In early 2027, Open Agents serves as a foundational platform for building browser-native and serverless agents, offering full support for FastMCP 3.1, Vercel AI SDK 5.0, and multi-model execution across **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**.

## What problem it solves
It bridges the gap between static LLM text generation and interactive web-based software execution. Open Agents eliminates the complexity of managing persistent browser sessions, handling MFA and session tokens in agentic workflows, and providing visual feedback loops for computer-use tasks. By adopting FastMCP 3.1, it standardizes tool registration and task reporting, enabling web agents to communicate seamlessly with enterprise orchestrators.

## Where it fits in the stack
**Agent / Web Automation / Serverless Platform**. It functions as an orchestration layer that combines the Vercel AI SDK with headless browser controllers ([Playwright](../development_ops/playwright.md)) and isolated Vercel Sandbox execution environments.

## Typical use cases
- **Automated Web Intelligence Gathering**: Synthesizing data from multiple authenticated web applications into structured analytical reports.
- **SaaS Platform Administration**: Executing routine administrative and configuration workflows across platforms like HubSpot, Jira, Salesforce, or cloud consoles.
- **Dynamic Application Ingestion**: Extracting and structuring deep content from dynamic, single-page web applications without fixed APIs.
- **Serverless Agentic Workflows**: Deploying ephemeral agents that execute shell scripts and browser actions within isolated Vercel Sandboxes.
- **Cross-System Task Execution**: Receiving tasks via FastMCP 3.1 endpoints and returning structured output to parent agent harnesses.

## Strengths
- **Vercel Ecosystem Native**: Deep integration with Next.js 16, Vercel AI SDK, and Vercel Functions / Sandboxes.
- **Robust Computer Use Capabilities**: Built-in design patterns for high-fidelity browser navigation, visual DOM positioning, and screenshot verification.
- **Serverless & Ephemeral Architecture**: Optimized for running inside low-latency edge and serverless environments without requiring dedicated VM clusters.
- **Frontier & Open Model Support**: Optimized for native Computer Use APIs in Claude 5.1 and GPT-5.5, with full support for open models like **DeepSeek-V4** and **Llama 4**.
- **Modular Skill Extensions**: Composable architecture allowing developers to grant granular skills (e.g., search, email dispatch, browser interaction).

## Limitations
- **DOM Fragility**: Performance can degrade if target application user interfaces undergo structural changes without corresponding selector updates.
- **Navigation Latency**: Multi-turn browser reasoning loops are inherently slower than direct REST/gRPC API invocations.
- **Serverless Resource Limits**: Running resource-intensive headless browser sessions inside serverless functions requires careful memory and timeout management.

## When to use it
- When building web-accessible agentic products that must perform actions on behalf of users across third-party websites.
- When extending Next.js applications with native agentic workflows using the Vercel AI SDK.
- When seeking an open-source, deployable alternative to proprietary computer-use cloud services.

## When not to use it
- When official, well-supported APIs exist for the target service (direct API calls should always be preferred over UI manipulation).
- For pure web scraping tasks where dedicated crawlers like [Firecrawl](../process_understanding/firecrawl.md) or [Crawl4AI](../process_understanding/crawl4ai.md) are more performant.
- When long-running, continuous local desktop state and native window controls are strictly required.

## Getting started
### Installation
Open Agents is typically integrated into a Next.js application template. Clone the official repository to initialize:

```bash
# Clone the open agents repository
git clone https://github.com/vercel-labs/open-agents
cd open-agents
npm install
```

### Basic Configuration
1. Create a `.env.local` file and add your provider keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `DEEPSEEK_API_KEY`).
2. Configure your Vercel Sandbox token if isolated shell execution is required.
3. Start the local development server: `npm run dev`.

## CLI examples
```bash
# Clone and set up the open agents workspace
git clone https://github.com/vercel-labs/open-agents
cd open-agents && npm install

# Start the local agent server interface
npm run dev

# Run automated browser test tasks in headless mode
npm test -- --headless

# Execute an agent task locally via the CLI test runner
npm run start-agent -- --task "Verify status of production deployments on Vercel Dashboard"
```

## API examples
Open Agents utilizes the Vercel AI SDK `generateText` or `streamText` functions paired with custom FastMCP tools. Example using the browser tool skill:

```typescript
import { generateText, tool } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

const result = await generateText({
  model: anthropic('claude-5-1-sonnet-20261022'),
  tools: {
    browser_navigate: tool({
      description: 'Navigate to a target URL and wait for DOM load',
      parameters: z.object({ url: z.string().url() }),
      execute: async ({ url }) => {
        // Implementation using Playwright
        return { screenshot: 'data:image/png;base64,...', pageContent: '...' };
      },
    }),
  },
  prompt: 'Go to the Vercel status page and check for any active incident reports.',
});
```

### Validation of Agent Action Sequences with Pydantic v2
This Python snippet parses and validates an agent's browser action sequence and execution telemetry using **Pydantic v2**:

```python
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class BrowserStep(BaseModel):
    step_id: int = Field(..., description="Chronological step index")
    action: str = Field(..., description="Executed action type (e.g., navigate, click, fill, screenshot)")
    target: Optional[str] = Field(None, description="Target DOM selector or screen coordinate")
    value: Optional[str] = Field(None, description="Input string value if applicable")

class OpenAgentSession(BaseModel):
    session_id: str = Field(..., description="Unique browser session identifier")
    task_description: str = Field(..., description="Task objective assigned to the agent")
    start_url: HttpUrl = Field(..., description="Initial target URL")
    steps: List[BrowserStep] = Field(default_factory=list, description="Sequence of browser actions executed")
    telemetry: Dict[str, Any] = Field(default_factory=dict, description="Session performance and token usage metrics")

def validate_agent_session(raw_json: str) -> Optional[OpenAgentSession]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2 model_validate
        return OpenAgentSession.model_validate(data)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload.")
        return None
```

## Related tools / concepts
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — Core agent integration SDK.
- [Playwright](../development_ops/playwright.md) — Underlying headless browser engine.
- [Stagehand](../automation_orchestration/stagehand.md) — AI web automation framework.
- [Claude Code](../development_ops/claude-code.md) — Reference terminal agent harness.
- [Browser Use](../automation_orchestration/browser-use.md) — Web browser agent library.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open tool communication standard.
- [Crawl4AI](../process_understanding/crawl4ai.md) — High-throughput web extraction library.
- [Firecrawl](../process_understanding/firecrawl.md) — Web extraction API platform.

## Sources / references
- [Vercel Labs Open Agents GitHub Repository](https://github.com/vercel-labs/open-agents)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Vercel Functions & Sandboxes Guide](https://vercel.com/docs/functions/sandboxes)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
