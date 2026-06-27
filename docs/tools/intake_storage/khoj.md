# Khoj

## What it is
Khoj is an open-source, personal AI assistant that serves as a "second brain" for your documents, notes, and web research. As of June 2026, it has expanded into a full agentic ecosystem with the **Pipali v2.0** desktop coworker and **Open Paper** research workbench.

## What problem it solves
It bridges the gap between disparate data sources (Markdown, PDFs, GitHub, Notion) and conversational AI. It solves the "context gap" by providing LLMs with secure, semantic access to your personal knowledge base while maintaining 100% data ownership.

## Where it fits in the stack
**Category**: Agent / Knowledge Management / Search. It acts as the retrieval and reasoning layer for personal data, connecting to various intake sources and exposing them via a unified interface.

## Typical use cases
- **Personal Knowledge Search**: Ask questions across Obsidian, Emacs Org-mode, and local PDF libraries.
- **Automated Research**: Use **Pipali** to conduct deep web research and generate polished briefs or reports.
- **Academic Workbench**: Leverage **Open Paper** to organize and understand academic papers with verifiable citations.
- **Self-Hosted AI**: Run private, local LLMs (Llama 4 Maverick, Mistral) against your sensitive data.

## Strengths
- **Local-First**: Supports 100% offline operation with local embedding and inference models.
- **Multimodal**: Handles text, images, and voice across multiple platforms (Web, Desktop, Obsidian, Emacs).
- **Agentic**: The **Pipali** agent can execute code in sandboxes and interact with apps via MCP 3.0.
- **Privacy-Centric**: Strong focus on data ownership and secure self-hosting with AGPL-3.0 licensing.

## Limitations
- Indexing very large datasets (100GB+) requires significant RAM and GPU resources.
- Initial Docker setup may be challenging for non-technical users.
- Performance on older hardware can be slow when using high-parameter local models.

## When to use it
- When you want a unified, AI-powered search across all your personal and professional knowledge.
- If you need a research assistant that can cite its sources from your own documents.
- If you require a privacy-focused alternative to cloud-based assistants.

## When not to use it
- For public-facing, high-traffic search engines.
- If you lack the hardware (minimum 16GB RAM) to run the indexing and LLM locally.
- If your primary data resides in proprietary cloud silos with no API access.

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
Khoj provides a CLI for indexing and the Pipali desktop component for local automation.

```bash
# Install Khoj CLI
pip install khoj

# Index a local directory
khoj configure --path ~/my-docs

# Start the Pipali desktop coworker (June 2026)
pipali start

# Add an MCP server to Pipali's skill set
pipali mcp add --transport stdio --command npx --args "@modelcontextprotocol/server-filesystem /docs"
```

## API examples
Khoj provides a REST API for agents and external integrations, supporting standard model identifiers like `claude-4-8-opus-20260528`.

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
    "model": "claude-4-8-opus-20260528",
    "agent_id": "research-assistant"
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json()['response'])
```

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) — Excellent as a primary data source for Khoj.
- [Verba](verba.md) — Weaviate-powered RAG alternative.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system that can feed into Khoj.
- [n8n](../../services/n8n.md) — Automate data ingestion into Khoj via standard webhooks.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The protocol used by Pipali for tool integration (Standard 3.0).
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Standard model for local privacy-first processing.
- [Claude 4.8](../providers/anthropic.md) — Frontier model supported via API integration.
- [AnyType](anytype.md) — Alternative local-first knowledge base.

## Sources / references
- [Official Website](https://khoj.dev/)
- [Khoj GitHub Repository](https://github.com/khoj-ai/khoj)
- [Pipali GitHub Repository](https://github.com/khoj-ai/pipali)
- [Khoj Documentation](https://docs.khoj.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
