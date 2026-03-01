# PageIndex

## What it is
PageIndex is a vectorless, reasoning-based RAG framework that builds hierarchical tree indices from long documents. It enables human-like retrieval by allowing LLMs to reason over document structure instead of relying on traditional vector similarity.

## What problem it solves
It addresses the inaccuracies of vector similarity search in professional documents where semantic similarity does not always equal relevance. By simulating how human experts navigate complex PDFs, PageIndex provides higher precision (98.7% on FinanceBench) and better explainability for domain-specific retrieval.

## Where it fits in the stack
**Tool / Agent**: It acts as a specialized retrieval tool and an agentic framework for document navigation.

## Typical use cases
- **Professional Analysis**: Analyzing SEC filings, insurance policies, or dense textbooks where precise section retrieval is required.
- **Tree-based Navigation**: Managing very long documents that exceed standard context limits by navigating a semantic "Table of Contents" tree.
- **Vision-based Retrieval**: Performing RAG directly on page images for documents where OCR is unreliable or layouts are highly visual.

## Strengths
- **No Vector DB Required**: Eliminates the overhead and performance bottlenecks of vector indices.
- **No Artificial Chunking**: Preserves natural document hierarchy and context.
- **High Explainability**: Retrieval steps are based on explicit reasoning and provide clear references.
- **Superior Accuracy**: State-of-the-art performance on benchmarks like FinanceBench.

## Limitations
- **LLM Cost/Latency**: Heavy reliance on multiple LLM reasoning calls can increase operational costs and latency.
- **Model Optimization**: Currently primarily optimized for high-end models like GPT-4o.

## When to use it
- When working with high-value professional documents where retrieval precision is paramount.
- When you need traceable, interpretable evidence for model answers.
- When document structure (headings, sections) is a strong signal for relevance.

## When not to use it
- For simple semantic searches where "vibe-based" retrieval is sufficient.
- When extremely low latency is required for a massive number of concurrent queries.

## Related tools / concepts
- [RAGFlow](./ragflow.md)
- [Retrieval-Augmented Generation (RAG)](../../knowledge_base/README.md)

## Sources / references
- [Official Website](https://pageindex.ai/)
- [GitHub Repository](https://github.com/VectifyAI/PageIndex)
- [PageIndex Framework Introduction](https://pageindex.ai/blog/pageindex-intro)


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01