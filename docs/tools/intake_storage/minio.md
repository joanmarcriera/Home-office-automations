# MinIO

## What it is
MinIO is a high-performance, S3-compatible object storage server. It is purpose-built for large-scale AI/ML data infrastructure, high-concurrency workloads, and cloud-native applications.

## What problem it solves
It provides a way to host your own S3-compatible storage on-premises or in private clouds, offering the same API as Amazon S3 but with full control over the infrastructure, data sovereignty, and cost.

## Where it fits in the stack
**Intake & Storage**. It acts as the primary object storage layer for unstructured data like images, videos, log files, model artifacts, and vector database snapshots.

## Typical use cases
- **AI/ML Data Lake**: Storing large datasets (Terabytes to Petabytes) for AI model training and fine-tuning.
- **Self-Hosted Backend**: Providing S3-compatible storage for applications like [Nextcloud](../../services/nextcloud.md), [Gitea](../../services/gitea.md), or [Authentik](../../services/authentik.md).
- **Private Cloud Infrastructure**: Building a scalable data layer for enterprise Kubernetes clusters.
- **Backup Target**: Serving as a high-durability target for [rclone Automation](../../services/rclone-automation.md) or specialized backup software.

## Key Features (May 2026 Update)
- **Object Lambda**: Perform on-the-fly data transformations (e.g., PII redaction, image resizing, format conversion) using custom Python or Go functions triggered during `GET` requests.
- **AI Hub Integration**: Native support for managing LLM weights and dataset versioning with built-in observability for AI training pipelines.
- **Global Console**: Centralized management for distributed MinIO clusters across different geographic regions.
- **Erasure Coding & Bitrot Protection**: High-durability data protection that allows for the loss of multiple drives without data loss.

## Strengths
- **Extreme Performance**: Capable of hundreds of GB/s throughput, making it ideal for GPU-accelerated workloads.
- **100% S3 Compatibility**: Seamlessly switch between AWS S3 and MinIO without changing application code.
- **Security-First**: Integrated encryption (SSE-S3, SSE-KMS), Identity Management (OIDC, AD/LDAP), and object locking (WORM).
- **Active-Active Replication**: Built-in multi-site replication for disaster recovery.

## Limitations
- **Infrastructure Management**: High-performance multi-node clusters require expertise in networking and storage hardware.
- **Not a File System**: While `rclone mount` exists, MinIO is not a replacement for high-performance block storage or traditional NAS (NFS/SMB) for small files.

## When to use it
- When you need high-performance object storage for AI/ML or production applications.
- For local development where you need a reliable S3 API.
- When data residency and sovereignty are critical requirements.

## When not to use it
- For simple document sharing among non-technical users (use [Nextcloud](../../services/nextcloud.md)).
- If you only need a few hundred GBs and prefer a managed service (consider [Storj](../../services/storj.md)).

## Licensing and cost
- **Open Source**: GNU AGPLv3 (Community Edition).
- **Enterprise**: Commercial license available for additional security, management tools, and support.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Storj](../../services/storj.md): Decentralized S3-compatible storage.
- [rclone Automation](../../services/rclone-automation.md): The "Swiss Army Knife" for moving data to/from MinIO.
- [S3 Compatible Providers](../providers/index.md): Comparison of S3-based storage options.

## Getting started

### Docker (Single Node)
Run a single-node MinIO server with the Console enabled:

```bash
docker run -p 9000:9000 -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=password123" \
  -v /mnt/data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

### Quick Setup
1. Open `http://localhost:9001` (MinIO Console).
2. Login with `admin` / `password123`.
3. Create a bucket named `ai-models`.
4. Upload a sample file to verify functionality.

## CLI examples
The `mc` (MinIO Client) is a powerful tool for managing any S3-compatible storage.

```bash
# Add a local server alias
mc alias set myminio http://localhost:9000 admin password123

# Create a bucket with versioning enabled
mc mb myminio/backups --with-versioning

# Mirror a directory with progress tracking
mc mirror --follow --watch ./datasets myminio/datasets

# Find files older than 30 days and remove them
mc rm --recursive --older-than 30d myminio/logs/
```

## API examples

### Python (Boto3)
Standard S3 library integration.

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password123"
)

# List all buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(f'Bucket: {bucket["Name"]}')
```

### Python (Object Lambda Example)
Registering a webhook for on-the-fly transformation.

```python
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/transform', methods=['POST'])
def transform_object():
    event = request.json
    s3_url = event["getObjectContext"]["inputS3Url"]

    # Fetch original object
    r = requests.get(s3_url)
    data = r.text

    # Simple transformation: Reverse text
    transformed_data = data[::-1]

    return transformed_data

if __name__ == "__main__":
    app.run(port=5000)
```

## Sources / References
- [Official Website](https://min.io/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [MinIO GitHub](https://github.com/minio/minio)
- [Object Lambda Blog Post](https://www.min.io/blog/minio-object-lambda)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
