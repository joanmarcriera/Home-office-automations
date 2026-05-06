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
- When you want a visual environment to prototype and deploy LLM applications
- When building RAG or agent applications that connect to local LLM infrastructure

## When not to use it
- When you need fine-grained programmatic control over LLM pipelines
- When the overhead of running another service is not justified for simple tasks

## Getting started

### Installation (Docker Compose)
Dify is best deployed using Docker Compose for self-hosting.

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
```

### Accessing the Dashboard
Once the containers are running, navigate to `http://localhost/install` in your browser to complete the initial setup and create your admin account.

## CLI examples

### 1. Start Dify Infrastructure
```bash
docker compose up -d
```

### 2. View Service Logs
```bash
docker compose logs -f api
```

### 3. Database Migration (Maintenance)
```bash
docker exec -it dify-api-1 flask db upgrade
```

## API examples

### Calling a Dify Chat Application (Python)
Dify provides an official Python SDK for interacting with your deployed applications.

```bash
pip install dify-client
```

```python
from dify_client import ChatClient

# Initialize the ChatClient with your App's API Key
client = ChatClient(api_key="app-xxxxxxxxxxxxxx")

# Create a chat message
response = client.create_chat_message(
    inputs={},
    query="How can I optimize my local RAG pipeline?",
    user="user_123",
    response_mode="blocking"
)

print(response.json())
```

## Related tools / concepts
- [Flowise](flowise.md)
- [LangChain](langchain.md)
- [LlamaIndex](llamaindex.md)
- [Langflow](../frameworks/langflow.md)
- [AnythingLLM](anythingllm.md)
- [Ollama](../../services/ollama.md)

## Sources / references
- [Official Website](https://dify.ai/)
- [GitHub Repository](https://github.com/langgenius/dify)
- [Dify Documentation](https://docs.dify.ai/)

## Contribution Metadata

- Last reviewed: 2026-05-28
- Confidence: high
