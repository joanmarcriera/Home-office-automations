# Dify

Dify is an open-source LLM application development platform that allows you to visually create and operate AI applications based on various LLMs.

## What it is

Dify is an open-source LLM application development platform. As of early **January 2027 (v1.4)**, it enables teams to visually build, evaluate, and operate complex agentic applications, multi-agent networks, and advanced visual RAG 2.0 pipelines. It provides a full-stack experience from model management and Model Context Protocol (MCP 3.1 / FastMCP 3.1) integration to production monitoring and deployment.

## What problem it solves

Lowers the barrier to building LLM-powered applications by providing a visual interface for designing prompts, RAG pipelines, and agent workflows without writing extensive code. It addresses the complexity of managing multiple model providers, vector databases, and application states.

## Where it fits in the stack

**AI & Knowledge / Application Orchestration**. Serves as a visual platform for building and deploying LLM applications, typically connecting to local inference engines like [Ollama](../../services/ollama.md) or frontier models like [Claude 5.6](../ai_knowledge/claude.md) and GPT-5.6.

## Typical use cases

- **Visual RAG 2.0 Construction**: Building multi-stage hybrid RAG applications with a visual drag-and-drop interface.
- **Agent Orchestration**: Rapid prototyping of complex agent workflows with FastMCP 3.1 tool-calling and multi-step reasoning.
- **Prompt IDE**: Collaborative prompt engineering and versioning within a team.
- **Enterprise AI Gateway**: Providing a unified API for internal applications to access multiple LLMs with usage tracking and fine-grained permissions.
- **MCP Tool Integration**: Connecting [Model Context Protocol (MCP 3.1)](../../tools/automation_orchestration/mcp.md) servers to provide agents with real-world tools.

## Strengths

- **Privacy-First**: Open-source and self-hostable, allowing for complete data sovereignty.
- **User Friendly**: Visual interface makes LLM app development accessible to non-developers.
- **Batteries Included**: Comes with built-in support for multiple vector databases ([Pinecone](../infrastructure/pinecone.md), [Weaviate](../infrastructure/weaviate.md), [Milvus](../infrastructure/milvus.md), Chroma) and model providers.
- **Scalable**: Supports multi-user organizations and production-grade monitoring.

## Limitations

- **Infrastructure Heavy**: Requires running an additional service stack (Redis, PostgreSQL, Vector DB) with its own resource overhead.
- **Extensibility**: Less flexible than code-first frameworks (like [LangChain](../ai_knowledge/langchain.md)) for highly custom, non-standard orchestration logic.
- **Version Drift**: Rapid development of the core platform can sometimes lead to breaking changes in YAML configurations.

## When to use it

- When you want a visual environment to prototype and deploy LLM applications.
- When building RAG or agent applications that need to connect to local LLM infrastructure.
- In team environments where non-technical stakeholders need to participate in prompt tuning.

## When not to use it

- When you need absolute, fine-grained programmatic control over LLM pipelines.
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

### Python (Dify App Input and Workflow Schema Validation)
Use **Pydantic v2** to enforce strict data contracts on Dify node variables and user context before dispatching chat payloads to the Dify HTTP API:

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

class DifyAppInput(BaseModel):
    user_context: str = Field(..., description="Homelab environment or workspace identifier")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Key-value pairs representing node variables")
    max_steps: int = Field(50, gt=0, le=100)

    @field_validator("user_context")
    @classmethod
    def validate_workspace(cls, v: str) -> str:
        allowed = ["home-office", "production-server", "staging-cluster"]
        if v not in allowed:
            raise ValueError(f"user_context must be one of {allowed}")
        return v

class DifyChatPayload(BaseModel):
    query: str = Field(..., min_length=1, description="Message string to send to Dify agent")
    user: str = Field(..., description="Unique ID of the end-user")
    inputs: DifyAppInput = Field(..., description="Structured variables matching Dify workspace schemas")
    response_mode: str = Field("blocking", pattern="^(blocking|streaming)$")

# Example construction of safe Dify request payload
payload_data = {
    "query": "How do I integrate Dify with my local Ollama instance?",
    "user": "jules_agent",
    "inputs": {
        "user_context": "home-office",
        "variables": {"model_backend": "gemma-3-9b", "temperature": 0.1}
    },
    "response_mode": "blocking"
}

validated_payload = DifyChatPayload.model_validate(payload_data)
# Convert to dictionary ready for requests.post() payload
request_body = validated_payload.model_dump()
print(f"Validated payload prepared for user: {request_body['user']}")
```

## Related tools / concepts

- [Flowise](../ai_knowledge/flowise.md) — Alternative visual LLM orchestration.
- [LangChain](../ai_knowledge/langchain.md) — The code-first foundation for many Dify patterns.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Advanced RAG capabilities often integrated into Dify.
- [Langflow](../frameworks/langflow.md) — Visual interface specifically for LangChain.
- [Ollama](../../services/ollama.md) — Primary local model backend for Dify.
- [n8n](../../services/n8n.md) — General-purpose automation often used to trigger Dify APIs.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Emerging standard for tool discovery in agentic platforms.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Simpler alternative for personal RAG.
- [Gemma 3](../ai_knowledge/local_llms.md) — Recommended local model for Dify-hosted agents.

## Sources / references

- [Dify Official Website](https://dify.ai/)
- [Dify Documentation](https://docs.dify.ai/)
- [Dify GitHub Repository](https://github.com/langgenius/dify)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
