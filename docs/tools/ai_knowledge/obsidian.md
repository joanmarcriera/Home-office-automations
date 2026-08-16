# Obsidian

## What it is
Obsidian is a personal knowledge management (PKM) application built on top of a local vault of plain-text Markdown files. Highly extensible through community plugins and core modules, Obsidian supports native Model Context Protocol (**FastMCP 3.1**) integration as of early January 2027. Obsidian prioritizes total data ownership, local-first operation, and long-term file longevity.

## What problem it solves
It solves the risk of vendor lock-in, proprietary file formats, and data privacy exposure common in cloud note-taking services. By storing notes as plain Markdown files on local storage, Obsidian ensures notes remain accessible to standard text editors, version control systems, and local scripts. This architecture provides a private knowledge base for Retrieval-Augmented Generation (RAG) pipelines without transmitting sensitive data to external servers.

## Where it fits in the stack
**AI & Knowledge** — serves as a primary personal knowledge base storing plain Markdown notes. It functions as a privacy-focused knowledge repository within the home-office ecosystem, providing local RAG context for frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4**.

## Typical use cases
- Building a personal knowledge graph using bidirectional links, block references, and dynamic graph views.
- Authoring documentation, research notes, technical playbooks, and daily logs.
- Integrating agentic workflows where **Claude 5.1** or **GPT-5.5** securely queries local notes via **FastMCP 3.1**.
- Executing local-first RAG pipelines over private vaults without cloud vector databases.
- Mapping complex multi-topic concepts using the built-in Canvas and Graph interfaces.

## Strengths
- **100% Data Ownership**: Notes are plain Markdown files stored locally, ensuring zero vendor lock-in.
- **Agentic Integration**: Native **FastMCP 3.1** server plugins allow AI agents to search, read, create, and link notes via standard tool protocols.
- **Extensible Ecosystem**: Thousands of community plugins available for Kanban boards, Dataview queries, and local AI assistance.
- **Local-First Architecture**: Operates completely offline, offering low latency and maximum privacy.
- **Deep Interlinking**: Fine-grained block references and backlink analysis foster semantic connections between ideas.

## Limitations
- **Proprietary Application**: The desktop and mobile applications are closed-source, though the underlying data format (Markdown) is open.
- **Sync Setup**: Cross-device synchronization requires Obsidian Sync or manual configuration using Git, Tailscale, or Syncthing.
- **Extension Overhead**: Large plugin suites require ongoing maintenance and configuration management.

## When to use it
- When building a highly customizable, local-first knowledge base with an active community plugin ecosystem.
- When long-term data preservation in plain Markdown is essential.
- When providing frontier AI models with private contextual access to notes via local FastMCP 3.1 servers.

## When not to use it
- When requiring an entirely open-source core application (consider [Logseq](logseq.md) instead).
- When real-time, concurrent multi-user document editing is required.
- When preferring an outliner-only interface over document-focused Markdown.

## Getting started

### Installation
Obsidian is available for macOS, Windows, Linux, iOS, and Android.
Download the installer from the [official website](https://obsidian.md/download).

### Recommended Initial Setup
1. **Create Vault**: Select a local directory to host your Markdown notes.
2. **Community Plugins**: Navigate to `Settings` -> `Community plugins` and enable third-party plugins.
3. **Core Modules**: Enable `Daily notes`, `Graph view`, `Canvas`, and `Backlinks`.
4. **FastMCP Server**: Install the 'MCP Obsidian' plugin to enable agentic tool integration.

## CLI examples

### 1. Triggering Note Actions via URI
Obsidian supports custom URI calls for terminal-based automation:
```bash
# Open a specific vault note
open "obsidian://open?vault=my-vault&file=my-note"

# Create a new note with content
open "obsidian://new?vault=my-vault&name=meeting-notes&content=Discuss%20Claude%205-1%20integration"
```

### 2. Searching Notes via Grep
Query notes directly using standard command-line utilities:
```bash
# Search for specific terms across vault files
grep -r "FastMCP 3.1" ~/Documents/ObsidianVault/
```

### 3. Local Vault Indexing
Index vault Markdown files for vector search using local embedding utilities:
```bash
python3 scripts/obsidian_incremental_indexing.py --vault ~/ObsidianVault --db ./data/chroma_db
```

## API examples

### Dataview Inline Query
Using the Dataview plugin JS API to list recently updated notes:

```javascript
// List notes modified today in the Projects directory
dv.list(dv.pages('"Projects"').where(p => p.file.mday.toISODate() == dv.date('today').toISODate()).file.link);
```

### Python: Validating Note Metadata with Pydantic v2
Parse YAML frontmatter from Obsidian Markdown files using strict **Pydantic v2** validation schemas:

```python
import pathlib
import frontmatter
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class NoteMetadataSchema(BaseModel):
    title: str = Field(..., description="Note title from frontmatter or filename")
    last_reviewed: datetime = Field(..., description="ISO review timestamp")
    confidence: str = Field(default="high")
    tags: list[str] = Field(default_factory=list)

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: str) -> str:
        allowed = {"high", "medium", "low"}
        if v.lower() not in allowed:
            raise ValueError(f"Confidence must be one of {allowed}")
        return v.lower()

def load_and_validate_note(file_path: pathlib.Path) -> NoteMetadataSchema:
    post = frontmatter.load(file_path)
    metadata = NoteMetadataSchema(
        title=post.get("title", file_path.stem),
        last_reviewed=post.get("Last reviewed", datetime.now()),
        confidence=post.get("Confidence", "high"),
        tags=post.get("tags", [])
    )
    return metadata

# Execution example
note_file = pathlib.Path.home() / "ObsidianVault/Architecture.md"
if note_file.exists():
    validated = load_and_validate_note(note_file)
    print("Validated note metadata:")
    print(validated.model_dump())
```

### FastMCP 3.1 Tool Request Schema
An agent running **Claude 5.1** or **GPT-5.5** uses this FastMCP 3.1 payload to search Obsidian notes:

```json
{
  "tool": "obsidian_search",
  "arguments": {
    "query": "FastMCP 3.1 architecture standards",
    "vault": "MainVault",
    "limit": 5
  }
}
```

## Related tools / concepts
- [Logseq](logseq.md) - Outliner-based local Markdown PKM alternative.
- [Anytype](../intake_storage/anytype.md) - Local-first, object-oriented PKM software.
- [SilverBullet](../intake_storage/silverbullet.md) - Extensible Markdown wiki system.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Communication standard for agentic note access (FastMCP 3.1).
- [Claude](../ai_knowledge/claude.md) - Frontier model commonly paired with Obsidian for research synthesis.
- [Syncthing](../../services/syncthing.md) - Open-source utility for cross-device vault synchronization.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) - Implementing retrieval pipelines over private Obsidian notes.

## Sources / references
- [Obsidian Official Website](https://obsidian.md/)
- [Obsidian Documentation](https://help.obsidian.md/)
- [MCP Obsidian Plugin Repository](https://github.com/vrtmrz/mcp-obsidian)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
