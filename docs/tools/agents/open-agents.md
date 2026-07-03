# Open Agents

## What it is
Open Agents is an open-source framework and collection of deployable AI agents developed by Vercel Labs. It is designed to enable "Computer Use" and "Web Use" capabilities, allowing agents to navigate the web, interact with authenticated applications, and perform complex tasks across different software ecosystems. As of July 2026, it serves as a primary reference implementation for building autonomous browser-based agents that are optimized for serverless deployment and now features native support for the **MCP 3.0 Task Protocol**.

## What problem it solves
It bridges the gap between static LLM text generation and actionable web-based automation. Open Agents solves the complexity of managing browser sessions, handling authentication in agentic workflows, and providing a reliable feedback loop for "Computer Use" tasks. By adopting MCP 3.0, it also standardizes how web-based agents discover and execute tasks, making them more interoperable with other agentic systems.

## Where it fits in the stack
**Agent / Web Automation / Developer Platform**. It functions as an orchestration layer that combines the Vercel AI SDK with headless browser controllers (Playwright/Puppeteer) and sandboxed execution environments.

## Typical use cases
- **Automated Web Research**: Synthesizing data from multiple authenticated web sources into structured reports.
- **SaaS Task Execution**: Performing administrative tasks across platforms like HubSpot, Jira, or AWS Console.
- **Dynamic Data Ingestion**: Scraping and structuring data from complex, JavaScript-heavy web applications.
- **Computer-as-a-Service**: Deploying agents that can execute terminal and browser tasks in isolated Vercel Sandboxes.
- **Standardized Task Execution**: Using the MCP 3.0 Task Protocol to receive and report on tasks from parent orchestrators.

## Strengths
- **Optimized for Vercel Ecosystem**: Seamless integration with Next.js, Vercel AI SDK, and Vercel Functions.
- **Reliable Computer Use**: Built-in patterns for high-fidelity browser interaction and visual feedback processing.
- **Serverless Ready**: Designed to operate within ephemeral environments, minimizing infrastructure management.
- **Frontier Model Native**: Optimized for the latest "Computer Use" capabilities in Claude 4.8 Opus and GPT-5.5, while maintaining compatibility with **Gemma 3** for local/hybrid workflows.
- **Modular Skills**: Features a composable architecture where agents can be granted specific "skills" (e.g., search, email, browser).

## Limitations
- **UI Fragility**: Like all browser-based agents, performance can degrade if target websites undergo significant DOM changes.
- **Latency**: High-fidelity web navigation involves multiple reasoning steps, which can be slower than direct API calls.
- **Resource Intensive**: Running headless browsers in serverless environments can be more costly than standard API interactions.

## When to use it
- When building a web-accessible agent that needs to perform actions on the user's behalf across the internet.
- If you are already using the Vercel AI SDK and want to extend your assistant with "Computer Use" capabilities.
- When you need a deployable, open-source alternative to proprietary "Computer Use" platforms.

## When not to use it
- If a stable, well-documented API exists for the target service (prefer direct API integration).
- For simple web scraping tasks where a basic crawler like Firecrawl or Crawl4AI would be more efficient.
- In environments where persistent browser sessions and long-running local state are mandatory.

## Getting started
### Installation
Open Agents is typically integrated into a Next.js project. Clone the official template to get started:

```bash
# Clone the open agents repository
git clone https://github.com/vercel-labs/open-agents
cd open-agents
npm install
```

### Basic Configuration
1. Create a `.env.local` file and add your `ANTHROPIC_API_KEY` (for Claude 4.8 Opus) or `OPENAI_API_KEY` (for GPT-5.5).
2. Configure a Vercel Sandbox if you require isolated code execution.
3. Start the development server: `npm run dev`.

## CLI examples
```bash
# Clone the open agents repository
git clone https://github.com/vercel-labs/open-agents

# Install dependencies
npm install

# Start the local development server for the agent platform
npm run dev

# Run specific agent tests in headless mode
npm test -- --headless

# Running the agent locally for testing
npm run start-agent -- --task "Book a table for 2 at The Ivy in London"
```

## API examples
Open Agents utilizes the Vercel AI SDK `generateText` or `streamText` functions with specialized tools. Example using the browser skill:

```typescript
import { generateText, tool } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

const result = await generateText({
  model: anthropic('claude-4-8-opus-20260528'),
  tools: {
    browser_navigate: tool({
      description: 'Navigate to a URL and wait for the page to load',
      parameters: z.object({ url: z.string().url() }),
      execute: async ({ url }) => {
        // Implementation using Playwright
        return { screenshot: '...', content: '...' };
      },
    }),
  },
  prompt: 'Go to the Vercel status page and check for any active incidents.',
});
```

## Related tools / concepts
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — The core integration framework.
- [Playwright](../development_ops/playwright.md) — Underlying browser controller.
- [Stagehand](../automation_orchestration/stagehand.md) — Higher-level web agent framework.
- [Claude Code](../development_ops/claude-code.md) — Reference for agentic tool use.
- [Browser Use](../automation_orchestration/browser-use.md) — Alternative computer-use library.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Interoperability standard.
- [Crawl4AI](../development_ops/crawl4ai.md) — Optimized scraping alternative.
- [Firecrawl](../development_ops/firecrawl.md) — API-first web extraction.

## Sources / references
- [Vercel Labs Open Agents GitHub](https://github.com/vercel-labs/open-agents)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Vercel Sandbox Guide](https://vercel.com/docs/functions/sandboxes)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/task-protocol)

## Contribution Metadata
- Last reviewed: 2026-07-03
- Confidence: high
