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

## Getting started
The project is modular. You can clone specific agent templates from the Vercel Labs GitHub.

```bash
git clone https://github.com/vercel-labs/open-agents
cd open-agents
npm install
```

## Related tools / concepts

- [Browser Use](../automation_orchestration/browser-use.md)
- [Stagehand](../automation_orchestration/stagehand.md)
- [Cline](cline.md)
- [Claude Code](../development_ops/claude-code.md)
- [AI SDK (by Vercel)](../development_ops/vercel-ai-sdk.md)

## Sources / references
- [vercel-labs/open-agents](https://github.com/vercel-labs/open-agents)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)

## Contribution Metadata
- Last reviewed: 2026-05-16
- Confidence: high
