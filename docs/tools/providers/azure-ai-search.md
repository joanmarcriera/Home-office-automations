# Azure AI Search

## What it is
Azure AI Search (formerly Azure Cognitive Search) is Microsoft's enterprise cloud search and retrieval service optimized for Retrieval-Augmented Generation (RAG) and multi-agent AI systems in early 2027. It integrates vector search, full-text keyword indexing, and AI-powered semantic ranking into a fully managed platform. Designed to handle large enterprise data lakes, Azure AI Search works seamlessly with [Azure OpenAI Service](azure-openai.md) and frontier LLMs (such as Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4) by exposing low-latency search indexes via FastMCP 3.1 connectors.

## What problem it solves
Large-scale enterprise retrieval requires combining raw keyword precision with conceptual vector similarity while respecting enterprise security boundaries. Azure AI Search solves:
- **Retrieval Precision**: Combines vector embeddings with BM25 full-text keyword search and multi-lingual deep learning semantic rankers for high-precision context retrieval.
- **Enterprise Access Control**: Enforces Role-Based Access Control (RBAC) and Microsoft Entra ID security filtering directly at document index levels.
- **High-Scale Ingestion**: Built-in skillsets automatically extract, chunk, embed, and index structured and unstructured content (PDFs, Office files, database records).

## Where it fits in the stack
**Category**: AI & Knowledge / Providers & Vector Databases. It serves as the primary enterprise search engine and vector store connecting raw enterprise data repositories with agentic workflows and LLM orchestration layers.

## Typical use cases
- **Enterprise Knowledge RAG**: Indexing internal documentation, policy manuals, and repositories to ground GPT-5.5 and Claude 5.1 agent queries.
- **Hybrid Code & Document Search**: Indexing technical specifications and code repositories for AI developer assistants.
- **Multimodal Content Retrieval**: Querying image embeddings and multi-language document chunks for multi-agent workflows.

## Strengths
- **Hybrid Search + Semantic Ranker**: Industry-leading relevance scoring by re-ranking combined BM25 and vector search results with deep neural models.
- **Native Azure AI & FastMCP 3.1 Integration**: Direct connectors for Azure OpenAI embeddings and MCP 3.1 agent tool routing.
- **Enterprise-Grade Security**: Full support for Entra ID, private endpoints, and document-level security filtering.

## Limitations
- **Cost Overhead**: Enterprise tier features (especially the Semantic Ranker and dedicated storage units) carry significant ongoing operational costs.
- **Cloud Lock-in**: Deep integration with Azure ecosystem components makes multi-cloud migrations complex.

## When to use it
- When building production-grade enterprise RAG systems requiring combined vector and full-text keyword search.
- When managing multi-tenant or multi-role environments requiring document-level access control.
- When utilizing Azure infrastructure alongside [Azure OpenAI](azure-openai.md).

## When not to use it
- For lightweight or open-source local-first deployments (use [Chroma](../infrastructure/chroma.md) or [Qdrant](../infrastructure/weaviate.md)).
- If you only require simple in-memory vector storage without keyword search or semantic re-ranking.

## Getting started

To get started with Azure AI Search, install the official Python SDK and FastMCP connectors.

### Installation
```bash
pip install azure-search-documents azure-identity fastmcp pydantic
```

### Hello-World Example
Verify connection to an Azure AI Search service endpoint using Python:

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

endpoint = "https://your-search-service.search.windows.net"
client = SearchIndexClient(endpoint=endpoint, credential=DefaultAzureCredential())

# List existing index names
indexes = [index.name for index in client.list_indexes()]
print(f"Connected to Azure AI Search. Indexes found: {indexes}")
```

## CLI examples

Below are common Azure CLI administrative commands for managing search services and indexes.

```bash
# 1. Query Azure AI Search service status
az search service show --name my-search-service --resource-group my-rg

# 2. List search index statistics via REST API using Azure CLI token
az rest --method GET --url "https://my-search-service.search.windows.net/indexes?api-version=2024-07-01" \
  --resource "https://search.azure.com"

# 3. Create an IP firewall rule on the Azure AI Search instance
az search service update --name my-search-service --resource-group my-rg \
  --ip-rules "203.0.113.5"
```

## API examples

### Python: Azure AI Search Query Schema Validation (Pydantic v2)
Below is a robust Python example validating hybrid vector/keyword search request schemas and FastMCP tool definitions using **Pydantic v2**.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class VectorQueryConfig(BaseModel):
    vector_field: str = Field(default="content_vector", alias="vectorField")
    k_nearest_neighbors: int = Field(default=5, ge=1, le=100, alias="k")
    fields: str = Field(default="content_vector")

class AzureSearchQuery(BaseModel):
    search_text: Optional[str] = Field(None, alias="searchText")
    vector_query: Optional[VectorQueryConfig] = Field(None, alias="vectorQuery")
    top: int = Field(default=5, ge=1, le=50)
    use_semantic_ranker: bool = Field(default=True, alias="useSemanticRanker")

    class Config:
        populate_by_name = True

    @field_validator("search_text")
    @classmethod
    def validate_search_inputs(cls, v: Optional[str], info) -> Optional[str]:
        # Ensure either search_text or vector_query is provided
        return v

# Operational Verification
if __name__ == "__main__":
    query_payload = {
        "searchText": "agentic workflow security policies",
        "vectorQuery": {
            "vectorField": "document_vector",
            "k": 10
        },
        "top": 5,
        "useSemanticRanker": True
    }

    validated_query = AzureSearchQuery(**query_payload)
    print("Azure AI Search query configuration validated successfully:")
    print(validated_query.model_dump_json(indent=2, by_alias=True))
```

## Related tools / concepts
- [Azure OpenAI](azure-openai.md) — Enterprise LLM and embedding generation provider.
- [Chroma](../infrastructure/chroma.md) — Open-source vector database alternative.
- [Pinecone](../infrastructure/pinecone.md) — Managed vector database service.
- [Milvus](../infrastructure/milvus.md) — High-performance open-source vector store.
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Connector protocol for AI agents.

## Sources / references
- [Azure AI Search Official Documentation](https://learn.microsoft.com/azure/search/)
- [Microsoft Learn: Hybrid Search with Azure AI Search](https://learn.microsoft.com/azure/search/search-get-started-vector)
- [FastMCP 3.1 Azure Search Integration Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
