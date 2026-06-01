# RAGFlow

## What it is
RAGFlow is an open-source Retrieval-Augmented Generation (RAG) engine that integrates deep document understanding with agentic capabilities. It is designed to handle complex, unstructured data and provide a high-fidelity context layer for LLMs. It features a vision-based "DeepDoc" parser that understands document structure (tables, headers, footnotes) as a human would.

## What problem it solves
It solves the "garbage in, garbage out" problem in RAG systems by using advanced document parsing (DeepDoc) to extract structured knowledge from complicated PDF formats, tables, and images. It minimizes hallucinations by ensuring retrieval is grounded in well-parsed evidence and provides explicit citations back to the source document segments.

## Where it fits in the stack
**Tool / Infra**: It serves as a specialized RAG infrastructure and toolset for document processing and retrieval. It acts as the "Cognitive Engine" for agents that need to reason over large, complex document corpora.

## Typical use cases
- **Complex PDF Parsing**: Extracting accurate information from financial reports, legal documents, and technical manuals that contain complex layouts.
- **Agentic Knowledge Retrieval**: Serving as the knowledge backend for agents that need to perform multi-step reasoning over large document collections.
- **Enterprise Search**: Building a private, self-hosted search engine across heterogeneous data sources like Notion, Google Drive, and S3.
- **Automated Data Intake**: Parsing incoming invoices or technical specs via n8n for structured storage.

## Strengths
- **DeepDoc Parsing**: Superior extraction of knowledge from unstructured data compared to simple text chunking; handles OCR and layout analysis natively.
- **Template-based Chunking**: Provides intelligent and explainable options for segmenting data based on document type (e.g., Book, Laws, Presentation).
- **Multi-modal Capabilities**: Can reason over images and charts within documents using vision models.
- **Agent Integration**: Fuses RAG with agentic workflows for more dynamic task execution and self-correction.

## Limitations
- **Hardware Requirements**: High resource consumption (minimum 4 cores, 16GB RAM recommended for production).
- **Setup Complexity**: Requires multiple services (Elasticsearch/Infinity, Redis, MySQL, MinIO) making it more complex to deploy than lightweight RAG wrappers.
- **Latency**: Deep document parsing (especially with OCR) is computationally intensive and slower than simple text extraction.

## When to use it
- When document layouts are too complex for standard RAG systems (e.g., multi-column PDFs with embedded tables).
- When production-grade grounding and citation accuracy are critical.
- When building agents that require a deep, well-structured knowledge base.

## When not to use it
- For simple, text-only RAG tasks where lightweight solutions like a basic vector DB would suffice.
- In resource-constrained environments (e.g., low-power edge devices).
- When near-instantaneous indexing of new documents is required (due to parsing overhead).

## Getting started

### Installation
```bash
# Clone the repository
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker

# Increase vm.max_map_count for Elasticsearch (required)
sudo sysctl -w vm.max_map_count=262144

# Start the server using Docker Compose
docker compose up -d
```

### Basic usage
Access the RAGFlow UI at `http://localhost` (default port 80). Log in and configure your LLM API keys in the "Model Providers" settings. Create a new "Knowledge Base," choose a parsing template (e.g., "General"), and upload your first PDF.

## CLI examples
```bash
# Pull the latest RAGFlow image
docker pull infiniflow/ragflow:v0.25.1

# Check backend logs for parsing status
docker logs -f ragflow-server

# Enter the backend container to check connectivity to Elasticsearch
docker exec -it ragflow-server curl -X GET "http://ragflow-es:9200/_cluster/health?pretty"
```

## API examples

### Python SDK (Document Management)
```python
# RAGFlow provides a Python SDK for programmatic access
from ragflow_sdk import RAGFlow

# Initialize the client
ragflow = RAGFlow(api_key="YOUR_API_KEY", base_url="http://localhost:9337")

# Create a dataset (Knowledge Base)
dataset = ragflow.create_dataset(name="Project Documentation")

# Upload and start parsing a document
document = dataset.upload_document(filepath="manual.pdf")
dataset.parse_document(document_ids=[document.id])

# Query the dataset
results = dataset.retrieve(question="How do I reset the device?", top_k=3)
for res in results:
    print(f"Content: {res['content_with_weight']}\nSource: {res['doc_name']}\n")
```

### n8n Integration Pattern
RAGFlow can be integrated into n8n using the **HTTP Request** node to trigger document ingestion:
- **Method**: `POST`
- **URL**: `http://<ragflow-ip>/api/v1/document/upload`
- **Headers**: `Authorization: Bearer <API_KEY>`
- **Body (Form-Data)**:
    - `file`: (Binary data from previous node)
    - `kb_id`: `<YOUR_KB_ID>`

## Related tools / concepts
- [Dify](../ai_knowledge/dify.md)
- [PageIndex](./pageindex.md)
- [OCRmyPDF](./ocrmypdf.md)
- [Docling](./docling.md)
- [Firecrawl](./firecrawl.md)
- [Unstructured](../ai_knowledge/unstructured.md)
- [LlamaParse](../ai_knowledge/llamaparse.md)

## Sources / references
- [Official Website](https://ragflow.io/)
- [GitHub Repository](https://github.com/infiniflow/ragflow)
- [RAGFlow Documentation](https://ragflow.io/docs/dev/)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
