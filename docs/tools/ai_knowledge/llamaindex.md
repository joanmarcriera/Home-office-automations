# LlamaIndex

## What it is
LlamaIndex is a data framework for LLM applications to ingest, structure, and access private or domain-specific data. As of July 2026, it has matured into a modular ecosystem (v0.12.0) that supports advanced RAG, multi-agent orchestration via Workflows, and native integration with the [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## What problem it solves
Simplifies the process of connecting LLMs to private and domain-specific data by providing purpose-built abstractions for data ingestion, indexing, and retrieval. It handles the "context window management" and "knowledge retrieval" challenges for both proprietary models (like [Claude 5.1](../providers/anthropic.md)) and local models (like [Gemma 3](local_llms.md)).

## Where it fits in the stack
**Data Framework Layer**. It sits between your data storage (files, databases, APIs) and your AI agents/applications, providing the context necessary for grounded responses in [KnowledgeOps](../../knowledge_base/multi_agent_knowledgeops.md) pipelines.

## Typical use cases
- **Modular RAG Pipelines**: Building question-answering systems over private document collections (PDFs, Notion, Slack).
- **Agentic Workflows**: Creating autonomous agents that use [LlamaIndex Workflows](https://docs.llamaindex.ai/en/stable/module_guides/workflow/) to manage stateful, multi-step processes.
- **MCP Integration**: Using LlamaIndex as an MCP client to fetch data from any [MCP Server](../../knowledge_base/patterns/tool-calling-and-mcp.md).
- **Structured Data Extraction**: Converting unstructured documents into Pydantic objects for use in [Data Copilot](../../architecture/data-copilot-text-to-sql.md) architectures.

## Strengths
- **Data Centric**: Purpose-built for data ingestion and retrieval, making RAG setup straightforward.
- **LlamaHub**: Access to hundreds of data connectors (Google Drive, GitHub, Discord, etc.).
- **Native Gemma 3 Integration**: Optimized for local-first workflows using **Gemma 3** (27b and 4b) via FastMCP.
- **MCP 3.0 Task Protocol**: Full support for agentic tool discovery and multi-hop reasoning over heterogeneous data sources.
- **Evaluation Tools**: Built-in tools for measuring retrieval quality and response faithfulness.
- **Advanced Retrieval**: Supports complex patterns like sub-question querying and reranking.

## Limitations
- **Abstraction Depth**: The transition to Workflows adds a learning curve for developers used to the simpler v0.6.x patterns.
- **Resource Usage**: Large-scale vector indexing can be memory-intensive; requires robust vector databases like [ChromaDB](../../services/chromadb.md) for production.

## When to use it
- When building data-intensive LLM applications that require complex RAG or knowledge graph retrieval.
- When you need a unified interface to heterogeneous data sources (SQL, NoSQL, APIs, Files).
- For building stateful AI agents that require fine-grained control over execution flows.

## When not to use it
- For simple "chat with a single PDF" tasks where [AnythingLLM](../ai_knowledge/anythingllm.md) or [Khoj](../intake_storage/khoj.md) offer a better out-of-the-box UI.
- When building low-level model inference engines (use [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md) instead).

## Getting started

### 1. Installation
LlamaIndex is highly modular. Install the core library and the July 2026 recommended defaults:

```bash
pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file
```

### 2. Basic Workflow Example
A minimal event-driven RAG workflow:

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

class RAGWorkflow(Workflow):
    @step
    async def ingest(self, ev: StartEvent) -> StopEvent:
        documents = SimpleDirectoryReader("./data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(ev.query)
        return StopEvent(result=str(response))

# Usage
w = RAGWorkflow()
result = await w.run(query="What are the key takeaways?")
```

## CLI examples
```bash
# Ingest a directory and create a local index
llamaindex-cli index --directory ./my_docs --index_name local_index

# Query a local index via CLI
llamaindex-cli query --index_name local_index "Summarize the project status"

# Start a LlamaIndex-powered MCP server
mcp run llama_index_mcp_server --config ./mcp_config.yaml
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

### Using Gemma 3 for Local Reasoning
LlamaIndex supports the latest local frontier models via [Ollama](../../services/ollama.md).

```python
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

Settings.llm = Ollama(model="gemma3:27b", request_timeout=120.0)

response = Settings.llm.complete("Explain the Anysync protocol used in Anytype.")
print(response)
```

### MCP Tool Integration
Registering an [MCP Tool](../../knowledge_base/patterns/tool-calling-and-mcp.md) for use in a LlamaIndex Agent.

```python
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.tools.mcp import MCPToolSpec

# Connect to a local MCP server (e.g., Paperless-ngx)
mcp_spec = MCPToolSpec(server_url="http://localhost:8000/mcp")
tools = mcp_spec.to_tool_list()

agent = FunctionCallingAgentWorker.from_tools(tools).as_agent()
agent.chat("Search my documents for the latest invoice from 2026.")
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
- [July 2026 Release Notes: The Era of Workflows](https://llamaindex.ai/blog/workflows-v0-12)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
