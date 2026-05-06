# MinIO

## What it is
MinIO is a high-performance, S3-compatible object storage server. It is built for large-scale AI/ML data infrastructure and cloud-native applications.

## What problem it solves
It provides a way to host your own S3-compatible storage on-premises or in private clouds, offering the same API as Amazon S3 but with full control over the infrastructure and data.

## Where it fits in the stack
**Intake & Storage**. It acts as the object storage layer for storing unstructured data like images, videos, log files, and model artifacts.

## Typical use cases
- Storing large datasets for AI model training.
- Providing S3-compatible storage for self-hosted applications (e.g., Nextcloud, GitLab).
- Building a private "data lake" for enterprise analytics.
- Serving as a backup target for various systems.

## Strengths
- High performance (capable of hundreds of gigabytes per second).
- 100% S3 compatible API.
- Cloud-native and container-friendly.
- Built-in data protection (Erasure Coding, Bitrot protection).

## Limitations
- Managing large clusters requires significant infrastructure knowledge.
- Not a block storage or file system replacement (optimized for object storage).

## When to use it
- When you need high-performance object storage and want to avoid cloud lock-in.
- For local development where you need an S3 API without paying for AWS.

## When not to use it
- For simple file sharing (consider [Nextcloud](../../services/nextcloud.md) or [Syncthing](../../services/syncthing.md)).
- If you only need a small amount of storage and prefer a managed service (consider [Storj](../../services/storj.md) or Amazon S3).

## Licensing and cost
- **Open Source**: Yes (GNU AGPLv3)
- **Cost**: Free (Community), Paid (Enterprise Support)
- **Self-hostable**: Yes

## Related tools / concepts
- [Storj](../../services/storj.md)
- [rclone Automation](../../services/rclone-automation.md)
- [S3 Compatible Providers](../providers/index.md)

## Getting started

### Docker
Run a single-node MinIO server using Docker:

```bash
docker run -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  -v /mnt/data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

### Hello World
1. Access the MinIO Console at `http://localhost:9001`.
2. Log in with the `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` defined above.
3. Click **Create Bucket** and name it `test-bucket`.
4. Click **Upload** to add a file to your new bucket.
5. You now have a functional S3-compatible storage server!

## CLI examples
The `mc` (MinIO Client) tool is the standard way to manage MinIO and other S3-compatible services.

```bash
# Add a server alias
mc alias set myminio http://localhost:9000 AKIAIOSFODNN7EXAMPLE wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# List buckets
mc ls myminio

# Mirror a local directory to a bucket
mc mirror ./my-local-data myminio/test-bucket

# Set an anonymous policy (public read) on a bucket
mc anonymous set download myminio/test-bucket
```

## API examples
Use the `boto3` library (Python) or the official MinIO SDKs.

### Python (Boto3)
```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
)

# Upload a file
s3.upload_file("test.txt", "test-bucket", "test.txt")

# Download a file
s3.download_file("test-bucket", "test.txt", "downloaded_test.txt")
```

## Sources / References
- [Official Website](https://min.io/)
- [Documentation](https://min.io/docs/minio/linux/index.html)
- [MinIO GitHub](https://github.com/minio/minio)

## Contribution Metadata
- Last reviewed: 2026-04-28
- Confidence: high
