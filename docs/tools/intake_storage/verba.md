# Verba

## What it is
Verba is an open-source Retrieval-Augmented Generation (RAG) application built on top of Weaviate. As of early January 2027, it provides a "Golden RAG" experience, focusing on simplicity, modularity, and high-quality hybrid retrieval out of the box.

## What problem it solves
It provides an intuitive interface and modular engine for building RAG applications, handling document ingestion, chunking, embedding, and querying with LLMs. It eliminates the complexity of setting up a complete RAG pipeline by providing a unified stack for experimentation and production use.

## Where it fits in the stack
**Category**: Tool / Knowledge Management / RAG. It serves as the application layer on top of a vector database (Weaviate) to enable conversational search over private enterprise and homelab documents.

## Typical use cases
- Creating a personal knowledge base with AI search.
- Question-answering over private document collections (PDF, Markdown, Text).
- Testing different chunking and retrieval strategies.
- Evaluating model performance (e.g., comparing **Claude 5.1** vs **GPT-5.5**) on specific knowledge sets.

## Strengths
- **Easy Setup**: Reliable Docker-based deployment and python package installation.
- **Multimodal Support**: Built-in support for multiple document and data types (PDF, txt, markdown, docx).
- **Native Weaviate Integration**: Leverages Weaviate's advanced vector search, including hybrid keyword-vector search and reranking.
- **Model Flexibility**: Supports frontier models like **Llama 4**, **Claude 5.1**, and **GPT-5.5**.

## Limitations
- **Ecosystem Focus**: Primary integrations and optimized features are closely tied to the Weaviate ecosystem.
- **Configuration Overhead**: May require custom chunking tuning for optimal performance with specialized or dense technical datasets.
- **UI Constraints**: The built-in frontend is optimized for specific RAG workflows and may require customization for complex enterprise portals.

## When to use it
- When you want a production-ready RAG interface without building a custom frontend and retrieval pipeline from scratch.
- For prototyping RAG workflows with Weaviate as the vector database backend.
- When you need a local-first RAG solution that can seamlessly scale to cloud deployments.

## When not to use it
- If you need a highly custom retrieval pipeline that departs significantly from Verba's modular architecture.
- If you are already committed to a different vector database (e.g., Pinecone, Qdrant, Milvus) and do not wish to use Weaviate.

## Getting started

To get started with Verba, install it using `pip` and run a quick verification script.

### Installation
```bash
# Install Verba from PyPI
pip install goldenverba pydantic
```

### Hello-World Example
Below is a simple Python snippet to initialize the Verba environment and verify that the module is correctly installed:
```python
from goldenverba.components.interfaces import Generator

# Verify the interface can be imported and initialized
class HelloWorldGenerator(Generator):
    def __init__(self):
        super().__init__()
        self.name = "HelloWorld"
        self.description = "A simple verification generator for Verba"

    def generate(self, queries, context):
        return "Hello World from Verba RAG!"

generator = HelloWorldGenerator()
print(f"Verba {generator.name} initialized: {generator.generate([], '')}")
```

### Docker Deployment Option
Alternatively, you can run Verba's full stack (including Weaviate) using Docker Compose:
```bash
git clone https://github.com/weaviate/Verba
cd Verba
docker compose up -d
```

## CLI examples

Verba provides a dedicated command line tool (`verba`) to spin up servers, ingest datasets, and inspect overall health.

```bash
# 1. Start the Verba server on port 8000
verba start --port 8000

# 2. Import documents from a local folder into the knowledge base
verba import --path ./my_documents/

# 3. View the state of connected databases and API keys
verba status
```

## API examples

### Python (Querying Verba API with Pydantic v2 Validation)
Verba exposes a backend REST API. The example below validates request schemas using **Pydantic v2** and sends a query to the running server.

```python
import requests
from pydantic import BaseModel, Field
from typing import Optional

# Define validation schema following strict Pydantic v2 guidelines
class VerbaQueryPayload(BaseModel):
    query: str = Field(..., min_length=1, description="The search or question string")
    conversation_id: Optional[str] = Field(default=None, description="Conversation tracker UUID")
    model: str = Field(default="claude-5-1-sonnet-20261022", description="Target model")

# Payload to validate
raw_query_data = {
    "query": "How do I configure the OIDC middleware for Traefik?",
    "model": "claude-5-1-sonnet-20261022"
}

try:
    # Strict validation under Pydantic v2
    validated_query = VerbaQueryPayload.model_validate(raw_query_data)
    print(f"Validated query: '{validated_query.query}'")

    # Send the request to local Verba API
    response = requests.post(
        "http://localhost:8000/api/query",
        json=validated_query.model_dump(exclude_none=True),
        timeout=10
    )
    if response.status_code == 200:
        print("Response received:", response.json().get("answer"))
except Exception as e:
    print(f"RAG query pipeline execution failed: {e}")
```

## Related tools / concepts
- [Weaviate](../infrastructure/weaviate.md) — The vector database powering Verba.
- [Khoj](khoj.md) — Personal AI search assistant for notes and local files.
- [AnyType](anytype.md) — Local-first P2P knowledge base tool.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architecture for retrieval augmentation.
- [Obsidian](../ai_knowledge/obsidian.md) — Markdown note source for Verba.
- [LangChain](../ai_knowledge/langchain.md) — Framework often used to extend Verba workflows.
- [Ollama](../../services/ollama.md) — Supported local inference backend for private RAG.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standard protocol for connecting tools to agents.

## Sources / references
- [Official Verba Website](https://verba.weaviate.io/)
- [Verba GitHub Repository](https://github.com/weaviate/Verba)
- [Weaviate Documentation](https://weaviate.io/developers/verba)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
