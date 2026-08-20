# LlamaParse

## What it is
A specialized PDF and document parsing service from LlamaIndex designed to extract structured data from complex documents (tables, diagrams, nested layouts). It is a key component for high-fidelity RAG pipelines and agentic knowledge operations.

## What problem it solves
Overcomes the limitations of standard PDF text extraction by using vision-aware parsing to maintain document semantics. It ensures that frontier models like **Claude 5.1** and **GPT-5.5** can reason over complex visual data such as multi-column financial reports, technical manuals, and complex architectural schematics.

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
- **FastMCP 3.1 Optimized**: Fully supports **Llama 4**'s extended context and [MCP 3.1](../automation_orchestration/mcp.md) integration via `mcp.llamaindex.ai` (Standard 3.1).
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
# Example of using a LlamaIndex RAG CLI that uses LlamaParse
llamaindex-cli rag --files "./data/*.pdf" --parse-tier agentic

# Configure the LlamaParse MCP server for Claude Code (FastMCP 3.1)
claude mcp add --transport http llamaparse https://mcp.llamaindex.ai/mcp
```

## API examples
The LlamaParse API supports multiple tiers for different accuracy needs. Programmatic inputs should be validated via **Pydantic v2**.

### Parsing Tiers (Early 2027 SOTA)
| Tier | Best For | Cost (Credits/Page) |
| :--- | :--- | :---: |
| **Fast** | Plain text, single column, no tables. | 0.5 |
| **Cost Effective** | Text with simple tables; clean markdown. | 3 |
| **Agentic** | Scanned pages, multi-column, charts. | 10 |
| **Agentic Plus** | Dense financial reports, mission-critical accuracy. | 45 |

### Advanced Usage and Payload Validation (Python)
```python
import os
from pydantic import BaseModel, Field
from typing import Optional
from llama_parse import LlamaParse

# Define Pydantic v2 validation schema for parser configuration parameters
class LlamaParseConfig(BaseModel):
    api_key: str = Field(..., min_length=5, description="The Llama Cloud API key starting with llx-")
    result_type: str = Field(default="markdown", pattern="^(markdown|text)$")
    parsing_instruction: Optional[str] = Field(default=None)
    gpt4o_mode: bool = Field(default=True, description="Enables frontier vision models")
    premium_mode: bool = Field(default=True, description="Required for advanced agentic parsing tiers")

# Raw payload dictionary
config_data = {
    "api_key": os.environ.get("LLAMA_CLOUD_API_KEY", "llx-dummy-key-for-validation"),
    "result_type": "markdown",
    "parsing_instruction": "This is a financial report with complex tables. Please extract all tables into Markdown.",
    "gpt4o_mode": True,
    "premium_mode": True
}

try:
    # Model validation under Pydantic v2 guidelines
    validated_config = LlamaParseConfig.model_validate(config_data)
    print(f"Validated parsing instruction: '{validated_config.parsing_instruction[:30]}...'")

    # Initialize parser with validated config parameters
    parser = LlamaParse(
        api_key=validated_config.api_key,
        result_type=validated_config.result_type,
        parsing_instruction=validated_config.parsing_instruction,
        gpt4o_mode=validated_config.gpt4o_mode,
        premium_mode=validated_config.premium_mode,
    )

    # documents = parser.load_data("complex_report.pdf")
except Exception as e:
    print(f"Configuration validation failed: {e}")
```

## Related tools / concepts
- [Unstructured.io](unstructured.md) — Alternative document partitioning tool.
- [Docling](../process_understanding/docling.md) — Fast local document parser.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — The primary framework for LlamaParse.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Architecture utilizing parsed output.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for agent-tool communication (FastMCP v3.1).
- [Claude 5.1](../providers/anthropic.md) — Recommended model for reasoning over parsed data.
- [GPT-5.5](../ai_knowledge/openai.md) — High-performance alternative for document synthesis.
- [Llama 4](../ai_knowledge/local_llms.md) — Local model for processing LlamaParse outputs.

## Sources / references
- [LlamaParse (LlamaIndex)](https://www.llamaindex.ai/llamaparse)
- [LlamaParse API Reference](https://docs.cloud.llamaindex.ai/api-reference)
- [LlamaParse MCP: Agentic OCR tools](https://www.llamaindex.ai/blog/llamaparse-mcp-the-tooling-layer-for-your-document-agents)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
