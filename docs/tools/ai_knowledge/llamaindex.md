# LlamaIndex

## What it is
LlamaIndex is a data framework for LLM applications to ingest, structure, and access private or domain-specific data. It provides tools for building RAG applications, including data connectors, indexes, and query engines.

## What problem it solves
Simplifies the process of connecting LLMs to private and domain-specific data by providing purpose-built abstractions for data ingestion, indexing, and retrieval.

## Where it fits in the stack
AI & Knowledge — serves as a data-centric framework for building RAG pipelines over local or private data, complementing the Ollama-based LLM infrastructure.

## Typical use cases
- Building RAG applications over private document collections
- Structured data extraction from documents such as invoices
- Creating query engines that combine multiple data sources

## Strengths
- Purpose-built for data ingestion and retrieval, making RAG setup straightforward
- Wide range of data connectors for different file formats and sources
- Clean abstractions for indexing and querying

## Limitations
- Less suited for complex agent workflows compared to LangChain
- Rapid development pace can lead to API changes between versions
- Smaller ecosystem for non-RAG use cases

## When to use it
- When the primary goal is building RAG over private or domain-specific data
- When you need structured data extraction from documents

## When not to use it
- When building complex multi-agent workflows (consider LangChain or LangGraph instead)
- When the application does not involve data retrieval or indexing

## Related tools / concepts
- [LangChain](langchain.md)
- [Haystack](https://github.com/deepset-ai/haystack)

## Sources / references
- [Official Website](https://www.llamaindex.ai/)
- [GitHub Repository](https://github.com/run-llama/llama_index)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
