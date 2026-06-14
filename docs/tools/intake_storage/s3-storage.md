# S3 / S3-Compatible Storage

## What it is
S3 (Simple Storage Service) is a scalable object storage service pioneered by AWS. "S3-compatible" refers to other storage services and software (like Cloudflare R2, MinIO, or Google Cloud Storage) that use the same API for data management.

## What problem it solves
It provides virtually unlimited, durable, and highly available storage for unstructured data (images, videos, documents, backups, and logs). It allows AI agents and applications to store and retrieve data from any location via simple HTTP/HTTPS calls, serving as the primary "data lake" for agentic workflows.

## Where it fits in the stack
**Intake & Storage / Object Storage**. It acts as the foundational persistence layer for raw intake data and agent traces before they are processed into vector databases or knowledge bases.

## Typical use cases
- **AI Log Storage**: Storing raw traces and JSON logs from AI providers like [OpenRouter](../ai_knowledge/openrouter.md).
- **RAG Data Lakes**: Hosting the original PDF, Word, and HTML documents used in retrieval-augmented generation.
- **Model Checkpoint Storage**: Saving and versioning large LLM weights and fine-tuning artifacts for Llama 4 or Mistral.
- **Data Backups**: Storing automated backups of home-office services and knowledge bases.
- **Agent Memory Persistence**: Saving long-term context files for frontier models like `claude-4-8-opus-20260528`.

## Strengths
- **Extreme Scalability**: Handles everything from a few bytes to petabytes of data.
- **High Durability**: Designed for 99.999999999% (11 nines) of durability.
- **Industry Standard API**: The S3 API is supported by almost every AI tool and framework, including LangChain, LlamaIndex, and AutoGen.
- **Cost-Effective**: Pay-as-you-go pricing with tiered storage options (Hot, Cold, Archive).
- **Interoperability**: Easily integrates with compute layers for data processing and inference.

## Limitations
- **Object Latency**: Not suitable for applications requiring extremely low-latency block storage (e.g., high-performance databases).
- **Complexity at Scale**: Managing access policies (IAM), versioning, and lifecycle rules can become complex as the data lake grows.
- **Data Egress Costs**: Cloud providers often charge for data transferred out of their network.

## When to use it
- When you need a highly scalable, durable place to store large amounts of unstructured AI data (logs, datasets, media).
- For cross-tool data sharing where multiple agents or services need to read/write to a common storage layer via a standard API.
- If you want a cost-effective, tiered storage solution that can archive older data automatically.
- As the backend for [Paperless-ngx](../../services/paperless-ngx.md) or other document management systems.

## When not to use it
- For high-frequency, low-latency database operations (use a relational database or NoSQL instead).
- If you have zero connectivity to cloud services and need purely local, file-system based storage for a single machine (use local SSDs).
- For structured data that requires complex querying and indexing (use [Supabase](../infrastructure/supabase.md) or [PostgreSQL](../../services/postgresql.md)).

## Getting started

### OpenRouter Broadcast Configuration
OpenRouter can stream each AI interaction as a separate JSON file to an S3 bucket.

- **Path Template**: `openrouter-traces/{year}/{month}/{day}/{traceId}.json`
- **File Format**: Each file contains the full trace including prompt, response, model, and cost.

### R2 Setup (Cloudflare)
Cloudflare R2 is a popular S3-compatible choice due to zero egress fees.
1. Create a bucket in the Cloudflare dashboard.
2. Generate an API token with "Object Read & Write" permissions.
3. Use the provided S3 endpoint in your tools.

## CLI examples

```bash
# Upload a file to your AI data lake using AWS CLI
aws s3 cp my-logs.json s3://my-ai-bucket/logs/

# List daily traces
aws s3 ls s3://my-ai-bucket/openrouter-traces/2026/06/12/

# Download a specific trace for local analysis
aws s3 cp s3://my-ai-bucket/openrouter-traces/2026/06/12/abc123.json .

# Sync a local directory of datasets to S3
aws s3 sync ./datasets/ s3://my-ai-bucket/datasets/
```

## API examples

### Python example (Boto3)
```python
import boto3
import json

# Initialize S3 client for an S3-compatible service (e.g., Cloudflare R2)
s3 = boto3.client(
    's3',
    endpoint_url='https://<account_id>.r2.cloudflarestorage.com',
    aws_access_key_id='<access_key>',
    aws_secret_access_key='<secret_key>'
)

# Fetch and parse an AI trace
bucket = 'my-ai-traces'
key = 'openrouter-traces/2026/06/12/example-trace.json'

response = s3.get_object(Bucket=bucket, Key=key)
trace_data = json.loads(response['Body'].read().decode('utf-8'))

print(f"Model used: {trace_data['model']}")
print(f"Total tokens: {trace_data['total_tokens']}")
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Streams logs directly to S3.
- [Unstructured.io](unstructured.md) — Often ingests raw data from S3 for processing.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system.
- [Rclone Automation](../../services/rclone-automation.md) — Tool for syncing data between providers.
- [Supabase](../infrastructure/supabase.md) — Provides an S3-compatible storage layer.
- [Snowflake](../process_understanding/snowflake.md) — Data warehouse that can ingest from S3.
- [ClickHouse](../process_understanding/clickhouse.md) — OLAP database with S3 integration.
- [Filesystem Context](../../knowledge_base/patterns/filesystem-context.md) — Pattern for giving agents access to files.

## Sources / references
- [AWS S3 Official Site](https://aws.amazon.com/s3/)
- [MinIO (Self-hosted S3)](https://min.io/)
- [OpenRouter S3 Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/s3)
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
