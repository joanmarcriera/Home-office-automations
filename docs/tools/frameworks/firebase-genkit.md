# Firebase Genkit

## What it is
Firebase Genkit is an open-source framework from the Google Firebase team designed to help app developers build full-stack, AI-powered applications. It focuses on integrating generative AI features using familiar patterns and paradigms from the Firebase ecosystem, including the native **Genkit Agents API** introduced in preview in July 2026 for building stateful, autonomous agentic workflows.

## What problem it solves
It reduces the friction of building production-ready AI apps by providing a unified interface for LLMs, a streamlined tool-calling system, and built-in observability for debugging and performance tracking. It is specifically designed to work seamlessly with serverless architectures like Firebase Cloud Functions and Cloud Run.

## Where it fits in the stack
**Category**: Frameworks / Full-Stack AI Framework

## Typical use cases
- **AI-Powered Mobile/Web Apps**: Adding features like chatbots, content generation, or data summarization to Firebase apps.
- **Serverless AI Backends**: Running AI logic in Cloud Functions for Firebase or Google Cloud Run.
- **RAG for App Data**: Integrating vector search and document retrieval using Firestore or other vector stores.
- **Agentic App Logic**: Using Genkit "Flows" to orchestrate complex multi-step AI tasks.
- **Multi-Agent Collaboration with Agents API**: Deploying specialized, tool-equipped autonomous agents using the Genkit Agents API to collaborate on complex objectives.

## Strengths
- **App Developer Centric**: Uses paradigms and tooling familiar to mobile and web developers.
- **Unified API**: Support for Gemini, OpenAI, Ollama, DeepSeek, and [Gemma 3](../ai_knowledge/local_llms.md).
- **Developer Experience (DX)**: Includes a local Developer UI for testing prompts, flows, and tool calls in real-time.
- **Observability**: Built-in support for traces, logs, and token usage metrics.
- **Seamless Firebase Integration**: Works out-of-the-box with Firebase Auth, Firestore, and Cloud Functions.
- **MCP 3.0 Support**: Native integration with the [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) for extensible tool usage.

## Limitations
- **Ecosystem Focus**: While open-source, it is optimized for the Google Cloud/Firebase stack.
- **Python Support**: While in preview, the Python SDK may lag behind the JavaScript/TypeScript implementation in terms of feature parity.

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

## CLI examples

### Start the Developer UI
```bash
genkit start
```

### Run a Flow from CLI
```bash
genkit flow:run myFlow '"input data"'
```

### Deploy to Cloud Functions
```bash
firebase deploy --only functions
```

## API examples

### Genkit Agents API (TypeScript Preview)
The native Agents API allows for standard tool binding and agent definitions directly within the Genkit instantiation loop.

```typescript
import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';

const ai = genkit({
  plugins: [googleAI()],
});

// Define tools for the agent
const webSearchTool = ai.defineTool(
  {
    name: 'webSearch',
    description: 'search the web for current information',
    inputSchema: z.object({ query: z.string() }),
    outputSchema: z.string(),
  },
  async (input) => {
    return `Results for ${input.query}: Genkit Agents API released in July 2026.`;
  }
);

// Define the agent using Genkit Agents API (preview)
export const researchAgent = ai.defineAgent({
  name: 'researchAgent',
  model: googleAI.model('gemini-2.5-flash'),
  prompt: 'You are a high-fidelity research agent. Use tools to find information.',
  tools: [webSearchTool],
});
```

### Basic Flow Example (TypeScript)
```typescript
import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';

const ai = genkit({
  plugins: [googleAI()],
});

export const myFlow = ai.defineFlow(
  {
    name: 'myFlow',
    inputSchema: z.string(),
  },
  async (input) => {
    const { text } = await ai.generate({
      model: googleAI.model('gemini-1.5-flash'),
      prompt: `Tell me a joke about ${input}`,
    });
    return text;
  }
);
```

### Multimodal Generation (Python Preview)
Genkit now supports multimodal generation, allowing you to generate images and text simultaneously.

```python
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI

ai = Genkit(plugins=[GoogleAI()])

response = await ai.generate(
    model='googleai/gemini-2.5-flash-image',
    prompt='a banana riding a bicycle',
    config={'response_modalities': ['IMAGE', 'TEXT']}
)

if response.media:
    print(f"Generated image: {response.media.url}")
print(f"Generated text: {response.text}")
```

## Related tools / concepts
- [Google Gemini](../ai_knowledge/google-gemini.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [Firebase Studio (Sunset March 2027)](../development_ops/firebase-studio.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Google ADK](google-adk.md)
- [Langflow](langflow.md)
- [Dify](../ai_knowledge/dify.md)
- [Instructor](instructor.md)
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [Official Website](https://genkit.dev/)
- [Genkit Documentation](https://firebase.google.com/docs/genkit)
- [Genkit Introduction](https://firebase-genkit.mintlify.app/introduction)
- [Firebase AI Codelab](https://firebase.google.com/codelabs/ai-genkit-rag)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
