# Curiosity

## What it is
Curiosity is a desktop-first AI search application and enterprise knowledge assistant that provides a unified interface for searching across local files, emails, cloud storage, and enterprise applications. As of early January 2027, it has expanded into the **Curiosity Workspace** platform, offering enhanced enterprise features, SSO support (OIDC/SAML), and deep integration with local LLMs (via Ollama, vLLM) and multi-model vector indexing powered by FastMCP 3.1 Task Protocols.
- **Licensing**: Proprietary (Freemium)
- **Cost**: Free (Personal) / Paid (Pro & Workspace)
- **Self-hostable**: Desktop app (Local data) / Workspace (On-premise option)

## What problem it solves
It solves the problem of "information fragmentation" where data is scattered across multiple SaaS apps (Slack, Jira, Notion, Confluence, Google Drive, OneDrive) and local folders. Curiosity provides a single "source of truth" for search, combined with an AI assistant that reasons over indexed data locally, ensuring privacy and reducing the need to upload sensitive files to public clouds.

## Where it fits in the stack
**Enterprise AI / Personal Productivity / Desktop Search**. It acts as a human-facing "Agentic Interface" that bridges the gap between local files and cloud-based knowledge.

## Architecture & System Flow

```
+-----------------------------------------------------------------------------------+
|                            Curiosity Desktop & Workspace                          |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Global Launcher / UI (Cmd+Space / Alt+Space, Multi-Tab Workspaces)            |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Local Search & Indexing Engine (SQLite / VectorDB / BM25 Hybrid Search)      |  |
|  +-----------------------------------------------------------------------------+  |
|           ||                                 ||                        ||         |
|           \/                                 \/                        \/         |
|  +-----------------------+       +-----------------------+   +-----------------+  |
|  | Local Connectors      |       | Cloud Connectors      |   | FastMCP 3.1     |  |
|  | (Files, Mail, Notes)  |       | (Slack, Jira, M365)   |   | Task Protocol   |  |
|  +-----------------------+       +-----------------------+   +-----------------+  |
|                                                                        ||         |
|                                                                        \/         |
|  +-----------------------------------------------------------------------------+  |
|  | Reasoning Engine (Local Ollama / vLLM OR Cloud Claude 5.6 / GPT-5.6 Gateway)  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Unified Global Search**: Finding a specific email attachment, Slack thread, or Jira ticket using a single global keyboard shortcut.
- **Private Local RAG**: Asking questions about your local PDF library or code documentation using a local model via [Ollama](../../services/ollama.md).
- **Workspace Collaboration**: Grouping related files, notes, and emails into "Spaces" that can be shared across a team with centralized SSO.
- **Agentic Automation**: Utilizing AI agents that can retrieve information, summarize threads, and even "ask" the user for clarification mid-task using FastMCP 3.1.

## Feature Matrix & Comparison

| Feature Capability | Curiosity Workspace | Generic Desktop Search | Cloud RAG Solutions |
| :--- | :--- | :--- | :--- |
| **Local Data Privacy** | Full local index & execution | Full local index | Cloud-stored embeddings |
| **SaaS Connectors** | 50+ native cloud & local integrations | Local disk only | Cloud-first focus |
| **Local LLM Integration** | Native Ollama/vLLM FastMCP 3.1 | None | Cloud API dependent |
| **Agentic Questioning** | Supported via MCP 3.1 Task Protocols | None | Basic webhooks |
| **Enterprise SSO & Audit** | OIDC/SAML2 & Token Usage Dashboard | None | Cloud SSO standard |

## Strengths
- **Privacy-First Architecture**: Most indexing and AI processing (with local LLMs) occur on the user's machine.
- **Native Desktop Experience**: High-performance, keyboard-driven interface with instant "Launcher" access.
- **Extensive Connectors**: Supports 50+ cloud and local sources including Microsoft 365, Google Workspace, GitHub, and Notion.
- **Early 2027 SOTA Features**: **LLM Usage Dashboard** (cost/token tracking), **Multi-Model Vector Indexing** (run embedding models side-by-side), and **Agentic Questioning** (human-in-the-loop support) utilizing FastMCP 3.1 Task Protocols.
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
- **macOS**: DMG or Homebrew Cask (`brew install --cask curiosity`).
- **Windows**: MSI/EXE installer.
- **Linux**: AppImage, DEB, or RPM packages.

### Connecting Local LLM (Ollama)
1. Ensure [Ollama](../../services/ollama.md) is running on your machine (`ollama serve`).
2. In Curiosity, navigate to **Settings > AI Assistant**.
3. Select **Local LLM (Ollama)** as the provider.
4. Choose your preferred model (e.g., `gemma4:27b` or `deepseek-v4:32b`) and click **Connect**.

## CLI examples
Curiosity Workspace includes a CLI for administrative tasks, and it supports the [Model Context Protocol](../../architecture/multi_agent_knowledgeops.md) for agentic integration.

```bash
# Register Curiosity as a FastMCP 3.1 Task Protocol server for an agent
mcp register curiosity-server --command "curiosity-mcp" --args "--workspace-url https://my-org.curiosity.ai"

# Trigger a re-index of a specific source via Workspace CLI
curiosity-cli index trigger --source "google-drive-shared" --workspace "enterprise-docs"

# Query the workspace index health
curiosity-cli status --json

# Launcher Shortcuts (Keyboard-first productivity)
# Alt + Space (Win/Linux) or Cmd + Space (Mac): Toggle Launcher.
# / : Start a command or search filter (e.g., /type:pdf src:github).
```

## API examples
Curiosity Workspace provides a REST API for automated data ingestion and triggering AI tasks using frontier reasoning models like [Claude 5.6](../providers/anthropic.md), GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, and Qwen 3.6 VL.

### FastMCP 3.1 Tool Registration & Pydantic v2 Validation
Using FastMCP 3.1 and Pydantic v2, we validate Curiosity search results before feeding them to downstream frontier agents.

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional, Dict, Any
from datetime import datetime
import requests

# FastMCP 3.1 Server Definition
mcp = FastMCP("CuriositySearchBridge", version="3.1")

class CuriosityDocument(BaseModel):
    id: str = Field(..., description="Unique document node ID in Curiosity")
    title: str = Field(..., description="Document title or subject")
    source: str = Field(..., description="Origin source system (e.g., Slack, GitHub, local)")
    score: float = Field(..., description="Relevance score", ge=0.0, le=1.0)
    last_modified: Optional[datetime] = Field(None, description="Last modification timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom document attributes")

    @field_validator("source")
    @classmethod
    def validate_source(cls, v: str) -> str:
        valid_sources = {"slack", "github", "google-drive", "notion", "jira", "local-file", "email"}
        if v.lower() not in valid_sources:
            return "custom"
        return v.lower()

class CuriositySearchResult(BaseModel):
    query: str = Field(..., description="The original search string")
    total_hits: int = Field(..., description="Total documents matching query", ge=0)
    documents: List[CuriosityDocument] = Field(default_factory=list, description="List of matched documents")
    search_duration_ms: float = Field(default=0.0, ge=0.0)

@mcp.tool(name="search_workspace", description="Perform high-speed hybrid search across Curiosity Workspace index")
def search_workspace(query: str, max_results: int = 10) -> Dict[str, Any]:
    """FastMCP 3.1 tool implementation querying Curiosity Workspace."""
    api_token = "MOCK_WORKSPACE_TOKEN"
    api_url = "https://your-workspace.curiosity.ai/api/v1/search"

    raw_response = {
        "query": query,
        "total_hits": 1,
        "documents": [
            {
                "id": "slack-thread-12345",
                "title": "2027 Q1 Roadmap Planning",
                "source": "slack",
                "score": 0.99,
                "last_modified": "2027-01-07T14:30:00Z",
                "metadata": {"channel": "#engineering", "author": "alex"}
            }
        ],
        "search_duration_ms": 14.2
    }

    try:
        validated = CuriositySearchResult.model_validate(raw_response)
        return validated.model_dump(mode="json")
    except ValidationError as e:
        return {"error": f"Validation failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
```

### Triggering Agentic Tasks via API
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
    "model_override": "claude-5-6-sonnet"
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())
```

## Operational Best Practices & Troubleshooting

### Memory & Index Optimization
- **Exclusion Filters**: Exclude large binary folders (e.g., `node_modules`, `.venv`, build targets) in Curiosity Settings > Exclusions to reduce CPU usage.
- **Vector Model Allocation**: When utilizing multi-model vector indexing, restrict local embedding tasks to GPU-accelerated devices or allocate dedicated VRAM.
- **SSO Re-authentication**: OIDC tokens refresh automatically, but SAML session state should be verified every 30 days in enterprise deployments.

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
- [Curiosity Platform Release Notes](https://knowledge.curiositysoftware.ie/docs/curiosity-platform-release-notes)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
