# Open WebUI

## What it is
Open WebUI is a user-friendly WebUI for Large Language Models (LLMs), designed to provide a feature-rich, self-hosted chat interface.

## What problem it solves
It provides a polished, ChatGPT-like interface for local LLMs (via Ollama) and external APIs, making them accessible to non-technical users. It adds features like RAG, multi-user support, and image generation that basic CLIs lack.

## Where it fits in the stack
**User Interface / Frontend**. It sits on top of inference engines like Ollama or LiteLLM to provide the chat experience.

## Typical use cases
- **Self-Hosted AI Chat**: A private alternative to ChatGPT for family or organization use.
- **Local RAG**: Uploading documents to chat with them using local embeddings and LLMs.
- **Model Comparison**: Chatting with multiple models side-by-side to compare performance.

## Strengths
- **Beautiful UI**: Modern, responsive, and customizable.
- **Local RAG Support**: Built-in support for document ingestion and retrieval.
- **Role-Based Access Control**: Multi-user support with admin controls.
- **Wide Compatibility**: Works with Ollama, OpenAI-compatible APIs, and more.

## Limitations
- **Resource Heavy**: Requires its own resources alongside the inference engine.
- **Setup Complexity**: RAG and advanced features require additional configuration (embeddings, vector stores).

## When to use it
- When you want a professional chat interface for your local models.
- If you need to share access to your LLM server with other people securely.
- For local document-based question answering (RAG).

## When not to use it
- If you prefer a minimal CLI-only workflow.
- If you have extremely limited system resources.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation with Ollama (Docker Compose)
This example shows how to run Open WebUI and link it to an Ollama instance.

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    volumes:
      - ./ollama:/root/.ollama
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    volumes:
      - ./open-webui:/app/backend/data
    depends_on:
      - ollama
    ports:
      - 3000:8080
    environment:
      - 'OLLAMA_BASE_URL=http://ollama:11434'
    restart: unless-stopped
```

## Related tools / concepts
- [Ollama](ollama.md)
- [LiteLLM](litellm.md)
- [RAG (Retrieval Augmented Generation)](../knowledge_base/patterns/rag.md)

## Backlog
- Integrate with internal knowledge base for RAG.

## Sources / References
- [Official Website](https://openwebui.com/)
- [GitHub Repository](https://github.com/open-webui/open-webui)
- [Ollama WebUI GitHub](https://github.com/ollama-webui/ollama-webui)

## Contribution Metadata
- Last reviewed: 2026-03-08
- Confidence: high
