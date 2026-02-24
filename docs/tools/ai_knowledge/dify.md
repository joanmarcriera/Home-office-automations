# Dify

## What it is
Dify is an open-source Large Language Model (LLM) application development platform. It combines Backend-as-a-Service with a low-code visual interface for building AI applications.

## What problem it solves
It simplifies the creation of AI agents and RAG pipelines, allowing users to build complex AI-powered workflows without deep programming knowledge.

## Where it fits in the pipeline
**Reason / Orchestrate / Act**

## Typical use cases (in this homelab / family automation context)
- **Custom Home Assistant**: Building a specialized AI that has access to your personal documents (via Paperless-ngx) to answer family questions.
- **Workflow Automation**: Creating an AI agent that monitors specific web sources and generates summarized reports for your homelab logs.
- **RAG Dashboard**: Providing a unified interface for multiple knowledge bases (Nextcloud, Paperless, GitHub).

## Integration points
- **LLM Providers**: Supports OpenAI, Anthropic, Ollama, and many others.
- **API**: Provides a clean REST API to trigger AI applications from Home Assistant or n8n.
- **Knowledge Base**: Built-in support for ingesting PDFs, text, and other documents for RAG.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 / Sustainable Use)
- **Cost**: Free (Self-hosted)
- **Free tier**: Yes (Cloud version has limited free tier).
- **Self-hostable**: Yes

## Strengths
- Very intuitive visual workflow builder.
- Built-in observability and performance monitoring.
- Comprehensive set of tools for managing prompt templates and data.

## Limitations
- Deployment can be complex (multiple Docker containers).
- Significant resource requirements for self-hosting.

## Alternatives / Related tools
- **Flowise**
- **LangChain**
- **n8n** (using AI nodes)

## Links
- [Official Website](https://dify.ai/)
- [GitHub](https://github.com/langgenius/dify)
