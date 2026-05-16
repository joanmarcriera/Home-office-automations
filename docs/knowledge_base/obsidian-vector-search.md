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

## Getting started

There are several ways to implement vector search in Obsidian, ranging from plug-and-play community plugins to custom local pipelines.

### Option 1: Smart Connections (Community Plugin)
The most popular "chat with your notes" plugin for Obsidian.
1. Install **Smart Connections** from the Community Plugins gallery.
2. Select an embedding provider:
   - **Local**: Use Ollama (e.g., `nomic-embed-text`) or built-in transformers.
   - **Cloud**: OpenAI, Anthropic, or Cohere.
3. Allow the plugin to index your vault (stored in `.obsidian/plugins/smart-connections/`).
4. Use the sidebar to ask questions or find "Smart Links" to related notes.

### Option 2: Khoj (Self-hosted)
A more robust, cross-platform AI assistant that integrates with Obsidian.
1. Run the Khoj server (Docker recommended).
2. Point Khoj to your Obsidian vault directory.
3. Khoj creates a vector index and provides a search interface/API that can be accessed via the Khoj Obsidian plugin.

## Technical implementation (Local Pipeline)

For maximum control, you can build a local indexing pipeline using Python and a vector database.

```python
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Load model and notes
model = SentenceTransformer('all-MiniLM-L6-v2')
vault_path = "/path/to/your/obsidian/vault"
notes = [os.path.join(vault_path, f) for f in os.listdir(vault_path) if f.endswith('.md')]

def load_content(path):
    with open(path, 'r') as f:
        return f.read()

# 2. Generate Embeddings
documents = [load_content(n) for n in notes]
embeddings = model.encode(documents)

# 3. Create FAISS Index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

# 4. Search
query = "How do I set up a home lab?"
query_vector = model.encode([query])
D, I = index.search(np.array(query_vector).astype('float32'), k=5)

print("Top related notes:")
for idx in I[0]:
    print(f"- {notes[idx]}")
```

## Related tools / concepts
- [Obsidian](../../tools/ai_knowledge/obsidian.md)
- [Vector DB Comparison](./vector-db-comparison.md)
- [RAG Patterns](../patterns/rag.md)
- [Khoj](../../tools/ai_knowledge/khoj.md)
- [Verba](../../tools/ai_knowledge/verba.md)
- [LlamaIndex](../../tools/ai_knowledge/llamaindex.md)
- [LocalAI](../../tools/ai_knowledge/localai.md)
- [Ollama](../../tools/ai_knowledge/ollama.md)

## Sources / references
- [Obsidian-Vibe GitHub](https://github.com/vibe/obsidian-vibe)
- [Embedding Obsidian Notes (Blog)](https://simonwillison.net/2023/Oct/23/embeddings/)

## Contribution Metadata
- Last reviewed: 2026-05-16
- Confidence: high
