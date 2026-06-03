# LlamaIndex.TS

## What it is
LlamaIndex.TS is the TypeScript version of the LlamaIndex data framework. It is designed to help developers build AI-powered applications with their own data using JavaScript or TypeScript in environments like Node.js, Deno, and Bun. As of June 2026, it has fully embraced **Workflows** as the primary composition primitive for building complex RAG and agentic systems.

## What problem it solves
It bridges the gap between Large Language Models (LLMs) and custom data sources in the JavaScript/TypeScript ecosystem. It provides tools for data ingestion, indexing, and querying, enabling retrieval-augmented generation (RAG) and agentic workflows in web and backend applications.

## Where it fits in the stack
**Category**: AI & Knowledge / Agent Framework (TypeScript)

## Typical use cases
- **Full-Stack AI Apps**: Integrating RAG into Next.js, Nuxt, or SvelteKit applications.
- **Serverless AI Functions**: Running data retrieval and LLM calls in Vercel Edge Runtime or Cloudflare Workers.
- **Edge Data Processing**: Using Deno or Bun for high-performance data indexing and query orchestration.
- **Production Agentic RAG**: Building multi-step, stateful retrieval pipelines using the **Workflows** API.

## Strengths
- **Native TypeScript Support**: Excellent type safety and IDE autocompletion.
- **Workflows API**: (New for 2026) Event-driven orchestration for complex agent loops and RAG pipelines.
- **Environment Flexibility**: Supports Node.js, Deno, Bun, and major serverless runtimes.
- **llama-deploy**: Native support for deploying LlamaIndex workflows as scalable microservices.
- **Observability**: Built-in integration with **traceAI** and OpenTelemetry for production monitoring.

## Limitations
- **Ecosystem Maturity**: While rapidly growing, it may have fewer community connectors compared to the Python version.
- **Browser Constraints**: Direct browser support is limited due to the lack of `AsyncLocalStorage` in many browser environments.
- **Cloud-First Shift**: Some advanced features require LlamaCloud for optimal performance (e.g., LlamaParse).

## When to use it
- **Full-Stack TS Apps**: When your entire stack is TypeScript-based and you want a native, type-safe RAG implementation.
- **Serverless/Edge Deployment**: When deploying to environments like Vercel, Netlify, or Cloudflare Workers where JS/TS runtimes are the primary choice.
- **Production Workflows**: When building complex, multi-agent systems that need to be deployed via `llama-deploy`.

## When not to use it
- **Data Science Heavy Workflows**: If your project relies on extensive Python-only data science libraries (Pandas, Polars, Scikit-learn), the Python version is more suitable.
- **Legacy Projects**: For older projects with no TypeScript support, the overhead of adding it might not outweigh the benefits.

## Getting started

### Installation
```bash
npm install llamaindex
```

### Basic Workflow Example (2026)
LlamaIndex.TS now prioritizes **Workflows** for building logic:

```typescript
import { Workflow, StartEvent, StopEvent, step } from "llamaindex";

class MyRAGWorkflow extends Workflow {
  @step()
  async retrieve(ev: StartEvent): Promise<StopEvent> {
    // Logic for data retrieval and LLM call
    const result = "LlamaIndex Workflows are event-driven.";
    return new StopEvent({ result });
  }
}

const workflow = new MyRAGWorkflow();
const result = await workflow.run();
console.log(result);
```

## Production Deployment
- **llama-deploy**: Use the `llama-deploy` CLI to containerize and deploy your TypeScript workflows to Kubernetes or cloud providers.
- **traceAI**: Enable production observability by configuring the `traceAI` instrumentation in your application entry point.

## Related tools / concepts
- [LlamaIndex (Python)](../ai_knowledge/llamaindex.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [LangGraph](../frameworks/langgraph.md)
- [Pydantic AI](../frameworks/pydantic-ai.md)
- [Instructor](../frameworks/instructor.md)
- [Mastra](../frameworks/mastra.md)
- [AG2](../frameworks/ag2.md)
- [Llama-deploy](https://github.com/run-llama/llama-deploy)
- [TraceAI](https://llamatrace.com/)

## Sources / references
- [Official Website](https://ts.llamaindex.ai/)
- [GitHub Repository](https://github.com/run-llama/LlamaIndexTS)
- [LlamaIndex 2026: Workflows and Production](https://ts.llamaindex.ai/blog/workflows-and-production-2026)
- [Documentation](https://ts.llamaindex.ai/docs/llamaindex/getting_started)
- [Llama-deploy](https://github.com/run-llama/llama-deploy)
- [LlamaTrace (TraceAI)](https://llamatrace.com/)

## Contribution Metadata
- Last reviewed: 2026-06-03
- Confidence: high
