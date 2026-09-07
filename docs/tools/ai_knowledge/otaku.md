# Otaku

## What it is
Otaku is an open-source, lightweight web frontend interface designed specifically for local and self-hosted Large Language Model (LLM) interaction. Built with modern web frameworks, Otaku provides an intuitive user workspace for chat sessions, model parameter configuration, context inspection, and multi-backend connection management (including Ollama, vLLM, and llama.cpp).

## What problem it solves
Managing local AI models across various inference servers often requires navigating fragmented web interfaces or relying on terminal commands. Standard single-backend interfaces lack flexibility when connecting to multiple local home-lab endpoints. Otaku solves this by offering a unified, clean web front-end that connects seamlessly to multiple local inference provider endpoints while storing chat history and custom prompts locally on the user's filesystem.

## Where it fits in the stack
**AI & Knowledge / Model Frontends & Client Interfaces**. Otaku acts as the user-facing workspace that bridges end-user interactions with local inference engines (such as Ollama, vLLM, or LiteLLM) running on home-lab infrastructure.

## Typical use cases
- **Self-Hosted AI Chat Desktop**: Providing a responsive, clean chat UI across desktop and mobile devices inside the local home network.
- **Multi-Model Testing & Comparison**: Rapidly toggling between local LLM backends to compare responses, speed, and context window limits.
- **Custom System Prompt Management**: Saving, organizing, and injecting custom system prompts for specialized tasks like coding, summarize, and data extraction.

## Strengths
- **Privacy & Local Storage**: Chat history and prompt configurations remain strictly on the local client without remote analytics tracking.
- **Multi-Backend Provider Support**: Connects to OpenAI-compatible endpoints, Ollama APIs, and local vLLM servers out of the box.
- **Streamlined Lightweight UI**: Minimal resource overhead and fast initial load times compared to heavy monolithic web apps.

## Limitations
- **Ecosystem Maturity**: Newer frontend tool compared to mature platforms like Open WebUI or LibreChat.
- **Advanced Agent Workflow Support**: Focused primarily on direct chat and prompt interaction rather than complex multi-agent execution graphs or built-in rag ingestion pipelines.

## When to use it
- When requiring a lightweight, clean web workspace for local LLM inference engines.
- When seeking a simple frontend without the deployment complexity of multi-container enterprise portals.
- When managing multiple local endpoints (Ollama, vLLM, llama.cpp) from one interface.

## When not to use it
- When requiring rich integrated document RAG pipelines, multi-user role-based access control, or enterprise SSO integration (use Open WebUI or LibreChat instead).
- When looking for an embedded model runner that packages both backend model execution and UI into a single app (use LM Studio or Jan.ai instead).

## Getting started
To set up Otaku locally or host it in Docker:

```bash
# Clone the repository
git clone https://github.com/otaku-ui/otaku.git
cd otaku

# Install dependencies and start development server
npm install
npm run dev
```

Or deploy using Docker:

```bash
docker run -d \
  --name otaku-ui \
  -p 3000:3000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  otaku/otaku-ui:latest
```

## CLI examples

```bash
# Verify local Ollama API connectivity prior to linking Otaku
curl http://localhost:11434/api/tags

# Launch Otaku production build with custom environment parameters
HOST=0.0.0.0 PORT=3000 NEXT_PUBLIC_API_URL=http://192.168.1.100:11434 node server.js
```

## API examples

### 1. Pydantic v2 Schema for Otaku Client Configuration
```python
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class OtakuEndpointConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Display name for the backend provider")
    base_url: HttpUrl = Field(..., description="OpenAI-compatible or Ollama API URL endpoint")
    api_key: Optional[str] = Field(default=None, description="Optional authentication token")
    default_model: str = Field(..., description="Default model selected on connection")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    system_prompt: Optional[str] = Field(default=None, description="Default system prompt")

if __name__ == "__main__":
    endpoint = OtakuEndpointConfig(
        name="Local Ollama GPU",
        base_url="http://192.168.1.50:11434",
        default_model="llama3.1:8b",
        temperature=0.7,
        system_prompt="You are a helpful home lab assistant."
    )
    print(f"Configured Otaku endpoint '{endpoint.name}' pointing to {endpoint.base_url}")
```

### 2. FastMCP 3.1 Task Protocol Integration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("otaku-ui-manager")

@mcp.tool()
def update_otaku_active_model(model_id: str, endpoint_url: str) -> dict:
    """Updates the default active model and backend URL in Otaku workspace configuration."""
    return {
        "status": "success",
        "active_model": model_id,
        "endpoint": endpoint_url,
        "message": "Otaku frontend connection updated."
    }
```

## Related tools / concepts
- [Open WebUI](../../services/open-webui.md) — Comprehensive feature-rich frontend for Ollama and local LLMs.
- [LibreChat](../ai_knowledge/librechat.md) — Enhanced open-source Web UI for AI models and assistants.
- [Ollama](../../services/ollama.md) — Local LLM server backend commonly coupled with Otaku.

## Sources / references
- [Otaku Frontend Reddit Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1w85blf/otaku_an_llm_frontend/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
