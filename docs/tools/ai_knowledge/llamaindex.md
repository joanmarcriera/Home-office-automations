# LlamaIndex

## What it is
LlamaIndex is a premier data orchestration framework for LLM applications to ingest, structure, search, and retrieve private or domain-specific data. As of January 2027, LlamaIndex (v0.12+) features an event-driven Workflows architecture, native FastMCP 3.1 client/server integration, and full compatibility with frontier models such as **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Gemma 3**.

## What problem it solves
LlamaIndex eliminates the friction of connecting LLMs to disparate enterprise data sources (databases, document management systems, APIs, cloud storage) by providing robust abstractions for data ingestion, vector indexing, hybrid retrieval, and stateful agentic workflows. It automates context window management, chunking strategy selection, and structured metadata extraction, allowing models like **Claude 5.1** or local **Gemma 3** instances to deliver accurately grounded, hallucination-free answers.

## Where it fits in the stack
**Data & RAG Orchestration Layer**. It sits between your storage engine (e.g., [ChromaDB](../../services/chromadb.md), [Milvus](../infrastructure/milvus.md), [Supabase](../infrastructure/supabase.md)) and your AI agents/applications, providing the contextual knowledge layer for [KnowledgeOps](../../knowledge_base/multi_agent_knowledgeops.md) pipelines and [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Advanced RAG Pipelines**: Building multi-hop, hybrid search QA engines over complex PDF, Notion, Slack, and SQL data repositories.
- **Agentic Workflows**: Constructing stateful, event-driven multi-step agents using [LlamaIndex Workflows](https://docs.docs.llamaindex.ai/en/stable/module_guides/workflow/).
- **FastMCP 3.1 Integration**: Serving LlamaIndex query engines or indices as FastMCP tools for multi-agent systems, or using LlamaIndex agents as FastMCP clients.
- **Structured Data Extraction**: Transforming raw, unstructured enterprise documents into validated Pydantic v2 objects for automated downstream storage and routing.

## Strengths
- **Data Centricity**: Built ground-up for data ingestion, indexing, and high-precision retrieval.
- **LlamaHub Ecosystem**: Direct access to hundreds of pre-built data loaders, readers, and vector store adapters.
- **Native FastMCP 3.1 Support**: Seamlessly exposes indices and tools over modern Model Context Protocol standards.
- **Frontier Model Optimization**: Native adapters for **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Gemma 3** (via Ollama or vLLM).
- **Evaluation & Observability**: Native integration with evaluation metrics (faithfulness, relevancy, context precision) and trace exporters (e.g., [LangFuse](../process_understanding/langfuse.md), [OpenTelemetry](../process_understanding/opentelemetry-collector.md)).

## Limitations
- **Workflow Learning Curve**: Event-driven Workflows require moving beyond simple linear chains.
- **Resource Footprint**: High-throughput indexing over millions of documents demands optimized vector stores and dedicated embedding compute.

## When to use it
- When building data-intensive LLM applications requiring complex RAG or knowledge graph retrieval.
- When you need a unified, typed interface to heterogeneous data sources (SQL, NoSQL, APIs, local files).
- For building event-driven AI agents with granular execution, retry, and event routing logic.

## When not to use it
- For lightweight "chat with a single file" utilities where out-of-the-box UIs like [AnythingLLM](anythingllm.md) or [Khoj](../intake_storage/khoj.md) are sufficient.
- For building raw model inference infrastructure (use [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md)).

## Getting started

### 1. Installation
Install core LlamaIndex along with January 2027 standard integrations:

```bash
pip install llama-index-core llama-index-llms-openai llama-index-llms-anthropic llama-index-embeddings-openai llama-index-readers-file pydantic
```

### 2. Event-Driven Workflow Example
A stateful RAG workflow using LlamaIndex Workflows:

```python
import asyncio
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

class EnterpriseRAGWorkflow(Workflow):
    @step
    async def process_query(self, ev: StartEvent) -> StopEvent:
        query = ev.get("query")
        data_dir = ev.get("data_dir", "./data")

        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine(similarity_top_k=5)

        response = await query_engine.aquery(query)
        return StopEvent(result=str(response))

async def main():
    wf = EnterpriseRAGWorkflow(timeout=60.0)
    result = await wf.run(query="What are the main security requirements?", data_dir="./docs")
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
The LlamaIndex CLI enables rapid prototyping, index building, and app scaffolding:

```bash
# Rapidly start an interactive RAG chat over local documents
llamaindex-cli rag --files "./data/*.pdf"

# Scaffold a new LlamaIndex application
llamaindex-cli create-app --name enterprise-data-agent --template workflow-rag

# Inspect available LlamaHub loaders
llamaindex-cli hub list --category readers
```

## API examples

### Pydantic v2 Structured Extraction with LlamaIndex & Claude 5.1
Extracting structured enterprise metadata from raw documents using strict Pydantic v2 schemas:

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.anthropic import Anthropic

class DocumentAnalysis(BaseModel):
    model_config = ConfigDict(frozen=True)

    doc_title: str = Field(description="Title or subject of the document")
    category: str = Field(description="Document taxonomy classification")
    key_entities: List[str] = Field(description="Extracted entities or organization names")
    action_items: List[str] = Field(description="Explicit tasks or action items found")
    risk_score: float = Field(description="Assessed risk score from 0.0 to 1.0")

prompt_template_str = """
Analyze the following document and extract structured metadata:
-------------------
{document_text}
-------------------
"""

program = LLMTextCompletionProgram.from_defaults(
    output_cls=DocumentAnalysis,
    prompt_template_str=prompt_template_str,
    llm=Anthropic(model="claude-5-1-sonnet", temperature=0.0)
)

sample_text = "Q1 Project Launch Plan: Acquired approval from Vertex Corp. Assigning Security Audit to Engineering team by Friday."
structured_output = program(document_text=sample_text)
print(structured_output.model_dump_json(indent=2))
```

### FastMCP 3.1 Tool Registration
Connecting LlamaIndex to FastMCP agentic toolchains:

```python
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import FunctionTool

def query_knowledge_base(topic: str) -> str:
    """Queries enterprise LlamaIndex index for topic information."""
    return f"Retrieved grounded context regarding {topic}."

kb_tool = FunctionTool.from_defaults(fn=query_knowledge_base)

# Initialize Agent Worker with FastMCP / OpenAI compatible function call interface
agent = FunctionCallingAgentWorker.from_tools([kb_tool]).as_agent()
response = agent.chat("Check knowledge base regarding January 2027 compliance updates.")
print(response)
```

## Related tools / concepts
- [LangChain](langchain.md) — Multi-purpose LLM orchestration framework.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Retrieval augmented generation design.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standard protocol for tool/resource streaming.
- [ChromaDB](../../services/chromadb.md) — Open-source vector database.
- [LlamaParse](../intake_storage/llamaparse.md) — GenAI-native document parsing.
- [Unstructured](../intake_storage/unstructured.md) — Partitioning complex document formats.
- [Gemma 3](local_llms.md) — Open frontier model family.

## Sources / references
- [LlamaIndex Official Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub Repository](https://github.com/run-llama/llama_index)
- [LlamaHub Data Connectors](https://llamahub.ai/)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
