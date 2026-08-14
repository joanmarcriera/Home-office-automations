# Metadata Schema: Scanned Manuals

## What it is
A YAML-based and JSON-schema-validated metadata structure that defines the fields for indexing, tagging, and retrieving scanned household manuals. It ensures that technical documentation is stored with enough semantic context to be useful for both human reference and automated AI retrieval.

As of early January 2027, this schema enables frontier agents like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro/Flash** to navigate complex physical documents by providing a semantic "table of contents" and highly precise metadata anchors.

## What problem it solves
Scanned manuals are often large, unsearchable PDFs. Without a structured schema, finding specific information (like the "Troubleshooting" section or "Error Codes" for a specific dishwasher model) is highly inefficient. This schema enables "Section-Aware" indexing, making it possible for an AI agent to pinpoint exactly where the relevant information is located, reducing hallucinations and retrieval latency.

## Where it fits in the stack
The schema sits at the **Data Management Layer**. It is used by **Document Management Systems** (like Paperless-ngx) to organize files and by **Vector Databases** (like Chroma, Milvus, or Pinecone) to structure metadata for Retrieval-Augmented Generation (RAG).

## Typical use cases
- **Automated Troubleshooting**: An agent reads the "Error Codes" section of a manual to explain a blinking light on an appliance.
- **Maintenance Reminders**: Extracting service intervals from a car manual to create calendar events.
- **Home Inventory**: Building a digital twin of a home's appliances with direct links to their manuals.
- **Auto-Discovery**: MCP servers can expose tools to list all available manuals and their associated metadata (manufacturer, model) to autonomous agents.

## Strengths
- **Granularity**: Section-aware page ranges allow for precise retrieval of technical instructions.
- **Consistency**: Standardizes how model numbers and manufacturers are recorded across the entire library.
- **LLM-Friendly**: Structured metadata makes it easier for LLMs to filter results before reading content.
- **MCP Native**: Integrates with Model Context Protocol 3.1 and FastMCP 3.1 for querying via agentic tools.

## Limitations
- **Manual Effort**: Initially requires identifying page ranges for key sections (unless automated via VLM/OCR post-processing).
- **Schema Evolution**: May need updates as new types of appliances or specialized technical documents are added.
- **OCR Quality**: Reliability is strictly dependent on the quality of the underlying OCR (e.g., Tesseract vs. Omni Tools VLM).

## When to use it
- When building a "Household Manual RAG" system for local troubleshooting.
- For high-stakes appliances where troubleshooting speed is critical (HVAC, solar inverters, security systems).
- When digitizing a large physical library of paper manuals to ensure they remain actionable.

## When not to use it
- For simple, one-page quick start guides that don't have multiple sections.
- If the manufacturer provides a robust, searchable online portal that the agent can already access via a specialized MCP tool.
- For ephemeral or disposable product documentation.

## Getting started

### 1. Tagging in Paperless-ngx
Ensure the following custom fields and tags are configured:
- **Custom Fields**: `Manufacturer`, `Model Number`, `Product Name`.
- **Tags**: Apply the `Admin/Manual` tag to trigger the ingestion pipeline.

### 2. Ingestion Pipeline
Use the [process_manuals.py](../../scripts/process_manuals.py) script to extract text and sections. The script uses "Section-Aware" chunking where each section (e.g., "Troubleshooting") is treated as a coherent unit.

## CLI examples
Use the following commands to process and query manuals.

```bash
# Process a PDF manual and store in ChromaDB
python3 scripts/process_manuals.py /path/to/manual.pdf --output processed_manual.json --chroma-dir ./chroma_db

# Query the manuals database for a specific problem
python3 scripts/process_manuals.py --query "How do I clean the filter on my Bosch dishwasher?"

# Export metadata for a specific model
grep "SMS6ZCI42E" processed_manual.json -A 10
```

## API examples
The schema is typically defined in YAML and consumed by Python-based processors.

### Schema Definition (YAML)
```yaml
manual_metadata:
  document_type: "Manual"
  product_name: "String (e.g., 'Dishwasher Series 6')"
  manufacturer: "String (e.g., 'Bosch')"
  model_number: "String (e.g., 'SMS6ZCI42E')"
  year_of_manufacture: "Integer (optional)"
  language: "ISO 639-1 Code (e.g., 'en', 'de')"
  sections:
    - title: "String (e.g., 'Installation')"
      page_range: [start_page, end_page]
  tags:
    - "Admin/Manual"
    - "Appliance/Kitchen" # Example category
```

### Metadata Integration via Pydantic v2
Here is how the YAML metadata is parsed, validated, and embedded in the vector store:

```python
from typing import List, Tuple, Optional
from pydantic import BaseModel, Field, field_validator

class ManualSection(BaseModel):
    title: str = Field(..., description="Title of the section, e.g., 'Troubleshooting'")
    page_range: Tuple[int, int] = Field(..., description="Start and end page indices (0-based)")

    @field_validator('page_range')
    @classmethod
    def check_page_range(cls, v: Tuple[int, int]) -> Tuple[int, int]:
        if v[0] > v[1]:
            raise ValueError("Start page cannot be greater than end page")
        return v

class ManualMetadata(BaseModel):
    document_type: str = "Manual"
    product_name: str = Field(..., description="The name of the appliance/product")
    manufacturer: str = Field(..., description="The manufacturer name")
    model_number: str = Field(..., description="The appliance model number")
    year_of_manufacture: Optional[int] = Field(None, description="The manufacturing year")
    language: str = Field("en", description="ISO 639-1 code")
    sections: List[ManualSection] = Field(default_factory=list, description="Section coordinates")
    tags: List[str] = Field(default_factory=list, description="Associated taxonomic tags")
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The primary storage engine for these documents.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md): How this metadata is used to improve AI responses.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): The broader tagging system including `Admin/Manual`.
- [Warranty Extraction](../../reference-implementations/llm-prompts/warranty-extraction.md): A complementary schema for receipts and coverage.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The system that consumes this data.
- [n8n](../../services/n8n.md): Orchestrating the flow from scan to RAG database.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Multi-step processes for handling document intake.
- [Manual Processor Script](../../scripts/process_manuals.py): The reference implementation for PDF processing and vector storage.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): For querying manuals via agentic tools.

## Sources / References
- [Paperless-ngx Custom Fields](https://docs.paperless-ngx.com/usage/#custom-fields)
- [YAML Standard Specification](https://yaml.org/spec/1.2.2/)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
