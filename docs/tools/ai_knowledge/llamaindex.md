# LlamaIndex

## What it is
LlamaIndex is an open-source data framework and context orchestration platform for building LLM applications, retrieval-augmented generation (RAG) systems, and stateful autonomous data agents. As of early 2027, LlamaIndex (v0.12+) features event-driven Workflows architecture, native support for **FastMCP 3.1** and the **MCP 3.0 Task Protocol**, and seamless integration with frontier models including [Claude 5.6](../providers/anthropic.md), [GPT-5.6](openai.md), [Gemini 4.0 Ultra](gemini.md), [DeepSeek-V4](deepseek-r1.md), [Qwen 3.6 VL](qwen.md), and [Gemma 4](local_llms.md).

LlamaIndex abstracts context window management, structured data extraction, chunking, embedding generation, vector store querying, and multi-hop retrieval pipelines while replacing brittle legacy chains with reactive, event-driven state machine workflows.

```mermaid
architecture-beta
    group client_layer(cloud, "Client & Agent Layer")
    service fastmcp_client(server, "FastMCP 3.1 Agent") in client_layer
    service cli_tool(terminal, "LlamaIndex CLI") in client_layer

    group orchestration(database, "LlamaIndex Core Orchestration Engine")
    service workflow_engine(cpu, "Event-Driven Workflow State Machine") in orchestration
    service chunker(disk, "Sentence / Semantic Node Parser") in orchestration
    service retriever(search, "Hybrid Vector & BM25 Retriever") in orchestration
    service extractor(code, "Pydantic v2 Structured Extractor") in orchestration

    group external_storage(internet, "Storage & Frontier Model Layer")
    service vector_db(database, "Qdrant / ChromaDB") in external_storage
    service llm_provider(cloud, "Claude 5.6 / GPT-5.6 / DeepSeek-V4") in external_storage

    fastmcp_client --> workflow_engine: FastMCP Tool Execution
    cli_tool --> workflow_engine: Shell Execution
    workflow_engine --> chunker: Raw Document Streams
    chunker --> vector_db: Embeddings & Vector Indexing
    workflow_engine --> retriever: Multi-Hop Vector Queries
    retriever --> vector_db: Similarity Search & Reranking
    workflow_engine --> extractor: Structured Metadata Parsing
    extractor --> llm_provider: Tool Calls & JSON Schemas
    retriever --> llm_provider: Synthesized Context Window
```

## What problem it solves
Simplifies connecting LLMs to private and heterogeneous data sources (PDFs, SQL databases, Notion, vector stores, cloud APIs). It abstracts context window optimization, document parsing, embedding generation, chunking strategies, and multi-hop retrieval pipelines while eliminating brittle custom ingestion logic.

In enterprise and agentic environments, raw document ingestion suffers from loss of formatting, poor chunk boundary selection, context dilution, and inability to trace agent execution flows. LlamaIndex solves this through:
- **Hierarchical Node Parsing**: Preserving document metadata, heading relationships, and chunk provenance.
- **Event-Driven Workflows**: Replacing sequential `Chain` objects with asynchronous, event-streamed step functions.
- **Protocol Interoperability**: Exposing RAG tools and pipelines directly via FastMCP 3.1 server endpoints.

## Where it fits in the stack
**Data Framework / Context Orchestration Layer**. It sits between raw enterprise or local storage repositories and high-level agent frameworks or applications, acting as the primary retrieval and context ingestion engine for [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) pipelines.

```
+-----------------------------------------------------------------------+
|                       Application / UI Layer                          |
|             (Cursor, AnythingLLM, FastMCP 3.1 Web Clients)            |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|            Context Orchestration Layer (LlamaIndex v0.12+)            |
|  +---------------------+ +--------------------+ +------------------+  |
|  | Event Workflows     | | Hybrid Retrievers  | | Pydantic v2      |  |
|  | State Machine       | | Vector + BM25      | | Extraction       |  |
|  +---------------------+ +--------------------+ +------------------+  |
+-----------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+----------------------------------+       +----------------------------+
| Vector Stores & Storage Index    |       | Frontier Intelligence APIs |
| (Qdrant, ChromaDB, PGvector)     |       | (Claude 5.6, GPT-5.6)      |
+----------------------------------+       +----------------------------+
```

## Typical use cases
- **Modular RAG Pipelines**: Building question-answering systems over unstructured and structured document collections with dense vector retrieval, sparse lexical search, and neural reranking.
- **Stateful Agentic Workflows**: Creating multi-step, stateful agents using event-driven LlamaIndex Workflows that handle human-in-the-loop validation, asynchronous loops, and branch joins.
- **FastMCP 3.1 Integration**: Exposing LlamaIndex indexes and tools over standardized FastMCP endpoints for agentic discovery and remote invocation.
- **Structured Data Extraction**: Transforming raw documents, invoices, and tech specs into strictly validated Pydantic v2 objects for automated workflows and [Data Copilot](../../architecture/data-copilot-text-to-sql.md) systems.
- **Multimodal Knowledge Graph Ingestion**: Ingesting images, architectural diagrams, and video transcripts into knowledge graph structures paired with semantic vector embeddings.

## Strengths
- **Data Centricity**: Built from the ground up for data loading, indexing, and retrieval across hundreds of LlamaHub readers and connectors.
- **Workflows Architecture**: Event-driven execution model replacing rigid legacy chains with explicit state management, step decorated async handlers, and event emitters.
- **Native FastMCP 3.1 & MCP 3.0 Support**: Out-of-the-box MCP client and server capabilities for agentic tool discovery, remote execution, and task protocol state synchronization.
- **Frontier Model Optimization**: Native support for Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL, and local Gemma 4 models via Ollama or vLLM.
- **Built-in Evaluation & Observability**: Comprehensive suite for measuring retrieval context precision, recall, hit rate, and response faithfulness integrated with Sentry and Langfuse.

## Limitations
- **Workflow Learning Curve**: Migrating from early `VectorStoreIndex` patterns to event-driven `Workflow` state machines requires explicit step design and event stream handling.
- **Resource Footprint**: High-throughput vector indexing and local embedding models require adequate GPU/RAM resources or managed vector stores like [ChromaDB](../infrastructure/chroma.md) or Qdrant.
- **API Surface Breadth**: Rapid ecosystem evolution across LlamaHub packages requires pinning dependencies to ensure version stability in production.

## When to use it
- When building data-intensive LLM applications requiring complex RAG, hybrid search, or knowledge graph querying.
- When unifying multi-source data ingestion (PDFs, Notion, SQL, S3, APIs) into a standardized retrieval interface.
- When creating stateful AI agents that need transparent control over multi-step execution flows and async event pipelines.
- When exposing vector indexes or structured extractors as remote tools over FastMCP 3.1.

## When not to use it
- For quick, out-of-the-box file-chat GUIs without custom development (use [AnythingLLM](anythingllm.md) or [Khoj](../intake_storage/khoj.md)).
- When serving low-level LLM model weights directly (use [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md)).
- For ultra-lightweight single-prompt completions where an LLM SDK directly suffices without context indexing.

## Getting started

### Installation
Install LlamaIndex core, standard provider integrations, vector store tools, and Pydantic v2:

```bash
pip install llama-index-core \
    llama-index-llms-openai \
    llama-index-llms-anthropic \
    llama-index-embeddings-openai \
    llama-index-readers-file \
    llama-index-vector-stores-qdrant \
    pydantic>=2.0.0 \
    fastmcp>=3.1.0
```

### Basic Workflow Example
A minimal event-driven RAG workflow using `llama-index-core` Workflows:

```python
import asyncio
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

class QueryEvent(Event):
    query: str
    documents_loaded: int

class RAGWorkflow(Workflow):
    @step
    async def load_and_index(self, ev: StartEvent) -> QueryEvent:
        data_dir = ev.get("data_dir", "./data")
        query_text = ev.get("query", "Summarize key findings")

        documents = SimpleDirectoryReader(data_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents)
        return QueryEvent(query=query_text, documents_loaded=len(documents))

    @step
    async def query_index(self, ev: QueryEvent) -> StopEvent:
        query_engine = self.index.as_query_engine()
        response = await query_engine.aquery(ev.query)
        return StopEvent(result={
            "query": ev.query,
            "docs_processed": ev.documents_loaded,
            "response": str(response)
        })

async def main():
    w = RAGWorkflow(timeout=60)
    result = await w.run(data_dir="./data", query="What are the main technical architecture updates?")
    print("Workflow Execution Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
The LlamaIndex CLI enables rapid indexing, environment configuration, and RAG execution directly from the shell:

```bash
# Ingest a directory and query via CLI with hybrid retrieval
llamaindex-cli rag --files "./data/*.pdf" --query "Summarize the quarterly goals"

# Create a new LlamaIndex application boilerplate with FastMCP 3.1 integration
llamaindex-cli create-app --name my-data-agent --template high-fidelity-rag

# List available readers and loaders on LlamaHub
llamaindex-cli hub list --category readers

# Export an existing vector index metadata summary
llamaindex-cli index summary --index-path ./storage
```

## API examples

### Structured Extraction with Pydantic v2 Validation
Extracting validated metadata using LlamaIndex structured programs and Pydantic v2 schemas:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.openai import OpenAI

class SecurityAuditItem(BaseModel):
    severity: str = Field(..., description="Risk severity level: HIGH, MEDIUM, LOW")
    component: str = Field(..., description="Target service or component name")
    vulnerability: str = Field(..., description="Detailed description of the vulnerability")
    remediation_step: str = Field(..., description="Recommended fix or patch")

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v: str) -> str:
        upper_v = v.upper().strip()
        if upper_v not in {"HIGH", "MEDIUM", "LOW"}:
            raise ValueError(f"Invalid severity level: {v}")
        return upper_v

class SecurityReport(BaseModel):
    report_title: str = Field(..., description="Title of the audit report")
    findings: List[SecurityAuditItem] = Field(default_factory=list)
    compliance_score: float = Field(..., ge=0.0, le=100.0)

prompt_template_str = """\
You are an expert security auditor. Extract structured audit findings from the log below.
Audit Log:
{log_text}
"""

def extract_security_report(log_text: str) -> SecurityReport:
    program = LLMTextCompletionProgram.from_defaults(
        output_parser=None,
        output_cls=SecurityReport,
        prompt_template_str=prompt_template_str,
        llm=OpenAI(model="gpt-5.6", temperature=0.0),
    )
    result = program(log_text=log_text)
    return result

if __name__ == "__main__":
    sample_log = """
    Security Review 2027-Q1
    Service: auth-gateway. Critical buffer overflow in token parser. Severity: HIGH. Patch required: upgrade to v3.2.1.
    Service: asset-storage. Permissive S3 CORS configuration. Severity: MEDIUM. Patch required: restrict origin whitelist.
    Overall Compliance Rating: 84.5%
    """
    report = extract_security_report(sample_log)
    print(json.dumps(report.model_dump(), indent=2))
```

### FastMCP 3.1 SSE Server Exposing LlamaIndex Workflows
Connecting LlamaIndex event-driven workflows to FastMCP 3.1 server tools for agentic discovery:

```python
import asyncio
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.openai import OpenAI

# Initialize FastMCP 3.1 Server
mcp = FastMCP("llamaindex-knowledge-server", version="3.1.0")

# In-memory document index store for demonstration
documents = [
    Document(text="FastMCP 3.1 introduces streaming SSE transport and native task protocol execution."),
    Document(text="LlamaIndex v0.12+ provides event-driven Workflows with step function decorators.")
]
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=OpenAI(model="gpt-5.6"))

class SearchInput(BaseModel):
    query: str = Field(..., description="The search query string")
    similarity_top_k: int = Field(default=3, ge=1, le=10)

class SearchResponse(BaseModel):
    query: str
    answer: str
    source_nodes: int

@mcp.tool(
    name="query_knowledge_base",
    description="Query internal LlamaIndex knowledge base using hybrid vector search."
)
async def query_knowledge_base(params: SearchInput) -> SearchResponse:
    res = await query_engine.aquery(params.query)
    return SearchResponse(
        query=params.query,
        answer=str(res),
        source_nodes=len(res.source_nodes)
    )

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

## Related tools / concepts
- [LangChain](langchain.md) — Multi-agent and chain ecosystem.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architectural pattern for retrieval.
- [ChromaDB](../infrastructure/chroma.md) — Vector database integration.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Interoperability standard (FastMCP 3.1).
- [Gemma 4](local_llms.md) — Local frontier model execution.
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — Text-to-SQL and structured context architecture.

## Sources / references
- [LlamaIndex Official Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub Repository](https://github.com/run-llama/llama_index)
- [FastMCP 3.1 & MCP 3.0 Specification](https://modelcontextprotocol.io/spec/3.0)
- [LlamaHub Integrations Directory](https://llamahub.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
