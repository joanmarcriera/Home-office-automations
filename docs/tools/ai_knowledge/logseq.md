# Logseq

## What it is
Logseq is a privacy-first, open-source knowledge management and collaboration platform. It is a local-first application that treats information as a "knowledge graph" rather than a set of files, utilizing an outliner-based approach to capture and organize thoughts.

## What problem it solves
Traditional note-taking apps often struggle with "file-system thinking," where information is siloed into rigid folder structures. Logseq solves this by using bidirectional linking and block-level references, allowing users to build a non-linear network of ideas while maintaining 100% data ownership via local plain-text files (Markdown or Org-mode).

## Where it fits in the stack
AI & Knowledge — serves as a privacy-focused knowledge intake and storage point. Its block-level granularity makes it exceptionally well-suited for RAG (Retrieval-Augmented Generation) applications using models like **Claude 4.8** or **Llama 4 Maverick**, as agents can cite specific bullet points rather than entire documents.

## Typical use cases
- **Daily Journaling**: Using the "Journals" page as the primary entry point for all thoughts, tasks, and meetings.
- **Agentic PKM**: Connecting Logseq to an [MCP](../automation_orchestration/mcp.md) server to allow **GPT-5.5** to read and write to your knowledge graph.
- **Project Management**: Linking blocks to project pages to create a dynamic view of all related information across different dates.
- **Research Database**: Utilizing block-level citations and PDF annotation features to build a structured knowledge base.

## Strengths
- **Open Source**: Fully transparent codebase with a strong community focus.
- **Privacy-First**: No cloud sync required; data stays on your local machine.
- **Granularity**: Block-level references allow for extremely precise linking and retrieval.
- **MCP Integration**: Official support for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) allows AI agents to interact with the graph as a tool.

## Limitations
- **Learning Curve**: The outliner-only paradigm and query language (Datalog) can be daunting for new users.
- **Performance**: Very large graphs (20k+ pages) can occasionally experience slow indexing times without high-speed NVMe storage.
- **Mobile Sync**: Requires third-party tools like iCloud, Git, or Syncthing for cross-device synchronization.

## When to use it
- When you want a local-first knowledge graph that prioritizes relationships between ideas over file organization.
- When you need a tool that integrates natively with Git for version control.
- For users who prefer "Atomic" note-taking (one thought per block) for better AI retrieval.

## When not to use it
- When you require a traditional "document" editor (consider [Obsidian](obsidian.md) instead).
- When real-time, multi-user web collaboration is the primary requirement.

## Getting started

### Installation
Download the latest release from the [Logseq website](https://logseq.com/) or install via a package manager:
```bash
# macOS (Homebrew)
brew install --cask logseq
```

### Basic Workflow
1. Open Logseq and select a local folder to store your "Graph."
2. Start typing in the **Journals** page.
3. Create a new page by typing `[[Page Name]]`.
4. Link to an existing block by typing `((block-uuid))`.

## CLI examples

### 1. Version Control with Git
If you have Git enabled in your graph, you can manage it via the CLI:
```bash
cd ~/my-logseq-graph
git status
git commit -m "Daily update $(date +%Y-%m-%d)"
```

### 2. Batch Processing with Python
You can use standard CLI tools to process the Markdown files:
```bash
# Find all blocks containing "TODO" and list them
grep -r "TODO" ~/my-logseq-graph/journals/*.md
```

### 3. Logseq API via MCP
If running an MCP server for Logseq, you can query it via the `mcp-cli`:
```bash
mcp call logseq-server search_blocks --query "Project Alpha"
```

## API examples

### Python: Extracting Blocks
Since Logseq uses plain Markdown, you can parse it directly, but for structured access, use the Logseq Plugin API (running in the app) or an external MCP bridge:

```python
import pathlib

# Simple direct file access
graph_path = pathlib.Path("~/Documents/logseq/journals/2026_06_10.md").expanduser()
if graph_path.exists():
    content = graph_path.read_text()
    todo_blocks = [line for line in content.splitlines() if "TODO" in line]
    print(f"Today's Tasks: {todo_blocks}")
```

### MCP Tool Call (Agentic)
An AI agent using **Claude 4.8** might call the following tool to add a note:

```json
{
  "tool": "logseq_add_note",
  "arguments": {
    "page": "2026-06-10",
    "content": "Discussed Llama 4 Maverick quantization with the team.",
    "parent_block_id": "optional-uuid"
  }
}
```

## Related tools / concepts
- [Obsidian](obsidian.md) - The primary non-outliner alternative.
- [Anytype](../intake_storage/anytype.md) - Local-first, object-oriented PKM.
- [SilverBullet](../intake_storage/silverbullet.md) - Markdown-based extensible wiki.
- [Ollama](../../services/ollama.md) - Run local models for Logseq AI plugins.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Standard for AI-Logseq interaction.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) - Using Logseq as a source for RAG.
- [Syncthing](../../services/syncthing.md) - Recommended tool for syncing Logseq graphs.

## Sources / references
- [Logseq Official Documentation](https://docs.logseq.com/)
- [Logseq GitHub Repository](https://github.com/logseq/logseq)
- [MCP Logseq Server](https://github.com/logseq/mcp-server-logseq)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
