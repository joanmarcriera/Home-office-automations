# Retrieval-Augmented Generation (RAG)

## What it is
Retrieval-Augmented Generation (RAG) is an architectural pattern that optimizes the output of a Large Language Model (LLM) by referencing an authoritative knowledge base outside of its training data before generating a response. In June 2026, RAG has evolved into **Agentic RAG**, where models use [Tool Calling](tool-calling-and-mcp.md) to dynamically plan and execute multi-step retrieval strategies across heterogeneous data sources.

## What problem it solves
It bridges the gap between the generative power of LLMs and the need for factual, up-to-date, and private information.
- **Hallucination Reduction**: Grounding models in retrieved facts significantly reduces incorrect "plausible-sounding" generation.
- **Knowledge Freshness**: Enables access to real-time data (e.g., stock prices, news) without the cost of retraining.
- **Explainability**: RAG systems provide citations, enabling users to verify the source of information.
- **Data Sovereignty**: Allows general-purpose models to reason over private datasets (e.g., company wikis, legal archives) without exposing that data during the model training phase.

## Where it fits in the stack
RAG is a core **Reasoning Engine** pattern. It sits between the raw **Infrastructure/Models** (Layer 0-2) and the **Orchestration/Frameworks** (Layer 5-6) that implement the retrieval logic. It is often the primary mechanism for [Personal AI Assistants](../../knowledge_base/self-healing-agent-research.md) to access user-specific context.

## Typical use cases
- **Personal Knowledge Management**: Querying a private library of notes, emails, and documents (e.g., via [NotebookLM](../../tools/ai_knowledge/notebooklm.md)).
- **Technical Support**: Answering complex configuration questions based on product manuals and GitHub issues.
- **Automated Financial Analysis**: Reasoning over real-time market data and historical earnings reports.
- **Legal & Compliance**: Searching through vast repositories of contracts and regulations to identify specific clauses or risks.
- **Medical Diagnostics Support**: Referencing the latest clinical research and patient history in a secure, RAG-grounded environment.

## Strengths
- **Factual Reliability**: High accuracy for knowledge-intensive tasks compared to base LLMs.
- **Resource Efficiency**: Updating a vector database is orders of magnitude cheaper than fine-tuning a model.
- **Transparency**: Citations and "source-grounding" increase user trust and auditability.
- **Flexibility**: Can be easily adapted to new domains by swapping the underlying document store.

## Limitations
- **Retrieval Fragility**: The answer is only as good as the retrieved chunks ("Garbage In, Garbage Out").
- **Latency**: The retrieval, re-ranking, and context-augmentation steps add time to the overall response.
- **Context Window Management**: Despite RAG, models still have limits on how much retrieved context they can effectively process in a single turn.
- **Semantic Drift**: Vector search can occasionally retrieve semantically similar but factually irrelevant "noise."

## When to use it
- When the model needs access to private, proprietary, or rapidly changing information.
- When factual accuracy and citation of sources are mandatory requirements.
- When you need to scale knowledge access to millions of documents without fine-tuning costs.
- When building [Agentic Workflows](agentic-workflows.md) that require long-term memory.

## When not to use it
- For purely creative writing (fiction, poetry) where external facts are unnecessary.
- When the entire dataset fits within a frontier model's massive context window (e.g., Gemini 3.5 Pro's 10M tokens) and cost is not a primary constraint.
- When sub-100ms latency is required for a simple, non-factual interaction.
- When the LLM's base training data is already sufficient and up-to-date for the task.

## Getting started

### Minimal Agentic RAG Setup (Python)
In 2026, [Smolagents](../../tools/frameworks/smolagents.md) is a popular way to build lightweight Agentic RAG.

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# 1. Define the agent with a search tool (Retrieval)
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel()
)

# 2. Run the agentic retrieval loop
response = agent.run("What is the current status of the MCP 3.0 specification?")
print(response)
```

### Local RAG with Ollama and LlamaIndex
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

# Setup local models
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)

# Load data and index
documents = SimpleDirectoryReader("./my_docs").load_data()
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
print(query_engine.query("Summarize the Q2 highlights."))
```

## CLI examples

### Indexing a Directory
Using the `ragflow-cli` (v2026.5) to prepare a knowledge base:

```bash
# Parse and index all PDFs in a directory with layout awareness
ragflow-cli index --path ./manuals --parser deepdoc --output-collection manuals_v1
```

### Testing Retrieval Quality
```bash
# Query the vector store directly and view top-K similarity scores
ragflow-cli search --query "How do I reset the device?" --collection manuals_v1 --top-k 5
```

## API examples

### Contextual Retrieval (Anthropic SDK)
Prepending situational context to chunks to improve retrieval accuracy.

```python
import anthropic

client = anthropic.Anthropic()

# Every chunk is augmented with its position in the larger document
contextual_chunk = """
<situational_context>
This chunk is from the 'Troubleshooting' section of the 'Model X' manual, specifically discussing battery issues.
</situational_context>
To reset the battery, hold the power button for 15 seconds until the LED flashes red.
"""

# Embed the contextualized chunk...
```

### Hybrid Search with Weaviate (MCP)
```python
import weaviate

client = weaviate.connect_to_local()
collection = client.collections.get("Manuals")

# Combine vector search with keyword (BM25) search
result = collection.query.hybrid(
    query="battery reset",
    alpha=0.5, # Balance between vector and keyword
    limit=3
)
```

## Related tools / concepts
- [Agentic RAG](data-copilot-agentic-rag.md) — Multi-step retrieval and reasoning.
- [Tool Calling & MCP](tool-calling-and-mcp.md) — The mechanism for agent-driven retrieval.
- [RAGFlow](../../tools/process_understanding/ragflow.md) — Vision-native knowledge engine.
- [ColQwen](../../tools/ai_knowledge/colqwen.md) — Multi-modal RAG using late interaction.
- [Docling](../../tools/process_understanding/docling.md) — High-fidelity document parsing for RAG.
- [Vector Databases](../../tools/infrastructure/index.md#sub-categories) — The storage layer for RAG.
- [GraphRAG](../../knowledge_base/patterns/agentic-workflows.md) — RAG using knowledge graphs for global context.
- [Self-Healing Agents](../../knowledge_base/self-healing-agent-research.md) — Using RAG for autonomous system remediation.

## Sources / references
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401)
- [Anthropic: Contextual Retrieval Guide (2025)](https://www.anthropic.com/news/contextual-retrieval)
- [IBM Research: The Evolution of Agentic RAG (2026)](https://research.ibm.com/blog/evolution-agentic-rag)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
