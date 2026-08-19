# Haystack

## What it is
Haystack is an end-to-end open-source framework for building production-ready search, Retrieval-Augmented Generation (RAG), and agentic applications powered by LLMs and vector search engines. Developed by deepset, Haystack 2.x provides a flexible DAG (Directed Acyclic Graph) architecture to construct, serialize, and scale modular AI pipelines.

## What problem it solves
Haystack simplifies the complexity of enterprise RAG and conversational search pipelines by providing standardized, loosely coupled components for document parsing, embedding, vector retrieval, conditional routing, and response generation. Its explicit pipeline graph paradigm eliminates opaque abstractions, making data flow, error handling, and model switching (**Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**) transparent and reproducible.

## Where it fits in the stack
**Framework / RAG Orchestration Layer**. Haystack sits between storage engines (e.g., [Qdrant](../infrastructure/qdrant.md), [ClickHouse](../process_understanding/clickhouse.md), Elasticsearch) and frontier LLM providers. In early 2027 architectures, Haystack pipelines serve as robust retrieval backends for [FastMCP 3.1](../automation_orchestration/mcp.md) servers and enterprise knowledge management applications.

## Typical use cases
- **Enterprise Semantic Search & RAG**: Constructing scalable RAG pipelines over millions of unstructured corporate documents.
- **Agentic Routing Pipelines**: Utilizing `ConditionalRouter` components to dynamically route queries between fast local models (**Qwen 3.8**) and frontier reasoning models (**Claude 5.1**).
- **Structured Metadata Extraction**: Processing unstructured documents into validated Pydantic v2 schemas.
- **FastMCP Tool Integration**: Exposing Haystack pipelines as standardized MCP tools and resources for external agent frameworks.

## Strengths
- **Explicit DAG Pipeline Design**: Clear graph topology (`pipeline.add_component()` and `pipeline.connect()`) ensuring total visibility into data transformations.
- **Pipeline Serialization**: Native serialization to YAML or JSON for reproducible deployments across CI/CD environments.
- **Haystack 2.x Architecture**: Modern, highly performant component model with explicit runtime input/output typing.
- **FastMCP 3.1 Compatibility**: Seamless connection with FastMCP tool servers for resource retrieval and execution.
- **Robust Component Ecosystem**: Extensive connectors for vector databases, embedding models, and frontier LLMs.

## Limitations
- **Ecosystem Scale vs. LangChain**: Smaller community ecosystem for experimental edge cases compared to LangChain.
- **Migration Effort**: Code written for legacy Haystack 1.x requires complete restructuring for the 2.x component pipeline architecture.
- **Strict Typing Discipline**: Explicit component connections require careful adherence to type contracts between pipeline nodes.

## When to use it
- When building production-grade enterprise RAG systems requiring strict architectural control and serialization.
- When you prefer explicit component graphs over implicit, magic wrapper chains.
- When deploying production pipelines that must be defined in YAML and validated via strict schema checks.

## When not to use it
- For quick, single-file exploratory prompt scripts where a simple API client call is sufficient.
- If your team is already standardized on another framework like [LlamaIndex](../ai_knowledge/llamaindex.md) without requiring pipeline graph serialization.
- For non-retrieval applications that do not involve data processing, embedding, or graph routing.

## Getting started

### Installation
Install Haystack AI with standard components:

```bash
pip install "haystack-ai>=2.8.0" "pydantic>=2.10.0"
```

### Minimal Python Example (DAG Pipeline)
```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator

prompt_template = "Summarize the key architectural advantages of {{framework_name}} in bullet points."

pipeline = Pipeline()
pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
pipeline.add_component("llm", OpenAIGenerator(model="gpt-5.5-preview"))
pipeline.connect("prompt_builder", "llm")

result = pipeline.run({"prompt_builder": {"framework_name": "Haystack 2.x"}})
print(result["llm"]["replies"][0])
```

## CLI examples

```bash
# Export a python-defined pipeline to YAML configuration
python3 my_pipeline.py --export-yaml pipeline.yaml

# Run a serialized Haystack pipeline from the command line
haystack-run --config pipeline.yaml --input "What is FastMCP 3.1?"

# Validate pipeline schema configuration
haystack-validate --file pipeline.yaml
```

## API examples

### Custom Haystack Component with Pydantic v2 Validation
```python
from pydantic import BaseModel, Field, field_validator
from haystack import component

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Search query string")
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        if "DROP TABLE" in v.upper():
            raise ValueError("Forbidden query syntax detected.")
        return v.strip()

@component
class ValidatedQueryProcessor:
    @component.output_types(query=str, top_k=int)
    def run(self, query: str, top_k: int = 5):
        validated = QueryRequest(query=query, top_k=top_k)
        return {"query": validated.query, "top_k": validated.top_k}
```

### Conditional Routing Pipeline with Claude 5.1 Integration
```python
from haystack import Pipeline
from haystack.components.routers import ConditionalRouter
from haystack.components.generators import AnthropicGenerator

routes = [
    {
        "condition": "{{query|length > 100}}",
        "output": "{{query}}",
        "output_name": "complex_query",
        "output_type": str,
    }
]

router = ConditionalRouter(routes=routes)
claude_generator = AnthropicGenerator(model="claude-5-1-sonnet-20261022")

pipeline = Pipeline()
pipeline.add_component("router", router)
pipeline.add_component("claude", claude_generator)
pipeline.connect("router.complex_query", "claude.prompt")
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md) — Comprehensive framework for LLM applications.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Knowledge-centric indexing and RAG framework.
- [DSPy](dspy.md) — Declarative prompt and pipeline optimizer.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Tool and resource protocol standard.
- [Qdrant](../infrastructure/qdrant.md) — High-performance vector database often paired with Haystack.
- [RAG Patterns](../../knowledge_base/patterns/rag-pattern.md) — Enterprise RAG architectural patterns.

## Sources / references
- [Haystack Official Website](https://haystack.deepset.ai/)
- [Haystack GitHub Repository](https://github.com/deepset-ai/haystack)
- [Haystack 2.x Documentation](https://docs.haystack.deepset.ai/docs/intro)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
