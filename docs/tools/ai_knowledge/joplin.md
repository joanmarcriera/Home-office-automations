# Joplin

## What it is
Joplin is a free, open-source note-taking and to-do application, which can handle a large number of notes organized into notebooks. In late September 2026, it remains a cornerstone for privacy-conscious users who want to maintain absolute control over their data while leveraging modern notes structure. It features native end-to-end encryption (E2EE) and provides a secure API allowing frontier models to index and query note graphs.

## What problem it solves
It provides a secure, private way to sync notes across multiple devices (desktop and mobile) using various cloud or self-hosted services (Nextcloud, Dropbox, WebDAV, etc.). It supports end-to-end encryption (E2EE), solving the privacy concerns associated with proprietary, cloud-only platforms. It also provides a robust API for integration with AI agents like Claude 5.1 and GPT-5.5 via the MCP 3.1 protocol, enabling secure multi-agent local knowledge lookups.

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

### Python Integration
AI agents can interact with Joplin using the REST API to store or retrieve knowledge.

```python
import requests

JOPLIN_TOKEN = "your_auth_token"
BASE_URL = "http://localhost:41184"

def create_note(title, body, folder_id=None):
    params = {"token": JOPLIN_TOKEN}
    data = {
        "title": title,
        "body": body
    }
    if folder_id:
        data["parent_id"] = folder_id

    response = requests.post(f"{BASE_URL}/notes", params=params, json=data)
    return response.json()

# Example: Create a research note
note = create_note("Claude 5.1 Research Findings", "Analysis of latest model performance...")
print(f"Created note ID: {note['id']}")
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
- Last reviewed: 2026-09-24
- Confidence: high
