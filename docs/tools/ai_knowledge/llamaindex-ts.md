# LlamaIndex.TS

## What it is
LlamaIndex.TS is the TypeScript version of the LlamaIndex data framework. It is designed to help developers build AI-powered applications with their own data using JavaScript or TypeScript in environments like Node.js, Deno, and Bun. By June 2026, it has fully integrated with **MCP 3.0** and supports state-of-the-art agentic orchestration.

## What problem it solves
It bridges the gap between Large Language Models (LLMs) and custom data sources in the JavaScript/TypeScript ecosystem. It provides tools for data ingestion, indexing, and querying, enabling retrieval-augmented generation (RAG) and agentic workflows. It solves the "Context Management" problem for web developers by providing a unified interface for connecting various data sources to frontier models.

## Where it fits in the stack
**AI & Knowledge / Agent Framework (TypeScript)**. It sits in the application layer, orchestrating data retrieval from the [Persistence Layer](../infrastructure/index.md) and feeding it to models like [Claude 4.8](../ai_knowledge/claude.md) or [GPT-5.5](../ai_knowledge/openai.md) via standardized protocols.

## Typical use cases
- **Full-Stack AI Apps**: Integrating RAG into Next.js, Nuxt, or SvelteKit applications.
- **Serverless AI Functions**: Running data retrieval and LLM calls in Vercel Edge Runtime or Cloudflare Workers.
- **Edge Data Processing**: Using Deno or Bun for high-performance data indexing and query orchestration.
- **Production Agentic RAG**: Building multi-step, stateful retrieval pipelines using standardized orchestration patterns.
- **MCP Tool Creation**: Developing TypeScript-based toolkits for the [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## Strengths
- **Native TypeScript Support**: Excellent type safety, IDE autocompletion, and compatibility with modern web frameworks.
- **Broad Ecosystem**: Support for hundreds of data loaders (LlamaHub) and vector store integrations.
- **MCP 3.0 Native**: (June 2026) Direct support for the Model Context Protocol, enabling easy tool use for agents.
- **High Performance**: Optimized for modern runtimes like Bun and Deno, providing low-latency indexing and retrieval.
- **Modular Design**: Easy to swap out LLMs, embedding models, and storage backends.

## Limitations
- **Ecosystem Fragmentation**: As a TypeScript port, some features may lag slightly behind the primary Python version of LlamaIndex.
- **Runtime Limitations**: Certain heavy data processing tasks may still be more performant in a Python/Rust environment.
- **Learning Curve**: The framework's extensive feature set can be overwhelming for beginners.

## When to use it
- When building AI applications within the JavaScript/TypeScript ecosystem (Node.js, Browser, Edge).
- When you need a robust, production-ready framework for RAG and agentic workflows.
- When you want to leverage the [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) in a TypeScript environment.

## When not to use it
- If your primary development environment is Python-centric (use the original LlamaIndex).
- For simple, single-prompt AI calls where a framework might add unnecessary overhead.
- When performing extremely complex, long-running data science tasks where Python's library ecosystem is superior.

## Getting started
1. **Install**:
```bash
npm install llamaindex
# or
bun add llamaindex
```
2. **Setup**: Configure your environment variables for your chosen LLM provider (e.g., `OPENAI_API_KEY`).
3. **Basic Usage**: Create a simple query engine.
```typescript
import { Document, VectorStoreIndex } from "llamaindex";

const document = new Document({ text: "LlamaIndex is an agentic data framework." });
const index = await VectorStoreIndex.fromDocuments([document]);
const queryEngine = index.asQueryEngine();
const response = await queryEngine.query({ query: "What is LlamaIndex?" });
console.log(response.toString());
```

## CLI examples
The LlamaIndex CLI allows for quick data ingestion and chat:

```bash
# Ingest a directory of documents
llamaindex-ts ingest --dir ./docs

# Start a chat session with your indexed data
llamaindex-ts chat

# List active MCP 3.0 toolsets
llamaindex-ts mcp list
```

## API examples
### Agentic Tool Use (TypeScript)
```typescript
import { OpenAIAgent, FunctionTool } from "llamaindex";

const myTool = new FunctionTool((args: { input: string }) => {
  return `Processed: ${args.input}`;
}, {
  name: "processor",
  description: "Processes a given string"
});

const agent = new OpenAIAgent({ tools: [myTool] });
const response = await agent.chat({ message: "Process the string 'hello world'" });
console.log(response.toString());
```

## Related tools / concepts
- [LlamaIndex (Python)](llamaindex.md)
- [LangChain.js](langchain.md)
- [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude 4.8](../ai_knowledge/claude.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [Llama-deploy](https://github.com/run-llama/llama-deploy)
- [LlamaTrace](https://llamatrace.com/)

## Sources / References
- [LlamaIndex.TS Documentation](https://ts.llamaindex.ai/)
- [LlamaHub (Data Loaders)](https://llamahub.ai/)
- [LlamaIndex GitHub Repository](https://github.com/run-llama/LlamaIndexTS)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
