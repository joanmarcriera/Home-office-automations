# LlamaParse

## What it is
LlamaParse is a specialized PDF parsing service from LlamaIndex designed to extract structured data from complex documents (tables, diagrams, nested layouts). It is a key component for high-fidelity RAG pipelines. As of June 2026, it is the standard for vision-aware document ingestion. It is a proprietary service (freemium) but offers an Enterprise Docker version for self-hosting.

## What problem it solves
It overcomes the limitations of standard PDF text extraction by using vision-aware parsing to maintain document semantics. It ensures that frontier models like **Claude 4.8 Opus** and **GPT-5.5** can reason over complex visual data such as multi-column financial reports, which typically "break" with traditional OCR.

## Where it fits in the stack
**Category**: Intake & Storage / Data Processing. It provides the "structural grounding" layer for agents and RAG applications, sitting between raw document storage and the vector database.

## Typical use cases
- **Complex PDF Extraction**: Parsing documents with multi-column layouts, nested tables, and embedded diagrams.
- **Markdown-first RAG**: Converting PDFs directly to high-quality Markdown for [LlamaIndex](../ai_knowledge/llamaindex.md) ingestion.
- **Financial Report Analysis**: Extracting tabular data from annual reports with tiered precision levels (Fast, Agentic, Agentic Plus).
- **Agentic Document Processing**: Using the [LlamaParse MCP server](../automation_orchestration/mcp.md) for real-time document understanding in [Claude Desktop](../../knowledge_base/ai_tool_access_matrix.md).

## Strengths
- **Vision-Aware**: Uses advanced vision models to understand document layout better than traditional OCR.
- **Markdown Output**: Optimized for LLMs, preserving hierarchies and table structures in clean Markdown.
- **Tiered Precision**: Offers multiple processing tiers (Fast to Agentic Plus) to balance cost, latency, and accuracy.
- **June 2026 Optimized**: Fully supports **Llama 4 Maverick**'s extended context and [MCP 3.0](../automation_orchestration/mcp.md) integration.
- **Ecosystem Integration**: Seamlessly connects with [LlamaIndex](../ai_knowledge/llamaindex.md) and [LangChain](../ai_knowledge/langchain.md).

## Limitations
- **Cloud Dependency**: Primarily a cloud-based service, which may not suit strictly air-gapped environments.
- **Latency**: High-accuracy "Agentic Plus" vision-based parsing can be slower than simple text extraction.
- **Cost at Scale**: Beyond the free tier (1,000 pages/month), the credit-based system can become expensive for massive datasets.

## When to use it
- When traditional PDF parsers fail on complex layouts or tables.
- When you want "LLM-ready" Markdown output without manual cleaning.
- When you are building agentic workflows that require structural document understanding.
- When utilizing **Claude 4.8** or **GPT-5.5** for high-fidelity document reasoning.

## When not to use it
- For simple, text-only PDFs where `PyPDF2` or `marker` would be faster and cheaper.
- If your data cannot leave your local environment (though enterprise self-hosting is available).
- For simple note-taking apps that don't require high-precision table extraction.

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
The agentic tier uses advanced reasoning to handle messy layouts.

```python
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key=os.environ["LLAMA_CLOUD_API_KEY"],
    result_type="markdown",
    parsing_instruction="Extract all financial tables accurately.",
    gpt4o_mode=True, # Use GPT-4o vision for maximum accuracy
    premium_mode=True, # Required for Agentic tiers
)

documents = parser.load_data("complex_report.pdf")
```

## CLI examples
LlamaParse can be integrated into CLI workflows and used via MCP 3.0.

### MCP 3.0 Configuration
```bash
# Configure the LlamaParse MCP server for Claude Code (June 2026)
claude mcp add --transport http llamaparse https://mcp.llamaindex.ai/mcp
```

### LlamaIndex CLI
```bash
# Using a LlamaIndex RAG CLI with LlamaParse tiering
llamaindex-cli rag --files "./data/*.pdf" --parse-tier agentic
```

## API examples
LlamaParse offers a robust REST API (v2) for asynchronous document processing.

### Create a Parse Job
```bash
curl -X POST 'https://api.cloud.llamaindex.ai/api/v2/parse' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \
  --data '{
    "file_id": "cafe1337-e0dd-4762-b5f5-769fef112558",
    "tier": "agentic",
    "version": "latest"
  }'
```

### Retrieve Results
```bash
curl 'https://api.cloud.llamaindex.ai/api/v2/parse/{job_id}?expand=markdown' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY"
```

## Related tools / concepts
- [Unstructured](unstructured.md) — Multi-format document partitioning library.
- [Docling](../process_understanding/docling.md) — High-performance PDF parsing alternative.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Primary ecosystem for LlamaParse.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Underlying architectural concept for document retrieval.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Used for real-time document tool access.
- [Claude](../ai_knowledge/claude.md) — Recommended frontier model for reasoning over LlamaParse output.
- [GPT-5.5](../ai_knowledge/openai.md) — Supported frontier model for document analysis.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Local model optimized for structural grounding.

## Sources / references
- [LlamaParse (LlamaIndex)](https://www.llamaindex.ai/llamaparse)
- [LlamaParse API Reference](https://docs.cloud.llamaindex.ai/api-reference)
- [LlamaParse MCP: Agentic OCR tools](https://www.llamaindex.ai/blog/llamaparse-mcp-the-tooling-layer-for-your-document-agents)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
