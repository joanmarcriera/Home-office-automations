# Open WebUI

## What it is
Open WebUI is a user-friendly WebUI for Large Language Models (LLMs), designed to provide a feature-rich, self-hosted chat interface. As of July 2026, it serves as a central hub for multi-model orchestration, featuring native Model Context Protocol (MCP 3.0) support, **FastMCP 3.0** discovery, and seamless integration with frontier models like Claude 4.8 Opus, GPT-5.5, and [Gemma 3](../tools/ai_knowledge/local_llms.md). Open WebUI is open source (MIT License) and free to self-host.

## What problem it solves
It provides a polished, ChatGPT-like interface for local LLMs (via Ollama) and external APIs, making them accessible to non-technical users. It adds features like RAG, multi-user support, tool execution, and image generation that basic CLIs lack.

## Where it fits in the stack
**User Interface / Frontend**. It sits on top of inference engines like Ollama or LiteLLM to provide the chat experience. It acts as an **Agentic Desktop** when used with its built-in tool and MCP capabilities.

## Typical use cases
- **Self-Hosted AI Chat**: A private alternative to ChatGPT for family or organization use.
- **Local RAG**: Uploading documents to chat with them using local embeddings and LLMs.
- **Model Comparison**: Chatting with multiple models side-by-side to compare performance.
- **Agentic Workflows**: Utilizing MCP 3.0 tools to interact with local files, databases, and APIs directly from the chat interface.
- **Agentic Session Orchestration**: Coordinating multi-tool sessions using the **MCP 3.0 Task Protocol** for complex, long-running agent tasks.

## Strengths
- **Beautiful UI**: Modern, responsive, and customizable.
- **Local RAG Support**: Built-in support for document ingestion and retrieval with ChromaDB or external vector stores.
- **Role-Based Access Control**: Multi-user support with admin controls and granular permissions.
- **MCP 3.0 Support**: Native integration with the Model Context Protocol for extensible tool use.
- **Channels & Streaming**: Support for real-time model streaming in Channels with full tool and RAG support.

## Limitations
- **Resource Heavy**: Requires its own resources alongside the inference engine.
- **Setup Complexity**: RAG and advanced features (MCP, external DBs) require additional configuration.

## When to use it
- When you want a professional chat interface for your local models.
- If you need to share access to your LLM server with other people securely.
- For local document-based question answering (RAG) and agentic tool use via MCP.

## When not to use it
- If you prefer a minimal CLI-only workflow.
- If you have extremely limited system resources.

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
    image: ghcr.io/open-webui/open-webui:main # v0.9.x (June 2026)
    container_name: open-webui
    volumes:
      - ./open-webui:/app/backend/data
    depends_on:
      - ollama
    ports:
      - 3000:8080
    environment:
      - 'OLLAMA_BASE_URL=http://ollama:11434'
      - 'AIOHTTP_CLIENT_ALLOW_REDIRECTS=false' # SSRF protection
      - 'IFRAME_CSP=default-src ''self''; script-src ''none'';' # Sandbox
    restart: unless-stopped
```

## CLI examples
Open WebUI is primarily a web service, but the backend can be managed via `docker exec`:

```bash
# Reset admin password
docker exec -it open-webui /app/backend/run_db_script.py --reset-admin

# List all users
docker exec -it open-webui /app/backend/run_db_script.py --list-users

# Export configuration
docker exec -it open-webui tar -czf config_backup.tar.gz /app/backend/data
```

## API examples
Open WebUI exposes an API for programmatic chat and management.

### Chat Completion (OpenAI Compatible)
```bash
curl -X POST http://localhost:3000/api/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Management API (Python)
```python
import requests

API_KEY = "your_admin_api_key"
BASE_URL = "http://localhost:3000/api/v1"

headers = {"Authorization": f"Bearer {API_KEY}"}

# Get system health
response = requests.get(f"{BASE_URL}/health", headers=headers)
print(response.json())

# List available models
models = requests.get(f"{BASE_URL}/models", headers=headers)
for model in models.json()["data"]:
    print(f"Model ID: {model['id']}")
```

## Related tools / concepts
- [Ollama](ollama.md) — Primary inference engine for chat and embeddings.
- [LiteLLM](litellm.md) — For connecting Open WebUI to external APIs and frontier models like Claude 4.8 Opus.
- [RAG (Retrieval Augmented Generation)](../knowledge_base/patterns/rag-pattern.md) — The underlying architecture for chatting with documents.
- [Model Context Protocol](../automation_orchestration/mcp.md) — The standard for tool integration supported by Open WebUI.
- [Everything MCP](https://github.com/punkpeye/awesome-mcp) — A curated list of MCP servers that can be used with Open WebUI.
- [ChromaDB](https://www.trychroma.com/) — The default vector database used for local RAG.
- [n8n](n8n.md) — For building complex workflows that Open WebUI can trigger via webhooks.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Powerful local model for use with Open WebUI.
- [Authentik](authentik.md) — For adding SSO and security to self-hosted utilities.
- [FastMCP](https://github.com/jlowin/fastmcp) — High-performance MCP server framework for ultra-low latency tool execution.

## Sources / References
- [Open WebUI Official Docs](https://docs.openwebui.com/)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
