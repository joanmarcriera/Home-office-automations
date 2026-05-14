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

## Prompt Engineering & Templates
Paperless-AI uses system prompts to guide the LLM in document analysis. High-quality templates are essential for accurate extraction of complex documents like invoices.

### Advanced Invoice Extraction Template
For best results when extracting financial data, use a structured prompt that enforces JSON output and defines data types.

```markdown
You are a high-precision data extraction assistant. Analyze the provided document and extract the following fields.

## Fields to Extract:
- **Amount**: Total amount including tax. Format: [CurrencyCode][Amount] (e.g., USD150.00).
- **Date**: The issue date of the invoice. Format: YYYY-MM-DD.
- **Correspondent**: The name of the company or person who issued the invoice.
- **Invoice Number**: The unique identifier for this document.

## Output Rules:
1. Return ONLY a valid JSON object. No markdown, no explanations.
2. If a field cannot be found, omit it from the JSON.
3. Use a period (.) as the decimal separator. No thousand separators.
```

### Configuration via Environment
You can override the default prompts using environment variables in your `docker-compose.yaml`:

```yaml
environment:
  - SYSTEM_PROMPT="You are a document classifier..."
  - USER_PROMPT="Analyze this document and return tags..."
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — The core document management system.
- [Ollama](ollama.md) — For running local LLMs like Llama 3 or Mistral.
- [n8n](n8n.md) — For advanced post-processing workflows.
- [Extraction and Classification](../reference-implementations/llm-prompts/extraction-and-classification.md) — General patterns for LLM extraction.

## Backlog

## Sources / References
- [GitHub Repository](https://github.com/clusterfudge/paperless-ai)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
