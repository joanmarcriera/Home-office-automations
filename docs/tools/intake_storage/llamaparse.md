# LlamaParse

## What it is
A specialized PDF parsing service from LlamaIndex designed to extract structured data from complex documents (tables, diagrams, nested layouts). It is a key component for high-fidelity RAG pipelines.

## What problem it solves
Overcomes the limitations of standard PDF text extraction by using vision-aware parsing to maintain document semantics. It ensures that frontier models like **Claude 4.8** and **GPT-5.5** can reason over complex visual data such as multi-column financial reports and technical manuals.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing. It provides the "structural grounding" layer for agents and RAG applications, converting raw PDFs into LLM-optimized Markdown.

## Typical use cases
- **Complex PDF Extraction**: Parsing documents with multi-column layouts, nested tables, and embedded diagrams.
- **Markdown-first RAG**: Converting PDFs directly to high-quality Markdown for [LlamaIndex](../ai_knowledge/llamaindex.md) ingestion.
- **Financial Report Analysis**: Extracting tabular data from annual reports and statements with high fidelity.
- **Agentic Document Processing**: Using the [LlamaParse MCP server](../automation_orchestration/mcp.md) for real-time document understanding in [Claude Desktop](../../knowledge_base/ai_tool_access_matrix.md).

## Strengths
- **Vision-Aware**: Uses advanced vision models to understand document layout better than traditional OCR.
- **Markdown Output**: Optimized for LLMs, preserving hierarchies and table structures in clean Markdown.
- **June 2026 Optimized**: Fully supports **Llama 4 Maverick**'s extended context and [MCP 3.0](../automation_orchestration/mcp.md) integration via `mcp.llamaindex.ai`.
- **Ecosystem Integration**: Seamlessly connects with [LlamaIndex](../ai_knowledge/llamaindex.md) and [LangChain](../ai_knowledge/langchain.md).

## Limitations
- **Cloud Dependency**: Primarily a cloud-based service, which may not suit strictly air-gapped environments.
- **Latency**: High-accuracy vision-based parsing (Agentic tiers) can be slower than simple text extraction.
- **Cost at Scale**: Beyond the free tier, it operates on a credit-based system that can become significant for massive datasets.

## When to use it
- When traditional PDF parsers fail on complex layouts or tables.
- When you want "LLM-ready" Markdown output without manual cleaning.
- When building agentic workflows that require structural document understanding.
- To handle scanned documents or those with poor text layers.

## When not to use it
- For simple, text-only PDFs where `PyPDF2` or `marker` would be faster and cheaper.
- If your data cannot leave your local environment (though local versions are evolving).
- For massive, low-complexity datasets where the credit cost outweighs the layout accuracy benefits.

## Getting started
### Installation
```bash
pip install llama-parse
```

### Basic usage
```python
import os
from llama_parse import LlamaParse

# Set up the parser
parser = LlamaParse(
    api_key="llx-...",  # can also be set via LLAMA_CLOUD_API_KEY env var
    result_type="markdown"
)

# Parse a document
documents = parser.load_data("./my_document.pdf")

# Access the content
for doc in documents:
    print(doc.text)
```

## CLI examples
LlamaParse can be used via the LlamaIndex CLI and integrated into agentic environments.

```bash
# Example of using a LlamaIndex RAG CLI that might use LlamaParse internally
llamaindex-cli rag --files "./data/*.pdf" --parse-tier agentic

# Configure the LlamaParse MCP server for Claude Code (June 2026)
claude mcp add --transport http llamaparse https://mcp.llamaindex.ai/mcp
```

## API examples
The LlamaParse API supports multiple tiers for different accuracy needs.

### Parsing Tiers (June 2026)
| Tier | Best For | Cost (Credits/Page) |
| :--- | :--- | :---: |
| **Fast** | Plain text, single column, no tables. | 0.5 |
| **Cost Effective** | Text with simple tables; clean markdown. | 3 |
| **Agentic** | Scanned pages, multi-column, charts. | 10 |
| **Agentic Plus** | Dense financial reports, mission-critical accuracy. | 45 |

### Advanced Usage (Python)
```python
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key=os.environ["LLAMA_CLOUD_API_KEY"],
    result_type="markdown",
    parsing_instruction="""
    This is a financial report with complex tables.
    Please extract all tables into clear Markdown format,
    ensuring that nested headers are correctly represented.
    """,
    gpt4o_mode=True, # Use frontier vision models for maximum accuracy
    premium_mode=True, # Required for Agentic tiers
)

# Using the sync parser for high-priority documents
documents = parser.load_data("complex_report.pdf")
full_markdown = "\n\n".join([doc.text for doc in documents])
```

## Related tools / concepts
- [Unstructured.io](unstructured.md) — Alternative document partitioning tool.
- [Docling](../process_understanding/docling.md) — Fast local document parser.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — The primary framework for LlamaParse.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architecture utilizing parsed output.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for agent-tool communication (v3.0).
- [Claude 4.8](../providers/anthropic.md) — Recommended model for reasoning over parsed data.
- [GPT-5.5](../ai_knowledge/openai.md) — High-performance alternative for document synthesis.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Local model for processing LlamaParse outputs.

## Sources / references
- [LlamaParse (LlamaIndex)](https://www.llamaindex.ai/llamaparse)
- [LlamaParse API Reference](https://docs.cloud.llamaindex.ai/api-reference)
- [LlamaParse MCP: Agentic OCR tools](https://www.llamaindex.ai/blog/llamaparse-mcp-the-tooling-layer-for-your-document-agents)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
