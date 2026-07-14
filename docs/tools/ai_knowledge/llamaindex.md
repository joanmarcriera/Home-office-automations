# LlamaIndex

## What it is
LlamaIndex is a data framework for LLM applications to ingest, structure, and access private or domain-specific data. As of July 2026, **LlamaIndex v0.12.0** features native support for the **MCP 3.0 Task Protocol**, enabling data agents to autonomously discover and utilize tools across distributed environments. It provides standardized abstractions for building high-fidelity RAG pipelines and agentic reasoning loops.

## What problem it solves
Simplifies the process of connecting LLMs to private and domain-specific data by providing purpose-built abstractions for data ingestion, indexing, and retrieval. It handles the "glue" code between data sources and LLM prompts.

## Where it fits in the stack
**Data Framework Layer**. It sits between your data storage (files, databases, APIs) and your AI agents/applications, providing the context necessary for grounded responses.

## Typical use cases
- **RAG Pipelines**: Building question-answering systems over private document collections (PDFs, Notion, Slack).
- **Structured Extraction**: Converting unstructured documents like invoices or receipts into Pydantic objects.
- **Data Agents**: Creating agents that can autonomously decide which data source to query to answer a user request.
- **Knowledge Graphs**: Building and querying property graphs for complex relational data.

## Strengths
- **Data Centric**: Purpose-built for data ingestion and retrieval, making RAG setup straightforward.
- **LlamaHub**: Access to hundreds of data connectors (Google Drive, GitHub, Discord, etc.).
- **Native Gemma 3 Integration**: Optimized for local-first workflows using **Gemma 3** (27b and 4b) via FastMCP.
- **MCP 3.0 Task Protocol**: Full support for agentic tool discovery and multi-hop reasoning over heterogeneous data sources.
- **Evaluation Tools**: Built-in tools for measuring retrieval quality and response faithfulness.
- **Advanced Retrieval**: Supports complex patterns like sub-question querying and reranking.

## Limitations
- **Rapid Evolution**: The API changes frequently between versions (e.g., the v0.10.0 refactor was a major breaking change).
- **Abstractions Overhead**: The deep nested abstractions can sometimes make it harder to customize low-level logic compared to building with raw LangChain.

## When to use it
- When the primary goal is building RAG over private or domain-specific data.
- When you need a "data-first" approach to LLM application development.
- For structured data extraction from complex documents.

## When not to use it
- When building simple chat applications that don't require external data.
- For extremely complex multi-agent orchestration where [LangGraph](langchain.md) might offer more control.

## Getting started

### 1. Installation
LlamaIndex is now modular. Install the core library and any necessary integrations:

```bash
pip install llama-index-core llama-index-readers-file llama-index-llms-openai
```

### 2. Basic RAG Example
Minimal example to query a directory of documents:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents from a 'data' directory
documents = SimpleDirectoryReader("./data").load_data()

# Create index and query engine
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("What is the main topic?")
print(response)
```

## CLI examples
The LlamaIndex CLI allows for quick RAG pipeline deployment and data management.

```bash
# Rapidly start a RAG chat over a directory of documents
llamaindex-cli rag --files "./data/*.pdf" --parse-tier agentic

# Create a new LlamaIndex project from a template
llamaindex-cli create-app --name my-data-agent --template high-fidelity-rag

# List and manage connected LlamaHub loaders
llamaindex-cli hub list --category readers
```

## API examples

### Property Graph Index
Property graphs allow for modeling complex relationships between entities extracted from text.

```python
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

# Define a schema for extraction
entities = ["Organization", "Person", "Event"]
relations = ["WORKS_AT", "ATTENDED", "FOUNDED"]
validation_schema = {
    "Organization": ["WORKS_AT", "FOUNDED"],
    "Person": ["WORKS_AT", "ATTENDED"],
}

kg_extractor = SchemaLLMPathExtractor(
    kg_schema=validation_schema,
    strict=True
)

index = PropertyGraphIndex.from_documents(
    documents,
    kg_extractors=[kg_extractor]
)

query_engine = index.as_query_engine(include_text=True)
response = query_engine.query("Who founded the organization?")
```

### Customizing the LLM and Embeddings
LlamaIndex allows easy switching of backend providers (e.g., using [OpenRouter](openrouter.md) or [LocalAI](../infrastructure/localai.md)).

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = OpenAI(
    model="gpt-4o",
    api_base="https://openrouter.ai/api/v1",
    api_key="your-key"
)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
```

## Related tools / concepts
- [LangChain](langchain.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [LlamaHub](https://llamahub.ai/)
- [ChromaDB](../../services/chromadb.md)
- [OpenPipe](../infrastructure/openpipe.md)
- [Haystack](../frameworks/haystack.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Gemma 3](local_llms.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)

## Sources / references
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [LlamaHub Connectors](https://llamahub.ai/)
- [MCP 3.0 Specification for Data Agents](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
