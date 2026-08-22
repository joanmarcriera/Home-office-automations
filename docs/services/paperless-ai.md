# Paperless-AI

Paperless-AI is a companion tool for Paperless-ngx that uses Artificial Intelligence to automate document tagging, correspondent detection, and metadata extraction.

## What it is
Paperless-AI is a specialized automation layer designed to enhance [Paperless-ngx](paperless-ngx.md). It leverages Large Language Models (LLMs) to analyze document content semantically, providing a level of organization and insight that traditional rule-based systems cannot achieve. As of early January 2027, it features native integration with frontier models including **Claude 5.1 / 5.6**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, **DeepSeek-V4**, **Llama 4**, **Gemma 3**, and **Qwen 3.8** for high-precision extraction and autonomous categorization via the **MCP 3.1 / FastMCP** Task Protocol.

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
- **MCP 3.1 Compliance**: Can be called as a tool by other agents to retrieve or process document metadata.
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

### AI Provider Configuration (Early January 2027)
Paperless-AI supports multiple AI backends. For maximum privacy, a local setup is recommended, while cloud providers offer the highest extraction accuracy.

| Provider | Note |
| :--- | :--- |
| **Ollama** | Best for home use. Supports Gemma 3, Qwen 3.8, DeepSeek-V4, and Llama 4 local extraction models. |
| **Claude 5.1 / 5.6** | Recommended for complex, multi-page financial audits and legal reviews. |
| **GPT-5.5 / 5.6** | High-speed, high-accuracy extraction with native autonomous capabilities. |
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
Paperless-AI does not expose a public REST API for external consumers; it acts as a client to the Paperless-ngx API. It can also be controlled via **MCP 3.1** Task Protocol when enabled. To interact with processed metadata directly, use the [Paperless-ngx API](paperless-ngx.md).

Here is a Python example utilizing **Pydantic v2** validation to define and validate Paperless-AI's structured document extraction schemas:

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class PaperlessAIDocumentModel(BaseModel):
    """
    Pydantic v2 model representing structured AI extraction metadata
    from processed Paperless-ngx documents.
    """
    document_id: int = Field(..., description="Unique Paperless-ngx document ID")
    title: str = Field(..., min_length=1, description="AI-generated or verified document title")
    correspondent: Optional[str] = Field(None, description="Sender, company, or institution")
    tags: List[str] = Field(default_factory=list, description="Extracted category or organizational tags")
    document_date: Optional[date] = Field(None, description="Extracted creation/invoice date")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence rating of extraction")

# Example validation
raw_extraction = {
    "document_id": 412,
    "title": "Acrome Plumbing Service Invoice - Jan 2027",
    "correspondent": "Acrome Plumbing LLC",
    "tags": ["Invoice", "Utilities", "Maintenance"],
    "document_date": "2027-01-07",
    "confidence": 0.98
}

doc = PaperlessAIDocumentModel.model_validate(raw_extraction)
print(f"Validated Document: {doc.title} (Confidence: {doc.confidence * 100}%)")
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — The core document management system.
- [Ollama](ollama.md) — For running local LLMs like Gemma 3 or Llama 4.
- [n8n](n8n.md) — For advanced post-processing workflows.
- [Actual Budget](actual-budget.md) — For matching extracted invoices to transactions.
- [Claude 5.1](../tools/providers/anthropic.md) — Flagship Anthropic model for high-fidelity extraction.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of running models locally.
- [Whisper](whisper.md) — For transcribing audio files before intake.
- [Linkwarden](linkwarden.md) — For capturing web content to be archived.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Standard for agentic tool use.

## Sources / references
- [GitHub Repository](https://github.com/clusterfudge/paperless-ai)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
