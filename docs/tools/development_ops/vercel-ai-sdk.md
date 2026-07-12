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

## Limitations
- **TypeScript First**: Optimized primarily for TypeScript; JS support exists but is less ergonomic.
- **Rapid Versioning**: As of July 2026, the ecosystem moves quickly (v4.x), requiring developers to keep dependencies (like `ai` and `@ai-sdk/provider-utils`) updated to the latest canary for the newest features.

## When to use it
- When building production-grade AI web applications with TypeScript that require multi-provider support.
- When needing to ship complex "Streaming + Tool Use" patterns (e.g., RAG pipelines or research agents).
- When looking for the de facto standard in the Vercel/Next.js ecosystem.

## When not to use it
- In Python-only backend environments (use [Pydantic AI](../frameworks/pydantic-ai.md) or [LangChain](../ai_knowledge/langchain.md)).
- If you require a library with a minimal bundle footprint for a simple single-provider project (consider [TanStack AI](https://tanstack.com/ai)).

## Getting started

### Installation
```bash
npm install ai @ai-sdk/openai
```

### Basic Setup
Create a `.env.local` file and add your API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## CLI examples
The AI SDK does not provide a standalone CLI, but it is often used in conjunction with the Vercel CLI for deployment and environment management.

### Initialize a Next.js AI Project
```bash
npx create-next-app@latest my-ai-app --example https://github.com/vercel/ai-chatbot
```

### Environment Setup
```bash
vercel env add OPENAI_API_KEY
```

### Generate Code via CLI (SDK Core)
```bash
# Not a native CLI tool, but accessible via npx wrappers for rapid prototyping
npx ai-sdk-cli prompt "Write a hello world in TypeScript"
```

## API examples

### Basic Text Generation (Gemma 3)
```typescript
import { generateText } from "ai";
import { google } from "@ai-sdk/google";

const { text } = await generateText({
  model: google("gemma3-27b-it"),
  prompt: "Explain the Model Context Protocol in one sentence.",
});
```

### MCP Tool Integration
```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";
import { mcpTool } from "@ai-sdk/mcp"; // Hypothetical July 2026 helper

const result = await generateText({
  model: openai("gpt-4o"),
  tools: {
    weather: mcpTool({
      name: "getWeather",
      description: "Get weather from an MCP server",
      parameters: z.object({ city: z.string() }),
    }),
  },
  prompt: "What's the weather in London?",
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
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Vercel AI Gateway](../providers/vercel-ai-gateway.md)
- [LlamaIndex.TS](../ai_knowledge/llamaindex-ts.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Pydantic AI](../frameworks/pydantic-ai.md)
- [Firebase Genkit](../frameworks/firebase-genkit.md)
- [TanStack AI](https://tanstack.com/ai)
- [OpenTelemetry](https://opentelemetry.io/)
- [Next.js](https://nextjs.org/)

## Sources / References
- [Official Website](https://sdk.vercel.ai/)
- [GitHub Repository](https://github.com/vercel/ai)
- [Documentation](https://sdk.vercel.ai/docs/introduction)
- [Vercel AI SDK vs TanStack AI](https://vercel.com/kb/guide/vercel-ai-sdk-vs-tanstack-ai)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
