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

## Getting started

Install LlamaIndex:

```bash
pip install llama-index
```

Minimal example to query a directory of documents:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
```

## API examples

### Load Documents, Create Index, and Query

This example shows how to load data from a local directory, create a searchable index, and execute a query.

```python
import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)

# 1. Load data from a directory
# Assumes you have a folder named 'docs_folder' with text files
reader = SimpleDirectoryReader(input_dir="./docs_folder")
documents = reader.load_data()

# 2. Create an index from the documents
index = VectorStoreIndex.from_documents(documents)

# 3. Create a query engine
query_engine = index.as_query_engine()

# 4. Query the index
response = query_engine.query("Summarize the main points of the documentation.")
print(f"Response: {response}")

# 5. (Optional) Persist the index to disk
index.storage_context.persist(persist_dir="./storage")

# 6. (Optional) Load the index later
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

## Sources / references
- [Official Website](https://www.llamaindex.ai/)
- [GitHub Repository](https://github.com/run-llama/llama_index)

## Contribution Metadata

- Last reviewed: 2026-02-28
- Confidence: medium
