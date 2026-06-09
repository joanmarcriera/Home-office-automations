# LlamaParse

## What it is
A specialized PDF parsing service from LlamaIndex designed to extract structured data from complex documents (tables, diagrams, nested layouts). It is a key component for high-fidelity RAG pipelines.

## What problem it solves
Overcomes the limitations of standard PDF text extraction by using vision-aware parsing to maintain document semantics. It ensures that frontier models like **Claude 4.7** and **GPT-5.5** can reason over complex visual data such as multi-column financial reports.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing. It provides the "structural grounding" layer for agents and RAG applications.

## Typical use cases
- **Complex PDF Extraction**: Parsing documents with multi-column layouts, nested tables, and embedded diagrams.
- **Markdown-first RAG**: Converting PDFs directly to high-quality Markdown for [LlamaIndex](../ai_knowledge/llamaindex.md) ingestion.
- **Financial Report Analysis**: Extracting tabular data from annual reports and statements with high fidelity.
- **Agentic Document Processing**: Using the [LlamaParse MCP server](../automation_orchestration/mcp.md) for real-time document understanding in [Claude Desktop](../../knowledge_base/ai_tool_access_matrix.md).

## Strengths
- **Vision-Aware**: Uses advanced vision models to understand document layout better than traditional OCR.
- **Markdown Output**: Optimized for LLMs, preserving hierarchies and table structures in clean Markdown.
- **June 2026 Optimized**: Fully supports **Llama 4 Maverick**'s extended context and [MCP](../automation_orchestration/mcp.md) integration via `mcp.llamaindex.ai`.
- **Ecosystem Integration**: Seamlessly connects with [LlamaIndex](../ai_knowledge/llamaindex.md) and [LangChain](../ai_knowledge/langchain.md).

## Parsing Tiers
LlamaParse offers four tiers that trade off cost, latency, and accuracy:

| Tier | Best For | Cost (Credits/Page) |
| :--- | :--- | :---: |
| **Fast** | Plain text, single column, no tables. | 0.5 |
| **Cost Effective** | Text with simple tables; clean markdown. | 3 |
| **Agentic** | Scanned pages, multi-column, charts. | 10 |
| **Agentic Plus** | Dense financial reports, mission-critical accuracy. | 45 |

## Limitations
- **Cloud Dependency**: Primarily a cloud-based service, which may not suit air-gapped environments.
- **Latency**: High-accuracy vision-based parsing can be slower than simple text extraction.
- **Cost at Scale**: Beyond the free tier, it operates on a credit-based system that can become significant for massive datasets.

## When to use it
- When traditional PDF parsers fail on complex layouts or tables.
- When you want "LLM-ready" Markdown output without manual cleaning.
- When you are building agentic workflows that require structural document understanding.

## When not to use it
- For simple, text-only PDFs where `PyPDF2` or `marker` would be faster and cheaper.
- If your data cannot leave your local environment (though local versions are evolving).

## Licensing and cost
- **Open Source**: No (Proprietary service)
- **Cost**: Freemium (1,000 pages per month free)
- **Self-hostable**: Limited (Docker image available for enterprise)

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

### Agentic Tier Example (Vision-Aware Parsing)
The agentic tier uses advanced reasoning to handle messy layouts and tables.

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
    gpt4o_mode=True, # Use GPT-4o vision for maximum accuracy
    premium_mode=True, # Required for Agentic tiers
)

# Using the sync parser for high-priority documents
documents = parser.load_data("complex_report.pdf")
full_markdown = "\n\n".join([doc.text for doc in documents])

with open("output.md", "w") as f:
    f.write(full_markdown)
```

## CLI examples
```bash
# Example of using a LlamaIndex RAG CLI that might use LlamaParse internally
llamaindex-cli rag --files "./data/*.pdf" --parse-tier agentic

# Configure the LlamaParse MCP server for Claude Code (June 2026)
claude mcp add --transport http llamaparse https://mcp.llamaindex.ai/mcp
```

## API examples
```bash
# Create a parse job using the REST API (v2)
curl -X POST 'https://api.cloud.llamaindex.ai/api/v2/parse' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \
  --data '{
    "file_id": "cafe1337-e0dd-4762-b5f5-769fef112558",
    "tier": "agentic",
    "version": "latest"
  }'

# Retrieve results (Markdown)
curl 'https://api.cloud.llamaindex.ai/api/v2/parse/{job_id}?expand=markdown' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"

# List completed jobs
curl 'https://api.cloud.llamaindex.ai/api/v2/parse?page_size=10&status=COMPLETED' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"
```

## Related tools / concepts

- [Unstructured.io](unstructured.md)
- [Docling](../process_understanding/docling.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude 4.7](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)

## Sources / references
- [LlamaParse (LlamaIndex)](https://www.llamaindex.ai/llamaparse)
- [LlamaParse API Reference](https://docs.cloud.llamaindex.ai/api-reference)
- [LlamaParse MCP: Agentic OCR tools](https://www.llamaindex.ai/blog/llamaparse-mcp-the-tooling-layer-for-your-document-agents)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
