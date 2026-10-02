# MinIO

## What it is
MinIO is a high-performance, Kubernetes-native, S3-compatible object storage suite designed for enterprise AI/ML data infrastructure, high-concurrency data lakes, and private cloud deployments. Written in Go and optimized with assembly micro-kernels for SIMD instructions (AVX-512, ARM NEON), MinIO delivers wire-speed S3 API performance. It allows organizations to deploy on-premises or private cloud object stores with complete control over data sovereignty, encryption, and lifecycle management.

In autonomous agent architectures and FastMCP 3.1 ecosystems, MinIO acts as the central **S3 Data Lake and Storage Gateway**. It provides durable storage for unstructured datasets, RAG vector index snapshots, GGUF model weights, training checkpoints, and media files while serving webhooks and bucket event notifications for real-time automation.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Autonomous Agent & Application Workflows                         │
│       (FastMCP 3.1 Tools, LangGraph Agents, n8n Automation, PyTorch Pipelines)         │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                             Amazon S3 REST API (HTTP / HTTPS)
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                             MinIO High-Performance Server                              │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Amazon S3 Compatibility API Gateway (REST, Pre-Signed URLs, Multipart Uploads)   │  │
│  ├──────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Erasure Coding Engine & Bitrot Protection (Reed-Solomon Data/Parity Sharding)    │  │
│  ├──────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Event Notification Engine (AMQP, Kafka, Webhooks, NATS, PostgreSQL Triggers)     │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Direct NVMe / Block Disk I/O
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                            Distributed Storage Infrastructure                          │
│        [ Multi-Node NVMe Drives / Direct-Attached Disks / Kubernetes PVs ]            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
Managing large-scale unstructured datasets for AI/ML and enterprise applications on public cloud infrastructure introduces significant security and operational challenges:
1. **Public Cloud Egress Costs & Lock-in**: Transferring multi-terabyte datasets or model weights into and out of public cloud S3 buckets generates massive data egress bills and creates cloud vendor lock-in.
2. **Data Sovereignty & Strict Privacy Compliance**: Regulatory mandates (GDPR, HIPAA, SOC 2, HIPAA) frequently prohibit storing sensitive customer data, medical scans, or proprietary financial records on multi-tenant public cloud infrastructure.
3. **High Latency for Local Fine-Tuning**: Loading large model weights (e.g. 70B parameter models) or streaming training datasets across remote WAN networks creates severe GPU idle time. MinIO on local NVMe arrays achieves hundreds of GB/s local read throughput.
4. **Data Corruption & Drive Failures**: Traditional RAID controllers struggle with drive rebuild times for multi-terabyte drives. MinIO's inline Reed-Solomon erasure coding and continuous bitrot verification guarantee high durability without hardware RAID dependencies.

## Where it fits in the stack
MinIO operates in the **Intake & Storage** layer of modern AI and data engineering architectures. It serves as the primary object storage backend for raw data ingestion, model artifact versioning, and RAG vector store persistence.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             Data Ingestion & Ingestion Sources                         │
│           [ Web Crawlers, IoT Sensors, Paperless Scans, External API Logs ]            │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ S3 Object Writes
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              MinIO Local Enterprise Storage                            │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Buckets: `ai-datasets`, `model-weights`, `rag-embeddings`, `backups`             │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    │ Bucket Webhook Events                         │ S3 Read Requests
                    ▼                                               ▼
┌───────────────────────────────────────┐       ┌────────────────────────────────────────┐
│    FastMCP 3.1 & Event Processors     │       │     Model Training & Inference         │
│ (Trigger Document Parsing & Vector)   │       │  (vLLM, Ollama, PyTorch, Llamafile)    │
└───────────────────────────────────────┘       └────────────────────────────────────────┘
```

## Typical use cases
- **AI/ML Data Lake & Model Registry**: Storing petabyte-scale training datasets (JSONL, Parquet, ImageNet) and serving model checkpoints to local training nodes or inference servers.
- **Agentic Model Management**: Enabling autonomous AI agents via FastMCP 3.1 tools to programmatically store, version, and download fine-tuned GGUF weights, evaluation reports, and code artifacts.
- **Private S3 Storage for Enterprise Apps**: Serving as the primary S3-compatible backend for self-hosted services like [Nextcloud](../../services/nextcloud.md), [Gitea](../../services/gitea.md), [Authentik](../../services/authentik.md), and [Paperless-ngx](../../services/paperless-ngx.md).
- **Immutable Security & Audit Logging**: Configuring Object Lock (WORM - Write Once Read Many) for compliance log archives, protecting audit logs against ransomware modification or deletion.

## Strengths
- **100% Amazon S3 API Compatibility**: Complete compatibility with S3 SDKs (`boto3`, `@aws-sdk/client-s3`, Go SDK) and tools (`aws-cli`, `rclone`, `mc`).
- **High Read/Write Performance**: Reaches multi-gigabyte-per-second throughput per node on NVMe storage, leveraging SIMD assembly acceleration for encryption and checksum calculations.
- **Flexible Erasure Coding Durability**: Configurable per-bucket Reed-Solomon data and parity drive ratios, surviving multiple simultaneous drive or node failures without data loss.
- **Active Event Notifications**: Native real-time event triggers sent to Webhooks, Kafka, AMQP, MQTT, NATS, or PostgreSQL upon object creation or deletion.
- **Enterprise Security Suite**: Native Server-Side Encryption (SSE-S3, SSE-KMS via HashiCorp Vault), OIDC/OAuth2/Active Directory authentication, and IAM fine-grained access policies.

## Limitations
- **High Memory Requirements for Large Clusters**: Distributed deployments require significant host RAM per node for caching metadata and tracking erasure code blocks.
- **Not a POSIX Shared File System**: Object storage is optimized for whole-object read/write operations; random byte modifications inside small files require full object replacement (unlike NFS/SMB).
- **Cluster Expansion Complexity**: Expanding existing storage pools requires adding drives in matching pool multiples (erasure sets).

## When to use it
- When you require **high-performance, on-premises S3 object storage** for AI model training, datasets, or vector databases.
- For air-gapped enterprise environments where data privacy laws mandate zero external cloud connectivity.
- When building event-driven pipelines where object uploads trigger automated processing workflows via webhooks or FastMCP 3.1 servers.

## When not to use it
- For basic end-user file sharing and desktop document syncing — use [Nextcloud](../../services/nextcloud.md).
- For small multi-tenant web applications requiring simple low-cost cloud storage — use managed S3-compatible cloud providers like Backblaze B2 or Storj.
- For high-transaction SQL relational databases requiring low-latency random block disk writes (use PostgreSQL or NVMe block volumes).

## Getting started

### Single-Node Docker Deployment
Run a single-node MinIO instance with the web console enabled:

```bash
docker run -d \
  --name minio-server \
  -p 9000:9000 \
  -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadminpassword" \
  -v /mnt/minio_data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

### Accessing the Web Console
1. Open `http://localhost:9001` in your browser.
2. Log in using credentials `minioadmin` / `minioadminpassword`.
3. Create a bucket named `ai-models` and generate a set of API Access/Secret Keys under **Identity > Service Accounts**.

## CLI examples

### MinIO Client (`mc`) Bucket Management
The `mc` CLI provides administrative control over MinIO clusters and S3 endpoints:

```bash
# Configure local server alias
mc alias set myminio http://localhost:9000 minioadmin minioadminpassword

# Create a bucket with versioning and object locking enabled
mc mb myminio/ai-datasets --with-lock

# Mirror local dataset directory to MinIO with continuous sync
mc mirror --follow --watch ./local_datasets myminio/ai-datasets

# Generate a pre-signed download URL valid for 2 hours
mc share download myminio/ai-datasets/finetune_v1.jsonl --expire 2h

# Set a lifecycle policy to transition objects older than 30 days to cold tier
mc ilm add myminio/ai-datasets --expiry-days 30
```

### Configuring Event Notifications to Webhooks
```bash
# Register a target HTTP webhook endpoint
mc admin config set myminio notify_webhook:1 \
    endpoint="http://127.0.0.1:8000/minio-webhook" \
    queue_limit="1000"

# Restart MinIO service to apply configuration
mc admin service restart myminio

# Subscribe the webhook target to s3:ObjectCreated events on 'ai-datasets' bucket
mc event add myminio/ai-datasets arn:minio:sqs::1:webhook --event put
```

## API examples

### FastMCP 3.1 & Pydantic v2 MinIO Bucket Management Server
The following production Python service implements a **FastMCP 3.1** server for managing MinIO object storage. It uses **Pydantic v2** schema validation to handle presigned URL generation, dataset uploads, lifecycle policy enforcement, and bucket metadata audits.

```python
"""
MinIO FastMCP 3.1 Storage Gateway Server
Exposes high-performance S3 object storage operations, dataset management,
and pre-signed URL generation for autonomous AI agent pipelines.
"""

import os
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import boto3
from botocore.client import Config
from pydantic import BaseModel, Field, field_validator, HttpUrl, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("MinIO-Storage-Gateway", version="3.1.0")

# ---------------------------------------------------------------------------
# Pydantic v2 Validation Schemas
# ---------------------------------------------------------------------------

class MinioConnectionConfig(BaseModel):
    """Configuration schema for target MinIO S3 endpoint."""
    endpoint_url: HttpUrl = Field(default="http://127.0.0.1:9000", description="MinIO server URL")
    access_key: str = Field(..., min_length=3, description="MinIO access key ID")
    secret_key: str = Field(..., min_length=8, description="MinIO secret access key")
    region: str = Field(default="us-east-1")
    use_ssl: bool = Field(default=False)

class BucketCreationRequest(BaseModel):
    """Request payload for creating a new S3 bucket."""
    bucket_name: str = Field(..., min_length=3, max_length=63, description="Target bucket name")
    enable_versioning: bool = Field(default=True)
    enable_object_lock: bool = Field(default=False)

    @field_validator("bucket_name")
    @classmethod
    def validate_bucket_naming(cls, v: str) -> str:
        if not v.islower() or "_" in v:
            raise ValueError("Bucket names must consist only of lowercase letters, numbers, and hyphens.")
        return v

class PresignedUrlRequest(BaseModel):
    """Request payload for generating a pre-signed URL."""
    bucket_name: str = Field(..., min_length=3, max_length=63)
    object_name: str = Field(..., min_length=1, description="Object key path")
    expiration_seconds: int = Field(default=3600, ge=60, le=86400, description="Expiration time in seconds")
    operation: str = Field(default="get_object", description="'get_object' or 'put_object'")

class ObjectMetadata(BaseModel):
    """Structured object item description."""
    object_name: str
    size_bytes: int = Field(..., ge=0)
    last_modified: datetime
    etag: str
    content_type: str = Field(default="application/octet-stream")

class StorageOperationResponse(BaseModel):
    """Unified response envelope for storage operations."""
    status: str = Field(..., description="'success' or 'error'")
    operation: str
    bucket_name: str
    details: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: float = Field(..., ge=0.0)
    error_message: Optional[str] = Field(default=None)

# ---------------------------------------------------------------------------
# Core MinIO S3 Client
# ---------------------------------------------------------------------------

class MinioStorageClient:
    """Wrapper client managing MinIO S3 operations using boto3."""

    def __init__(self, config: MinioConnectionConfig):
        self.config = config
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=str(config.endpoint_url),
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            region_name=config.region,
            config=Config(signature_version="s3v4"),
            verify=config.use_ssl
        )

    def create_bucket(self, req: BucketCreationRequest) -> StorageOperationResponse:
        start_time = time.perf_counter()
        try:
            self.s3_client.create_bucket(Bucket=req.bucket_name)

            if req.enable_versioning:
                self.s3_client.put_bucket_versioning(
                    Bucket=req.bucket_name,
                    VersioningConfiguration={"Status": "Enabled"}
                )

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return StorageOperationResponse(
                status="success",
                operation="create_bucket",
                bucket_name=req.bucket_name,
                details={"versioning": req.enable_versioning},
                latency_ms=round(elapsed_ms, 2)
            )
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return StorageOperationResponse(
                status="error",
                operation="create_bucket",
                bucket_name=req.bucket_name,
                latency_ms=round(elapsed_ms, 2),
                error_message=str(err)
            )

    def generate_presigned_url(self, req: PresignedUrlRequest) -> StorageOperationResponse:
        start_time = time.perf_counter()
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod=req.operation,
                Params={"Bucket": req.bucket_name, "Key": req.object_name},
                ExpiresIn=req.expiration_seconds
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return StorageOperationResponse(
                status="success",
                operation="generate_presigned_url",
                bucket_name=req.bucket_name,
                details={"presigned_url": url, "expires_in": req.expiration_seconds},
                latency_ms=round(elapsed_ms, 2)
            )
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return StorageOperationResponse(
                status="error",
                operation="generate_presigned_url",
                bucket_name=req.bucket_name,
                latency_ms=round(elapsed_ms, 2),
                error_message=str(err)
            )

# ---------------------------------------------------------------------------
# FastMCP Tool Registrations
# ---------------------------------------------------------------------------

@mcp.tool(
    name="minio_create_bucket",
    description="Create a new S3-compatible storage bucket in local MinIO cluster with optional versioning."
)
def minio_create_bucket(
    bucket_name: str,
    enable_versioning: bool = True,
    endpoint_url: str = "http://127.0.0.1:9000",
    access_key: str = "minioadmin",
    secret_key: str = "minioadminpassword"
) -> Dict[str, Any]:
    """MCP tool wrapping MinIO bucket creation."""
    try:
        conn_cfg = MinioConnectionConfig(
            endpoint_url=HttpUrl(endpoint_url),
            access_key=access_key,
            secret_key=secret_key
        )
        req = BucketCreationRequest(bucket_name=bucket_name, enable_versioning=enable_versioning)
        client = MinioStorageClient(conn_cfg)
        res = client.create_bucket(req)
        return res.model_dump()
    except ValidationError as val_err:
        return {
            "status": "error",
            "operation": "create_bucket",
            "bucket_name": bucket_name,
            "latency_ms": 0.0,
            "error_message": f"Validation error: {str(val_err)}"
        }

@mcp.tool(
    name="minio_generate_presigned_url",
    description="Generate a pre-signed S3 URL for secure direct object download or upload."
)
def minio_generate_presigned_url(
    bucket_name: str,
    object_name: str,
    expiration_seconds: int = 3600,
    operation: str = "get_object",
    endpoint_url: str = "http://127.0.0.1:9000",
    access_key: str = "minioadmin",
    secret_key: str = "minioadminpassword"
) -> Dict[str, Any]:
    """MCP tool for pre-signed URL generation."""
    try:
        conn_cfg = MinioConnectionConfig(
            endpoint_url=HttpUrl(endpoint_url),
            access_key=access_key,
            secret_key=secret_key
        )
        req = PresignedUrlRequest(
            bucket_name=bucket_name,
            object_name=object_name,
            expiration_seconds=expiration_seconds,
            operation=operation
        )
        client = MinioStorageClient(conn_cfg)
        res = client.generate_presigned_url(req)
        return res.model_dump()
    except ValidationError as val_err:
        return {
            "status": "error",
            "operation": "generate_presigned_url",
            "bucket_name": bucket_name,
            "latency_ms": 0.0,
            "error_message": f"Validation error: {str(val_err)}"
        }

if __name__ == "__main__":
    # Launch FastMCP server over standard I/O streams
    mcp.run()
```

## Storage Architecture & Erasure Coding Matrix

### MinIO Erasure Coding (Reed-Solomon)
MinIO divides stored objects into data ($N$) and parity ($M$) blocks distributed across drives within an erasure set. The default parity ratio ($EC:4$) allows the cluster to lose up to 4 drives per set without data loss or service downtime.

| Erasure Setting (Parity / Data) | Drive Storage Overhead | Fault Tolerance (Drives Lost) | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| **EC:2** (14 Data, 2 Parity) | 12.5% Overhead | Up to 2 drives per set | Non-critical temporary scratch data / caching |
| **EC:4** (12 Data, 4 Parity) | 33.3% Overhead | Up to 4 drives per set | Standard enterprise AI datasets & model weights |
| **EC:8** (8 Data, 8 Parity) | 100.0% Overhead | Up to 8 drives per set | Mission-critical financial records & legal archives |

### NVMe Throughput Optimization Checklist
To achieve maximum read throughput (> 100 GB/s) for GPU model loading:
1. **Enable Direct I/O (`O_DIRECT`)**: Ensure raw storage mount points bypass OS filesystem page caching to eliminate CPU memory copy overhead.
2. **Network Card Bonding & SR-IOV**: Bind dual 100GbE / 200GbE NICs using LACP (802.3ad) to prevent network bottlenecks during distributed dataset streaming.
3. **RAM Sizing**: Allocate at least 2 GB RAM per NVMe drive for caching drive block descriptors and metadata.

## Production Operational Runbook & Health Auditing

### Cluster Health Monitoring Commands
```bash
# Check overall cluster hardware health and drive status
mc admin info myminio

# Run drive performance benchmark across all cluster nodes
mc admin speedtest myminio --size 10GiB

# Audit bitrot health and run background healing
mc admin heal myminio --recursive
```

### Systemd Production Unit Configuration
For bare-metal production nodes, deploy MinIO under a restricted systemd service `/etc/systemd/system/minio.service`:

```ini
[Unit]
Description=MinIO High-Performance Enterprise Object Storage
Documentation=https://docs.min.io
After=network.target

[Service]
Type=simple
User=minio-user
Group=minio-user
LimitNOFILE=65536
ExecStart=/usr/local/bin/minio server /mnt/drive{1...4}/minio --console-address ":9001"
Restart=always
RestartSec=10

# Security Hardening
ProtectSystem=full
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now minio
```

## Related tools / concepts
- [Storj](../../services/storj.md) — Decentralized S3-compatible cloud storage alternative.
- [rclone Automation](../../services/rclone-automation.md) — Command-line data sync tool for moving data to/from MinIO.
- [Nextcloud](../../services/nextcloud.md) — Enterprise file collaboration suite utilizing MinIO as primary storage.
- [Authentik](../../services/authentik.md) — Identity management provider providing OIDC SSO for MinIO Console.
- [Gitea](../../services/gitea.md) — Self-hosted Git server using MinIO for LFS and artifact storage.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system archiving documents into MinIO buckets.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Real-time agentic storage orchestration protocol.

## Sources / references
- [MinIO Official Website](https://min.io/)
- [MinIO Server & Client Documentation](https://min.io/docs/minio/linux/index.html)
- [MinIO GitHub Repository](https://github.com/minio/minio)
- [MinIO High-Performance Benchmark Reports](https://www.min.io/blog/blackwell-storage-performance)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
