# Open Agents

## What it is
Open Agents is a project by Vercel Labs focused on creating open-source, deployable AI agents that can perform various tasks across the web and integrated applications. It provides a blueprint for "Computer Use" and "Web Use" agents.

## What problem it solves
It provides a set of ready-to-use agents and a framework for building new ones, lowering the barrier to entry for developers wanting to integrate agentic capabilities into their apps. It bridges the gap between static LLM responses and actionable browser-based automation.

## Where it fits in the stack
**Category**: Agent / Web Automation

## Typical use cases
- **Web Automation**: Booking flights, managing SaaS dashboards, or scraping complex web apps.
- **Information Retrieval**: Synthesizing data from multiple authenticated web sources.
- **Task Orchestration**: Using an agent to "bridge" two apps that don't have a direct API integration.

## Vercel Labs Context
As a Vercel Labs project, Open Agents is optimized for:
- **Serverless Execution**: Designed to run in ephemeral environments.
- **Next.js Integration**: Easy to embed agentic chat or action interfaces into React/Next.js apps.
- **Streamlined Auth**: Patterns for managing user credentials for the sites the agent needs to visit.

## Strengths
- **Developer First**: Focuses on clean APIs and easy deployment to Vercel/Cloudflare.
- **Browser-Native**: Strong emphasis on reliable browser interaction (via Playwright or Puppeteer).
- **Composable**: Agents are built from modular "skills" that can be reused across different projects.

## Limitations
- **Security Overhead**: Requires careful management of session cookies and credentials.
- **Dynamic Web Failures**: Like all browser agents, it can break if the target website's UI changes significantly.

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
```

## Getting started
### Installation
The project is modular. You can clone specific agent templates from the Vercel Labs GitHub.

```bash
git clone https://github.com/vercel-labs/open-agents
cd open-agents
npm install
```

### Basic Usage
1. Set up your environment variables (OpenAI/Anthropic API keys).
2. Configure a `Vercel Sandbox` to execute code in isolated environments.
3. Use the pre-built `Computer Use` skill to automate browser tasks.

## API examples
Open Agents uses the Vercel AI SDK patterns for stream-based agent responses:

```typescript
import { generateText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: openai('gpt-4o'),
  tools: {
    browser_search: tool({
      description: 'Search the web using a headless browser',
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => { /* ... */ },
    }),
  },
  prompt: 'Find the latest price for AAPL stock.',
});
```

## Related tools / concepts
- [Browser Use](../automation_orchestration/browser-use.md)
- [Stagehand](../automation_orchestration/stagehand.md)
- [Cline](cline.md)
- [Claude Code](../development_ops/claude-code.md)
- [AI SDK (by Vercel)](../development_ops/vercel-ai-sdk.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)

## Sources / references
- [vercel-labs/open-agents](https://github.com/vercel-labs/open-agents)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Vercel Coding Agent Platform Template](https://vercel.com/templates/next.js/coding-agent-platform)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
