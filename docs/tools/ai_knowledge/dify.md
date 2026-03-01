# Dify

## What it is
Dify is an open-source LLM application development platform. It allows you to visually create and operate AI applications based on various LLMs, and includes tools for prompt engineering, RAG, and agent orchestration.

## What problem it solves
Lowers the barrier to building LLM-powered applications by providing a visual interface for designing prompts, RAG pipelines, and agent workflows without writing extensive code.

## Where it fits in the stack
AI & Knowledge — serves as a visual platform for building and deploying LLM applications, potentially connecting to the local Ollama instance.

## Typical use cases
- Building RAG applications with a visual drag-and-drop interface
- Rapid prototyping of prompt chains and agent workflows
- Setting up local RAG pipelines with Ollama and private data

## Strengths
- Open-source and self-hostable, aligning with the privacy-first approach
- Visual interface makes LLM app development accessible to non-developers
- Supports multiple LLM backends including local models via Ollama

## Limitations
- Requires running an additional service with its own dependencies
- Less flexible than code-first frameworks for highly custom workflows
- Smaller community and ecosystem compared to LangChain

## When to use it
- When you want to visually prototype and deploy LLM applications without writing code
- When building RAG or agent applications that connect to local LLM infrastructure

## When not to use it
- When you need fine-grained programmatic control over LLM pipelines
- When the overhead of running another service is not justified for simple tasks

## Related tools / concepts
- [Flowise](flowise.md)
- [LangFlow](https://github.com/langflow-ai/langflow)

## Getting started

Dify is typically deployed via Docker. Once running, you can access its features through the web UI or via its REST API. To use the API, you first need to create an application in the Dify dashboard and generate an API Key.

Minimal Python client example:

```bash
pip install dify-client
```

```python
from dify_client import ChatClient

client = ChatClient(api_key="your-api-key")
response = client.create_chat_message(inputs={}, query="Hello Dify!", user="jules")
```

## API examples

### Calling a Dify Workflow API

Workflows in Dify can be triggered via a POST request.

```bash
curl -X POST 'https://api.dify.ai/v1/workflows/run' \
--header 'Authorization: Bearer {YOUR_API_KEY}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {
        "query": "What are the benefits of self-hosting LLMs?"
    },
    "response_mode": "blocking",
    "user": "unique_user_id_123"
}'
```

## Sources / references
- [Official Website](https://dify.ai/)
- [GitHub Repository](https://github.com/langgenius/dify)

## Contribution Metadata

- Last reviewed: 2026-03-01
- Confidence: medium
