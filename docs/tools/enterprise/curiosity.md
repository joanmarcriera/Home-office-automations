# Curiosity

## What it is
Curiosity is a desktop-first AI search application and enterprise knowledge assistant that provides a unified interface for searching across local files, emails, cloud storage, and enterprise applications. Expanding into the **Curiosity Workspace** platform, it offers enterprise features, SSO support (OIDC/SAML2), and integration with local LLMs (via Ollama, vLLM) and multi-model vector indexing powered by FastMCP 3.1 Task Protocols.
- **Licensing**: Proprietary (Freemium)
- **Cost**: Free (Personal) / Paid (Pro & Workspace)
- **Self-hostable**: Desktop app (Local data) / Workspace (On-premise option)

## What problem it solves
It solves the problem of "information fragmentation" where data is scattered across multiple SaaS apps (Slack, Jira, Notion, Confluence, Google Drive, OneDrive) and local folders. Curiosity provides a single "source of truth" for search, combined with an AI assistant that reasons over indexed data locally, ensuring privacy and reducing the need to upload sensitive files to public clouds.

## Where it fits in the stack
**Category**: [Enterprise](../enterprise/index.md) / Enterprise AI & Unified Search. Curiosity acts as a human-facing "Agentic Interface" that bridges the gap between local desktop files and enterprise cloud knowledge repositories.

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
|  | Reasoning Engine (Local Ollama / vLLM OR Cloud Claude / GPT / Gemini Gateway)  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Detailed Search & FastMCP 3.1 Data Flow Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Agent
    participant Launcher as Curiosity Desktop Launcher
    participant HybridSearch as Hybrid Search Engine (BM25 + Vector)
    participant FastMCP as FastMCP 3.1 Search Server
    participant Validator as Pydantic v2 Schema Gate
    participant LocalLLM as Local LLM (Ollama / vLLM)

    User->>Launcher: Type Query (e.g., "@slack 2027 Q1 roadmap")
    Launcher->>HybridSearch: Dispatch Parallel Query (BM25 Keyword + Embedding)
    HybridSearch->>HybridSearch: Execute Reciprocal Rank Fusion (RRF)
    HybridSearch-->>Launcher: Return Ranked Document Nodes
    Launcher->>FastMCP: Dispatch Search Results for Context Assembly
    FastMCP->>Validator: Validate Document Metadata & Source Permissions
    Validator-->>FastMCP: Approved Document Context Payload
    FastMCP->>LocalLLM: Send Structured Context + RAG Prompt
    LocalLLM-->>FastMCP: Stream Generated Answer Synthesis
    FastMCP-->>Launcher: Render Answer + Source Citations in Launcher UI
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

## Key Technical Specifications & Architectural Standards

| Dimension | Standard / Specification | Production Requirement |
| :--- | :--- | :--- |
| **Search Architecture** | Hybrid Reciprocal Rank Fusion (RRF) | Combination of BM25 sparse and HNSW vector dense indexing |
| **Inter-Agent Protocol** | FastMCP 3.1 / Model Context Protocol | JSON-RPC 2.0 transport over Local Pipe or SSE |
| **Authentication** | OIDC / SAML2 / PKCE | Enterprise Single Sign-On with automatic token rotation |
| **Local LLM Integration** | Ollama / vLLM REST Endpoint | Native HTTP API compatibility with OpenAI / Ollama schemas |

## Strengths
- **Privacy-First Architecture**: Most indexing and AI processing (with local LLMs) occur on the user's machine.
- **Native Desktop Experience**: High-performance, keyboard-driven interface with instant "Launcher" access.
- **Extensive Connectors**: Supports 50+ cloud and local sources including Microsoft 365, Google Workspace, GitHub, and Notion.
- **Enterprise Features**: **LLM Usage Dashboard** (cost/token tracking), **Multi-Model Vector Indexing** (run embedding models side-by-side), and **Agentic Questioning** (human-in-the-loop support) utilizing FastMCP 3.1 Task Protocols.
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

## System Configuration & Operational Parameters

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `CURIOSITY_PORT` | `8093` | Network listener port for Curiosity FastMCP 3.1 search bridge. |
| `CURIOSITY_WORKSPACE_URL` | `https://workspace.curiosity.ai` | Target Curiosity Workspace enterprise server URL. |
| `CURIOSITY_OLLAMA_HOST` | `http://localhost:11434` | Endpoint for local Ollama LLM provider. |
| `CURIOSITY_MAX_RESULTS` | `20` | Default maximum document nodes returned per hybrid search query. |

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
4. Choose your preferred model (e.g., `gemma3:8b` or `llama4:scout`) and click **Connect**.

## CLI examples

### 1. FastMCP 3.1 Service Registration & Management
```bash
# Register Curiosity as a FastMCP 3.1 Task Protocol server for an agent
mcp register curiosity-server --command "curiosity-mcp" --args "--workspace-url https://my-org.curiosity.ai"

# Trigger a re-index of a specific source via Workspace CLI
curiosity-cli index trigger --source "google-drive-shared" --workspace "enterprise-docs"
```

### 2. Status Auditing & Launcher Productivity
```bash
# Query the workspace index health
curiosity-cli status --json

# Launcher Shortcuts (Keyboard-first productivity)
# Alt + Space (Win/Linux) or Cmd + Space (Mac): Toggle Launcher.
# / : Start a command or search filter (e.g., /type:pdf src:github).
```

## API examples

### 1. FastMCP 3.1 Tool Server & Pydantic v2 Search Validation
The following FastMCP 3.1 server validates Curiosity Workspace search payloads using Pydantic v2 schemas:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CuriositySearchBridge")

mcp = FastMCP("CuriositySearchBridge")

class CuriosityDocument(BaseModel):
    id: str = Field(..., description="Unique document node ID in Curiosity")
    title: str = Field(..., description="Document title or subject")
    source: str = Field(..., description="Origin source system (e.g., Slack, GitHub, local)")
    score: float = Field(..., description="Relevance score", ge=0.0, le=1.0)
    last_modified: Optional[datetime] = Field(None, description="Last modification timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom document attributes")

    @field_validator("source")
    def validate_source(cls, v: str) -> str:
        valid_sources = {"slack", "github", "google-drive", "notion", "jira", "local-file", "email"}
        if v.lower() not in valid_sources:
            return "custom"
        return v.lower()

class CuriositySearchResult(BaseModel):
    query: str = Field(..., description="Original search string")
    total_hits: int = Field(..., description="Total documents matching query", ge=0)
    documents: List[CuriosityDocument] = Field(default_factory=list, description="Matched document nodes")
    search_duration_ms: float = Field(default=0.0, ge=0.0)

@mcp.tool(description="Perform high-speed hybrid search across Curiosity Workspace index.")
def search_workspace(query: str, max_results: int = 10) -> str:
    """FastMCP 3.1 tool implementation querying Curiosity Workspace."""
    logger.info(f"Executing hybrid search for query: '{query}' (limit {max_results})")

    mock_response = {
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

    validated = CuriositySearchResult.model_validate(mock_response)
    return validated.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### 2. Triggering AI Summary Tasks via REST API
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
    "model_override": "claude-3-7-sonnet"
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())
```

## Production Systemd Service Unit Configuration

To host the Curiosity FastMCP 3.1 search bridge as a persistent system daemon, create `/etc/systemd/system/curiosity-bridge.service`:

```ini
[Unit]
Description=FastMCP 3.1 Curiosity Workspace Search Bridge Service
After=network.target

[Service]
Type=simple
User=curiosity
Group=curiosity
WorkingDirectory=/opt/curiosity-bridge
Environment="PATH=/opt/curiosity-bridge/venv/bin:/usr/local/bin:/usr/bin"
Environment="CURIOSITY_PORT=8093"
Environment="CURIOSITY_WORKSPACE_URL=https://my-org.curiosity.ai"
ExecStart=/opt/curiosity-bridge/venv/bin/python3 -m curiosity_bridge.server
Restart=always
RestartSec=5
LimitNOFILE=65536

# Security Hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and manage the service via systemctl:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now curiosity-bridge.service
sudo systemctl status curiosity-bridge.service
```

## Diagnostic Troubleshooting Matrix

| Symptom / Issue | Primary Cause | Diagnostic Command | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **High System Memory Usage** | Local embedding models and continuous indexing consuming RAM. | `curiosity-cli status --json` | Add exclusion filters for heavy folders (`node_modules`, `.venv`). Restrict local vector model threads. |
| **Local Ollama Disconnect** | Curiosity cannot connect to Ollama endpoint at `http://localhost:11434`. | `curl http://localhost:11434/api/tags` | Ensure `OLLAMA_ORIGINS="*" env` is set and Ollama background daemon is running (`ollama serve`). |
| **FastMCP Tool Timeout** | Workspace API search query took over 10 seconds to return results. | `journalctl -u curiosity-bridge.service -n 50` | Re-index connector sources or reduce `CURIOSITY_MAX_RESULTS` to 10. |
| **SSO Token Expiration** | SAML2/OIDC session expired for enterprise workspace connectors. | `curiosity-cli auth status` | Re-authenticate user session via `curiosity-cli auth login --provider oidc`. |

## Related tools / concepts
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Flexible local RAG management suite.
- [Khoj](../intake_storage/khoj.md) — Open-source personal AI search assistant.
- [Msty](../infrastructure/msty.md) — Desktop-native local LLM workbench.
- [Ollama](../../services/ollama.md) — Primary local model provider for Curiosity.
- [Elasticsearch](elastic.md) — Scalable enterprise search infrastructure.
- [Authentik](../../services/authentik.md) — OIDC/SAML identity provider for Curiosity Workspace.

## Sources / references
- [Curiosity.ai Official Site](https://curiosity.ai/)
- [Curiosity Documentation](https://docs.curiosity.ai/)
- [Curiosity Platform Release Notes](https://knowledge.curiositysoftware.ie/docs/curiosity-platform-release-notes)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
