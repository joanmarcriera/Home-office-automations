# Paperless-AI

Paperless-AI is a companion tool for Paperless-ngx that uses Artificial Intelligence to automate document tagging, correspondent detection, and metadata extraction.

## What it is
Paperless-AI is a specialized automation layer designed to enhance [Paperless-ngx](paperless-ngx.md). It leverages Large Language Models (LLMs) to analyze document content semantically, providing a level of organization and insight that traditional rule-based systems cannot achieve. As of July 2026, it supports native integration with **Gemma 3**, **Claude 4.8**, and **GPT-5.5** for high-precision extraction and autonomous categorization via the **MCP 3.0 Task Protocol**.

## What problem it solves
It eliminates the tedious manual work of organizing scanned documents. While Paperless-ngx has robust matching algorithms, they are often restricted to literal text matches or regex. Paperless-AI understands the context of a document, allowing it to accurately categorize "that weird invoice from the plumber" even if it doesn't follow a standard template, reducing administrative overhead.

## Where it fits in the stack
**Service Companion / Automation**. It works alongside Paperless-ngx, acting as an intelligent processing layer for newly added documents. It is typically deployed as a Docker container within the same network as the Paperless-ngx instance, often integrated into [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md) for automated bookkeeping.

## Typical use cases
- **Automated Tagging**: Assigning tags like "Invoice", "Medical", or "Contract" based on document content.
- **Correspondent Detection**: Identifying the sender or organization associated with a document.
- **Metadata Extraction**: Pulling specific fields like dates, amounts, or account numbers from documents.
- **Document Q&A**: Using the "Chat" function to query the content of your archive using local or cloud LLMs.
- **Automated Expense Tracking**: Syncing extracted invoice data with [Actual Budget](actual-budget.md).

## Strengths
- **Native Paperless-ngx Integration**: Designed specifically to work with the Paperless-ngx API.
- **Local LLM Support**: Can use [Ollama](ollama.md) or [LM Studio](../tools/infrastructure/lm-studio.md) for completely private document processing.
- **MCP 3.0 Compliance**: Can be called as a tool by other agents to retrieve or process document metadata.
- **Improved Accuracy**: Uses the semantic power of frontier models like [Gemma 3](../tools/ai_knowledge/local_llms.md) instead of fragile regex.
- **Open Source**: MIT Licensed and fully self-hostable.

## Limitations
- **Processing Time**: LLM analysis takes significantly longer than simple matching rules.
- **Dependency**: Requires a running instance of Paperless-ngx and an LLM provider (local or cloud).
- **VRAM Requirements**: Running high-quality local models (like Llama 4 Maverick or Gemma 3 27B) requires significant GPU resources.

## When to use it
- If you have a high volume of documents in Paperless-ngx that need organization.
- When you want to leverage local AI for document management without data leaving your server.
- If your documents vary wildly in format, making standard matching rules ineffective.
- For building an automated [Knowledge Management](../knowledge_base/README.md) system for personal or small business use.

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
AI_MODEL=gemma3:27b
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
      - AI_MODEL=gemma3:27b
    restart: unless-stopped
```

## AI Provider Configuration (July 2026)
Paperless-AI supports multiple AI backends. For maximum privacy, a local setup is recommended, while cloud providers offer the highest extraction accuracy.

| Provider | Note |
| :--- | :--- |
| **Ollama** | Best for home use. Supports Gemma 3 and specialized extraction models. |
| **Claude 4.8** | Recommended for complex, multi-page financial audits and legal reviews. |
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
Paperless-AI does not expose a public REST API for external consumers; it acts as a client to the Paperless-ngx API. It can also be controlled via **MCP 3.0** Task Protocol when enabled. To interact with processed metadata directly, use the [Paperless-ngx API](paperless-ngx.md).

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — The core document management system.
- [Ollama](ollama.md) — For running local LLMs like Gemma 3 or Llama 4.
- [n8n](n8n.md) — For advanced post-processing workflows.
- [Actual Budget](actual-budget.md) — For matching extracted invoices to transactions.
- [Claude 4.8](../tools/providers/anthropic.md) — Flagship Anthropic model for high-fidelity extraction.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of running models locally.
- [Whisper](whisper.md) — For transcribing audio files before intake.
- [Linkwarden](linkwarden.md) — For capturing web content to be archived.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Standard for agentic tool use.

## Sources / references
- [GitHub Repository](https://github.com/clusterfudge/paperless-ai)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
