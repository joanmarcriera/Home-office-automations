# Obsidian Vector Search

## What it is
The application of vector search technology to personal knowledge bases stored in Obsidian.

## What problem it solves
Traditional keyword search in Obsidian often fails to find related concepts if different terminology is used. Vector search enables "semantic" discovery across years of journals and notes.

## Where it fits in the stack
Bridges the gap between static Markdown files and local AI agents (RAG).

## Typical use cases
- "What did I learn about gardening last year?" (Retrieves notes even if they don't contain the exact word 'gardening').
- Finding connections between disparate project logs.
- Synthesizing "Daily Briefings" with relevant historical context.

## Strengths
- Enables "Talk to your notes" interfaces.
- Works entirely offline with local embeddings (e.g., via Ollama).
- Plugins like `Obsidian-Vibe` or custom python scripts make indexing easy.

## Limitations
- Requires re-indexing when notes change significantly.
- Can be "noisy" if notes are not well-chunked.

## When to use it
- When you have a large vault (>1000 notes) and find it hard to navigate.
- When building a "Personal Second Brain" agent.

## When not to use it
- If your vault is small or you rely heavily on strict tag/folder structures.

## Related tools / concepts
- [Obsidian](../../tools/ai_knowledge/obsidian.md)
- [Vector DB Comparison](./vector-db-comparison.md)
- [RAG Patterns](../patterns/rag.md)

## Sources / references
- [Obsidian-Vibe GitHub](https://github.com/vibe/obsidian-vibe)
- [Embedding Obsidian Notes (Blog)](https://simonwillison.net/2023/Oct/23/embeddings/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: medium
