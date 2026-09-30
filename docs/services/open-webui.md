# Open WebUI

## What it is
Open WebUI is a user-friendly, feature-rich, self-hosted web interface designed for Large Language Models (LLMs) and multi-agent orchestration. As of early 2027, it serves as an enterprise-grade AI desktop and gateway, providing seamless compatibility with local inference servers (such as [Ollama](ollama.md), [KoboldCPP](../tools/infrastructure/koboldcpp.md), and [vLLM](../tools/infrastructure/vllm.md)) alongside frontier cloud providers (such as OpenAI GPT-5.5/5.6, Anthropic Claude 5.1/5.6, Google Gemini 4.0, and DeepSeek-V4).

Open WebUI is open source (MIT License) and completely free to self-host. Beyond basic chat interactions, it acts as an **Agentic Operating Workspace**, supporting native Model Context Protocol (**MCP 3.1** / **FastMCP 3.1**), local document Retrieval-Augmented Generation (RAG), multi-user Role-Based Access Control (RBAC), code execution sandboxes, real-time audio synthesis/transcription, and customizable Function/Pipe extensions.

## What problem it solves
Managing local models and API keys across multiple command-line tools or fragmented user interfaces creates operational friction for organizations and non-technical end-users. Open WebUI solves this by providing a unified, polished interface similar to ChatGPT or Claude Desktop while keeping data strictly within self-hosted or private enterprise environments.

Key challenges addressed by Open WebUI include:
1. **Centralized Model Access**: Exposing both local self-hosted models and external cloud API endpoints through a single, authenticated web interface or API proxy.
2. **Local Data Privacy & RAG**: Enabling users to drag-and-drop documents (PDFs, DOCX, TXT, code repositories) for instant vector search and grounded Q&A without leaking sensitive data to public cloud indexers.
3. **Tool Execution & Agent Capabilities**: Integrating MCP 3.1 endpoints, web search engines (SearXNG, Tavily), and custom Python execution pipes directly into chat sessions.
4. **Multi-Tenant Governance**: Providing admins with granular controls over user quotas, model accessibility, system prompts, usage tracking, and Single Sign-On (SSO / OAuth2 / OIDC).

## Architectural Overview & Request Lifecycle

Open WebUI is structured as an async FastAPI backend paired with a modern, responsive SvelteKit frontend. It utilizes SQLite or PostgreSQL for state persistence and integrates ChromaDB or PGVector for local document embeddings.

```mermaid
graph TD
    A[User Web Client / Browser] -->|HTTPS / WSS| B[Open WebUI SvelteKit Frontend]
    B -->|REST API / SSE Streams| C[FastAPI Backend Engine]

    C -->|Authentication & RBAC| D[(SQLite / PostgreSQL DB)]
    C -->|RAG Ingestion / Embeddings| E[(ChromaDB / Vector Store)]

    C -->|Chat Inference Request| F{Model Router / Provider}

    F -->|Local HTTP 11434| G[Ollama Server]
    F -->|OpenAI-Compatible REST| H[LiteLLM Gateway / vLLM]
    F -->|Cloud API Call| I[Anthropic / OpenAI / Gemini]

    C -->|Tool Call Execution| J[MCP 3.1 Tool Runner / FastMCP]
    J -->|JSON-RPC 2.0| K[External MCP Servers / APIs]

    G -->|Streaming Tokens| C
    H -->|Streaming Tokens| C
    I -->|Streaming Tokens| C
    C -->|SSE Token Stream| A
```

### Complete Sequence Flow for a RAG & MCP Chat Query

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as Open WebUI Frontend
    participant Backend as FastAPI Backend
    participant VectorDB as ChromaDB Vector Store
    participant LLM as Inference Engine (Ollama/LiteLLM)
    participant MCP as FastMCP 3.1 Server

    User->>Frontend: Send Message + Attach Document
    Frontend->>Backend: POST /api/chat/completions (With file ID)
    Backend->>VectorDB: Query relevant chunks (Cosine similarity)
    VectorDB-->>Backend: Return top-k document passages
    Backend->>Backend: Inject passages into System Prompt context
    Backend->>LLM: POST /v1/chat/completions (Prompt + Context + Tools)
    LLM-->>Backend: Response with Tool Call request (json)
    Backend->>MCP: Execute Tool via MCP 3.1 Task Protocol
    MCP-->>Backend: Return Tool Execution Result
    Backend->>LLM: Second Inference Pass (With Tool Result)
    LLM-->>Backend: Final Answer Token Stream
    Backend-->>Frontend: Server-Sent Events (SSE Stream)
    Frontend-->>User: Render Markdown + Citations
```

## Where it fits in the stack

**User Interface / Agentic Frontend Layer**. Open WebUI operates at the top of the self-hosted AI software stack. It interfaces downward with inference engines, vector databases, and MCP tool servers, while facing upward toward end users and client applications via OpenAI-compatible endpoints.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      End Users & Client Apps                           │
│           (Web Browser, Mobile PWA, API Extensions)                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Web Interface / SSE Token Stream
┌───────────────────────────────────▼────────────────────────────────────┐
│                             OPEN WEBUI                                 │
│  ┌───────────────────────┐ ┌──────────────────────┐ ┌───────────────┐  │
│  │  SvelteKit UI / Web   │ │ FastAPI Backend Core │ │ Admin & RBAC  │  │
│  └───────────────────────┘ └──────────────────────┘ └───────────────┘  │
│  ┌───────────────────────┐ ┌──────────────────────┐ ┌───────────────┐  │
│  │ Local RAG / ChromaDB  │ │ Pipes & Functions    │ │ MCP 3.1 Engine│  │
│  └───────────────────────┘ └──────────────────────┘ └───────────────┘  │
└──────────┬────────────────────────┬─────────────────────────┬──────────┘
           │ Local HTTP             │ OpenAI API              │ MCP / Webhooks
┌──────────▼───────────┐ ┌──────────▼───────────┐ ┌───────────▼──────────┐
│   Ollama / vLLM      │ │ LiteLLM / Cloud APIs │ │ FastMCP Tool Servers │
│  (Local GPU / GGUF)  │ │ (Claude, GPT, Gemini)│ │ (Databases, Scripts) │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

## Typical use cases

- **Enterprise AI Workstation**: Replacing commercial SaaS chat accounts with a private, audited self-hosted platform.
- **Interactive Document Analysis (Local RAG)**: Uploading research papers, financial reports, or technical manuals to perform cross-document comparison and citation extraction.
- **Model Arena & Evaluation**: Comparing outputs from multiple models (e.g., DeepSeek-V4 vs. Claude 5.1 vs. Llama 4) side-by-side using unified prompts.
- **Agentic Workflow Execution**: Exposing local shell execution, database query tools, and web browsing capabilities through MCP 3.1 servers.
- **Multi-User Team Collaboration**: Creating shared Channels, custom system prompts, and shared document knowledge bases across teams with granular access permissions.

## Key Features & Deep Capabilities

### 1. Advanced RAG Engine
Open WebUI features a built-in document ingestion engine supporting PDF, DOCX, PPTX, CSV, Markdown, and TXT files. It performs text extraction, chunking (with configurable overlap and chunk size), vector generation using local sentence-transformers (e.g., `all-MiniLM-L6-v2` or custom embedding endpoints), and stores embeddings in ChromaDB or PGVector.

### 2. Native MCP 3.1 & FastMCP Support
The platform natively speaks the Model Context Protocol. MCP servers can be added directly through the Admin Settings UI, enabling models to discover tools, resources, and prompt templates dynamically during conversation runs.

### 3. Open WebUI Pipelines & Functions
Users can extend Open WebUI using Python-based **Pipes** and **Filters**:
- **Pipes**: Act as custom model providers or workflow agents (e.g., routing requests through complex LangGraph or CrewAI chains).
- **Filters**: Intercept input prompts or output token streams for guardrailing, PII masking, or custom formatting.

### 4. Enterprise Security & RBAC
- **SSO/OIDC Integration**: Connects with [Authentik](authentik.md), Keycloak, Okta, or Entra ID.
- **Granular Permissions**: Admins can restrict specific models, document collections, or MCP tools to designated user roles.
- **SSRF & Sandbox Protections**: Built-in safeguards against Server-Side Request Forgery when calling external webhooks or running code interpreters.

## Strengths

- **User Experience**: Highly responsive, clean, modern UI featuring LaTeX math rendering, syntax-highlighted code blocks, and audio output.
- **Extensible Integration**: Supports Ollama, OpenAI-compatible APIs, direct Anthropic/Google endpoints, and custom Python Pipes.
- **Native Local RAG**: Drag-and-drop document upload with zero external database dependencies required out-of-the-box.
- **Built-In Multi-User Admin**: Comprehensive user management, invite links, rate limits, and usage logs.
- **Active Ecosystem & Community**: Rapid release cycles, extensive webhooks, and active community plugin contributions.

## Limitations

- **Resource Requirements**: Running the full web backend alongside vector embeddings and inference models requires sufficient RAM (minimum 4GB for web service, plus GPU memory for models).
- **Setup Complexity for Enterprise RAG**: Scaling vector storage to millions of chunks requires externalizing ChromaDB or migrating to PostgreSQL with `pgvector`.

## When to use it

- When setting up a multi-user AI portal for teams, family members, or an entire enterprise.
- When you need a private, self-hosted interface supporting both local GPU models and frontier cloud APIs.
- For local document question answering and agentic tool use via MCP 3.1.

## When not to use it

- When building a strictly headless API microservice that does not require a web interface.
- On ultra-resource-constrained single-board computers (e.g., Raspberry Pi 3/4) where CLI models are preferable.

## Getting started

### Enterprise Docker Compose Setup with Security Hardening

This production-grade Docker Compose configuration deploys Open WebUI alongside Ollama and an isolated PostgreSQL database for backend state storage.

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: open-webui-db
    environment:
      POSTGRES_DB: openwebui
      POSTGRES_USER: webui_admin
      POSTGRES_PASSWORD: SecurePostgresPassword2027!
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U webui_admin -d openwebui"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    container_name: ollama-server
    volumes:
      - ollama_storage:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui-app
    ports:
      - "3000:8080"
    depends_on:
      db:
        condition: service_healthy
      ollama:
        condition: service_started
    environment:
      - 'DATABASE_URL=postgresql://webui_admin:SecurePostgresPassword2027!@db:5432/openwebui'
      - 'OLLAMA_BASE_URL=http://ollama:11434'
      - 'WEBUI_SECRET_KEY=GeneratingSuperSecretJwtKey2027String'
      - 'ENABLE_RAG_WEB_SEARCH=True'
      - 'RAG_WEB_SEARCH_ENGINE=searxng'
      - 'SEARXNG_QUERY_URL=http://searxng:8080/search?q=<query>'
      - 'AIOHTTP_CLIENT_ALLOW_REDIRECTS=false'
      - 'IFRAME_CSP=default-src ''self''; script-src ''none'';'
    volumes:
      - open_webui_data:/app/backend/data
    restart: unless-stopped

volumes:
  postgres_data:
  ollama_storage:
  open_webui_data:
```

## CLI examples

Open WebUI is primarily a web service, but backend management tasks can be executed via `docker exec`:

```bash
# Reset admin user credentials via backend script
docker exec -it open-webui-app /app/backend/run_db_script.py --reset-admin

# Execute vector index reindexing for local RAG collections
docker exec -it open-webui-app python3 /app/backend/apps/rag/reindex.py

# Export database backup
docker exec -it open-webui-db pg_dump -U webui_admin openwebui > openwebui_backup_2027.sql
```

## API examples

### 1. OpenAI-Compatible Chat Completion Endpoint

```bash
curl -X POST http://localhost:3000/api/chat/completions \
  -H "Authorization: Bearer sk-openwebui-api-key-2027" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.3:latest",
    "messages": [
      {"role": "system", "content": "You are a helpful AI assistant."},
      {"role": "user", "content": "Explain quantum entanglement briefly."}
    ],
    "temperature": 0.7,
    "stream": false
  }'
```

### 2. FastMCP 3.1 Server & Pydantic v2 Open WebUI Management Tool

This Python service creates a FastMCP 3.1 server that manages Open WebUI user permissions, model quotas, and document collection queries with strict Pydantic v2 validation.

```python
import json
import logging
import requests
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from mcp.server.fastmcp import FastMCP

# Initialize Logging & FastMCP Server
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenWebUI-Manager")
mcp = FastMCP("OpenWebUI-Admin-Server")

class UserCreationSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of user")
    email: EmailStr = Field(..., description="Valid user email address")
    role: str = Field(default="user", description="Role: 'user' or 'admin'")
    password: str = Field(..., min_length=8, description="Initial account password")

class RAGQuerySchema(BaseModel):
    collection_name: str = Field(..., description="Target ChromaDB collection identifier")
    query_text: str = Field(..., min_length=3, description="Search prompt for document retrieval")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of document chunks to return")

class WebUIConfig(BaseModel):
    endpoint: str = Field(default="http://localhost:3000/api/v1")
    admin_api_key: str = Field(..., description="Admin bearer token")

@mcp.tool()
def create_webui_user(config_json: str, user_json: str) -> str:
    """
    Creates a new user in Open WebUI using admin credentials after validating
    input schemas with Pydantic v2.
    """
    try:
        cfg = WebUIConfig(**json.loads(config_json))
        user_data = UserCreationSchema(**user_json if isinstance(user_json, dict) else json.loads(user_json))

        url = f"{cfg.endpoint}/auth/admin/user/create"
        headers = {
            "Authorization": f"Bearer {cfg.admin_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": user_data.name,
            "email": user_data.email,
            "role": user_data.role,
            "password": user_data.password
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            return json.dumps({"status": "SUCCESS", "user_email": user_data.email, "role": user_data.role})
        else:
            return json.dumps({"status": "FAILED", "code": response.status_code, "detail": response.text})

    except Exception as e:
        logger.error(f"User creation failed: {str(e)}")
        return json.dumps({"status": "ERROR", "message": str(e)})

@mcp.tool()
def query_rag_knowledge_base(config_json: str, query_json: str) -> str:
    """
    Queries a specific Open WebUI RAG document collection for semantic chunks.
    """
    try:
        cfg = WebUIConfig(**json.loads(config_json))
        q = RAGQuerySchema(**query_json if isinstance(query_json, dict) else json.loads(query_json))

        url = f"{cfg.endpoint}/rag/query"
        headers = {"Authorization": f"Bearer {cfg.admin_api_key}"}
        payload = {
            "collection_name": q.collection_name,
            "query": q.query_text,
            "k": q.top_k
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json()
            return json.dumps({"status": "SUCCESS", "chunks_returned": len(results), "data": results}, indent=2)
        else:
            return json.dumps({"status": "FAILED", "code": response.status_code, "detail": response.text})

    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)})

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Ollama](ollama.md) — Primary local inference engine for chat and embeddings.
- [KoboldCPP](../tools/infrastructure/koboldcpp.md) — GGUF inference backend for local LLMs.
- [LiteLLM](litellm.md) — Unified API gateway for mapping Open WebUI requests to multi-cloud LLM providers.
- [Authentik](authentik.md) — Enterprise identity provider for SSO authentication.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Open standard for connecting tool servers to Open WebUI.
- [SearXNG](searXNG.md) — Privacy-respecting meta-search engine used for live web search grounding in Open WebUI.
- [n8n](n8n.md) — Workflow automation tool that can be triggered via Open WebUI webhooks or tools.

## Sources / references
- [Open WebUI Official Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub Repository](https://github.com/open-webui/open-webui)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
