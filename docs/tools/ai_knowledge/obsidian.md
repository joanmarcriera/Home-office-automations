# Obsidian

## What it is
Obsidian is a powerful knowledge base built on top of a local folder of plain text Markdown files. It is highly extensible through plugins and themes, allowing you to build a personalized second brain.

## What problem it solves
Provides a flexible, local-first environment for organizing notes and knowledge using plain Markdown files, with a rich plugin ecosystem for customization. It solves the "data lock-in" problem of cloud-based note-taking apps by keeping all files as standard Markdown on your local disk.

## Where it fits in the stack
AI & Knowledge — serves as a personal knowledge management tool that stores data locally as Markdown, fitting the privacy-first philosophy of the stack. It often acts as the primary interface for "thinking in public" and "thinking in private" within the homelab ecosystem.

## Typical use cases
- Building a personal knowledge base with bidirectional links and graph view
- Writing and organizing documentation, research notes, and daily journals
- Extending functionality with community plugins such as AI-powered note linking
- Implementing Zettelkasten or other knowledge management methodologies
- Local-first RAG (Retrieval-Augmented Generation) source for personal agents

## Strengths
- Data stored as plain Markdown files, ensuring portability and longevity
- Large and active plugin and theme ecosystem (1000+ community plugins)
- Strong graph visualization for exploring connections between notes
- Completely local-first, works offline, and respects privacy
- Highly customizable interface and workflow

## Limitations
- Not open-source (core application is proprietary, though data is open)
- Real-time collaboration features are limited compared to cloud-based tools
- Sync across devices requires Obsidian Sync (paid) or third-party solutions (Git, Syncthing)
- Can become complex to manage with too many plugins or deep customization

## When to use it
- When you want a highly customizable, local-first knowledge base with a large plugin ecosystem
- When plain Markdown portability is important for long-term knowledge preservation
- When you want to leverage local LLMs to query your personal notes

## When not to use it
- When you need a fully open-source tool (consider [Logseq](logseq.md) or [SilverBullet](../intake_storage/silverbullet.md) instead)
- When real-time multi-user collaboration is a core requirement
- When you prefer a structured database-like approach over free-form Markdown (consider [AnyType](../intake_storage/anytype.md))

## Getting started

### Installation
Obsidian is available for Windows, macOS, Linux, iOS, and Android.
Download the installer from the [official website](https://obsidian.md/download).

### Recommended Initial Setup
1. **Create a Vault**: Choose a local folder where your Markdown files will live.
2. **Enable Community Plugins**: Go to `Settings` -> `Community plugins` -> `Turn on community plugins`.
3. **Core Plugins**: Enable `Daily notes`, `Graph view`, and `Backlinks`.

## Technical examples

### Obsidian URI Scheme
Obsidian provides a custom URI scheme to trigger actions from other apps (e.g., n8n or terminal).

```bash
# Open a specific vault and file
open "obsidian://open?vault=my-vault&file=my-note"

# Create a new note with content
open "obsidian://new?vault=my-vault&name=new-note&content=Hello%20world"
```

### Dataview Query (Plugin)
If the Dataview plugin is installed, you can query your notes like a database.

```markdown
```dataview
TABLE file.mtime AS "Last Modified"
FROM "Projects"
WHERE status = "In Progress"
SORT file.mtime DESC
```
```

### Unified Search Integration
Using the project's `scripts/unified_search.py`, you can index Obsidian notes into a local vector DB.

```bash
python3 scripts/obsidian_incremental_indexing.py --vault /path/to/vault --db ./data/chroma_db
```

## Related tools / concepts

- [Logseq](logseq.md)
- [SilverBullet](../intake_storage/silverbullet.md)
- [AnyType](../intake_storage/anytype.md)
- [Joplin](joplin.md)
- [AI Templates](aitmpl.md)
- [Google Gemini](google-gemini.md)
- [Google Opal](google-opal.md)
- [Syncthing](../../services/syncthing.md)
- [Paperless-ngx](../../services/paperless-ngx.md)

## Sources / references
- [Official Website](https://obsidian.md/)
- [Obsidian Help (Official Documentation)](https://help.obsidian.md/)
- [Obsidian Community Plugins](https://obsidian.md/plugins)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
