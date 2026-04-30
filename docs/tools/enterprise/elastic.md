# Elastic (Elasticsearch)

## What it is
A distributed, RESTful search and analytics engine capable of addressing a growing number of use cases, including vector search and generative AI integration.

## What problem it solves
Provides a powerful and flexible infrastructure for searching, analyzing, and visualizing data in real-time. It is the foundation for many RAG (Retrieval-Augmented Generation) implementations.

## Where it fits in the stack
**Category**: Enterprise AI / Search & Infrastructure

## Typical use cases
- **Application Search**: Building custom search experiences into applications.
- **Log Analytics**: Centralizing and analyzing system logs (often as part of the ELK stack).
- **Vector Search for RAG**: Storing and retrieving vector embeddings for LLM-powered applications.

## Strengths
- **Massive Scalability**: Designed to handle petabytes of data across distributed clusters.
- **Versatile**: Supports full-text search, structured search, and vector search.
- **Mature Ecosystem**: Large community, extensive documentation, and many third-party integrations.

## Limitations
- **Operational Complexity**: Running and tuning a large Elastic cluster requires specialized knowledge.
- **Resource Intensive**: Requires significant RAM and CPU for high performance.

## When to use it
- When you need a highly scalable, customizable search backend.
- When building complex RAG pipelines that require hybrid search (vector + keyword).

## When not to use it
- For very simple search needs where a managed service or lighter database would suffice.
- If you don't have the resources to manage the underlying infrastructure.

## Licensing and cost
- **Open Source**: Elastic License (Source-available) / Paid (Elastic Cloud)
- **Cost**: Free (Self-hosted) / Paid (Managed service)
- **Self-hostable**: Yes

## Related tools / concepts
- [Coveo](coveo.md)
- [Supabase](../infrastructure/supabase.md)
- [Vector Databases](../../knowledge_base/patterns/rag.md)

## Sources / references
- [Elastic Official Site](https://www.elastic.co/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
