# Paperless-AI

## What it is
Paperless-AI is an enhancement tool for Paperless-ngx that leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide semantic search and chat capabilities.

## What problem it solves
It moves beyond basic keyword matching in Paperless-ngx, allowing users to ask complex questions about their archived documents (e.g., "What was my total electricity spend in 2024?") and receive natural language answers.

## Where it fits in the pipeline
**Process / Reason**

## Typical use cases (in this homelab / family automation context)
- **Document Q&A**: Asking for specific details inside a long insurance policy or school manual.
- **Semantic Tagging**: Using AI to automatically suggest or apply relevant tags based on content meaning.
- **Summarization**: Getting quick summaries of dense administrative documents.

## Integration points
- **Paperless-ngx**: Connects via API to access the document archive and OCR data.
- **LLMs (OpenAI, Ollama, etc.)**: Connects to external or local models for reasoning and text generation.
- **LiteLLM**: Can be used as a proxy to manage multiple LLM backends.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Enables natural language interaction with your archive.
- RAG-powered, meaning answers are grounded in your actual documents.
- Easy to deploy alongside existing Paperless-ngx instances.

## Limitations
- Quality of answers depends heavily on the chosen LLM.
- Requires significant compute resources if running LLMs locally (e.g., via Ollama).

## Alternatives / Related tools
- **LocalGPT**
- **PrivateGPT**

## Links
- [GitHub](https://github.com/clusterzx/paperless-ai)
