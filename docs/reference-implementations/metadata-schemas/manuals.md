# Metadata Schema: Scanned Manuals

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

## Sources / References
- [Paperless-ngx Custom Fields](https://docs.paperless-ngx.com/usage/#custom-fields)
- [RAG Best Practices](../../knowledge_base/patterns/rag.md)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
