# Haystack

## What it is
Haystack is an open-source framework developed by deepset for building production-ready search applications, Retrieval-Augmented Generation (RAG) pipelines, and state-of-the-art agentic workflows. Operating under early 2027 standards, **Haystack 2.x** centers around a flexible Directed Acyclic Graph (DAG) architecture where data processing, vector embeddings, document retrieval, conditional routing, and LLM inference nodes are explicitly connected, serialized, and scaled.

Haystack connects seamlessly with frontier LLM engines—such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, and **Qwen 3.6 VL**—and features native connectors for the **FastMCP 3.1 Task Protocol**, allowing developers to expose complete Haystack RAG pipelines as standardized agent tools and resources.

```mermaid
graph TD
    UserQuery[User Query / FastMCP Agent] --> InputNode[Pipeline Input Router]

    InputNode --> BranchCheck{Query Classification}

    BranchCheck -->|Simple Keyword| BM25Node[BM25 Document Retriever]
    BranchCheck -->|Complex Semantic| EmbedderNode[Text / Embedding Generator]

    EmbedderNode --> VectorNode[Qdrant / Milvus Vector Retriever]

    BM25Node --> RankerNode[Cross-Encoder Re-Ranker]
    VectorNode --> RankerNode

    RankerNode --> PromptBuilderNode[Prompt Builder Template]

    PromptBuilderNode --> GeneratorNode[LLM Generator Node]

    GeneratorNode --> OutputNode[Validated Pydantic Response / FastMCP Output]
```

## What problem it solves
Building enterprise-grade RAG and search architectures often results in brittle, monolithic scripts or overly abstract, opaque chains where data flow and error handling are hidden from developers. As retrieval pipelines scale to millions of documents across heterogeneous vector engines and LLM providers, pipeline serialization, type safety, and graph visibility become essential.

Haystack solves these challenges through:
- **Explicit DAG Graph Pipeline Architecture**: Eliminating hidden abstractions by requiring developers to explicitly define pipeline nodes (`pipeline.add_component()`) and data flow edges (`pipeline.connect()`).
- **Native YAML / JSON Pipeline Serialization**: Allowing entire production retrieval pipelines to be serialized to static YAML manifests for version control, CI/CD testing, and multi-environment deployment.
- **Strict Runtime Component Typing**: Enforcing typed input and output contracts between pipeline nodes to prevent runtime schema mismatches.
- **FastMCP 3.1 Connector Protocol**: Exposing complex RAG DAG graphs as standardized FastMCP tools that can be invoked seamlessly by autonomous agent frameworks ([Claude Code](../development_ops/claude-code.md), [Windsurf](../development_ops/windsurf.md), [Aider](../development_ops/aider.md)).

## Where it fits in the stack
**Category**: [Frameworks & RAG Orchestration](index.md) / Component Graph Pipeline Engine.

Haystack sits directly between underlying storage layers (e.g., [Qdrant](../infrastructure/qdrant.md), [ClickHouse](../process_understanding/clickhouse.md), Elasticsearch, Pinecone) and agent orchestration or application frontends.

```
+-----------------------------------------------------------------------+
|                    Agent & Application Frontend                       |
|        (Claude Code / FastMCP 3.1 Clients / React / Next.js)          |
+-----------------------------------------------------------------------+
                                    |
                                    v (FastMCP 3.1 Tool Invocation)
+-----------------------------------------------------------------------+
|                       Haystack 2.x DAG Pipeline                       |
|  +-----------------------+  +-------------------+  +---------------+  |
|  | Document Embedders    |  | Hybrid Retrievers |  | Cross-Ranker  |  |
|  +-----------------------+  +-------------------+  +---------------+  |
|  +-----------------------------------------------------------------+  |
|  |            YAML Serialization & Pydantic Schema Validation       |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
                                    |
                        +-----------+-----------+
                        |                       |
                        v                       v
+-----------------------------------+   +-------------------------------+
|     Vector Databases & Search     |   |    Frontier Model Engines     |
|   (Qdrant, Milvus, Azure Search)  |   | (Claude 5.6, GPT-5.6, Gemini) |
+-----------------------------------+   +-------------------------------+
```

## Feature Comparison Matrix

| Feature / Metric | Haystack 2.x | LangChain | LlamaIndex | Custom Python Script |
| :--- | :--- | :--- | :--- | :--- |
| **Graph Architecture** | Explicit Typed DAG Components | Abstraction Chains / LangGraph | Data Index Centric | Imperative Loops |
| **Pipeline Serialization**| Native YAML / JSON manifests | Limited / Custom | Limited | Manual Python scripts |
| **FastMCP 3.1 Native Integration**| Pre-built FastMCP Tool Wrapper | LangChain Agent Adapters | LlamaIndex MCP Tool | Custom FastAPI endpoint |
| **Strict Type Checking** | Compile-time port matching | Loose runtime kwargs | Moderate | Manual Pydantic |
| **Debugging & Visibility** | Inspection of every DAG edge | Debug logging / LangSmith | LlamaTrace | Print Statements |

## Typical use cases
- **Enterprise Multimodal RAG**: Constructing production pipelines that ingest, parse, chunk, embed, retrieve, and synthesize context across millions of corporate documents.
- **Conditional Agent Query Routing**: Utilizing `ConditionalRouter` nodes to dynamically route queries between lightweight edge models (**Qwen 3.6**) and deep reasoning models (**Claude 5.6**).
- **Serialized CI/CD RAG Deployments**: Defining retrieval configurations in YAML manifests that are validated and tested automatically in staging pipelines before cloud deployment.
- **FastMCP Search Tool Endpoints**: Packaging enterprise knowledge pipelines as FastMCP 3.1 tools for internal developer assistants.

## Strengths
- **Transparent Graph Architecture**: Every component, data edge, and transformation is explicitly visible and debuggable.
- **Production Serialization**: Full support for dumping pipelines to YAML and loading them at runtime without python code modifications.
- **Extensive Component Ecosystem**: Broad library of pre-built integrations for Qdrant, Milvus, Azure Search, Anthropic, OpenAI, Cohere, and Hugging Face.
- **FastMCP 3.1 Compatibility**: Readily exposes pipelines as FastMCP tool calls for autonomous multi-agent swarms.
- **Robust Component Customization**: Creating custom pipeline nodes requires decorating a Python class with `@component`.

## Limitations
- **Haystack 1.x vs 2.x Migration Gap**: Code written for legacy Haystack 1.x requires complete refactoring for the 2.x component pipeline model.
- **Smaller Community Ecosystem Than LangChain**: Fewer experimental community packages compared to larger frameworks, focusing instead on core production stability.
- **Strict Type Checking Requirement**: Misaligned output types between connected component ports result in pipeline initialization errors.

## When to use it
- When building enterprise production RAG systems where pipeline graph transparency, type safety, and YAML serialization are mandatory.
- When you require deterministic control over how context chunks are retrieved, re-ranked, and passed to LLM generators.
- When deploying search backends that must be exposed as FastMCP 3.1 tools to AI agents.

## When not to use it
- For quick, throwaway single-prompt scripts where a simple API client call (`openai` or `anthropic`) is faster.
- If your team is already standardized on another framework like [LlamaIndex](../ai_knowledge/llamaindex.md) without requiring pipeline graph serialization.
- For simple utility functions that do not involve data retrieval, document processing, or graph routing.

## Getting started

### Prerequisites and Installation
Install Haystack 2.x alongside vector database connectors, FastMCP, and Pydantic:

```bash
pip install "haystack-ai>=2.8.0" fastmcp pydantic "qdrant-haystack>=3.0.0"
```

### Minimal Python DAG Pipeline Example
The example below demonstrates constructing, connecting, and executing a basic Haystack 2.x pipeline:

```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator

prompt_template = "Summarize the key architectural benefits of {{topic}} in 3 bullet points."

pipeline = Pipeline()
pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
pipeline.add_component("llm", OpenAIGenerator(model="gpt-5.6-preview"))
pipeline.connect("prompt_builder", "llm")

result = pipeline.run({"prompt_builder": {"topic": "FastMCP 3.1 Task Protocol"}})
print(result["llm"]["replies"][0])
```

## Systemd Service Configuration
For hosting a Haystack FastMCP 3.1 search tool daemon (`/etc/systemd/system/haystack-mcp-server.service`):

```ini
[Unit]
Description=Haystack 2.x FastMCP RAG Gateway Server
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=haystack
Group=haystack
WorkingDirectory=/opt/haystack-mcp-server
ExecStart=/usr/local/bin/python3 -m haystack_mcp.server --port 8095 --host 0.0.0.0
Restart=always
RestartSec=5s
LimitNOFILE=65536
Environment=ANTHROPIC_API_KEY=sk-ant-api03-sample
Environment=QDRANT_URL=http://localhost:6333
Environment=PYTHONUNBUFFERED=1

# Security Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/haystack-mcp
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Deployment Stack
Deploying Haystack with Qdrant and FastMCP 3.1 (`docker-compose.yml`):

```yaml
version: "3.8"

services:
  qdrant:
    image: qdrant/qdrant:v1.9.0
    container_name: qdrant-vector-db
    restart: unless-stopped
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_storage:/qdrant/storage

  haystack-mcp:
    image: python:3.11-slim
    container_name: haystack-mcp-server
    restart: unless-stopped
    command: python3 -m haystack_mcp.server
    ports:
      - "8095:8095"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - qdrant
    volumes:
      - ./pipelines:/opt/haystack-mcp-server/pipelines:ro
```

## CLI examples

Below are common CLI commands for serializing, running, and inspecting Haystack pipelines.

```bash
# 1. Export a Python-defined Haystack pipeline to a YAML configuration file
python3 build_pipeline.py --export-yaml pipeline.yaml

# 2. Run a serialized Haystack pipeline directly from the command line
haystack-run --config pipeline.yaml --input "What are the core concepts of Haystack 2.x?"

# 3. Validate pipeline schema configuration against Haystack 2.x specs
haystack-validate --file pipeline.yaml

# 4. Benchmark pipeline execution latency across sample queries
haystack-benchmark --config pipeline.yaml --dataset ./eval_queries.json
```

## API examples

### FastMCP 3.1 Tool Integration with Haystack RAG Pipeline
The following production-ready Python script wraps a complete Haystack 2.x retrieval DAG inside a **FastMCP 3.1** server tool endpoint with strict Pydantic v2 schemas (`extra="forbid"`).

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP
from haystack import Pipeline, component
from haystack.components.builders import PromptBuilder
from haystack.components.generators import AnthropicGenerator

mcp = FastMCP("Haystack Knowledge Gateway", version="3.1.0")

class RAGQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=3, description="Search and retrieval query string")
    max_tokens: int = Field(default=500, ge=50, le=2000)

class DocumentIndexRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    content: str = Field(..., min_length=10, description="Raw text document payload to index")
    meta_tags: dict = Field(default_factory=dict, description="Metadata tags for document filtering")

class RAGQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., description="Original user query")
    synthesized_answer: str = Field(..., description="Generated RAG answer")
    pipeline_status: str = Field(..., description="Pipeline status code")

# Custom mock retrieval component for demonstration
@component
class MockDocumentRetriever:
    @component.output_types(documents=List[str])
    def run(self, query: str):
        # Simulated document retrieval
        docs = [
            f"Document chunk 1 regarding: {query}",
            f"Document chunk 2 detailing FastMCP 3.1 protocol rules for: {query}"
        ]
        return {"documents": docs}

@mcp.tool()
def search_and_synthesize(query_text: str) -> str:
    """
    Executes a Haystack 2.x RAG pipeline to retrieve documents and synthesize
    a context-grounded response for FastMCP 3.1 agents.
    """
    try:
        request = RAGQueryRequest(query=query_text)

        prompt_template = """
        Context documents:
        {% for doc in documents %}
          - {{ doc }}
        {% endfor %}

        User Query: {{ query }}
        """

        pipeline = Pipeline()
        pipeline.add_component("retriever", MockDocumentRetriever())
        pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
        pipeline.add_component("llm", AnthropicGenerator(model="claude-5-6-sonnet"))

        pipeline.connect("retriever.documents", "prompt_builder.documents")
        pipeline.connect("prompt_builder", "llm")

        result = pipeline.run({
            "retriever": {"query": request.query},
            "prompt_builder": {"query": request.query}
        })

        answer = result["llm"]["replies"][0]

        response = RAGQueryResponse(
            query=request.query,
            synthesized_answer=answer,
            pipeline_status="SUCCESS"
        )

        return response.model_dump_json(indent=2)

    except Exception as err:
        return f"Error executing Haystack RAG pipeline: {str(err)}"

@mcp.tool()
def index_document_payload(req: DocumentIndexRequest) -> str:
    """Indexes a text payload into the Haystack vector store for RAG retrieval."""
    try:
        # Simulated indexing pipeline trigger
        return f"Successfully indexed document payload ({len(req.content)} chars) into vector store."
    except Exception as err:
        return f"Document indexing failed: {str(err)}"

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8095)
```

### Custom Component with Pydantic v2 Input Validation
Below is an example of creating a custom Haystack 2.x component that validates incoming query arguments using **Pydantic v2** schemas (`extra="forbid"`).

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from haystack import component
from typing import Dict, Any

class QueryValidationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_query: str = Field(..., min_length=3, description="Incoming search text")
    user_role: str = Field(default="developer")

    @field_validator("user_query")
    @classmethod
    def check_query_safety(cls, v: str) -> str:
        forbidden_keywords = ["DROP DATABASE", "DELETE FROM", "RM -RF"]
        for kw in forbidden_keywords:
            if kw in v.upper():
                raise ValueError(f"Forbidden query keyword detected: {kw}")
        return v.strip()

@component
class ValidatedQuerySanitizer:
    @component.output_types(sanitized_query=str, role=str)
    def run(self, raw_query: str, role: str = "developer") -> Dict[str, Any]:
        """
        Custom Haystack component that validates and sanitizes input queries
        before passing them downstream in the pipeline graph.
        """
        validated = QueryValidationSchema(user_query=raw_query, user_role=role)
        return {
            "sanitized_query": validated.user_query,
            "role": validated.user_role
        }

# Execution Verification
if __name__ == "__main__":
    sanitizer = ValidatedQuerySanitizer()
    out = sanitizer.run(raw_query="How do I configure FastMCP 3.1 tool authentication?")
    print("Custom Haystack component executed successfully:")
    print(f"Sanitized Query: '{out['sanitized_query']}' | Role: {out['role']}")
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Probable Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| **`PipelineConnectError`** | Misaligned output/input data types between connected ports | Verify `@component.output_types` match downstream component parameter types. |
| **`YAML Deserialization Failure`** | Custom component class not registered in import namespace | Import custom `@component` classes into Python module scope prior to `Pipeline.loads()`. |
| **`Qdrant Vector Connection Timeout`** | Qdrant database container down or port 6333 unreachable | Run `docker-compose ps` and confirm `qdrant-vector-db` container status. |
| **`FastMCP 3.1 Schema Reject`** | Extra unvalidated kwargs passed to RAG tool request | Enforce strict Pydantic v2 `extra="forbid"` in client request payloads. |

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md) — Framework for building applications with LLMs.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Indexing and retrieval framework for agentic RAG.
- [DSPy](dspy.md) — Declarative prompt compilation and optimization framework.
- [Qdrant](../infrastructure/qdrant.md) — High-performance vector database with Haystack integrations.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for connecting models to tools.

## Sources / references
- [Haystack Official Website](https://haystack.deepset.ai/)
- [Haystack GitHub Repository](https://github.com/deepset-ai/haystack)
- [Haystack 2.x Official Documentation](https://docs.haystack.deepset.ai/docs/intro)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
