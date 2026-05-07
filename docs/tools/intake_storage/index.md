# Intake & Storage

The intake and storage layer is responsible for the extraction, transformation, and persistence of unstructured and semi-structured data. This layer ensures that documents (PDFs, images, logs, web content) are converted into formats that LLMs and agentic workflows can effectively consume.

## Core Capabilities

| Capability | Description | Core Tools |
| :--- | :--- | :--- |
| **Parsing & Extraction** | Converting complex PDFs, HTML, and office docs into clean Markdown/JSON. | [Unstructured.io](unstructured.md), [LlamaParse](llamaparse.md), [Docling](../process_understanding/docling.md) |
| **Object Storage** | Durable persistence for raw files and processed artifacts. | [S3 / S3-Compatible](s3-storage.md), [MinIO](minio.md) |
| **Hybrid Systems** | Integrated environments for personal knowledge management and search. | [AnyType](anytype.md), [Khoj](khoj.md), [SilverBullet](silverbullet.md) |
| **Database Sync** | Synchronizing specialized data types like calendars or journals. | [Caldav](caldav.md) |
| **Analytics Warehouses** | Columnar and cloud warehouses for logs, traces, and analytical workloads. | [ClickHouse](../process_understanding/clickhouse.md), [Snowflake](../process_understanding/snowflake.md) |

## Tool Selection Guidance

- **High-Volume ETL**: Use [Unstructured.io](unstructured.md) for its broad format support and local-first partitioning strategies.
- **Complex Documents**: Use [LlamaParse](llamaparse.md) when dealing with nested tables and multi-column layouts that require vision-aware parsing.
- **Privacy-First Search**: Use [Khoj](khoj.md) or [Verba](verba.md) for local-first RAG over personal document collections.
- **Standardized Object Store**: Use MinIO or AWS [S3](s3-storage.md) as the backbone for cross-service document access.

## Related Tools / Concepts

- [RAG Patterns](../../knowledge_base/patterns/rag.md)
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md)
- [Process & Understanding](../process_understanding/index.md)
- [Self-hosted Services](../../services/README.md)
- [Paperless-ngx](../../services/paperless-ngx.md)
