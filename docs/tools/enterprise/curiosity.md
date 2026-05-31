# Curiosity

Curiosity is a desktop-first AI search application and knowledge assistant that provides a unified interface for searching across local files, emails, and cloud storage. As of May 2026, it has expanded into the **Curiosity Workspace** platform, offering enhanced enterprise features, SSO support, and deeper integration with local LLMs (via Ollama) for privacy-conscious AI chat.

## What it is
Curiosity is a "Command+Space" (macOS) or "Alt+Space" (Windows/Linux) replacement designed for information retrieval. It indexes data locally on your machine, allowing for fast, private, and powerful search across diverse sources like Slack, Google Drive, Dropbox, Gmail, and your local filesystem.

## What problem it solves
It solves the problem of "information fragmentation" where data is scattered across multiple SaaS apps and local folders. Curiosity provides a single "source of truth" for search, combined with an AI assistant that can reason over the indexed data without the user having to upload sensitive files to a public cloud.

## Where it fits in the stack
- **Category**: [Enterprise AI](../enterprise/index.md) / Personal Productivity
- **Layer**: [Productivity & Operations Layer](../../architecture/README.md) (Human-facing client)

## Typical use cases
- **Unified Global Search**: Finding a specific email attachment or a Slack thread from six months ago using a single shortcut.
- **Local RAG (Chat with Files)**: Asking questions about your local PDF library or code documentation using a local LLM.
- **Workspace Spaces**: Grouping related files, notes, and emails into project-specific "Spaces" for better context management.
- **AI-Powered Summarization**: Instantly summarizing long document threads or drafting email replies based on project history.

## Strengths
- **Privacy-First Architecture**: Indexing and most AI processing happen on the local machine.
- **Native Desktop Integration**: High-performance, keyboard-driven interface that feels like a natural part of the OS.
- **Extensive Connectors**: Supports 50+ cloud and local data sources (Microsoft 365, Google Workspace, Jira, GitHub, Notion, etc.).
- **Ollama Support**: Can connect to local [Ollama](../../services/ollama.md) instances to power its AI assistant.
- **SSO & Workspace**: New in May 2026, Curiosity Workspace supports enterprise SSO (OIDC/SAML) for cloud and on-premise deployments.

## Limitations
- **Closed Source**: The application itself is proprietary.
- **Resource Intensive**: Indexing large numbers of files and running local LLMs can significantly impact CPU and RAM usage.
- **Desktop Primary**: While a Workspace web version exists, the core power comes from the desktop agent's local indexing.

## When to use it
- If you value privacy and want to search your local files alongside your cloud data.
- If you find yourself constantly switching between browser tabs and local folders to find information.
- If you want a desktop-native AI assistant that "knows" your work history.

## When not to use it
- If you strictly require 100% open-source software (see [Khoj](../intake_storage/khoj.md)).
- If you prefer a pure web-based experience and do not want to install a local agent.
- For high-performance cluster-wide search (see [Elasticsearch](elastic.md)).

## Licensing and cost
- **Open Source**: No.
- **Cost**: Freemium. Personal Pro and Workspace (Enterprise) tiers available.
- **Self-hostable**: Desktop app (Local data) / Workspace (On-premise option).

## Getting started

### Installation
Download the installer for your platform from [curiosity.ai](https://curiosity.ai/).
- **macOS**: DMG or Homebrew (if available via community cask).
- **Windows**: MSI/EXE.
- **Linux**: AppImage or DEB/RPM.

### Connecting Local LLM (Ollama)
1. Ensure [Ollama](../../services/ollama.md) is running on your machine.
2. In Curiosity, go to **Settings > AI Assistant**.
3. Select **Local LLM (Ollama)** as the provider.
4. Choose your preferred model (e.g., `llama3:8b`, `mistral`).

## CLI & Keyboard Shortcuts
Curiosity is primarily GUI-driven, but emphasizes keyboard speed:
- `Alt + Space` (Win/Linux) or `Cmd + Space` (Mac): Toggle Curiosity Launcher.
- `Cmd + K`: Open Command Palette within the app.
- `/`: Start a command or search filter (e.g., `/type:pdf`).

### Search Filter Examples
```text
# Find documents modified this week
modified:this-week

# Search only within a specific Space
space:"Project Alpha"

# Find emails from a specific person with an attachment
from:john has:attachment
```

## Related tools / concepts
- [AnythingLLM](../ai_knowledge/anythingllm.md) — For flexible local RAG management.
- [Khoj](../intake_storage/khoj.md) — Open-source personal AI search.
- [Msty](../infrastructure/msty.md) — Desktop-native local LLM interface.
- [Elasticsearch](elastic.md) — For large-scale enterprise search infrastructure.
- [OIDC Authentication](../../services/authentik.md) — Supported in Curiosity Workspace.

## Links
- [Official Website](https://curiosity.ai/)
- [Curiosity Documentation](https://docs.curiosity.ai/)
- [Release Notes](https://knowledge.curiositysoftware.ie/docs/curiosity-platform-release-notes)

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-31

## Sources / References
- https://knowledge.curiositysoftware.ie/docs/curiosity-platform-release-notes
- https://docs.curiosity.ai/app/features/
- https://karthikeyanrathinam.medium.com/no-internet-no-problem-create-your-own-ai-assistant-with-local-llm-20-frameworks-2026-75aea74d024f
- KnowledgeOps Triage (2026-05-31)
