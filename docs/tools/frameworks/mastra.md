# Mastra

## What it is
Mastra is an open-source framework designed to help developers build, deploy, and manage AI agents. It focuses on providing a unified platform for agent orchestration, tool integration, and observability. As of May 2026, it has reached **v1.8.0**, introducing advanced multi-agent coordination and comprehensive workspace tooling.

## What problem it solves
It addresses the challenges of fragmented AI development by offering a cohesive set of tools for building reliable agents, connecting them to various data sources and APIs, and monitoring their performance. It simplifies multi-agent orchestration through first-class patterns like the **Supervisor Pattern**.

## Where it fits in the stack
**Framework / Agent Platform**.

## Typical use cases
- **Multi-Agent Coordination**: Orchestrating specialized agents (e.g., researcher + writer) using a central supervisor to delegate and evaluate completion.
- **Agentic Workflows**: Building complex, durable multi-step workflows with built-in tripwires and error handling.
- **TypeScript-Native Agents**: Ideal for teams using TypeScript/Next.js who want a cohesive, type-safe agent stack.
- **Enterprise Observability**: Monitoring agent iterations, tool calls, and completion scores in real-time.

## Strengths
- **Supervisor Pattern**: Dedicated primitive for managing delegation, iteration tracking, and context isolation between agents.
- **Server Adapters**: Native adapters for Express, Hono, Fastify, and Koa to expose agents and tools as HTTP endpoints easily.
- **Developer Experience**: Modern TypeScript-first design with built-in LSP diagnostics for workspace edits.
- **Flexible Memory**: Supports metadata-only vector queries for hybrid indexing without embedding costs.

## Limitations
- **Learning Curve**: Introduces specific primitives (Mastra instances, Agents, Tools, Workflows) that require alignment with its architectural patterns.
- **Rapidly Evolving**: Frequent updates to core packages may require consistent dependency management.

## When to use it
- When you want a complete, type-safe platform for building and managing multi-agent systems.
- When you value built-in observability and standardized patterns for agent coordination.
- When you need to integrate agents into existing Node.js/TypeScript servers.

## When not to use it
- For quick, one-off AI experiments where a lighter framework might be faster.
- If you are not working in a TypeScript/JavaScript environment.

## Getting started

### Installation
```bash
npx create-mastra@latest
```

### Supervisor Pattern Example
```typescript
import { Agent, Mastra } from '@mastra/core';

const researcher = new Agent({ name: 'Researcher', ... });
const writer = new Agent({ name: 'Writer', ... });

const supervisor = new Agent({
  name: 'Manager',
  instructions: 'Coordinate the researcher and writer to produce a report.',
  model: { provider: 'OPEN_AI', name: 'gpt-4o' },
});

const mastra = new Mastra({
  agents: [researcher, writer],
  // The supervisor coordinates delegation and tracks iterations
});

const response = await supervisor.generate('Research and write about May 2026 AI trends.');
console.log(response.text);
```

### Server Adapter Example (Express)
```typescript
import express from 'express';
import { MastraServer } from '@mastra/express';
import { mastra } from './mastra';

const app = express();
const server = new MastraServer({ app, mastra });
await server.init();

app.listen(3001);
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 License)
- **Cost**: Free (OSS)
- **Self-hostable**: Yes

## Related tools / concepts
- [Phidata](../agents/phidata.md)
- [LangGraph](langgraph.md)
- [CrewAI](crewai.md)
- [Agno](../agents/agno.md)
- [Temporal](../orchestration/temporal.md)
- [PydanticAI](pydantic-ai.md)
- [AG2](ag2.md)
- [Smolagents](smolagents.md)
- [Rivet](rivet.md)

## Sources / References
- [Official Website](https://mastra.ai/)
- [Changelog](https://mastra.ai/blog/category/changelogs)
- [GitHub](https://github.com/mastra-ai/mastra)

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high
