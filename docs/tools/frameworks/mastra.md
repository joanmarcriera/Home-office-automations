# Mastra

## What it is
Mastra is an open-source framework designed to help developers build, deploy, and manage AI agents. It focuses on providing a unified platform for agent orchestration, tool integration, and observability.

## What problem it solves
It addresses the challenges of fragmented AI development by offering a cohesive set of tools for building reliable agents, connecting them to various data sources and APIs, and monitoring their performance.

## Where it fits in the stack
**Framework / Agent Platform**.

## Typical use cases
- **Agentic Workflows**: Building complex multi-step workflows that can be monitored and managed.
- **TypeScript-Native Agents**: Ideal for teams working with a modern TypeScript/Next.js stack.
- **Enterprise Agent Platforms**: Providing a unified platform for multi-agent systems with built-in observability.

## Strengths
- **Unified Platform**: Combines orchestration, tools, and monitoring in a single framework.
- **Focus on Reliability**: Provides features for building robust and predictable AI agents.
- **Developer Experience**: Designed to be easy for developers to integrate into their existing workflows.

## Limitations
- **Newer Framework**: The ecosystem of pre-built integrations is still being established.
- **Platform Overhead**: Introduces its own concepts and patterns that developers must learn.

## When to use it
- When you want a complete platform for building and managing AI agents.
- When you value built-in observability and monitoring for your AI applications.

## When not to use it
- For quick, one-off AI experiments where a lighter framework might be faster.
- If you already have established tools for orchestration and monitoring.

## Getting started

### Installation
```bash
npx create-mastra@latest
```

### Basic Example (Manual Setup)
```typescript
import { Mastra, Agent } from '@mastra/core';

const agent = new Agent({
  name: 'Assistant',
  instructions: 'You are a helpful assistant.',
  model: {
    provider: 'OPEN_AI',
    name: 'gpt-4',
  },
});

const mastra = new Mastra({
  agents: [agent],
});

const response = await agent.generate('Tell me about Mastra.');
console.log(response.text);
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 License)
- **Cost**: Free
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

## Sources / References
- [Official Website](https://mastra.ai/)
- [GitHub](https://github.com/mastra-ai/mastra)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
