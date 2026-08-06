# Firebase Genkit

## What it is
Firebase Genkit is an open-source framework from Google designed to help app developers build full-stack, AI-powered applications. As of late 2026, Genkit has matured into **v1.2.0+**, featuring the native **Genkit Agents API** (released in preview in July 2026, stabilized in late 2026) for building stateful, autonomous agentic workflows. It supports deep integration with **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**, and provides first-class support for frontier models such as Claude 5.1, GPT-5.5, Gemini 4.0, and [Gemma 3](../ai_knowledge/local_llms.md).

## What problem it solves
It reduces the friction of building production-ready AI apps by providing a unified interface for LLMs, a streamlined tool-calling system, and built-in observability for debugging and performance tracking. It solves the orchestration gap for application engineers by integrating generative AI patterns natively with serverless architectures like Firebase Cloud Functions and Cloud Run, avoiding the need for complex, heavy-weight Python agent servers.

## Where it fits in the stack
**Category**: Frameworks / Full-Stack AI Framework

## Typical use cases
- **AI-Powered Mobile/Web Apps**: Adding features like chatbots, content generation, or data summarization to Firebase-backed applications.
- **Serverless AI Backends**: Running low-latency, secure AI logic in Cloud Functions for Firebase or Google Cloud Run.
- **RAG for App Data**: Integrating vector search and real-time document retrieval using Cloud Firestore or other Google Cloud vector stores.
- **Stateful Multi-Agent Orchestration**: Deploying specialized, tool-equipped autonomous agents using the Genkit Agents API to collaborate on complex user objectives.

## Strengths
- **App Developer Centric**: Uses paradigms, TypeScript/Go languages, and tooling familiar to mobile and web developers.
- **Unified API**: Support for Gemini 4.0, Claude 5.1, GPT-5.5, DeepSeek, and local [Gemma 3](../ai_knowledge/local_llms.md) / Ollama.
- **Developer Experience (DX)**: Includes a local Developer UI for testing prompts, flows, and tool calls in real-time.
- **Observability**: Native, built-in support for traces, logs, and token usage metrics.
- **Seamless Firebase Integration**: Works out-of-the-box with Firebase Auth, Cloud Firestore, and Cloud Functions.
- **MCP 3.1 Support**: Native integration with the Model Context Protocol for dynamic tool and resource discovery.

## Limitations
- **Ecosystem Focus**: Highly optimized for Google Cloud and Firebase, making deployment on other clouds less streamlined.
- **Python SDK Parity**: While improving, the Python SDK still lags behind the JavaScript/TypeScript implementation in terms of complete feature coverage.

## When to use it
- When you are already using the Firebase or Google Cloud ecosystem and want to add AI features with minimal friction.
- For building production-ready AI applications that require serverless deployment and built-in observability.
- When you prefer a structured, flow-based approach to orchestrating AI tasks in JavaScript/TypeScript or Go.

## When not to use it
- If you are building highly complex, research-oriented agentic systems that require the extreme flexibility of frameworks like LangChain or AutoGen.
- For Python-heavy data science or AI research workflows where Python is the non-negotiable standard.

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

### Genkit Agents API (TypeScript)
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
    return `Results for ${input.query}: Gemini 4.0 and Genkit Agents API in action.`;
  }
);

// Define the agent using Genkit Agents API
export const researchAgent = ai.defineAgent({
  name: 'researchAgent',
  model: googleAI.model('gemini-4.0-flash'),
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
      model: googleAI.model('gemini-4.0-flash'),
      prompt: `Tell me a joke about ${input}`,
    });
    return text;
  }
);
```

### Python (Genkit Run Schema & Execution Validation)
When Genkit flows execute on Node.js/Go serverless backends, they frequently emit structured logs and execution metrics. Python telemetry and data processing pipelines can validate Genkit flow executions using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator

# 1. Define Genkit Flow Run validation schemas
class GenkitStepTrace(BaseModel):
    step_name: str = Field(..., serialization_alias="stepName", validation_alias="stepName")
    step_type: str = Field(..., serialization_alias="stepType", validation_alias="stepType")
    duration_ms: float = Field(..., ge=0, serialization_alias="durationMs", validation_alias="durationMs")
    status: Literal["success", "failed"] = Field(default="success")

class GenkitFlowExecution(BaseModel):
    flow_id: str = Field(..., serialization_alias="flowId", validation_alias="flowId")
    frontier_model: str = Field(..., serialization_alias="frontierModel", validation_alias="frontierModel")
    steps: List[GenkitStepTrace] = Field(default_factory=list)
    completion_tokens: int = Field(..., ge=0, serialization_alias="completionTokens", validation_alias="completionTokens")
    prompt_tokens: int = Field(..., ge=0, serialization_alias="promptTokens", validation_alias="promptTokens")

    @field_validator("frontier_model")
    @classmethod
    def validate_frontier_model(cls, v: str) -> str:
        allowed = ["Claude 5.1", "GPT-5.5", "Gemini 4.0", "Gemma 3"]
        if not any(model in v for model in allowed):
            raise ValueError(f"Model {v} must contain a late 2026 SOTA model: {allowed}")
        return v

# 2. Simulated JSON payload emitted from a Genkit TypeScript serverless flow execution
genkit_execution_payload = {
    "flowId": "flow-user-onboarding-893",
    "frontierModel": "Gemini 4.0 Pro",
    "completionTokens": 450,
    "promptTokens": 180,
    "steps": [
        {
            "stepName": "retrieve-auth-context",
            "stepType": "action",
            "durationMs": 42.1,
            "status": "success"
        },
        {
            "stepName": "generate-welcome-email",
            "stepType": "llm-generation",
            "durationMs": 780.4,
            "status": "success"
        }
    ]
}

# 3. Perform validation
try:
    execution = GenkitFlowExecution(**genkit_execution_payload)
    print("Genkit Flow execution payload validated successfully!")
    print(f"Flow ID: {execution.flow_id}")
    print(f"Frontier Model Used: {execution.frontier_model}")
    print(f"Tokens (Prompt / Completion): {execution.prompt_tokens} / {execution.completion_tokens}")
    for step in execution.steps:
        print(f"  - Step: {step.step_name} [{step.step_type}] -> {step.status} in {step.duration_ms}ms")
except Exception as e:
    print(f"Validation failed: {e}")
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

## Sources / references
- [Official Website](https://genkit.dev/)
- [Genkit Documentation](https://firebase.google.com/docs/genkit)
- [Genkit Introduction](https://firebase-genkit.mintlify.app/introduction)
- [Firebase AI Codelab](https://firebase.google.com/codelabs/ai-genkit-rag)

## Contribution Metadata
- Last reviewed: 2026-12-10
- Confidence: high
