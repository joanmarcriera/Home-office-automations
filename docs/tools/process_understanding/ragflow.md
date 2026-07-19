# RAGFlow

## What it is
RAGFlow is a vision-native, open-source Retrieval-Augmented Generation (RAG) engine that prioritizes deep document understanding (DeepDoc) for complex, unstructured data. As of July 2026 (v0.34.x), it has evolved into an enterprise-grade 'Knowledge Engine' for agentic workflows, featuring multi-modal reasoning, native integration with frontier models like Claude 5.1, GPT-5.5, and Gemma 3, and a modular architecture for production-ready RAG pipelines.

## What problem it solves
It eliminates the "garbage in, garbage out" failure mode of standard RAG systems by using layout-aware parsing (DeepDoc) instead of naive text chunking. It accurately extracts structured information from multi-column PDFs, nested tables, and embedded charts, ensuring that agentic retrieval is grounded in high-fidelity evidence with precise, pixel-level citations and visual grounding.

## Where it fits in the stack
**Knowledge / Inference Layer**. RAGFlow serves as the specialized 'Cognitive Memory' in the agentic stack. It sits between raw data storage (S3, MinIO) and the orchestration layer (n8n, AG2, Flowise), providing a high-confidence context window for frontier models.

## Typical use cases
- **Complex Document Analysis**: Parsing financial statements (10-Ks, 10-Qs) and technical manuals where table structure and image context are critical.
- **Agentic RAG Pipelines**: Providing a high-fidelity knowledge source for agents built on Claude 5.1, GPT-5.5, or Gemma 3.
- **Multi-modal Knowledge Extraction**: Reasoning over diagrams, flowcharts, and handwritten notes in scanned documents.
- **Enterprise-Grade Grounding**: Building self-hosted search systems with strict citation requirements and data sovereignty constraints.

## Strengths
- **Vision-Based Parsing (DeepDoc)**: Superior handling of complex layouts and tables compared to OCR-only or text-only extractors.
- **Template-Driven Chunking**: Intelligent segmentation based on document intent (e.g., Q&A, Paper, Manual, Book, Resume).
- **Multi-modal Native**: Integrated support for VLM-based reasoning (e.g., InternVL2, Qwen3-VL, Llama 4 Vision, Gemma 3 Vision) directly within the RAG pipeline.
- **Agentic Hooks**: Features native MCP 3.0/3.1 support for seamless integration with agentic tool-use protocols.

## Limitations
- **Resource Intensive**: Requires significant GPU/CPU resources (32GB+ RAM recommended for production DeepDoc parsing).
- **Initial Indexing Latency**: Vision-based parsing is slower than traditional plain-text extraction methods.
- **Configuration Depth**: The high degree of parsing control requires a learning curve to optimize for specific document types.

## When to use it
- When documents contain complex tables, multi-column layouts, or critical visual information.
- When you need a self-hosted, vision-native RAG solution that integrates with MCP 3.0/3.1.
- When high-confidence citations and grounding are the primary system requirements.

## When not to use it
- For simple, structured text data (JSON, CSV) where a basic vector database or Postgres (pgvector) is sufficient.
- In low-latency scenarios where indexing speed is prioritized over parsing fidelity.
- On hardware with less than 16GB of RAM or no access to specialized inference engines.

## Getting started

### Installation (Docker Compose)
RAGFlow recommends a multi-container deployment for its cognitive services (Elasticsearch/Infinity, Redis, MySQL, MinIO).

```bash
# Clone the repository
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker

# Increase system map count (required for Elasticsearch)
sudo sysctl -w vm.max_map_count=262144

# Start the cluster using the July 2026 stable branch config
docker compose up -d
```

### Basic Workflow
1. Access the UI at `http://localhost:80`.
2. Configure your model providers (Claude 5.1 / GPT-5.5 / Gemma 3 / local Ollama).
3. Create a 'Knowledge Base' and select the 'DeepDoc' parser template.
4. Upload documents and monitor the parsing queue in the 'Files' tab.

## CLI examples

### Health and Log Monitoring
```bash
# Check status of RAGFlow cognitive services
docker compose ps

# Follow parsing server logs
docker logs -f ragflow-server

# Verify Infinity/Elasticsearch connectivity
docker exec -it ragflow-server curl -X GET "http://ragflow-es:9200/_cluster/health?pretty"
```

### Image Management
```bash
# Pull the latest July 2026 production image
docker pull infiniflow/ragflow:v0.34.0-cuda
```

## API examples

### Python SDK: Agentic Document Intake
```python
from ragflow_sdk import RAGFlow

# Initialize with July 2026 API standards
ragflow = RAGFlow(api_key="rf-your-key", base_url="http://localhost:9337")

# Create an agent-aware dataset
dataset = ragflow.create_dataset(name="Legal Intelligence", parsing_template="Law")

# Upload and parse
document = dataset.upload_document(filepath="./contract_v4.pdf")
dataset.parse_document(document_ids=[document.id])

# Query with VLM grounding
results = dataset.retrieve(
    question="What are the indemnification limits in section 4.2?",
    top_k=5,
    visual_grounding=True
)
```

### MCP 3.0/3.1 Integration (Agentic Context)
RAGFlow exposes knowledge bases via MCP 3.0/3.1, allowing agents to query the document store directly with standard HTTP/SSE transport layers:
```json
{
  "mcpServers": {
    "ragflow": {
      "command": "npx",
      "args": ["@ragflow/mcp-server", "--base-url", "http://ragflow:9337", "--api-key", "rf-key"]
    }
  }
}
```

## Related tools / concepts
- [Dify](../ai_knowledge/dify.md)
- [Docling](./docling.md)
- [Docling MCP](./docling-mcp.md)
- [OCRmyPDF](./ocrmypdf.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Firecrawl](./firecrawl.md)
- [Crawl4AI](./crawl4ai.md)
- [AG2](../frameworks/ag2.md)
- [Flowise](../ai_knowledge/flowise.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)
- [Ragas](./ragas.md)

## Sources / references
- [RAGFlow Official Site](https://ragflow.io/)
- [GitHub: infiniflow/ragflow](https://github.com/infiniflow/ragflow)
- [DeepDoc Architecture Deep Dive](https://ragflow.io/docs/dev/deepdoc)
- [July 2026 Release Notes (v0.34)](https://github.com/infiniflow/ragflow/releases/tag/v0.34.0)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
