# Paperless-AI

Paperless-AI is a companion tool for Paperless-ngx that uses Artificial Intelligence to automate document tagging, correspondent detection, and metadata extraction.

## What it is
Paperless-AI is a specialized automation layer designed to enhance [Paperless-ngx](paperless-ngx.md). It leverages Large Language Models (LLMs) to analyze document content semantically, providing a level of organization and insight that traditional rule-based systems cannot achieve. As of June 2026, it supports native integration with **Claude 4.8 Opus** and **GPT-5.5** for high-precision extraction.

## What problem it solves
It eliminates the tedious manual work of organizing scanned documents. While Paperless-ngx has robust matching algorithms, they are often restricted to literal text matches or regex. Paperless-AI understands the context of a document, allowing it to accurately categorize "that weird invoice from the plumber" even if it doesn't follow a standard template.

## Where it fits in the stack
**Service Companion / Automation**. It works alongside Paperless-ngx, acting as an intelligent processing layer for newly added documents. It is typically deployed as a Docker container within the same network as the Paperless-ngx instance.

## Typical use cases
- **Automated Tagging**: Assigning tags like "Invoice", "Medical", or "Contract" based on document content.
- **Correspondent Detection**: Identifying the sender or organization associated with a document.
- **Metadata Extraction**: Pulling specific fields like dates, amounts, or account numbers from documents.
- **Document Q&A**: Using the "Chat" function to query the content of your archive using local or cloud LLMs.

## Strengths
- **Native Paperless-ngx Integration**: Designed specifically to work with the Paperless-ngx API.
- **Local LLM Support**: Can use [Ollama](ollama.md) or [LM Studio](../tools/infrastructure/lm-studio.md) for completely private document processing.
- **Chat Functionality**: Interact with your documents via a chat interface (enhanced in 2026).
- **Improved Accuracy**: Uses the semantic power of LLMs instead of fragile regex or keyword matching.
- **Open Source**: MIT Licensed and fully self-hostable.

## Limitations
- **Processing Time**: LLM analysis takes significantly longer than simple matching rules.
- **Dependency**: Requires a running instance of Paperless-ngx and an LLM provider (local or cloud).
- **VRAM Requirements**: Running high-quality local models (like Llama 4 Maverick) requires significant GPU resources.

## When to use it
- If you have a high volume of documents in Paperless-ngx that need organization.
- When you want to leverage local AI for document management without data leaving your server.
- If your documents vary wildly in format, making standard matching rules ineffective.

## When not to use it
- If your document organization needs are already well-handled by Paperless-ngx's native matching algorithms.
- If you have very limited CPU/GPU resources and cannot use cloud APIs.
- For extremely sensitive documents where even local AI processing is restricted by policy.

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

## AI Provider Configuration (June 2026)
Paperless-AI supports multiple AI backends. For maximum privacy, a local setup is recommended, while cloud providers offer the highest extraction accuracy.

| Provider | Note |
| :--- | :--- |
| **Ollama** | Best for home use. Supports Llama 4 Maverick and specialized extraction models. |
| **Claude 4.8 Opus** | Recommended for complex, multi-page financial audits and legal reviews. |
| **GPT-5.5** | High-speed, high-accuracy extraction with native autonomous capabilities. |
| **LM Studio** | Local desktop alternative. Useful for testing different quantization levels. |

## CLI examples
Paperless-AI is primarily a background service and does not offer a standalone CLI for document processing. Management is handled via environment variables and the Paperless-ngx interface.

```bash
# View service logs to monitor extraction progress
docker logs -f paperless-ai

# Restart the service to apply configuration changes
docker restart paperless-ai
```

## API examples
Paperless-AI does not expose a public REST API for external consumers; it acts as a client to the Paperless-ngx API. To interact with processed metadata, use the [Paperless-ngx API](paperless-ngx.md).

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
- [Ollama](ollama.md) — For running local LLMs like Llama 4 or Mistral.
- [n8n](n8n.md) — For advanced post-processing workflows.
- [Claude 4.8 Opus](../tools/ai_knowledge/claude.md) — Flagship Anthropic model for high-fidelity extraction.
- [GPT-5.5](../tools/ai_knowledge/openai.md) — Premier OpenAI model for complex document reasoning.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of running models locally for document processing.
- [Whisper](whisper.md) — For transcribing audio files before intake into Paperless-ngx.
- [Linkwarden](linkwarden.md) — For capturing web content to be archived in Paperless-ngx.
- [Extraction and Classification](../reference-implementations/llm-prompts/extraction-and-classification.md) — General patterns for LLM extraction.

## Sources / references
- [GitHub Repository](https://github.com/clusterfudge/paperless-ai)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Tailscale: AI-enhanced documents with Paperless-ngx](https://tailscale.com/blog/paperless-ngx-local-ai-document-search)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
