# Trilium Notes (TriliumNext)

Trilium Notes is a hierarchical note taking application with focus on building large personal knowledge bases. Following the transition of the original project to maintenance mode, the community-driven [TriliumNext](https://github.com/TriliumNext/TriliumNext) fork has become the primary active branch, introducing significant modern features.

## What it is
Trilium Notes is a hierarchical note-taking application focused on building large personal knowledge bases. It features deep nesting, powerful scripting (JavaScript), and advanced visualization of note relationships. The **TriliumNext** fork continues this legacy with improved performance, security, and modern note types.

## What problem it solves
Managing thousands of notes with complex inter-relationships is difficult in standard "flat" or "shallow" note apps. Trilium solves this by treating notes as a forest of trees, allowing a single note to exist in multiple places, and providing an automation engine to manage metadata and note lifecycle.

## Where it fits in the stack
**Category**: Services / Knowledge Management. It serves as the **core intellectual repository** for structured long-term knowledge, research, and documentation.

## Typical use cases
- Building a Personal Knowledge Base (PKB).
- Journaling and daily logs.
- Technical documentation and code snippet management.
- Structured data management using the new **Spreadsheet** note type.
- Digitizing paper notes via built-in **OCR**.

## Strengths
- Extremely flexible hierarchical structure.
- Built-in scripting (JavaScript) and automation.
- Self-hostable with strong sync capabilities.
- Native support for **Spreadsheets** (Excel-like editing via Univer Sheets).
- Built-in **OCR support** for images, PDFs, and Office documents.

## Limitations
- Steeper learning curve compared to simple note apps.
- UI can feel cluttered due to high feature density.
- Transitioning from `api.axios` to `fetch()` in legacy scripts.

## When to use it
- When you need more than just flat tags or shallow folders for your notes.
- When you want to automate your knowledge base with scripts.
- When you need integrated spreadsheet and document search capabilities.

## When not to use it
- For quick, ephemeral notes (use a simple scratchpad).
- If you prefer a "polished" SaaS interface over a powerful, local-first tool.

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

## Advanced Features
### Spreadsheets
TriliumNext introduces a native spreadsheet note type powered by Univer Sheets. This allows for complex calculations, formulas, and structured data entry directly within the note hierarchy.

### OCR & Text Extraction
The built-in OCR engine (configured in Media options) automatically extracts text from:
- Images (PNG, JPG)
- PDF Documents
- Office Files (Word, Excel, PowerPoint)
This text is indexed and becomes fully searchable within the Trilium global search.

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md)
- [Logseq](../tools/ai_knowledge/logseq.md)
- [Joplin](../tools/ai_knowledge/joplin.md)
- [AnyType](../tools/ai_knowledge/anytype.md) — for a decentralized alternative
- [SilverBullet](../tools/ai_knowledge/silverbullet.md) — for a hackable, markdown-based knowledge base
- [n8n](n8n.md) — for automating note creation from external events
- [Paperless-ngx](paperless-ngx.md) — for advanced document management and OCR

## Sources / References
- [Official Website (TriliumNext)](https://github.com/TriliumNext/TriliumNext)
- [TriliumNext Releases](https://github.com/TriliumNext/TriliumNext/releases)
- [Trilium Wiki](https://github.com/zadam/trilium/wiki)

## Backlog
- [x] Perform quarterly technical freshness audit (Completed 2026-05-26).

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high
