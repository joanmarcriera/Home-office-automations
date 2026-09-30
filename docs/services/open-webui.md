# Open WebUI

Open WebUI is an extensible, self-hosted AI interface and multi-backend orchestration platform designed for seamless interactions with local models and cloud LLMs. As of **January 2027**, Open WebUI features full native support for **MCP 3.1** (**FastMCP 3.1**), dynamic WebUI Pipelines, agentic session state management, multi-vector database RAG integration (ChromaDB, Qdrant, PGVector), granular Role-Based Access Control (RBAC), and multi-provider load balancing across Ollama, vLLM, LiteLLM, OpenAI, and Anthropic backends.

```mermaid
architecture-beta
    group user_layer(cloud, "User & Client Access")
    service browser(internet, "Web Browser / PWA", "client") in user_layer
    service mobile(internet, "Mobile App / Tablet", "client") in user_layer

    group webui_app(server, "Open WebUI Core Stack")
    service frontend(disk, "React / Svelte UI", "app") in webui_app
    service backend(server, "FastAPI Backend Engine", "app") in webui_app
    service pipeline(cpu, "WebUI Pipelines (Python)", "app") in webui_app
    service mcp_client(server, "MCP 3.1 Orchestrator", "app") in webui_app

    group storage_layer(database, "Persistence & RAG")
    service postgres(database, "PostgreSQL (State/RBAC)", "db") in storage_layer
    service vector_db(database, "Chroma / Qdrant / PGVector", "db") in storage_layer

    group backend_providers(cloud, "Inference Providers")
    service ollama(cpu, "Ollama (Local Models)", "server") in backend_providers
    service vllm(cpu, "vLLM / TensorRT-LLM", "server") in backend_providers
    service cloud_llm(cloud, "Claude / GPT-5.5 / Gemini", "cloud") in backend_providers

    browser -->> frontend: HTTPS Websocket / SSE
    frontend -->> backend: REST API / Streaming
    backend -->> postgres: Session & User Auth (OAuth2/SSO)
    backend -->> vector_db: Embeddings & Context Retrieval
    backend -->> pipeline: Custom Filters & Valves
    backend -->> mcp_client: FastMCP 3.1 Tool Execution
    mcp_client -->> backend_providers: Multi-Provider Chat Routing
```

## What it is
Open WebUI is an open-source (MIT License), self-hosted AI operating interface that provides a feature-complete ChatGPT-style application for multi-modal model orchestration. It bridges user-facing client applications with inference runtimes like Ollama, vLLM, LiteLLM, and proprietary APIs.

Beyond simple chat rendering, Open WebUI provides enterprise-grade infrastructure components:
- **WebUI Pipelines**: A flexible modular framework allowing custom Python pre/post-processing filters, guardrails, and model valves.
- **Native MCP 3.1 Host**: Dynamic discovery and execution of Model Context Protocol tools over stdio and Server-Sent Events (SSE).
- **Hybrid RAG Engine**: Multi-stage document chunking, embedding generation, re-ranking, and context injection into model prompts.
- **Multi-Tenant Administration**: Comprehensive OAuth2/OIDC single sign-on (SSO), workspace quota management, group permissions, and audit logging.

```mermaid
flowchart TD
    A[User Query / Document Upload] --> B{Action Type?}

    B -->|Document Upload| C[Document Processing Pipeline]
    C --> C1[Text Extraction: PyPDF/Docling]
    C1 --> C2[Chunking: Recursive / Semantic]
    C2 --> C3[Embedding Generation: BGE / Nomic]
    C3 --> C4[Vector Indexing: Chroma / Qdrant]
    C4 --> D[RAG Knowledge Store]

    B -->|Interactive Chat| E[WebUI FastAPI Core]
    E --> F[Auth & RBAC Verification]
    F --> G[WebUI Pipelines Filter Engine]
    G --> H{RAG Enabled?}

    H -->|Yes| I[Query Vector DB]
    I --> J[Re-rank Results: Cross-Encoder]
    J --> K[Inject Retrieved Chunks into System Prompt]
    H -->|No| K

    K --> L{MCP Tools Required?}
    L -->|Yes| M[FastMCP 3.1 Tool Execution]
    M --> N[Append Tool Outputs to Context]
    L -->|No| N

    N --> O[Route Query to Inference Engine]
    O --> O1[Ollama / Local LLM]
    O --> O2[vLLM High-Throughput Cluster]
    O --> O3[Cloud API: Claude / GPT-5.5]

    O1 & O2 & O3 --> P[Stream Response via SSE to Client]
```

## What problem it solves
Managing local LLM deployments and cloud model subscriptions across teams introduces fragmented interfaces, security risks, and technical friction:
1. **Fragmented UI & CLI Barriers**: Non-technical team members lack friendly web interfaces to interact with local Ollama or vLLM models.
2. **Data Privacy & Compliance**: Uploading sensitive documents to public SaaS platforms risks data leakage; Open WebUI guarantees that document processing and vector embeddings remain 100% self-hosted.
3. **Inconsistent Agent & Tool Standards**: Custom scripts lack uniform protocol standards; Open WebUI standardizes tool calls using MCP 3.1.
4. **Lack of Multi-Model Governance**: Organizations need centralized access control, user usage tracking, and model routing rules across local and cloud backends.

## Where it fits in the stack
Open WebUI functions as the **AI Application & Orchestration Layer**. It interfaces between frontend clients and underlying inference engines, vector databases, and external APIs:

```
+-----------------------------------------------------------------------+
|                      Client Layer (PWA / Browser)                      |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                     Open WebUI Frontend & WebSockets                  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                   Open WebUI FastAPI Orchestrator                     |
|  - Auth & RBAC (OAuth2 / OIDC)    - WebUI Pipelines (Filters/Valves)  |
|  - Hybrid RAG Engine (Chroma/Qdrant) - FastMCP 3.1 Tool Host           |
+-----------------------------------------------------------------------+
         |                         |                         |
         v                         v                         v
+------------------+     +------------------+     +--------------------+
|  Ollama / vLLM   |     | Vector DB Store  |     | Cloud API Gateways |
|  (Local Models)  |     | (Qdrant / PGVec) |     | (LiteLLM / Claude) |
+------------------+     +------------------+     +--------------------+
```

## Typical use cases
- **Self-Hosted Enterprise AI Hub**: Providing employees with a secure, brandable, private chat interface with SSO auth.
- **Local Document Knowledge Graph**: Uploading technical PDF manuals, codebase archives, and internal wikis for accurate RAG Q&A.
- **Agentic Multi-Tool Workflows**: Connecting FastMCP 3.1 tools to query SQL databases, search web engines, or trigger local code tools.
- **Multi-Model Side-by-Side Arena**: Executing identical prompts across multiple models simultaneously to compare output quality.
- **Custom Guardrail Enforcement**: Deploying WebUI Pipelines to automatically censor PII, enforce prompt formatting, or enforce safety checks.

## Strengths
- **Native FastMCP 3.1 Tooling**: Comprehensive support for Model Context Protocol tools and resources.
- **Multi-Vector DB Support**: Native integration with ChromaDB, Qdrant, Milvus, and PostgreSQL PGVector.
- **WebUI Pipelines Middleware**: Hot-swappable Python scripts for prompt interception, filtering, and API augmentation.
- **Fine-Grained RBAC & SSO**: Built-in support for Keycloak, Authentik, Okta, and OpenID Connect.
- **Channels & Live Voice Chat**: Supports real-time ambient web socket streaming and voice-to-voice communication modes.

## Limitations
- **Operational Overhead**: Advanced setups with external vector stores, Redis caching, and WebUI Pipelines require dedicated Docker/Kubernetes management.
- **Memory Footprint**: Running the WebUI stack alongside local embedding models and high-throughput vector DBs increases host RAM requirements.

## When to use it
- When building a privacy-first, self-hosted chat environment for local models and cloud LLMs.
- When teams require document interaction (RAG) backed by dedicated vector infrastructure.
- When standardizing agentic workflows across local and remote MCP 3.1 servers.

## When not to use it
- If you only require a lightweight command-line interface (CLI) for quick local model testing.
- On embedded or edge devices with under 4 GB RAM.

## Getting started

### Docker Compose Stack with PostgreSQL, Qdrant, and Ollama
Below is a production-grade `docker-compose.yml` file deploying Open WebUI configured with PostgreSQL for persistent user state, Qdrant for vector storage, and Ollama for model inference.

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: openwebui-postgres
    environment:
      POSTGRES_DB: openwebui
      POSTGRES_USER: webui_admin
      POSTGRES_PASSWORD: SecurePassword2027!
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U webui_admin -d openwebui"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:v1.12.0
    container_name: openwebui-qdrant
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    container_name: openwebui-ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ollama_models:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    depends_on:
      postgres:
        condition: service_healthy
      qdrant:
        condition: service_started
      ollama:
        condition: service_started
    environment:
      - DATABASE_URL=postgresql://webui_admin:SecurePassword2027!@postgres:5432/openwebui
      - OLLAMA_BASE_URL=http://ollama:11434
      - VECTOR_DB=qdrant
      - QDRANT_URI=http://qdrant:6333
      - ENABLE_OAUTH_SIGNUP=true
      - ENABLE_RAG_HYBRID_SEARCH=true
      - RAG_TOP_K=5
      - RAG_RERANKING_MODEL=BAAI/bge-reranker-v2-m3
      - WEBUI_SECRET_KEY=SuperSecretWebUIKey2027
    volumes:
      - webui_data:/app/backend/data
    restart: unless-stopped

volumes:
  postgres_data:
  qdrant_data:
  ollama_models:
  webui_data:
```

## CLI examples

### User & Database Management CLI
Open WebUI provides backend Python CLI scripts executable within the running container for administrative maintenance:

```bash
# 1. Promote a user account to Super Admin
docker exec -it open-webui python /app/backend/apps/webui/internal/db.py --promote-admin --email admin@company.internal

# 2. Re-index vector store collection for updated RAG configuration
docker exec -it open-webui python /app/backend/run_db_script.py --reindex-rag

# 3. Prune orphaned chat history and temporary attachments
docker exec -it open-webui python /app/backend/run_db_script.py --clean-orphaned-data

# 4. Dump Open WebUI configuration and user permission flags to JSON
docker exec -it open-webui python -c "
import json
from apps.webui.config import AppConfig
print(json.dumps(AppConfig().dict(), indent=2))
"
```

## API examples

### Open WebUI FastMCP 3.1 Pipeline & RAG Orchestration Server
Below is a full Python server implementation leveraging **FastMCP 3.1** and **Pydantic v2** to programmatically manage Open WebUI models, trigger RAG document ingestion, and route user prompts through WebUI Pipelines.

```python
"""
FastMCP 3.1 Server for Managing Open WebUI Pipelines, RAG Ingestion, and RBAC Roles.
"""

import os
import json
import requests
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    title="Open WebUI Orchestration Server",
    version="3.1.0",
    description="FastMCP server for programmatic interaction with Open WebUI backend APIs."
)


# --- Pydantic v2 Validation Schemas ---

class OpenWebUIConnection(BaseModel):
    """Pydantic v2 model for Open WebUI API connection details."""
    model_config = ConfigDict(extra="forbid")

    base_url: str = Field(default="http://localhost:3000/api/v1", description="Open WebUI base API endpoint")
    api_key: str = Field(description="JWT or Admin API token")

    @field_validator("base_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("base_url must start with http:// or https://")
        return v.rstrip("/")


class DocumentIngestionRequest(BaseModel):
    """Pydantic v2 schema for uploading document content to Open WebUI RAG."""
    model_config = ConfigDict(extra="forbid")

    collection_name: str = Field(description="Target vector collection identifier")
    document_title: str = Field(description="Display title of the document")
    content: str = Field(min_length=10, description="Raw markdown or text content to embed")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")


class PipelineFilterConfig(BaseModel):
    """Pydantic v2 schema for configuring WebUI Pipeline filters."""
    model_config = ConfigDict(extra="forbid")

    pipeline_id: str = Field(description="Unique pipeline ID registered in Open WebUI")
    enable_guardrails: bool = Field(default=True, description="Enable PII/Safety guardrail filter")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(default=2048, ge=64, le=32768, description="Maximum token generation limit")


# --- FastMCP 3.1 Tools ---

@mcp.tool()
def query_openwebui_models(conn_json: str) -> str:
    """
    Retrieves all available local and cloud models registered in Open WebUI.
    """
    try:
        conn_data = json.loads(conn_json)
        conn = OpenWebUIConnection(**conn_data)
    except Exception as e:
        return f"Error: Invalid connection parameters - {str(e)}"

    headers = {"Authorization": f"Bearer {conn.api_key}"}
    url = f"{conn.base_url}/models"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        models = resp.json().get("data", [])
        return json.dumps({"status": "success", "count": len(models), "models": models}, indent=2)
    except Exception as e:
        return f"API Error: Failed to fetch models from Open WebUI - {str(e)}"


@mcp.tool()
def ingest_rag_document(conn_json: str, doc_json: str) -> str:
    """
    Ingests text content into Open WebUI vector store for RAG document retrieval.
    """
    try:
        conn = OpenWebUIConnection(**json.loads(conn_json))
        doc = DocumentIngestionRequest(**json.loads(doc_json))
    except Exception as e:
        return f"Error: Validation failure - {str(e)}"

    headers = {
        "Authorization": f"Bearer {conn.api_key}",
        "Content-Type": "application/json"
    }
    url = f"{conn.base_url}/documents/"

    payload = {
        "name": doc.document_title,
        "collection_name": doc.collection_name,
        "content": doc.content,
        "metadata": {"tags": doc.tags, "source": "FastMCP-3.1"}
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return json.dumps({"status": "success", "document": resp.json()}, indent=2)
    except Exception as e:
        return f"API Error: Failed to ingest document - {str(e)}"


@mcp.tool()
def trigger_pipeline_chat(conn_json: str, pipeline_config_json: str, prompt: str) -> str:
    """
    Sends a chat completion request through a configured Open WebUI Pipeline filter.
    """
    try:
        conn = OpenWebUIConnection(**json.loads(conn_json))
        pconfig = PipelineFilterConfig(**json.loads(pipeline_config_json))
    except Exception as e:
        return f"Error: Validation failure - {str(e)}"

    headers = {
        "Authorization": f"Bearer {conn.api_key}",
        "Content-Type": "application/json"
    }
    url = f"{conn.base_url}/chat/completions"

    payload = {
        "model": pconfig.pipeline_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": pconfig.temperature,
        "max_tokens": pconfig.max_tokens,
        "valves": {"enable_guardrails": pconfig.enable_guardrails}
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)
    except Exception as e:
        return f"API Error: Failed pipeline chat execution - {str(e)}"


if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Ollama](ollama.md) — Local model inference daemon providing model runtimes for Open WebUI.
- [vLLM](../tools/infrastructure/vllm.md) — High-throughput LLM serving engine for cluster deployments.
- [LiteLLM](litellm.md) — Multi-provider unified API proxy for routing prompts to cloud LLMs.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Open standard for connecting AI models to external tools and context.
- [Qdrant](../tools/infrastructure/qdrant.md) — High-performance vector search engine used for scalable RAG storage.
- [Authentik](authentik.md) — Self-hosted identity provider for OIDC SSO integration with Open WebUI.
- [n8n](n8n.md) — Workflow automation engine triggerable via Open WebUI webhooks.

## Sources / references
- [Open WebUI Official Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub Repository](https://github.com/open-webui/open-webui)
- [WebUI Pipelines Framework GitHub](https://github.com/open-webui/pipelines)
- [MCP 3.1 Specification](https://modelcontextprotocol.io)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
