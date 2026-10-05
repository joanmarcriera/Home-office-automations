# Pizza Bot

## What it is
Pizza Bot is an open-source, self-hosted application that gives AI agents an email-client-style inbox for background work. Agents run scheduled or webhook-triggered tasks, can delegate to specialised workers, and surface results (or approval requests) in the inbox. It was created by AWS developers Joseph Dolivo and Igor Fil as a community project, is licensed under Apache 2.0, and is not an AWS-supported product.

## What problem it solves
Most agent tooling is chat-first: the human must be present while the agent works. Pizza Bot targets "ambient" or background agents (a concept popularised by LangChain) by moving the interaction model to an asynchronous inbox, where work arrives, is triaged, and is approved or rejected when the human has time.

## Where it fits in the stack
**Agent / human-in-the-loop interface.** A client-server, local-first application that sits above model providers, MCP servers and Agent Skills, which it connects to as configured.

## Typical use cases
- Scheduled background tasks whose results are reviewed later in an inbox.
- Webhook-triggered agent runs.
- Delegating sub-tasks to specialised workers and tracking them in an activity panel.
- Approval gates where an agent must wait for a human decision before acting.

## Strengths
- Inbox UX with All, Unread and Action queues instead of a single chat thread.
- Supports multiple model providers, MCP servers and Agent Skills.
- Local-first: state, threads, checkpoints, attachments and logs are stored locally; prompts and attachments only go to the model providers and MCP servers the user enables.
- Apache 2.0 licensed.

## Limitations
- Community project with no AWS support or SLA.
- The operator is responsible for deployment, backups and updates.
- Reported only via a news article at the time of writing; maturity and feature depth were not independently verified.

## When to use it
- When you want agents to work asynchronously and review results in batches.
- When you need explicit human approval gates and want data kept on your own machine.

## When not to use it
- When you need a vendor-supported product with an SLA.
- For interactive, low-latency chat or pair-programming workflows.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free software; model-provider usage billed separately by whichever providers you configure
- **Self-hostable**: Yes

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - protocol Pizza Bot uses to reach tool servers.
- [Claude Code](../development_ops/claude-code.md) - CLI coding agent, an interactive counterpart to background agents.
- [Agents overview](index.md)

## Sources / References
- [InfoQ: Pizza Bot, Open-Source Inbox for Background AI Agents (2026-10-04)](https://www.infoq.com/news/2026/10/pizza-bot-ai-agents/)
- [GitHub: pizza-bot-app/pizza-bot](https://github.com/pizza-bot-app/pizza-bot) (linked from the InfoQ article; not fetched directly)

## Contribution Metadata
- Last reviewed: 2026-10-05
- Confidence: medium
