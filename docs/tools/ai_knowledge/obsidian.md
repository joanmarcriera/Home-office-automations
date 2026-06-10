# Obsidian

## What it is
Obsidian is a powerful knowledge base built on top of a local folder of plain text Markdown files. It is highly extensible through plugins and themes, allowing you to build a personalized "second brain" with native support for the **Model Context Protocol (MCP)** as of early 2026.

## What problem it solves
It provides a flexible, local-first environment for organizing notes and knowledge using plain Markdown files, with a rich plugin ecosystem for customization. It solves the "data lock-in" problem of cloud-based note-taking apps by keeping all files as standard Markdown on your local disk.

## Where it fits in the stack
AI & Knowledge — serves as a personal knowledge management tool that stores data locally as Markdown, fitting the privacy-first philosophy of the stack. It often acts as the primary interface for "thinking in public" and "thinking in private" within the homelab ecosystem, frequently used as a RAG source for models like **Claude 4.8** and **GPT-5.5**.

## Typical use cases
- Building a personal knowledge base with bidirectional links and graph view.
- Writing and organizing documentation, research notes, and daily journals.
- Integrating with agentic workflows where **Claude 4.8** reads your notes to provide context.
- Local-first RAG (Retrieval-Augmented Generation) source for personal agents via [MCP](../automation_orchestration/mcp.md).
- Visualizing complex relationships between ideas using the built-in Canvas and Graph views.

## Strengths
- **Data Ownership**: Files are plain Markdown on your disk, ensuring portability and longevity.
- **Agentic Ready**: Native **MCP** server plugins allow AI agents to securely search and retrieve notes.
- **Extensible**: Over 2,000 community plugins for everything from Kanban boards to advanced AI assistants.
- **Local-First**: Works entirely offline, respecting privacy and providing instant response times.
- **Deep Linking**: Block-level references and bidirectional links create a dense web of information.

## Limitations
- **Not Open-Source**: The core application is proprietary, although the data format (Markdown) is open.
- **Sync Complexity**: Real-time sync across devices requires Obsidian Sync (paid) or manual setup with Git or Syncthing.
- **Learning Curve**: The vast plugin ecosystem can lead to "configuration paralysis" for new users.

## When to use it
- When you want a highly customizable, local-first knowledge base with a large plugin ecosystem.
- When plain Markdown portability is important for long-term knowledge preservation.
- When you want to leverage frontier models like **GPT-5.5** to query your personal notes securely.

## When not to use it
- When you need a fully open-source tool (consider [Logseq](logseq.md) instead).
- When real-time multi-user web collaboration is the primary requirement.
- When you prefer a structured database-like approach over free-form Markdown.

## Getting started

### Installation
Obsidian is available for Windows, macOS, Linux, iOS, and Android.
Download the installer from the [official website](https://obsidian.md/download).

### Recommended Initial Setup
1. **Create a Vault**: Choose a local folder where your Markdown files will live.
2. **Enable Community Plugins**: Go to `Settings` -> `Community plugins` -> `Turn on community plugins`.
3. **Core Plugins**: Enable `Daily notes`, `Graph view`, and `Backlinks`.

## CLI examples

### 1. Opening Notes via URI
Obsidian provides a custom URI scheme to trigger actions from the terminal:
```bash
# Open a specific vault and file
open "obsidian://open?vault=my-vault&file=my-note"

# Create a new note with content from the CLI
open "obsidian://new?vault=my-vault&name=meeting-notes&content=Discuss%20GPT-5.5%20integration"
```

### 2. Searching Vault via Grep
Since files are plain text, you can use standard CLI tools:
```bash
# Find all notes mentioning 'Llama 4'
grep -r "Llama 4" ~/Documents/ObsidianVault/
```

### 3. Indexing for RAG
Use the repository's indexing script to prepare your vault for AI retrieval:
```bash
python3 scripts/obsidian_incremental_indexing.py --vault ~/ObsidianVault --db ./data/chroma_db
```

## API examples

### 1. Dataview Query (Internal API)
If the Dataview plugin is installed, you can use its JS API within notes:

```javascript
// List all notes modified today
dv.list(dv.pages().where(p => p.file.mday.toISODate() == dv.date('today').toISODate()).file.link);
```

### 2. Python: Accessing Metadata
You can use `frontmatter` to read Obsidian note metadata in your own scripts:

```python
import frontmatter

post = frontmatter.load('/path/to/vault/MyNote.md')
print(f"Status: {post.get('status')}")
print(f"Content: {post.content[:100]}...")
```

### 3. MCP Tool Call (Agentic)
An AI agent using the Obsidian MCP server might execute this call:

```json
{
  "tool": "obsidian_search",
  "arguments": {
    "query": "architecture standards",
    "vault": "MainVault"
  }
}
```

## Related tools / concepts
- [Logseq](logseq.md) - The primary outliner alternative.
- [Anytype](../intake_storage/anytype.md) - Local-first, object-oriented PKM.
- [SilverBullet](../intake_storage/silverbullet.md) - Markdown-based wiki system.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Standard for connecting Obsidian to AI.
- [Claude](../ai_knowledge/claude.md) - Frequently used with Obsidian via plugins.
- [Syncthing](../../services/syncthing.md) - Recommended for syncing Obsidian vaults.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) - Implementing retrieval over Obsidian notes.

## Sources / references
- [Obsidian Official Website](https://obsidian.md/)
- [Obsidian Help (Official Documentation)](https://help.obsidian.md/)
- [MCP Obsidian Server](https://github.com/vrtmrz/mcp-obsidian)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
