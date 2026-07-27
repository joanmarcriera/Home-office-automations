# Obsidian

## What it is
Obsidian is a powerful personal knowledge management (PKM) tool built on top of a local folder of plain text Markdown files (a "Vault"). It is highly extensible through a robust ecosystem of core and community plugins, and it provides native integration with the Model Context Protocol (MCP 3.1) as of late September 2026. Obsidian prioritizes local data ownership, longevity, and offline capability.

## What problem it solves
It solves the issue of proprietary cloud note-taking platforms with strict data lock-in and potential privacy leaks. By storing notes as standard Markdown on local disk, Obsidian ensures that your knowledge remains portable, permanent, and accessible to standard CLI text tools. This architecture makes it an ideal private retrieval source for Retrieval-Augmented Generation (RAG) pipelines without exposing sensitive notes to public cloud services.

## Where it fits in the stack
**AI & Knowledge** — serves as a personal knowledge management tool that stores data locally as Markdown, fitting the privacy-first philosophy of the stack. It acts as the canonical source for "thinking in public" and "thinking in private" within the homelab ecosystem, and acts as a high-signal local RAG source for frontier models like Claude 5.1, GPT-5.5, and Llama 4.

## Typical use cases
- Building a personal knowledge base with bidirectional links and a dynamic graph view.
- Writing and organizing documentation, research notes, and daily journals.
- Integrating with agentic workflows where Claude 5.1 securely reads your notes to provide deep local context.
- Implementing local-first RAG (Retrieval-Augmented Generation) over private notes using [MCP 3.1](../automation_orchestration/mcp.md).
- Visualizing complex relationships between ideas using the built-in Canvas and Graph views.

## Strengths
- **Data Ownership**: Files are plain Markdown on your local disk, ensuring 100% portability and longevity.
- **Agentic Ready**: Native **MCP 3.1** server plugins allow AI agents to securely query, search, and update notes via standard tool protocols.
- **Extensible**: Over 2,500 community plugins for everything from Kanban boards to advanced local AI assistants.
- **Local-First**: Works entirely offline, respecting privacy and offering near-instant latency.
- **Deep Linking**: Block-level references and bidirectional links create a dense, semantic web of information.

## Limitations
- **Not Open-Source**: The core desktop and mobile applications are proprietary, although the data format (Markdown) is completely open.
- **Sync Complexity**: Real-time sync across devices requires Obsidian Sync (paid) or manual setup with Git or Syncthing.
- **Learning Curve**: The vast plugin ecosystem can lead to "configuration paralysis" for new users.

## When to use it
- When you want a highly customizable, local-first knowledge base with a large community plugin ecosystem.
- When plain Markdown portability is important for long-term knowledge preservation.
- When you want to leverage frontier models like Claude 5.1 and GPT-5.5 to query your personal notes securely and privately.

## When not to use it
- When you require a fully open-source tool (consider [Logseq](logseq.md) instead).
- When real-time multi-user web-based collaboration is the primary requirement.
- When you prefer a structured database-like approach over free-form, link-heavy Markdown.

## Getting started

### Installation
Obsidian is available for Windows, macOS, Linux, iOS, and Android.
Download the installer from the [official website](https://obsidian.md/download).

### Recommended Initial Setup
1. **Create a Vault**: Choose a local folder where your Markdown files will live.
2. **Enable Community Plugins**: Go to `Settings` -> `Community plugins` -> `Turn on community plugins`.
3. **Core Plugins**: Enable `Daily notes`, `Graph view`, and `Backlinks`.
4. **Install MCP Server Plugin**: To enable agentic access, install the 'MCP Obsidian' plugin from the community marketplace.

## CLI examples

### 1. Opening Notes via URI
Obsidian provides a custom URI scheme to trigger actions from the terminal:
```bash
# Open a specific vault and file
open "obsidian://open?vault=my-vault&file=my-note"

# Create a new note with content from the CLI
open "obsidian://new?vault=my-vault&name=meeting-notes&content=Discuss%20Claude%205-1%20integration"
```

### 2. Searching Vault via Grep
Since files are plain text, you can use standard CLI tools:
```bash
# Find all notes mentioning 'Llama 4 Maverick'
grep -r "Llama 4 Maverick" ~/Documents/ObsidianVault/
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
// List all notes modified today in the 'Projects' folder
dv.list(dv.pages('"Projects"').where(p => p.file.mday.toISODate() == dv.date('today').toISODate()).file.link);
```

### 2. Python: Accessing Metadata with frontmatter
You can use the `python-frontmatter` library to read Obsidian note metadata and YAML frontmatter:

```python
import frontmatter
from pydantic import BaseModel, Field
from datetime import datetime

class NoteMetadata(BaseModel):
    title: str
    last_reviewed: datetime
    confidence: str = Field("high")

# Load a note and print its status
post = frontmatter.load('/path/to/vault/MyNote.md')
metadata = NoteMetadata(
    title=post.get('title', 'Untitled'),
    last_reviewed=post.get('Last reviewed'),
    confidence=post.get('Confidence', 'high')
)
print(f"Validated metadata: {metadata.model_dump()}")
print(f"Content: {post.content[:100]}...")
```

### 3. MCP 3.1 Tool Call (Agentic)
An AI agent using the Obsidian MCP 3.1 server can execute this standard JSON tool call:

```json
{
  "tool": "obsidian_search",
  "arguments": {
    "query": "architecture standards 2026",
    "vault": "MainVault",
    "limit": 10
  }
}
```

## Related tools / concepts
- [Logseq](logseq.md) - The primary outliner-based alternative for PKM.
- [Anytype](../intake_storage/anytype.md) - Local-first, object-oriented PKM focusing on data sovereignty.
- [SilverBullet](../intake_storage/silverbullet.md) - Markdown-based wiki system for extensible note-taking.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Standards for connecting Obsidian to AI agents (MCP 3.1).
- [Claude](../ai_knowledge/claude.md) - Frontier model frequently used with Obsidian for synthesis.
- [Syncthing](../../services/syncthing.md) - Recommended tool for syncing Obsidian vaults across devices.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) - Implementing retrieval over private Obsidian notes.

## Sources / references
- [Obsidian Official Website](https://obsidian.md/)
- [Obsidian Help (Official Documentation)](https://help.obsidian.md/)
- [MCP Obsidian Server Repository](https://github.com/vrtmrz/mcp-obsidian)

## Contribution Metadata
- Last reviewed: 2026-09-24
- Confidence: high
