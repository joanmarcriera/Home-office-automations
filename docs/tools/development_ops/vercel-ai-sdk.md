# AI SDK (by Vercel)

## What it is
The AI SDK (v4+) is a TypeScript toolkit designed to help developers build AI-powered applications and agents with React, Next.js, Vue, Svelte, Node.js, and more. It provides a unified API for interacting with 20+ LLM providers and building generative user interfaces.

## What problem it solves
It standardizes the integration of Large Language Models (LLMs) across multiple providers (OpenAI, Anthropic, Gemini, DeepSeek, etc.), reducing the technical overhead and boilerplate code required to build AI-driven features like streaming chat, structured data extraction, and autonomous agents.

## Where it fits in the stack
**Category**: Development & Ops / AI App SDK. It sits at the **Application Layer**, bridging the gap between frontier models and user interfaces.

## Typical use cases
- **AI Chat Interfaces**: Building responsive, streaming chat components in Next.js or React.
- **Generative UI**: Creating user interfaces that change dynamically based on LLM outputs (e.g., streaming components via AI RSC).
- **Autonomous Agents**: Implementing multi-step tool-calling loops and agentic workflows using `generateText` and `streamText`.
- **Structured Data Extraction**: Using `generateObject` or `streamObject` to extract type-safe JSON from natural language.

## Strengths
- **Framework Agnostic**: Works across React, Next.js, Vue, Svelte, Nuxt, and Node.js.
- **Unified Provider API**: Swap between OpenAI, Anthropic, Gemini, and Groq with a single line change.
- **Agent Primitives**: Native support for tool calling, JSON mode, and Zod schema validation.
- **First-Class Streaming**: Built-in support for real-time token streaming and progressive delivery.
- **AI RSC Support**: Specialized hooks and primitives for streaming React Server Components.
- **Observability**: Built-in OpenTelemetry instrumentation for monitoring and tracing.

## Comparison: AI SDK vs. TanStack AI
- **AI SDK**: Best for full-stack AI applications. Treats AI development as a cohesive problem, providing agent abstractions, multi-modal primitives, and deep Vercel/Next.js integration.
- **TanStack AI**: Best for library-focused composition. Prioritizes per-model type inference and minimal bundle footprints, following the design principles of TanStack Query.

## When to use it
- When building production-grade AI web applications with TypeScript that require multi-provider support.
- When needing to ship complex "Streaming + Tool Use" patterns (e.g., RAG pipelines or research agents).
- When looking for the de facto standard in the Vercel/Next.js ecosystem.

## When not to use it
- In Python-only backend environments (use [Pydantic AI](../frameworks/pydantic-ai.md) or [LangChain](../frameworks/langchain.md)).
- If you require a library with a minimal bundle footprint for a simple single-provider project (consider [TanStack AI](https://tanstack.com/ai)).

## Limitations
- **TypeScript First**: Optimized primarily for TypeScript; JS support exists but is less ergonomic.
- **Rapid Versioning**: As of 2026, the ecosystem moves quickly (v4+), requiring developers to keep dependencies (like `ai` and `@ai-sdk/provider-utils`) updated to the latest canary for the newest features.

## Getting started

### Installation
```bash
npm install ai
```

### Basic Text Generation
```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

const { text } = await generateText({
  model: openai("gpt-4o"),
  prompt: "What is the best way to learn TypeScript?",
});
```

### Streaming Chat (Next.js)
```typescript
'use client';

import { useChat } from 'ai/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>{m.role}: {m.content}</div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

## Related tools / concepts
- [Vercel AI Gateway](../providers/vercel-ai-gateway.md)
- [LlamaIndex.TS](../ai_knowledge/llamaindex-ts.md)
- [LangChain](../frameworks/langchain.md)
- [Pydantic AI](../frameworks/pydantic-ai.md)
- [Model Context Protocol (MCP)](../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [Official Website](https://sdk.vercel.ai/)
- [GitHub Repository](https://github.com/vercel/ai)
- [Documentation](https://sdk.vercel.ai/docs/introduction)
- [Vercel AI SDK vs TanStack AI](https://vercel.com/kb/guide/vercel-ai-sdk-vs-tanstack-ai)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
