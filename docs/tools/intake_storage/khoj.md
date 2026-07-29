# Khoj

## What it is
Khoj is an open-source, personal AI assistant that serves as a "second brain" for your documents, notes, and web research. As of late 2026, it has expanded into a full agentic ecosystem with the **Pipali v2.5** desktop coworker and **Open Paper** research workbench.

## What problem it solves
It bridges the gap between disparate data sources (Markdown, PDFs, GitHub, Notion) and conversational AI. It solves the "context gap" by providing LLMs with secure, semantic access to your personal knowledge base while maintaining 100% data ownership.

## Where it fits in the stack
**Category**: Agent / Knowledge Management / Search. It acts as the retrieval and reasoning layer for personal data, connecting to various intake sources and exposing them via a unified interface.

## Typical use cases
- **Personal Knowledge Search**: Ask questions across Obsidian, Emacs Org-mode, and local PDF libraries.
- **Automated Research**: Use **Pipali** to conduct deep web research and generate polished briefs or reports.
- **Academic Workbench**: Leverage **Open Paper** to organize and understand academic papers with verifiable citations.
- **Self-Hosted AI**: Run private, local LLMs (Llama 4, Gemma 3) against your sensitive data.

## Strengths
- **Local-First**: Supports 100% offline operation with local embedding and inference models.
- **Multimodal**: Handles text, images, and voice across multiple platforms (Web, Desktop, Obsidian, Emacs).
- **Agentic**: The **Pipali** agent can execute code in sandboxes and interact with apps via MCP 3.1.
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

### Docker Compose Setup
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

# Start the Pipali desktop coworker
pipali start

# Add an MCP server to Pipali's skill set (MCP 3.1 Standard)
pipali mcp add --transport stdio --command npx --args "@modelcontextprotocol/server-filesystem /docs"
```

## API examples
Khoj provides a REST API for agents and external integrations. Under late 2026 guidelines, programmatic queries should validate both request schemas and model payloads using **Pydantic v2**.

### Chat payload validation and execution (Python)
```python
import requests
from pydantic import BaseModel, Field
from typing import Optional

# Define Pydantic v2 schemas for request verification
class KhojChatPayload(BaseModel):
    message: str = Field(..., min_length=1, description="Message to Khoj agent")
    stream: bool = Field(default=False)
    model: str = Field(default="claude-5-1-sonnet-20261022", description="Frontier model target")
    agent_id: Optional[str] = Field(default="research-assistant")

class KhojChatResponse(BaseModel):
    response: str
    context_sources: Optional[list] = None

# Validate input request
raw_input = {
    "message": "Summarize my notes on the K3s cluster migration.",
    "model": "claude-5-1-sonnet-20261022",
    "agent_id": "research-assistant"
}

try:
    # Model validation under Pydantic v2
    payload = KhojChatPayload.model_validate(raw_input)
    print(f"Validated payload message: '{payload.message}'")

    API_TOKEN = "YOUR_KHOJ_API_TOKEN"
    API_URL = "http://localhost:8000/api/chat"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # response = requests.post(API_URL, headers=headers, json=payload.model_dump())
    # parsed_resp = KhojChatResponse.model_validate(response.json())
except Exception as e:
    print(f"Schema validation failed: {e}")
```

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) — Excellent as a primary data source for Khoj.
- [Verba](verba.md) — Weaviate-powered RAG alternative.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system that can feed into Khoj.
- [n8n](../../services/n8n.md) — Automate data ingestion into Khoj via standard webhooks.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The protocol used by Pipali for tool integration (Standard 3.1).
- [Llama 4](../ai_knowledge/local_llms.md) — Standard model for local privacy-first processing.
- [Claude 5.1](../providers/anthropic.md) — Frontier model supported via API integration.
- [AnyType](anytype.md) — Alternative local-first knowledge base.

## Sources / references
- [Official Website](https://khoj.dev/)
- [Khoj GitHub Repository](https://github.com/khoj-ai/khoj)
- [Pipali GitHub Repository](https://github.com/khoj-ai/pipali)
- [Khoj Documentation](https://docs.khoj.dev/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
