# Joplin

## What it is
Joplin is a free, open-source note-taking and to-do application capable of managing structured notes across extensive notebook hierarchies. As of early January 2027, Joplin v3.2 remains a foundational component for privacy-focused KnowledgeOps, offering native End-to-End Encryption (E2EE), SQLite storage backends, and a local REST API integrated with FastMCP 3.1 protocol servers for multi-agent retrieval.

## What problem it solves
It provides a private, open platform to synchronize structured knowledge across devices via self-hosted backends (Nextcloud, WebDAV, S3). It resolves privacy and data lock-in issues inherent in proprietary note systems while enabling local AI agents (powered by Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, and Qwen 3.8) to perform secure semantic searches and note mutations over local encrypted vaults.

## Where it fits in the stack
**AI & Knowledge / Note Taking**. It serves as a privacy-focused knowledge management and note-taking tool that integrates into the homelab automation stack via its REST API and web clipper, and connects to the Model Context Protocol (MCP 3.1) layer.

## Typical use cases
- **Personal Knowledge Management**: Organizing personal and professional notes in a structured notebook format.
- **Web Research**: Capturing web pages and screenshots using the web clipper extension.
- **Cross-Device Syncing**: Syncing notes across devices with E2EE for maximum privacy.
- **AI Integration**: Using Joplin as a long-term memory or scratchpad for AI agents via the Data API, allowing Llama 4 and Gemini 3.5 to process local markdown entries.

## Strengths
- **Privacy**: Strong E2EE and support for various sync targets (including self-hosted).
- **Format**: Notes are stored in Markdown format, ensuring long-term accessibility.
- **Extensibility**: Support for plugins, themes, and a powerful Data API.
- **Web Clipper**: Powerful extension for capturing online content directly into notes.

## Limitations
- **Sync Conflict Resolution**: Can sometimes be less intuitive than cloud-native alternatives like Notion.
- **UI**: While functional and improved in late 2026, the UI may feel less "fluid" to some users compared to proprietary tools.
- **Real-time Collaboration**: Lacks the seamless real-time multi-user editing found in web-first platforms.

## When to use it
- When you need a cross-platform, open-source note-taking app with strong privacy features.
- When you want to host your own note synchronization (e.g., using Nextcloud or WebDAV).
- When you need a note-taking tool that is highly scriptable via an API.

## When not to use it
- When real-time, multi-user collaboration is the primary requirement.
- When you prefer the "canvas" or "block" based approach of tools like Obsidian or Notion.

## Getting started

### Installation
To start using Joplin, download the application for your platform:
1. **Desktop**: Download from the [Official Website](https://joplinapp.org/).
2. **Mobile**: Available on the App Store and Google Play.
3. **CLI**: Install the terminal application via NPM:
   ```bash
   npm install -g joplin
   ```

### Enabling the API
1. Open Joplin Desktop.
2. Go to **Settings > Web Clipper**.
3. Enable the Web Clipper service.
4. Copy the **Authorization token** for use in scripts.

## CLI examples

### Joplin Terminal Application
Joplin offers a full-featured terminal application for console-based workflows.

```bash
# Start the terminal application
joplin

# Use internal commands (inside the joplin console)
:help
:ls
:edit "Project Notes"
:sync
```

### REST API via curl
List all notebooks using curl:
```bash
curl -X GET "http://localhost:41184/folders?token=YOUR_TOKEN"
```

## API examples

### Python Integration (Pydantic v2 Schema)
AI agents can interact with Joplin using the local REST API to store or retrieve knowledge securely:

```python
import urllib.request
import json
from pydantic import BaseModel, Field, field_validator

class JoplinNoteCreate(BaseModel):
    title: str = Field(..., description="Note title.")
    body: str = Field(..., description="Markdown note content.")
    parent_id: str | None = Field(default=None, description="Optional target notebook folder ID.")
    token: str = Field(..., description="Joplin Web Clipper authorization token.")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty.")
        return v.strip()

def create_joplin_note(req: JoplinNoteCreate) -> dict:
    url = f"http://localhost:41184/notes?token={req.token}"
    data = {"title": req.title, "body": req.body}
    if req.parent_id:
        data["parent_id"] = req.parent_id

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))

# Example execution schema
payload = JoplinNoteCreate(
    title="Claude 5.1 & Gemini 4.0 Pro Research Findings",
    body="Substantive analysis of early 2027 SOTA model benchmarks and FastMCP 3.1 integrations.",
    token="your_auth_token_here"
)
# note_res = create_joplin_note(payload)
```

### Web Clipper Service
The Web Clipper is a browser extension that allows you to save web pages directly. It communicates with the same local API used by scripts.

## Related tools / concepts
- [Obsidian](obsidian.md)
- [Logseq](logseq.md)
- [Trilium Notes](../../services/trilium.md)
- [Anytype](../intake_storage/anytype.md)
- [Nextcloud](../../services/nextcloud.md)
- [Khoj](../intake_storage/khoj.md)
- [Notion AI](notion-ai.md)
- [Markdown](../ai_knowledge/logseq.md)
- [E2EE Patterns](../../knowledge_base/patterns/agentic-workflows.md)
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://joplinapp.org/)
- [Joplin Data API Reference](https://joplinapp.org/api/references/rest_api/)
- [Joplin GitHub](https://github.com/laurent22/joplin)
- [Joplin Plugin Marketplace](https://joplinapp.org/plugins/)
- [MCP 3.1 Joplin Server Implementation](https://github.com/joplin/mcp-server)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
