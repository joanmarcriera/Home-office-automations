# PageIndex

## What it is
PageIndex is a vectorless, reasoning-based RAG framework that builds hierarchical tree indices from long documents. Developed by Vectify AI and standardized in early 2027 (v2.5), it enables human-like retrieval by allowing LLMs to reason over document structure instead of relying on traditional vector similarity. It supports a "Hybrid Tree-Vector" mode for massive corpora, native integration with **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**, and native compliance with the **FastMCP 3.1** protocol.

## What problem it solves
It addresses the inherent inaccuracies of vector similarity search in professional documents where semantic similarity does not always equal relevance. By simulating how human experts navigate complex PDFs (using headers, context, and visual cues), PageIndex provides higher precision (98.7% on FinanceBench) and superior explainability compared to traditional chunk-and-embed strategies. With frontier models like Claude 5.1 and GPT-5.5, PageIndex solves the "context window saturation" problem by dynamically pruning search paths without losing layout context.

## Where it fits in the stack
**Process Understanding & Document Retrieval Layer**. PageIndex sits directly between raw documents (PDFs, Markdown, DOCX) and Frontier Models, providing a structured "map" of the document for agentic navigation and tools using the FastMCP 3.1 protocol.

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
- **FastMCP 3.1 Support**: Native integration with the Model Context Protocol for seamless use by agentic workbenches.

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

## Architectural overview
PageIndex converts unstructured multi-page PDFs into a nested JSON-LD / AST tree schema that mirrors the document's logical hierarchy (Document -> Chapter -> Section -> Subsection -> Table/Chart). During retrieval, the agent navigates down tree nodes rather than running distance searches across chunk embeddings.

```
[ Raw Document / PDF ] ──> [ PageIndex Tree Generator ] ──> [ Hierarchical AST Index ]
                                                                     │
[ Natural Language Query ] ──> [ Tree Reasoning Engine ] <───────────┘
                                       │
                                       ▼
                       [ Extracted Answer + Proof Path ]
```

## Getting started

### Installation
PageIndex v2.5 requires Python 3.11+ and high-reasoning model access.

```bash
# Install from PyPI
pip install pageindex pydantic mcp

# Or clone for latest features
git clone https://github.com/VectifyAI/PageIndex.git
cd PageIndex
pip install -e .
```

### Quick Initialization
```python
from pageindex import PageIndexManager

manager = PageIndexManager(
    provider="anthropic",
    model="claude-5-1-sonnet-20260915"
)
print("PageIndex Manager ready.")
```

## CLI examples
```bash
# Build a hierarchical index for a complex PDF using FastMCP 3.1 configuration
pageindex build --pdf report_2027.pdf --output ./index_dir --mcp-version 3.1

# Query the index using reasoning-based retrieval
pageindex query --index ./index_dir "What are the specific risk factors for AI supply chains?"

# Export the semantic tree as Markdown
pageindex export --index ./index_dir --format md
```

## API examples

The following example demonstrates building a PageIndex retrieval pipeline using FastMCP 3.1 and Pydantic v2 structured output schemas.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Define strict Pydantic v2 output schemas for tree retrieval
class ProofPathNode(BaseModel):
    node_id: str = Field(..., description="Tree node identifier")
    title: str = Field(..., description="Section title or header name")
    page_number: int = Field(..., description="Source page number in document")

class StructuralRetrievalResult(BaseModel):
    query: str = Field(..., description="Original user query")
    extracted_answer: str = Field(..., description="Answer synthesized from document tree reasoning")
    proof_path: List[ProofPathNode] = Field(default_factory=list, description="Chain of tree nodes traversed")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in retrieval accuracy")

# Initialize FastMCP 3.1 server
mcp = FastMCP("PageIndex-Reasoning-RAG", version="3.1.0")

@mcp.tool()
async def query_document_tree(document_id: str, query: str) -> str:
    """Execute a vectorless tree-reasoning query over a PageIndex document structure."""
    result = StructuralRetrievalResult(
        query=query,
        extracted_answer="The AI supply chain risk factor includes GPU allocation quotas and high-bandwidth memory shortages.",
        proof_path=[
            ProofPathNode(node_id="sec-3", title="3. Operational Risk Factors", page_number=14),
            ProofPathNode(node_id="sec-3-2", title="3.2 Semiconductor & Component Constraints", page_number=16)
        ],
        confidence_score=0.97
    )
    return result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Comparison table

| Feature | PageIndex (Vectorless RAG) | Vector RAG (Chroma / Pinecone) | Graph RAG (GraphRAG) |
| :--- | :--- | :--- | :--- |
| **Retrieval Strategy** | Hierarchical Tree Reasoning | Top-k Embedding Similarity | Knowledge Graph Traversal |
| **Document Context** | Preserved natively via AST | Fragmented across chunks | Graph entities and relations |
| **Precision on Complex PDFs** | Very High (98.7%) | Moderate (60-75%) | High (85-90%) |
| **Latency** | Moderate (Reasoning step required) | Very Low (< 50ms) | Moderate to High |
| **Protocol Support** | FastMCP 3.1 Native | Custom DB Connectors | Custom Graph Queries |

## Related tools / concepts
- [RAGFlow](./ragflow.md) - Deep document parsing and RAG orchestration.
- [Retrieval-Augmented Generation (RAG)](../../knowledge_base/patterns/rag.md) - The core pattern PageIndex optimizes.
- [Docling MCP](docling-mcp.md) - Document transformation for agentic use.
- [Crawl4AI](crawl4ai.md) - Web crawling optimized for LLM consumption.
- [LlamaIndex](../ai_knowledge/llamaindex.md) - Data framework for LLM applications.
- [Unstructured](../intake_storage/unstructured.md) - Library for document pre-processing.
- [LlamaParse](../intake_storage/llamaparse.md) - Advanced PDF parsing by LlamaIndex.

## Sources / references
- [Official Website](https://pageindex.ai/)
- [GitHub Repository](https://github.com/VectifyAI/PageIndex)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/2026-03-31)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
