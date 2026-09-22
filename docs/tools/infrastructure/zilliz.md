# Zilliz

## What it is
Zilliz (Zilliz Cloud) is a fully managed, cloud-native vector database platform built on top of open-source **Milvus**. It is engineered specifically for massive-scale vector similarity search, unstructured data retrieval, and retrieval-augmented generation (RAG) applications.

## What problem it solves
Self-hosting large-scale Milvus clusters requires significant operational overhead, including managing distributed Kubernetes deployments, tuning vector index parameters (HNSW, IVF_FLAT, DiskANN), and scaling cloud storage/compute independently. Zilliz Cloud solves this by offering a fully managed serverless and dedicated vector database with automated indexing, enterprise security, auto-scaling, and multi-cloud availability.

## Where it fits in the stack
**Infrastructure / Vector Database**. It functions as the enterprise managed vector memory layer for LLM applications, RAG pipelines, and agentic memory systems.

## Typical use cases
- **Enterprise RAG Systems**: Storing and searching millions to billions of document embeddings with sub-10ms query latencies.
- **Agentic Long-Term Memory**: Storing conversational histories, semantic knowledge bases, and multi-modal vector representations for persistent AI agents.
- **Hybrid Search**: Combining dense vector similarity search with sparse keyword search and metadata filtering in a single query execution.

## Strengths
- **Milvus Compatibility**: 100% compatible with the open-source PyMilvus SDK and ecosystem toolchains.
- **Auto-Indexing & Tuning**: Automatically chooses and optimizes vector indexes (including Cardinal indexing engine) without manual parameter tuning.
- **Serverless & Multi-Cloud**: Offers pay-as-you-go serverless clusters across AWS, GCP, and Azure.
- **Enterprise Security**: SOC 2 Type II compliant, with support for RBAC, private link connections (VPC peering), and encryption at rest/in transit.

## Limitations
- **Cloud Proprietary Service**: While API-compatible with Milvus, the hosted platform service features usage-based cloud pricing.
- **Latency Over Network**: Remote cloud endpoint query latency includes network round-trip time compared to embedded databases like LanceDB or DuckDB.

## When to use it
- When you need enterprise-grade Milvus capabilities without the operational overhead of managing Kubernetes clusters.
- For production RAG systems scaling beyond tens of millions of high-dimensional vector embeddings.
- When multi-cloud flexibility (AWS, Azure, GCP) and enterprise security compliance are required.

## When not to use it
- For lightweight, local-first applications where embedded vector engines (e.g., LanceDB, Chroma, Qdrant local) are sufficient.
- When complete air-gapped or on-premises deployment is mandatory (use self-hosted open-source Milvus).

## Getting started

### Installation
Install the official PyMilvus SDK (compatible with Zilliz Cloud):

```bash
pip install pymilvus
```

### Connection Example
Connect to Zilliz Cloud using your instance URI and API token:

```python
from pymilvus import MilvusClient

client = MilvusClient(
    uri="https://in01-123456789.api.gcp-us-west1.zillizcloud.com",
    token="YOUR_ZILLIZ_API_KEY"
)

# Create a collection with auto-indexing
client.create_collection(
    collection_name="rag_knowledge_base",
    dimension=1536  # OpenAI text-embedding-3-large dimension
)
```

## CLI examples
```bash
# Installing Zilliz / Milvus CLI tool
pip install milvus-cli

# Connecting to Zilliz Cloud instance
milvus-cli connect -h https://in01-123456789.api.gcp-us-west1.zillizcloud.com -t YOUR_ZILLIZ_API_KEY

# Listing collections
milvus-cli list collections
```

## API examples
```python
# Insert vector embeddings with metadata
data = [
    {"id": 1, "vector": [0.1] * 1536, "title": "Doc A", "category": "architecture"},
    {"id": 2, "vector": [0.2] * 1536, "title": "Doc B", "category": "playbook"},
]
res = client.insert(collection_name="rag_knowledge_base", data=data)

# Perform vector similarity search with scalar filtering
search_res = client.search(
    collection_name="rag_knowledge_base",
    data=[[0.1] * 1536],
    limit=5,
    filter='category == "architecture"'
)
print(search_res)
```

## Related tools / concepts
- **[Milvus](milvus.md)**: Open-source distributed vector database engine underpinning Zilliz Cloud.
- **[Qdrant](qdrant.md)**: High-performance Rust-based vector database.
- **[Pinecone](pinecone.md)**: Managed serverless cloud vector database platform.

## Sources / references
- [Zilliz Official Site](https://zilliz.com/?ref=2026-09-21-audit)
- [Zilliz Cloud Documentation](https://docs.zilliz.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
