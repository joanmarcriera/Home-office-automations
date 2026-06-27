# Khoj

## What it is
Khoj is an open-source, personal AI assistant that serves as a "second brain" for your documents, notes, and web research. As of June 2026, it has expanded into a full agentic ecosystem with the **Pipali** desktop coworker and **Open Paper** research workbench. It is licensed under AGPL-3.0 and supports 100% private, self-hosted operation.

## What problem it solves
It bridges the gap between disparate data sources (Markdown, PDFs, GitHub, Notion) and conversational AI. It solves the "context gap" by providing frontier models like **Claude 4.8 Opus** and **GPT-5.5** with secure, semantic access to your personal knowledge base without sacrificing privacy.

## Where it fits in the stack
**Category**: Agent / Knowledge Management / Search. It acts as the retrieval and reasoning layer for personal and organizational knowledge bases.

## Typical use cases
- **Personal Knowledge Search**: Ask questions across Obsidian, Emacs Org-mode, and local PDF libraries.
- **Automated Research**: Use **Pipali** to conduct deep web research and generate polished briefs or reports.
- **Academic Workbench**: Leverage **Open Paper** to organize and understand academic papers with verifiable citations.
- **Self-Hosted AI**: Run private, local LLMs (Llama 4 Maverick, Mistral) against your sensitive data.

## Strengths
- **Local-First**: Supports 100% offline operation with local embedding and inference models.
- **Multimodal**: Handles text, images, and voice across multiple platforms (Web, Desktop, Obsidian, Emacs).
- **Agentic**: The **Pipali** agent can execute code in sandboxes and interact with apps via MCP 3.0.
- **Privacy-Centric**: Strong focus on data ownership and secure self-hosting.
- **Open Source**: Fully transparent AGPL-3.0 codebase.

## Limitations
- Indexing very large datasets (100GB+) requires significant RAM and GPU resources.
- Initial Docker setup may be challenging for non-technical users.
- Real-time synchronization for some cloud providers (e.g., Notion) can have latency.

## When to use it
- When you want a unified, AI-powered search across all your personal and professional knowledge.
- If you need a research assistant that can cite its sources from your own documents.
- If you require a privacy-focused alternative to cloud-based assistants.
- When using **Claude 4.8** or **GPT-5.5** for high-precision knowledge work.

## When not to use it
- For public-facing, high-traffic search engines.
- If you lack the hardware (minimum 16GB RAM) to run the indexing and LLM locally.
- For extremely simple note-taking that doesn't require AI search or reasoning.

## Getting started
### Docker Compose Setup (v2.0+)
Khoj requires PostgreSQL with `pgvector` for semantic search.

```yaml
services:
  khoj:
    image: ghcr.io/khoj-ai/khoj-cloud:latest
    ports:
      - "8000:8000"
    volumes:
      - khoj_data:/app/khoj
    environment:
      - KHOJ_ADMIN_EMAIL=admin@example.com
      - KHOJ_ADMIN_PASSWORD=secure_password
      - DATABASE_URL=postgresql://khoj:password@db:5432/khoj
    depends_on:
      db:
        condition: service_healthy

  db:
    image: pgvector/pgvector:pg16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=khoj
      - POSTGRES_USER=khoj
      - POSTGRES_PASSWORD=password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U khoj"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  khoj_data:
  postgres_data:
```

## CLI examples
Khoj and Pipali offer robust command-line interfaces for indexing and agentic control.

### Basic Indexing
```bash
# Install the Khoj CLI
pip install khoj

# Index a local directory of Markdown files
khoj index --path ~/Documents/Notes --type markdown

# Start the search server
khoj serve
```

### Pipali (Desktop Coworker)
```bash
# Start Pipali with MCP 3.0 support
pipali start --mcp-port 3000

# List active tools available to Pipali
pipali tools list
```

## API examples
Khoj provides a REST API and supports MCP 3.0 for tool-based retrieval.

### Chat with an Agent (Python)
```python
import requests

API_TOKEN = "YOUR_KHOJ_API_TOKEN"
API_URL = "http://localhost:8000/api/chat"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "message": "Summarize my notes on the K3s cluster migration.",
    "stream": False,
    "agent_id": "research-assistant"
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json()['response'])
```

### MCP 3.0 Tool Calling
Pipali exposes tools via MCP 3.0:
- `khoj_search`: Semantic search across indexed docs.
- `khoj_research`: Multi-step web + local research task.
- `khoj_update_index`: Force refresh of data sources.

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) — Primary data source and interface for Khoj.
- [Verba](verba.md) — Weaviate-powered RAG alternative for personal knowledge.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system that can feed into Khoj.
- [n8n](../../services/n8n.md) — Automate data ingestion into the Khoj knowledge base.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The protocol used by Pipali for tool integration.
- [Chronos MCP](../automation_orchestration/mcp.md) — Used for calendar orchestration within the Khoj ecosystem.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Recommended local model for private reasoning.
- [AnyType](anytype.md) — Local-first P2P knowledge base.

## Sources / references
- [Official Website](https://khoj.dev/)
- [Khoj GitHub Repository](https://github.com/khoj-ai/khoj)
- [Pipali GitHub Repository](https://github.com/khoj-ai/pipali)
- [Khoj Documentation](https://docs.khoj.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
