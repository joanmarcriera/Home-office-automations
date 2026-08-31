# Curiosity

## What it is
Curiosity is a desktop-first AI search application and knowledge assistant that provides a unified interface for searching across local files, emails, and cloud storage. As of early January 2027, it has expanded into the **Curiosity Workspace** platform, offering enhanced enterprise features, SSO support (OIDC/SAML), FastMCP 3.1 Task Protocol integrations, and deep support for local LLMs (via Ollama) and multi-model vector indexing.
- **Licensing**: Proprietary (Freemium)
- **Cost**: Free (Personal) / Paid (Pro & Workspace)
- **Self-hostable**: Desktop app (Local data) / Workspace (On-premise option)

## What problem it solves
It solves the problem of "information fragmentation" where data is scattered across multiple SaaS apps (Slack, Jira, Notion) and local folders. Curiosity provides a single "source of truth" for search, combined with an AI assistant that reasons over indexed data locally, ensuring privacy and reducing the need to upload sensitive files to public clouds.

## Where it fits in the stack
**Enterprise AI / Personal Productivity / Desktop Search**. It acts as a human-facing "Agentic Interface" that bridges the gap between local files and cloud-based knowledge.

## Typical use cases
- **Unified Global Search**: Finding a specific email attachment, Slack thread, or Jira ticket using a single global keyboard shortcut.
- **Private Local RAG**: Asking questions about your local PDF library or code documentation using a local model via [Ollama](../../services/ollama.md).
- **Workspace Collaboration**: Grouping related files, notes, and emails into "Spaces" that can be shared across a team with centralized SSO.
- **Agentic Automation**: Utilizing AI agents that can retrieve information, summarize threads, and even "ask" the user for clarification mid-task via FastMCP 3.1 Task Protocols.

## Strengths
- **Privacy-First Architecture**: Most indexing and AI processing (with local LLMs) occur on the user's machine.
- **Native Desktop Experience**: High-performance, keyboard-driven interface with instant "Launcher" access.
- **Extensive Connectors**: Supports 50+ cloud and local sources including Microsoft 365, Google Workspace, GitHub, and Notion.
- **Early 2027 Features**: **LLM Usage Dashboard** (cost/token tracking), **Multi-Model Vector Indexing** (run embedding models side-by-side), and **Agentic Questioning** (human-in-the-loop support) utilizing FastMCP 3.1.
- **Advanced Filtering**: Robust inline filters (e.g., `@file`, `ext:`, `src:`) for precision search.

## Limitations
- **Closed Source**: The core application and Workspace server are proprietary.
- **Resource Intensity**: Indexing large datasets and running local LLMs can significantly impact system CPU and RAM.
- **Desktop Focus**: While a web version exists for Workspace, the primary power and local indexing require the desktop agent.

## When to use it
- If you value privacy and want to search local files alongside cloud data without centralized storage.
- If you find yourself constantly switching between browser tabs and local folders to find project info.
- If you want a desktop-native AI assistant that "knows" your work history across multiple apps.

## When not to use it
- If you strictly require 100% open-source software (consider [Khoj](../intake_storage/khoj.md)).
- If you prefer a pure web-based experience and do not want to install a local agent.
- For high-performance, cluster-wide enterprise search where a dedicated engine like [Elasticsearch](elastic.md) is required.

## Getting started

### Installation
Download the installer for your platform from [curiosity.ai](https://curiosity.ai/).
- **macOS**: DMG or Homebrew Cask.
- **Windows**: MSI/EXE.
- **Linux**: AppImage, DEB, or RPM.

### Connecting Local LLM (Ollama)
1. Ensure [Ollama](../../services/ollama.md) is running on your machine.
2. In Curiosity, navigate to **Settings > AI Assistant**.
3. Select **Local LLM (Ollama)** as the provider.
4. Choose your preferred model (e.g., `gemma4:31b` or `qwen3.6-instruct`) and click **Connect**.

## CLI examples
Curiosity Workspace includes a CLI for administrative tasks, and it supports the FastMCP 3.1 Task Protocol for agentic integration.

```bash
# Register Curiosity as a FastMCP 3.1 server for an agent (January 2027)
mcp register curiosity-server --command "curiosity-mcp" --args "--workspace-url https://my-org.curiosity.ai"

# Trigger a re-index of a specific source via Workspace CLI
curiosity-cli index trigger --source "google-drive-shared" --workspace "enterprise-docs"

# Launcher Shortcuts (Keyboard-first productivity)
# Alt + Space (Win/Linux) or Cmd + Space (Mac): Toggle Launcher.
# / : Start a command or search filter (e.g., /type:pdf).
```

## API examples
Curiosity Workspace provides a REST API for automated data ingestion and triggering AI tasks using frontier models like [Gemma 4](local_llms.md), [Claude 5.6](../providers/anthropic.md), GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL.

### Schema Validation & Search Integration (Python & Pydantic v2)
Using FastMCP 3.1 and Pydantic v2, we validate Curiosity search results before feeding them to downstream frontier agents.

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import datetime
import requests

class CuriosityDocument(BaseModel):
    id: str = Field(..., description="Unique document node ID in Curiosity")
    title: str = Field(..., description="Document title or subject")
    source: str = Field(..., description="Origin source system (e.g., Slack, GitHub, local)")
    score: float = Field(..., description="Relevance score", ge=0.0)
    last_modified: Optional[datetime] = Field(None, description="Last modification timestamp")

class CuriositySearchResult(BaseModel):
    query: str = Field(..., description="The original search string")
    total_hits: int = Field(..., description="Total documents matching query", ge=0)
    documents: List[CuriosityDocument] = Field(default_factory=list, description="List of matched documents")

# Example validation of API response payload
def fetch_and_validate_curiosity_search(query: str, api_token: str) -> Optional[CuriositySearchResult]:
    api_url = "https://your-workspace.curiosity.ai/api/v1/search"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    params = {"q": query}

    try:
        # Simulated structure following early January 2027 FastMCP 3.1 specs
        response_data = {
            "query": query,
            "total_hits": 1,
            "documents": [
                {
                    "id": "slack-thread-12345",
                    "title": "2027 Q1 Roadmap Planning",
                    "source": "Slack",
                    "score": 0.98,
                    "last_modified": "2027-01-07T14:30:00Z"
                }
            ]
        }

        # Strict Pydantic v2 validation
        validated_data = CuriositySearchResult.model_validate(response_data)
        return validated_data
    except ValidationError as e:
        print(f"Curiosity response validation failed: {e.errors()}")
        return None

# Execute search validation
api_token = "MOCK_WORKSPACE_TOKEN"
result = fetch_and_validate_curiosity_search("roadmap 2027", api_token)
if result:
    print(f"Validated query '{result.query}': Found {result.total_hits} secure hits.")
```

### Triggering AI Tasks (Python)
```python
import requests

API_TOKEN = "YOUR_WORKSPACE_TOKEN"
API_URL = "https://your-workspace.curiosity.ai/api/v1/tasks/summarize"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "node_id": "slack-thread-12345",
    "prompt_template": "Executive Summary",
    "model_override": "gemma4-31b-it"
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())
```

### Searching the Knowledge Base
```bash
# Search for specific documents via API
curl -X GET "https://your-workspace.curiosity.ai/api/v1/search?q=roadmap+2027" \
     -H "Authorization: Bearer <API_TOKEN>"
```

## Related tools / concepts
- [AnythingLLM](../ai_knowledge/anythingllm.md) — For flexible local RAG management.
- [Khoj](../intake_storage/khoj.md) — Open-source personal AI search.
- [Msty](../infrastructure/msty.md) — Desktop-native local LLM interface.
- [Ollama](../../services/ollama.md) — Primary local model provider for Curiosity.
- [Elasticsearch](elastic.md) — For large-scale enterprise search infrastructure.
- [Authentik](../../services/authentik.md) — For OIDC/SAML integration with Curiosity Workspace.
- [MCP Registry](../../architecture/multi_agent_knowledgeops.md) — For extending agentic context.

## Sources / References
- [Curiosity.ai Official Site](https://curiosity.ai/)
- [Curiosity Documentation](https://docs.curiosity.ai/)
- [Curiosity Blog: January 2027 Release Overview](https://blog.curiosity.ai/blog/release-overview-january-2027)
- [Curiosity Platform Release Notes](https://knowledge.curiositysoftware.ie/docs/curiosity-platform-release-notes)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
