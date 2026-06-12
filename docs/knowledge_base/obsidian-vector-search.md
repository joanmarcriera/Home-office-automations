# Obsidian Vector Search

## What it is
Obsidian Vector Search is the application of vector database and embedding technology to personal knowledge bases stored in [Obsidian](../tools/ai_knowledge/obsidian.md). It enables semantic search, automated linking, and retrieval-augmented generation (RAG) across years of journals, research notes, and project logs.

## What problem it solves
Traditional keyword search in Obsidian often fails to find related concepts if different terminology is used (e.g., "AI" vs "Machine Learning"). Vector search enables "semantic" discovery, allowing users to find connections between notes based on their meaning rather than exact word matches.

## Where it fits in the stack
**Knowledge Management / RAG Layer**. It bridges the gap between static Markdown files and local AI agents, serving as the "long-term memory" for personalized LLM workflows.

## Typical use cases
- **Semantic Retrieval**: "What did I learn about gardening last year?" (Retrieves notes even if they don't contain the exact word 'gardening').
- **Connection Discovery**: Finding links between disparate project logs and historical research.
- **Automated Synthesis**: Generating "Daily Briefings" with relevant historical context pulled from the entire vault.

## Strengths
- **Contextual Understanding**: Finds relevant notes that keyword search misses.
- **Privacy-First**: Works entirely offline with local embeddings (e.g., via [Ollama](../services/ollama.md)).
- **Agent-Ready**: Provides a structured interface for agents like [Claude Code](../tools/development_ops/claude-code.md) to query personal notes.

## Limitations
- **Indexing Overhead**: Requires re-indexing when notes change significantly.
- **Chunking Sensitivity**: Search quality depends on how well notes are broken down into semantically meaningful chunks.
- **Hardware Requirements**: Local embedding and search require moderate RAM and CPU resources.

## When to use it
- When you have a large vault (>1,000 notes) and find it hard to navigate via tags or folders alone.
- When building a "Personal Second Brain" AI assistant.
- When you need to synthesize information from multi-year archives.

## When not to use it
- If your vault is small or you rely on strict, well-maintained folder structures.
- If you lack the hardware resources to run local embedding models.

## Getting started

### Option 1: Smart Connections (Community Plugin)
The most popular "chat with your notes" plugin for Obsidian.
1. Install **Smart Connections** from the Community Plugins gallery.
2. Select an embedding provider:
   - **Local**: Use [Ollama](../services/ollama.md) (e.g., `nomic-embed-text`) or built-in transformers.
   - **Cloud**: OpenAI or Anthropic.
3. Allow the plugin to index your vault (stored in `.obsidian/plugins/smart-connections/`).

### Option 2: Khoj (Self-hosted)
A robust AI assistant that integrates with Obsidian and other sources.
1. Run the [Khoj](../tools/intake_storage/khoj.md) server (Docker recommended).
2. Point Khoj to your Obsidian vault directory.
3. Access the vector index via the Khoj Obsidian plugin or web UI.

## CLI examples

### Local Embedding with Ollama
Generate an embedding for a specific note using the command line:
```bash
ollama run nomic-embed-text "This is a note about home automation."
```

### Search with Khoj CLI
Query your indexed vault directly from the terminal:
```bash
khoj chat "How do I set up a home lab?"
```

### Verifying MCP Connectivity
Test the Obsidian MCP server (if installed via [uvx](https://github.com/astral-sh/uv)):
```bash
uvx mcp-server-obsidian --path /path/to/your/vault
```

## API examples

### Python Pipeline (FAISS)
A minimal example of a local indexing pipeline using Python.

```python
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Load model and notes
model = SentenceTransformer('all-MiniLM-L6-v2')
vault_path = "/path/to/your/obsidian/vault"
notes = [os.path.join(vault_path, f) for f in os.listdir(vault_path) if f.endswith('.md')]

# 2. Generate Embeddings
documents = [open(n).read() for n in notes]
embeddings = model.encode(documents)

# 3. Create FAISS Index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype('float32'))

# 4. Search
query_vector = model.encode(["How do I set up a home lab?"])
D, I = index.search(np.array(query_vector).astype('float32'), k=5)
```

### MCP Configuration
Add the Obsidian MCP server to your [Claude Desktop Config](../automation_orchestration/mcp.md).

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-server-obsidian", "--path", "/path/to/your/vault"]
    }
  }
}
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md): The primary note-taking platform.
- [Vector DB Comparison](vector-db-comparison.md): Background on storage engines.
- [RAG Patterns](patterns/rag.md): How retrieval is used in agent workflows.
- [Khoj](../tools/intake_storage/khoj.md): Integrated knowledge assistant.
- [Verba](../tools/ai_knowledge/verba.md): RAG alternative.
- [Ollama](../services/ollama.md): Provider for local embeddings.
- [Model Context Protocol](../automation_orchestration/mcp.md): For bridging notes to agents.
- [LlamaIndex](../tools/ai_knowledge/llamaindex.md): Framework for building RAG pipelines.

## Sources / references
- [Obsidian Official Documentation](https://help.obsidian.md/)
- [Khoj: Personal AI Assistant](https://khoj.dev/)
- [Smart Connections Plugin GitHub](https://github.com/brianpetro/obsidian-smart-connections)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
