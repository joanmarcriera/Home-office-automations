# PageIndex

## What it is
PageIndex is a vectorless, reasoning-based RAG framework that builds hierarchical tree indices from long documents. Developed by Vectify AI, it enables human-like retrieval by allowing LLMs to reason over document structure instead of relying on traditional vector similarity. As of late September 2026 (v2.2), it supports a "Hybrid Tree-Vector" mode for massive corpora, native integration with Claude 5.1 and GPT-5.5, and compliance with the Model Context Protocol (MCP 3.1) standard.

## What problem it solves
It addresses the inherent inaccuracies of vector similarity search in professional documents where semantic similarity does not always equal relevance. By simulating how human experts navigate complex PDFs (using headers, context, and visual cues), PageIndex provides higher precision (98.7% on FinanceBench) and superior explainability compared to traditional chunk-and-embed strategies. In September 2026, with the arrival of frontier models like Llama 4 and Gemini 3.5, PageIndex solves the "context window saturation" problem by dynamically pruning search paths without losing layout context.

## Where it fits in the stack
PageIndex sits in the **Process Understanding** and **Retrieval** layer. It acts as an intelligent middleware between raw documents (PDFs, Markdown) and Frontier Models, providing a structured "map" of the document for agentic navigation and tools using the MCP 3.1 protocol.

## Typical use cases
- **Complex Financial Analysis**: Analyzing SEC filings, audit reports, or insurance policies with dense nested sections.
- **Multimodal Document RAG**: Navigating documents where charts, tables, and page layouts are critical for understanding.
- **Long-Context Management**: Handling documents exceeding 2M tokens by using a semantic "Table of Contents" tree to prune search paths.
- **Explainable Retrieval**: Providing exact reasoning steps and structural references for every retrieved fragment in compliance-driven industries.

## Strengths
- **No Vector DB Required**: Operates directly on semantic tree structures, eliminating embedding drift and database overhead.
- **Preserves Context**: Maintains the natural document hierarchy, preventing the "lost in the middle" problem of arbitrary chunking.
- **Superior Precision**: State-of-the-art performance on domain-specific benchmarks (FinanceBench, PolicyBench).
- **Vision-Native**: Uses vision-aware LLMs (such as Claude 5.1 and GPT-5.5) to "see" document layouts, charts, and diagrams during retrieval.
- **MCP 3.1 Support**: Native integration with the Model Context Protocol for seamless use by agentic workbenches.

## Limitations
- **High Reasoning Latency**: Multiple LLM calls for tree navigation result in higher latency than simple vector lookups.
- **Operational Cost**: Increased token consumption due to the iterative reasoning steps required for structural navigation.
- **Model Sensitivity**: Requires high-reasoning models (Claude 5.1, GPT-5.5, Llama 4) for optimal performance.

## When to use it
- When retrieval precision is more important than millisecond latency.
- When working with high-value, structured professional documents (Legal, Finance, Engineering).
- When you need a "Self-Correction" loop where the agent can re-navigate the document if the first answer is insufficient.

## When not to use it
- For high-volume, low-latency applications (e.g., real-time customer support chat on simple FAQs).
- When the document corpus consists of unstructured "brain dumps" with no internal hierarchy.
- For extremely large collections where initial tree generation cost is prohibitive without the Hybrid mode.

## Getting started

### Installation
PageIndex v2.2 requires Python 3.12+ and high-reasoning model access.

```bash
# Install from PyPI
pip install pageindex

# Or clone for latest features
git clone https://github.com/VectifyAI/PageIndex.git
cd PageIndex
pip install -e .
```

### Initial Setup
```python
from pageindex import PageIndexManager

# Initialize with vision-aware provider
manager = PageIndexManager(
    provider="anthropic",
    model="claude-5-1-sonnet-20260915"
)
```

## CLI examples
```bash
# Build a hierarchical index for a complex PDF using MCP 3.1 configuration
pageindex build --pdf report_2026.pdf --output ./index_dir --mcp-version 3.1

# Query the index using reasoning-based retrieval
pageindex query --index ./index_dir "What are the specific risk factors for AI supply chains?"

# Export the semantic tree as Markdown
pageindex export --index ./index_dir --format md
```

## API examples
PageIndex provides a unified Python API and an MCP server.

### Basic Retrieval API
```python
import pageindex

# Load index and query with reasoning
idx = pageindex.load("./my_index")
result = idx.navigate(
    query="Extract all data points from the ESG chart on page 42.",
    max_depth=3,
    mcp_compliant=True
)

print(result.answer)
print(result.reasoning_path) # Shows the tree nodes visited
```

### MCP 3.1 Configuration (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "pageindex": {
      "command": "npx",
      "args": ["-y", "@vectify/pageindex-mcp@latest"],
      "env": {
        "PAGEINDEX_API_KEY": "YOUR_KEY",
        "ANTHROPIC_API_KEY": "YOUR_KEY",
        "MCP_PROTOCOL_VERSION": "3.1"
      }
    }
  }
}
```

## Related tools / concepts
- [RAGFlow](./ragflow.md) - Deep document parsing and RAG orchestration.
- [Retrieval-Augmented Generation (RAG)](../../knowledge_base/patterns/rag.md) - The core pattern PageIndex optimizes.
- [Docling MCP](docling-mcp.md) - Document transformation for agentic use.
- [Crawl4AI](crawl4ai.md) - Web crawling optimized for LLM consumption.
- [LlamaIndex](../ai_knowledge/llamaindex.md) - Data framework for LLM applications.
- [Unstructured](../intake_storage/unstructured.md) - Library for document pre-processing.
- [LlamaParse](../intake_storage/llamaparse.md) - Advanced PDF parsing by LlamaIndex.
- [Agentic RAG](../../knowledge_base/patterns/rag.md#agentic-rag) - The paradigm of using agents for iterative retrieval.

## Sources / references
- [Official Website](https://pageindex.ai/)
- [GitHub Repository](https://github.com/VectifyAI/PageIndex)
- [Vectify AI Blog: Reasoning over Structure](https://pageindex.ai/blog/reasoning-vs-vectors)
- [PageIndex v2.2 Release Notes](https://github.com/VectifyAI/PageIndex/releases/tag/v2.2.0)

## Contribution Metadata
- Last reviewed: 2026-09-24
- Confidence: high
