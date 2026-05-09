# AI SDK (by Vercel)

## What it is
The AI SDK is a TypeScript toolkit designed to help developers build AI-powered applications and agents with React, Next.js, Vue, Svelte, Node.js, and more. It provides a unified API for interacting with various LLM providers and building generative user interfaces.

## What problem it solves
It standardizes the integration of Large Language Models (LLMs) across multiple providers (OpenAI, Anthropic, Gemini, etc.), reducing the technical overhead and boilerplate code required to build AI-driven features like streaming chat, structured data extraction, and tool-calling agents.

## Where it fits in the stack
**Category**: Development & Ops / AI App SDK

## Typical use cases
- **AI Chat Interfaces**: Building responsive, streaming chat components in Next.js or React.
- **Generative UI**: Creating user interfaces that change dynamically based on LLM outputs (e.g., streaming components instead of just text).
- **Autonomous Agents**: Implementing multi-step tool-calling loops and agentic workflows in TypeScript.
- **Structured Data Extraction**: Using the SDK to extract type-safe JSON objects from natural language.

## Strengths
- **Framework Agnostic**: Works across React, Next.js, Vue, Svelte, and Node.js.
- **Unified Provider API**: Easily switch between LLM providers with minimal code changes.
- **First-Class Streaming**: Built-in support for streaming text and structured objects.
- **Rich Hook Library**: Simplifies frontend state management for AI interactions with hooks like `useChat` and `useCompletion`.
- **OpenTelemetry Support**: Built-in instrumentation for monitoring and tracing LLM calls.

## When to use it
- When building AI-powered web applications with TypeScript that require multi-provider support and first-class streaming.
- When needing deep integration with the Vercel platform and Next.js ecosystem.

## When not to use it
- In Python-only backend environments where libraries like LangChain or LlamaIndex (Python) are more native.
- If the project requires a heavy focus on non-web UI agentic frameworks (e.g., AutoGen).

## Limitations
- **TypeScript First**: While usable in JS, it is primarily optimized for TypeScript environments.
- **Vercel Ecosystem Affinity**: While it works anywhere, it has deeper integrations and optimizations for the Vercel platform.

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
- [LangChain](../ai_knowledge/langchain.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://sdk.vercel.ai/)
- [GitHub Repository](https://github.com/vercel/ai)
- [Documentation](https://sdk.vercel.ai/docs/introduction)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
