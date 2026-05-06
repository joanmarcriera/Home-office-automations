# S3 / S3-Compatible Storage

## What it is
S3 (Simple Storage Service) is a scalable object storage service pioneered by AWS. "S3-compatible" refers to other storage services and software (like Cloudflare R2, MinIO, or Google Cloud Storage) that use the same API for data management.

## What problem it solves
It provides virtually unlimited, durable, and highly available storage for unstructured data (images, videos, documents, backups, and logs). It allows AI agents and applications to store and retrieve data from any location via simple HTTP/HTTPS calls.

## Where it fits in the stack
**Category**: Intake & Storage / Object Storage

## Typical use cases
- **AI Log Storage**: Storing raw traces and JSON logs from AI providers like OpenRouter.
- **RAG Data Lakes**: Hosting the original PDF, Word, and HTML documents used in retrieval-augmented generation.
- **Model Checkpoint Storage**: Saving and versioning large LLM weights and fine-tuning artifacts.
- **Data Backups**: Storing automated backups of home-office services and knowledge bases.

## Strengths
- **Extreme Scalability**: Handles everything from a few bytes to petabytes of data.
- **High Durability**: Designed for 99.999999999% (11 nines) of durability.
- **Industry Standard API**: The S3 API is supported by almost every AI tool and framework.
- **Cost-Effective**: Pay-as-you-go pricing with tiered storage options (Hot, Cold, Archive).

## Limitations
- **Object Latency**: Not suitable for applications requiring extremely low-latency block storage (e.g., databases).
- **Complexity at Scale**: Managing access policies (IAM), versioning, and lifecycle rules can become complex.
- **Data Egress Costs**: Cloud providers often charge for data transferred out of their network.

## Getting started

### OpenRouter Broadcast Configuration
OpenRouter can stream each AI interaction as a separate JSON file to an S3 bucket.

- **Path Template**: `openrouter-traces/{year}/{month}/{day}/{traceId}.json`
- **File Format**: Each file contains the full trace including prompt, response, model, and cost.

### CLI example (AWS CLI)
```bash
# Upload a file to your AI data lake
aws s3 cp my-logs.json s3://my-ai-bucket/logs/

# List daily traces
aws s3 ls s3://my-ai-bucket/openrouter-traces/2026/05/18/

# Download a specific trace
aws s3 cp s3://my-ai-bucket/openrouter-traces/2026/05/18/abc123.json .
```

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
key = 'openrouter-traces/2026/05/18/example-trace.json'

response = s3.get_object(Bucket=bucket, Key=key)
trace_data = json.loads(response['Body'].read().decode('utf-8'))

print(f"Model used: {trace_data['model']}")
print(f"Total tokens: {trace_data['total_tokens']}")
```

## Related tools / concepts
- [Unstructured.io](unstructured.md) (often ingests from S3)
- [OpenRouter](../ai_knowledge/openrouter.md) (can stream logs directly to S3)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Rclone Automation](../../services/rclone-automation.md)

## Sources / references
- [AWS S3 Official Site](https://aws.amazon.com/s3/)
- [MinIO (Self-hosted S3)](https://min.io/)
- [OpenRouter S3 Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/s3)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
