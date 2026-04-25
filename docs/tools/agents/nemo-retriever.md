# NVIDIA NeMo Retriever

## What it is
NVIDIA NeMo Retriever is a generative AI microservice that lets organizations connect their custom data to large language models (LLMs) to deliver highly accurate responses for AI applications using Retrieval-Augmented Generation (RAG).

## What problem it solves
It addresses the limitations of standard dense retrieval by providing an "agentic retrieval pipeline" that uses a reasoning loop (ReACT architecture) to iteratively search, evaluate, and refine results. It bridges the gap between retrievers that sift through millions of documents and LLMs that provide deep reasoning.

## Where it fits in the stack
**Category**: Agents / Retrieval

## Typical use cases
- **Enterprise RAG**: High-accuracy retrieval over diverse, non-curated enterprise datasets.
- **Complex Document Search**: Parsing and reasoning over visually rich documents (e.g., PDFs with charts and tables).
- **Multi-step Reasoning**: Queries that require breaking down into simpler sub-queries.

## Strengths
- **Generalizability**: Dynamically adapts its search strategy to the data without requiring architectural changes.
- **Top Performance**: Secured #1 spot on ViDoRe v3 pipeline leaderboard and #2 on BRIGHT leaderboard.
- **Scale and Speed**: Uses thread-safe singleton retrievers in-process to minimize overhead compared to standard MCP-based architectures.

## Limitations
- **Cost and Latency**: Agentic retrieval is more token-intensive and slower than standard dense retrieval due to the iterative reasoning loop.
- **Resource Intensive**: Benefits significantly from high-end GPUs (e.g., A100/H100).

## When to use it
- When high-stakes, complex queries require maximum accuracy.
- When dealing with multi-domain data that semantic similarity alone cannot handle.

## When not to use it
- For simple keyword-based or semantic searches where low latency is critical.
- When compute costs are a primary constraint.

## Related tools / concepts
- [NVIDIA NeMo](../frameworks/index.md)
- [RAG](../../knowledge_base/patterns/rag.md)
- [ViDoRe (Visual Document Retrieval Benchmark)](../benchmarking/index.md)
- [BRIGHT Benchmark](../benchmarking/vakra.md)

## Sources / References
- [Beyond Semantic Similarity: Introducing NVIDIA NeMo Retriever’s Generalizable Agentic Retrieval Pipeline](https://huggingface.co/blog/nvidia/nemo-retriever-agentic-retrieval)
- [Official NeMo Retriever Library](https://github.com/NVIDIA/NeMo-Retriever)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: high
