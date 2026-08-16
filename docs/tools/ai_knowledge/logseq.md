# Logseq

## What it is
Logseq is a privacy-first, open-source knowledge management and collaboration platform. It is a local-first application that treats information as a "knowledge graph" rather than a set of files, utilizing an outliner-based approach to capture and organize thoughts. As of early January 2027, Logseq is a cornerstone of privacy-first Personal Knowledge Management (PKM), offering high-performance SQLite database storage alongside local Markdown/Org-mode files, fully compatible with **FastMCP 3.1** (Model Context Protocol) for autonomous agent graph interaction.

## What problem it solves
Traditional note-taking apps force users into rigid, hierarchy-bound file systems. Logseq solves this by using bidirectional linking and block-level references, allowing users to build a non-linear network of ideas while retaining 100% data ownership via local plain-text files and high-speed local database indexes. This architecture prevents vendor lock-in and ensures private knowledge graphs remain accessible offline and to local or cloud-hosted AI agents.

## Where it fits in the stack
**AI & Knowledge** — serves as a privacy-focused knowledge intake and storage engine. Its block-level granularity makes it exceptionally well-suited for RAG (Retrieval-Augmented Generation) applications using models like **Claude 5.1**, **GPT-5.5**, or **Llama 4**, as agents can retrieve and cite precise bullet points rather than entire documents, minimizing context noise.

## Typical use cases
- **Daily Journaling**: Using the "Journals" page as the primary entry point for daily tasks, meeting records, and thoughts.
- **Agentic PKM**: Connecting Logseq to a [FastMCP 3.1](../automation_orchestration/mcp.md) server to allow **Claude 5.1** and **GPT-5.5** to query, index, and update notes securely.
- **Project Management**: Linking blocks to project master pages to build dynamic views across multi-date journal entries.
- **Academic & Technical Research**: Annotating PDFs and structuring block references into synthesis graphs.

## Strengths
- **Open Source**: Fully transparent codebase with an active developer community.
- **Privacy-First**: No mandatory cloud sync; all data resides locally on disk by default.
- **Atomic Granularity**: Block-level references allow micro-citations, making it ideal for LLM context retrieval.
- **FastMCP 3.1 Native**: Native integration with Model Context Protocol servers enables autonomous multi-agent graph navigation.
- **Version Control**: Built-in Git integration for local revision history and cross-machine syncing.

## Limitations
- **Learning Curve**: The outliner-only paradigm and Datalog query syntax require an initial adjustment period.
- **Performance at Scale**: Very large graphs (100k+ blocks) require high-speed NVMe storage when running complex Datalog queries.
- **Mobile Sync Overhead**: Syncing across mobile devices without Logseq Sync requires third-party mechanisms like Syncthing or Git.

## When to use it
- When you require a local-first knowledge graph that prioritizes semantic relationships over strict folder trees.
- When you need native Git integration for versioning and collaborative graph building.
- For atomic note-taking where every bullet point can serve as an indexed RAG chunk for frontier models like Gemini 4.0 Pro or Llama 4.

## When not to use it
- When you prefer traditional long-form document layout editors (consider [Obsidian](obsidian.md)).
- When real-time multi-user web-based document editing is mandatory (consider Google Docs or Microsoft Loop).
- For canvas-centric visual whiteboarding as the primary interface.

## Getting started

### Installation
Download Logseq for macOS, Linux, or Windows from the official site or package manager:
```bash
# macOS (Homebrew)
brew install --cask logseq
```

### Basic Workflow
1. Open Logseq and initialize a local folder as your "Graph."
2. Write daily notes in the **Journals** section (`YYYY_MM_DD.md`).
3. Link concepts using `[[Page Name]]`.
4. Reference specific blocks using `((block-uuid))`.

## CLI examples

### 1. Version Control with Git
If Git tracking is enabled, manage graph commits via CLI:
```bash
cd ~/my-logseq-graph
git status
git commit -m "Daily update $(date +%Y-%m-%d) via Home Admin Agent"
```

### 2. Batch Task Filtering
Query open tasks across journal files using standard utilities:
```bash
# Find all blocks containing "TODO" across journals
grep -r "TODO" ~/my-logseq-graph/journals/*.md
```

### 3. Querying Logseq FastMCP 3.1 Server
Invoke Logseq FastMCP tools via `mcp-cli`:
```bash
mcp call logseq-server search_blocks --query "Project Alpha" --mcp-version 3.1
```

## API examples

### Python: Validating and Extracting Journal Blocks
The following example demonstrates using **Pydantic v2** to parse and validate Logseq block data extracted from Markdown files:

```python
import pathlib
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class LogseqBlock(BaseModel):
    block_id: Optional[str] = Field(default=None, description="UUID of the block if present")
    content: str = Field(..., description="Raw Markdown content of the block")
    is_todo: bool = Field(default=False)

    @field_validator("is_todo", mode="before")
    @classmethod
    def check_todo(cls, v: bool, info) -> bool:
        if isinstance(v, bool):
            return v
        return False

class JournalEntry(BaseModel):
    date_str: str = Field(..., pattern=r"^\d{4}_\d{2}_\d{2}$")
    blocks: List[LogseqBlock] = Field(default_factory=list)

def parse_journal_file(file_path: pathlib.Path) -> JournalEntry:
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    blocks = []
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            blocks.append(LogseqBlock(
                content=cleaned,
                is_todo="TODO" in cleaned
            ))

    date_part = file_path.stem
    return JournalEntry(date_str=date_part, blocks=blocks)

# Example execution
journal_path = pathlib.Path.home() / "Documents/logseq/journals/2027_01_07.md"
if journal_path.exists():
    entry = parse_journal_file(journal_path)
    print(f"Parsed journal {entry.date_str} with {len(entry.blocks)} blocks.")
    print(entry.model_dump())
```

### FastMCP 3.1 Tool Request Schema
When an AI agent powered by **Claude 5.1** or **GPT-5.5** writes to Logseq via FastMCP 3.1:

```json
{
  "tool": "logseq_add_note",
  "arguments": {
    "page": "2027-01-07",
    "content": "Verified FastMCP 3.1 graph indexer on Llama 4 local instance.",
    "parent_block_id": "6a89c201-41b9-4a7b-8c1d-ef1234567890"
  }
}
```

## Related tools / concepts
- [Obsidian](obsidian.md) - Non-outliner local Markdown knowledge base alternative.
- [Anytype](../intake_storage/anytype.md) - Local-first, object-oriented personal knowledge base.
- [SilverBullet](../intake_storage/silverbullet.md) - Extensible Markdown wiki system.
- [Ollama](../../services/ollama.md) - Host local LLMs for private Logseq AI plugins.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Protocol for AI-Logseq graph integration (FastMCP 3.1).
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) - Using Logseq blocks as precise retrieval sources.
- [Syncthing](../../services/syncthing.md) - Recommended open-source cross-device file synchronization.

## Sources / references
- [Logseq Official Site](https://logseq.com/)
- [Logseq GitHub Repository](https://github.com/logseq/logseq)
- [FastMCP Logseq Bridge Spec](https://github.com/logseq/mcp-server-logseq)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
