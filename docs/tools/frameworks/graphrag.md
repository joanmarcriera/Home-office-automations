# GraphRAG

## What it is
GraphRAG is a Graph-based Retrieval Augmented Generation framework developed by Microsoft and the open-source community that combines knowledge graph construction with Large Language Models (LLMs) to perform complex, multi-hop reasoning over unstructured text. As of early January 2027, GraphRAG supports **FastMCP 3.1** protocol schemas, integrated hierarchical community summarization, and direct multi-hop vector-graph hybrid queries powered by frontier models like [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), DeepSeek-V4, Qwen 3.6 VL, and [Gemma 4](../ai_knowledge/local_llms.md).

## What problem it solves
Traditional baseline RAG (vector similarity search) struggles with global dataset comprehension, semantic query aggregation across disconnected documents, and multi-step relational reasoning. GraphRAG solves these limitations by automatically extracting entities, relationships, and claims to construct a structured knowledge graph, organizing graph nodes into hierarchical communities, and pre-generating multi-level summaries. This enables models to answer holistic, thematic queries (e.g., "What are the main themes across all company audit reports?") that baseline vector retrieval cannot resolve.

## Where it fits in the stack
**Category**: Frameworks & Retrieval Systems. GraphRAG sits between raw document storage and AI agents/reasoning engines. It functions as an advanced retrieval orchestration layer, feeding structured graph contexts and community summaries into LLMs via standardized interfaces or MCP resource endpoints.

## Typical use cases
- **Multi-Hop Knowledge Discovery**: Executing complex queries that require traversing multi-step entity relationships (e.g., "How do regulatory changes in EU AI policy impact our supply chain partners?").
- **Global Document Summarization**: Generating holistic thematic summaries across large, unorganized text document corpora.
- **Enterprise Intelligence & Fraud Detection**: Mapping complex networks of corporate entities, transactions, and leadership connections for risk assessment.
- **Agentic Knowledge Augmentation**: Serving as a rich, structured graph backend for autonomous agent workflows running via [FastMCP 3.1](../automation_orchestration/mcp.md).

## Strengths
- **Superior Global Query Answering**: Delivers unprecedented answer quality on holistic and high-level synthesis questions compared to naive vector search.
- **Structured Relational Context**: Preserves entity connections, claims, and semantic relationships explicitly in graph structures.
- **Hierarchical Summarization**: Auto-groups graph elements into multi-tiered communities for granular or macro-level context injection.
- **MCP Native Integration**: Seamlessly exposes graph retrieval endpoints to agentic runtimes using FastMCP 3.1 Task Protocol schemas.

## Limitations
- **High Ingestion Cost & Latency**: Knowledge graph extraction and community summarization require extensive LLM calls during indexing.
- **Graph Maintenance Overhead**: Updating graph nodes incrementally as source documents change requires careful graph maintenance strategy.
- **Domain Tuning Required**: Optimal entity and relationship extraction prompts often need customized schema definitions for specialized domains.

## When to use it
- When your application requires answering global questions over large document collections.
- When query accuracy depends on understanding multi-hop relationships between entities.
- When building domain knowledge bases where structural context and claim verification are critical.

## When not to use it
- For basic factual retrieval over small document collections where traditional vector RAG is sufficient and cheaper.
- When immediate zero-latency document indexing is required without pre-computation budget.

## Getting started
### Installation
Install GraphRAG via pip:
```bash
pip install graphrag pydantic>=2.0.0
```

### Initializing a GraphRAG Workspace
```bash
graphrag init --root ./graphrag_workspace
```

## CLI examples
### Indexing a Dataset
```bash
graphrag index --root ./graphrag_workspace
```

### Executing a Global Search Query
```bash
graphrag query --root ./graphrag_workspace --method global "What are the key technological shifts described in the reports?"
```

### Executing a Local Entity-Centric Search Query
```bash
graphrag query --root ./graphrag_workspace --method local "What are the main risks associated with Entity X?"
```

## API examples
The following Python example demonstrates executing GraphRAG queries and validating structured search responses using **Pydantic v2** schemas.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class GraphEntity(BaseModel):
    name: str = Field(..., description="Entity name")
    type: str = Field(..., description="Entity classification type")
    description: Optional[str] = Field(None, description="Extracted entity summary")

class GraphSearchResult(BaseModel):
    query: str = Field(..., description="The query string executed")
    response: str = Field(..., description="Synthesized graph answer")
    extracted_entities: List[GraphEntity] = Field(default_factory=list, description="Entities involved in multi-hop reasoning")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Response confidence score")

async def mock_graphrag_search(query_str: str) -> dict:
    # Simulated GraphRAG hybrid retrieval response payload
    return {
        "query": query_str,
        "response": "GraphRAG multi-hop reasoning identified key regulatory impacts originating from EU AI Directives affecting enterprise software vendors.",
        "extracted_entities": [
            {"name": "EU AI Directive", "type": "Regulation", "description": "European Union Artificial Intelligence Governance Framework"},
            {"name": "Enterprise Vendor X", "type": "Organization", "description": "Global software provider"}
        ],
        "confidence_score": 0.94
    }

async def main():
    raw_response = await mock_graphrag_search("Analyze regulatory impact across vendors")
    try:
        validated_result = GraphSearchResult.model_validate(raw_response)
        print("GraphRAG query execution verified with Pydantic v2:")
        print(f"Query: {validated_result.query}")
        print(f"Confidence: {validated_result.confidence_score}")
        print(f"Answer: {validated_result.response}")
        print(f"Entities Found: {len(validated_result.extracted_entities)}")
    except ValidationError as e:
        print(f"Validation error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [LlamaIndex](llamaindex.md) — Framework supporting knowledge graph index abstractions.
- [LangChain](langchain.md) — Modular framework for RAG and graph retrieval pipelines.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for exposing graph resources to agents.
- [Neo4j](../infrastructure/milvus.md) — Graph database backend options for enterprise scale.
- [RAG Patterns](../../knowledge_base/patterns/rag.md) — Architectural patterns for retrieval augmented generation.

## Sources / references
- [GraphRAG Python Multi-Hop Reasoning](https://thenewstack.io/graphrag-multi-hop-reasoning-python/)
- [Microsoft GraphRAG Documentation](https://microsoft.github.io/graphrag/)
- [Microsoft GraphRAG GitHub Repository](https://github.com/microsoft/graphrag)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
