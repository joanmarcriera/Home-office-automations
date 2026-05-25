# Trilium Notes

Trilium Notes is a hierarchical note taking application with focus on building large personal knowledge bases.

## What it is
Trilium Notes is a hierarchical note-taking application focused on building large personal knowledge bases. It features deep nesting, powerful scripting (JavaScript), and advanced visualization of note relationships.

## What problem it solves
Managing thousands of notes with complex inter-relationships is difficult in standard "flat" or "shallow" note apps. Trilium solves this by treating notes as a forest of trees, allowing a single note to exist in multiple places, and providing an automation engine to manage metadata and note lifecycle.

## Where it fits in the stack
**Category**: Services / Knowledge Management. It serves as the **core intellectual repository** for structured long-term knowledge, research, and documentation.

## Typical use cases
- Building a Personal Knowledge Base (PKB).
- Journaling and daily logs.
- Technical documentation and code snippet management.

## Strengths
- Extremely flexible hierarchical structure.
- Built-in scripting (JavaScript) and automation.
- Self-hostable with strong sync capabilities.

## Limitations
- Steeper learning curve compared to simple note apps.
- UI can feel cluttered due to high feature density.

## When to use it
- When you need more than just flat tags or shallow folders for your notes.
- When you want to automate your knowledge base with scripts.

## When not to use it
- For quick, ephemeral notes (use a simple scratchpad).
- If you prefer a "polished" SaaS interface over a powerful, local-first tool.

## Getting started

The easiest way to self-host Trilium is via Docker.

### Installation (Docker)
```bash
docker run -d -p 8080:8080 -v ~/trilium-data:/home/node/trilium-data zadam/trilium:latest
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

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md)
- [Logseq](../tools/ai_knowledge/logseq.md)
- [Joplin](../services/joplin.md)
- [AnyType](../tools/ai_knowledge/anytype.md) — for a decentralized alternative
- [SilverBullet](../tools/ai_knowledge/silverbullet.md) — for a hackable, markdown-based knowledge base
- [n8n](n8n.md) — for automating note creation from external events

## Sources / References
- [Official Website](https://github.com/zadam/trilium)
- [Trilium Wiki](https://github.com/zadam/trilium/wiki)

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
