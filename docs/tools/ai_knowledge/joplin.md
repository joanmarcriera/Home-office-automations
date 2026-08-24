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
Install the Joplin CLI tool globally via NPM (or download the desktop app from [joplinapp.org](https://joplinapp.org/)):

```bash
npm install -g joplin
```

### Hello-world example
Verify the installation and check version status:

```bash
joplin version
```

To enable the REST Data API for programmatic access:
1. Open Joplin Desktop.
2. Go to **Tools > Options > Web Clipper** (or **Preferences** on macOS).
3. Enable the Web Clipper service.
4. Copy the generated **Authorization Token**.

## CLI examples

### 1. Create a Note inside a Notebook
Create a Markdown note inside a designated notebook:

```bash
joplin mknote "Daily AI Digest" --body "Summary of Claude 5.1 and FastMCP 3.1 updates."
```

### 2. List Notebooks
Display all notebooks in the hierarchy:

```bash
joplin ls /
```

### 3. Synchronize Notes with Remote Backend
Trigger synchronization across configured targets (Nextcloud / WebDAV):

```bash
joplin sync
```

## API examples

### Python Integration with Joplin Data REST API
AI agents can interact with Joplin using the local Data REST API and validate payloads with Pydantic v2:

```python
import requests
from pydantic import BaseModel, Field
from typing import Optional

class NoteCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, description="Note title")
    body: str = Field(..., description="Markdown body content")
    parent_id: Optional[str] = Field(None, description="Notebook folder ID")

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

if __name__ == "__main__":
    client = JoplinClient(token="your_auth_token_here")
    new_note = NoteCreateSchema(
        title="FastMCP 3.1 Architecture Overview",
        body="Key concepts include zero-overhead transport and typed schema validation."
    )
    # res = client.create_note(new_note)
    print(f"Validated note payload for title: {new_note.title}")
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
