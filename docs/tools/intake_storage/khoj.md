# Khoj

## What it is
Khoj is an open-source, personal AI assistant that can search through your notes, documents, and even external files to provide context-aware answers.

## What problem it solves
It bridges the gap between your disparate data sources (Markdown notes, PDFs, GitHub repos) and a conversational AI interface.

## Where it fits in the stack
**Category**: Agent / Knowledge Management / Search

## Typical use cases
- Searching through personal notes (Obsidian, Emacs Org-mode).
- Asking questions about local document repositories.
- Automating information retrieval for daily tasks.

## Strengths
- Supports offline, local-first operation.
- Integrates with popular note-taking apps.
- Features a desktop app and Emacs plugin.

## Limitations
- Indexing large datasets can be resource-intensive.
- Initial setup might require some technical knowledge.

## When to use it
- When you want a unified, AI-powered search across all your personal knowledge.

## When not to use it
- For public-facing search engines or large-scale enterprise data.

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0)
- **Cost**: Free (Self-hosted) / Paid (Cloud)
- **Self-hostable**: Yes

## Getting started
### Docker Compose Setup
Khoj can be self-hosted using Docker. It requires a PostgreSQL database with the `pgvector` extension.

```yaml
services:
  khoj:
    image: ghcr.io/khoj-ai/khoj-cloud:latest
    ports:
      - "8000:8000"
    environment:
      - KHOJ_ADMIN_EMAIL=admin@example.com
      - KHOJ_ADMIN_PASSWORD=secure_password
      - DATABASE_URL=postgresql://khoj:password@db:5432/khoj
    depends_on:
      db:
        condition: service_healthy

  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_DB=khoj
      - POSTGRES_USER=khoj
      - POSTGRES_PASSWORD=password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U khoj"]
      interval: 5s
      timeout: 5s
      retries: 5
```

## API examples
Khoj provides a REST API for interacting with your indexed documents and agents.

### Chat with an Agent
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What do my notes say about the K3s cluster setup?",
    "stream": false
  }'
```

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) — Primary source for many Khoj users.
- [AnyType](anytype.md) — Local-first P2P knowledge base.
- [Verba](verba.md) — Weaviate-powered RAG assistant.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system.
- [n8n](../../services/n8n.md) — Automation tool for ingesting data into Khoj.
- [Local LLM](../ai_knowledge/ollama.md) — Can be used as the inference backend for Khoj.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — The underlying architecture of Khoj.

## Sources / References
- [Official Website](https://khoj.dev/)
- [GitHub Repository](https://github.com/khoj-ai/khoj)
- [Khoj Documentation](https://docs.khoj.dev/)
- [Railway Deployment Template](https://railway.com/deploy/khoj)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
