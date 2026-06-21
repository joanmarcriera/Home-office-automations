# Mastra

## What it is
Mastra is an open-source, TypeScript-native framework designed to help developers build, deploy, and manage AI agents. It focuses on providing a unified platform for agent orchestration, tool integration, and observability. As of June 2026, it has matured with **v1.8.0**, introducing advanced multi-agent coordination patterns and deeper workspace integration.

## What problem it solves
It addresses the challenges of fragmented AI development in the TypeScript ecosystem. Mastra provides a cohesive set of tools for building reliable agents, connecting them to various data sources via **MCP**, and monitoring their performance. It simplifies multi-agent coordination through first-class primitives like the **Supervisor Pattern** and provides high-performance infrastructure via the **Blaxel sandbox provider**.

## Where it fits in the stack
**Framework / Agent Platform / Orchestration Layer**.

## Typical use cases
- **Multi-Agent Coordination**: Orchestrating specialized agents (e.g., researcher + writer) using a central supervisor to delegate and evaluate completion.
- **Agentic Workflows**: Building complex, durable multi-step workflows with built-in error handling and tripwires.
- **Enterprise Observability**: Monitoring agent iterations, tool calls, and completion scores in real-time with native LSP diagnostics.
- **High-Performance Sandboxing**: Executing agent tools in secure, isolated environments via the **Blaxel provider**.

## Strengths
- **Supervisor Pattern**: Dedicated primitive for managing delegation, iteration tracking, and context isolation between agents.
- **Efficiency**: Supports **metadata-only vector queries**, enabling hybrid indexing and retrieval without the high cost of constant embedding generation.
- **Developer Experience**: Modern TypeScript-first design with built-in LSP diagnostics for real-time workspace feedback.
- **Flexible Deployment**: Native adapters for Express, Hono, Fastify, and Koa to expose agents as HTTP endpoints.

## Limitations
- **Ecosystem Maturity**: While rapidly growing, it is still newer than frameworks like LangChain or AutoGen, meaning fewer third-party community plugins.
- **TypeScript Only**: Primarily targeted at the Node.js/TypeScript ecosystem, which may exclude Python-heavy data science teams.

## When to use it
- When you want a complete, type-safe platform for building and managing multi-agent systems in TypeScript.
- When you value built-in observability and standardized patterns like the Supervisor Pattern.
- When you need to run agentic tools in secure, managed sandboxes (Blaxel).

## When not to use it
- For simple, one-off AI experiments where a lighter SDK is sufficient.
- If your primary development environment is Python.

## Getting started

### Installation
```bash
npx create-mastra@latest
```

### Basic Supervisor Setup
```typescript
import { Agent, Mastra } from '@mastra/core';

const supervisor = new Agent({
  name: 'Manager',
  instructions: 'Coordinate the researcher and writer.',
  model: { provider: 'OPEN_AI', name: 'gpt-4o' },
});

const mastra = new Mastra({
  agents: [researcher, writer],
  supervisor // Enables the Supervisor Pattern
});
```

## CLI examples

### Initializing a Project
```bash
mastra init my-agent-project
```

### Running the Dev Server
```bash
mastra dev
```

## API examples

### Metadata-Only Vector Query
```typescript
const results = await mastra.vector.query({
  collection: 'knowledge-base',
  query: 'June 2026 AI trends',
  metadataOnly: true // Hybrid retrieval without embeddings
});
```

### Using the Blaxel Sandbox
```typescript
const agent = new Agent({
  name: 'Coder',
  sandbox: 'blaxel', // Secure, high-performance sandbox
  tools: [codeInterpreter]
});
```

## Related tools / concepts
- [Phidata](../agents/phidata.md) — Assistant framework with memory.
- [LangGraph](langgraph.md) — Graph-based agent coordination.
- [CrewAI](crewai.md) — Multi-agent role-playing framework.
- [Agno](../agents/agno.md) — Rebranded Phidata.
- [AG2](ag2.md) — Universal agent runtime.
- [PydanticAI](pydantic-ai.md) — Python-based type-safe agents.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Native support in Mastra.
- [Rivet](rivet.md) — Visual agent design.

## Sources / References
- [Official Website](https://mastra.ai/)
- [Mastra Changelog](https://mastra.ai/blog/category/changelogs)
- [GitHub Repository](https://github.com/mastra-ai/mastra)

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-06-21)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
