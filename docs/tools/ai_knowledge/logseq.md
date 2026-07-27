# Logseq

## What it is
Logseq is a privacy-first, open-source knowledge management and collaboration platform. It is a local-first application that treats information as a "knowledge graph" rather than a set of files, utilizing an outliner-based approach to capture and organize thoughts. By late September 2026, it has become a cornerstone of the "Invisible PKM" movement, supporting native SQLite database storage option in parallel with Markdown/Org-mode and fully complying with **MCP 3.1** for autonomous agent interaction.

## What problem it solves
Traditional note-taking apps often struggle with "file-system thinking," where information is siloed into rigid folder structures. Logseq solves this by using bidirectional linking and block-level references, allowing users to build a non-linear network of ideas while maintaining 100% data ownership via local plain-text files (Markdown or Org-mode) and high-speed local database indexes. This prevents "vendor lock-in" and ensures your second brain remains accessible regardless of cloud service availability.

## Where it fits in the stack
**AI & Knowledge** — serves as a privacy-focused knowledge intake and storage point. Its block-level granularity makes it exceptionally well-suited for RAG (Retrieval-Augmented Generation) applications using models like **Claude 5.1** or **Llama 4**, as agents can cite specific bullet points rather than entire documents, significantly reducing context window noise.

## Typical use cases
- **Daily Journaling**: Using the "Journals" page as the primary entry point for all thoughts, tasks, and meetings.
- **Agentic PKM**: Connecting Logseq to an [MCP 3.1](../automation_orchestration/mcp.md) server to allow **GPT-5.5** and Llama 4 to read and write to your knowledge graph autonomously.
- **Project Management**: Linking blocks to project pages to create a dynamic view of all related information across different dates.
- **Research Database**: Utilizing block-level citations and PDF annotation features to build a structured knowledge base for academic or professional work.

## Strengths
- **Open Source**: Fully transparent codebase with a strong community-driven development model.
- **Privacy-First**: No cloud sync required; all data stays on your local machine by default.
- **Granularity**: Block-level references allow for extremely precise linking and retrieval, ideal for LLM-based RAG.
- **MCP 3.1 Native**: Full support for the **Model Context Protocol (MCP 3.1)** allows AI agents to interact with the graph as a sophisticated tool.
- **Version Control**: Native Git integration for tracking changes and syncing across devices.

## Limitations
- **Learning Curve**: The outliner-only paradigm and query language (Datalog) can be daunting for users accustomed to traditional document editors.
- **Performance**: Very large graphs (50k+ blocks) can occasionally experience slow indexing times without high-speed NVMe storage.
- **Mobile Sync**: While improved in late 2026, it still requires third-party tools like iCloud, Git, or Syncthing for reliable cross-device synchronization without the official sync service.

## When to use it
- When you want a local-first knowledge graph that prioritizes relationships between ideas over file organization.
- When you need a tool that integrates natively with Git for version control and collaborative workflows.
- For users who prefer "Atomic" note-taking (one thought per block) for better AI-assisted retrieval and synthesis.

## When not to use it
- When you require a traditional "document" editor (consider [Obsidian](obsidian.md) instead).
- When real-time, multi-user web collaboration is the primary requirement (consider Google Docs or Microsoft Loop).
- When you prefer a purely visual or canvas-first approach to note-taking.

## Getting started

### Installation
Download the latest release from the [Logseq website](https://logseq.com/) or install via a package manager:
```bash
# macOS (Homebrew)
brew install --cask logseq
```

### Basic Workflow
1. Open Logseq and select a local folder to store your "Graph."
2. Start typing in the **Journals** page (standardized as `YYYY_MM_DD.md`).
3. Create a new page by typing `[[Page Name]]`.
4. Link to an existing block by typing `((block-uuid))`.

## CLI examples

### 1. Version Control with Git
If you have Git enabled in your graph, you can manage it via the CLI:
```bash
cd ~/my-logseq-graph
git status
git commit -m "Daily update $(date +%Y-%m-%d) via Home Admin Agent"
```

### 2. Batch Processing with Python
You can use standard CLI tools to process the Markdown files:
```bash
# Find all blocks containing "TODO" and list them
grep -r "TODO" ~/my-logseq-graph/journals/*.md
```

### 3. Logseq API via MCP 3.1
If running an MCP server for Logseq, you can query it via the `mcp-cli` conforming to MCP 3.1:
```bash
mcp call logseq-server search_blocks --query "Project Alpha" --mcp-version 3.1
```

## API examples

### Python: Extracting Blocks
Since Logseq uses plain Markdown, you can parse it directly, but for structured access, use the Logseq Plugin API (running in the app) or an external MCP bridge:

```python
import pathlib

# Simple direct file access to a journal entry
graph_path = pathlib.Path("~/Documents/logseq/journals/2026_09_24.md").expanduser()
if graph_path.exists():
    content = graph_path.expanduser().read_text()
    todo_blocks = [line for line in content.splitlines() if "TODO" in line]
    print(f"Today's Tasks: {todo_blocks}")
```

### MCP 3.1 Tool Call (Agentic)
An AI agent using **Claude 5.1** might call the following tool to add a note:

```json
{
  "tool": "logseq_add_note",
  "arguments": {
    "page": "2026-09-24",
    "content": "Verified Llama 4 quantization on the new Home Admin server.",
    "parent_block_id": "optional-uuid"
  }
}
```

## Related tools / concepts
- [Obsidian](obsidian.md) - The primary non-outliner alternative for personal knowledge management.
- [Anytype](../intake_storage/anytype.md) - Local-first, object-oriented PKM with a focus on privacy.
- [SilverBullet](../intake_storage/silverbullet.md) - Markdown-based extensible wiki system for power users.
- [Ollama](../../services/ollama.md) - Run local models for Logseq AI plugins and agentic workflows.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Standard for AI-Logseq interaction (MCP 3.1).
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) - Using Logseq as a primary source for Retrieval-Augmented Generation.
- [Syncthing](../../services/syncthing.md) - Recommended open-source tool for syncing Logseq graphs across devices.

## Sources / references
- [Logseq Official Documentation](https://docs.logseq.com/)
- [Logseq GitHub Repository](https://github.com/logseq/logseq)
- [MCP Logseq Server](https://github.com/logseq/mcp-server-logseq)

## Contribution Metadata
- Last reviewed: 2026-09-24
- Confidence: high
