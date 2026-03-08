# Paperless-AI

## What it is
Paperless-AI is a companion tool for Paperless-ngx that uses Artificial Intelligence to automate document tagging, correspondent detection, and metadata extraction.

## What problem it solves
It eliminates the tedious manual work of organizing scanned documents. By analyzing the actual content of documents with LLMs, it can accurately categorize them in ways that simple rule-based matching cannot.

## Where it fits in the stack
**Service Companion / Automation**. It works alongside Paperless-ngx, acting as an intelligent processing layer for newly added documents.

## Typical use cases
- **Automated Tagging**: Assigning tags like "Invoice", "Medical", or "Contract" based on document content.
- **Correspondent Detection**: Identifying the sender or organization associated with a document.
- **Metadata Extraction**: Pulling specific fields like dates, amounts, or account numbers from documents.

## Strengths
- **Native Paperless-ngx Integration**: Designed specifically to work with the Paperless-ngx API.
- **Local LLM Support**: Can use Ollama for completely private document processing.
- **Improved Accuracy**: Uses the semantic power of LLMs instead of fragile regex or keyword matching.

## Limitations
- **Processing Time**: LLM analysis takes longer than simple matching rules.
- **Dependency**: Requires a running instance of Paperless-ngx and an LLM provider (local or cloud).

## When to use it
- If you have a high volume of documents in Paperless-ngx that need organization.
- When you want to leverage local AI for document management without data leaving your server.

## When not to use it
- If your document organization needs are already well-handled by Paperless-ngx's native matching algorithms.
- If you have very limited CPU/GPU resources for running LLMs.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Environment Configuration (Local Ollama)
To connect Paperless-AI to a local Ollama instance and Paperless-ngx:

```bash
# Paperless-ngx Connection
PAPERLESS_URL=http://paperless-ngx:8000
PAPERLESS_TOKEN=your_api_token_here

# AI Provider (Ollama)
AI_PROVIDER=ollama
OLLAMA_URL=http://ollama:11434
AI_MODEL=llama3
```

### Docker Compose Snippet
```yaml
services:
  paperless-ai:
    image: clusterfudge/paperless-ai:latest
    container_name: paperless-ai
    environment:
      - PAPERLESS_URL=http://paperless-ngx:8000
      - PAPERLESS_TOKEN=your_token
      - AI_PROVIDER=ollama
      - OLLAMA_URL=http://ollama:11434
      - AI_MODEL=llama3
    restart: unless-stopped
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md)
- [Ollama](ollama.md)

## Backlog
- Improve prompt templates for better invoice extraction.

## Sources / References
- [GitHub Repository](https://github.com/clusterfudge/paperless-ai)
- [Teedy Official Website](https://teedy.io/)

## Contribution Metadata
- Last reviewed: 2026-03-08
- Confidence: medium
