# Open WebUI

## What it is
Open WebUI is a user-friendly WebUI for Large Language Models (LLMs), designed to provide a feature-rich, self-hosted chat interface. As of **June 2026**, it has fully adopted the **Model Context Protocol (MCP 3.0)** for natural language tool execution and resource discovery.

## What problem it solves
It provides a polished, ChatGPT-like interface for local LLMs (via Ollama) and external APIs, making them accessible to non-technical users. It adds features like RAG, multi-user support, and image generation that basic CLIs lack.

## Where it fits in the stack
**User Interface / Frontend**. It sits on top of inference engines like Ollama or LiteLLM to provide the chat experience. In an agentic ecosystem, it serves as the primary **human-agent collaboration portal**.

## Typical use cases
- **Self-Hosted AI Chat**: A private alternative to ChatGPT for family or organization use.
- **Local RAG**: Uploading documents to chat with them using local embeddings and LLMs.
- **Model Comparison**: Chatting with multiple models side-by-side to compare performance.
- **Agent Orchestration**: Invoking **Claude 4.8 Opus** or **GPT-5.5** with access to local tools and files.

## Strengths
- **Beautiful UI**: Modern, responsive, and customizable.
- **Local RAG Support**: Built-in support for document ingestion and retrieval.
- **Role-Based Access Control**: Multi-user support with admin controls.
- **Wide Compatibility**: Works with Ollama, OpenAI-compatible APIs, and more.
- **Channels & Streaming**: (v0.9.0+) Support for real-time model streaming in Channels with full tool and RAG support.
- **MCP 3.0 Integration**: Native support for connecting to and executing tools from any MCP-compliant server.

## Limitations
- **Resource Heavy**: Requires its own resources alongside the inference engine.
- **Setup Complexity**: RAG and advanced features require additional configuration (embeddings, vector stores).

## When to use it
- When you want a professional chat interface for your local models.
- If you need to share access to your LLM server with other people securely.
- For local document-based question answering (RAG).
- When you need a unified interface for multiple model providers with integrated tool support.

## When not to use it
- If you prefer a minimal CLI-only workflow.
- If you have extremely limited system resources.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation with Ollama (Docker Compose)
This example shows how to run Open WebUI and link it to an Ollama instance.

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    volumes:
      - ./ollama:/root/.ollama
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main # v0.9.0+ (June 2026)
    container_name: open-webui
    volumes:
      - ./open-webui:/app/backend/data
    depends_on:
      - ollama
    ports:
      - 3000:8080
    environment:
      - 'OLLAMA_BASE_URL=http://ollama:11434'
      # Security (v0.9.0+)
      - 'AIOHTTP_CLIENT_ALLOW_REDIRECTS=false' # SSRF protection
      - 'IFRAME_CSP=default-src '\''self'\''; script-src '\''none'\'';' # Artifacts/Previews sandbox
    restart: unless-stopped
```

## Security Posture (June 2026 Updates)
Open WebUI has introduced critical security hardening in recent versions (v0.8.11 and v0.9.0).
- **SSRF Protection**: Redirects are blocked by default for all outbound HTTP requests (web fetch, image loading, tool execution) to prevent server-side request forgery.
- **Iframe Sandboxing**: Administrators can now enforce a `Content-Security-Policy` for tool embeds and artifacts via the `IFRAME_CSP` environment variable.
- **CVE Fixes**: v0.8.11 addressed an information disclosure flaw (CVE-2026-45666) in the notes API; v0.9.0 addressed an authorization bypass (CVE-2026-45671) in file management.

## RAG & Knowledge Bases
Open WebUI provides a native "Knowledge" workspace to manage documents for Retrieval-Augmented Generation (RAG).

### Setting Up a Knowledge Base
1. Navigate to **Workspace > Knowledge**.
2. Click the **+** icon to create a new Knowledge Base.
3. Upload files (PDF, CSV, TXT, etc.) or sync an entire directory.
4. **Focused Retrieval**: Open WebUI will chunk and embed your documents using a local embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`) and store them in its internal ChromaDB.

### Using Knowledge in Chat
- **Direct Mention**: Type `#` in the chat bar to select a specific file or an entire Knowledge Base to include in the context.
- **Model Scoping**: Go to **Workspace > Models**, edit a model, and attach a Knowledge Base. This model will now automatically use that knowledge for every query.

### External Vector Databases
For large scale RAG, Open WebUI supports external vector stores like `Milvus` or `Qdrant` via environment variables:
```yaml
environment:
  - RAG_EMBEDDING_ENGINE=ollama
  - RAG_EMBEDDING_MODEL=mxbai-embed-large
  - VECTOR_DB=milvus
  - MILVUS_URI=http://milvus:19530
```

## CLI examples
Open WebUI is primarily a web application, but you can interact with its backend or manage the service via Docker.

```bash
# Pull the latest image
docker pull ghcr.io/open-webui/open-webui:main

# View application logs
docker logs -f open-webui

# Execute a maintenance command inside the container
docker exec -it open-webui flask db upgrade
```

## API examples
Open WebUI exposes an API for programmatic interaction, often used for custom integrations or agentic workflows.

### Python (Chat Completion)
```python
import requests

API_URL = "http://localhost:3000/api/chat/completed"
API_KEY = "YOUR_OPEN_WEBUI_API_KEY"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello, Open WebUI!"}]
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json())
```

## Related tools / concepts
- [Ollama](ollama.md) — Primary inference engine for chat and embeddings.
- [LiteLLM](litellm.md) — For connecting Open WebUI to external APIs with a single standard.
- [RAG (Retrieval Augmented Generation)](../knowledge_base/patterns/rag-pattern.md) — The underlying architecture for chatting with documents.
- [n8n](n8n.md) — For automating data ingestion into Open WebUI knowledge bases.
- [Authentik](authentik.md) — For managing SSO and RBAC in multi-user deployments.
- [Claude 4.8 Opus](../tools/ai_knowledge/claude.md) — High-fidelity reasoning model compatible with Open WebUI via LiteLLM.
- [GPT-5.5](../tools/ai_knowledge/chatgpt.md) — Premier multimodal model for Open WebUI orchestration.
- [MCP 3.0](../knowledge_base/patterns/tool-calling-and-mcp.md) — The protocol used for tool and resource discovery.

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Sources / References
- [Open WebUI Official Documentation](https://docs.openwebui.com/)
- [Open WebUI GitHub Repository](https://github.com/open-webui/open-webui)
- [Open WebUI Changelog](https://github.com/open-webui/open-webui/blob/main/CHANGELOG.md)
- [CVE-2026-45666 Vulnerability Details](https://www.sentinelone.com/vulnerability-database/cve-2026-45666/)
- [CVE-2026-45671 Vulnerability Details](https://www.sentinelone.com/vulnerability-database/cve-2026-45671/)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
