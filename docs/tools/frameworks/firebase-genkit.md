# Firebase Genkit

## What it is
Firebase Genkit is an open-source framework from the Google Firebase team designed to help app developers build full-stack, AI-powered applications. It focuses on integrating generative AI features using familiar patterns and paradigms from the Firebase ecosystem.

## What problem it solves
It reduces the friction of building production-ready AI apps by providing a unified interface for LLMs, a streamlined tool-calling system, and built-in observability for debugging and performance tracking. It is specifically designed to work seamlessly with serverless architectures like Firebase Cloud Functions and Cloud Run.

## Where it fits in the stack
**Category**: Frameworks / Full-Stack AI Framework

## Typical use cases
- **AI-Powered Mobile/Web Apps**: Adding features like chatbots, content generation, or data summarization to Firebase apps.
- **Serverless AI Backends**: Running AI logic in Cloud Functions for Firebase or Google Cloud Run.
- **RAG for App Data**: Integrating vector search and document retrieval using Firestore or other vector stores.
- **Agentic App Logic**: Using Genkit "Flows" to orchestrate complex multi-step AI tasks.

## Strengths
- **App Developer Centric**: Uses paradigms and tooling familiar to mobile and web developers.
- **Unified API**: Support for Gemini, OpenAI, Ollama, DeepSeek, and more.
- **Developer Experience (DX)**: Includes a local Developer UI for testing prompts, flows, and tool calls in real-time.
- **Observability**: Built-in support for traces, logs, and token usage metrics.
- **Seamless Firebase Integration**: Works out-of-the-box with Firebase Auth, Firestore, and Cloud Functions.

## Limitations
- **Language Support**: Currently supports JavaScript/TypeScript and Go, with Python support in development.
- **Ecosystem Focus**: While open-source, it is optimized for the Google Cloud/Firebase stack.

## When to use it
- When you are already using the Firebase or Google Cloud ecosystem and want to add AI features with minimal friction.
- For building production-ready AI applications that require serverless deployment and built-in observability.
- When you prefer a structured, flow-based approach to orchestrating AI tasks in JavaScript/TypeScript or Go.

## When not to use it
- If you are building highly complex, research-oriented agentic systems that require the extreme flexibility of frameworks like LangChain or AutoGen.
- For Python-heavy data science or AI research workflows (until full Python support is released).

## Getting started

### Installation
```bash
npm install -g genkit
```

### Initialize Project
```bash
genkit init
```

### Basic Flow Example (TypeScript)
```typescript
import { defineFlow, run } from '@genkit-ai/flow';
import { generate } from '@genkit-ai/ai';
import { gemini15Flash } from '@genkit-ai/googleai';

export const myFlow = defineFlow(
  { name: 'myFlow', inputSchema: z.string() },
  async (input) => {
    const response = await generate({
      model: gemini15Flash,
      prompt: `Tell me a joke about ${input}`,
    });
    return response.text();
  }
);
```

## Related tools / concepts
- [Google Gemini](../ai_knowledge/google-gemini.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [Firebase Studio](../development_ops/firebase-studio.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Google ADK](google-adk.md)
- [Langflow](langflow.md)
- [Dify](../ai_knowledge/dify.md)
- [Instructor](instructor.md)

## Sources / references
- [Official Website](https://firebase.google.com/docs/genkit)
- [Genkit Introduction](https://firebase-genkit.mintlify.app/introduction)
- [Firebase AI Codelab](https://firebase.google.com/codelabs/ai-genkit-rag)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
