# Obsidian Vector Search

## What it is
Obsidian Vector Search is the architectural implementation of semantic search and vector-embedding indexing over personal Markdown knowledge bases stored within Obsidian vaults. By converting static Markdown files into dense mathematical vectors (embeddings), users can perform semantic similarity searches that find related ideas, journals, or project notes based on conceptual meaning rather than matching exact keywords.

Key capabilities of the late August 2026 ecosystem include:
- **Local Embedding Pipelines**: Utilizing open-weight embedding models (e.g., `nomic-embed-text` or `bge-large-en-v1.5`) running locally via Ollama to ensure complete data privacy.
- **Unified Personal RAG (Retrieval-Augmented Generation)**: Providing real-time note retrieval to frontier local agents (such as Llama 4 or Gemma 3) or API models (Claude 5.1, GPT-5.5) for personalized synthesis.
- **Pipali v2.0 Desktop Coworker**: A desktop companion application from Khoj that acts as an ambient assistant, automatically indexing Obsidian vaults and executing tasks in the background.
- **Open Paper Research Workbench**: An advanced semantic canvas built for synthesizing scholarly papers and personal research vaults in parallel.
- **Model Context Protocol (MCP 3.1) Support**: Standardized MCP servers that expose your Obsidian vault directly as a secure, real-time context resource to developer workstations.

## What problem it solves
Traditional keyword searches fail when different terms are used to represent identical concepts (e.g., searching for "home automation" will miss notes that only mention "smart home lights"). Furthermore, as personal vaults scale beyond thousands of files, strict hierarchical folders and manual tag structures become impossible to maintain. Vector search bridges this "lexical gap" and uncovers forgotten conceptual connections automatically.

## Where it fits in the stack
**Knowledge Management / RAG Layer**. It acts as the local semantic indexing and retrieval engine that transforms static text vaults into an active long-term memory buffer for AI agents.

## Typical use cases
- **Semantic Concept Synthesis**: Uncovering unexpected connections across years of fragmented journal entries, meeting logs, and technical research.
- **Context-Aware Daily Briefings**: Prompting an assistant to "Summarize everything I have worked on regarding home servers over the past year," retrieving and synthesizing historical details.
- **Desktop Agent Memory**: Exposing personal notes as an active context repository for local coding agents using MCP 3.1.
- **Academic and Research Mapping**: Correlating personal thoughts with crawled scholarly articles using the Open Paper canvas.

## Strengths
- **Complete Privacy**: All embeddings, indexing, and model synthesis can run completely offline on local consumer hardware.
- **Flexible Context Isolation**: Overcomes the need for rigid folder structures or exhaustive tagging strategies.
- **Smarter Discovery**: Locates conceptual matches regardless of language syntax, terminology variations, or minor spelling errors.

## Limitations
- **Chunking Complexity**: Splitting long, disorganized Markdown files into cohesive vector blocks without losing context requires sophisticated parsing rules.
- **Index Synchronization Latency**: Re-indexing must occur regularly as vaults change, requiring background processes to monitor file alterations.
- **Compute Overhead**: Creating embeddings for large vaults (>10,000 files) can trigger high CPU/GPU spikes during initial indexing on standard laptops.

## When to use it
- When your personal Obsidian vault has grown very large (>1,000 notes) and folder/tag navigation has become inefficient.
- When building a privacy-first, local AI assistant or custom RAG pipeline using your personal history as its ground-truth knowledge.
- When you want to expose your notes programmatically to modern AI coding agents using standardized context servers.

## When not to use it
- If your vault is small and you prefer highly organized, manual tagging systems or strict folder hierarchies.
- If your hosting hardware lacks the RAM or GPU acceleration needed to run local embedding models in a responsive manner.

## Getting started

There are three primary methods to integrate vector search into Obsidian, from easy community plugins to completely customizable programmatic pipelines.

### Option 1: Smart Connections (Community Plugin)
The most popular "chat with your notes" plugin for Obsidian.
1. Inside Obsidian, navigate to **Community Plugins** and search for **Smart Connections**.
2. Install and enable the plugin.
3. Configure the **Embedding Provider**:
   - **Local**: Select **Ollama** and specify a running local model (e.g., `nomic-embed-text`).
   - **Cloud**: Input your API key for OpenAI, Anthropic, or Cohere.
4. Let the plugin build its local index file (`.smart-connections/`) in the background.

### Option 2: Khoj Pipali v2.0 (Local Workspace Assistant)
Khoj provides a deep system-level coworker.
1. Download and launch the **Pipali v2.0** desktop assistant.
2. Under workspace directories, add the absolute path to your Obsidian Vault.
3. Pipali will automatically start a background watcher, building semantic embeddings offline.
4. Interact with your vault using the ambient desktop sidebar or hotkeys.

### Option 3: Standard Obsidian MCP Server
Expose your vault as a Model Context Protocol tool for Claude Desktop.
1. Run the official obsidian-mcp server using `uvx`:
   ```bash
   uvx mcp-server-obsidian --path ~/Documents/Obsidian/MainVault
   ```
2. Configure Claude Desktop's `claude_desktop_config.json` file to recognize the server.

## CLI examples
Manage and query your local vector index from your terminal.

### 1. Triggering a Semantic Search Query via Khoj CLI
Query your indexed vault directly from the command line.

```bash
khoj --path ~/Documents/Obsidian/MainVault --query "How do I automate my home lab backup?" --limit 5
```

### 2. Generating Local Embeddings with Ollama
Generate raw vectors for a specific daily note using a local model.

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "'"$(cat ~/Documents/Obsidian/MainVault/Daily/2026-08-31.md)"'"
}'
```

### 3. Incremental Indexing Command
Force a background indexing run specifically for newly modified Markdown documents.

```bash
python3 -m scripts.obsidian_incremental_indexing \
  --vault ~/Documents/Obsidian/MainVault \
  --model nomic-embed-text \
  --force-refresh
```

## API examples
Build a highly custom local semantic retrieval pipeline using Python, FAISS, and sentence-transformers.

### 1. Building a Local Vector Search Engine (Python RAG)
The following script demonstrates how to parse a vault, create semantic embeddings offline, index them using FAISS, and execute queries.

```python
import os
import faiss
import numpy as np
from typing import List
from sentence_transformers import TransformerConfig, SentenceTransformer

# Enable high-speed execution
os.environ["OMP_NUM_THREADS"] = "4"

class ObsidianLocalSearch:
    def __init__(self, vault_path: str, model_name: str = 'nomic-embed-text'):
        self.vault_path = vault_path
        # Load local embedding model (automatically downloads from HuggingFace if missing)
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.documents: List[str] = []
        self.filenames: List[str] = []
        self.index = None

    def load_vault(self):
        """Scans the vault and extracts text blocks from markdown files."""
        for root, _, files in os.walk(self.vault_path):
            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:
                                # In a production script, you would split files into smaller paragraph chunks
                                self.documents.append(content)
                                self.filenames.append(filepath)
                    except Exception as e:
                        print(f"Skipping file {file} due to error: {e}")

    def build_vector_index(self):
        """Generates embeddings and builds a FAISS index."""
        if not self.documents:
            print("No markdown files discovered in vault.")
            return

        print(f"Encoding {len(self.documents)} documents. Please wait...")
        embeddings = self.model.encode(self.documents, show_progress_bar=True)

        # Convert embeddings to float32 numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        dimension = embeddings_array.shape[1]

        # Initialize FAISS IndexFlatL2
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_array)
        print("FAISS index constructed successfully!")

    def query(self, search_text: str, top_k: int = 3):
        """Executes a semantic similarity query over the FAISS index."""
        if self.index is None:
            raise ValueError("Vector index has not been constructed.")

        query_vector = self.model.encode([search_text]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1:
                results.append({
                    "file": self.filenames[idx],
                    "distance": float(dist),
                    "snippet": self.documents[idx][:250] + "..."
                })
        return results

if __name__ == "__main__":
    # Representative usage assuming an existing vault directory
    search_engine = ObsidianLocalSearch(vault_path="/path/to/your/obsidian/vault")
    # search_engine.load_vault()
    # search_engine.build_vector_index()
    # matches = search_engine.query("smart home network setup", top_k=2)
    # for match in matches:
    #     print(f"Match found in: {match['file']} (Score: {match['distance']})")
```

### 2. Searching the Khoj API Programmatically
Query a running Khoj local server to fetch context matches.

```python
import requests

def query_khoj_knowledge_base(query_text: str) -> dict:
    url = "http://localhost:8000/api/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "q": query_text,
        "n": 5
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md)
- [SilverBullet](../tools/intake_storage/silverbullet.md)
- [Anytype](../tools/intake_storage/anytype.md)
- [Vector DB Comparison](./vector-db-comparison.md)
- [RAG Patterns](patterns/rag.md)
- [Khoj](../tools/intake_storage/khoj.md)
- [Verba](../tools/intake_storage/verba.md)
- [LlamaIndex](../tools/ai_knowledge/llamaindex.md)
- [LocalAI](../tools/infrastructure/localai.md)
- [Ollama](../services/ollama.md)

## Sources / references
- [Obsidian Smart Connections Repository](https://github.com/brianpetro/obsidian-smart-connections)
- [Khoj Documentation & Pipali Desktop Guides](https://docs.khoj.ai/)
- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
