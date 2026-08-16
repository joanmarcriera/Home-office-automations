# Joplin

## What it is
Joplin is a free, open-source note-taking and to-do application capable of managing structured notes across notebooks. It features native end-to-end encryption (E2EE) and provides a secure Data API allowing frontier models (including Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4) to index, query, and synchronize note graphs via **FastMCP 3.1** protocol servers.

## What problem it solves
It provides a secure, private way to sync notes across multiple devices (desktop, mobile, terminal) using self-hosted or cloud services (Nextcloud, WebDAV, Dropbox). It solves the privacy concerns associated with proprietary, cloud-only platforms while providing a robust REST API for autonomous agents to perform local knowledge lookups, scratchpad storage, and long-term memory operations.

## Where it fits in the stack
**AI & Knowledge / Note Taking**. It serves as a privacy-focused knowledge management and note-taking tool that integrates into the homelab automation stack via its REST API, web clipper, and **FastMCP 3.1** connectors.

## Typical use cases
- **Personal Knowledge Management**: Organizing personal and professional notes in a structured markdown notebook hierarchy.
- **Web Research**: Capturing web pages and screenshots using the web clipper extension.
- **Cross-Device Syncing**: Syncing notes across devices with E2EE for maximum privacy.
- **AI Integration**: Serving as long-term memory or scratchpad storage for AI agents via the Data API and FastMCP 3.1 connectors.

## Strengths
- **Privacy**: Strong E2EE and support for various sync targets (including self-hosted Nextcloud/WebDAV).
- **Format**: Notes are stored in plain Markdown format, ensuring long-term accessibility and AI parsing.
- **Extensibility**: Support for plugins, custom themes, and a powerful local Data REST API.
- **Web Clipper**: Web browser extension for capturing online content directly into notes.

## Limitations
- **Sync Conflict Resolution**: Can sometimes be less intuitive than cloud-native alternatives like Notion.
- **UI**: While functional, the interface may feel less fluid than web-first canvas platforms.
- **Real-Time Collaboration**: Lacks multi-user simultaneous real-time editing.

## When to use it
- When you need a cross-platform, open-source note-taking app with strong privacy and E2EE features.
- When you want to host your own note synchronization (e.g., using Nextcloud or WebDAV).
- When you need a note-taking tool that is scriptable via an API and integrated into FastMCP 3.1 agent loops.

## When not to use it
- When real-time, multi-user collaboration is the primary requirement.
- When you prefer the canvas or block-based approach of tools like Obsidian or Notion.

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
4. Copy the **Authorization token** for use in scripts and FastMCP 3.1 connections.

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

### Python Integration with Pydantic v2 Validation
AI agents can interact with Joplin using the REST API to store or retrieve knowledge securely.

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class NoteCreateSchema(BaseModel):
    title: str = Field(..., description="Note title")
    body: str = Field(..., description="Markdown note body")
    parent_id: Optional[str] = Field(None, description="Folder / Notebook ID")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Note title cannot be blank")
        return v

class JoplinClient:
    def __init__(self, token: str, base_url: str = "http://localhost:41184"):
        self.token = token
        self.base_url = base_url

    def create_note(self, note: NoteCreateSchema) -> dict:
        params = {"token": self.token}
        data = note.model_dump(exclude_none=True)
        response = requests.post(f"{self.base_url}/notes", params=params, json=data)
        response.raise_for_status()
        return response.json()

# Example usage
client = JoplinClient(token="your_auth_token")
note_data = NoteCreateSchema(
    title="Claude 5.1 Research Findings",
    body="Analysis of latest model performance and FastMCP 3.1 integration..."
)
res = client.create_note(note_data)
print(f"Created note ID: {res.get('id')}")
```

## Related tools / concepts
- [Obsidian](obsidian.md)
- [Logseq](logseq.md)
- [Trilium Notes](../../services/trilium.md)
- [Anytype](../intake_storage/anytype.md)
- [Nextcloud](../../services/nextcloud.md)
- [Khoj](../intake_storage/khoj.md)
- [Notion AI](notion-ai.md)
- [Model Context Protocol (FastMCP 3.1)](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://joplinapp.org/)
- [Joplin Data API Reference](https://joplinapp.org/api/references/rest_api/)
- [Joplin GitHub](https://github.com/laurent22/joplin)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
