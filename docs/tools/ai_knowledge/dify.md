# Dify

Dify is an open-source LLM application development platform that allows you to visually create and operate AI applications based on various LLMs.

## What it is

Dify is an open-source LLM application development platform. It allows you to visually create and operate AI applications based on various LLMs, and includes tools for prompt engineering, RAG, and agent orchestration. The July 2026 update (v1.2+) includes native support for the [MCP 3.0 Task Protocol](../../architecture/multi_agent_knowledgeops.md) and [FastMCP 3.0](../../architecture/multi_agent_knowledgeops.md) for tool hosting.

## What problem it solves

Lowers the barrier to building LLM-powered applications by providing a visual interface for designing prompts, RAG pipelines, and agent workflows without writing extensive code. It addresses the complexity of managing multiple model providers, vector databases, and application states. It serves as a visual bridge for [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) governance.

## Where it fits in the stack

**AI & Knowledge / Application Orchestration**. Serves as a visual platform for building and deploying LLM applications, typically connecting to local inference engines like [Ollama](../../services/ollama.md) or frontier models like [Gemma 3](local_llms.md).

## Typical use cases

- **Visual RAG Construction**: Building RAG applications with a visual drag-and-drop interface.
- **Agent Orchestration**: Rapid prototyping of complex agent workflows with tool-calling and multi-step reasoning.
- **Prompt IDE**: Collaborative prompt engineering and versioning within a team.
- **Enterprise AI Gateway**: Providing a unified API for internal applications to access multiple LLMs with usage tracking via [Authentik](../../services/authentik.md).

## Strengths

- **Privacy-First**: Open-source and self-hostable, allowing for complete data sovereignty.
- **User Friendly**: Visual interface makes LLM app development accessible to non-developers.
- **Batteries Included**: Comes with built-in support for multiple vector databases ([Milvus](../infrastructure/milvus.md), [Weaviate](../infrastructure/weaviate.md)) and model providers.
- **Scalable**: Supports multi-user organizations and production-grade monitoring.

## Limitations

- **Infrastructure Heavy**: Requires running an additional service stack (Redis, PostgreSQL, Vector DB) with its own resource overhead.
- **Extensibility**: Less flexible than code-first frameworks (like [LangChain](langchain.md)) for highly custom, non-standard orchestration logic.
- **Version Drift**: Rapid development of the core platform can sometimes lead to breaking changes in YAML configurations.

## When to use it

- When you want a visual environment to prototype and deploy LLM applications.
- When building RAG or agent applications that need to connect to local LLM infrastructure.
- In team environments where non-technical stakeholders need to participate in prompt tuning.

## When not to use it

- When you need absolute, fine-grained programmatic control over LLM pipelines (use [PydanticAI](../frameworks/pydantic-ai.md) instead).
- When the overhead of running a full Dify stack is not justified for simple, single-script tasks.

## Getting started

Dify is best deployed using Docker Compose for self-hosting.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/langgenius/dify.git
    cd dify/docker
    ```
2.  **Environment Setup**:
    ```bash
    cp .env.example .env
    ```
3.  **Deploy**:
    ```bash
    docker compose up -d
    ```
4.  **Setup Admin**: Navigate to `http://localhost/install` in your browser to create the admin account and initialize the database.

## CLI examples

Managing the Dify infrastructure via the command line:

```bash
# View the health of all Dify services
docker compose ps

# Access the logs for the main API service
docker compose logs -f api

# Perform a database migration manually (usually automated on startup)
docker exec -it dify-api flask db upgrade
```

## API examples

Interacting with a deployed Dify application using the official Python SDK:

```python
from dify_client import ChatClient

# Initialize the ChatClient with your App's API Key
client = ChatClient(api_key="app-xxxxxxxxxxxxxx")

# Send a message to your agent or RAG application
response = client.create_chat_message(
    inputs={"user_context": "home-office"},
    query="How do I integrate Dify with my local Ollama instance?",
    user="jules_agent",
    response_mode="blocking"
)

# Extract and print the answer
print(f"Dify Response: {response.json().get('answer')}")
```

## Related tools / concepts

- [Flowise](flowise.md) — Alternative visual LLM orchestration.
- [LangChain](langchain.md) — The code-first foundation for many Dify patterns.
- [LlamaIndex](llamaindex.md) — Advanced RAG capabilities often integrated into Dify.
- [Langflow](../frameworks/langflow.md) — Visual interface specifically for LangChain.
- [Ollama](../../services/ollama.md) — Primary local model backend for Dify.
- [n8n](../../services/n8n.md) — General-purpose automation often used to trigger Dify APIs.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — The governance framework Dify integrates with.
- [AnythingLLM](anythingllm.md) — Simpler alternative for personal RAG.
- [Gemma 3](local_llms.md) — Canonical local model for Dify applications.

## Sources / references

- [Dify Official Website](https://dify.ai/)
- [Dify Documentation](https://docs.dify.ai/)
- [Dify GitHub Repository](https://github.com/langgenius/dify)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
