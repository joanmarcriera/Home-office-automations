# Manual Assistant Troubleshooting Backend

Reference implementation for a RAG-based backend to search and answer questions from household manuals.

## What it is
A FastAPI-based backend that integrates with ChromaDB to perform hybrid (vector + metadata filtered) search across OCR'd manuals and provides an interface for LLM-based troubleshooting.

## What problem it solves
It centralizes the "brain" for the [AI-Powered Warranty & Manual Assistant](../../roadmap.md), allowing users to ask natural language questions like "How do I clean the filter on my Bosch dishwasher?" and get answers directly from the scanned PDF.

## Where it fits in the stack
- **Upstream**: Paperless-ngx (source of PDFs), `scripts/process_manuals.py` (ingestion to ChromaDB).
- **This Layer**: API for searching and LLM orchestration.
- **Downstream**: Streamlit or Open WebUI (frontend for family use).

## Typical use cases
- Troubleshooting appliance error codes.
- Finding maintenance schedules in manuals.
- Verifying warranty terms for specific products.

## Strengths
- **Metadata Filtering**: Quickly narrows search to the correct manufacturer/model.
- **Async Execution**: Built on FastAPI for high performance.
- **Decoupled**: Can be used by multiple frontends (web, mobile, voice).

## Limitations
- Requires pre-indexed manuals in ChromaDB.
- Accuracy depends heavily on OCR quality from Paperless-ngx.

## When to use it
When you want to build a custom chat interface for your homelab that goes beyond simple keyword search in Paperless-ngx.

## When not to use it
If you only have a few manuals; simple full-text search in Paperless-ngx might be sufficient.

## Related tools / concepts
- [ChromaDB](../../docs/knowledge_base/vector-db-comparison.md)
- [scripts/process_manuals.py](../../scripts/process_manuals.py)

## Sources / References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## Contribution Metadata
- Last reviewed: 2025-05-20
- Confidence: high
