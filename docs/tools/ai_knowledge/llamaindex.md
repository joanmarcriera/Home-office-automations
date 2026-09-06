# LlamaIndex

## What it is
LlamaIndex is an open-source data framework for building LLM applications, retrieval-augmented generation (RAG) systems, and autonomous data agents. As of early 2027, LlamaIndex (v0.12+) features event-driven Workflows, native support for **FastMCP 3.1** and the **MCP 3.0 Task Protocol**, and seamless integration with frontier models including [Claude 5.6](../providers/anthropic.md), [GPT-5.6](openai.md), [Gemini 4.0 Ultra](gemini.md), [DeepSeek-V4](deepseek-r1.md), [Qwen 3.6 VL](qwen.md), and [Gemma 4](local_llms.md).

## What problem it solves
Simplifies connecting LLMs to private and heterogeneous data sources (PDFs, SQL databases, Notion, vector stores, APIs). It abstracts context window optimization, document parsing, embedding generation, chunking strategies, and multi-hop retrieval pipelines while eliminating brittle custom ingestion logic.

## Where it fits in the stack
**Data Framework / Context Orchestration Layer**. It sits between raw enterprise or local storage repositories and high-level agent frameworks or applications, acting as the primary retrieval and context ingestion engine for [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) pipelines.

## Typical use cases
- **Modular RAG Pipelines**: Building question-answering systems over unstructured and structured document collections.
- **Stateful Agentic Workflows**: Creating multi-step, stateful agents using event-driven LlamaIndex Workflows.
- **FastMCP 3.1 Integration**: Exposing LlamaIndex tools or querying remote MCP servers using standardized task protocols.
- **Structured Data Extraction**: Transforming raw documents into strictly validated Pydantic v2 objects for automated workflows and [Data Copilot](../../architecture/data-copilot-text-to-sql.md) systems.

## Strengths
- **Data Centricity**: Built from the ground up for data loading, indexing, and retrieval across hundreds of LlamaHub integrations.
- **Workflows Architecture**: Event-driven execution model replacing rigid legacy chains with explicit state management.
- **Native FastMCP 3.1 & MCP 3.0 Support**: Out-of-the-box MCP client and server capabilities for agentic tool discovery.
- **Frontier Model Optimization**: Native support for Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL, and local Gemma 4 models via Ollama or vLLM.
- **Built-in Evaluation**: Comprehensive suite for measuring retrieval context precision, recall, and response faithfulness.

## Limitations
- **Workflow Learning Curve**: Migrating from early `VectorStoreIndex` patterns to event-driven `Workflow` state machines requires explicit step design.
- **Resource Footprint**: High-throughput vector indexing and local embedding models require adequate GPU/RAM resources or managed vector stores like [ChromaDB](../infrastructure/chroma.md).

## When to use it
- When building data-intensive LLM applications requiring complex RAG, hybrid search, or knowledge graph querying.
- When unifying multi-source data ingestion into a standardized retrieval interface.
- When creating stateful AI agents that need transparent control over multi-step execution flows.

## When not to use it
- For quick, out-of-the-box file-chat GUIs without custom development (use [AnythingLLM](anythingllm.md) or [Khoj](../intake_storage/khoj.md)).
- When serving low-level LLM model weights directly (use [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md)).

## Getting started

### Installation
Install LlamaIndex core and standard provider integrations:

```bash
pip install llama-index-core llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file pydantic
```

### Basic Workflow Example
A minimal event-driven RAG workflow:

```python
import asyncio
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

class RAGWorkflow(Workflow):
    @step
    async def ingest_and_query(self, ev: StartEvent) -> StopEvent:
        query_text = ev.get("query", "Summarize key findings")
        documents = SimpleDirectoryReader("./data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(query_text)
        return StopEvent(result=str(response))

async def main():
    w = RAGWorkflow()
    result = await w.run(query="What are the key takeaways?")
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
The LlamaIndex CLI enables rapid indexing and RAG execution directly from the shell:

```bash
# Ingest a directory and query via CLI
llamaindex-cli rag --files "./data/*.pdf" --query "Summarize the quarterly goals"

# Create a new LlamaIndex application boilerplate
llamaindex-cli create-app --name my-data-agent --template high-fidelity-rag

# List available loaders on LlamaHub
llamaindex-cli hub list --category readers
```

## API examples

### Structured Extraction with Pydantic v2
Extracting validated metadata using LlamaIndex and Pydantic v2:

```python
from pydantic import BaseModel, Field
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.openai import OpenAI

class DocumentSummary(BaseModel):
    title: str = Field(description="Title of the document")
    key_topics: list[str] = Field(description="Key topics discussed")
    action_items: list[str] = Field(default_factory=list, description="Extracted action items")

prompt_template_str = """\
Extract structured information from the text below.
Text: {text}
"""

program = LLMTextCompletionProgram.from_defaults(
    output_parser=None,
    output_cls=DocumentSummary,
    prompt_template_str=prompt_template_str,
    llm=OpenAI(model="gpt-5.6"),
)

result = program(text="Project Alpha kickoff: Complete API contract review by Friday. Lead: Sarah.")
print(result.model_dump_json(indent=2))
```

### FastMCP 3.1 Tool Integration
Connecting LlamaIndex agents to FastMCP servers:

```python
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.tools.mcp import MCPToolSpec

# Connect to FastMCP server endpoint
mcp_spec = MCPToolSpec(server_url="http://localhost:8000/mcp")
tools = mcp_spec.to_tool_list()

agent = FunctionCallingAgentWorker.from_tools(tools).as_agent()
response = agent.chat("Search the internal knowledge base for the 2027 security protocol.")
print(response)
```

## Related tools / concepts
- [LangChain](langchain.md) — Multi-agent and chain ecosystem.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architectural pattern for retrieval.
- [ChromaDB](../infrastructure/chroma.md) — Vector database integration.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Interoperability standard.
- [Gemma 4](local_llms.md) — Local frontier model.

## Sources / references
- [LlamaIndex Official Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub Repository](https://github.com/run-llama/llama_index)
- [FastMCP 3.1 & MCP 3.0 Specification](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
