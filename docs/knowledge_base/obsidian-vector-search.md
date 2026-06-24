# Obsidian Vector Search

## What it is
The application of vector search technology to personal knowledge bases stored in Obsidian. It involves converting Markdown notes into mathematical vectors (embeddings) to enable semantic retrieval based on meaning rather than just keywords.

## What problem it solves
Traditional keyword search in Obsidian often fails to find related concepts if different terminology is used. Vector search enables "semantic" discovery across years of journals and notes, overcoming the "lexical gap" in personal knowledge management.

## Where it fits in the stack
**Knowledge Management / RAG Layer**. It bridges the gap between static Markdown files and local AI agents, serving as the retrieval engine for Personal Retrieval-Augmented Generation (RAG).

## Typical use cases
- **Semantic Retrieval**: "What did I learn about gardening last year?" (Retrieves notes even if they don't contain the exact word 'gardening').
- **Knowledge Synthesis**: Finding hidden connections between disparate project logs and research papers.
- **Automated Briefings**: Synthesizing "Daily Briefings" with relevant historical context pulled from years of notes.

## Strengths
- **Smarter Discovery**: Finds relevant context that keyword search would miss.
- **Privacy**: Works entirely offline with local embeddings (e.g., via **Ollama**).
- **Extensibility**: Integrates with frontier agents like **Claude 4.8** for advanced synthesis.

## Limitations
- **Maintenance**: Requires re-indexing when notes change significantly.
- **Chunking Sensitivity**: Can be "noisy" if notes are not well-chunked into logical units.
- **Compute Cost**: Local embedding generation can be resource-intensive for very large vaults (>10k notes).

## When to use it
- When you have a large vault (>1000 notes) and find it hard to navigate using folders or tags.
- When building a "Personal Second Brain" agent that needs to quote your own historical thoughts.

## When not to use it
- If your vault is small or you rely heavily on strict, well-maintained tag/folder structures.
- If you lack the local compute (GPU/RAM) for performant local embedding models.

## Getting started

There are several ways to implement vector search in Obsidian, ranging from plug-and-play community plugins to custom local pipelines.

### Option 1: Smart Connections (Community Plugin)
The most popular "chat with your notes" plugin for Obsidian.
1. Install **Smart Connections** from the Community Plugins gallery.
2. Select an embedding provider:
   - **Local**: Use Ollama (e.g., `nomic-embed-text`) or built-in transformers.
   - **Cloud**: OpenAI, Anthropic, or Cohere.
3. Allow the plugin to index your vault.

### Option 2: Khoj (Self-hosted)
A robust AI assistant that integrates with Obsidian and supports multiple platforms.
1. Run the Khoj server (Docker recommended).
2. Point Khoj to your Obsidian vault directory.

## CLI examples

### 1. Run Khoj with Obsidian Scope
Start the Khoj server and point it specifically to your Obsidian vault for indexing.

```bash
khoj --path ~/Documents/Obsidian/MainVault --index-only
```

### 2. Generate Embeddings with Ollama
Use Ollama to generate a vector for a specific note for testing.

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "'"$(cat ~/Documents/Obsidian/MainVault/Daily/2026-06-12.md)"'"
}'
```

### 3. Use `uvx` for Obsidian MCP
Serve your Obsidian vault as context for Claude Desktop via MCP.

```bash
uvx mcp-server-obsidian --path ~/Documents/Obsidian/MainVault
```

## API examples

### Searching the Khoj API
You can query your indexed Obsidian vault programmatically.

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"q": "How do I automate my home lab?", "n": 5}'
```

### Local Python Indexing (FAISS)
For custom workflows, use the `sentence-transformers` and `faiss` libraries.

```python
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('nomic-embed-text')
vault_path = "/path/to/obsidian/vault"
notes = [os.path.join(vault_path, f) for f in os.listdir(vault_path) if f.endswith('.md')]

# Generate embeddings
documents = [open(n).read() for n in notes]
embeddings = model.encode(documents)

# Index and Search
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype('float32'))

D, I = index.search(np.array(model.encode(["home lab setup"])).astype('float32'), k=3)
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md)
- [Vector DB Comparison](./vector-db-comparison.md)
- [RAG Patterns](patterns/rag.md)
- [Khoj](../tools/intake_storage/khoj.md)
- [Verba](../tools/intake_storage/verba.md)
- [LlamaIndex](../tools/ai_knowledge/llamaindex.md)
- [LocalAI](../tools/infrastructure/localai.md)
- [Ollama](../services/ollama.md)

## Sources / references
- [Obsidian Smart Connections](https://github.com/brianpetro/obsidian-smart-connections)
- [Khoj Documentation](https://docs.khoj.ai/)
- [Anthropic: Long Context Optimization](https://docs.anthropic.com/claude/docs/long-context-window-tips)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
