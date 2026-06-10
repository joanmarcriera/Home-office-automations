# Khoj

## What it is
Khoj is an open-source, personal AI assistant that serves as a "second brain" for your documents, notes, and web research. As of 2026, it has expanded into a full agentic ecosystem with the **Pipali** desktop coworker and **Open Paper** research workbench.

## What problem it solves
It bridges the gap between disparate data sources (Markdown, PDFs, GitHub, Notion) and conversational AI. It solves the "context gap" by providing LLMs with secure, semantic access to your personal knowledge base.

## Where it fits in the stack
**Category**: Agent / Knowledge Management / Search

## Typical use cases
- **Personal Knowledge Search**: Ask questions across Obsidian, Emacs Org-mode, and local PDF libraries.
- **Automated Research**: Use **Pipali** to conduct deep web research and generate polished briefs or reports.
- **Academic Workbench**: Leverage **Open Paper** to organize and understand academic papers with verifiable citations.
- **Self-Hosted AI**: Run private, local LLMs (Llama 4 Maverick, Mistral) against your sensitive data.

## Strengths
- **Local-First**: Supports 100% offline operation with local embedding and inference models.
- **Multimodal**: Handles text, images, and voice across multiple platforms (Web, Desktop, Obsidian, Emacs).
- **Agentic**: The **Pipali** agent can execute code in sandboxes and interact with apps via MCP.
- **Privacy-Centric**: Strong focus on data ownership and secure self-hosting.

## Limitations
- Indexing very large datasets (100GB+) requires significant RAM and GPU resources.
- Initial Docker setup may be challenging for non-technical users.

## When to use it
- When you want a unified, AI-powered search across all your personal and professional knowledge.
- If you need a research assistant that can cite its sources from your own documents.
- If you require a privacy-focused alternative to cloud-based assistants.

## When not to use it
- For public-facing, high-traffic search engines.
- If you lack the hardware (minimum 16GB RAM) to run the indexing and LLM locally.

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0)
- **Cost**: Free (Self-hosted) / Paid (Cloud)
- **Self-hostable**: Yes

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

## API examples
Khoj provides a REST API for agents and external integrations.

### Chat with an Agent (Python)
```python
import requests

API_TOKEN = "YOUR_KHOJ_API_TOKEN" # Standardized naming
API_URL = "http://localhost:8000/api/chat"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "message": "Summarize my notes on the K3s cluster migration.",
    "stream": False,
    "agent_id": "research-assistant" # Optional: specify a custom agent
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json()['response'])
```

## CLI and Desktop Integration
- **Pipali**: The desktop coworker (`pipali`) runs on your machine and uses MCP to talk to your local apps.
- **Khoj CLI**: Use `pip install khoj` for command-line indexing and search.

## Model Context Protocol (MCP) Integration
Khoj and Pipali support MCP to bridge your knowledge base with your tools.

**Available Tools (via Pipali):**
- `khoj_search`: Perform semantic search across your indexed documents.
- `khoj_research`: Trigger a multi-step research task using the web and local docs.
- `khoj_update_index`: Force a refresh of specific folders or data sources.

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) — Excellent as a primary data source for Khoj.
- [Verba](verba.md) — Weaviate-powered RAG alternative.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system that can feed into Khoj.
- [n8n](../../services/n8n.md) — Automate data ingestion into Khoj.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The protocol used by Pipali for tool integration.

## Sources / References
- [Official Website](https://khoj.dev/)
- [Khoj GitHub Repository](https://github.com/khoj-ai/khoj)
- [Pipali GitHub Repository](https://github.com/khoj-ai/pipali)
- [Khoj Documentation](https://docs.khoj.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
