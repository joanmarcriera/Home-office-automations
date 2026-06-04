# Logseq

## What it is
Logseq is a privacy-first, open-source knowledge management and collaboration platform. It is a local-first application that treats information as a "knowledge graph" rather than a set of files, utilizing an outliner-based approach to capture and organize thoughts.

## What problem it solves
Traditional note-taking apps often struggle with "file-system thinking," where information is siloed into rigid folder structures. Logseq solves this by using bidirectional linking and block-level references, allowing users to build a non-linear network of ideas while maintaining 100% data ownership via local plain-text files (Markdown or Org-mode).

## Where it fits in the stack
AI & Knowledge — serves as a privacy-focused knowledge intake and storage point. Its block-level granularity makes it exceptionally well-suited for RAG (Retrieval-Augmented Generation) applications, as agents can cite specific bullet points rather than entire documents.

## Typical use cases
- **Daily Journaling**: Using the "Journals" page as the primary entry point for all thoughts, tasks, and meetings.
- **Project Management**: Linking blocks to project pages to create a dynamic view of all related information across different dates.
- **Academic Research**: Utilizing block-level citations and PDF annotation features to build a structured research database.

## Strengths
- **Open Source**: Fully transparent codebase with a strong community focus.
- **Privacy-First**: No cloud sync required; data stays on your local machine.
- **Granularity**: Block-level references allow for extremely precise linking and retrieval.
- **Extensible**: Built-in query engine (Datalog) for creating dynamic lists of tasks and notes.

## Limitations
- **Learning Curve**: The outliner-only paradigm and query language can be daunting for new users.
- **Performance**: Large graphs (10k+ pages) can occasionally experience slow indexing times.
- **Formatting**: Not ideal for users who need to export information as polished, long-form PDF documents.

## When to use it
- When you want a local-first knowledge graph that prioritizes relationships between ideas over file organization.
- When you need a tool that integrates natively with Git for version control.
- For users who prefer "Atomic" note-taking (one thought per block).

## When not to use it
- When you require a traditional "document" editor (consider [Obsidian](obsidian.md) instead).
- When real-time, multi-user web collaboration is the primary requirement.

## Getting started

### 1. Installation
Download the latest release from the [Logseq website](https://logseq.com/) or install via a package manager:
```bash
# macOS (Homebrew)
brew install --cask logseq
```

### 2. Basic Workflow
1. Open Logseq and select a local folder to store your "Graph."
2. Start typing in the **Journals** page.
3. Create a new page by typing `[[Page Name]]`.
4. Link to an existing block by typing `((block-uuid))`.

### 3. AI Integration
Logseq supports several community plugins for AI integration (e.g., `Logseq AI Assistant`). You can connect it to [Ollama](../../services/ollama.md) or [OpenRouter](openrouter.md) to:
- Generate summaries of long journal entries.
- Ask questions about your local graph using RAG.
- Auto-tag blocks based on content.

## Related tools / concepts
- [Obsidian](obsidian.md)
- [Anytype](../intake_storage/anytype.md)
- [SilverBullet](../intake_storage/silverbullet.md)
- [Ollama](../../services/ollama.md)
- [OpenRouter](openrouter.md)
- [LlamaIndex](llamaindex.md)
- [LangChain](langchain.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)

## Sources / references
- [Logseq Official Documentation](https://docs.logseq.com/)
- [Logseq GitHub Repository](https://github.com/logseq/logseq)

## Contribution Metadata
- Last reviewed: 2026-05-14
- Confidence: high
