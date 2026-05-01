# LlamaIndex.TS

## What it is
LlamaIndex.TS is the TypeScript version of the LlamaIndex data framework. It is designed to help developers build AI-powered applications with their own data using JavaScript or TypeScript in environments like Node.js, Deno, and Bun.

## What problem it solves
It bridges the gap between Large Language Models (LLMs) and custom data sources in the JavaScript/TypeScript ecosystem. It provides tools for data ingestion, indexing, and querying, enabling retrieval-augmented generation (RAG) and agentic workflows in web and backend applications.

## Where it fits in the stack
**Category**: AI & Knowledge / Agent Framework (TypeScript)

## Typical use cases
- **Full-Stack AI Apps**: Integrating RAG into Next.js, Nuxt, or SvelteKit applications.
- **Serverless AI Functions**: Running data retrieval and LLM calls in Vercel Edge Runtime or Cloudflare Workers.
- **Edge Data Processing**: Using Deno or Bun for high-performance data indexing and query orchestration.

## Strengths
- **Native TypeScript Support**: Excellent type safety and IDE autocompletion.
- **Environment Flexibility**: Supports Node.js, Deno, Bun, and major serverless runtimes.
- **Ecosystem Integration**: Works with major LLM providers (OpenAI, Anthropic, Gemini) and vector databases.
- **LlamaCloud Support**: Seamlessly connects to LlamaIndex's cloud parsing and indexing services.

## Limitations
- **Ecosystem Maturity**: While rapidly growing, it may have fewer community connectors compared to the Python version.
- **Browser Constraints**: Direct browser support is limited due to the lack of `AsyncLocalStorage` in many browser environments.
- **Deprecation Warning**: As of April 30, 2026, the core `LlamaIndexTS` repository is marked as deprecated in favor of unified Python/Cloud-first documentation, though the NPM package remains widely used for JS/TS integrations.

## Getting started

### Installation
```bash
npm install llamaindex
```

### Basic usage
```typescript
import { Document, VectorStoreIndex } from "llamaindex";

async function main() {
  const document = new Document({ text: "LlamaIndex is a data framework for LLMs." });
  const index = await VectorStoreIndex.fromDocuments([document]);
  const queryEngine = index.asQueryEngine();
  const response = await queryEngine.query({ query: "What is LlamaIndex?" });
  console.log(response.toString());
}

main();
```

## Related tools / concepts
- [LlamaIndex (Python)](../ai_knowledge/llamaindex.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [RAG](../../knowledge_base/patterns/rag.md)

## Sources / references
- [Official Website](https://ts.llamaindex.ai/)
- [GitHub Repository](https://github.com/run-llama/LlamaIndexTS)
- [Documentation](https://ts.llamaindex.ai/docs/llamaindex/getting_started)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
