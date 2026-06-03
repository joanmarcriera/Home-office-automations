# AnythingLLM

## What it is
AnythingLLM is a privacy-first workspace application for running AI assistants with documents, vector search, agent workflows, and multiple local or hosted model backends.

## What problem it solves
It gives teams an "all-in-one" application surface for internal knowledge work without forcing them to assemble chat UI, retrieval, vector storage, and model connectors from scratch.

## Where it fits in the stack
**AI & Knowledge / Internal AI Workspace**. It is an application layer for internal knowledge assistants, document-grounded chat, and lightweight agent workflows.

## Typical use cases
- Internal knowledge base chat over company docs
- Team workspaces with document upload and retrieval
- Privacy-first AI assistant deployments using local or self-hosted models

## Strengths
- Strong out-of-the-box internal assistant experience
- Works with local and hosted model backends
- Useful bridge between prototype and internal deployment

## Limitations
- Less flexible than building your own fully custom app stack
- Product conventions may not match every enterprise workflow

## When to use it
- When you want a fast internal AI workspace for teams
- When document-grounded assistants matter more than bespoke product UX

## When not to use it
- When you need a fully custom application architecture
- When a simple RAG API service is enough and a full workspace UI is unnecessary

## Getting started

### Installation
AnythingLLM can be installed as a Desktop application or run via Docker.

**Desktop**: Download the installer from the [official website](https://anythingllm.com/download).

**Docker (Linux/macOS/Windows)**:
```bash
docker pull mintplexlabs/anythingllm
export STORAGE_LOCATION=$HOME/anythingllm && mkdir -p $STORAGE_LOCATION && touch "$STORAGE_LOCATION/.env"
docker run -d -p 3001:3001 --cap-add SYS_ADMIN -v "$STORAGE_LOCATION:/app/storage" -v "$STORAGE_LOCATION/.env:/app/server/.env" --name anythingllm mintplexlabs/anythingllm
```

## CLI examples

### 1. Run via Docker Compose
Create a `docker-compose.yml`:
```yaml
services:
  anythingllm:
    image: mintplexlabs/anythingllm
    container_name: anythingllm
    ports:
      - "3001:3001"
    cap_add:
      - SYS_ADMIN
    volumes:
      - ./storage:/app/storage
      - .env:/app/server/.env
    restart: always
```
Then run: `docker compose up -d`

### 2. View Container Logs
```bash
docker logs -f anythingllm
```

### 3. Access Container Shell
```bash
docker exec -it anythingllm /bin/bash
```

## API examples

### REST API (Python/curl)
AnythingLLM provides a Developer API (enabled in Settings -> Developer API).

```bash
# Get all workspaces
curl -X GET 'http://localhost:3001/api/v1/workspaces' \
  -H "Authorization: Bearer $ANYTHINGLLM_API_KEY"
```

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "http://localhost:3001/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Chat with a specific workspace
workspace_slug = "my-internal-kb"
data = {
    "message": "What is our policy on remote work?",
    "mode": "query" # 'query' for RAG, 'chat' for conversation
}

response = requests.post(f"{BASE_URL}/workspace/{workspace_slug}/chat", json=data, headers=headers)
print(response.json()['textResponse'])
```

## Related tools / concepts
- [Flowise](flowise.md)
- [Ollama](../../services/ollama.md)
- [LocalAI](../infrastructure/localai.md)
- [Open WebUI](../../services/open-webui.md)
- [LibreChat](librechat.md)
- [Dify](dify.md)

## Sources / References
- [Official Website](https://anythingllm.com)
- [GitHub Repository](https://github.com/Mintplex-Labs/anything-llm)
- [AnythingLLM Documentation](https://docs.useanything.com/introduction)

## Contribution Metadata
- Last reviewed: 2026-06-03
- Confidence: high
