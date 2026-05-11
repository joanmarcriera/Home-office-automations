# Metadata Schema: Scanned Manuals

## What it is
A YAML-based metadata schema that defines the structure for indexing, tagging, and retrieving scanned household manuals. It ensures that technical documentation is stored with enough context to be useful for both human reference and automated AI retrieval.

## What problem it solves
Scanned manuals are often large, unsearchable PDFs. Without a schema, finding specific information (like the "Troubleshooting" section for a specific dishwasher model) is difficult. This schema enables "Section-Aware" indexing, making it possible for an AI agent to pinpoint exactly where the relevant information is located.

## Where it fits in the stack
The schema sits at the **Data Management layer**. It is used by **Document Management Systems** (like Paperless-ngx) to organize files and by **Vector Databases** (like Chroma or Pinecone) to structure metadata for Retrieval-Augmented Generation (RAG).

## Typical use cases
- **Automated Troubleshooting**: An agent reads the "Error Codes" section of a manual to explain a blinking light on an appliance.
- **Maintenance Reminders**: Extracting service intervals from a car manual to create calendar events.
- **Home Inventory**: Building a digital twin of a home's appliances with direct links to their manuals.

## Strengths
- **Granularity**: Section-aware page ranges allow for precise retrieval.
- **Consistency**: Standardizes how model numbers and manufacturers are recorded across the library.
- **LLM-Friendly**: Structured metadata makes it easier for LLMs to filter results before reading content.

## Limitations
- **Manual Effort**: Initially requires identifying page ranges for key sections (unless automated via LLM).
- **Schema Evolution**: May need updates as new types of appliances or technical documents are added.

## When to use it
- When building a "Household Manual RAG" system.
- For high-stakes appliances where troubleshooting speed is critical (HVAC, security systems).
- When digitizing a large physical library of paper manuals.

## When not to use it
- For simple, one-page quick start guides.
- If the manufacturer provides a robust, searchable online portal that the agent can already access.

## Purpose
This schema defines how scanned household manuals should be tagged and indexed in Paperless-ngx and subsequently stored in a vector database for RAG.

## Schema (YAML)

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

## Implementation in Paperless-ngx
1. **Custom Fields**:
   - `Manufacturer`: Text
   - `Model Number`: Text
   - `Product Name`: Text
2. **Tags**: Apply the `Admin/Manual` tag to trigger the RAG ingestion pipeline.

## Ingestion Pipeline Logic
- **Chunking Strategy**: Use "Section-Aware" chunking. Each section (e.g., "Troubleshooting," "Maintenance") should be treated as a coherent unit.
- **Embedding Metadata**: Include `manufacturer` and `model_number` in every vector's metadata to allow filtered retrieval.

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The primary storage engine for these documents.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md): How this metadata is used to improve AI responses.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): The broader tagging system including `Admin/Manual`.
- [Warranty Extraction](../../reference-implementations/llm-prompts/warranty-extraction.md): A complementary schema for receipts and coverage.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The system that consumes this data.
- [n8n](../../services/n8n.md): Orchestrating the flow from scan to RAG database.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Multi-step processes for handling document intake.

## Sources / References
- [Paperless-ngx Custom Fields](https://docs.paperless-ngx.com/usage/#custom-fields)
- [YAML Standard](https://yaml.org/spec/1.2.2/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
