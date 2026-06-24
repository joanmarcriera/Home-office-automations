# Trilium Notes (TriliumNext)

Trilium Notes is a hierarchical note taking application with focus on building large personal knowledge bases. Following the transition of the original project to maintenance mode, the community-driven [TriliumNext](https://github.com/TriliumNext/TriliumNext) fork has become the primary active branch, introducing significant modern features.

## What it is
Trilium Notes is a hierarchical note-taking application focused on building large personal knowledge bases. It features deep nesting, powerful scripting (JavaScript), and advanced visualization of note relationships. The **TriliumNext** fork continues this legacy with improved performance, security, and modern note types.

## What problem it solves
Managing thousands of notes with complex inter-relationships is difficult in standard "flat" or "shallow" note apps. Trilium solves this by treating notes as a forest of trees, allowing a single note to exist in multiple places, and providing an automation engine to manage metadata and note lifecycle.

## Where it fits in the stack
**Category**: Services / Knowledge Management. It serves as the **core intellectual repository** for structured long-term knowledge, research, and documentation.

## Typical use cases
- Building a Personal Knowledge Base (PKB) with deep hierarchical organization.
- Journaling and daily logs with automated metadata tagging.
- Technical documentation and code snippet management.
- Complex information management using the powerful JavaScript scripting engine.
- Visualizing knowledge maps and relationship graphs.

## Strengths
- **Extreme Flexibility**: Deeply nested hierarchical structure with no practical limit on depth.
- **Automation-Ready**: Built-in JavaScript scripting allows for advanced note lifecycle automation.
- **Local-First**: Self-hostable with strong synchronization between desktop and server instances.
- **Modern Fork**: TriliumNext provides active maintenance, improved security, and performance optimizations.
- **Extensible**: Powerful API and "Widget" system for creating custom UI components.

## Limitations
- **Steeper Learning Curve**: The high feature density and scripting requirements can be intimidating for new users.
- **UI Density**: The interface is functional but can feel cluttered compared to modern minimalist note apps.
- **Legacy Migration**: Transitioning older scripts from `api.axios` to `fetch()` in newer versions of the fork.

## When to use it
- When you need a highly structured, hierarchical knowledge base that goes beyond simple folders and tags.
- When you want to automate your documentation workflows using JavaScript.
- When data sovereignty and local-first execution are primary requirements.

## When not to use it
- For quick, ephemeral notes (consider a simple scratchpad or mobile-first app).
- If you prefer a highly polished, minimalist "SaaS-like" user interface.
- If you have no need for scripting or advanced automation in your notes.

## Getting started

The easiest way to self-host TriliumNext is via Docker.

### Installation (Docker)
```bash
docker run -d -p 8080:8080 -v ~/trilium-data:/home/node/trilium-data triliumnext/notes:latest
```

## CLI examples
Trilium doesn't have an official first-party CLI, but you can interact with its API using `curl` or manage the service via Docker.

### Check health
```bash
curl http://localhost:8080/api/health
```

### Search for notes via API (curl)
```bash
curl -H "Authorization: <your_token>" "http://localhost:8080/api/notes?search=markdown"
```

### Export a note as HTML
```bash
curl -H "Authorization: <your_token>" "http://localhost:8080/api/notes/<note_id>/export?format=html" -o note.html
```

## API examples

### Create a note (Python)
```python
import requests

TRILIUM_URL = "http://localhost:8080/api"
API_TOKEN = "your-api-token"

headers = {
    "Authorization": API_TOKEN
}

note_data = {
    "parentNoteId": "root",
    "title": "My New Note",
    "type": "text",
    "content": "This is a note created via API."
}

response = requests.post(f"{TRILIUM_URL}/notes", json=note_data, headers=headers)
print(response.json())
```

### Scripting: Fetch API Transition
In TriliumNext v0.103+, `api.axios` has been removed. Use the native `fetch` API for back-end scripts:

```javascript
// New fetch-based pattern
const response = await fetch('https://api.example.com/data');
const data = await response.json();
api.log(data.message);
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md) — For a Markdown-first personal knowledge base.
- [Logseq](../tools/ai_knowledge/logseq.md) — For privacy-first, local-first outliner notes.
- [Joplin](../tools/ai_knowledge/joplin.md) — For a cross-platform, E2EE alternative.
- [AnyType](../tools/ai_knowledge/anytype.md) — For a decentralized, local-first knowledge operating system.
- [SilverBullet](../tools/ai_knowledge/silverbullet.md) — For a hackable, markdown-based knowledge base with integrated query engine.
- [n8n](n8n.md) — For automating note creation and intake from external events.
- [Paperless-ngx](paperless-ngx.md) — For professional-grade document management and archival.
- [Habitica](habitica.md) — For integrating note-taking with gamified productivity.

## Sources / References
- [Official Website (TriliumNext)](https://github.com/TriliumNext/TriliumNext)
- [TriliumNext Releases](https://github.com/TriliumNext/TriliumNext/releases)
- [Trilium Wiki](https://github.com/zadam/trilium/wiki)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
